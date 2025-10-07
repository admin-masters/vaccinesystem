from __future__ import annotations
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction

from .models import Child, ChildDose, VaccineDose
from .utils import birth_window, series_window
from .services import current_schedule, reanchor_dependents
from .utils_schedule import build_series_prev_maps


@receiver(post_save, sender=Child)
def create_child_doses_on_child_create(sender, instance: Child, created: bool, **kwargs):
    """
    Create all ChildDose records when a new Child is created.
    Uses proper seeding logic to prevent boosters from getting premature due dates.
    """
    if not created:
        return
    sv = current_schedule()
    if not sv:
        return
    
    # Get all VaccineDose records for the current schedule in proper order
    doses = (VaccineDose.objects.using("default").filter(schedule_version=sv)
             .select_related("previous_dose", "vaccine")
             .order_by("vaccine__name", "sequence_index"))
    
    # Create ChildDose objects in memory first to establish relationships
    cds = []  # create in-memory to compute prevs while seeding
    
    for dose in doses:
        cd = ChildDose(child=instance, dose=dose)  # do not set dates yet
        cds.append(cd)
    
    # Build fallback prev context on the pseudo-list that mirrors the schedule order
    prev_cd_by, prev_min_by = build_series_prev_maps(cds)
    
    # Now calculate dates properly using the series mapping
    for cd in cds:
        dep = cd.dose
        prev_cd = prev_cd_by.get(dep.id)  # None during seeding
        prev_min = prev_min_by.get(dep.id)

        if prev_cd is None and prev_min is None:
            # First dose in series - calculate from birth date
            birth_date = instance.get_date_of_birth_encrypted()
            dd, du = birth_window(birth_date, dep.min_offset_days, dep.max_offset_days)
        else:
            # Dependent dose - not eligible yet (dates remain None)
            # This prevents boosters from getting premature due dates
            dd, du = (None, None)
        
        cd.due_date = dd
        cd.due_until_date = du
    
    # Save all ChildDose records
    if cds:
        ChildDose.objects.using("patients").bulk_create(cds, batch_size=500)
        
        # Auto-implement complete IAP schedule with proper dates
        birth_date = instance.get_date_of_birth_encrypted()
        
        # Implement complete IAP schedule automation
        def implement_iap_schedule():
            try:
                from datetime import timedelta
                
                # Use dynamic IAP schedule based on vaccine database min_offset_days
                # This uses the actual vaccine schedule data instead of hard-coding
                
                saved_doses = ChildDose.objects.using("patients").filter(child=instance)
                doses_to_update = []
                
                for cd in saved_doses:
                    try:
                        # Load vaccine info with min_offset_days from database
                        dose = VaccineDose.objects.using("default").select_related("vaccine").get(pk=cd.dose_id)
                        
                        # Use the actual min_offset_days from the vaccine database
                        if dose.min_offset_days is not None:
                            expected_due_date = birth_date + timedelta(days=dose.min_offset_days)
                            
                            # Update due date based on database schedule
                            cd.due_date = expected_due_date
                            cd.due_until_date = expected_due_date + timedelta(days=dose.max_offset_days - dose.min_offset_days if dose.max_offset_days else 30)
                            doses_to_update.append(cd)
                            
                            # Don't automatically mark birth vaccines as given
                            # Let parents/doctors mark them manually when actually administered
                        else:
                            # If no min_offset_days, leave as waiting (will be anchored later)
                            pass
                                
                    except Exception as e:
                        print(f"Warning: Could not process dose {cd.dose_id}: {e}")
                        continue
                
                # Bulk update all doses with proper IAP dates (no automatic given_date)
                if doses_to_update:
                    ChildDose.objects.using("patients").bulk_update(
                        doses_to_update, 
                        ['due_date', 'due_until_date'], 
                        batch_size=100
                    )
                
                # No automatic reanchoring - let it happen when vaccines are actually given
                    
            except Exception as e:
                # Log error but don't break child creation
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error implementing IAP schedule: {e}")
        
        # Schedule the IAP implementation after transaction commits
        transaction.on_commit(implement_iap_schedule)


@receiver(pre_save, sender=ChildDose)
def mark_given_date_change(sender, instance: ChildDose, **kwargs):
    """
    Track when the given_date field changes to trigger reanchoring of dependent doses.
    """
    if not instance.pk:
        # New instance - mark as changed if given_date is set
        instance._given_date_changed = bool(instance.given_date)
        return
    
    try:
        # Get the previous state from database
        prev = ChildDose.objects.using("patients").only("given_date").get(pk=instance.pk)
    except ChildDose.DoesNotExist:
        instance._given_date_changed = bool(instance.given_date)
        return
    
    # Check if given_date has actually changed
    instance._given_date_changed = (prev.given_date != instance.given_date)


@receiver(post_save, sender=ChildDose)
def reanchor_dependents_on_save(sender, instance: ChildDose, **kwargs):
    """
    Recalculate due dates for dependent doses when a dose is marked as given.
    Uses transaction.on_commit to ensure this runs after the save is complete.
    """
    if not getattr(instance, "_given_date_changed", False):
        return
    
    # Reanchor dependent doses after the transaction commits
    transaction.on_commit(lambda: reanchor_dependents(instance.child, [instance]))