from __future__ import annotations
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction

from .models import Child, ChildDose, VaccineDose
from .utils import birth_window
from .services import current_schedule, reanchor_dependents


@receiver(post_save, sender=Child)
def create_child_doses_on_child_create(sender, instance: Child, created: bool, **kwargs):
    if not created:
        return
    sv = current_schedule()
    if not sv:
        return
    doses = (VaccineDose.objects.filter(schedule_version=sv)
             .select_related("previous_dose")
             .order_by("vaccine_id", "sequence_index"))
    to_create = []
    for d in doses:
        if d.previous_dose_id is None:
            dd, du = birth_window(instance.date_of_birth, d.min_offset_days, d.max_offset_days)
        else:
            dd = du = None
        to_create.append(ChildDose(child=instance, dose=d, due_date=dd, due_until_date=du))
    if to_create:
        ChildDose.objects.bulk_create(to_create, batch_size=500)


@receiver(pre_save, sender=ChildDose)
def mark_given_date_change(sender, instance: ChildDose, **kwargs):
    if not instance.pk:
        instance._given_date_changed = bool(instance.given_date)
        return
    try:
        prev = ChildDose.objects.only("given_date").get(pk=instance.pk)
    except ChildDose.DoesNotExist:
        instance._given_date_changed = bool(instance.given_date)
        return
    instance._given_date_changed = (prev.given_date != instance.given_date)


@receiver(post_save, sender=ChildDose)
def reanchor_dependents_on_save(sender, instance: ChildDose, **kwargs):
    if not getattr(instance, "_given_date_changed", False):
        return
    transaction.on_commit(lambda: reanchor_dependents(instance.child, [instance]))
