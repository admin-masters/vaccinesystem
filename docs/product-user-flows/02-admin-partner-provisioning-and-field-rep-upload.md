# Admin Partner Provisioning and Field Rep Upload

## 1. Title
Admin Partner Provisioning and Field Rep Upload

## 2. Document Purpose
Show how a partner administrator opens the partner workspace, creates a partner profile, uploads field representatives, and generates a doctor registration link.

## 3. Primary User
Partner admin, field operations lead, or internal business operations owner

## 4. Entry Point
Admin access gate at `/admin/access/`, followed by `/partners/new/`

## 5. Workflow Summary
The live product provides a lightweight admin password gate for partner setup. After access is granted, the admin can create a partner, upload field rep CSV data, and obtain a doctor registration link to circulate.

## 6. Step-By-Step Instructions

### Step 1. Pass the admin access gate
- What the user does: Open the admin access page and enter the configured admin password.
- What the user sees: A focused password gate that protects the partner provisioning workspace.
- Why the step matters: This is the first gate that separates general users from partner administrators.
- Expected result: The session is authorized for partner creation.
- Common issues or trainer notes: In the local demo build, the admin quick password is derived from the local secret key.
- Screenshot placeholder section:
  - Suggested file path: `docs/product-user-flows/assets/admin-partner-provisioning-and-field-rep-upload/01-admin-access.png`
  - Screenshot caption: Admin access gate before partner setup
  - What the screenshot should show: The password prompt at `/admin/access/`.

### Step 2. Create the partner workspace
- What the user does: Open the partner creation screen after access is granted.
- What the user sees: A form with Partner Name and Field Reps CSV upload fields.
- Why the step matters: This is where the whitelabel / partner shell and field rep import are initiated.
- Expected result: The admin is ready to create the partner record.
- Common issues or trainer notes: The field rep CSV expects `rep_code` and `full_name` columns.
- Screenshot placeholder section:
  - Suggested file path: `docs/product-user-flows/assets/admin-partner-provisioning-and-field-rep-upload/02-partner-create-form.png`
  - Screenshot caption: Partner creation form with CSV upload
  - What the screenshot should show: The Create Partner & Upload Field Reps form.

### Step 3. Generate and share the doctor registration link
- What the user does: Submit the partner form with the field rep CSV.
- What the user sees: A success message showing the generated doctor registration link.
- Why the step matters: This link is the handoff artifact used by field teams and partner operators to onboard doctors.
- Expected result: The partner exists and its registration link can be shared.
- Common issues or trainer notes: Treat the link as the official onboarding URL for partner-led doctor registration.
- Screenshot placeholder section:
  - Suggested file path: `docs/product-user-flows/assets/admin-partner-provisioning-and-field-rep-upload/03-partner-created.png`
  - Screenshot caption: Partner creation success state with the generated onboarding link
  - What the screenshot should show: The success message after partner creation, including the registration link text.

## 7. Success Criteria
- The admin can reach the partner workspace.
- A partner record is created with field reps loaded from CSV.
- A working doctor registration link is produced for onward sharing.

## 8. Related Documents
- [04-partner-led-doctor-onboarding.md](04-partner-led-doctor-onboarding.md)
- [03-doctor-self-registration-and-portal-access.md](03-doctor-self-registration-and-portal-access.md)

## 9. Status
Validated against the local demo build on April 9, 2026. Documentation reflects live behavior; mismatches with older expectations are noted.
