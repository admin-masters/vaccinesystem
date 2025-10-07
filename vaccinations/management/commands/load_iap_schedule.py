# vaccinations/management/commands/load_iap_schedule.py
import csv
from django.core.management.base import BaseCommand
from vaccinations.models import ScheduleVersion, Vaccine, VaccineDose

class Command(BaseCommand):
    help = "Load IAP vaccination schedule from CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv-file',
            type=str,
            default='iap.csv',
            help='Path to the CSV file (default: iap.csv)',
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        
        self.stdout.write(f"Loading IAP vaccination schedule from {csv_file}...")
        
        # Create or get the schedule version
        schedule, created = ScheduleVersion.objects.using("masters").get_or_create(
            code="IAP-2025",
            defaults={
                "name": "Indian Academy of Pediatrics 2025",
                "source_url": "https://iapindia.org/",
                "is_current": True
            }
        )
        
        if created:
            self.stdout.write(f"✓ Created schedule version: {schedule.name}")
        else:
            self.stdout.write(f"Using existing schedule version: {schedule.name}")
        
        vaccines_created = 0
        doses_created = 0
        
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
                    
                    # Normalize vaccine name to group doses properly
                    normalized_name = self.normalize_vaccine_name(vaccine_name)
                    vaccine_code = normalized_name.lower().replace(' ', '_').replace('/', '_')
                    
                    # Create or get vaccine
                    vaccine, v_created = Vaccine.objects.using("masters").get_or_create(
                        schedule_version=schedule,
                        code=vaccine_code,
                        defaults={
                            "name": normalized_name,
                            "is_active": True
                        }
                    )
                    
                    if v_created:
                        vaccines_created += 1
                        self.stdout.write(f"  ✓ Created vaccine: {vaccine_name}")
                    
                    # Determine sequence index
                    existing_doses = VaccineDose.objects.using("masters").filter(
                        schedule_version=schedule,
                        vaccine=vaccine
                    ).count()
                    sequence_index = existing_doses + 1
                    
                    # Find previous dose if this is a booster
                    previous_dose = None
                    if is_booster and previous_vaccine and previous_vaccine != '-':
                        try:
                            prev_vaccine_code = previous_vaccine.lower().replace(' ', '_').replace('/', '_')
                            prev_vaccine = Vaccine.objects.using("masters").get(
                                schedule_version=schedule,
                                code=prev_vaccine_code
                            )
                            previous_dose = VaccineDose.objects.using("masters").filter(
                                schedule_version=schedule,
                                vaccine=prev_vaccine
                            ).first()
                        except Vaccine.DoesNotExist:
                            self.stdout.write(f"⚠ Previous vaccine '{previous_vaccine}' not found for {vaccine_name}")
                    
                    # Create vaccine dose
                    dose_label = f"Dose {sequence_index}" if sequence_index > 1 else "Primary"
                    
                    dose, d_created = VaccineDose.objects.using("masters").get_or_create(
                        schedule_version=schedule,
                        vaccine=vaccine,
                        sequence_index=sequence_index,
                        defaults={
                            "dose_label": dose_label,
                            "min_offset_days": offset_days,
                            "max_offset_days": offset_days + 30,  # Allow 30 day window
                            "is_booster": is_booster,
                            "previous_dose": previous_dose,
                            "anchor_policy": "L"  # Later of age and interval
                        }
                    )
                    
                    if d_created:
                        doses_created += 1
                        self.stdout.write(f"    ✓ Created dose: {vaccine_name} - {dose_label} (Day {offset_days})")
        
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"❌ CSV file '{csv_file}' not found"))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error reading CSV: {e}"))
            return
        
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Successfully loaded IAP schedule!"))
        self.stdout.write(f"  - Created {vaccines_created} vaccines")
        self.stdout.write(f"  - Created {doses_created} vaccine doses")
        self.stdout.write(f"  - Total vaccines: {Vaccine.objects.using('masters').count()}")
        self.stdout.write(f"  - Total doses: {VaccineDose.objects.using('masters').count()}")

    def parse_time_period(self, time_period):
        """Parse time period string to days"""
        time_period = time_period.lower().strip()
        
        if time_period == "0 days" or time_period == "birth":
            return 0
        elif "weeks" in time_period:
            try:
                weeks = int(time_period.split()[0])
                return weeks * 7
            except (ValueError, IndexError):
                return None
        elif "months" in time_period:
            try:
                # Handle ranges like "6-9 months", "12-15 months", "16-18 months", "18-19 months"
                if "�" in time_period or "-" in time_period:
                    # Take the first number from range
                    import re
                    match = re.search(r'(\d+)', time_period)
                    if match:
                        months = int(match.group(1))
                        return months * 30
                else:
                    months = int(time_period.split()[0])
                    return months * 30  # Approximate
            except (ValueError, IndexError):
                return None
        elif "years" in time_period:
            try:
                # Handle ranges like "4-6 years", "9-15 years", "10-12 years"
                if "�" in time_period or "-" in time_period:
                    import re
                    match = re.search(r'(\d+)', time_period)
                    if match:
                        years = int(match.group(1))
                        return years * 365
                else:
                    years = int(time_period.split()[0])
                    return years * 365  # Approximate
            except (ValueError, IndexError):
                return None
        elif "year" in time_period:
            # Handle "2nd year", "3rd year", etc.
            import re
            match = re.search(r'(\d+)', time_period)
            if match:
                years = int(match.group(1))
                return years * 365
        
        return None

    def normalize_vaccine_name(self, vaccine_name):
        """Normalize vaccine names to group doses properly"""
        name = vaccine_name.strip()
        
        # Remove dose numbers and suffixes
        import re
        
        # Patterns to normalize
        patterns = [
            (r'^(Hep B)\d+$', r'\1'),  # Hep B1, Hep B2, etc. -> Hep B
            (r'^(DTwP / DTaP)\d*$', r'\1'),  # DTwP / DTaP1, DTwP / DTaP2, etc. -> DTwP / DTaP
            (r'^(Hib)-?\d+$', r'\1'),  # Hib-1, Hib-2, etc. -> Hib
            (r'^(IPV)-?\d+$', r'\1'),  # IPV-1, IPV-2, etc. -> IPV
            (r'^(PCV)\s+\d+$', r'\1'),  # PCV 1, PCV 2, etc. -> PCV
            (r'^(Rota)-?\d+\*?$', r'\1'),  # Rota-1, Rota-2, Rota-3* -> Rota
            (r'^(Influenza)-?\d+$', r'\1'),  # Influenza-1, Influenza-2 -> Influenza
            (r'^(MMR)\s+\d+.*$', r'\1'),  # MMR 1 (Measles, Mumps, Rubella), MMR 2, MMR 3 -> MMR
            (r'^(Hepatitis A)-?\d+\*?\*?$', r'\1'),  # Hepatitis A-1, Hepatitis A-2** -> Hepatitis A
            (r'^(Varicella)\s*\d*$', r'\1'),  # Varicella, Varicella 2 -> Varicella
        ]
        
        for pattern, replacement in patterns:
            if re.match(pattern, name):
                return re.sub(pattern, replacement, name)
        
        # Special cases
        if 'Annual Influenza' in name:
            return 'Influenza'
        if 'Typhoid Conjugate' in name:
            return 'Typhoid Conjugate Vaccine'
        if 'HPV' in name:
            return 'HPV'
        if 'Tdap / Td' in name:
            return 'Tdap/Td'
        if 'PCV Booster' in name:
            return 'PCV Booster'
        
        return name
