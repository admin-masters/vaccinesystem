# Parent Self-Service Card, History, and Share Link

## 1. Title
Parent Self-Service Card, History, and Share Link

## 2. Document Purpose
Show how parents add or retrieve a child record, open the vaccination card, review history, use shared links, and access education content.

## 3. Primary User
Parent or guardian

## 4. Entry Point
Direct parent routes `/add/`, `/update/`, and shared link `/p/<token>/`

## 5. Workflow Summary
Parents can add a child, look up existing records by WhatsApp number, open the vaccination card, review vaccination history, verify a shared link, and open the patient education view. These flows are active in the product even though they are not promoted on the current public home page.

## 6. Step-By-Step Instructions

### Step 1. Use the public add-record route when starting fresh
- What the user does: Open the public Add Record page and review the child + parent fields.
- What the user sees: A simple add-record form for child details and the parent WhatsApp number.
- Why the step matters: This is the parent-side entry path when the family is not yet in the system.
- Expected result: The parent can create a new child record without using the doctor portal.
- Common issues or trainer notes: This route now works in the local demo build after aligning the view with the live model fields.
- Screenshot placeholder section:
  - Suggested file path: `docs/product-user-flows/assets/parent-self-service-card-history-and-share-link/01-parent-add-form.png`
  - Screenshot caption: Parent add-record form
  - What the screenshot should show: The public add form for child details and parent WhatsApp number.

### Step 2. Look up existing children by WhatsApp number
- What the user does: Open Update Record, enter the parent WhatsApp number, and proceed.
- What the user sees: A lookup form followed by the list of matching children for that number.
- Why the step matters: This is the fastest way for a returning family to re-enter the system.
- Expected result: The parent can choose the correct child record.
- Common issues or trainer notes: One parent number can return multiple children.
- Screenshot placeholder section:
  - Suggested file path: `docs/product-user-flows/assets/parent-self-service-card-history-and-share-link/03-parent-select-child.png`
  - Screenshot caption: Parent child-selection screen after WhatsApp lookup
  - What the screenshot should show: The child list returned after the parent WhatsApp lookup.

### Step 3. Open the vaccination card and history
- What the user does: Open the child vaccination card and then review the vaccination history page.
- What the user sees: The due-only vaccination card plus a separate history page with status badges and clinic call actions.
- Why the step matters: These are the parent’s main operational views for monitoring and reviewing vaccination progress.
- Expected result: The parent can see upcoming/due items and the historical record.
- Common issues or trainer notes: The history page also links into education content.
- Screenshot placeholder section:
  - Suggested file path: `docs/product-user-flows/assets/parent-self-service-card-history-and-share-link/05-parent-history.png`
  - Screenshot caption: Parent vaccination history view
  - What the screenshot should show: The parent history page after a valid child session has been established.

### Step 4. Use a doctor-issued share link
- What the user does: Open the shared link from WhatsApp, verify the WhatsApp number, and continue into the child card.
- What the user sees: A verification page followed by the child vaccination card once the number matches.
- Why the step matters: This is how clinics hand off the card to parents without asking them to search manually.
- Expected result: The parent reaches the correct child record through the tokenized link.
- Common issues or trainer notes: The shared link stores the expected last ten digits and asks the parent to confirm the number.
- Screenshot placeholder section:
  - Suggested file path: `docs/product-user-flows/assets/parent-self-service-card-history-and-share-link/06-share-link-verify.png`
  - Screenshot caption: Parent share-link verification screen
  - What the screenshot should show: The verification form asking the parent to confirm the WhatsApp number.

### Step 5. Open parent-facing vaccine education
- What the user does: Open the parent education link from the history or card workflow.
- What the user sees: A parent-facing education page with available vaccine video content.
- Why the step matters: Education supports understanding and follow-through, especially after reminders or history review.
- Expected result: The parent can move from record review into learning content without leaving the product journey.
- Common issues or trainer notes: This uses the patient education library and language preference logic where content exists.
- Screenshot placeholder section:
  - Suggested file path: `docs/product-user-flows/assets/parent-self-service-card-history-and-share-link/08-parent-vaccine-education.png`
  - Screenshot caption: Parent-facing vaccine education page
  - What the screenshot should show: The vaccine education screen reached from the parent flow.

## 7. Success Criteria
- The parent can reach the correct entry route for self-service.
- The parent can identify a child record and open the vaccination card.
- The parent can verify a share link and review history or education content.

## 8. Related Documents
- [05-doctor-portal-add-patient-and-share-link.md](05-doctor-portal-add-patient-and-share-link.md)
- [07-reminders-and-education-workflows.md](07-reminders-and-education-workflows.md)

## 9. Status
Validated against the local demo build on April 9, 2026. Documentation reflects live behavior; mismatches with older expectations are noted.
