from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [("vaccinations", "0006_oauthstate_redirect_uri")]
    operations = [
        migrations.CreateModel(
            name="ChildShareLink",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("token", models.CharField(max_length=64, unique=True, db_index=True)),
                ("expected_last10", models.CharField(max_length=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("expires_at", models.DateTimeField(null=True, blank=True)),
                ("is_active", models.BooleanField(default=True)),
                ("child", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                            related_name="share_links", to="vaccinations.child")),
                ("created_by", models.ForeignKey(null=True, blank=True,
                                                 on_delete=django.db.models.deletion.SET_NULL,
                                                 related_name="child_share_links",
                                                 to="vaccinations.doctor")),
            ],
            options={"db_table": "child_share_link"},
        ),
        migrations.AddIndex(
            model_name="childsharelink",
            index=models.Index(fields=["child"], name="idx_csl_child"),
        ),
        migrations.AddIndex(
            model_name="childsharelink",
            index=models.Index(fields=["expires_at"], name="idx_csl_exp"),
        ),
    ]



















