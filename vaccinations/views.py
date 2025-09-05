from __future__ import annotations
from datetime import date
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.utils import timezone

from .forms import AddChildForm, WhatsAppLookupForm
from .models import Parent, Child, ChildDose
from .utils import today, status_code_for

# -----------------------
# Helpers
# -----------------------
SESSION_PARENT_KEY = "parent_id"

def require_parent_session(request):
    pid = request.session.get(SESSION_PARENT_KEY)
    if not pid:
        return None
    try:
        return Parent.objects.get(pk=pid)
    except Parent.DoesNotExist:
        return None

# -----------------------
# Pages
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

        # Find/create parent
        wa = form.cleaned_data["parent_whatsapp"]
        parent, _ = Parent.objects.get_or_create(whatsapp_e164=wa)

        # Create child
        child = Child.objects.create(
            parent=parent,
            full_name=form.cleaned_data["child_name"],
            sex=form.cleaned_data["gender"],
            date_of_birth=form.cleaned_data["date_of_birth"],
            state=form.cleaned_data["state"],
        )

        # Persist parent session
        request.session[SESSION_PARENT_KEY] = parent.id
        messages.success(request, "Record added successfully.")
        return redirect("vaccinations:card", child_id=child.id)

class UpdateLookupView(View):
    """
    GET:
      - If parent in session:
          * 1 child  -> go straight to card
          * >1 child -> show selection
          * 0 child  -> show WhatsApp form + message
      - Else: show WhatsApp form
    POST:
      - Verify WhatsApp, set session, then same behavior as above.
    """
    def _route_for_parent(self, request, parent):
        children = list(parent.children.order_by("full_name", "date_of_birth"))
        if len(children) == 1:
            return redirect("vaccinations:card", child_id=children[0].id)
        if len(children) > 1:
            return render(request, "vaccinations/select_child.html",
                          {"parent": parent, "children": children})
        messages.error(request, "No children found for this WhatsApp number. Please add a record.")
        return render(request, "vaccinations/update_lookup.html",
                      {"form": WhatsAppLookupForm(initial={"parent_whatsapp": parent.whatsapp_e164})})

    def get(self, request):
        parent = require_parent_session(request)
        if parent:
            return self._route_for_parent(request, parent)
        return render(request, "vaccinations/update_lookup.html", {"form": WhatsAppLookupForm()})

    def post(self, request):
        form = WhatsAppLookupForm(request.POST)
        if not form.is_valid():
            return render(request, "vaccinations/update_lookup.html", {"form": form})

        wa = form.cleaned_data["parent_whatsapp"]
        parent = Parent.objects.filter(whatsapp_e164=wa).first()
        if not parent:
            messages.error(request, "No records found for that WhatsApp number. Please add a record first.")
            return render(request, "vaccinations/update_lookup.html", {"form": form})

        request.session[SESSION_PARENT_KEY] = parent.id
        return self._route_for_parent(request, parent)

class VaccinationCardView(View):
    """
    Show and update a single child's vaccination card.
    - Shows only doses with due_date <= today (or already given with due_date <= today)
    - Given = green and disabled; due/overdue = pink and editable
    """
    def get_child_and_check(self, request, child_id: int) -> Child:
        parent = require_parent_session(request)
        child = get_object_or_404(Child, pk=child_id)
        if not parent or child.parent_id != parent.id:
            messages.error(request, "Please verify your WhatsApp number to access this record.")
            return None
        return child

    def get(self, request, child_id: int):
        child = self.get_child_and_check(request, child_id)
        if not child:
            return redirect("vaccinations:update")

        t = today()
        doses = (child.doses
                 .select_related("dose__vaccine")
                 .filter(due_date__isnull=False, due_date__lte=t)
                 .order_by("dose__vaccine__name", "dose__sequence_index"))

        rows = []
        for cd in doses:
            status = status_code_for(cd.due_date, cd.due_until_date, cd.given_date)
            editable = cd.given_date is None
            rows.append({
                "child_dose": cd,
                "vaccine_name": cd.dose.vaccine.name,
                "dose_label": cd.dose.dose_label,
                "status": status,
                "editable": editable,
                # due_display is shown as a hint; input value is left blank by design
                "due_display": cd.due_date,
            })

        ctx = {"child": child, "rows": rows, "today": t}
        return render(request, "vaccinations/card.html", ctx)

    def post(self, request, child_id: int):
        child = self.get_child_and_check(request, child_id)
        if not child:
            return redirect("vaccinations:update")

        t = today()
        editable_qs = (child.doses
                       .filter(due_date__isnull=False, due_date__lte=t, given_date__isnull=True)
                       .select_related("dose__vaccine"))

        changed = 0
        for cd in editable_qs:
            key = f"dose_{cd.id}"
            # Only set if a non-empty value was submitted
            raw = request.POST.get(key, "").strip()
            if not raw:
                continue
            try:
                cd.given_date = date.fromisoformat(raw)
            except Exception:
                messages.error(request, f"Invalid date for {cd.dose.dose_label}.")
                continue
            if cd.given_date > t:
                messages.error(request, f"{cd.dose.dose_label} cannot be a future date.")
                continue
            cd.save(update_fields=["given_date", "updated_at"])
            changed += 1

        if changed:
            messages.success(request, "Vaccination record updated.")
        else:
            messages.info(request, "No changes were made.")

        return redirect("vaccinations:card", child_id=child.id)


# -----------------------
# Optional JSON endpoint
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
