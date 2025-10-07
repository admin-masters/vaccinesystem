from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('vaccinations', '0017_rename_eligible_sex_vaccinedose_eligible_gender_and_more'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveIndex(
                    model_name='child',
                    name='child_clinic__5e8bbe_idx',
                ),
                migrations.RemoveIndex(
                    model_name='child',
                    name='child_date_of_670404_idx',
                ),
                migrations.RenameField(
                    model_name='vaccinedose',
                    old_name='eligible_sex',
                    new_name='eligible_gender',
                ),
                migrations.RemoveField(
                    model_name='parent',
                    name='clinic',
                ),
                migrations.RemoveField(
                    model_name='parent',
                    name='created_at',
                ),
                migrations.RemoveField(
                    model_name='parent',
                    name='full_name',
                ),
                migrations.RemoveField(
                    model_name='parent',
                    name='whatsapp_e164',
                ),
                migrations.AlterField(
                    model_name='child',
                    name='date_of_birth',
                    field=models.DateField(blank=True, null=True),
                ),
                migrations.AlterField(
                    model_name='child',
                    name='full_name',
                    field=models.CharField(blank=True, default='', max_length=120),
                ),
                migrations.AlterField(
                    model_name='childdose',
                    name='last_reminder_by',
                    field=models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='reminders_sent',
                        to='vaccinations.doctor'
                    ),
                ),
                migrations.AlterField(
                    model_name='vaccinedose',
                    name='previous_dose',
                    field=models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='booster_children',
                        to='vaccinations.vaccinedose'
                    ),
                ),
                migrations.AlterModelTable(
                    name='parent',
                    table=None,
                ),
            ],
            database_operations=[],  # DB me kuch nahi karega
        ),
    ]
