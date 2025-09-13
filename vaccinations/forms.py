from __future__ import annotations
from django import forms
from .models import Child, LANGUAGE_CHOICES, Partner, FieldRepresentative, Doctor, Clinic
from .utils import normalize_msisdn

INDIAN_STATES = [
    "Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana",
    "Himachal Pradesh","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur",
    "Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana",
    "Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar Islands",
    "Chandigarh","Dadra and Nagar Haveli and Daman and Diu","Delhi","Jammu and Kashmir",
    "Ladakh","Lakshadweep","Puducherry"
]

class AddChildForm(forms.Form):
    child_name = forms.CharField(label="Child's Name", max_length=120)
    gender = forms.ChoiceField(choices=[("M","Male"),("F","Female"),("O","Other")])
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type":"date"}))
    state = forms.ChoiceField(choices=[("", "Select State")] + [(s, s) for s in INDIAN_STATES])
    parent_whatsapp = forms.CharField(label="Parent's WhatsApp No.", max_length=20)

    def clean_parent_whatsapp(self):
        return normalize_msisdn(self.cleaned_data["parent_whatsapp"])

class WhatsAppLookupForm(forms.Form):
    parent_whatsapp = forms.CharField(label="Parent's WhatsApp No.", max_length=20)

    def clean_parent_whatsapp(self):
        return normalize_msisdn(self.cleaned_data["parent_whatsapp"])

# --- Phase 2 forms (doctor registration & profile) ---

class DoctorRegistrationBaseForm(forms.Form):
    doctor_name = forms.CharField(label="Doctor's Name", max_length=120)
    doctor_whatsapp = forms.CharField(label="Doctor's WhatsApp Number", max_length=20)
    clinic_whatsapp = forms.CharField(label="Clinic WhatsApp Number", max_length=20, required=False)
    doctor_photo = forms.ImageField(label="Upload Doctor Photo", required=False)
    state = forms.ChoiceField(label="State", choices=[("", "Please select a state")] + [(s, s) for s in INDIAN_STATES])
    head_quarters = forms.CharField(label="Head Quarters", max_length=120, required=False)
    clinic_address = forms.CharField(label="Clinic Address", widget=forms.Textarea, required=False)
    preferred_languages = forms.MultipleChoiceField(
        label="Choose Preferred Languages for the patient to fill the form",
        choices=LANGUAGE_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    pincode = forms.CharField(label="Pincode", max_length=10, required=False)
    doctor_email = forms.EmailField(label="Doctor's Email ID")
    receptionist_email = forms.EmailField(label="Receptionist's Email ID", required=False)
    imc_number = forms.CharField(label="Indian Medical Council Number", max_length=30)

    def clean_doctor_whatsapp(self):
        return normalize_msisdn(self.cleaned_data["doctor_whatsapp"])

    def clean_clinic_whatsapp(self):
        raw = self.cleaned_data.get("clinic_whatsapp", "")
        return normalize_msisdn(raw) if raw else raw

    def clean_doctor_email(self):
        email = self.cleaned_data.get("doctor_email", "")
        if email and not email.endswith("@gmail.com"):
            raise forms.ValidationError("Please enter a valid Gmail ID (ending with @gmail.com)")
        return email

    def clean_receptionist_email(self):
        email = self.cleaned_data.get("receptionist_email", "")
        if email and not email.endswith("@gmail.com"):
            raise forms.ValidationError("Please enter a valid Gmail ID (ending with @gmail.com)")
        return email

class DoctorRegistrationSelfForm(DoctorRegistrationBaseForm):
    """Self-registration: no field rep fields."""
    pass

class DoctorRegistrationPartnerForm(DoctorRegistrationBaseForm):
    field_rep_code = forms.CharField(label="Field Rep Code", max_length=50)
    field_rep_name = forms.CharField(label="Field Rep Name", max_length=120)

    def __init__(self, *args, partner: Partner, **kwargs):
        super().__init__(*args, **kwargs)
        self.partner = partner

    def clean(self):
        cleaned = super().clean()
        code = cleaned.get("field_rep_code", "").strip()
        name = (cleaned.get("field_rep_name", "") or "").strip()
        try:
            fr = FieldRepresentative.objects.get(partner=self.partner, rep_code=code, is_active=True)
        except FieldRepresentative.DoesNotExist:
            raise forms.ValidationError("Invalid field rep code for this partner.")
        if name and name.lower() != fr.full_name.strip().lower():
            # non-fatal: we keep DB record truth - just add a warning, don't fail validation
            pass  # Remove the error to make it non-fatal
        cleaned["__field_rep_obj"] = fr
        return cleaned

class DoctorClinicProfileForm(DoctorRegistrationBaseForm):
    """Used in doctor portal to edit profile; same fields as registration."""
    # no field rep here
    pass
