import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaccination_project.settings')
django.setup()

from vaccinations.models import ScheduleVersion, Vaccine, VaccineDose

def copy_vaccines():
    print("Copying vaccine data from clinic_db to masters using ORM...")
    
    # Clear masters data first
    print("Clearing masters data...")
    try:
        VaccineDose.objects.using("masters").all().delete()
        print("✓ Cleared vaccine doses")
    except Exception as e:
        print(f"Error clearing doses: {e}")
    
    try:
        Vaccine.objects.using("masters").all().delete()
        print("✓ Cleared vaccines")
    except Exception as e:
        print(f"Error clearing vaccines: {e}")
    
    try:
        ScheduleVersion.objects.using("masters").all().delete()
        print("✓ Cleared schedule versions")
    except Exception as e:
        print(f"Error clearing schedules: {e}")
    
    # Copy schedule versions
    print("\nCopying schedule versions...")
    source_schedules = ScheduleVersion.objects.using("default").all()
    for schedule in source_schedules:
        new_schedule = ScheduleVersion(
            code=schedule.code,
            name=schedule.name,
            source_url=schedule.source_url,
            effective_from=schedule.effective_from,
            is_current=schedule.is_current
        )
        new_schedule.save(using="masters")
        print(f"✓ Copied: {schedule.name}")
    
    # Copy vaccines
    print("\nCopying vaccines...")
    source_vaccines = Vaccine.objects.using("default").all()
    vaccine_mapping = {}
    
    for vaccine in source_vaccines:
        masters_schedule = ScheduleVersion.objects.using("masters").get(code=vaccine.schedule_version.code)
        new_vaccine = Vaccine(
            schedule_version=masters_schedule,
            code=vaccine.code,
            name=vaccine.name,
            aliases=vaccine.aliases,
            is_active=vaccine.is_active,
            notes=vaccine.notes
        )
        new_vaccine.save(using="masters")
        vaccine_mapping[vaccine.id] = new_vaccine
        print(f"✓ Copied: {vaccine.name}")
    
    # Copy vaccine doses (first pass - without previous_dose)
    print("\nCopying vaccine doses...")
    source_doses = VaccineDose.objects.using("default").all()
    dose_mapping = {}
    
    for dose in source_doses:
        masters_vaccine = vaccine_mapping[dose.vaccine.id]
        masters_schedule = ScheduleVersion.objects.using("masters").get(code=dose.schedule_version.code)
        
        new_dose = VaccineDose(
            schedule_version=masters_schedule,
            vaccine=masters_vaccine,
            sequence_index=dose.sequence_index,
            dose_label=dose.dose_label,
            eligible_gender=dose.eligible_gender,
            min_offset_days=dose.min_offset_days,
            max_offset_days=dose.max_offset_days,
            is_booster=dose.is_booster,
            notes=dose.notes
        )
        new_dose.save(using="masters")
        dose_mapping[dose.id] = new_dose
        print(f"✓ Copied: {dose.vaccine.name} - {dose.dose_label}")
    
    # Second pass - update previous_dose relationships
    print("\nUpdating previous_dose relationships...")
    for dose in source_doses:
        if dose.previous_dose:
            masters_dose = dose_mapping[dose.id]
            masters_previous = dose_mapping[dose.previous_dose.id]
            masters_dose.previous_dose = masters_previous
            masters_dose.save(using="masters", update_fields=['previous_dose'])
    
    # Verify
    print("\n=== VERIFICATION ===")
    masters_schedules = ScheduleVersion.objects.using("masters").count()
    masters_vaccines = Vaccine.objects.using("masters").count()
    masters_doses = VaccineDose.objects.using("masters").count()
    
    print(f"✅ Masters database now has:")
    print(f"  - {masters_schedules} schedule versions")
    print(f"  - {masters_vaccines} vaccines")
    print(f"  - {masters_doses} vaccine doses")
    
    print(f"\n=== SAMPLE VACCINES ===")
    sample_vaccines = Vaccine.objects.using("masters").all()[:5]
    for vaccine in sample_vaccines:
        dose_count = VaccineDose.objects.using("masters").filter(vaccine=vaccine).count()
        print(f"  {vaccine.name} ({dose_count} doses)")

if __name__ == "__main__":
    copy_vaccines()
