# vaccinations/migrations/0014_fix_influenza_series.py
from django.db import migrations, transaction
from django.core.exceptions import FieldError

def _set_seq(obj, seq):
    if hasattr(obj, "sequence_index"):
        obj.sequence_index = seq
    if hasattr(obj, "series_seq"):
        obj.series_seq = seq

def forwards(apps, schema_editor):
    ScheduleVersion = apps.get_model("vaccinations", "ScheduleVersion")
    Vaccine = apps.get_model("vaccinations", "Vaccine")
    VaccineDose = apps.get_model("vaccinations", "VaccineDose")

    # Prefer is_current if present; fall back gracefully.
    qs = ScheduleVersion.objects.order_by("-effective_from", "-id")
    sv = None
    try:
        sv = qs.filter(is_current=True).first()
        if not sv:
            # If some older DB still has is_active, try that too
            sv = qs.filter(is_active=True).first()
    except FieldError:
        # Historical state without either flag – just take the latest row
        sv = qs.first()

    if not sv:
        print("No schedule version found, skipping migration")
        return

    def get_vaccine_qs():
        qs = Vaccine.objects
        if sv:
            qs = qs.filter(schedule_version=sv)
        return qs

    # Find vaccines more flexibly
    v_infl = get_vaccine_qs().filter(
        name__iregex=r'^(Influenza|Flu)'
    ).exclude(
        name__icontains='Annual'
    ).first()
    
    v_annual = get_vaccine_qs().filter(
        name__iregex=r'^(Annual Influenza|Annual Flu)'
    ).first()

    if not v_infl:
        print("Warning: No base Influenza vaccine found")
        return
    if not v_annual:
        print("Warning: No Annual Influenza vaccine found, using base Influenza")
        v_annual = v_infl

    # Get existing doses for Influenza series
    dose_qs = VaccineDose.objects
    if sv:
        dose_qs = dose_qs.filter(schedule_version=sv)
    
    existing_doses = list(dose_qs.filter(series_key="Influenza").order_by("id"))

    specs = [
        (v_infl,   "Influenza-1",          180, None, "A"),
        (v_infl,   "Influenza-2",          210, 1,    "A"),
        (v_annual, "Annual (Year 2)",      730, 2,    "A"),
        (v_annual, "Annual (Year 3)",     1095, 3,    "A"), 
        (v_annual, "Annual (Year 4)",     1460, 4,    "A"),
        (v_annual, "Annual (Year 5)",     1825, 5,    "A"),
    ]

    with transaction.atomic():
        doses_to_save = []
        
        # First pass: prepare all doses
        for idx, spec in enumerate(specs, start=1):
            vaccine, label, min_days, prev_seq, policy = spec
            
            # Check if dose already exists with same vaccine and sequence
            existing_dose = None
            for dose in existing_doses:
                if (dose.vaccine_id == vaccine.id and 
                    getattr(dose, 'sequence_index', getattr(dose, 'series_seq', None)) == idx):
                    existing_dose = dose
                    break
            
            if existing_dose:
                dose = existing_dose
                print(f"Updating existing dose: {label}")
            else:
                dose = VaccineDose()
                print(f"Creating new dose: {label}")
            
            dose.vaccine = vaccine
            dose.series_key = "Influenza"
            _set_seq(dose, idx)
            dose.dose_label = label
            dose.min_offset_days = min_days
            dose.max_offset_days = None
            dose.anchor_policy = policy
            
            if sv and hasattr(dose, "schedule_version_id"):
                dose.schedule_version = sv
                
            dose.is_active = True
            
            doses_to_save.append((dose, prev_seq))

        # Save all doses
        for dose, _ in doses_to_save:
            try:
                dose.save()
            except Exception as e:
                print(f"Error saving dose {dose.dose_label}: {e}")
                # Try to update if it's a unique constraint error
                if 'unique' in str(e).lower():
                    # Find and update existing record
                    existing = VaccineDose.objects.filter(
                        vaccine=dose.vaccine,
                        schedule_version=sv,
                        **{('sequence_index' if hasattr(dose, 'sequence_index') else 'series_seq'): _set_seq(dose, 0) and getattr(dose, 'sequence_index', getattr(dose, 'series_seq', None))}
                    ).first()
                    if existing:
                        existing.series_key = dose.series_key
                        existing.dose_label = dose.dose_label
                        existing.min_offset_days = dose.min_offset_days
                        existing.max_offset_days = dose.max_offset_days
                        existing.anchor_policy = dose.anchor_policy
                        existing.is_active = True
                        existing.save()
                        # Replace in our list for relationship setting
                        doses_to_save = [(existing if d[0] == dose else d[0], d[1]) for d in doses_to_save]

        # Second pass: set previous dose relationships
        for idx, (dose, prev_seq) in enumerate(doses_to_save, start=1):
            if hasattr(dose, "previous_dose_id") and prev_seq:
                prev_dose = doses_to_save[prev_seq - 1][0]
                dose.previous_dose = prev_dose
                try:
                    dose.save(update_fields=["previous_dose_id"])
                except Exception as e:
                    print(f"Error setting previous dose for {dose.dose_label}: {e}")

def backwards(apps, schema_editor):
    # No-op - safe rollback not trivial
    pass

class Migration(migrations.Migration):
    dependencies = [
        ("vaccinations", "0013_vaccinedose_series_key_vaccinedose_series_seq"),
    ]
    
    operations = [
        migrations.RunPython(forwards, backwards),
    ]