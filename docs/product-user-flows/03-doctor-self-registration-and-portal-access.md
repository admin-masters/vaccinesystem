# Doctor Self Registration and Portal Access

## 1. Title
Doctor Self Registration and Portal Access

## 2. Document Purpose
Train a doctor or clinic lead to self-register, understand the expected WhatsApp handoff, and recognize the portal landing page they use after sign-in.

## 3. Primary User
Doctor or clinic lead registering directly

## 4. Entry Point
Doctor self-registration form at `/doctor/register/`

## 5. Workflow Summary
Doctors can self-register through a public registration form. After submission, the current product opens WhatsApp with a prefilled portal message, and the doctor then uses the portal link to reach the clinic workspace.

## 6. Step-By-Step Instructions

### Step 1. Open the doctor registration form
- What the user does: Browse to the self-registration page.
- What the user sees: A detailed doctor registration form covering identity, clinic details, languages, contact numbers, and IMC number.
- Why the step matters: This is the doctor’s main onboarding form when no partner-issued link is involved.
- Expected result: The doctor can review the data required to register.
- Common issues or trainer notes: The form enforces Gmail-format email addresses in the current build.
- Screenshot placeholder section:
  - Suggested file path: `docs/product-user-flows/assets/doctor-self-registration-and-portal-access/01-doctor-self-registration-form.png`
  - Screenshot caption: Doctor self-registration form
  - What the screenshot should show: The full doctor registration form with the mandatory fields visible.

### Step 2. Submit and hand off to WhatsApp
- What the user does: Complete the form and click Register.
- What the user sees: The browser is redirected to WhatsApp with a prefilled message containing the doctor portal link.
- Why the step matters: This is how the product currently distributes the personalized portal URL.
- Expected result: The doctor receives a reusable portal link message.
- Common issues or trainer notes: The current implementation opens WhatsApp rather than using a server-side messaging gateway.
- Screenshot placeholder section:
  - Suggested file path: `docs/product-user-flows/assets/doctor-self-registration-and-portal-access/01-doctor-self-registration-form.png`
  - Screenshot caption: Registration form immediately before submission
  - What the screenshot should show: The completed form or the register action, since the next state is an external WhatsApp redirect.

### Step 3. Recognize the clinic portal home
- What the user does: Open the doctor portal link and sign in.
- What the user sees: A doctor portal home page with actions for Add-a-patient, Update a patient record, Reminders, and Edit doctor/clinic profile.
- Why the step matters: This is the control center the doctor returns to for daily clinic use.
- Expected result: The doctor can navigate to the main clinic workflows from one landing page.
- Common issues or trainer notes: The documentation screenshots use a local demo session to bypass unavailable Google OAuth credentials.
- Screenshot placeholder section:
  - Suggested file path: `docs/product-user-flows/assets/doctor-self-registration-and-portal-access/02-doctor-self-portal-home.png`
  - Screenshot caption: Doctor portal home after successful access
  - What the screenshot should show: The doctor portal home with the primary action buttons visible.

## 7. Success Criteria
- The doctor can complete the registration form.
- The doctor understands that submission hands off to WhatsApp with the portal link.
- The doctor recognizes the portal home once authenticated.

## 8. Related Documents
- [05-doctor-portal-add-patient-and-share-link.md](05-doctor-portal-add-patient-and-share-link.md)
- [06-doctor-portal-update-card-and-profile.md](06-doctor-portal-update-card-and-profile.md)

## 9. Status
Validated against the local demo build on April 9, 2026. Documentation reflects live behavior; mismatches with older expectations are noted.
