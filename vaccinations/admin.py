from django.contrib import admin
from .models import (
    Partner, FieldRepresentative, Clinic, Doctor, 
    VaccineEducationPatient, VaccineEducationDoctor,
    Parent, Child, ChildDose, ScheduleVersion, Vaccine, VaccineDose,
    UiString, UiStringTranslation
)
from .utils import normalize_msisdn, hmac_sha256
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

@admin.register(VaccineEducationPatient)
class VaccineEducationPatientAdmin(admin.ModelAdmin):
    list_display = ("vaccine", "language", "title", "rank", "is_active")
    list_filter = ("language", "is_active", "vaccine__schedule_version")
    search_fields = ("title", "video_url", "vaccine__name", "vaccine__code")
    ordering = ("vaccine__name", "language", "rank")

@admin.register(VaccineEducationDoctor)
class VaccineEducationDoctorAdmin(admin.ModelAdmin):
    list_display = ("vaccine", "title", "rank", "is_active")
    list_filter = ("is_active", "vaccine__schedule_version")
    search_fields = ("title", "video_url", "vaccine__name", "vaccine__code")
    ordering = ("vaccine__name", "rank")

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ("id", "whatsapp_hash")
    search_fields = ("whatsapp_hash",)

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "sex", "date_of_birth", "parent", "clinic", "state")
    search_fields = ("full_name", "parent__whatsapp_hash")  # indexable
    # Optional: allow searching by clear number typed in the admin box
    def get_search_results(self, request, queryset, search_term):
        qs, use_distinct = super().get_search_results(request, queryset, search_term)
        phone = (normalize_msisdn(search_term) if hasattr(__import__('vaccinations.utils'), 'normalize_msisdn') else search_term.strip())
        if phone:
            qs |= self.model.objects.filter(parent__whatsapp_hash=hmac_sha256(phone.encode('utf-8')))
        return qs, use_distinct

@admin.register(ChildDose)
class ChildDoseAdmin(admin.ModelAdmin):
    search_fields = ("child__full_name", "dose__vaccine__name")
    list_filter = ("dose__vaccine__name",)
    
    def vaccine_name(self, obj):
        return obj.dose.vaccine.name
    vaccine_name.short_description = "Vaccine"
    
    def dose_label(self, obj):
        return obj.dose.dose_label
    dose_label.short_description = "Dose"

@admin.register(ScheduleVersion)
class ScheduleVersionAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_current", "effective_from")
    list_filter = ("is_current",)

@admin.register(Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "schedule_version", "is_active")
    list_filter = ("schedule_version", "is_active")
    search_fields = ("name", "code")

@admin.register(VaccineDose)
class VaccineDoseAdmin(admin.ModelAdmin):
    list_display = ("vaccine", "dose_label", "sequence_index", "min_offset_days", "previous_dose")
    list_filter = ("vaccine__schedule_version",)
    search_fields = ("vaccine__name", "dose_label")

@admin.register(UiString)
class UiStringAdmin(admin.ModelAdmin):
    list_display = ("key", "description")
    search_fields = ("key", "description")

@admin.register(UiStringTranslation)
class UiStringTranslationAdmin(admin.ModelAdmin):
    list_display = ("ui", "language", "text")
    list_filter = ("language",)
    search_fields = ("ui__key", "text")
