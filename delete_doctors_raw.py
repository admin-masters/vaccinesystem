import os
import django
from django.db import connections

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaccination_project.settings')
django.setup()

try:
    # Get the masters database connection
    masters_db = connections['masters']
    cursor = masters_db.cursor()
    
    # Check current doctors
    cursor.execute("SELECT id, full_name FROM doctor")
    doctors = cursor.fetchall()
    print(f'Found {len(doctors)} doctors:')
    for doctor_id, name in doctors:
        print(f'  ID: {doctor_id}, Name: {name}')
    
    # Delete all doctors using raw SQL
    cursor.execute("DELETE FROM doctor")
    deleted_count = cursor.rowcount
    print(f'\nDeleted {deleted_count} doctors')
    
    # Verify deletion
    cursor.execute("SELECT COUNT(*) FROM doctor")
    remaining = cursor.fetchone()[0]
    print(f'Remaining doctors: {remaining}')
    
    cursor.close()
    
except Exception as e:
    print(f'Error: {e}')
