from django.db import migrations

def drop_idx_if_exists(schema_editor, table, index):
    with schema_editor.connection.cursor() as cursor:
        constraints = schema_editor.connection.introspection.get_constraints(cursor, table)
    if index not in constraints:
        return
    if schema_editor.connection.vendor == "mysql":
        schema_editor.execute(f"DROP INDEX `{index}` ON `{table}`")
    else:
        schema_editor.execute(f'DROP INDEX "{index}"')

def forwards(apps, schema_editor):
    for idx in (
        "child_parent__16983e_idx",
    ):
        drop_idx_if_exists(schema_editor, "child", idx)

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
