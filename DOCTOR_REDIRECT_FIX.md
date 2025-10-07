# Doctor Card Update Redirect Fix

## Problem
When doctors update vaccination cards, they were being redirected to the vaccination history page instead of staying on the card page.

## Root Cause
The issue was in the shared `card.html` template. The navigation links were hardcoded to parent URLs:
- `{% url 'vaccinations:card' child.id %}` (parent URL)
- `{% url 'vaccinations:card-all' child.id %}` (parent URL)

When doctors clicked these links, they were redirected to parent views, and form submissions went to parent POST handlers, which redirect to history page after updates.

## Solution
1. **Updated `card.html` template** to be context-aware:
   - Added conditional logic to use doctor URLs when `doctor` context is present
   - Uses `{% url 'vaccinations:doc-card' doctor.portal_token child.id %}` for doctors
   - Uses `{% url 'vaccinations:card' child.id %}` for parents

2. **Updated doctor views** to pass `doctor` context:
   - `DoctorPortalCardDueView.get()` now passes `"doctor": self.doctor`
   - `DoctorPortalCardAllView.get()` now passes `"doctor": self.doctor`

## Result
- **Doctors**: Update card → Stay on doctor card page ✅
- **Parents**: Update card → Redirect to history page ✅ (unchanged)

## Files Modified
1. `vaccinations/templates/vaccinations/card.html` - Added conditional URLs
2. `vaccinations/views.py` - Added doctor context to template

## Testing
Doctors should now:
1. Access card via `/d/{token}/card/{child_id}/`
2. Update vaccination dates
3. Stay on the same doctor card page (not redirect to history)
