from django.core.management.base import BaseCommand
from django.db import transaction
from vaccinations.models import Doctor, DoctorSessionToken, OAuthState


class Command(BaseCommand):
    help = 'Clear only doctor data with proper database routing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletion without interactive prompt',
        )

    def handle(self, *args, **options):
        # Count records before deletion with proper database routing
        doctors_count = Doctor.objects.using("masters").count()
        session_tokens_count = DoctorSessionToken.objects.using("patients").count()
        oauth_states_count = OAuthState.objects.using("patients").count()

        self.stdout.write(f"📊 Doctor Data Count:")
        self.stdout.write(f"   Doctors (masters DB): {doctors_count}")
        self.stdout.write(f"   Doctor Sessions (patients DB): {session_tokens_count}")
        self.stdout.write(f"   OAuth States (patients DB): {oauth_states_count}")

        total_records = doctors_count + session_tokens_count + oauth_states_count

        if total_records == 0:
            self.stdout.write(self.style.SUCCESS("✅ No doctor data to delete."))
            return

        if not options['confirm']:
            confirm = input(f"\n⚠️ Are you sure you want to delete ALL {total_records} doctor records? This action cannot be undone. (yes/no): ")
            if confirm.lower() != 'yes':
                self.stdout.write("❌ Deletion cancelled.")
                return

        self.stdout.write("🗑️ Starting doctor data deletion...")

        try:
            # Delete OAuth States first (patients DB)
            if oauth_states_count > 0:
                deleted_oauth = OAuthState.objects.using("patients").all().delete()
                self.stdout.write(f"   ✅ Deleted {deleted_oauth[0]} OAuth states")

            # Delete Doctor Session Tokens (patients DB)
            if session_tokens_count > 0:
                deleted_sessions = DoctorSessionToken.objects.using("patients").all().delete()
                self.stdout.write(f"   ✅ Deleted {deleted_sessions[0]} doctor sessions")

            # Delete Doctors (masters DB)
            if doctors_count > 0:
                deleted_doctors = Doctor.objects.using("masters").all().delete()
                self.stdout.write(f"   ✅ Deleted {deleted_doctors[0]} doctors")

            self.stdout.write(self.style.SUCCESS(f"\n🎉 Successfully deleted all {total_records} doctor records!"))
            self.stdout.write("📊 Patient and vaccine data preserved.")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error during deletion: {e}"))
            import traceback
            traceback.print_exc()
