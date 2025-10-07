"""
Management command to correctly calculate ALL due dates based on IAP schedule.
All dates are calculated from birth date using min_offset_days.
"""
from django.core.management.base import BaseCommand
from vaccinations.models import Child, ChildDose
from vaccinations.utils import birth_window


class Command(BaseCommand):
    help = 'Recalculate all due dates correctly from birth date (IAP schedule)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--child-id',
            type=int,
            help='Calculate dates for a specific child only',
        )

    def handle(self, *args, **options):
        child_id = options.get('child_id')
        
        if child_id:
            children = Child.objects.filter(id=child_id)
            if not children.exists():
                self.stdout.write(self.style.ERROR(f'Child with ID {child_id} not found'))
                return
        else:
            children = Child.objects.all()
        
        total_children = children.count()
        if total_children == 0:
            self.stdout.write(self.style.WARNING('No children found'))
            return
        
        self.stdout.write(f'Processing {total_children} children...\n')
        
        total_updated = 0
        
        for child in children:
            self.stdout.write(f'Child: {child.full_name} (DOB: {child.date_of_birth})')
            
            # Get all doses for this child
            cds = child.doses.select_related("dose__vaccine").all()
            
            if not cds:
                self.stdout.write('  No doses found, skipping')
                continue
            
            updated_count = 0
            
            # Calculate dates for all doses directly from birth date
            for cd in cds:
                # Skip if already given
                if cd.given_date:
                    continue
                
                # Calculate from birth date using min_offset and max_offset
                dd, du = birth_window(
                    child.date_of_birth,
                    cd.dose.min_offset_days,
                    cd.dose.max_offset_days
                )
                
                # Update only if date changed
                if cd.due_date != dd or cd.due_until_date != du:
                    cd.due_date = dd
                    cd.due_until_date = du
                    cd.save(update_fields=['due_date', 'due_until_date', 'updated_at'])
                    updated_count += 1
            
            self.stdout.write(self.style.SUCCESS(f'  Updated {updated_count} doses'))
            total_updated += updated_count
        
        self.stdout.write(self.style.SUCCESS(f'\nCompleted! Updated {total_updated} doses for {total_children} children'))
