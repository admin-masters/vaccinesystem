# Doctor Portal Add Patient and Share Link

## 1. Title
Doctor Portal Add Patient and Share Link

## 2. Document Purpose
Teach clinic staff how to register a patient, create the patient vaccination card, and understand the optional share-link handoff to the parent.

## 3. Primary User
Doctor or clinic staff member working inside the portal

## 4. Entry Point
Doctor portal home `/d/<token>/` -> Add-a-patient

## 5. Workflow Summary
From the portal, the doctor can add a patient by recording child details and the parent’s WhatsApp number. The portal supports a standard submit path and also shows a Register & Send to Patient action that opens WhatsApp Web with a shareable card link.

## 6. Step-By-Step Instructions

### Step 1. Open the add-patient form
- What the user does: Choose Add-a-patient from the portal home.
- What the user sees: The child registration form with Submit and Register & Send to Patient actions.
- Why the step matters: This is the clinic-side starting point for bringing a new child into the system.
- Expected result: The clinic user can record patient details and decide whether to also hand off a share link.
- Common issues or trainer notes: The send button is only shown inside the doctor portal, not on the public parent add flow.
- Screenshot placeholder section:
  - Suggested file path: `docs/product-user-flows/assets/doctor-portal-add-patient-and-share-link/01-doctor-add-patient-form.png`
  - Screenshot caption: Doctor portal add-patient form with both action buttons
  - What the screenshot should show: The form and the Register & Send to Patient button.

### Step 2. Create the patient record
- What the user does: Submit the child details and parent WhatsApp number.
- What the user sees: The child’s vaccination card inside the doctor portal.
- Why the step matters: This confirms that the patient record and linked vaccination schedule were created successfully.
- Expected result: The doctor can immediately review and update the child card.
- Common issues or trainer notes: The child is scoped to the doctor’s clinic for later update and reminder workflows.
- Screenshot placeholder section:
  - Suggested file path: `docs/product-user-flows/assets/doctor-portal-add-patient-and-share-link/02-doctor-card-after-add.png`
  - Screenshot caption: Doctor view of the vaccination card after adding a patient
  - What the screenshot should show: The doctor-facing vaccination card returned after patient creation.

### Step 3. Use the optional share-link path
- What the user does: Choose Register & Send to Patient instead of the standard submit action when appropriate.
- What the user sees: WhatsApp Web opens with a bilingual message and the parent share link.
- Why the step matters: This enables the clinic to hand off self-service access to the parent at the moment of registration.
- Expected result: The parent receives a direct verification link to the child card.
- Common issues or trainer notes: The final messaging step happens outside the app in WhatsApp Web.
- Screenshot placeholder section:
  - Suggested file path: `docs/product-user-flows/assets/doctor-portal-add-patient-and-share-link/01-doctor-add-patient-form.png`
  - Screenshot caption: The add-patient screen where the share-link handoff is initiated
  - What the screenshot should show: The same add-patient form, highlighting the Register & Send to Patient button.

## 7. Success Criteria
- The clinic can open the add-patient form.
- Submitting the form creates the child vaccination card.
- Staff understand that the optional send action opens WhatsApp Web with a share link.

## 8. Related Documents
- [06-doctor-portal-update-card-and-profile.md](06-doctor-portal-update-card-and-profile.md)
- [08-parent-self-service-card-history-and-share-link.md](08-parent-self-service-card-history-and-share-link.md)

## 9. Status
Validated against the local demo build on April 9, 2026. Documentation reflects live behavior; mismatches with older expectations are noted.
