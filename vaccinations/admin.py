from django.contrib import admin
from .models import Partner, FieldRepresentative, Clinic, Doctor

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "registration_token", "created_at")
    search_fields = ("name", "slug", "registration_token")

@admin.register(FieldRepresentative)
class FieldRepAdmin(admin.ModelAdmin):
    list_display = ("partner", "rep_code", "full_name", "is_active", "created_at")
    list_filter = ("partner", "is_active")
    search_fields = ("rep_code", "full_name")

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ("name", "state", "pincode", "whatsapp_e164")
    search_fields = ("name", "state", "pincode")

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "clinic", "email", "imc_number", "partner", "field_rep", "portal_token")
    list_filter = ("partner",)
    search_fields = ("full_name", "email", "imc_number", "portal_token")
