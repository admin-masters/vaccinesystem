from django.core.management.base import BaseCommand
from django.db import transaction
from vaccinations.models import Child, ChildDose

class Command(BaseCommand):
    help = 'Clean up duplicate ChildDose records'

    def handle(self, *args, **options):
        self.stdout.write("Cleaning up duplicate child doses...")
        
        total_deleted = 0
        
        with transaction.atomic():
            for child in Child.objects.all():
                # Get all child doses for this child
                child_doses = ChildDose.objects.filter(
                    child=child
                ).order_by('dose__sequence_index', 'id')
                
                # Group by dose and keep only the first one
                seen_doses = set()
                deleted_count = 0
                
                for cd in child_doses:
                    if cd.dose_id in seen_doses:
                        self.stdout.write(f"  Deleting duplicate: {cd.dose.dose_label} for {child.full_name}")
                        cd.delete()
                        deleted_count += 1
                    else:
                        seen_doses.add(cd.dose_id)
                
                if deleted_count > 0:
                    self.stdout.write(self.style.WARNING(f"  Removed {deleted_count} duplicate doses for {child.full_name}"))
                    total_deleted += deleted_count
        
        if total_deleted > 0:
            self.stdout.write(self.style.SUCCESS(f"\n✓ Removed {total_deleted} duplicate child doses total"))
        else:
            self.stdout.write(self.style.SUCCESS("\n✓ No duplicate doses found"))
