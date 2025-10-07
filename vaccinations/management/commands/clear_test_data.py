from django.core.management.base import BaseCommand
from django.db import transaction
from vaccinations.models import Doctor, Child, Parent, ChildDose, ChildShareLink, OAuthState, DoctorSessionToken


class Command(BaseCommand):
    help = 'Clear all test data - doctors, children, parents, and related records'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm that you want to delete all data',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING(
                    'This will delete ALL doctors, children, parents and related data.\n'
                    'Run with --confirm to proceed.'
                )
            )
            return

        with transaction.atomic():
            # Delete in proper order to avoid foreign key constraints
            
            # Delete child doses first
            try:
                child_dose_count = ChildDose.objects.using('patients').count()
                ChildDose.objects.using('patients').all().delete()
                self.stdout.write(f'Deleted {child_dose_count} child doses')
            except Exception as e:
                self.stdout.write(f'Could not delete child doses: {e}')
            
            # Delete child share links
            try:
                share_link_count = ChildShareLink.objects.using('patients').count()
                ChildShareLink.objects.using('patients').all().delete()
                self.stdout.write(f'Deleted {share_link_count} child share links')
            except Exception as e:
                self.stdout.write(f'Could not delete child share links: {e}')
            
            # Delete OAuth states
            try:
                oauth_count = OAuthState.objects.using('patients').count()
                OAuthState.objects.using('patients').all().delete()
                self.stdout.write(f'Deleted {oauth_count} OAuth states')
            except Exception as e:
                self.stdout.write(f'Could not delete OAuth states: {e}')
            
            # Delete doctor session tokens
            try:
                token_count = DoctorSessionToken.objects.using('patients').count()
                DoctorSessionToken.objects.using('patients').all().delete()
                self.stdout.write(f'Deleted {token_count} doctor session tokens')
            except Exception as e:
                self.stdout.write(f'Could not delete doctor session tokens: {e}')
            
            # Delete children
            try:
                child_count = Child.objects.using('patients').count()
                Child.objects.using('patients').all().delete()
                self.stdout.write(f'Deleted {child_count} children')
            except Exception as e:
                self.stdout.write(f'Could not delete children: {e}')
            
            # Delete parents
            try:
                parent_count = Parent.objects.using('patients').count()
                Parent.objects.using('patients').all().delete()
                self.stdout.write(f'Deleted {parent_count} parents')
            except Exception as e:
                self.stdout.write(f'Could not delete parents: {e}')
            
            # Delete doctors
            try:
                doctor_count = Doctor.objects.using('masters').count()
                Doctor.objects.using('masters').all().delete()
                self.stdout.write(f'Deleted {doctor_count} doctors')
            except Exception as e:
                self.stdout.write(f'Could not delete doctors: {e}')

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully cleared all test data!'
            )
        )
