from __future__ import annotations
from datetime import date
from typing import List, Dict

from django.contrib import messages
from django.db.models import QuerySet
from django.db.models.functions import Length, Substr
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View

from .forms import AddChildForm, WhatsAppLookupForm
from .models import Parent, Child, ChildDose, VaccineDose
from .utils import today
from .services import reanchor_dependents

# -----------------------
# Helpers
# -----------------------

SESSION_PARENT_KEY = "parent_id"                 # primary parent id
SESSION_PARENT_IDS = "parent_ids"                # all equivalent parents' ids (same phone last-10)
SESSION_ANCHORED_ONCE = "anchored_child_dose_ids"

def require_parent_session(request):
    pid = request.session.get(SESSION_PARENT_KEY)
    if not pid:
        return None
    try:
        return Parent.objects.get(pk=pid)
    except Parent.DoesNotExist:
        return None

def _digits_only(raw: str) -> str:
    return "".join(ch for ch in (raw or "") if ch.isdigit())

def _equivalent_parents_by_input(wa_input: str) -> QuerySet:
    """
    Return ALL Parent rows that share the same last-10 digits with wa_input.
    If no 10 digits are available, try exact match; otherwise empty QS.
    Cross-backend (SQLite/MySQL/Postgres) via Substr/Length.
    """
    if not wa_input:
        return Parent.objects.none()

    # Try exact first (keeps previously stored canonical format working)
    exact = Parent.objects.filter(whatsapp_e164=wa_input)
    if exact.exists():
        wa = exact.first().whatsapp_e164
        digits = _digits_only(wa)
        last10 = digits[-10:] if len(digits) >= 10 else None
        if last10:
            return (
                Parent.objects
                .annotate(last10=Substr("whatsapp_e164", Length("whatsapp_e164") - 9, 10))
                .filter(last10=last10)
                .order_by("id")
            )
        return exact.order_by("id")

    # Fall back to user input's last 10
    digits = _digits_only(wa_input)
    last10 = digits[-10:] if len(digits) >= 10 else None
    if not last10:
        return Parent.objects.none()

    return (
        Parent.objects
        .annotate(last10=Substr("whatsapp_e164", Length("whatsapp_e164") - 9, 10))
        .filter(last10=last10)
        .order_by("id")
    )

def _set_parent_session(request, primary_parent: Parent, equivalent_parents: QuerySet):
    ids = list(equivalent_parents.values_list("id", flat=True))
    if primary_parent.id not in ids:
        ids.insert(0, primary_parent.id)
    request.session[SESSION_PARENT_KEY] = primary_parent.id
    request.session[SESSION_PARENT_IDS] = ids

def _route_to_child_list(request, parents_qs: QuerySet):
    """
    Render the selection page for ALL children of the equivalent parents.
    """
    if not parents_qs.exists():
        messages.error(request, "No records found for that WhatsApp number. Please add a record.")
        return render(request, "vaccinations/update_lookup.html", {"form": WhatsAppLookupForm()})

    primary = parents_qs.first()  # pick a stable "primary" (oldest id)
    _set_parent_session(request, primary, parents_qs)

    child_qs = Child.objects.filter(parent_id__in=list(parents_qs.values_list("id", flat=True)))
    children = list(child_qs.order_by("full_name", "date_of_birth"))
    if not children:
        messages.error(request, "No children found for this WhatsApp number. Please add a record.")
        return render(
            request,
            "vaccinations/update_lookup.html",
            {"form": WhatsAppLookupForm(initial={"parent_whatsapp": primary.whatsapp_e164})},
        )

    return render(
        request,
        "vaccinations/select_child.html",
        {"parent": primary, "children": children},
    )

def _compute_ui_state(child: Child, cds: List[ChildDose], show_all: bool, newly_anchored_ids: set = None) -> List[Dict]:
    """
    Build UI rows with correct status & editability.
    - show_all=True: include all doses (future + waiting)
    - show_all=False: include only due/overdue/given up to today, plus newly anchored doses
    - newly_anchored_ids: set of ChildDose IDs that should be shown even if future
    """
    t = today()
    if newly_anchored_ids is None:
        newly_anchored_ids = set()

    by_dose_id = {cd.dose_id: cd for cd in cds}
    rows = []
    for cd in cds:
        prev_required = cd.dose.previous_dose_id is not None
        prev_given = None
        if prev_required:
            prev_cd = by_dose_id.get(cd.dose.previous_dose_id)
            prev_given = prev_cd.given_date if prev_cd else None

        if cd.given_date:
            state = "given"
        elif cd.due_date is None or (prev_required and not prev_given):
            state = "waiting-previous"
        else:
            if t < cd.due_date:
                state = "future"
            else:
                if (cd.due_until_date is None) or (cd.due_date <= t <= cd.due_until_date):
                    state = "due"
                else:
                    state = "overdue"

        if not show_all and state in ("future", "waiting-previous"):
            if cd.id not in newly_anchored_ids:
                continue

        editable = (state in ("due", "overdue")) and (cd.given_date is None)

        rows.append({
            "child_dose": cd,
            "vaccine_name": cd.dose.vaccine.name,
            "dose_label": cd.dose.dose_label,
            "status": state,
            "editable": editable,
            "due_display": cd.due_date,
            "prev_label": (cd.dose.previous_dose.dose_label if cd.dose.previous_dose_id else ""),
            "is_newly_anchored": cd.id in newly_anchored_ids,
        })

    rows.sort(key=lambda r: (r["child_dose"].dose.vaccine.name, r["child_dose"].dose.sequence_index))
    return rows

# -----------------------
# Pages (Add & Update entrypoints)
# -----------------------

class HomeView(View):
    def get(self, request):
        return render(request, "vaccinations/home.html")

class AddRecordView(View):
    def get(self, request):
        return render(request, "vaccinations/add_record.html", {"form": AddChildForm()})

    def post(self, request):
        form = AddChildForm(request.POST)
        if not form.is_valid():
            return render(request, "vaccinations/add_record.html", {"form": form})

        wa_input = form.cleaned_data["parent_whatsapp"]

        # Reuse existing parent with the same last-10 digits if found; otherwise create new
        parents_qs = _equivalent_parents_by_input(wa_input)
        if parents_qs.exists():
            parent = parents_qs.first()
        else:
            parent = Parent.objects.create(whatsapp_e164=wa_input)
            parents_qs = Parent.objects.filter(pk=parent.pk)

        child = Child.objects.create(
            parent=parent,
            full_name=form.cleaned_data["child_name"],
            sex=form.cleaned_data["gender"],
            date_of_birth=form.cleaned_data["date_of_birth"],
            state=form.cleaned_data["state"],
        )

        _set_parent_session(request, parent, parents_qs)
        messages.success(request, "Record added successfully.")
        return redirect("vaccinations:card", child_id=child.id)

class UpdateLookupView(View):
    """
    GET:
      - If parent in session -> rebuild equivalence by last-10 and show the list.
      - Else -> show form (or accept ?wa= to resolve directly).
    POST:
      - Resolve by last-10 and show the list.
    """
    def get(self, request):
        parent = require_parent_session(request)
        if parent:
            parents_qs = _equivalent_parents_by_input(parent.whatsapp_e164)
            return _route_to_child_list(request, parents_qs)

        wa = request.GET.get("wa")
        if wa:
            parents_qs = _equivalent_parents_by_input(wa)
            return _route_to_child_list(request, parents_qs)

        return render(request, "vaccinations/update_lookup.html", {"form": WhatsAppLookupForm()})

    def post(self, request):
        form = WhatsAppLookupForm(request.POST)
        if not form.is_valid():
            return render(request, "vaccinations/update_lookup.html", {"form": form})
        wa = form.cleaned_data["parent_whatsapp"]
        parents_qs = _equivalent_parents_by_input(wa)
        return _route_to_child_list(request, parents_qs)

# -----------------------
# CARD VARIANT A: SHOW-ALL
# -----------------------

class VaccinationCardAllView(View):
    """
    Shows ALL doses (past, today, future).
    Editable only for due/overdue (not future / waiting-previous / given).
    """
    def get_child_and_check(self, request, child_id: int) -> Child:
        parent = require_parent_session(request)
        child = get_object_or_404(Child, pk=child_id)
        if not parent:
            messages.error(request, "Please verify your WhatsApp number to access this record.")
            return None
        allowed_ids = request.session.get(SESSION_PARENT_IDS, [parent.id])
        if child.parent_id not in allowed_ids:
            messages.error(request, "This record doesn't belong to your WhatsApp number.")
            return None
        return child

    def get(self, request, child_id: int):
        child = self.get_child_and_check(request, child_id)
        if not child:
            return redirect("vaccinations:update")

        cds = list(child.doses.select_related("dose__vaccine", "dose__previous_dose"))
        rows = _compute_ui_state(child, cds, show_all=True)
        return render(request, "vaccinations/card.html", {"child": child, "rows": rows, "today": today(), "show_all": True})

    def post(self, request, child_id: int):
        child = self.get_child_and_check(request, child_id)
        if not child:
            return redirect("vaccinations:update")

        t = today()
        editable_qs = (child.doses
                       .filter(due_date__isnull=False, due_date__lte=t, given_date__isnull=True)
                       .select_related("dose__vaccine"))

        changed = 0
        changed_bases: List[ChildDose] = []
        for cd in editable_qs:
            raw = (request.POST.get(f"dose_{cd.id}", "") or "").strip()
            if not raw:
                continue
            try:
                given = date.fromisoformat(raw)
            except Exception:
                messages.error(request, f"Invalid date for {cd.dose.dose_label}.")
                continue
            if given > t:
                messages.error(request, f"{cd.dose.dose_label} cannot be a future date.")
                continue

            cd.given_date = given
            cd.save(update_fields=["given_date", "updated_at"])
            changed += 1
            changed_bases.append(cd)

        newly_anchored = reanchor_dependents(child, changed_bases)

        if newly_anchored:
            txt = "; ".join([f"{x.dose.vaccine.name} — {x.dose.dose_label}: {x.due_date}" for x in newly_anchored])
            messages.success(request, f"Updated. Newly anchored next doses: {txt}")
        elif changed:
            messages.success(request, "Vaccination record updated.")
        else:
            messages.info(request, "No changes were made.")

        return redirect("vaccinations:card-all", child_id=child.id)

# -----------------------
# CARD VARIANT B: DUE-ONLY (past + today)
# -----------------------

class VaccinationCardDueView(View):
    """
    Shows only doses with due_date <= today (and given ones with such due dates).
    Plus newly anchored doses even if they are future.
    Editable only for due/overdue (not future / waiting-previous / given).
    """
    def get_child_and_check(self, request, child_id: int) -> Child:
        parent = require_parent_session(request)
        child = get_object_or_404(Child, pk=child_id)
        if not parent:
            messages.error(request, "Please verify your WhatsApp number to access this record.")
            return None
        allowed_ids = request.session.get(SESSION_PARENT_IDS, [parent.id])
        if child.parent_id not in allowed_ids:
            messages.error(request, "This record doesn't belong to your WhatsApp number.")
            return None
        return child

    def get(self, request, child_id: int):
        child = self.get_child_and_check(request, child_id)
        if not child:
            return redirect("vaccinations:update")

        t = today()
        cds_all = list(child.doses.select_related("dose__vaccine", "dose__previous_dose"))

        anchored_ids = set(request.session.pop(SESSION_ANCHORED_ONCE, []) or [])
        rows = _compute_ui_state(child, cds_all, show_all=False, newly_anchored_ids=anchored_ids)

        if anchored_ids:
            newly_anchored_rows = [r for r in rows if r.get("is_newly_anchored", False)]
            if newly_anchored_rows:
                txt = "; ".join([f"{r['vaccine_name']} — {r['dose_label']}: {r['due_display']}" for r in newly_anchored_rows])
                messages.success(request, f"Next dose(s) automatically scheduled: {txt}")

        return render(request, "vaccinations/card.html", {"child": child, "rows": rows, "today": t, "show_all": False})

    def post(self, request, child_id: int):
        child = self.get_child_and_check(request, child_id)
        if not child:
            return redirect("vaccinations:update")

        t = today()
        editable_qs = (child.doses
                       .filter(due_date__isnull=False, due_date__lte=t, given_date__isnull=True)
                       .select_related("dose__vaccine"))

        changed = 0
        changed_bases: List[ChildDose] = []
        for cd in editable_qs:
            raw = (request.POST.get(f"dose_{cd.id}", "") or "").strip()
            if not raw:
                continue
            try:
                given = date.fromisoformat(raw)
            except Exception:
                messages.error(request, f"Invalid date for {cd.dose.dose_label}.")
                continue
            if given > t:
                messages.error(request, f"{cd.dose.dose_label} cannot be a future date.")
                continue

            cd.given_date = given
            cd.save(update_fields=["given_date", "updated_at"])
            changed += 1
            changed_bases.append(cd)

        newly_anchored = reanchor_dependents(child, changed_bases)
        if newly_anchored:
            request.session[SESSION_ANCHORED_ONCE] = [cd.id for cd in newly_anchored]

        if changed and not newly_anchored:
            messages.success(request, "Vaccination record updated.")
        elif not changed:
            messages.info(request, "No changes were made.")

        return redirect("vaccinations:card", child_id=child.id)

# -----------------------
# Optional JSON endpoint (unchanged)
# -----------------------

from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from .serializers import ChildCardSerializer

class ChildCardAPI(RetrieveAPIView):
    queryset = (Child.objects.select_related("parent")
                .prefetch_related("doses__dose__vaccine"))
    permission_classes = [AllowAny]
    serializer_class = ChildCardSerializer
    lookup_field = "pk"

# --- Phase 2 views ---
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.core.files.uploadedfile import UploadedFile
import csv

from .models import Partner, FieldRepresentative, Doctor, Clinic
from .forms import (
    DoctorRegistrationSelfForm, DoctorRegistrationPartnerForm, DoctorClinicProfileForm,
    AddChildForm, WhatsAppLookupForm
)
from .services import send_doctor_portal_link

# ---------- Partner publishing (admin/staff only) ----------
def staff_required(u): return u.is_active and u.is_staff

@method_decorator(user_passes_test(staff_required), name="dispatch")
class PartnerCreateUploadView(View):
    """
    Single screen for system admin:
      - create a Partner
      - (optional) upload field reps CSV with columns: rep_code, full_name
    """
    template_name = "vaccinations/partners_create_upload.html"

    def get(self, request):
        return render(request, self.template_name, {"created": False})

    def post(self, request):
        name = (request.POST.get("partner_name", "") or "").strip()
        if not name:
            messages.error(request, "Partner name is required.")
            return render(request, self.template_name, {"created": False})

        partner = Partner.new(name)
        partner.save()
        created_reps = 0

        f: UploadedFile | None = request.FILES.get("csv_file")
        if f and f.size:
            try:
                decoded = f.read().decode("utf-8-sig").splitlines()
                reader = csv.DictReader(decoded)
                for row in reader:
                    code = (row.get("rep_code") or "").strip()
                    full_name = (row.get("full_name") or "").strip()
                    if not code or not full_name:
                        continue
                    FieldRepresentative.objects.update_or_create(
                        partner=partner, rep_code=code,
                        defaults={"full_name": full_name, "is_active": True}
                    )
                    created_reps += 1
            except Exception as ex:
                messages.error(request, f"Could not parse CSV: {ex}")
                return render(request, self.template_name, {"created": False})

        reg_link = request.build_absolute_uri(partner.doctor_registration_link)
        messages.success(request, f"Partner '{partner.name}' created with {created_reps} field reps.")
        return render(request, self.template_name, {
            "created": True,
            "partner": partner,
            "registration_link": reg_link,
        })

# ---------- Doctor registration (self) ----------
class DoctorRegisterSelfView(View):
    template_name = "vaccinations/doctor_register.html"

    def get(self, request):
        return render(request, self.template_name, {"form": DoctorRegistrationSelfForm(), "mode": "self"})

    def post(self, request):
        form = DoctorRegistrationSelfForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form, "mode": "self"})

        clinic = Clinic.objects.create(
            name=form.cleaned_data["doctor_name"],
            address=form.cleaned_data.get("clinic_address",""),
            phone="",  # optional
            state=form.cleaned_data["state"],
            headquarters=form.cleaned_data.get("head_quarters",""),
            pincode=form.cleaned_data.get("pincode",""),
            whatsapp_e164=form.cleaned_data.get("clinic_whatsapp",""),
            receptionist_email=form.cleaned_data.get("receptionist_email",""),
        )
        clinic.set_languages(form.cleaned_data.get("preferred_languages", []))
        clinic.save()

        doctor = Doctor.objects.create(
            clinic=clinic,
            full_name=form.cleaned_data["doctor_name"],
            whatsapp_e164=form.cleaned_data["doctor_whatsapp"],
            email=form.cleaned_data["doctor_email"],
            imc_number=form.cleaned_data["imc_number"],
            photo=form.cleaned_data.get("doctor_photo"),
        )
        send_doctor_portal_link(doctor, request)
        
        # For self registration, also redirect to WhatsApp
        import re
        import urllib.parse
        from django.urls import reverse
        
        # Clean and format phone number
        doctor_whatsapp = form.cleaned_data["doctor_whatsapp"]
        phone_number = re.sub(r'[^\d+]', '', doctor_whatsapp)
        if not phone_number.startswith('+'):
            if phone_number.startswith('91'):
                phone_number = '+' + phone_number
            elif phone_number.startswith('0'):
                phone_number = '+91' + phone_number[1:]
            else:
                phone_number = '+91' + phone_number
        
        # Remove + for WhatsApp URL
        clean_number = phone_number.replace('+', '')
        
        # Create WhatsApp URL with pre-filled message including portal link
        portal_link = request.build_absolute_uri(reverse("vaccinations:doc-home", args=[doctor.portal_token]))
        message = f"""Hello Dr. {doctor.full_name},

Please find below the link for your personalized vaccination system under the aegis of South Asia Pediatric Association (SAPA).

This system is supported for your clinic by the Serum Institute of India.

You can now send timely vaccination reminders to your patients. You can also keep track of your patient's vaccinations.

Link: {portal_link}"""
        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"https://wa.me/{clean_number}?text={encoded_message}"
        
        # Redirect to WhatsApp
        return redirect(whatsapp_url)

# ---------- Doctor registration (partner link, with field rep) ----------
class DoctorRegisterPartnerView(View):
    template_name = "vaccinations/doctor_register.html"

    def dispatch(self, request, token: str, *args, **kwargs):
        self.partner = Partner.objects.filter(registration_token=token).first()
        if not self.partner:
            messages.error(request, "Invalid or expired partner link.")
            return redirect("vaccinations:home")
        return super().dispatch(request, token, *args, **kwargs)

    def get(self, request, token: str):
        form = DoctorRegistrationPartnerForm(partner=self.partner)
        return render(request, self.template_name, {"form": form, "mode": "partner", "partner": self.partner})

    def post(self, request, token: str):
        form = DoctorRegistrationPartnerForm(request.POST, request.FILES, partner=self.partner)
        if not form.is_valid():
            print(f"Form validation failed: {form.errors}")
            return render(request, self.template_name, {"form": form, "mode": "partner", "partner": self.partner})

        print("Form is valid, creating doctor...")
        clinic = Clinic.objects.create(
            name=form.cleaned_data["doctor_name"],
            address=form.cleaned_data.get("clinic_address",""),
            phone="",
            state=form.cleaned_data["state"],
            headquarters=form.cleaned_data.get("head_quarters",""),
            pincode=form.cleaned_data.get("pincode",""),
            whatsapp_e164=form.cleaned_data.get("clinic_whatsapp",""),
            receptionist_email=form.cleaned_data.get("receptionist_email",""),
        )
        clinic.set_languages(form.cleaned_data.get("preferred_languages", []))
        clinic.save()

        doctor = Doctor.objects.create(
            clinic=clinic,
            full_name=form.cleaned_data["doctor_name"],
            whatsapp_e164=form.cleaned_data["doctor_whatsapp"],
            email=form.cleaned_data["doctor_email"],
            imc_number=form.cleaned_data["imc_number"],
            photo=form.cleaned_data.get("doctor_photo"),
            partner=self.partner,
            field_rep=form.cleaned_data["__field_rep_obj"],
        )
        send_doctor_portal_link(doctor, request)
        
        # Store the doctor's WhatsApp number before creating new form
        doctor_whatsapp = form.cleaned_data["doctor_whatsapp"]
        print(f"Doctor created successfully. WhatsApp: {doctor_whatsapp}")
        
        # For partner registration, redirect to WhatsApp immediately
        import re
        import urllib.parse
        from django.urls import reverse
        
        # Clean and format phone number
        phone_number = re.sub(r'[^\d+]', '', doctor_whatsapp)
        if not phone_number.startswith('+'):
            if phone_number.startswith('91'):
                phone_number = '+' + phone_number
            elif phone_number.startswith('0'):
                phone_number = '+91' + phone_number[1:]
            else:
                phone_number = '+91' + phone_number
        
        # Remove + for WhatsApp URL
        clean_number = phone_number.replace('+', '')
        
        # Create WhatsApp URL with pre-filled message including portal link
        portal_link = request.build_absolute_uri(reverse("vaccinations:doc-home", args=[doctor.portal_token]))
        message = f"""Hello Dr. {doctor.full_name},

Please find below the link for your personalized vaccination system under the aegis of South Asia Pediatric Association (SAPA).

This system is supported for your clinic by the Serum Institute of India.

You can now send timely vaccination reminders to your patients. You can also keep track of your patient's vaccinations.

Link: {portal_link}"""
        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"https://wa.me/{clean_number}?text={encoded_message}"
        
        # Redirect to WhatsApp
        return redirect(whatsapp_url)

# ---------- Doctor portal (token-based) ----------

class DoctorPortalMixin:
    doctor: Doctor = None

    def dispatch(self, request, token: str, *args, **kwargs):
        self.doctor = Doctor.objects.filter(portal_token=token, is_active=True).select_related("clinic").first()
        if not self.doctor:
            messages.error(request, "Invalid or inactive portal link.")
            return redirect("vaccinations:home")
        request._portal_doctor = self.doctor
        return super().dispatch(request, token, *args, **kwargs)

class DoctorPortalHomeView(DoctorPortalMixin, View):
    template_name = "vaccinations/doctor_portal_home.html"
    def get(self, request, token: str):
        return render(request, self.template_name, {"doctor": self.doctor})

# Reuse AddChildForm & logic, but force clinic to current doctor's clinic
class DoctorPortalAddRecordView(DoctorPortalMixin, View):
    template_name = "vaccinations/add_record.html"

    def get(self, request, token: str):
        return render(request, self.template_name, {"form": AddChildForm(), "header_home": self.doctor.portal_path})

    def post(self, request, token: str):
        form = AddChildForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form, "header_home": self.doctor.portal_path})
        wa = form.cleaned_data["parent_whatsapp"]
        parents_qs = _equivalent_parents_by_input(wa)  # existing helper
        if parents_qs.exists():
            parent = parents_qs.first()
        else:
            parent = Parent.objects.create(whatsapp_e164=wa)
            parents_qs = Parent.objects.filter(pk=parent.pk)
        child = Child.objects.create(
            parent=parent,
            clinic=self.doctor.clinic,   # <-- scope to this clinic
            full_name=form.cleaned_data["child_name"],
            sex=form.cleaned_data["gender"],
            date_of_birth=form.cleaned_data["date_of_birth"],
            state=form.cleaned_data["state"] or self.doctor.clinic.state,
        )
        messages.success(request, "Record added successfully.")
        # Use doctor-version of the card views:
        return redirect("vaccinations:doc-card", token=self.doctor.portal_token, child_id=child.id)

# Doctor lookup -> list children in THIS clinic only
class DoctorPortalUpdateLookupView(DoctorPortalMixin, View):
    template_name = "vaccinations/doctor_update_lookup.html"

    def get(self, request, token: str):
        return render(request, self.template_name, {"form": WhatsAppLookupForm(), "doctor": self.doctor})

    def post(self, request, token: str):
        form = WhatsAppLookupForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form, "doctor": self.doctor})
        wa = form.cleaned_data["parent_whatsapp"]
        parents_qs = _equivalent_parents_by_input(wa)
        child_qs = Child.objects.filter(
            parent_id__in=list(parents_qs.values_list("id", flat=True)),
            clinic=self.doctor.clinic,
        )
        children = list(child_qs.order_by("full_name", "date_of_birth"))
        return render(request, "vaccinations/doctor_select_child.html", {"doctor": self.doctor, "children": children})

# Card views (doctor-scoped authorization)
class DoctorPortalCardDueView(DoctorPortalMixin, View):
    def get_child(self, child_id: int) -> Child | None:
        child = get_object_or_404(Child, pk=child_id)
        if child.clinic_id != self.doctor.clinic_id:
            messages.error(self.request, "This record is not part of your clinic.")
            return None
        return child

    def get(self, request, token: str, child_id: int):
        child = self.get_child(child_id)
        if not child: return redirect("vaccinations:doc-update", token=self.doctor.portal_token)
        t = today()
        cds_all = list(child.doses.select_related("dose__vaccine", "dose__previous_dose"))
        rows = _compute_ui_state(child, cds_all, show_all=False, newly_anchored_ids=set())
        return render(request, "vaccinations/card.html", {"child": child, "rows": rows, "today": t, "show_all": False})

    def post(self, request, token: str, child_id: int):
        child = self.get_child(child_id)
        if not child: return redirect("vaccinations:doc-update", token=self.doctor.portal_token)
        t = today()
        editable_qs = (child.doses
            .filter(due_date__isnull=False, due_date__lte=t, given_date__isnull=True)
            .select_related("dose__vaccine"))
        changed = 0
        changed_bases: List[ChildDose] = []
        for cd in editable_qs:
            raw = (request.POST.get(f"dose_{cd.id}", "") or "").strip()
            if not raw: continue
            try:
                given = date.fromisoformat(raw)
            except Exception:
                messages.error(request, f"Invalid date for {cd.dose.dose_label}.")
                continue
            if given > t:
                messages.error(request, f"{cd.dose.dose_label} cannot be a future date.")
                continue
            cd.given_date = given
            cd.save(update_fields=["given_date", "updated_at"])
            changed += 1
            changed_bases.append(cd)
        newly_anchored = reanchor_dependents(child, changed_bases)
        if newly_anchored:
            txt = "; ".join([f"{x.dose.vaccine.name} — {x.dose.dose_label}: {x.due_date}" for x in newly_anchored])
            messages.success(request, f"Updated. Newly anchored next doses: {txt}")
        elif changed:
            messages.success(request, "Vaccination record updated.")
        else:
            messages.info(request, "No changes were made.")
        return redirect("vaccinations:doc-card", token=self.doctor.portal_token, child_id=child.id)

class DoctorPortalCardAllView(DoctorPortalMixin, View):
    def get_child(self, child_id: int) -> Child | None:
        child = get_object_or_404(Child, pk=child_id)
        if child.clinic_id != self.doctor.clinic_id:
            messages.error(self.request, "This record is not part of your clinic.")
            return None
        return child

    def get(self, request, token: str, child_id: int):
        child = self.get_child(child_id)
        if not child: return redirect("vaccinations:doc-update", token=self.doctor.portal_token)
        cds = list(child.doses.select_related("dose__vaccine", "dose__previous_dose"))
        rows = _compute_ui_state(child, cds, show_all=True)
        return render(request, "vaccinations/card.html", {"child": child, "rows": rows, "today": today(), "show_all": True})

    def post(self, request, token: str, child_id: int):
        # identical to DoctorPortalCardDueView.post but redirect back to card-all
        child = self.get_child(child_id)
        if not child: return redirect("vaccinations:doc-update", token=self.doctor.portal_token)
        t = today()
        editable_qs = (child.doses
            .filter(due_date__isnull=False, due_date__lte=t, given_date__isnull=True)
            .select_related("dose__vaccine"))
        changed = 0
        changed_bases: List[ChildDose] = []
        for cd in editable_qs:
            raw = (request.POST.get(f"dose_{cd.id}", "") or "").strip()
            if not raw: continue
            try:
                given = date.fromisoformat(raw)
            except Exception:
                messages.error(request, f"Invalid date for {cd.dose.dose_label}.")
                continue
            if given > t:
                messages.error(request, f"{cd.dose.dose_label} cannot be a future date.")
                continue
            cd.given_date = given
            cd.save(update_fields=["given_date", "updated_at"])
            changed += 1
            changed_bases.append(cd)
        newly_anchored = reanchor_dependents(child, changed_bases)
        if newly_anchored:
            txt = "; ".join([f"{x.dose.vaccine.name} — {x.dose.dose_label}: {x.due_date}" for x in newly_anchored])
            messages.success(request, f"Updated. Newly anchored next doses: {txt}")
        elif changed:
            messages.success(request, "Vaccination record updated.")
        else:
            messages.info(request, "No changes were made.")
        return redirect("vaccinations:doc-card-all", token=self.doctor.portal_token, child_id=child.id)

# Profile edit
class DoctorPortalEditProfileView(DoctorPortalMixin, View):
    template_name = "vaccinations/doctor_profile.html"

    def get(self, request, token: str):
        c = self.doctor.clinic
        initial = {
            "doctor_name": self.doctor.full_name,
            "doctor_whatsapp": self.doctor.whatsapp_e164,
            "clinic_whatsapp": c.whatsapp_e164,
            "state": c.state,
            "head_quarters": c.headquarters,
            "clinic_address": c.address,
            "preferred_languages": c.get_languages(),
            "pincode": c.pincode,
            "doctor_email": self.doctor.email,
            "receptionist_email": c.receptionist_email,
            "imc_number": self.doctor.imc_number,
        }
        return render(request, self.template_name, {
            "form": DoctorClinicProfileForm(initial=initial),
            "doctor": self.doctor
        })

    def post(self, request, token: str):
        form = DoctorClinicProfileForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form, "doctor": self.doctor})
        # update clinic
        c = self.doctor.clinic
        c.state = form.cleaned_data["state"]
        c.headquarters = form.cleaned_data.get("head_quarters","")
        c.address = form.cleaned_data.get("clinic_address","")
        c.set_languages(form.cleaned_data.get("preferred_languages", []))
        c.pincode = form.cleaned_data.get("pincode","")
        c.whatsapp_e164 = form.cleaned_data.get("clinic_whatsapp","")
        c.receptionist_email = form.cleaned_data.get("receptionist_email","")
        c.save()
        # update doctor
        self.doctor.full_name = form.cleaned_data["doctor_name"]
        self.doctor.whatsapp_e164 = form.cleaned_data["doctor_whatsapp"]
        self.doctor.email = form.cleaned_data["doctor_email"]
        self.doctor.imc_number = form.cleaned_data["imc_number"]
        if form.cleaned_data.get("doctor_photo"):
            self.doctor.photo = form.cleaned_data["doctor_photo"]
        self.doctor.save()
        messages.success(request, "Profile updated.")
        return redirect("vaccinations:doc-home", token=self.doctor.portal_token)
