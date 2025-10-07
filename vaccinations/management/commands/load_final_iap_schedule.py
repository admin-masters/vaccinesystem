# vaccinations/management/commands/load_final_iap_schedule.py
import csv
import re
from django.core.management.base import BaseCommand
from vaccinations.models import ScheduleVersion, Vaccine, VaccineDose

class Command(BaseCommand):
    help = "Load final IAP vaccination schedule exactly as specified"

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv-file',
            type=str,
            default='iap_final.csv',
            help='Path to the final IAP CSV file (default: iap_final.csv)',
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        
        self.stdout.write(f"Loading Final IAP vaccination schedule from {csv_file}...")
        
        # Clear existing data
        self.stdout.write("Clearing existing vaccine data...")
        VaccineDose.objects.using("default").all().delete()
        Vaccine.objects.using("default").all().delete()
        ScheduleVersion.objects.using("default").all().delete()
        
        # Create schedule version
        schedule = ScheduleVersion.objects.using("default").create(
            code="IAP-2025-FINAL",
            name="Indian Academy of Pediatrics 2025 - Final Schedule",
            source_url="https://iapindia.org/",
            is_current=True
        )
        
        self.stdout.write(f"✓ Created schedule version: {schedule.name}")
        
        vaccines_created = {}
        doses_created = []
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row_num, row in enumerate(reader, start=2):
                    time_period = row['Time Period'].strip()
                    vaccine_name = row['Vaccines'].strip()
                    is_booster = row['Booster Yes/No'].strip().lower() == 'yes'
                    previous_vaccine = row['Previous Vaccine'].strip()
                    
                    if not vaccine_name or vaccine_name == '-':
                        continue
                    
                    # Parse time period to get offset days
                    offset_days = self.parse_time_period(time_period)
                    if offset_days is None:
                        self.stdout.write(f"⚠ Skipping row {row_num}: Could not parse time period '{time_period}'")
                        continue
                    
                    # Clean vaccine name (remove asterisks, quotes, etc.)
                    clean_vaccine_name = vaccine_name.replace('*', '').replace('"', '').strip()
                    
                    # Create or get vaccine
                    vaccine_code = self.generate_vaccine_code(clean_vaccine_name)
                    
                    if vaccine_code not in vaccines_created:
                        vaccine = Vaccine.objects.using("default").create(
                            schedule_version=schedule,
                            code=vaccine_code,
                            name=clean_vaccine_name,
                            is_active=True
                        )
                        vaccines_created[vaccine_code] = vaccine
                        self.stdout.write(f"  ✓ Created vaccine: {clean_vaccine_name}")
                    else:
                        vaccine = vaccines_created[vaccine_code]
                    
                    # Determine sequence index
                    existing_doses_count = len([d for d in doses_created if d['vaccine_code'] == vaccine_code])
                    sequence_index = existing_doses_count + 1
                    
                    # Create dose label
                    if sequence_index == 1:
                        dose_label = clean_vaccine_name
                    else:
                        dose_label = f"{clean_vaccine_name} - Dose {sequence_index}"
                    
                    # Store dose info for later creation (after all vaccines are created)
                    dose_info = {
                        'vaccine_code': vaccine_code,
                        'vaccine': vaccine,
                        'sequence_index': sequence_index,
                        'dose_label': dose_label,
                        'min_offset_days': offset_days,
                        'max_offset_days': offset_days + 30,  # 30-day window
                        'is_booster': is_booster,
                        'previous_vaccine_name': previous_vaccine if previous_vaccine != '-' else None,
                        'original_vaccine_name': vaccine_name
                    }
                    doses_created.append(dose_info)
        
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"❌ CSV file '{csv_file}' not found"))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error reading CSV: {e}"))
            return
        
        # Create doses and set up previous_dose relationships
        self.stdout.write("Creating vaccine doses...")
        dose_objects = {}
        
        for dose_info in doses_created:
            dose = VaccineDose.objects.using("default").create(
                schedule_version=schedule,
                vaccine=dose_info['vaccine'],
                sequence_index=dose_info['sequence_index'],
                dose_label=dose_info['dose_label'],
                min_offset_days=dose_info['min_offset_days'],
                max_offset_days=dose_info['max_offset_days'],
                is_booster=dose_info['is_booster'],
                anchor_policy="L"  # Later of age and interval
            )
            
            # Store for previous_dose linking
            dose_objects[dose_info['original_vaccine_name']] = dose
            
            self.stdout.write(f"    ✓ Created dose: {dose_info['dose_label']} (Day {dose_info['min_offset_days']})")
        
        # Second pass: Set up previous_dose relationships
        self.stdout.write("Setting up dose dependencies...")
        for dose_info in doses_created:
            if dose_info['previous_vaccine_name']:
                dose = dose_objects[dose_info['original_vaccine_name']]
                previous_dose = dose_objects.get(dose_info['previous_vaccine_name'])
                
                if previous_dose:
                    dose.previous_dose = previous_dose
                    dose.save(using="default", update_fields=['previous_dose'])
                    self.stdout.write(f"    ✓ Linked {dose.dose_label} -> {previous_dose.dose_label}")
                else:
                    self.stdout.write(f"    ⚠ Previous dose not found: {dose_info['previous_vaccine_name']}")
        
        # Summary
        total_vaccines = Vaccine.objects.using("default").count()
        total_doses = VaccineDose.objects.using("default").count()
        
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Successfully loaded Final IAP schedule!"))
        self.stdout.write(f"  - Created {total_vaccines} vaccines")
        self.stdout.write(f"  - Created {total_doses} vaccine doses")
        self.stdout.write(f"  - Schedule: {schedule.name}")

    def parse_time_period(self, time_period):
        """Parse time period string to days"""
        time_period = time_period.lower().strip()
        
        if time_period == "birth":
            return 0
        elif "weeks" in time_period:
            try:
                weeks = int(re.search(r'(\d+)', time_period).group(1))
                return weeks * 7
            except (ValueError, AttributeError):
                return None
        elif "months" in time_period:
            try:
                # Handle ranges like "6–9 months", "12–15 months"
                match = re.search(r'(\d+)', time_period)
                if match:
                    months = int(match.group(1))
                    return months * 30
            except (ValueError, AttributeError):
                return None
        elif "years" in time_period:
            try:
                # Handle ranges like "4–6 years", "9–15 years"
                match = re.search(r'(\d+)', time_period)
                if match:
                    years = int(match.group(1))
                    return years * 365
            except (ValueError, AttributeError):
                return None
        elif "year" in time_period:
            # Handle "2nd year", "3rd year", etc.
            match = re.search(r'(\d+)', time_period)
            if match:
                years = int(match.group(1))
                return years * 365
        
        return None

    def generate_vaccine_code(self, vaccine_name):
        """Generate a clean vaccine code"""
        # Remove special characters and normalize
        code = re.sub(r'[^\w\s-]', '', vaccine_name.lower())
        code = re.sub(r'\s+', '_', code)
        code = code.replace('__', '_').strip('_')
        return code[:50]  # Limit to 50 chars
