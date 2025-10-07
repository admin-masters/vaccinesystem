import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaccination_project.settings')
django.setup()

from vaccinations.models import Doctor

try:
    doctors = Doctor.objects.using('masters').all()
    print(f'Total doctors: {doctors.count()}')
    
    for doctor in doctors:
        print(f'\nDoctor Details:')
        print(f'ID: {doctor.id}')
        print(f'Full Name: {doctor.full_name}')
        print(f'WhatsApp: {doctor.whatsapp_e164}')
        print(f'Clinic: {doctor.clinic.name if doctor.clinic else "No clinic"}')
        print(f'Google ID: {doctor.google_id if hasattr(doctor, "google_id") else "N/A"}')
        print(f'Created: {doctor.created_at if hasattr(doctor, "created_at") else "N/A"}')
        
except Exception as e:
    print(f'Error checking doctors: {e}')
