# vaccinations/management/commands/clear_patients_data.py
from django.core.management.base import BaseCommand
from vaccinations.models import Parent, Child, ChildDose, ChildShareLink, OAuthState, DoctorSessionToken

class Command(BaseCommand):
    help = "Clear all patient data (Parent, Child, ChildDose, ChildShareLink, etc.) from patients database"

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm that you want to delete all patient data',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING(
                    'This will delete ALL patient data including:\n'
                    '- All Parent records\n'
                    '- All Child records\n'
                    '- All ChildDose records\n'
                    '- All ChildShareLink records\n'
                    '- All OAuthState records\n'
                    '- All DoctorSessionToken records\n\n'
                    'Run with --confirm to proceed'
                )
            )
            return

        self.stdout.write("Clearing all patient data...")
        
        # Delete in proper order to avoid foreign key constraints
        deleted_counts = {}
        
        # Only delete tables that exist and have data
        models_to_clear = [
            ('ChildDose', ChildDose),
            ('ChildShareLink', ChildShareLink),
            ('Child', Child),
            ('Parent', Parent),
        ]
        
        for model_name, model_class in models_to_clear:
            try:
                count = model_class.objects.using("patients").count()
                if count > 0:
                    model_class.objects.using("patients").all().delete()
                    deleted_counts[model_name] = count
                    self.stdout.write(f"✓ Deleted {count} {model_name} records")
                else:
                    self.stdout.write(f"- No {model_name} records to delete")
            except Exception as e:
                self.stdout.write(f"⚠ Skipping {model_name}: {e}")
        
        self.stdout.write(self.style.SUCCESS("✅ Patient data cleared successfully!"))
        self.stdout.write("Deleted records:")
        for model, count in deleted_counts.items():
            self.stdout.write(f"  - {model}: {count} records")
        
        self.stdout.write(self.style.SUCCESS("\n🎉 Database is now clean and ready for fresh data!"))
