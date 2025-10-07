import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaccination_project.settings')
django.setup()

from vaccinations.models import Doctor

try:
    # Get count before deletion
    count = Doctor.objects.using('masters').count()
    print(f'Found {count} doctors to delete')
    
    # Delete doctors one by one to handle constraints
    for doctor in Doctor.objects.using('masters').all():
        try:
            print(f'Deleting doctor: {doctor.full_name} (ID: {doctor.id})')
            doctor.delete()
            print(f'Successfully deleted doctor ID: {doctor.id}')
        except Exception as e:
            print(f'Error deleting doctor {doctor.id}: {e}')
    
    # Verify deletion
    remaining = Doctor.objects.using('masters').count()
    print(f'Remaining doctors: {remaining}')
    
except Exception as e:
    print(f'Error accessing doctors: {e}')
