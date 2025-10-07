# vaccinations/management/commands/load_exact_iap_schedule.py
import csv
import re
from django.core.management.base import BaseCommand
from vaccinations.models import ScheduleVersion, Vaccine, VaccineDose

class Command(BaseCommand):
    help = "Load exact IAP vaccination schedule as per the provided CSV format"

    def handle(self, *args, **options):
        self.stdout.write("Loading EXACT IAP vaccination schedule...")
        
        # Clear existing data
        self.stdout.write("Clearing existing vaccine data...")
        from django.db import connections
        cursor = connections['default'].cursor()
        cursor.execute('SET FOREIGN_KEY_CHECKS = 0')
        cursor.execute('DELETE FROM vaccine_dose')
        cursor.execute('DELETE FROM vaccine') 
        cursor.execute('DELETE FROM schedule_version')
        cursor.execute('SET FOREIGN_KEY_CHECKS = 1')
        
        # Clear ChildDose records too
        cursor = connections['patients'].cursor()
        cursor.execute('DELETE FROM child_dose')
        
        # Create schedule version
        schedule = ScheduleVersion.objects.using("default").create(
            code="IAP-2025-EXACT",
            name="Indian Academy of Pediatrics 2025 - Exact Schedule",
            source_url="https://iapindia.org/",
            is_current=True
        )
        
        self.stdout.write(f"✓ Created schedule version: {schedule.name}")
        
        # Define exact IAP schedule as per your CSV
        iap_schedule = [
            # Birth vaccines
            {"time": "Birth", "vaccine": "BCG", "booster": False, "previous": None, "days": 0},
            {"time": "Birth", "vaccine": "Hep B1", "booster": False, "previous": None, "days": 0},
            {"time": "Birth", "vaccine": "OPV", "booster": False, "previous": None, "days": 0},
            
            # 6 weeks vaccines
            {"time": "6 weeks", "vaccine": "DTwP / DTaP1", "booster": False, "previous": None, "days": 42},
            {"time": "6 weeks", "vaccine": "Hib-1", "booster": False, "previous": None, "days": 42},
            {"time": "6 weeks", "vaccine": "IPV-1", "booster": False, "previous": None, "days": 42},
            {"time": "6 weeks", "vaccine": "Hep B2", "booster": True, "previous": "Hep B1", "days": 42},
            {"time": "6 weeks", "vaccine": "PCV 1", "booster": False, "previous": None, "days": 42},
            {"time": "6 weeks", "vaccine": "Rota-1", "booster": False, "previous": None, "days": 42},
            
            # 10 weeks vaccines
            {"time": "10 weeks", "vaccine": "DTwP / DTaP2", "booster": True, "previous": "DTwP / DTaP1", "days": 70},
            {"time": "10 weeks", "vaccine": "Hib-2", "booster": True, "previous": "Hib-1", "days": 70},
            {"time": "10 weeks", "vaccine": "IPV-2", "booster": True, "previous": "IPV-1", "days": 70},
            {"time": "10 weeks", "vaccine": "Hep B3", "booster": True, "previous": "Hep B2", "days": 70},
            {"time": "10 weeks", "vaccine": "PCV 2", "booster": True, "previous": "PCV 1", "days": 70},
            {"time": "10 weeks", "vaccine": "Rota-2", "booster": True, "previous": "Rota-1", "days": 70},
            
            # 14 weeks vaccines
            {"time": "14 Weeks", "vaccine": "DTwP / DTaP3", "booster": True, "previous": "DTwP / DTaP2", "days": 98},
            {"time": "14 Weeks", "vaccine": "Hib-3", "booster": True, "previous": "Hib-2", "days": 98},
            {"time": "14 Weeks", "vaccine": "IPV-3", "booster": True, "previous": "IPV-2", "days": 98},
            {"time": "14 Weeks", "vaccine": "Hep B4", "booster": True, "previous": "Hep B3", "days": 98},
            {"time": "14 Weeks", "vaccine": "PCV 3", "booster": True, "previous": "PCV 2", "days": 98},
            {"time": "14 Weeks", "vaccine": "Rota-3*", "booster": True, "previous": "Rota-2", "days": 98},
            
            # 6-7 months vaccines
            {"time": "6 Months", "vaccine": "Influenza-1", "booster": False, "previous": None, "days": 180},
            {"time": "7 Months", "vaccine": "Influenza-2", "booster": True, "previous": "Influenza-1", "days": 210},
            {"time": "6–9 Months", "vaccine": "Typhoid Conjugate Vaccine", "booster": False, "previous": None, "days": 180},
            
            # 9-15 months vaccines
            {"time": "9 Months", "vaccine": "MMR 1 (Measles, Mumps, Rubella)", "booster": False, "previous": None, "days": 270},
            {"time": "12 Months", "vaccine": "Hepatitis A-1", "booster": False, "previous": None, "days": 360},
            {"time": "12–15 Months", "vaccine": "PCV Booster", "booster": True, "previous": "PCV 3", "days": 360},
            {"time": "15 Months", "vaccine": "MMR 2", "booster": True, "previous": "MMR 1 (Measles, Mumps, Rubella)", "days": 450},
            {"time": "15 Months", "vaccine": "Varicella", "booster": False, "previous": None, "days": 450},
            
            # 16-19 months vaccines
            {"time": "16–18 Months", "vaccine": "DTwP / DTaP", "booster": True, "previous": "DTwP / DTaP3", "days": 480},
            {"time": "16–18 Months", "vaccine": "Hib", "booster": True, "previous": "Hib-3", "days": 480},
            {"time": "16–18 Months", "vaccine": "IPV", "booster": True, "previous": "IPV-3", "days": 480},
            {"time": "18–19 Months", "vaccine": "Hepatitis A-2**", "booster": True, "previous": "Hepatitis A-1", "days": 540},
            {"time": "18–19 Months", "vaccine": "Varicella 2", "booster": True, "previous": "Varicella", "days": 540},
            
            # 4-6 years vaccines
            {"time": "4–6 Years", "vaccine": "DTwP / DTaP", "booster": True, "previous": "DTwP / DTaP (16–18 Months)", "days": 1460},
            {"time": "4–6 Years", "vaccine": "IPV", "booster": True, "previous": "IPV (16–18 Months)", "days": 1460},
            {"time": "4–6 Years", "vaccine": "MMR 3", "booster": True, "previous": "MMR 2", "days": 1460},
            
            # Later vaccines
            {"time": "9–15 Years (Girls)", "vaccine": "HPV (2 doses)", "booster": False, "previous": None, "days": 3285},
            {"time": "10–12 Years", "vaccine": "Tdap / Td", "booster": True, "previous": "DTwP / DTaP (4–6 Years)", "days": 3650},
            
            # Annual influenza vaccines
            {"time": "2nd Year", "vaccine": "Annual Influenza Vaccine", "booster": True, "previous": "Influenza-2", "days": 730},
            {"time": "3rd Year", "vaccine": "Annual Influenza Vaccine", "booster": True, "previous": "Previous Influenza dose", "days": 1095},
            {"time": "4th Year", "vaccine": "Annual Influenza Vaccine", "booster": True, "previous": "Previous Influenza dose", "days": 1460},
            {"time": "5th Year", "vaccine": "Annual Influenza Vaccine", "booster": True, "previous": "Previous Influenza dose", "days": 1825},
        ]
        
        # Create vaccines and doses
        vaccine_objects = {}
        dose_objects = {}
        
        for entry in iap_schedule:
            vaccine_name = entry["vaccine"]
            
            # Create vaccine if not exists
            vaccine_code = self.generate_vaccine_code(vaccine_name)
            
            if vaccine_code not in vaccine_objects:
                vaccine = Vaccine.objects.using("default").create(
                    schedule_version=schedule,
                    code=vaccine_code,
                    name=vaccine_name,
                    is_active=True
                )
                vaccine_objects[vaccine_code] = vaccine
                self.stdout.write(f"  ✓ Created vaccine: {vaccine_name}")
            else:
                vaccine = vaccine_objects[vaccine_code]
            
            # Create dose
            dose = VaccineDose.objects.using("default").create(
                schedule_version=schedule,
                vaccine=vaccine,
                sequence_index=1,  # Will be updated later
                dose_label=vaccine_name,
                min_offset_days=entry["days"],
                max_offset_days=entry["days"] + 30,
                is_booster=entry["booster"],
                anchor_policy="L"
            )
            
            dose_objects[vaccine_name] = dose
            self.stdout.write(f"    ✓ Created dose: {vaccine_name} (Day {entry['days']})")
        
        # Second pass: Set up previous_dose relationships
        self.stdout.write("Setting up dose dependencies...")
        for entry in iap_schedule:
            if entry["previous"]:
                dose = dose_objects[entry["vaccine"]]
                previous_dose = dose_objects.get(entry["previous"])
                
                if previous_dose:
                    dose.previous_dose = previous_dose
                    dose.save(using="default", update_fields=['previous_dose'])
                    self.stdout.write(f"    ✓ Linked {entry['vaccine']} -> {entry['previous']}")
                else:
                    # Handle special cases like "DTwP / DTaP (16–18 Months)"
                    if "16–18 Months" in entry["previous"]:
                        prev_dose = dose_objects.get("DTwP / DTaP")
                        if prev_dose:
                            dose.previous_dose = prev_dose
                            dose.save(using="default", update_fields=['previous_dose'])
                            self.stdout.write(f"    ✓ Linked {entry['vaccine']} -> DTwP / DTaP (16-18M)")
                    elif "4–6 Years" in entry["previous"]:
                        # Find the 4-6 years DTaP dose
                        for dose_name, dose_obj in dose_objects.items():
                            if "DTwP / DTaP" in dose_name and dose_obj.min_offset_days == 1460:
                                dose.previous_dose = dose_obj
                                dose.save(using="default", update_fields=['previous_dose'])
                                break
                    else:
                        self.stdout.write(f"    ⚠ Previous dose not found: {entry['previous']}")
        
        # Summary
        total_vaccines = Vaccine.objects.using("default").count()
        total_doses = VaccineDose.objects.using("default").count()
        
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Successfully loaded EXACT IAP schedule!"))
        self.stdout.write(f"  - Created {total_vaccines} vaccines")
        self.stdout.write(f"  - Created {total_doses} vaccine doses")
        self.stdout.write(f"  - Exact names and dates as per IAP CSV")
        
        self.stdout.write(f"\nNext step: Run 'python manage.py backfill_child_doses_from_clinic' to regenerate ChildDose records")

    def generate_vaccine_code(self, vaccine_name):
        """Generate a clean vaccine code"""
        code = re.sub(r'[^\w\s-]', '', vaccine_name.lower())
        code = re.sub(r'\s+', '_', code)
        code = code.replace('__', '_').strip('_')
        return code[:50]
