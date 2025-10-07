from django.db import migrations, models
import django.db.models.deletion
from django.utils import timezone

class Migration(migrations.Migration):

    dependencies = [
        ('vaccinations', '0026_parent_created_at_alter_child_created_at'),  # replace with last migration
    ]

    operations = [
        migrations.CreateModel(
            name='ChildShareLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=64, unique=True, db_index=True)),
                ('expected_last10', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='share_links', to='vaccinations.child')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child_share_links', to='vaccinations.doctor')),
            ],
            options={
                'db_table': 'child_share_link',
            },
        ),
        migrations.AddIndex(
            model_name='childsharelink',
            index=models.Index(fields=['child'], name='vaccinations_child_id_idx'),
        ),
        migrations.AddIndex(
            model_name='childsharelink',
            index=models.Index(fields=['expires_at'], name='vaccinations_expires_at_idx'),
        ),
    ]
