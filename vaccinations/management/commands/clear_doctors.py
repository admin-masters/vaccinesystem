from django.core.management.base import BaseCommand
from vaccinations.models import Doctor, Clinic, Partner, FieldRepresentative

class Command(BaseCommand):
    help = 'Delete all doctors from the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Skip confirmation prompt',
        )

    def handle(self, *args, **options):
        doctor_count = Doctor.objects.count()
        
        if doctor_count == 0:
            self.stdout.write(self.style.WARNING('No doctors found in the database.'))
            return

        if not options['force']:
            confirm = input(f'Are you sure you want to delete {doctor_count} doctors? This action cannot be undone. (yes/no): ')
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.WARNING('Operation cancelled.'))
                return

        # Delete all doctors
        deleted_doctors = Doctor.objects.all()
        doctor_names = [doctor.full_name for doctor in deleted_doctors]
        
        # Delete doctors (this will cascade to related sessions)
        deleted_count, _ = Doctor.objects.all().delete()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {deleted_count} doctors:')
        )
        
        for name in doctor_names:
            self.stdout.write(f'  - {name}')
        
        # Check if there are any orphaned clinics (not used by any doctors)
        orphaned_clinics = Clinic.objects.filter(doctors__isnull=True)
        if orphaned_clinics.exists():
            self.stdout.write(
                self.style.WARNING(f'\nFound {orphaned_clinics.count()} orphaned clinics (not used by any doctors):')
            )
            for clinic in orphaned_clinics:
                self.stdout.write(f'  - {clinic.name}')
            
            delete_clinics = input('\nDo you want to delete these orphaned clinics? (yes/no): ')
            if delete_clinics.lower() == 'yes':
                clinic_count, _ = orphaned_clinics.delete()
                self.stdout.write(
                    self.style.SUCCESS(f'Deleted {clinic_count} orphaned clinics.')
                )
            else:
                self.stdout.write('Orphaned clinics kept.')
        
        # Check if there are any orphaned partners
        orphaned_partners = Partner.objects.filter(doctors__isnull=True)
        if orphaned_partners.exists():
            self.stdout.write(
                self.style.WARNING(f'\nFound {orphaned_partners.count()} orphaned partners (not used by any doctors):')
            )
            for partner in orphaned_partners:
                self.stdout.write(f'  - {partner.name}')
            
            delete_partners = input('\nDo you want to delete these orphaned partners? (yes/no): ')
            if delete_partners.lower() == 'yes':
                partner_count, _ = orphaned_partners.delete()
                self.stdout.write(
                    self.style.SUCCESS(f'Deleted {partner_count} orphaned partners.')
                )
            else:
                self.stdout.write('Orphaned partners kept.')
        
        self.stdout.write(
            self.style.SUCCESS(f'\nOperation completed. Deleted {deleted_count} doctors.')
        )