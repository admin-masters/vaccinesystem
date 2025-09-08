from __future__ import annotations
from typing import Iterable, List, Tuple, Dict
from django.db import transaction
from django.utils import timezone

from .models import ScheduleVersion, VaccineDose, Child, ChildDose
from .utils import birth_window, booster_window


def current_schedule() -> ScheduleVersion | None:
    return (ScheduleVersion.objects
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


def reanchor_dependents(child: Child, bases: Iterable[ChildDose]) -> List[ChildDose]:
    """
    Recompute due windows for all direct dependents of the given base ChildDose(s).
    Rules:
      - If dependent.is_booster == True: anchor relative to base given date (delta rule).
      - Else (primary series): anchor to birth schedule (min/max offsets), BUT
        we only set/refresh this window after the previous dose has been given.

    IMPORTANT: We only touch direct dependents (DTaP2 when DTaP1 is set).
    Later chain members (DTaP3) become due only after DTaP2 is actually given.
    """
    updated: List[ChildDose] = []
    base_map = {cd.dose_id: cd for cd in bases if cd.given_date}
    if not base_map:
        return updated

    dependents = list(VaccineDose.objects.filter(previous_dose_id__in=base_map.keys())
                      .select_related("previous_dose"))
    if not dependents:
        return updated

    with transaction.atomic():
        for dep in dependents:
            base_cd = base_map.get(dep.previous_dose_id)
            if not base_cd:
                continue

            # Determine anchoring rule
            if dep.is_booster:
                # Booster: relative to previous actual given date
                dd, du = booster_window(
                    prev_given=base_cd.given_date,
                    booster_min=dep.min_offset_days,
                    prev_min=dep.previous_dose.min_offset_days,
                    booster_max=dep.max_offset_days,
                )
            else:
                # Primary series: absolute from birth (6w/10w/14w...), activated after prev is given
                dd, du = birth_window(child.date_of_birth, dep.min_offset_days, dep.max_offset_days)

            # Update the child's dependent dose row
            try:
                cd_dep = ChildDose.objects.get(child=child, dose=dep)
            except ChildDose.DoesNotExist:
                continue
            if cd_dep.due_date != dd or cd_dep.due_until_date != du:
                cd_dep.due_date = dd
                cd_dep.due_until_date = du
                cd_dep.updated_at = timezone.now()
                cd_dep.save(update_fields=["due_date", "due_until_date", "updated_at"])
            updated.append(cd_dep)

    return updated



