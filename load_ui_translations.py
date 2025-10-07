import os
import django
import csv
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaccination_project.settings')
django.setup()

from django.db import connections
from datetime import datetime

def load_ui_translations():
    print("Loading UI translations from phase5_ui_translations.csv...")
    
    masters_cursor = connections['masters'].cursor()
    
    try:
        # Clear existing data
        print("Clearing existing UI string data...")
        masters_cursor.execute("DELETE FROM ui_string_translation")
        masters_cursor.execute("DELETE FROM ui_string")
        print("✓ Cleared existing data")
        
        # Read CSV file
        csv_file = "phase5_ui_translations.csv"
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        
        ui_strings = {}  # key -> ui_string_id
        translations = []
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Debug: Print column names
            print(f"CSV columns: {reader.fieldnames}")
            
            for row in reader:
                # Handle BOM in column names
                key_col = 'key' if 'key' in row else '\ufeffkey'
                key = row[key_col].strip()
                description = row['description'].strip()
                language = row['language'].strip()
                text = row['text'].strip()
                
                if not key or not language or not text:
                    continue
                
                # Create ui_string if not exists
                if key not in ui_strings:
                    masters_cursor.execute("""
                        INSERT INTO ui_string (key_name, `key`, context, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s)
                    """, [key, key, description, current_time, current_time])
                    
                    ui_string_id = masters_cursor.lastrowid
                    ui_strings[key] = ui_string_id
                    print(f"  ✓ Created UI string: {key}")
                else:
                    ui_string_id = ui_strings[key]
                
                # Add translation
                translations.append({
                    'ui_string_id': ui_string_id,
                    'ui_id': ui_string_id,  # Duplicate for compatibility
                    'language_code': language,
                    'language': language,  # Duplicate for compatibility
                    'text': text,
                    'created_at': current_time,
                    'updated_at': current_time
                })
        
        # Insert all translations
        print(f"\nInserting {len(translations)} translations...")
        for translation in translations:
            masters_cursor.execute("""
                INSERT INTO ui_string_translation 
                (ui_string_id, ui_id, language_code, language, text, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, [
                translation['ui_string_id'],
                translation['ui_id'],
                translation['language_code'],
                translation['language'],
                translation['text'],
                translation['created_at'],
                translation['updated_at']
            ])
        
        print(f"✓ Inserted {len(translations)} translations")
        
        # Verify the data
        print(f"\n=== VERIFICATION ===")
        masters_cursor.execute("SELECT COUNT(*) FROM ui_string")
        ui_string_count = masters_cursor.fetchone()[0]
        
        masters_cursor.execute("SELECT COUNT(*) FROM ui_string_translation")
        translation_count = masters_cursor.fetchone()[0]
        
        print(f"UI strings created: {ui_string_count}")
        print(f"Translations created: {translation_count}")
        
        # Show sample data
        print(f"\nSample UI strings:")
        masters_cursor.execute("SELECT key_name, context FROM ui_string LIMIT 5")
        for row in masters_cursor.fetchall():
            print(f"  {row[0]} - {row[1]}")
        
        print(f"\nSample translations:")
        masters_cursor.execute("""
            SELECT us.key_name, ust.language, ust.text 
            FROM ui_string us 
            JOIN ui_string_translation ust ON us.id = ust.ui_string_id 
            WHERE us.key_name = 'history.title'
        """)
        for row in masters_cursor.fetchall():
            print(f"  {row[0]} ({row[1]}): {row[2]}")
        
        print(f"\n🎉 UI translations loaded successfully!")
        print(f"History page should now display proper content!")
        
    except Exception as e:
        print(f"❌ Error loading UI translations: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    load_ui_translations()
