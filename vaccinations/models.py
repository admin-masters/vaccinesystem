from django.db import models
from django.utils.text import slugify
import secrets

# ---------------------------
# Reuse these language codes in forms & model validators
# ---------------------------
LANGUAGE_CHOICES = [
    ("en", "English"),
    ("hi", "Hindi"),
    ("mr", "Marathi"),
    ("kn", "Kannada"),
    ("ml", "Malayalam"),
    ("te", "Telugu"),
    ("ta", "Tamil"),
]
LANGUAGE_CODE_SET = {c for c, _ in LANGUAGE_CHOICES}

class Clinic(models.Model):
    name = models.CharField(max_length=150)
    address = models.TextField(blank=True, default="")
    phone = models.CharField(max_length=30, blank=True, default="")
    # NEW (Phase 2)
    state = models.CharField(max_length=50, blank=True, default="")
    headquarters = models.CharField(max_length=120, blank=True, default="")
    pincode = models.CharField(max_length=10, blank=True, default="")
    whatsapp_e164 = models.CharField(max_length=20, blank=True, default="")
    receptionist_email = models.EmailField(blank=True, default="")
    languages_csv = models.CharField(
        max_length=100, blank=True, default="",
        help_text="Comma-separated language codes (e.g., en,hi,mr)",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "clinic"

    # helpers
    def set_languages(self, codes: list[str]) -> None:
        cleaned = [c for c in (codes or []) if c in LANGUAGE_CODE_SET]
        self.languages_csv = ",".join(sorted(set(cleaned)))

    def get_languages(self) -> list[str]:
        return [c for c in (self.languages_csv or "").split(",") if c]

class Parent(models.Model):
    full_name = models.CharField(max_length=120, blank=True, default="")
    whatsapp_e164 = models.CharField(
        max_length=20, unique=True,
        help_text="Parent WhatsApp in E.164 format, e.g. +919812345678",
    )
    clinic = models.ForeignKey(Clinic, null=True, blank=True,
                               on_delete=models.SET_NULL, related_name="parents")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "parent"

class Child(models.Model):
    class Sex(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHER = "O", "Other"

    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name="children")
    clinic = models.ForeignKey(Clinic, null=True, blank=True,
                               on_delete=models.SET_NULL, related_name="children")
    full_name = models.CharField(max_length=120)
    date_of_birth = models.DateField()
    sex = models.CharField(max_length=1, choices=Sex.choices, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, default="")  # <--- NEW
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "child"
        indexes = [
            models.Index(fields=["parent"]),
            models.Index(fields=["clinic"]),
            models.Index(fields=["date_of_birth"]),
        ]

class ScheduleVersion(models.Model):
    code = models.CharField(max_length=50, unique=True, help_text="e.g., IAP-2025")
    name = models.CharField(max_length=120)
    source_url = models.URLField(blank=True, default="")
    effective_from = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "schedule_version"

class Vaccine(models.Model):
    schedule_version = models.ForeignKey(ScheduleVersion, on_delete=models.PROTECT, related_name="vaccines")
    code = models.SlugField(max_length=50)
    name = models.CharField(max_length=120)
    aliases = models.CharField(max_length=255, blank=True, default="")
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "vaccine"
        unique_together = [("schedule_version", "code")]
        indexes = [models.Index(fields=["schedule_version", "name"])]

class VaccineDose(models.Model):
    schedule_version = models.ForeignKey(ScheduleVersion, on_delete=models.PROTECT, related_name="doses")
    vaccine = models.ForeignKey(Vaccine, on_delete=models.PROTECT, related_name="doses")
    sequence_index = models.PositiveSmallIntegerField()
    dose_label = models.CharField(max_length=60, blank=True, default="")
    eligible_sex = models.CharField(max_length=1, choices=Child.Sex.choices, blank=True, null=True)
    min_offset_days = models.PositiveIntegerField()
    max_offset_days = models.PositiveIntegerField(blank=True, null=True)
    is_booster = models.BooleanField(default=False)
    previous_dose = models.ForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True, related_name="booster_children"
    )
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "vaccine_dose"
        unique_together = [("schedule_version", "vaccine", "sequence_index")]
        indexes = [
            models.Index(fields=["schedule_version", "vaccine", "sequence_index"]),
            models.Index(fields=["previous_dose"]),
        ]
        constraints = [
            models.CheckConstraint(
                name="vd_offset_range_valid",
                check=(models.Q(max_offset_days__isnull=True) |
                       models.Q(max_offset_days__gte=models.F("min_offset_days"))),
            ),
            models.CheckConstraint(name="vd_prev_not_self",
                                   check=~models.Q(previous_dose=models.F("id"))),
        ]

class ChildDose(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name="doses")
    dose = models.ForeignKey(VaccineDose, on_delete=models.PROTECT, related_name="child_doses")
    given_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    due_until_date = models.DateField(blank=True, null=True)
    status_override = models.CharField(max_length=32, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "child_dose"
        unique_together = [("child", "dose")]
        indexes = [
            models.Index(fields=["child"]),
            models.Index(fields=["dose"]),
            models.Index(fields=["due_date"]),
            models.Index(fields=["given_date"]),
        ]

# ---------------------------
# NEW: Partner & FieldRepresentative
# ---------------------------
class Partner(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=60, unique=True)
    registration_token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "partner"

    @staticmethod
    def new(name: str) -> "Partner":
        base_slug = slugify(name)[:60] or secrets.token_hex(6)
        slug = base_slug
        
        # Handle duplicate slugs by appending a number
        counter = 1
        while Partner.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"[:60]
            counter += 1
            
        p = Partner(
            name=name,
            slug=slug,
            registration_token=secrets.token_urlsafe(24),
        )
        return p

    @property
    def doctor_registration_link(self) -> str:
        # URL path, use request.build_absolute_uri(...) in views
        from django.urls import reverse
        return reverse("vaccinations:doctor-register-partner", args=[self.registration_token])

class FieldRepresentative(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name="field_reps")
    rep_code = models.CharField(max_length=50)
    full_name = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "field_representative"
        unique_together = [("partner", "rep_code")]
        indexes = [models.Index(fields=["partner", "rep_code"])]

# ---------------------------
# NEW: Doctor
# ---------------------------
class Doctor(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="doctors")
    full_name = models.CharField(max_length=120)
    whatsapp_e164 = models.CharField(max_length=20)
    email = models.EmailField()
    imc_number = models.CharField(max_length=30, unique=True)
    photo = models.ImageField(upload_to="doctor_photos/", blank=True, null=True)
    partner = models.ForeignKey(Partner, on_delete=models.SET_NULL, null=True, blank=True, related_name="doctors")
    field_rep = models.ForeignKey(FieldRepresentative, on_delete=models.SET_NULL, null=True, blank=True, related_name="doctors")
    portal_token = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "doctor"
        indexes = [
            models.Index(fields=["clinic"]),
            models.Index(fields=["partner"]),
            models.Index(fields=["field_rep"]),
        ]

    def save(self, *args, **kwargs):
        if not self.portal_token:
            self.portal_token = secrets.token_urlsafe(24)
        super().save(*args, **kwargs)

    @property
    def portal_path(self) -> str:
        from django.urls import reverse
        return reverse("vaccinations:doc-home", args=[self.portal_token])
