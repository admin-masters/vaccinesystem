from __future__ import annotations
from typing import Iterable, List, Tuple, Dict
from django.db import transaction
from django.utils import timezone

from .models import ScheduleVersion, VaccineDose, Child, ChildDose, VaccineEducationPatient, VaccineEducationDoctor
from .utils import birth_window, booster_window, series_window
from .utils_schedule import build_series_prev_maps

def current_schedule() -> ScheduleVersion | None:
    return (ScheduleVersion.objects.using("default")
            .filter(is_current=True)
            .order_by("-effective_from", "-created_at")
            .first())


def ensure_series_links(sv: ScheduleVersion | None = None) -> int:
    """
    Ensure every VaccineDose in a schedule is chained to its immediate predecessor
    within the same vaccine (sequence_index > 1). Returns number of links created.
    Safe to run repeatedly (idempotent).
    """
    sv = sv or current_schedule()
    if not sv:
        return 0

    doses = (VaccineDose.objects
             .filter(schedule_version=sv)
             .order_by("vaccine_id", "sequence_index", "id"))
    by_vax: Dict[int, List[VaccineDose]] = {}
    for vd in doses:
        by_vax.setdefault(vd.vaccine_id, []).append(vd)

    linked = 0
    with transaction.atomic():
        for vax_id, arr in by_vax.items():
            for i in range(1, len(arr)):
                cur = arr[i]
                prev = arr[i - 1]
                if cur.previous_dose_id is None:
                    VaccineDose.objects.filter(pk=cur.id).update(previous_dose=prev)
                    linked += 1
    return linked


def reanchor_dependents(child, changed_bases):
    """
    For each changed base dose (now given), compute dependent doses and set their due window.
    Handles both same-series and cross-vaccine dependencies with proper database routing.
    Returns list[ChildDose] newly anchored.
    """
    try:
        from .models import VaccineDose, Vaccine, ChildDose
        from datetime import timedelta
        
        if not changed_bases:
            return []
        
        # Get all child doses
        all_child_doses = list(
            ChildDose.objects.using("patients")
            .filter(child=child)
        )
        
        # Create a mapping of dose_id -> dose info to avoid repeated queries
        dose_cache = {}
        
        # Load all dose and vaccine data separately with caching
        for cd in all_child_doses:
            if cd.dose_id not in dose_cache:
                try:
                    dose = VaccineDose.objects.using("default").select_related("vaccine").get(pk=cd.dose_id)
                    dose_cache[cd.dose_id] = {
                        'dose': dose,
                        'vaccine_code': dose.vaccine.code.lower(),
                        'vaccine_name': dose.vaccine.name,
                        'previous_dose_id': dose.previous_dose_id,
                        'min_offset_days': dose.min_offset_days,
                        'max_offset_days': dose.max_offset_days,
                    }
                except Exception as e:
                    print(f"Warning: Could not load dose {cd.dose_id}: {e}")
                    dose_cache[cd.dose_id] = None
        
        # Also load dose info for changed_bases
        for base_cd in changed_bases:
            if base_cd.dose_id not in dose_cache:
                try:
                    dose = VaccineDose.objects.using("default").select_related("vaccine").get(pk=base_cd.dose_id)
                    dose_cache[base_cd.dose_id] = {
                        'dose': dose,
                        'vaccine_code': dose.vaccine.code.lower(),
                        'vaccine_name': dose.vaccine.name,
                        'previous_dose_id': dose.previous_dose_id,
                        'min_offset_days': dose.min_offset_days,
                        'max_offset_days': dose.max_offset_days,
                    }
                except Exception as e:
                    print(f"Warning: Could not load base dose {base_cd.dose_id}: {e}")
                    dose_cache[base_cd.dose_id] = None
        
        newly_anchored = []
        
        # For each changed base dose, find dependent doses
        for base_cd in changed_bases:
            if not base_cd.given_date:
                continue
            
            base_dose_info = dose_cache.get(base_cd.dose_id)
            if not base_dose_info:
                continue
                
            # Find doses that depend on this base dose
            for cd in all_child_doses:
                if cd.given_date:  # Skip already given doses
                    continue
                    
                cd_dose_info = dose_cache.get(cd.dose_id)
                if not cd_dose_info:
                    continue
                
                # Check if this dose depends on the base dose
                if cd_dose_info['previous_dose_id'] == base_cd.dose_id:
                    
                    # Calculate new due date based on vaccine series logic
                    vaccine_code = cd_dose_info['vaccine_code']
                    base_vaccine_code = base_dose_info['vaccine_code']
                    
                    # Special handling for different vaccine series
                    if 'influenza' in vaccine_code and 'influenza' in base_vaccine_code:
                        # Influenza series: 30-day intervals
                        new_due_date = base_cd.given_date + timedelta(days=30)
                    elif 'annual' in vaccine_code and 'influenza' in base_vaccine_code:
                        # Annual Influenza: 1 year from Influenza-2
                        new_due_date = base_cd.given_date + timedelta(days=365)
                    elif 'annual' in vaccine_code and 'annual' in base_vaccine_code:
                        # Subsequent Annual Influenza: 1 year from previous annual
                        new_due_date = base_cd.given_date + timedelta(days=365)
                    else:
                        # Standard vaccine series: use offset difference
                        interval_days = cd_dose_info['min_offset_days'] - base_dose_info['min_offset_days']
                        if interval_days > 0:
                            new_due_date = base_cd.given_date + timedelta(days=interval_days)
                        else:
                            # Fallback: use minimum gap of 28 days (4 weeks)
                            new_due_date = base_cd.given_date + timedelta(days=28)
                    
                    # Update the due date
                    old_due_date = cd.due_date
                    cd.due_date = new_due_date
                    cd.due_until_date = new_due_date + timedelta(days=30)  # 30-day window
                    cd.save(using="patients", update_fields=["due_date", "due_until_date", "updated_at"])
                    
                    newly_anchored.append(cd)
                    
                    # print(f"✅ Reanchored {cd.dose.vaccine.code}: {old_due_date} → {new_due_date}")
        
        # Also handle chain reactions - if we anchored a dose, check if it anchors others
        if newly_anchored:
            # print(f"Checking for chain reactions from {len(newly_anchored)} newly anchored doses...")
            chain_anchored = reanchor_dependents(child, newly_anchored)
            newly_anchored.extend(chain_anchored)
        
        return newly_anchored
        
    except Exception as e:
        # If reanchor fails, log the error but don't break the vaccine update
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in reanchor_dependents: {e}")
        import traceback
        traceback.print_exc()
        return []  # Return empty list so vaccine update still succeeds


def get_patient_videos(vaccine, preferred_langs: Iterable[str]) -> list[VaccineEducationPatient]:
    """
    Return active patient videos for a vaccine, prioritizing preferred_langs order.
    """
    qs = VaccineEducationPatient.objects.using("masters").filter(vaccine=vaccine, is_active=True).order_by("rank")
    items = list(qs)
    # stable sort by preferred language order
    order = {code: i for i, code in enumerate(preferred_langs)}
    items.sort(key=lambda x: (order.get(x.language, 999), x.rank))
    return items

def get_doctor_videos(vaccine) -> list[VaccineEducationDoctor]:
    return list(VaccineEducationDoctor.objects.using("masters").filter(vaccine=vaccine, is_active=True).order_by("rank"))




def send_doctor_portal_link(doctor, request):
    """
    Send doctor portal link to the doctor via WhatsApp or other means.
    This is a placeholder function - implement actual sending logic as needed.
    """
    try:
        # Placeholder implementation
        # You can implement actual WhatsApp/SMS/Email sending logic here
        print(f"Sending doctor portal link to {doctor.name} ({doctor.whatsapp_e164})")
        
        # For now, just log that the function was called
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Doctor portal link requested for {doctor.name}")
        
        return True
        
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error sending doctor portal link: {e}")
        return False
