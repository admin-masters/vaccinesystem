from django.db import models
from django.utils.text import slugify
from django.utils import timezone
import secrets
import hashlib
from .crypto import encrypt, decrypt, hmac_sha256, encrypt_str, decrypt_str, hash_last10
from cryptography.fernet import Fernet
from .utils import normalize_msisdn, phone_hash
from django.conf import settings
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
def _fernet() -> Fernet:
    return Fernet(settings.PATIENT_DATA_FERNET_KEY)
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
    # encrypted-at-rest
    whatsapp_e164_enc = models.BinaryField(null=True, editable=False)                  # NOT NULL in final state
    whatsapp_hash = models.CharField(max_length=64, unique=True, db_index=True, default="")  # SHA-256(last10)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "parent"

    @property
    def whatsapp_e164(self) -> str:
        if not self.whatsapp_e164_enc:
            return ""
        try:
            # Try new Fernet decryption first
            return decrypt_str(self.whatsapp_e164_enc)
        except Exception:
            try:
                # Fallback to old AESGCM decryption
                return decrypt(self.whatsapp_e164_enc).decode("utf-8")
            except Exception:
                return ""

    @whatsapp_e164.setter
    def whatsapp_e164(self, raw: str) -> None:
        e164 = normalize_msisdn(raw)
        if not e164 or len("".join(ch for ch in e164 if ch.isdigit())) < 10:
            raise ValueError("Invalid WhatsApp number")
        self.whatsapp_e164_enc = encrypt_str(e164)
        self.whatsapp_hash = hash_last10(e164)

    @classmethod
    def hash_for(cls, raw: str) -> str:
        return hash_last10(normalize_msisdn(raw))    
class Child(models.Model):
    class Sex(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHER = "O", "Other"

    # Legacy fields (will be removed after encryption migration)
    full_name = models.CharField(max_length=120, blank=True, default="")
    date_of_birth = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=1, choices=Sex.choices, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, default="")
    
    # Encrypted fields
    child_name_enc = models.BinaryField(null=True, editable=False)
    date_of_birth_enc = models.BinaryField(null=True, editable=False)
    gender_enc = models.BinaryField(null=True, editable=False)
    state_enc = models.BinaryField(null=True, editable=False)
    
    # Foreign keys
    parent = models.ForeignKey("Parent", on_delete=models.CASCADE, related_name="children")
    clinic = models.ForeignKey("Clinic", on_delete=models.SET_NULL, null=True, blank=True, related_name="children")
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def get_child_name(self) -> str:
        """Get decrypted child name, fallback to legacy field"""
        if self.child_name_enc:
            return decrypt(self.child_name_enc).decode()
        return self.full_name or ""

    def set_child_name(self, v: str):
        """Set encrypted child name"""
        self.child_name_enc = encrypt((v or "").encode())

    def get_date_of_birth_encrypted(self):
        """Get decrypted date of birth, fallback to legacy field"""
        if self.date_of_birth_enc:
            import datetime
            raw = decrypt(self.date_of_birth_enc).decode()
            return datetime.date.fromisoformat(raw) if raw else None
        return self.date_of_birth

    def set_date_of_birth_encrypted(self, d):
        """Set encrypted date of birth"""
        self.date_of_birth_enc = encrypt(str(d).encode() if d else b"")

    def get_gender(self):
        """Get decrypted gender, fallback to legacy field"""
        if self.gender_enc:
            return decrypt(self.gender_enc).decode()
        return self.sex

    def set_gender(self, s):
        """Set encrypted gender"""
        self.gender_enc = encrypt((s or "").encode())

    def get_state_encrypted(self):
        """Get decrypted state, fallback to legacy field"""
        if self.state_enc:
            return decrypt(self.state_enc).decode()
        return self.state

    def set_state_encrypted(self, s):
        """Set encrypted state"""
        self.state_enc = encrypt((s or "").encode())

    class Meta:
        db_table = "child"
        indexes = [
            models.Index(fields=["clinic"], name="idx_child_clinic"),
            models.Index(fields=["date_of_birth"], name="idx_child_dob"),
            models.Index(fields=["parent"], name="idx_child_parent"),
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
    # NEW: education links
    education_parent_url = models.URLField(blank=True, default="")
    education_doctor_vimeo_url = models.URLField(blank=True, default="")
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
    eligible_gender = models.CharField(max_length=1, choices=Child.Sex.choices, blank=True, null=True)
    min_offset_days = models.PositiveIntegerField()
    max_offset_days = models.PositiveIntegerField(blank=True, null=True)
    is_booster = models.BooleanField(default=False)
    previous_dose = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="booster_children"
    )
    # What rule anchors the due window for this dose?
    # A = age-only (DOB + offsets)  [rare]
    # L = later-of(age-from-DOB, interval-from-previous-given)  [default for most series]
    # I = interval-from-previous-given only (e.g., Influenza-2, HPV-2, HepA-2, Varicella-2)
    anchor_policy = models.CharField(
        max_length=1,
        choices=[("A", "AGE_ONLY"), ("L", "LATER_OF_AGE_AND_INTERVAL"), ("I", "INTERVAL_ONLY")],
        default="L",
        db_index=True,
    )
    series_key  = models.CharField(max_length=32, default="", db_index=True)
    series_seq  = models.PositiveSmallIntegerField(default=1, db_index=True)
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "vaccine_dose"
        unique_together = [("schedule_version", "vaccine", "sequence_index")]
        indexes = [
            models.Index(fields=["schedule_version", "vaccine", "sequence_index"]),
            models.Index(fields=["vaccine", "sequence_index"]),
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
    # NEW: reminder tracking
    last_reminder_at = models.DateTimeField(blank=True, null=True)
    last_reminder_for_date = models.DateField(blank=True, null=True)
    last_reminder_by = models.ForeignKey(
        "Doctor", on_delete=models.SET_NULL, null=True, blank=True, related_name="reminders_sent"
    )
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
        while Partner.objects.using("masters").filter(slug=slug).exists():
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
    
    # NEW: Google account binding
    google_sub = models.CharField(
        max_length=64, unique=True, null=True, blank=True,
        help_text="Google OIDC subject (unique account id)."
    )
    last_login_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "doctor"
        managed=True
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

class OAuthState(models.Model):
    """
    Temporary storage for OAuth state to handle session issues.
    """
    state = models.CharField(max_length=128, unique=True)
    doctor_token = models.CharField(max_length=128)
    next_url = models.CharField(max_length=500, blank=True, default="")
    redirect_uri = models.CharField(max_length=500, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        db_table = "oauth_state"
        indexes = [
            models.Index(fields=["state", "expires_at"]),
        ]
    
    @classmethod
    def create_for(cls, state: str, doctor_token: str, next_url: str = "", redirect_uri: str = ""):
        """Create a new OAuth state with 10 minute expiry."""
        return cls.objects.create(
            state=state,
            doctor_token=doctor_token,
            next_url=next_url,
            redirect_uri=redirect_uri,
            expires_at=timezone.now() + timezone.timedelta(minutes=10),
        )
    
    @classmethod
    def get_and_delete(cls, state: str):
        """Get OAuth state by state parameter and delete it (one-time use)."""
        try:
            oauth_state = cls.objects.get(state=state, expires_at__gt=timezone.now())
            result = {
                "state": oauth_state.state,
                "doctor_token": oauth_state.doctor_token,
                "next": oauth_state.next_url,
                "redirect_uri": oauth_state.redirect_uri,
            }
            oauth_state.delete()
            return result
        except cls.DoesNotExist:
            return None

class DoctorSessionToken(models.Model):
    """
    Server-side session for a doctor portal. Token is stored in an HttpOnly cookie.
    """
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="sessions")
    token = models.CharField(max_length=128, unique=True)
    user_agent_hash = models.CharField(max_length=40, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    revoked = models.BooleanField(default=False)

    class Meta:
        db_table = "doctor_session_token"
        indexes = [
            models.Index(fields=["doctor", "expires_at"]),
        ]

    @staticmethod
    def _ua_hash(ua: str) -> str:
        return hashlib.sha1((ua or "").encode("utf-8")).hexdigest()

    @classmethod
    def create_for(cls, doctor, request, ttl_minutes: int):
        from django.conf import settings
        token = secrets.token_urlsafe(32)
        return cls.objects.create(
            doctor=doctor,
            token=token,
            user_agent_hash=cls._ua_hash(request.META.get("HTTP_USER_AGENT", "")),
            expires_at=timezone.now() + timezone.timedelta(minutes=ttl_minutes),
        )

    def matches_request(self, request) -> bool:
        return self.user_agent_hash == self._ua_hash(request.META.get("HTTP_USER_AGENT", ""))

# -- Share link a doctor can send to the parent to open the child's card --
class ChildShareLink(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name="share_links")
    token = models.CharField(max_length=64, unique=True, db_index=True)
    # store only last 10 digits of the parent's WhatsApp number for verification
    expected_last10 = models.CharField(max_length=10)
    created_by = models.ForeignKey(Doctor, null=True, blank=True,
                                   on_delete=models.SET_NULL, related_name="child_share_links")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "child_share_link"
        indexes = [
            models.Index(fields=["child"]),
            models.Index(fields=["expires_at"]),
        ]

    @staticmethod
    def _digits_only(s: str) -> str:
        return "".join(ch for ch in (s or "") if ch.isdigit())

    @classmethod
    def issue_for(cls, child: Child, *, created_by: Doctor | None,
                  ttl_days: int = 180) -> "ChildShareLink":
        import secrets
        # URL-safe; avoid + and / to keep links robust
        raw = secrets.token_urlsafe(32).replace("-", "_")
        last10 = cls._digits_only(getattr(child.parent, "whatsapp_e164", ""))[-10:]
        exp = timezone.now() + timezone.timedelta(days=ttl_days)
        return cls.objects.create(
            child=child, token=raw, expected_last10=last10,
            created_by=created_by, expires_at=exp
        )

    def still_valid(self) -> bool:
        return self.is_active and (self.expires_at is None or self.expires_at > timezone.now())

    def matches(self, input_number: str) -> bool:
        last10 = self._digits_only(input_number)[-10:]
        return self.still_valid() and (last10 == self.expected_last10)


# ---------------------------
# Education Video Models
# ---------------------------
class VideoPlatform(models.TextChoices):
    YOUTUBE = "youtube", "YouTube"
    VIMEO = "vimeo", "Vimeo"
    OTHER = "other", "Other"

class VaccineEducationPatient(models.Model):
    """
    Patient education video(s) per Vaccine and language.
    Typically one row per local language, but multiple are allowed (use 'rank').
    """
    vaccine = models.ForeignKey("Vaccine", on_delete=models.CASCADE,
                                related_name="patient_education")
    language = models.CharField(
        max_length=5, db_index=True,
        help_text="ISO 639-1 code (e.g. en, hi, mr, bn, gu, ta, te, kn, ml)."
    )
    title = models.CharField(max_length=200, blank=True, default="")
    video_url = models.URLField()
    platform = models.CharField(max_length=20, choices=VideoPlatform.choices,
                                default=VideoPlatform.YOUTUBE)
    thumbnail_url = models.URLField(blank=True, default="")
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    rank = models.PositiveSmallIntegerField(default=1,
                                            help_text="Lower = show first")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "vaccine_education_patient"
        indexes = [
            models.Index(fields=["vaccine", "language", "rank"]),
            models.Index(fields=["is_active"]),
        ]
        unique_together = [("vaccine", "language", "video_url")]

    def __str__(self) -> str:
        return f"PE[{self.language}] {self.vaccine.name} ({self.title or self.video_url})"

class VaccineEducationDoctor(models.Model):
    """
    Doctor education video(s) per Vaccine.
    Today language is mostly English, but we keep a field for flexibility.
    """
    vaccine = models.ForeignKey("Vaccine", on_delete=models.CASCADE,
                                related_name="doctor_education")
    language = models.CharField(max_length=5, default="en", db_index=True)
    title = models.CharField(max_length=200, blank=True, default="")
    video_url = models.URLField()
    platform = models.CharField(max_length=20, choices=VideoPlatform.choices,
                                default=VideoPlatform.VIMEO)
    rank = models.PositiveSmallIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "vaccine_education_doctor"
        indexes = [
            models.Index(fields=["vaccine", "rank"]),
            models.Index(fields=["is_active"]),
        ]
        unique_together = [("vaccine", "video_url")]

    def __str__(self) -> str:
        return f"DE {self.vaccine.name} ({self.title or self.video_url})"
class UiString(models.Model):
    key = models.CharField(max_length=120, unique=True)
    description = models.CharField(max_length=255, blank=True, default="")
    class Meta:
        db_table = "ui_string"
    def __str__(self): return self.key

class UiStringTranslation(models.Model):
    ui = models.ForeignKey(UiString, on_delete=models.CASCADE, related_name="translations")
    language = models.CharField(max_length=5, db_index=True)  # ISO-639-1
    text = models.TextField()
    class Meta:
        db_table = "ui_string_translation"
        unique_together = [("ui", "language")]
    def __str__(self): return f"{self.ui.key}[{self.language}]"


