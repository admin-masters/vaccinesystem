from __future__ import annotations
from django.core.management.base import BaseCommand
from django.db import transaction

from vaccinations.models import ChildDose
from vaccinations.utils import birth_window, booster_window


class Command(BaseCommand):
	help = "Recompute due windows for all child doses that depend on a previous dose (previous_dose not null)."

	def handle(self, *args, **opts):
		cds = (
			ChildDose.objects
			.select_related("child", "dose__previous_dose")
			.filter(dose__previous_dose__isnull=False)
		)
		updated, cleared = 0, 0
		with transaction.atomic():
			for cd in cds:
				prev_cd = ChildDose.objects.filter(child=cd.child, dose=cd.dose.previous_dose).first()
				if prev_cd and prev_cd.given_date:
					b = cd.dose
					if b.is_booster:
						# True booster: anchor relative to previous given date
						due_date, due_until = booster_window(
							prev_given=prev_cd.given_date,
							booster_min=b.min_offset_days,
							prev_min=b.previous_dose.min_offset_days,
							booster_max=b.max_offset_days,
						)
					else:
						# Primary series: anchor from birth, becomes active after previous is given
						due_date, due_until = birth_window(prev_cd.child.date_of_birth, b.min_offset_days, b.max_offset_days)
					if cd.due_date != due_date or cd.due_until_date != due_until:
						cd.due_date = due_date
						cd.due_until_date = due_until
						cd.save(update_fields=["due_date", "due_until_date", "updated_at"])
						updated += 1
				else:
					if cd.due_date is not None or cd.due_until_date is not None:
						cd.due_date = None
						cd.due_until_date = None
						cd.save(update_fields=["due_date", "due_until_date", "updated_at"])
						cleared += 1
		self.stdout.write(self.style.SUCCESS(f"Re-anchored: {updated}, Cleared (await base): {cleared}"))



