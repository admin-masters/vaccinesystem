#!/usr/bin/env python3
"""
Debug vaccination card loading
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaccination_project.settings')
django.setup()

from vaccinations.models import ChildDose, Child, VaccineDose, Vaccine
from vaccinations.views import _compute_ui_state
from django.db import models

def debug_vaccination_card():
    print("🔍 Debugging vaccination card loading...")
    
    # Check all children first
    children = Child.objects.using("patients").all()
    print(f"📊 Total children in database: {children.count()}")
    
    for child in children:
        dose_count = ChildDose.objects.using("patients").filter(child=child).count()
        print(f"  Child {child.id}: {child.get_child_name()} - {dose_count} doses")
    
    # Get child ID 6 (from the URL) or find one with doses
    child_id = 6
    try:
        child = Child.objects.using("patients").get(pk=child_id)
        print(f"\n✅ Child {child_id} found: {child.get_child_name()}")
    except Child.DoesNotExist:
        print(f"❌ Child {child_id} not found")
        # Try to find a child with doses
        child_with_doses = children.annotate(
            dose_count=models.Count('doses')
        ).filter(dose_count__gt=0).first()
        
        if child_with_doses:
            child = child_with_doses
            child_id = child.id
            print(f"✅ Using child {child_id} instead: {child.get_child_name()}")
        else:
            print(f"❌ No children with doses found")
            return
    
    # Test the fixed loading logic
    print(f"\n🔧 Testing fixed loading logic...")
    
    # Debug the child dose query
    print(f"🔍 Debugging child dose query for child {child.id}...")
    
    # Try different ways to query
    all_doses = ChildDose.objects.using("patients").all()
    print(f"  Total ChildDoses in DB: {all_doses.count()}")
    
    doses_for_child = ChildDose.objects.using("patients").filter(child_id=child.id)
    print(f"  Doses for child {child.id} (by child_id): {doses_for_child.count()}")
    
    doses_for_child_obj = ChildDose.objects.using("patients").filter(child=child)
    print(f"  Doses for child {child.id} (by child object): {doses_for_child_obj.count()}")
    
    # Check if child object has the right ID
    print(f"  Child object ID: {child.id}")
    print(f"  Child object PK: {child.pk}")
    
    # Test different queries
    print(f"  Testing without select_related...")
    cds_no_select = list(ChildDose.objects.using("patients").filter(child_id=child.id))
    print(f"  Without select_related: {len(cds_no_select)} doses")
    
    print(f"  Testing with select_related...")
    cds_with_select = list(ChildDose.objects.using("patients").filter(child_id=child.id).select_related("dose"))
    print(f"  With select_related: {len(cds_with_select)} doses")
    
    # Use the working query
    cds = cds_no_select  # Use the one that works
    
    print(f"📊 Found {len(cds)} child doses")
    
    # Load dose and vaccine data separately (using the fixed approach)
    successful_loads = 0
    for i, cd in enumerate(cds):
        try:
            # Load dose from default database
            dose = VaccineDose.objects.using("default").select_related("vaccine").get(pk=cd.dose_id)
            cd.dose = dose  # Attach the full dose with vaccine
            successful_loads += 1
            
            if i < 5:  # Show first 5 for debugging
                print(f"  ✅ Dose {cd.dose_id}: {dose.vaccine.name}")
                
        except Exception as e:
            print(f"  ❌ Failed to load dose {cd.dose_id}: {e}")
    
    print(f"📊 Successfully loaded vaccines for {successful_loads}/{len(cds)} doses")
    
    if successful_loads == 0:
        print(f"❌ No vaccines loaded - this is why card is empty!")
        return
    
    # Test UI state computation
    print(f"\n🎨 Testing UI state computation...")
    try:
        rows = _compute_ui_state(child, cds, show_all=False)  # show_all=False for "Show Due Only"
        print(f"📊 UI state computed: {len(rows)} rows")
        
        if len(rows) == 0:
            print(f"❌ No rows in UI state - this is why card shows 'No vaccines to display'")
            
            # Try with show_all=True
            rows_all = _compute_ui_state(child, cds, show_all=True)
            print(f"📊 With show_all=True: {len(rows_all)} rows")
            
            if len(rows_all) > 0:
                print(f"✅ Full schedule works, issue is with 'Show Due Only' filtering")
                
                # Check child's birth date and current date
                from datetime import date
                child_dob = child.get_date_of_birth_encrypted()
                today_date = date.today()
                print(f"  Child DOB: {child_dob}")
                print(f"  Today: {today_date}")
                print(f"  Age in days: {(today_date - child_dob).days}")
                
                # Show vaccine statuses
                for i, row in enumerate(rows_all[:10]):
                    status = row.get('status', 'unknown')
                    vaccine_name = row.get('vaccine_name', 'unknown')
                    due_date = row.get('due_date', 'No date')
                    print(f"  Row {i+1}: {vaccine_name} - {status} (Due: {due_date})")
                
                # Count statuses
                status_counts = {}
                for row in rows_all:
                    status = row.get('status', 'unknown')
                    status_counts[status] = status_counts.get(status, 0) + 1
                print(f"  Status summary: {status_counts}")
            
        else:
            print(f"✅ UI state has rows:")
            for i, row in enumerate(rows[:5]):
                status = row.get('status', 'unknown')
                vaccine_name = row.get('vaccine_name', 'unknown')
                print(f"  Row {i+1}: {vaccine_name} - {status}")
                
    except Exception as e:
        print(f"❌ Error in UI state computation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_vaccination_card()
