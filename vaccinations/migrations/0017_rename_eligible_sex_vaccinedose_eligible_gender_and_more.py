# migrations/0017b_safe_rename_vaccinedose_gender.py
from django.db import migrations

def forwards(apps, schema_editor):
    with schema_editor.connection.cursor() as c:
        c.execute("SHOW COLUMNS FROM `vaccine_dose` LIKE 'eligible_gender'")
        has_gender = c.fetchone()
        c.execute("SHOW COLUMNS FROM `vaccine_dose` LIKE 'eligible_sex'")
        has_sex = c.fetchone()
        if (not has_gender) and has_sex:
            c.execute("ALTER TABLE `vaccine_dose` RENAME COLUMN `eligible_sex` TO `eligible_gender`")

class Migration(migrations.Migration):
    dependencies = [
        ('vaccinations', '0016_remove_child_child_parent__16983e_idx_and_more'),
    ]
    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
