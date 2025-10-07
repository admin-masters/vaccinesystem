from django.db import migrations, connection

def drop_idx_if_exists(table, index):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 1
            FROM information_schema.statistics
            WHERE table_schema = DATABASE()
              AND table_name = %s
              AND index_name = %s
            LIMIT 1
        """, [table, index])
        if cursor.fetchone():
            cursor.execute(f"DROP INDEX `{index}` ON `{table}`")

def forwards(apps, schema_editor):
    # Adjust the list to match indexes in your 0016 file:
    for idx in (
        "child_parent__16983e_idx",
        # "child_clinic__XXXXXX_idx",
        # "child_date_of_birth_YYYYYY_idx",
    ):
        drop_idx_if_exists("child", idx)

class Migration(migrations.Migration):
    dependencies = [("vaccinations", "0015_patients_encryption")]
    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[migrations.RunPython(forwards, migrations.RunPython.noop)],
            state_operations=[
                migrations.RemoveIndex(model_name="child", name="child_parent__16983e_idx"),
                # migrations.RemoveIndex(model_name="child", name="child_clinic__XXXXXX_idx"),
                # migrations.RemoveIndex(model_name="child", name="child_date_of_birth_YYYYYY_idx"),
            ],
        ),
    ]
