from django.db import migrations, models
import django.db.models.deletion
from django.utils import timezone

class Migration(migrations.Migration):

    dependencies = [
        ('vaccinations', '0026_parent_created_at_alter_child_created_at'),  # replace with last migration
    ]

    operations = []
