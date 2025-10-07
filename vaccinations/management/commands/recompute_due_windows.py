from django.core.management.base import BaseCommand
from django.db import transaction
from vaccinations.models import Child
from vaccinations.utils import series_window, birth_window
from vaccinations.utils_schedule import build_series_prev_maps
class Command(BaseCommand):
    help = "Recompute due windows using series-aware previous mapping."

    def add_arguments(self, parser):
        parser.add_argument("--child-id", type=int)

    def handle(self, *args, **opts):
        qs = Child.objects.all()
        if opts.get("child_id"): qs = qs.filter(id=opts["child_id"])

        total = changed = 0
        for child in qs.iterator():
            cds = list(child.doses.select_related("dose__previous_dose", "dose__vaccine"))
            prev_cd_by, prev_min_by = build_series_prev_maps(cds)
            with transaction.atomic():
                for cd in cds:
                    dep = cd.dose
                    prev_cd = prev_cd_by.get(dep.id)
                    prev_min = prev_min_by.get(dep.id)

                    if prev_cd is None and prev_min is None:
                        dd, du = birth_window(child.date_of_birth, dep.min_offset_days, dep.max_offset_days)
                    else:
                        prev_given = prev_cd.given_date if prev_cd else None
                        dd, du = series_window(child.date_of_birth, dep, prev_given, prev_min)

                    if cd.due_date != dd or cd.due_until_date != du:
                        cd.due_date, cd.due_until_date = dd, du
                        cd.save(update_fields=["due_date","due_until_date","updated_at"])
                        changed += 1
                    total += 1

        self.stdout.write(self.style.SUCCESS(f"Recomputed {total} rows; changed {changed}."))
