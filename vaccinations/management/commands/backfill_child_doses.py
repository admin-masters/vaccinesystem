from __future__ import annotations
from django.core.management.base import BaseCommand
from django.db import transaction

from vaccinations.models import Child, ChildDose, VaccineDose, ScheduleVersion
from vaccinations.utils import birth_window


class Command(BaseCommand):
	help = "Create missing ChildDose rows for all children for the current schedule."

	def handle(self, *args, **opts):
		sv = (
			ScheduleVersion.objects.filter(is_current=True)
			.order_by("-effective_from", "-created_at").first()
		)
		if not sv:
			self.stdout.write(self.style.ERROR("No current ScheduleVersion found."))
			return

		doses = list(
			VaccineDose.objects.filter(schedule_version=sv)
			.select_related("previous_dose")
			.order_by("vaccine_id", "sequence_index")
		)

		children = list(Child.objects.all().select_related("parent"))
		created = 0
		with transaction.atomic():
			for child in children:
				existing = set(
					ChildDose.objects.filter(child=child).values_list("dose_id", flat=True)
				)
				to_create: list[ChildDose] = []
				for d in doses:
					if d.id in existing:
						continue
					if d.previous_dose_id is None:
						dd, du = birth_window(child.date_of_birth, d.min_offset_days, d.max_offset_days)
					else:
						dd = du = None
					to_create.append(ChildDose(child=child, dose=d, due_date=dd, due_until_date=du))
				if to_create:
					ChildDose.objects.bulk_create(to_create, batch_size=500)
					created += len(to_create)

		self.stdout.write(self.style.SUCCESS(f"ChildDose created: {created}"))


