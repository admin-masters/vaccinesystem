# vaccinations/management/commands/apply_hotfix_sql.py
from django.core.management.base import BaseCommand
from django.db import connections

class Command(BaseCommand):
    help = "Apply hot-fix SQL to temporarily relax whatsapp_hash constraints"

    def handle(self, *args, **opts):
        # Get the patients database connection
        patients_db = connections['patients']
        
        with patients_db.cursor() as cursor:
            self.stdout.write("Applying hot-fix SQL commands...")
            
            try:
                # 1) Allow NULLs temporarily and remove the accidental default '' path
                self.stdout.write("1. Modifying whatsapp_hash column to allow NULL...")
                cursor.execute("ALTER TABLE parent MODIFY COLUMN whatsapp_hash varchar(64) NULL;")
                self.stdout.write(self.style.SUCCESS("✓ Column modified to allow NULL"))
                
                # 2) Drop the unique index if it exists
                self.stdout.write("2. Dropping unique index on whatsapp_hash...")
                # Try different possible index names
                index_names = ['whatsapp_hash', 'ux_parent_whash']
                dropped = False
                for index_name in index_names:
                    try:
                        cursor.execute(f"ALTER TABLE parent DROP INDEX {index_name};")
                        self.stdout.write(self.style.SUCCESS(f"✓ Unique index '{index_name}' dropped"))
                        dropped = True
                        break
                    except Exception as e:
                        if "doesn't exist" in str(e).lower() or "can't drop" in str(e).lower():
                            continue
                        else:
                            raise e
                if not dropped:
                    self.stdout.write(self.style.WARNING("⚠ No whatsapp_hash index found to drop"))
                
                self.stdout.write(self.style.SUCCESS("\n🎉 Hot-fix SQL applied successfully!"))
                self.stdout.write("Next steps:")
                self.stdout.write("1. Deploy your code changes")
                self.stdout.write("2. Run: python manage.py backfill_encryption")
                self.stdout.write("3. Restore constraints with restore_constraints command")
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error applying hot-fix: {e}"))
                raise e
