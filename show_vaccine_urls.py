#!/usr/bin/env python3
"""
Show vaccine education URLs for testing
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaccination_project.settings')
django.setup()

from vaccinations.models import Vaccine

def show_vaccine_urls():
    print("🔗 Vaccine Education URLs for testing:")
    print("=" * 60)
    
    vaccines = Vaccine.objects.using("masters").all().order_by('name')
    
    for vaccine in vaccines:
        url = f"http://127.0.0.1:8000/edu/vaccine/{vaccine.id}/"
        print(f"{vaccine.name:25} - {url}")
    
    print("\n💡 Instructions:")
    print("1. Start the Django server: python manage.py runserver")
    print("2. Click on any vaccine name in the vaccination history page")
    print("3. Or directly visit any of the URLs above")
    print("4. You should see education videos for each vaccine")

if __name__ == "__main__":
    show_vaccine_urls()
