# vaccinations/migrations/00XX_patients_encryption.py
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("vaccinations", "0014_fix_influenza_series")]

    operations = [
        migrations.AddField(
            model_name="parent",
            name="whatsapp_e164_enc",
            field=models.BinaryField(null=True, editable=False),
        ),
        migrations.AddField(
            model_name="parent",
            name="whatsapp_hash",
            field=models.CharField(max_length=64, unique=True, db_index=True, default=""),
        ),
        migrations.AddField("child", "child_name_enc", models.BinaryField(null=True, editable=False)),
        migrations.AddField("child", "date_of_birth_enc", models.BinaryField(null=True, editable=False)),
        migrations.AddField("child", "gender_enc", models.BinaryField(null=True, editable=False)),
        migrations.AddField("child", "state_enc", models.BinaryField(null=True, editable=False)),
        migrations.AlterField(
            model_name="childdose",
            name="last_reminder_by",
            field=models.ForeignKey(
                "vaccinations.Doctor",
                on_delete=models.SET_NULL, null=True, blank=True,
                related_name="reminders_sent", db_constraint=False
            ),
        ),
    ]
