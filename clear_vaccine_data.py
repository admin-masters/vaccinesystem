import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaccination_project.settings')
django.setup()

from vaccinations.models import Vaccine, VaccineDose, ScheduleVersion

print("Clearing existing vaccine data...")
VaccineDose.objects.using('masters').all().delete()
print("✓ Cleared vaccine doses")

Vaccine.objects.using('masters').all().delete()
print("✓ Cleared vaccines")

ScheduleVersion.objects.using('masters').all().delete()
print("✓ Cleared schedule versions")

print("All vaccine data cleared successfully!")
