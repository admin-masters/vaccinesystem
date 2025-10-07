from django.core.management.base import BaseCommand
from django.db import transaction
from vaccinations.models import VaccineDose, ChildDose

class Command(BaseCommand):
    help = 'Clean up old Annual Influenza vaccine doses'

    def handle(self, *args, **options):
        self.stdout.write("Finding old Annual Influenza doses...")
        
        # The correct doses are IDs 85, 86, 87, 88 (series_key='Influenza')
        correct_dose_ids = [85, 86, 87, 88]
        
        # Find all Annual doses that are NOT the correct ones
        old_doses = VaccineDose.objects.filter(
            vaccine__name__icontains='annual'
        ).exclude(id__in=correct_dose_ids)
        
        self.stdout.write(f"Found {old_doses.count()} old Annual doses:")
        for d in old_doses:
            self.stdout.write(f"  ID {d.id}: {d.dose_label} (series_key: {d.series_key})")
        
        if old_doses.count() == 0:
            self.stdout.write(self.style.SUCCESS("No old doses to clean up!"))
            return
        
        with transaction.atomic():
            # Delete child doses first
            child_doses = ChildDose.objects.filter(dose__in=old_doses)
            cd_count = child_doses.count()
            self.stdout.write(f"\nDeleting {cd_count} child dose records...")
            child_doses.delete()
            
            # Clear any previous_dose references
            dose_ids = list(old_doses.values_list('id', flat=True))
            VaccineDose.objects.filter(previous_dose_id__in=dose_ids).update(previous_dose=None)
            
            # Delete the old doses
            self.stdout.write("Deleting old dose definitions...")
            old_doses.delete()
        
        self.stdout.write(self.style.SUCCESS("\n✓ Cleanup complete!"))
        self.stdout.write("Run 'recalculate_iap_dates' to regenerate child schedules.")
