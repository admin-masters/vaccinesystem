import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaccination_project.settings')
django.setup()

from django.db import connections

def copy_vaccines():
    default_db = connections['default']
    masters_db = connections['masters']
    
    print("Copying vaccine data from clinic_db to masters...")
    
    with masters_db.cursor() as masters_cursor, default_db.cursor() as default_cursor:
        # Clear masters data
        print("Clearing masters data...")
        masters_cursor.execute("DELETE FROM vaccine_dose")
        masters_cursor.execute("DELETE FROM vaccine")  
        masters_cursor.execute("DELETE FROM schedule_version")
        
        # Copy schedule_version
        print("Copying schedule versions...")
        default_cursor.execute("SELECT * FROM schedule_version")
        schedules = default_cursor.fetchall()
        
        for schedule in schedules:
            masters_cursor.execute("""
                INSERT INTO schedule_version 
                (id, code, name, source_url, effective_from, is_current, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, schedule)
        
        # Copy vaccines
        print("Copying vaccines...")
        default_cursor.execute("SELECT * FROM vaccine")
        vaccines = default_cursor.fetchall()
        
        for vaccine in vaccines:
            # Reorder columns to match masters schema
            # clinic_db: id, schedule_version_id, code, name, aliases, is_active, notes, created_at, education_doctor_vimeo_url, education_parent_url
            # masters: id, code, name, aliases, is_active, notes, created_at, schedule_version_id, education_parent_url, education_doctor_vimeo_url
            masters_cursor.execute("""
                INSERT INTO vaccine 
                (id, code, name, aliases, is_active, notes, created_at, schedule_version_id, education_parent_url, education_doctor_vimeo_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (vaccine[0], vaccine[2], vaccine[3], vaccine[4], vaccine[5], vaccine[6], vaccine[7], vaccine[1], vaccine[9], vaccine[8]))
        
        # Copy vaccine_dose
        print("Copying vaccine doses...")
        default_cursor.execute("SELECT * FROM vaccine_dose")
        doses = default_cursor.fetchall()
        
        for dose in doses:
            masters_cursor.execute("""
                INSERT INTO vaccine_dose 
                (id, sequence_index, dose_label, eligible_gender, min_offset_days, max_offset_days, 
                 is_booster, notes, created_at, previous_dose_id, schedule_version_id, vaccine_id,
                 anchor_policy, series_key, series_seq)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, dose)
        
        print("✅ Successfully copied all vaccine data!")
        
        # Verify
        masters_cursor.execute("SELECT COUNT(*) FROM schedule_version")
        schedule_count = masters_cursor.fetchone()[0]
        
        masters_cursor.execute("SELECT COUNT(*) FROM vaccine")
        vaccine_count = masters_cursor.fetchone()[0]
        
        masters_cursor.execute("SELECT COUNT(*) FROM vaccine_dose")
        dose_count = masters_cursor.fetchone()[0]
        
        print(f"Masters database now has:")
        print(f"  - {schedule_count} schedule versions")
        print(f"  - {vaccine_count} vaccines")
        print(f"  - {dose_count} vaccine doses")

if __name__ == "__main__":
    copy_vaccines()
