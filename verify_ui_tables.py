import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaccination_project.settings')
django.setup()

from django.db import connections

masters_cursor = connections['masters'].cursor()
masters_cursor.execute("SHOW TABLES LIKE 'ui_string%'")
tables = masters_cursor.fetchall()

print('UI String tables in masters DB:')
for table in tables:
    print(f'  {table[0]}')

if len(tables) >= 2:
    print('\n✅ UI string tables exist in masters database!')
    print('The history page error should be fixed!')
else:
    print('\n❌ UI string tables still missing')
