# vaccinations/management/commands/restore_constraints.py
from django.core.management.base import BaseCommand
from django.db import connections

class Command(BaseCommand):
    help = "Restore whatsapp_hash constraints after backfill is complete"

    def handle(self, *args, **opts):
        # Get the patients database connection
        patients_db = connections['patients']
        
        with patients_db.cursor() as cursor:
            self.stdout.write("Restoring whatsapp_hash constraints...")
            
            try:
                # 1) Make column NOT NULL again
                self.stdout.write("1. Making whatsapp_hash column NOT NULL...")
                cursor.execute("ALTER TABLE parent MODIFY COLUMN whatsapp_hash varchar(64) NOT NULL;")
                self.stdout.write(self.style.SUCCESS("✓ Column set to NOT NULL"))
                
                # 2) Create unique index
                self.stdout.write("2. Creating unique index on whatsapp_hash...")
                cursor.execute("CREATE UNIQUE INDEX ux_parent_whash ON parent (whatsapp_hash);")
                self.stdout.write(self.style.SUCCESS("✓ Unique index created"))
                
                self.stdout.write(self.style.SUCCESS("\n🎉 Constraints restored successfully!"))
                self.stdout.write("The whatsapp_hash column is now properly constrained.")
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error restoring constraints: {e}"))
                raise e
