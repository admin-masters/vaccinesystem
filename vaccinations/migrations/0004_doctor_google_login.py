# vaccinations/migrations/0004_doctor_google_login.py
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ("vaccinations", "0003_phase2_whitelabel"),
    ]

    operations = [
        migrations.AddField(
            model_name="doctor",
            name="google_sub",
            field=models.CharField(max_length=64, unique=True, null=True, blank=True),
        ),
        migrations.AddField(
            model_name="doctor",
            name="last_login_at",
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.CreateModel(
            name="DoctorSessionToken",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("token", models.CharField(max_length=128, unique=True)),
                ("user_agent_hash", models.CharField(max_length=40, blank=True, default="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("expires_at", models.DateTimeField()),
                ("revoked", models.BooleanField(default=False)),
                ("doctor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                             related_name="sessions", to="vaccinations.doctor")),
            ],
            options={"db_table": "doctor_session_token"},
        ),
        migrations.AddIndex(
            model_name="doctorsessiontoken",
            index=models.Index(fields=["doctor", "expires_at"], name="idx_doc_sess_exp"),
        ),
    ]

