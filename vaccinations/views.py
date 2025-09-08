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
