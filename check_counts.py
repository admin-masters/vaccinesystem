import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaccination_project.settings')
django.setup()

from vaccinations.models import Doctor, Child, Parent

try:
    doctors = Doctor.objects.using('masters').count()
    print(f'Doctors: {doctors}')
except Exception as e:
    print(f'Could not count doctors: {e}')

try:
    children = Child.objects.using('patients').count()
    print(f'Children: {children}')
except Exception as e:
    print(f'Could not count children: {e}')

try:
    parents = Parent.objects.using('patients').count()
    print(f'Parents: {parents}')
except Exception as e:
    print(f'Could not count parents: {e}')
