from django.core.management.base import BaseCommand
from vaccinations.models import Child

class Command(BaseCommand):
    help = 'Clear all children from the database'

    def handle(self, *args, **options):
        # Delete all children
        child_count = Child.objects.count()
        
        Child.objects.all().delete()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully deleted {child_count} children from the database.'
            )
        )

