from django.db import migrations, models
import django.db.models.deletion

def create_partner_slug_and_tokens(apps, schema_editor):
    # no-op; tokens are created in app logic
    pass

class Migration(migrations.Migration):
    dependencies = [
        ("vaccinations", "0002_child_state_alter_vaccine_code_alter_vaccine_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="clinic",
            name="state",
            field=models.CharField(max_length=50, blank=True, default=""),
        ),
        migrations.AddField(
            model_name="clinic",
            name="headquarters",
            field=models.CharField(max_length=120, blank=True, default=""),
        ),
        migrations.AddField(
            model_name="clinic",
            name="pincode",
            field=models.CharField(max_length=10, blank=True, default=""),
        ),
        migrations.AddField(
            model_name="clinic",
            name="whatsapp_e164",
            field=models.CharField(max_length=20, blank=True, default=""),
        ),
        migrations.AddField(
            model_name="clinic",
            name="receptionist_email",
            field=models.EmailField(max_length=254, blank=True, default=""),
        ),
        migrations.AddField(
            model_name="clinic",
            name="languages_csv",
            field=models.CharField(max_length=100, blank=True, default=""),
        ),
        migrations.CreateModel(
            name="Partner",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=150)),
                ("slug", models.SlugField(max_length=60, unique=True)),
                ("registration_token", models.CharField(max_length=64, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table": "partner"},
        ),
        migrations.CreateModel(
            name="FieldRepresentative",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("rep_code", models.CharField(max_length=50)),
                ("full_name", models.CharField(max_length=120)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("partner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                              related_name="field_reps", to="vaccinations.partner")),
            ],
            options={"db_table": "field_representative"},
        ),
        migrations.AlterUniqueTogether(
            name="fieldrepresentative",
            unique_together={("partner", "rep_code")},
        ),
        migrations.AddIndex(
            model_name="fieldrepresentative",
            index=models.Index(fields=["partner", "rep_code"], name="idx_rep_partner_code"),
        ),
        migrations.CreateModel(
            name="Doctor",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("full_name", models.CharField(max_length=120)),
                ("whatsapp_e164", models.CharField(max_length=20)),
                ("email", models.EmailField(max_length=254)),
                ("imc_number", models.CharField(max_length=30, unique=True)),
                ("photo", models.ImageField(blank=True, null=True, upload_to="doctor_photos/")),
                ("portal_token", models.CharField(max_length=64, unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("clinic", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                             related_name="doctors", to="vaccinations.clinic")),
                ("partner", models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL,
                                              related_name="doctors", to="vaccinations.partner")),
                ("field_rep", models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL,
                                                related_name="doctors", to="vaccinations.fieldrepresentative")),
            ],
            options={"db_table": "doctor"},
        ),
        migrations.AddIndex(model_name="doctor", index=models.Index(fields=["clinic"], name="idx_doctor_clinic")),
        migrations.AddIndex(model_name="doctor", index=models.Index(fields=["partner"], name="idx_doctor_partner")),
        migrations.AddIndex(model_name="doctor", index=models.Index(fields=["field_rep"], name="idx_doctor_rep")),
        migrations.RunPython(create_partner_slug_and_tokens, reverse_code=migrations.RunPython.noop),
    ]
