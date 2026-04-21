# Partner-Led Doctor Onboarding

## 1. Title
Partner-Led Doctor Onboarding

## 2. Document Purpose
Show how a partner-issued registration link adds field rep attribution to the doctor onboarding process and leads into the same portal experience.

## 3. Primary User
Field team member, partner coordinator, or doctor onboarding via partner link

## 4. Entry Point
Partner registration URL at `/doctor/register/<token>/`

## 5. Workflow Summary
Partner-led onboarding uses a tokenized doctor registration link. The form is similar to self-registration but adds field rep code and field rep name to attribute the onboarding to the partner team.

## 6. Step-By-Step Instructions

### Step 1. Open the partner-issued registration link
- What the user does: Open the doctor registration URL received from the partner/admin team.
- What the user sees: The doctor registration form with additional Field Rep Code and Field Rep Name inputs.
- Why the step matters: This route distinguishes partner-led onboarding from self-registration.
- Expected result: The doctor is in the correct registration context for partner attribution.
- Common issues or trainer notes: If the token is invalid or expired, the product redirects back to the home page with an error.
- Screenshot placeholder section:
  - Suggested file path: `docs/product-user-flows/assets/partner-led-doctor-onboarding/01-partner-led-registration-form.png`
  - Screenshot caption: Partner-led doctor registration form with field rep fields
  - What the screenshot should show: The registration form including Field Rep Code and Field Rep Name.

### Step 2. Complete registration with field rep details
- What the user does: Enter doctor details plus the partner field rep code/name and submit the form.
- What the user sees: The same WhatsApp redirect behavior used for self-registration, now tied to the partner and field rep.
- Why the step matters: This preserves partner attribution while still delivering the portal link to the doctor.
- Expected result: The doctor is stored with the linked partner and field rep association.
- Common issues or trainer notes: The live validation checks the field rep code against the selected partner.
- Screenshot placeholder section:
  - Suggested file path: `docs/product-user-flows/assets/partner-led-doctor-onboarding/01-partner-led-registration-form.png`
  - Screenshot caption: Partner-led registration form before submission
  - What the screenshot should show: The partner registration page prior to the WhatsApp redirect.

### Step 3. Confirm the partner doctor portal landing
- What the user does: Open the personalized portal link after sign-in.
- What the user sees: The same doctor portal home used in self-registration-based onboarding.
- Why the step matters: This confirms that partner-led onboarding still leads into the shared clinic operating workflow.
- Expected result: The partner-onboarded doctor can continue with routine clinic tasks.
- Common issues or trainer notes: The downstream portal experience is shared; the main difference is the onboarding attribution.
- Screenshot placeholder section:
  - Suggested file path: `docs/product-user-flows/assets/partner-led-doctor-onboarding/02-partner-doctor-portal-home.png`
  - Screenshot caption: Partner-onboarded doctor landing in the clinic portal
  - What the screenshot should show: The partner doctor’s portal home after access.

## 7. Success Criteria
- The doctor can open the partner-specific registration form.
- The form captures the required field rep information.
- The doctor reaches the same portal destination after the WhatsApp handoff.

## 8. Related Documents
- [02-admin-partner-provisioning-and-field-rep-upload.md](02-admin-partner-provisioning-and-field-rep-upload.md)
- [03-doctor-self-registration-and-portal-access.md](03-doctor-self-registration-and-portal-access.md)

## 9. Status
Validated against the local demo build on April 9, 2026. Documentation reflects live behavior; mismatches with older expectations are noted.
