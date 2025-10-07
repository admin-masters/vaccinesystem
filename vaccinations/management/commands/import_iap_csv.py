# vaccinations/migrations/0017_rename_eligible_sex_vaccinedose_eligible_gender_and_more.py
from django.db import migrations, connection, models

def rename_col_if_exists(apps, schema_editor):
    with connection.cursor() as c:
        c.execute("""
            SELECT COUNT(*) FROM information_schema.columns
            WHERE table_schema = DATABASE()
              AND table_name = 'vaccine_dose'
              AND column_name = 'eligible_sex'
        """)
        if c.fetchone()[0]:
            # old column exists -> do an in-place rename
            c.execute(
                "ALTER TABLE vaccine_dose "
                "CHANGE eligible_sex eligible_gender VARCHAR(1) NULL"
            )

class Migration(migrations.Migration):
    dependencies = [
        ('vaccinations', '0016_remove_child_child_parent__16983e_idx_and_more'),
    ]
    operations = [
        # Update Django's model state regardless of DB shape
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RenameField(
                    model_name='vaccinedose',
                    old_name='eligible_sex',
                    new_name='eligible_gender',
                ),
            ],
            database_operations=[],
        ),
        migrations.RunPython(rename_col_if_exists, reverse_code=migrations.RunPython.noop),

        # If you also changed on_delete for previous_dose in code, add:
        # migrations.AlterField(
        #     model_name='vaccinedose',
        #     name='previous_dose',
        #     field=models.ForeignKey(
        #         to='vaccinations.vaccinedose',
        #         null=True, blank=True,
        #         on_delete=models.SET_NULL,
        #         related_name='booster_children'
        #     ),
        # ),
    ]
