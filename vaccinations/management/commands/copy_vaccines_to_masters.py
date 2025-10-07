# vaccinations/management/commands/copy_vaccines_to_masters.py
from django.core.management.base import BaseCommand
from vaccinations.models import ScheduleVersion, Vaccine, VaccineDose

class Command(BaseCommand):
    help = "Copy vaccine data from clinic_db (default) to masters database"

    def handle(self, *args, **opts):
        self.stdout.write("Copying vaccine data from clinic_db to masters database...")
        
        # Clear existing data in masters
        self.stdout.write("Clearing existing data in masters...")
        VaccineDose.objects.using("masters").all().delete()
        Vaccine.objects.using("masters").all().delete()
        ScheduleVersion.objects.using("masters").all().delete()
        
        # Copy ScheduleVersion
        source_schedules = ScheduleVersion.objects.using("default").all()
        for schedule in source_schedules:
            new_schedule = ScheduleVersion(
                code=schedule.code,
                name=schedule.name,
                source_url=schedule.source_url,
                effective_from=schedule.effective_from,
                is_current=schedule.is_current,
                created_at=schedule.created_at
            )
            new_schedule.save(using="masters")
            self.stdout.write(f"✓ Copied schedule: {schedule.name}")
        
        # Copy Vaccines
        source_vaccines = Vaccine.objects.using("default").all().order_by('id')
        vaccine_id_mapping = {}
        
        for vaccine in source_vaccines:
            # Get the corresponding schedule in masters
            masters_schedule = ScheduleVersion.objects.using("masters").get(code=vaccine.schedule_version.code)
            
            new_vaccine = Vaccine(
                schedule_version=masters_schedule,
                code=vaccine.code,
                name=vaccine.name,
                aliases=vaccine.aliases,
                is_active=vaccine.is_active,
                notes=vaccine.notes,
                education_parent_url=vaccine.education_parent_url,
                education_doctor_vimeo_url=vaccine.education_doctor_vimeo_url,
                created_at=vaccine.created_at
            )
            new_vaccine.save(using="masters")
            vaccine_id_mapping[vaccine.id] = new_vaccine.id
            self.stdout.write(f"✓ Copied vaccine: {vaccine.name}")
        
        # Copy VaccineDoses
        source_doses = VaccineDose.objects.using("default").all().order_by('id')
        dose_id_mapping = {}
        
        # First pass: create all doses without previous_dose relationships
        for dose in source_doses:
            masters_vaccine = Vaccine.objects.using("masters").get(id=vaccine_id_mapping[dose.vaccine_id])
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
                anchor_policy=dose.anchor_policy,
                series_key=dose.series_key,
                series_seq=dose.series_seq,
                notes=dose.notes,
                created_at=dose.created_at
            )
            new_dose.save(using="masters")
            dose_id_mapping[dose.id] = new_dose.id
            self.stdout.write(f"✓ Copied dose: {dose.vaccine.name} - {dose.dose_label}")
        
        # Second pass: update previous_dose relationships
        for dose in source_doses:
            if dose.previous_dose_id:
                new_dose = VaccineDose.objects.using("masters").get(id=dose_id_mapping[dose.id])
                previous_dose = VaccineDose.objects.using("masters").get(id=dose_id_mapping[dose.previous_dose_id])
                new_dose.previous_dose = previous_dose
                new_dose.save(using="masters", update_fields=['previous_dose'])
        
        # Summary
        masters_schedules = ScheduleVersion.objects.using("masters").count()
        masters_vaccines = Vaccine.objects.using("masters").count()
        masters_doses = VaccineDose.objects.using("masters").count()
        
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Successfully copied vaccine data to masters!"))
        self.stdout.write(f"  - Schedule Versions: {masters_schedules}")
        self.stdout.write(f"  - Vaccines: {masters_vaccines}")
        self.stdout.write(f"  - Vaccine Doses: {masters_doses}")
        self.stdout.write("\nMasters database now has the correct vaccine data from clinic_db!")
