from __future__ import annotations
from django import forms
from .models import Child
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
