from django.core.management.base import BaseCommand
from vaccinations.models import VaccineDose

class Command(BaseCommand):
    help = "Print series order (series_key -> doses by series_seq with offsets and anchor_policy)."

    def handle(self, *a, **o):
        qs = VaccineDose.objects.order_by("series_key","series_seq")
        cur = None
        for d in qs:
            if d.series_key != cur:
                cur = d.series_key
                self.stdout.write(self.style.NOTICE(f"\\n[{cur}]"))
            self.stdout.write(f"  #{d.series_seq:<2} id={d.id:<4} name={d.vaccine.name:<28} "
                              f"min={d.min_offset_days!s:<4} max={d.max_offset_days!s:<5} "
                              f"policy={d.anchor_policy} prev={d.previous_dose_id}")
