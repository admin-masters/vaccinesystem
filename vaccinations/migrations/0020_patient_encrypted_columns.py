# vaccinations/migrations/0020_patient_encrypted_columns.py
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('vaccinations', '0018_remove_child_child_clinic__5e8bbe_idx_and_more'),
    ]
    operations = [
        # Parent encryption columns
        migrations.AddField(
            model_name='parent',
            name='whatsapp_e164_enc',
            field=models.BinaryField(null=True, editable=False),
        ),
        migrations.AddField(
            model_name='parent',
            name='whatsapp_hash',
            field=models.CharField(max_length=64, unique=True, db_index=True, default=""),
        ),

        # Child encryption columns
        migrations.AddField(
            model_name='child',
            name='child_name_enc',
            field=models.BinaryField(null=True, editable=False),
        ),
        migrations.AddField(
            model_name='child',
            name='date_of_birth_enc',
            field=models.BinaryField(null=True, editable=False),
        ),
        migrations.AddField(
            model_name='child',
            name='gender_enc',
            field=models.BinaryField(null=True, editable=False),
        ),
        migrations.AddField(
            model_name='child',
            name='state_enc',
            field=models.BinaryField(null=True, editable=False),
        ),
    ]
