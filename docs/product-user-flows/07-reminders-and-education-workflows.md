# Reminders and Education Workflows

## 1. Title
Reminders and Education Workflows

## 2. Document Purpose
Train clinic users on monitoring due doses, sending reminders, and opening the supporting vaccine education pages for providers and parents.

## 3. Primary User
Doctor or clinic staff member managing patient follow-up

## 4. Entry Point
Doctor portal -> Reminders, child reminder screens, and education pages

## 5. Workflow Summary
The clinic can review due and overdue doses, open child-level reminder schedules, and use linked education pages to reinforce communication with families. Reminder sending currently hands off to WhatsApp with a prefilled message.

## 6. Step-By-Step Instructions

### Step 1. Review the clinic-wide reminder dashboard
- What the user does: Open Reminders from the portal home.
- What the user sees: A reminder dashboard with status filters, vaccine filter, search, and Send Reminder actions.
- Why the step matters: This is the clinic’s queue view for follow-up work across all patients.
- Expected result: The clinic can identify who is due, overdue, upcoming, or already reminded.
- Common issues or trainer notes: Search accepts child text and mobile-number lookups.
- Screenshot placeholder section:
  - Suggested file path: `docs/product-user-flows/assets/reminders-and-education-workflows/01-reminders-dashboard.png`
  - Screenshot caption: Clinic-wide reminders dashboard
  - What the screenshot should show: The dashboard filters, patient rows, status text, and reminder buttons.

### Step 2. Inspect one child’s reminder schedule
- What the user does: Open the reminder detail screen for a specific child.
- What the user sees: A child-level table showing vaccine reminder status and eligibility.
- Why the step matters: This narrows the follow-up conversation to one patient when the clinic needs detail.
- Expected result: The clinic can see exactly which reminder actions are available for the child.
- Common issues or trainer notes: The child-level page is especially useful before sending a reminder manually.
- Screenshot placeholder section:
  - Suggested file path: `docs/product-user-flows/assets/reminders-and-education-workflows/02-child-reminders.png`
  - Screenshot caption: Child-level reminder schedule in the doctor portal
  - What the screenshot should show: The list of vaccine statuses and reminder actions for one child.

### Step 3. Open doctor-facing vaccine education
- What the user does: Open a vaccine education page from the reminder or card workflow.
- What the user sees: The provider education page for that vaccine.
- Why the step matters: Doctors may need refresher content or supporting material before discussing the vaccine with families.
- Expected result: The provider can access vaccine education without leaving the workflow context.
- Common issues or trainer notes: This page is provider-focused, separate from the simplified patient education page used in reminder links.
- Screenshot placeholder section:
  - Suggested file path: `docs/product-user-flows/assets/reminders-and-education-workflows/03-doctor-vaccine-education.png`
  - Screenshot caption: Doctor-facing vaccine education page
  - What the screenshot should show: The provider education view opened from the workflow.

### Step 4. Understand the patient education destination
- What the user does: Open the simplified patient education page used in reminder messaging.
- What the user sees: A patient-friendly video page with language-aware vaccine education content.
- Why the step matters: This is the educational destination parents reach from reminder messages.
- Expected result: The clinic understands what families see after clicking an education link.
- Common issues or trainer notes: This page is public and optimized for parent-facing education consumption.
- Screenshot placeholder section:
  - Suggested file path: `docs/product-user-flows/assets/reminders-and-education-workflows/04-patient-education-simple.png`
  - Screenshot caption: Simplified patient education page used by reminder links
  - What the screenshot should show: The public patient education view with vaccine videos.

## 7. Success Criteria
- The clinic can read the reminder dashboard filters and eligible actions.
- Staff can inspect reminder status for one child.
- Provider and patient education pages can be opened from the workflow.

## 8. Related Documents
- [06-doctor-portal-update-card-and-profile.md](06-doctor-portal-update-card-and-profile.md)
- [08-parent-self-service-card-history-and-share-link.md](08-parent-self-service-card-history-and-share-link.md)

## 9. Status
Validated against the local demo build on April 9, 2026. Documentation reflects live behavior; mismatches with older expectations are noted.
