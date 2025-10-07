#!/usr/bin/env python3
"""
Simple test for waiting vaccines
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaccination_project.settings')
django.setup()

from vaccinations.models import Child, ChildDose
from vaccinations.views import _compute_ui_state
from django.db.models import Prefetch
from vaccinations.models import VaccineDose

def simple_waiting_test():
    print("🔍 Simple waiting vaccines test...")
    
    child = Child.objects.using("patients").first()
    if not child:
        print("❌ No child found")
        return
    
    # Get child doses
    child_doses = list(
        ChildDose.objects.using("patients")
        .filter(child=child)
        .prefetch_related(
            Prefetch("dose", queryset=VaccineDose.objects.using("default").select_related("vaccine"))
        )
    )
    
    # Test Show Due Only
    show_due_rows = _compute_ui_state(child, child_doses, show_all=False)
    
    print(f"Show Due Only: {len(show_due_rows)} vaccines")
    
    # Count by status
    status_counts = {}
    for row in show_due_rows:
        status = row['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print("Status counts:")
    for status, count in status_counts.items():
        print(f"  {status}: {count}")
    
    # Show any vaccines with "waiting" status
    waiting_vaccines = [row for row in show_due_rows if row['status'] == 'waiting']
    
    if waiting_vaccines:
        print(f"\n❌ Found {len(waiting_vaccines)} vaccines with 'waiting' status:")
        for row in waiting_vaccines:
            cd = row['child_dose']
            print(f"  - {cd.dose.vaccine.code}")
    else:
        print("\n✅ No vaccines with 'waiting' status found")

if __name__ == "__main__":
    simple_waiting_test()
