from __future__ import annotations
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction
from django.utils import timezone

from .models import Child, ChildDose, ScheduleVersion, VaccineDose
from .utils import birth_window, booster_window

def _get_current_schedule_version() -> ScheduleVersion | None:
    return (ScheduleVersion.objects.filter(is_current=True)
            .order_by("-effective_from", "-created_at").first())

def _ensure_child_doses(child: Child) -> None:
    sv = _get_current_schedule_version()
    if not sv:
        return
    doses = (VaccineDose.objects
             .filter(schedule_version=sv)
             .select_related("previous_dose")
             .order_by("vaccine_id", "sequence_index"))
    existing = set(ChildDose.objects.filter(child=child).values_list("dose_id", flat=True))
    to_create = []
    for d in doses:
        if d.id in existing:
            continue
        due_date = None
        due_until = None
        if not d.is_booster:
            due_date, due_until = birth_window(child.date_of_birth, d.min_offset_days, d.max_offset_days)
        to_create.append(ChildDose(child=child, dose=d, due_date=due_date, due_until_date=due_until))
    if to_create:
        ChildDose.objects.bulk_create(to_create, batch_size=500)

@receiver(post_save, sender=Child)
def create_child_doses_on_child_create(sender, instance: Child, created: bool, **kwargs):
    if created:
        transaction.on_commit(lambda: _ensure_child_doses(instance))

@receiver(pre_save, sender=ChildDose)
def track_given_date_change(sender, instance: ChildDose, **kwargs):
    if not instance.pk:
        instance._given_date_became_set = bool(instance.given_date)
        return
    try:
        prev = ChildDose.objects.only("given_date").get(pk=instance.pk)
        instance._given_date_became_set = prev.given_date is None and instance.given_date is not None
    except ChildDose.DoesNotExist:
        instance._given_date_became_set = bool(instance.given_date)

@receiver(post_save, sender=ChildDose)
def compute_booster_due_dates_when_previous_given(sender, instance: ChildDose, **kwargs):
    if not getattr(instance, "_given_date_became_set", False):
        return
    prev_cd = instance
    prev_vd = prev_cd.dose
    given_date = prev_cd.given_date
    if not given_date:
        return

    boosters = VaccineDose.objects.filter(previous_dose=prev_vd).select_related("previous_dose")
    with transaction.atomic():
        for booster in boosters:
            due_date, due_until = booster_window(
                prev_given=given_date,
                booster_min=booster.min_offset_days,
                prev_min=prev_vd.min_offset_days,
                booster_max=booster.max_offset_days,
            )
            ChildDose.objects.filter(child=prev_cd.child, dose_id=booster.id).update(
                due_date=due_date, due_until_date=due_until, updated_at=timezone.now()
            )
