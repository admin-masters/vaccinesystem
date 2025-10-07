# Vaccination System - Database Structure

## Core Tables

### 1. schedule_version
IAP vaccination schedule versions
- `id` (PK)
- `code` (unique) - e.g., "IAP-2025"
- `name` - e.g., "IAP Schedule 2025"
- `source_url`
- `effective_from` (date)
- `is_current` (boolean)
- `created_at`

### 2. vaccine
Individual vaccines in the schedule
- `id` (PK)
- `schedule_version_id` (FK → schedule_version)
- `code` (slug) - e.g., "bcg", "dtwp-dtap"
- `name` - e.g., "BCG", "DTwP / DTaP"
- `aliases`
- `is_active` (boolean)
- `notes`
- `education_parent_url`
- `education_doctor_vimeo_url`
- `created_at`

### 3. vaccine_dose
Individual doses of each vaccine (e.g., DTwP1, DTwP2, DTwP3)
- `id` (PK)
- `schedule_version_id` (FK → schedule_version)
- `vaccine_id` (FK → vaccine)
- `sequence_index` - Order within vaccine series
- `dose_label` - e.g., "DTwP/DTaP1", "BCG"
- `min_offset_days` - Minimum days from birth (IAP schedule)
- `max_offset_days` - Maximum days from birth (can be NULL)
- `previous_dose_id` (FK → vaccine_dose, nullable) - Previous dose dependency
- `anchor_policy` - "L" (Later), "I" (Interval), "A" (Absolute)
- `series_key` - Groups doses in same series (e.g., "dtwp-dtap")
- `series_seq` - Sequence within series (1, 2, 3...)
- `created_at`

## Clinic & Doctor Tables

### 4. partner
Partner organizations (for field representatives)
- `id` (PK)
- `name`
- `slug` (unique)
- `registration_token` (unique)
- `created_at`

### 5. field_representative
Field representatives working for partners
- `id` (PK)
- `partner_id` (FK → partner)
- `rep_code` (unique)
- `full_name`
- `phone`
- `is_active` (boolean)
- `created_at`

### 6. clinic
Medical clinics
- `id` (PK)
- `partner_id` (FK → partner, nullable)
- `field_rep_id` (FK → field_representative, nullable)
- `name`
- `address`
- `state`
- `pincode`
- `phone`
- `whatsapp_e164`
- `created_at`

### 7. doctor
Doctors working at clinics
- `id` (PK)
- `clinic_id` (FK → clinic)
- `partner_id` (FK → partner, nullable)
- `field_rep_id` (FK → field_representative, nullable)
- `full_name`
- `email`
- `phone`
- `imc_number` - Indian Medical Council registration
- `portal_token` (unique) - For doctor portal access
- `created_at`

## Patient Tables

### 8. parent
Parents/guardians
- `id` (PK)
- `full_name`
- `whatsapp_e164` (unique) - WhatsApp number in E.164 format
- `clinic_id` (FK → clinic, nullable)
- `created_at`

### 9. child
Children receiving vaccinations
- `id` (PK)
- `parent_id` (FK → parent)
- `clinic_id` (FK → clinic, nullable)
- `full_name`
- `sex` - "M" or "F"
- `date_of_birth` (date)
- `state` - Indian state code
- `created_at`
- `updated_at`

### 10. child_dose
Individual vaccination records for each child
- `id` (PK)
- `child_id` (FK → child)
- `dose_id` (FK → vaccine_dose)
- `given_date` (date, nullable) - When vaccine was actually given
- `due_date` (date, nullable) - When vaccine is due (calculated)
- `due_until_date` (date, nullable) - Last date for on-time vaccination
- `created_at`
- `updated_at`
- **Unique constraint:** (child_id, dose_id)

### 11. child_share_link
Shareable links for parents to access child's vaccination card
- `id` (PK)
- `child_id` (FK → child)
- `token` (unique) - Random token for URL
- `last_10_digits` - Last 10 digits of parent's WhatsApp for verification
- `created_by_doctor_id` (FK → doctor, nullable)
- `expires_at` (datetime)
- `is_active` (boolean)
- `created_at`

## Education & Localization Tables

### 12. vaccine_education_patient
Patient/parent education videos for vaccines
- `id` (PK)
- `vaccine_id` (FK → vaccine)
- `language` - ISO 639-1 code (en, hi, mr, bn, etc.)
- `title`
- `video_url`
- `platform` - "youtube", "vimeo", "other"
- `thumbnail_url`
- `duration_seconds`
- `rank` - Display order (lower = show first)
- `is_active` (boolean)
- `created_at`
- `updated_at`
- **Unique constraint:** (vaccine_id, language, video_url)

### 13. vaccine_education_doctor
Doctor education videos for vaccines
- `id` (PK)
- `vaccine_id` (FK → vaccine)
- `language`
- `title`
- `video_url`
- `platform`
- `thumbnail_url`
- `duration_seconds`
- `rank`
- `is_active` (boolean)
- `created_at`
- `updated_at`

### 14. ui_string
UI text keys for localization
- `id` (PK)
- `key` (unique) - e.g., "history.title", "btn.update_due"
- `description`

### 15. ui_string_translation
Translations for UI strings
- `id` (PK)
- `ui_id` (FK → ui_string)
- `language` - ISO 639-1 code
- `text` - Translated text
- **Unique constraint:** (ui_id, language)

## Key Relationships

```
schedule_version (1) ──→ (N) vaccine
schedule_version (1) ──→ (N) vaccine_dose

vaccine (1) ──→ (N) vaccine_dose
vaccine (1) ──→ (N) vaccine_education_patient
vaccine (1) ──→ (N) vaccine_education_doctor

vaccine_dose (1) ──→ (1) vaccine_dose [self-reference: previous_dose]
vaccine_dose (1) ──→ (N) child_dose

partner (1) ──→ (N) field_representative
partner (1) ──→ (N) clinic
partner (1) ──→ (N) doctor

clinic (1) ──→ (N) doctor
clinic (1) ──→ (N) parent
clinic (1) ──→ (N) child

parent (1) ──→ (N) child
child (1) ──→ (N) child_dose
child (1) ──→ (N) child_share_link

doctor (1) ──→ (N) child_share_link [created_by]

ui_string (1) ──→ (N) ui_string_translation
```

## Important Business Logic

### Vaccination Schedule Flow
1. **ScheduleVersion** defines IAP schedule (e.g., IAP-2025)
2. **Vaccine** lists all vaccines (BCG, DTwP, etc.)
3. **VaccineDose** defines each dose with timing (e.g., DTwP1 at 6 weeks)
4. When **Child** is created, **ChildDose** records are auto-created for all doses
5. **due_date** is calculated from DOB using `min_offset_days`
6. When parent marks dose as given, dependent doses are reanchored

### Date Calculation
- **Primary doses** (no previous_dose): `due_date = DOB + min_offset_days`
- **Booster doses** (has previous_dose): Wait for previous dose to be given, then calculate
- **Reanchoring**: When previous dose given late/early, next dose shifts accordingly

### Access Control
- **Parents**: Access via WhatsApp verification or share links
- **Doctors**: Access via portal_token (unique per doctor)
- **Field Reps**: Can register doctors for their partner organization
