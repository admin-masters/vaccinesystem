from django.db import OperationalError, migrations

def table_exists(schema_editor, table):
    return table in schema_editor.connection.introspection.table_names(schema_editor.connection.cursor())

def drop_idx_if_exists(schema_editor, table, index):
    if not table_exists(schema_editor, table):
        return
    with schema_editor.connection.cursor() as cursor:
        constraints = schema_editor.connection.introspection.get_constraints(cursor, table)
    if index not in constraints:
        return
    try:
        if schema_editor.connection.vendor == "mysql":
            schema_editor.execute(f"DROP INDEX `{index}` ON `{table}`")
        else:
            schema_editor.execute(f'DROP INDEX "{index}"')
    except OperationalError as exc:
        # MySQL can keep this index as the backing index for the FK on child.parent_id.
        # In that case, leaving the index in place is safe and the migration should continue.
        if schema_editor.connection.vendor == "mysql" and getattr(exc, "args", [None])[0] == 1553:
            return
        raise

def forwards(apps, schema_editor):
    for idx in (
        "child_parent__16983e_idx",
    ):
        drop_idx_if_exists(schema_editor, "child", idx)

class Migration(migrations.Migration):
    atomic = False
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
