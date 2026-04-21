# Doctor Portal Update Card and Profile

## 1. Title
Doctor Portal Update Card and Profile

## 2. Document Purpose
Train clinic users on finding an existing patient, opening the card, updating vaccine dates, and maintaining the doctor/clinic profile.

## 3. Primary User
Doctor or clinic staff member

## 4. Entry Point
Doctor portal home -> Update a patient record, plus Edit doctor/clinic profile

## 5. Workflow Summary
This workflow covers the day-to-day clinic maintenance path: look up a parent by WhatsApp number, select the correct child, open the vaccination card, and update clinic profile details as needed.

## 6. Step-By-Step Instructions

### Step 1. Search by parent WhatsApp number
- What the user does: Open Update a patient record and enter the parent’s WhatsApp number.
- What the user sees: A WhatsApp lookup form specific to the doctor portal.
- Why the step matters: This is the quickest way to retrieve a family’s children already linked to the clinic.
- Expected result: The system is ready to show the matching child list.
- Common issues or trainer notes: The number lookup is based on the stored WhatsApp number.
- Screenshot placeholder section:
  - Suggested file path: `docs/product-user-flows/assets/doctor-portal-update-card-and-profile/01-doctor-update-lookup.png`
  - Screenshot caption: Doctor-side lookup form for an existing patient
  - What the screenshot should show: The clinic-scoped WhatsApp lookup screen.

### Step 2. Choose the correct child
- What the user does: Submit the lookup and review the matching children.
- What the user sees: A child-selection screen with actions for Open Vaccination Card, Full Schedule, and Send Reminders.
- Why the step matters: A single parent may have multiple children, so the clinic must choose the right record before editing anything.
- Expected result: The clinic can continue into the correct child workflow.
- Common issues or trainer notes: Only children in the current clinic appear in this list.
- Screenshot placeholder section:
  - Suggested file path: `docs/product-user-flows/assets/doctor-portal-update-card-and-profile/02-doctor-select-child.png`
  - Screenshot caption: Doctor-facing child selection after WhatsApp lookup
  - What the screenshot should show: The list of matched children and their action buttons.

### Step 3. Open and update the vaccination card
- What the user does: Open the due-only or full vaccination card and record given dates where needed.
- What the user sees: The doctor-facing vaccination card with due, overdue, given, and future status states.
- Why the step matters: This is the operational heart of the clinic workflow: maintaining the child’s vaccination record.
- Expected result: The card reflects the latest known vaccination dates.
- Common issues or trainer notes: The product automatically recalculates dependent doses when a given date changes.
- Screenshot placeholder section:
  - Suggested file path: `docs/product-user-flows/assets/doctor-portal-update-card-and-profile/03-doctor-vaccination-card.png`
  - Screenshot caption: Doctor view of the patient vaccination card
  - What the screenshot should show: The card layout with editable date inputs and schedule statuses.

### Step 4. Maintain the clinic profile
- What the user does: Open Edit doctor/clinic profile from the portal home.
- What the user sees: A profile form for doctor details, clinic contact data, languages, and IMC number.
- Why the step matters: Clinic identity, language settings, and contact details need to stay current for patient communication to work well.
- Expected result: The clinic profile can be updated without leaving the portal.
- Common issues or trainer notes: Preferred languages influence downstream patient-facing messaging.
- Screenshot placeholder section:
  - Suggested file path: `docs/product-user-flows/assets/doctor-portal-update-card-and-profile/04-doctor-profile.png`
  - Screenshot caption: Doctor and clinic profile maintenance screen
  - What the screenshot should show: The profile form with clinic and doctor data.

## 7. Success Criteria
- The clinic can find patients by parent WhatsApp number.
- The correct child record is opened within the clinic scope.
- The doctor/clinic profile can be updated from the same portal.

## 8. Related Documents
- [05-doctor-portal-add-patient-and-share-link.md](05-doctor-portal-add-patient-and-share-link.md)
- [07-reminders-and-education-workflows.md](07-reminders-and-education-workflows.md)

## 9. Status
Validated against the local demo build on April 9, 2026. Documentation reflects live behavior; mismatches with older expectations are noted.
