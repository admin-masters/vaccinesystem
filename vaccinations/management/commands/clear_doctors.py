from django.core.management.base import BaseCommand
from vaccinations.models import Doctor, Clinic

class Command(BaseCommand):
    help = 'Clear all doctors and clinics from the database'

    def handle(self, *args, **options):
        # Delete all doctors first (this will also delete related clinics due to CASCADE)
        doctor_count = Doctor.objects.count()
        clinic_count = Clinic.objects.count()
        
        Doctor.objects.all().delete()
        Clinic.objects.all().delete()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully deleted {doctor_count} doctors and {clinic_count} clinics from the database.'
            )
        )
