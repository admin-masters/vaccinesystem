from django.core.management.base import BaseCommand
from django.db import transaction
from vaccinations.models import Parent, Child, ChildDose, ChildShareLink


class Command(BaseCommand):
    help = 'Clear only parent and child data (keep doctors and vaccine data)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletion without interactive prompt',
        )

    def handle(self, *args, **options):
        # Count records before deletion
        parents_count = Parent.objects.using("patients").count()
        children_count = Child.objects.using("patients").count()
        child_doses_count = ChildDose.objects.using("patients").count()
        share_links_count = ChildShareLink.objects.using("patients").count()

        self.stdout.write(f"📊 Patient Data Count:")
        self.stdout.write(f"   Parents: {parents_count}")
        self.stdout.write(f"   Children: {children_count}")
        self.stdout.write(f"   Child Doses: {child_doses_count}")
        self.stdout.write(f"   Share Links: {share_links_count}")

        total_records = parents_count + children_count + child_doses_count + share_links_count

        if total_records == 0:
            self.stdout.write(self.style.SUCCESS("✅ No patient data to delete."))
            return

        if not options['confirm']:
            confirm = input(f"\n⚠️ Are you sure you want to delete ALL {total_records} patient records? This action cannot be undone. (yes/no): ")
            if confirm.lower() != 'yes':
                self.stdout.write("❌ Deletion cancelled.")
                return

        self.stdout.write("🗑️ Starting patient data deletion...")

        try:
            with transaction.atomic():
                # Delete in proper order to avoid foreign key constraints
                
                # 1. Delete ChildDose records
                if child_doses_count > 0:
                    deleted_doses = ChildDose.objects.using("patients").all().delete()
                    self.stdout.write(f"   ✅ Deleted {deleted_doses[0]} child doses")

                # 2. Delete ChildShareLink records
                if share_links_count > 0:
                    deleted_links = ChildShareLink.objects.using("patients").all().delete()
                    self.stdout.write(f"   ✅ Deleted {deleted_links[0]} share links")

                # 3. Delete Children
                if children_count > 0:
                    deleted_children = Child.objects.using("patients").all().delete()
                    self.stdout.write(f"   ✅ Deleted {deleted_children[0]} children")

                # 4. Delete Parents
                if parents_count > 0:
                    deleted_parents = Parent.objects.using("patients").all().delete()
                    self.stdout.write(f"   ✅ Deleted {deleted_parents[0]} parents")

            self.stdout.write(self.style.SUCCESS(f"\n🎉 Successfully deleted all {total_records} patient records!"))
            self.stdout.write("📊 Doctors and vaccine data preserved.")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error during deletion: {e}"))
            import traceback
            traceback.print_exc()
