# migrations/0017b_safe_rename_vaccinedose_gender.py
from django.db import migrations

def forwards(apps, schema_editor):
    with schema_editor.connection.cursor() as c:
        columns = {
            col.name
            for col in schema_editor.connection.introspection.get_table_description(c, "vaccine_dose")
        }
        if "eligible_gender" not in columns and "eligible_sex" in columns:
            schema_editor.execute(
                "ALTER TABLE vaccine_dose RENAME COLUMN eligible_sex TO eligible_gender"
            )

class Migration(migrations.Migration):
    dependencies = [
        ('vaccinations', '0016_remove_child_child_parent__16983e_idx_and_more'),
    ]
    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
