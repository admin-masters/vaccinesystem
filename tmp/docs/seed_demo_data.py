#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def bootstrap_django() -> None:
    root = repo_root()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vaccination_project.settings_local")

    import django

    django.setup()


def ensure_partner_csv(csv_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    if csv_path.exists():
        return
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["rep_code", "full_name"])
        writer.writerow(["REP001", "Anita Rao"])
        writer.writerow(["REP002", "Rahul Menon"])


def main() -> None:
    bootstrap_django()

    from django.conf import settings
    from django.db import transaction
    from vaccinations.models import (
        Child,
        ChildDose,
        ChildShareLink,
        Clinic,
        Doctor,
        FieldRepresentative,
        Parent,
        Partner,
        Vaccine,
        VaccineEducationDoctor,
        VaccineEducationPatient,
        VaccineDose,
    )

    root = repo_root()
    docs_tmp = root / "tmp" / "docs"
    state_path = docs_tmp / "demo_state.json"
    csv_path = docs_tmp / "demo_field_reps.csv"
    ensure_partner_csv(csv_path)

    partner, _ = Partner.objects.update_or_create(
        slug="demo-health-network",
        defaults={
            "name": "Demo Health Network",
            "registration_token": "partner-demo-onboarding",
        },
    )

    for rep_code, full_name in [("REP001", "Anita Rao"), ("REP002", "Rahul Menon")]:
        FieldRepresentative.objects.update_or_create(
            partner=partner,
            rep_code=rep_code,
            defaults={"full_name": full_name, "is_active": True},
        )

    clinic_self, _ = Clinic.objects.update_or_create(
        name="Sunrise Pediatrics",
        defaults={
            "address": "12 Lake View Road, Bengaluru",
            "phone": "+918035551234",
            "state": "Karnataka",
            "headquarters": "Bengaluru",
            "pincode": "560001",
            "whatsapp_e164": "+918035551234",
            "receptionist_email": "frontdesk.sunrise@gmail.com",
        },
    )
    clinic_self.set_languages(["en", "kn", "hi"])
    clinic_self.save()

    clinic_partner, _ = Clinic.objects.update_or_create(
        name="Riverfront Child Clinic",
        defaults={
            "address": "8 MG Road, Kochi",
            "phone": "+914842221234",
            "state": "Kerala",
            "headquarters": "Kochi",
            "pincode": "682001",
            "whatsapp_e164": "+914842221234",
            "receptionist_email": "frontdesk.riverfront@gmail.com",
        },
    )
    clinic_partner.set_languages(["en", "ml", "hi"])
    clinic_partner.save()

    doctor_self, _ = Doctor.objects.update_or_create(
        imc_number="IMC-DEMO-SELF-001",
        defaults={
            "clinic": clinic_self,
            "full_name": "Dr. Meera Shah",
            "whatsapp_e164": "+919901112233",
            "email": "dr.meera.shah@gmail.com",
            "portal_token": "doctor-self-demo-token",
            "partner": None,
            "field_rep": None,
            "is_active": True,
        },
    )

    doctor_partner, _ = Doctor.objects.update_or_create(
        imc_number="IMC-DEMO-PARTNER-001",
        defaults={
            "clinic": clinic_partner,
            "full_name": "Dr. Arjun Nair",
            "whatsapp_e164": "+919812223344",
            "email": "dr.arjun.nair@gmail.com",
            "portal_token": "doctor-partner-demo-token",
            "partner": partner,
            "field_rep": FieldRepresentative.objects.get(partner=partner, rep_code="REP001"),
            "is_active": True,
        },
    )

    parents = []
    for raw_number in ["+919876543210", "+919812345678"]:
        parent_hash = Parent.hash_for(raw_number)
        parent = Parent.objects.using("patients").filter(whatsapp_hash=parent_hash).first()
        if not parent:
            parent = Parent.objects.using("patients").create()
        parent.whatsapp_e164 = raw_number
        parent.save(using="patients")
        parents.append(parent)

    parent_public, parent_partner = parents

    with transaction.atomic(using="patients"):
        child_primary, _ = Child.objects.using("patients").update_or_create(
            parent=parent_public,
            full_name="Aarav Demo",
            defaults={
                "date_of_birth": date(2025, 10, 10),
                "sex": Child.Sex.MALE,
                "state": "Karnataka",
                "clinic": clinic_self,
            },
        )
        child_secondary, _ = Child.objects.using("patients").update_or_create(
            parent=parent_public,
            full_name="Anaya Demo",
            defaults={
                "date_of_birth": date(2024, 6, 15),
                "sex": Child.Sex.FEMALE,
                "state": "Karnataka",
                "clinic": clinic_self,
            },
        )
        child_partner, _ = Child.objects.using("patients").update_or_create(
            parent=parent_partner,
            full_name="Nila Demo",
            defaults={
                "date_of_birth": date(2025, 12, 5),
                "sex": Child.Sex.FEMALE,
                "state": "Kerala",
                "clinic": clinic_partner,
            },
        )

    def seed_given_dates(child: Child, count: int) -> None:
        doses = list(
            ChildDose.objects.using("patients")
            .filter(child=child)
            .order_by("due_date", "id")
        )
        for idx, cd in enumerate(doses[:count], start=1):
            base_date = child.get_date_of_birth_encrypted() or child.date_of_birth
            given = base_date + timedelta(days=idx * 3)
            ChildDose.objects.using("patients").filter(pk=cd.pk).update(given_date=given)

    seed_given_dates(child_primary, 3)
    seed_given_dates(child_secondary, 5)
    seed_given_dates(child_partner, 2)

    share_link, _ = ChildShareLink.objects.using("patients").update_or_create(
        token="share-demo-card-link",
        defaults={
            "child": child_primary,
            "expected_last10": parent_public.whatsapp_e164[-10:],
            "created_by": doctor_self,
            "is_active": True,
        },
    )

    patient_vaccine = (
        VaccineEducationPatient.objects.order_by("vaccine_id", "language").first()
    )
    doctor_vaccine = (
        VaccineEducationDoctor.objects.order_by("vaccine_id", "language").first()
    )

    fallback_patient_vaccine = Vaccine.objects.filter(code="bcg").first() or Vaccine.objects.order_by("id").first()
    fallback_doctor_vaccine = Vaccine.objects.filter(code="bcg").first() or Vaccine.objects.order_by("id").first()

    state = {
        "admin_access_password": settings.SECRET_KEY[:12],
        "partner": {
            "name": partner.name,
            "registration_token": partner.registration_token,
        },
        "field_rep": {
            "code": "REP001",
            "name": "Anita Rao",
        },
        "self_doctor": {
            "name": doctor_self.full_name,
            "portal_token": doctor_self.portal_token,
            "email": doctor_self.email,
            "clinic_name": clinic_self.name,
        },
        "partner_doctor": {
            "name": doctor_partner.full_name,
            "portal_token": doctor_partner.portal_token,
            "email": doctor_partner.email,
            "clinic_name": clinic_partner.name,
        },
        "parents": {
            "public": {
                "whatsapp": parent_public.whatsapp_e164,
            },
            "partner": {
                "whatsapp": parent_partner.whatsapp_e164,
            },
        },
        "children": {
            "primary": {
                "id": child_primary.id,
                "name": child_primary.get_child_name(),
                "share_token": share_link.token,
            },
            "secondary": {
                "id": child_secondary.id,
                "name": child_secondary.get_child_name(),
            },
            "partner": {
                "id": child_partner.id,
                "name": child_partner.get_child_name(),
            },
        },
        "vaccines": {
            "patient_education_vaccine_id": (
                patient_vaccine.vaccine_id if patient_vaccine else fallback_patient_vaccine.id
            ),
            "doctor_education_vaccine_id": (
                doctor_vaccine.vaccine_id if doctor_vaccine else fallback_doctor_vaccine.id
            ),
        },
        "assets": {
            "field_rep_csv": str(csv_path),
        },
    }

    state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
    print(f"Wrote demo state to {state_path}")


if __name__ == "__main__":
    main()
