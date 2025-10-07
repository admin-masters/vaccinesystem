# vaccinations/management/commands/sync_masters_schema.py
from django.core.management.base import BaseCommand
from django.db import connections

class Command(BaseCommand):
    help = "Synchronize masters database schema with model definitions"

    def handle(self, *args, **opts):
        # Get the masters database connection
        masters_db = connections['masters']
        
        with masters_db.cursor() as cursor:
            self.stdout.write("Synchronizing masters database schema...")
            
            # Define all required columns for each table
            table_schemas = {
                'vaccine': [
                    ('education_parent_url', "varchar(200) DEFAULT ''"),
                    ('education_doctor_vimeo_url', "varchar(200) DEFAULT ''")
                ],
                'vaccine_dose': [
                    ('anchor_policy', "varchar(1) DEFAULT 'L'"),
                    ('series_key', "varchar(32) DEFAULT ''"),
                    ('series_seq', "smallint unsigned DEFAULT 1")
                ]
            }
            
            # Column renames needed
            column_renames = {
                'vaccine_dose': [
                    ('eligible_sex', 'eligible_gender', 'varchar(1)')
                ]
            }
            
            total_changes = 0
            
            for table_name, required_columns in table_schemas.items():
                try:
                    # Get existing columns
                    cursor.execute(f"DESCRIBE {table_name}")
                    existing_columns = [row[0] for row in cursor.fetchall()]
                    
                    self.stdout.write(f"\nChecking {table_name} table...")
                    
                    # Handle column renames first
                    if table_name in column_renames:
                        for old_name, new_name, column_type in column_renames[table_name]:
                            if old_name in existing_columns and new_name not in existing_columns:
                                try:
                                    cursor.execute(f"ALTER TABLE {table_name} CHANGE {old_name} {new_name} {column_type}")
                                    self.stdout.write(f"  ✓ Renamed {old_name} to {new_name}")
                                    total_changes += 1
                                    # Update existing columns list
                                    existing_columns = [col if col != old_name else new_name for col in existing_columns]
                                except Exception as e:
                                    self.stdout.write(self.style.ERROR(f"  ❌ Error renaming {old_name}: {e}"))
                    
                    # Add missing columns
                    for column_name, column_def in required_columns:
                        if column_name not in existing_columns:
                            try:
                                cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_def}")
                                self.stdout.write(f"  ✓ Added {column_name}")
                                total_changes += 1
                            except Exception as e:
                                self.stdout.write(self.style.ERROR(f"  ❌ Error adding {column_name}: {e}"))
                        else:
                            self.stdout.write(f"  - {column_name} already exists")
                            
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing {table_name}: {e}"))
            
            if total_changes > 0:
                self.stdout.write(self.style.SUCCESS(f"\n🎉 Schema synchronization complete! Made {total_changes} changes."))
            else:
                self.stdout.write(self.style.SUCCESS("\n✅ Schema is already synchronized!"))
            
            self.stdout.write("\nMasters database schema is now up to date with model definitions.")
