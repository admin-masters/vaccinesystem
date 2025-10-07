from django.core.management.base import BaseCommand
from django.db import transaction
from vaccinations.models import Doctor, Parent, Child, ChildDose, DoctorSessionToken, OAuthState, ChildShareLink


class Command(BaseCommand):
    help = 'Clear all doctor, parent, and child data from the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletion without interactive prompt',
        )

    def handle(self, *args, **options):
        # Count records before deletion
        doctors_count = Doctor.objects.using("masters").count()
        parents_count = Parent.objects.using("patients").count()
        children_count = Child.objects.using("patients").count()
        child_doses_count = ChildDose.objects.using("patients").count()
        session_tokens_count = DoctorSessionToken.objects.using("patients").count()
        oauth_states_count = OAuthState.objects.using("patients").count()
        share_links_count = ChildShareLink.objects.using("patients").count()

        self.stdout.write(f"📊 Current Data Count:")
        self.stdout.write(f"   Doctors (masters): {doctors_count}")
        self.stdout.write(f"   Parents (patients): {parents_count}")
        self.stdout.write(f"   Children (patients): {children_count}")
        self.stdout.write(f"   Child Doses (patients): {child_doses_count}")
        self.stdout.write(f"   Doctor Sessions (patients): {session_tokens_count}")
        self.stdout.write(f"   OAuth States (patients): {oauth_states_count}")
        self.stdout.write(f"   Share Links (patients): {share_links_count}")

        total_records = (doctors_count + parents_count + children_count + 
                        child_doses_count + session_tokens_count + oauth_states_count + share_links_count)

        if total_records == 0:
            self.stdout.write(self.style.SUCCESS("✅ No data to delete."))
            return

        if not options['confirm']:
            confirm = input(f"\n⚠️ Are you sure you want to delete ALL {total_records} records? This action cannot be undone. (yes/no): ")
            if confirm.lower() != 'yes':
                self.stdout.write("❌ Deletion cancelled.")
                return

        self.stdout.write("🗑️ Starting deletion process...")

        try:
            with transaction.atomic():
                # Delete in proper order to avoid foreign key constraints
                
                # 1. Delete ChildDose records (patients DB)
                if child_doses_count > 0:
                    deleted_doses = ChildDose.objects.using("patients").all().delete()
                    self.stdout.write(f"   ✅ Deleted {deleted_doses[0]} child doses")

                # 2. Delete ChildShareLink records (patients DB)
                if share_links_count > 0:
                    deleted_links = ChildShareLink.objects.using("patients").all().delete()
                    self.stdout.write(f"   ✅ Deleted {deleted_links[0]} share links")

                # 3. Delete Children (patients DB)
                if children_count > 0:
                    deleted_children = Child.objects.using("patients").all().delete()
                    self.stdout.write(f"   ✅ Deleted {deleted_children[0]} children")

                # 4. Delete Parents (patients DB)
                if parents_count > 0:
                    deleted_parents = Parent.objects.using("patients").all().delete()
                    self.stdout.write(f"   ✅ Deleted {deleted_parents[0]} parents")

                # 5. Delete OAuth States (patients DB)
                if oauth_states_count > 0:
                    deleted_oauth = OAuthState.objects.using("patients").all().delete()
                    self.stdout.write(f"   ✅ Deleted {deleted_oauth[0]} OAuth states")

                # 6. Delete Doctor Session Tokens (patients DB)
                if session_tokens_count > 0:
                    deleted_sessions = DoctorSessionToken.objects.using("patients").all().delete()
                    self.stdout.write(f"   ✅ Deleted {deleted_sessions[0]} doctor sessions")

                # 7. Delete Doctors (masters DB)
                if doctors_count > 0:
                    deleted_doctors = Doctor.objects.using("masters").all().delete()
                    self.stdout.write(f"   ✅ Deleted {deleted_doctors[0]} doctors")

            self.stdout.write(self.style.SUCCESS(f"\n🎉 Successfully deleted all {total_records} records!"))
            self.stdout.write("📊 Database is now clean and ready for fresh data.")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error during deletion: {e}"))
            import traceback
            traceback.print_exc()
