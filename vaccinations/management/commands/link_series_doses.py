from __future__ import annotations
from django.core.management.base import BaseCommand
from django.db import transaction

from vaccinations.models import ScheduleVersion, VaccineDose


class Command(BaseCommand):
	help = "Link sequential doses within each vaccine to the previous dose (sets previous_dose for sequence_index>1 where missing)."

	def handle(self, *args, **opts):
		sv = (
			ScheduleVersion.objects.filter(is_current=True)
			.order_by("-effective_from", "-created_at").first()
		)
		if not sv:
			self.stdout.write(self.style.ERROR("No current ScheduleVersion found."))
			return

		linked = 0
		with transaction.atomic():
			per_vax: dict[int, list[VaccineDose]] = {}
			for vd in (
				VaccineDose.objects.filter(schedule_version=sv)
				.order_by("vaccine_id", "sequence_index", "id")
			):
				per_vax.setdefault(vd.vaccine_id, []).append(vd)

			for vax_id, arr in per_vax.items():
				for i in range(1, len(arr)):
					cur = arr[i]
					prev = arr[i - 1]
					if cur.previous_dose_id is None:
						VaccineDose.objects.filter(pk=cur.id).update(previous_dose=prev)
						linked += 1

		self.stdout.write(self.style.SUCCESS(f"Series links created/updated: {linked}"))



