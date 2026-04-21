# Project Handover

This document is meant to give a new thread enough context to continue work on this repository without re-discovering the project structure from scratch.

## 1. Snapshot

- Project: pediatric vaccination card and reminder system for clinics, doctors, and parents.
- Framework: Django 5.x with one main app, `vaccinations`.
- Current primary local repo: `/Users/inditech-tech/Documents/Vaccine/vaccinesystem-codex`
- Git remote: `https://github.com/gopalakrishnanplus-creator/vaccinesystem-codex.git`
- Current branch: `main`
- Current HEAD when this handover was written: `42efab3d6c4929f14fff2a12d57296f37046c0c9`
- Upstream README is not useful by itself. The real working context is in code, templates, SQL dumps, CSV/XLSX assets, and local bootstrap files added in this repo.

## 2. What This Product Is Supposed To Do

The intended product, based on the working brief in the thread, is a whitelabelled vaccination system for pediatric clinics with these main actors:

- Parent:
  - can add a child
  - can update the child’s vaccination record
  - can view a due-only vaccination card
  - can update given dates and then view vaccination history
  - can access multilingual patient education content
- Doctor / clinic staff:
  - can self-register or be registered via partner / field rep
  - receives a doctor portal link over WhatsApp
  - must log in via Google/Gmail before using the portal
  - can add patients
  - can optionally send a patient share link through WhatsApp at patient creation time
  - can update patient vaccination records
  - can edit doctor / clinic profile
  - can review reminder dashboards and send reminder messages
- Field partner / admin:
  - can create partners
  - can upload field rep CSVs
  - can generate partner registration links for doctors

## 3. What Is Actually Implemented Today

The codebase contains a substantial portion of that product, but not every part matches the desired product exactly.

Implemented or partly implemented:

- Doctor self-registration form
- Doctor partner-led registration form
- Partner creation + field rep CSV upload
- Doctor portal
- Add patient / update patient flows inside doctor portal
- Parent share-link verification by WhatsApp number
- Parent vaccination card pages
- Parent vaccination history page
- Patient and doctor vaccine education pages
- Reminder dashboards and send-reminder action
- Multi-language UI translation lookup for parent history page and related text
- Local test bootstrap with SQLite

Known mismatches between intended product and current implementation:

- The current public home page is doctor/admin oriented. It does not presently act as the parent landing page described in the brief.
- Parent add/update flows exist at direct routes like `/add/` and `/update/`, but the home page does not prominently expose them.
- WhatsApp gateway integration is not fully implemented. The app mostly opens WhatsApp or WhatsApp Web with prefilled messages rather than calling a business gateway.
- `send_doctor_portal_link()` in `vaccinations/services.py` is a placeholder that logs and returns `True`.
- Gmail login exists, but there are two parallel OAuth implementations in the codebase. The routed one is function-based in `vaccinations/views_auth.py`.
- Several models and views still mix encrypted-field accessors and legacy plain-field references.
- The due-date / booster logic is partly data-driven and partly custom fallback logic. It is functional enough for local testing but needs careful review against the full IAP rules.

## 4. Repo And Environment Inventory

### Remote repo

- `origin`: `https://github.com/gopalakrishnanplus-creator/vaccinesystem-codex.git`

### Local repo

- Main working copy: `/Users/inditech-tech/Documents/Vaccine/vaccinesystem-codex`

### Key top-level files

- `manage.py`
- `vaccination_project/settings.py`
- `vaccination_project/settings_local.py`
- `vaccinations/views.py`
- `vaccinations/views_auth.py`
- `vaccinations/models.py`
- `vaccinations/services.py`
- `vaccinations/signals.py`
- `vaccinations/forms.py`
- `vaccinations/urls.py`
- `iap_final.csv`
- `phase5_ui_translations.csv`
- `education.xlsx`
- `Vaccine_master.sql`
- `vaccine_clinic(db).sql`
- `deploy.sh`
- `.github/workflows/deploy.yml`
- `bootstrap_local.sh`
- `.env.test`

### Local working tree status

This repo currently has uncommitted local setup changes. At the time of writing, `git status --short` shows:

- modified:
  - `README.md`
  - `requirements.txt`
  - `vaccinations/migrations/0016_remove_child_child_parent__16983e_idx_and_more.py`
  - `vaccinations/migrations/0017_rename_eligible_sex_vaccinedose_eligible_gender_and_more.py`
  - `vaccinations/migrations/0018_remove_child_child_clinic__5e8bbe_idx_and_more.py`
  - `vaccinations/migrations/0019_add_encrypted_columns.py`
  - `vaccinations/migrations/0020_patient_encrypted_columns.py`
  - `vaccinations/migrations/0027_auto.py`
  - `vaccinations/migrations/0028_rename_vaccinations_child_id_idx_child_share_child_i_a28a1d_idx_and_more.py`
- untracked:
  - `.env.test`
  - `.venv/`
  - `.venv311/`
  - `bootstrap_local.sh`
  - `local_test.sqlite3`
  - `vaccination_project/settings_local.py`
  - this handover file

Important implication:

- The repo is not a clean checkout anymore.
- The local environment and SQLite compatibility work live in the working tree and are not necessarily present upstream.

## 5. Environments

### Production / server environment

Production details inferred from `deploy.sh`, `.github/workflows/deploy.yml`, and `vaccination_project/settings.py`:

- deployment target looks like an EC2 machine
- deploy path: `/var/www/vaccinesystem`
- production virtualenv: `/var/www/venv`
- env file: `/var/www/secrets/.env`
- deploy trigger: push to `main`
- deployment mechanism: GitHub Actions SSH into EC2 and run `./deploy.sh`
- service restarted at deploy: `gunicorn-vaccine`
- known host in Django settings: `newvaccine.cpdinclinic.co.in`

### Production database layout

The app is intended to run with three database aliases:

- `default`
- `masters`
- `patients`

Configured in `vaccination_project/settings.py`:

- `default` is MySQL, now driven by environment variables:
  - `CLINIC_DB_NAME`
  - `CLINIC_DB_USER`
  - `CLINIC_DB_PASSWORD`
  - `CLINIC_DB_HOST`
  - optional `CLINIC_DB_PORT` (defaults to `3306`)
- `masters` is MySQL, values from environment
- `patients` is MySQL, values from environment

Routing is handled by `vaccinations/routers.py`:

- masters-side models:
  - `ScheduleVersion`, `Vaccine`, `VaccineDose`
  - `Partner`, `FieldRepresentative`, `Clinic`, `Doctor`
  - `VaccineEducationPatient`, `VaccineEducationDoctor`
  - `UiString`, `UiStringTranslation`, `OauthState`
- patients-side models:
  - `Parent`, `Child`, `ChildDose`, `ChildShareLink`

### Local test environment

The repo now includes a runnable local test setup:

- local settings module: `vaccination_project.settings_local`
- local env file: `.env.test`
- local bootstrap script: `bootstrap_local.sh`
- local test database: `local_test.sqlite3`
- preferred local venv: `.venv311`

Local design decisions:

- local uses SQLite instead of MySQL
- all three DB aliases (`default`, `masters`, `patients`) point to the same SQLite DB
- database routers are disabled locally
- Google OAuth uses placeholder credentials in `.env.test`
- automatic send-to-parent is disabled locally

Local bootstrap command:

```bash
./bootstrap_local.sh
```

Manual local run:

```bash
source .venv311/bin/activate
DJANGO_SETTINGS_MODULE=vaccination_project.settings_local python manage.py runserver
```

Local verification already done in this repo:

- `DJANGO_SETTINGS_MODULE=vaccination_project.settings_local .venv311/bin/python manage.py check`
- result: `System check identified no issues (0 silenced).`

Current local seeded data in `local_test.sqlite3`:

- `schedule_version`: 1
- `vaccine`: 38
- `vaccine_dose`: 43
- `ui_string_translation`: 144

## 6. Required Secrets / Configuration

### Used directly by production settings or crypto code

- `PATIENT_DATA_FERNET_KEY`
- `CLINIC_DB_NAME`
- `CLINIC_DB_USER`
- `CLINIC_DB_PASSWORD`
- `CLINIC_DB_HOST`
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_OAUTH_REDIRECT_URI`
- `MASTERS_DB_NAME`
- `MASTERS_DB_USER`
- `MASTERS_DB_PASSWORD`
- `MASTERS_DB_HOST`
- `PATIENTS_DB_NAME`
- `PATIENTS_DB_USER`
- `PATIENTS_DB_PASSWORD`
- `PATIENTS_DB_HOST`
- `PHONE_HASH_SALT`
- `DATA_KEY_ACTIVE`
- `DATA_KEY_1`
- `SEARCH_PEPPER`

### Notes

- `vaccination_project/settings.py` loads env values from `.env`, `.env.production`, and `/var/www/secrets/.env` when those files exist.
- `vaccinations/crypto.py` imports `DATA_KEY_1` and `SEARCH_PEPPER` at import time, so startup fails if they are missing.
- There is also code in `vaccinations/views.py` referencing OAuth keys like `AUTH_URL`, `TOKEN_URL`, `USERINFO_URL`, and `REDIRECT_URI`, but the routed function-based OAuth flow in `vaccinations/views_auth.py` does not depend on those exact keys.
- There are effectively two OAuth implementations in the codebase. This should be consolidated later.

## 7. Architecture

### High-level shape

- Django project: `vaccination_project`
- Main app: `vaccinations`
- One very large view module: `vaccinations/views.py` at roughly 2,075 lines
- One separate auth view module: `vaccinations/views_auth.py`
- Templates: `vaccinations/templates/vaccinations/`
- Static assets: `vaccinations/static/vaccinations/`
- Management commands: `vaccinations/management/commands/`
- SQL dumps and import assets live at the repo root

### Major app modules

- `vaccinations/models.py`
  - all domain models
- `vaccinations/views.py`
  - parent flows
  - doctor flows
  - reminders
  - education pages
  - some duplicate / legacy OAuth logic
- `vaccinations/views_auth.py`
  - currently routed Google OAuth start/callback functions
- `vaccinations/forms.py`
  - parent add/lookup forms
  - doctor registration/profile forms
- `vaccinations/services.py`
  - current schedule lookup
  - dose reanchoring
  - education fetch helpers
  - placeholder doctor link send function
- `vaccinations/signals.py`
  - auto-create `ChildDose` rows when a `Child` is created
  - reanchor dependent doses when a dose gets a `given_date`
- `vaccinations/utils.py`
  - phone normalization/hash helpers
  - state-language mapping
  - WhatsApp message helpers
  - date window helpers and status helpers
- `vaccinations/utils_i18n.py`
  - multilingual UI string lookup
- `vaccinations/utils_schedule.py`
  - schedule display helpers and series mapping

## 8. Core Data Model

### Masters-side models

- `Clinic`
  - doctor / clinic profile and language settings
- `Partner`
  - whitelabel / partner entity
- `FieldRepresentative`
  - partner field reps
- `Doctor`
  - doctor identity, portal token, partner association, Google subject
- `ScheduleVersion`
  - vaccine schedule version
- `Vaccine`
  - vaccine master row
- `VaccineDose`
  - each scheduled dose / booster row, with offsets and dependency metadata
- `VaccineEducationPatient`
  - patient-facing education videos
- `VaccineEducationDoctor`
  - doctor-facing education videos
- `UiString`, `UiStringTranslation`
  - multilingual UI copy
- `OAuthState`
  - temporary OAuth state storage

### Patients-side models

- `Parent`
  - encrypted WhatsApp number
  - hash of last 10 digits for lookup
- `Child`
  - encrypted child demographics, legacy plain fields still present
- `ChildDose`
  - one row per child x vaccine dose
  - stores `given_date`, `due_date`, `due_until_date`
  - reminder tracking fields also live here
- `ChildShareLink`
  - tokenized link for parent access
  - stores expected last 10 digits for verification

### Important model reality

The codebase is in the middle of a transition:

- there are legacy plain fields
- there are encrypted fields
- some code uses accessors like `get_child_name()`
- some code still references direct fields like `full_name`, `child_name`, `gender`, `sex`

This is one of the main sources of fragility in the repo.

## 9. Schedule And Due-Date Logic

### Data source

- `iap_final.csv` is the current main import source for the local bootstrap.
- row count: 43
- boosters flagged as `Yes`: 29

### Seed / load behavior

`vaccinations/management/commands/load_final_iap_schedule.py`:

- clears existing vaccine data in `default`
- loads one schedule version
- creates vaccines and doses from `iap_final.csv`
- parses offsets as:
  - weeks = `7` days
  - months = `30` days
  - years = `365` days
- currently creates a generic `30-day` window by setting `max_offset_days = min_offset_days + 30`
- links `previous_dose` using the CSV’s `Previous Vaccine` field where possible

### Runtime due-date mechanics

- `signals.py` creates `ChildDose` rows automatically when a child is created.
- first-pass due dates are seeded from birth-date offsets.
- `services.reanchor_dependents()` recalculates dependent doses once a previous dose is marked given.
- there is special-case logic for influenza / annual influenza.

### Important caveat

The current implementation is not a clean, single-source-of-truth IAP engine. It is a mixture of:

- imported schedule offsets
- series helpers
- signal-driven seeding
- recursive reanchoring logic
- fallback interval logic

This area should be treated as high risk when making product changes.

## 10. Implemented User Flows

### Public / parent-side routes

- `/add/`
  - add child under a parent WhatsApp number
- `/update/`
  - look up children by parent WhatsApp number
- `/card/<child_id>/`
  - due-only card
- `/card-all/<child_id>/`
  - full schedule card
- `/p/<token>/`
  - parent share-link verification flow
- `/history/<child_id>/`
  - vaccination history page
- `/edu/vaccine/<vaccine_id>/`
  - parent education page
- `/edu/patient/<vaccine_id>/`
  - simplified education page used by reminder links

### Parent flow as currently coded

1. Parent can be looked up by WhatsApp number.
2. Matching parents are resolved by last 10 digits hash.
3. Parent sees child list.
4. Parent opens due-only or full card.
5. Parent enters given dates for due vaccines.
6. Changed doses trigger dependent reanchoring.
7. On successful update, parent is redirected to vaccination history.
8. Parent can open education links and clinic call links from history.

### Doctor registration and portal routes

- `/doctor/register/`
  - doctor self registration
- `/doctor/register/<token>/`
  - partner-led doctor registration
- `/d/<token>/`
  - doctor portal home
- `/d/<token>/add/`
  - add patient
- `/d/<token>/update/`
  - update patient lookup
- `/d/<token>/card/<child_id>/`
  - due-only patient card in doctor portal
- `/d/<token>/card-all/<child_id>/`
  - full card in doctor portal
- `/d/<token>/profile/`
  - edit doctor / clinic profile
- `/d/<token>/reminders/`
  - clinic-wide reminders dashboard
- `/d/<token>/child/<child_id>/reminders/`
  - child-level reminder schedule
- `/d/<token>/send-reminder/<child_dose_id>/`
  - open WhatsApp reminder message
- `/d/<token>/vaccine/<vaccine_id>/`
  - doctor education page

### Doctor flow as currently coded

1. Doctor registers directly or through a partner token.
2. Registration redirects to WhatsApp with a portal link.
3. Doctor opens portal link.
4. Routed OAuth flow is in `views_auth.py`; portal access relies on session key `doctor_auth`.
5. Doctor can add a patient.
6. Inside doctor add flow, there is an extra button:
   - `Register & Send to Patient`
7. That issues a `ChildShareLink`, builds a bilingual message, and opens WhatsApp Web.
8. Doctor can update patient records scoped to their clinic.
9. Doctor can view reminder dashboards and send reminder messages.
10. Doctor can edit clinic and profile fields.

### Admin / partner flow

- `/partners/new/`
  - create partner and upload field rep CSV
- `/admin/access/`
  - lightweight admin gate if session not already staff-authenticated

## 11. Messaging, Languages, And Education

### State-language mapping

Defined in `vaccinations/utils.py` as `STATE_LANG`.

Implemented template message languages in the code:

- `en`
- `hi`
- `mr`
- `kn`
- `ml`
- `te`
- `ta`

Translation CSV currently loaded for:

- `bn`
- `en`
- `hi`
- `kn`
- `ml`
- `mr`
- `ta`
- `te`

UI translations file:

- `phase5_ui_translations.csv`
- 144 translation rows

Education workbook:

- `education.xlsx`
- sheets:
  - `PE` with 321 rows
  - `DE` with 41 rows

Import commands:

- `python manage.py import_ui_translations phase5_ui_translations.csv`
- `python manage.py import_education education.xlsx`

## 12. Templates And UX Surfaces Worth Knowing

Key templates:

- `vaccinations/templates/vaccinations/home.html`
- `vaccinations/templates/vaccinations/add_record.html`
- `vaccinations/templates/vaccinations/card.html`
- `vaccinations/templates/vaccinations/parent_history.html`
- `vaccinations/templates/vaccinations/parent_share_verify.html`
- `vaccinations/templates/vaccinations/doctor_portal_home.html`
- `vaccinations/templates/vaccinations/doctor_register.html`
- `vaccinations/templates/vaccinations/doctor_update_lookup.html`
- `vaccinations/templates/vaccinations/doctor_select_child.html`
- `vaccinations/templates/vaccinations/doctor_reminders.html`

Important UX reality:

- `base.html` always links header navigation back to the global home page.
- Current home page offers `Doctor Registration` and `Field Partner (Admin)`.
- That does not match the parent-first homepage described in the product brief.

## 13. Known Technical Risks And Gaps

This section is important. A new thread should treat these as active context, not background noise.

### High-risk / architectural issues

- There are duplicate migration branches for encryption and `ChildShareLink`; local SQLite setup required making some of those migrations effectively no-ops.
- Some original migrations were MySQL-specific and had to be patched locally for SQLite compatibility.
- The repo is strongly coupled to multi-database usage via `.using("default"|"masters"|"patients")`.
- Cross-database relations are handled manually in many places by separately loading related objects.

### Model / field inconsistency issues

- Code mixes encrypted getters with legacy plain fields.
- Examples:
  - `get_child_name()` exists, but some code still uses `full_name` or `child_name`.
  - encrypted gender accessors exist, but some code still uses `sex`, `gender`, or Django display helpers inconsistently.

### OAuth / auth issues

- Two OAuth implementations exist:
  - function-based in `vaccinations/views_auth.py`
  - class-based / partially duplicated in `vaccinations/views.py`
- Session-based gate in active doctor portal views uses `_require_doctor_auth()`.
- There is also a cookie-based `DoctorAuthRequiredMixin` path that is not the active route path.
- These should eventually be unified.

### Reminder / messaging issues

- Reminder status logic is spread between helpers and views.
- Template text says "Overdue Today remains visible for 3 days", but clinic-wide reminder query currently includes all overdue vaccines, not just recent ones.
- `send_doctor_portal_link()` is a stub, not a real delivery integration.

### Data / import issues

- `requirements.txt` was effectively empty upstream; local development needed it to be filled manually.
- `load_final_iap_schedule.py` links some `Previous Vaccine` labels successfully, but not all human-readable labels resolve cleanly.
- Due windows are simplified with a generic 30-day window in the loader.

### Test coverage reality

- There is no standard Django test suite or pytest suite currently wired.
- There are many root-level `test_*.py` files, but most are empty or ad hoc scripts.
- `rg` found no `TestCase` / `pytest` based test suite in normal structure.

### Logging / debug residue

- Several views and helper scripts still contain `print(...)` debugging.
- Not fatal, but a sign that some code paths are still under active manual debugging rather than stabilized.

## 14. Local Bootstrap Work Added In This Repo

The following local-only setup was added to make this repo runnable here:

- `vaccination_project/settings_local.py`
- `.env.test`
- `bootstrap_local.sh`
- `README.md` updated with local quickstart
- `requirements.txt` populated
- migration patches for SQLite compatibility

What these local changes do:

- use Python 3.11 in `.venv311`
- use SQLite file `local_test.sqlite3`
- seed schedule + translations
- avoid production secrets and production MySQL dependencies

This is very useful for local iteration, but it is not the same as production architecture.

## 15. Suggested Starting Points For Future Threads

If the next thread is product-documentation focused:

- start from this handover file
- then read:
  - `vaccinations/urls.py`
  - `vaccinations/views.py`
  - `vaccinations/views_auth.py`
  - `vaccinations/models.py`
  - `vaccinations/forms.py`
  - `vaccinations/services.py`
  - `vaccinations/signals.py`

If the next thread is product-gap / implementation focused:

- first decide whether to optimize for:
  - product spec fidelity
  - production stability
  - local dev ergonomics
- the codebase currently cannot maximize all three at once without refactoring

If the next thread is environment / deployment focused:

- review:
  - `vaccination_project/settings.py`
  - `deploy.sh`
  - `.github/workflows/deploy.yml`
  - local SQLite bootstrap files
- then decide whether local SQLite support should remain an explicit development mode in version control

## 16. Useful Commands

Local bootstrap:

```bash
./bootstrap_local.sh
```

Run locally:

```bash
source .venv311/bin/activate
DJANGO_SETTINGS_MODULE=vaccination_project.settings_local python manage.py runserver
```

Sanity check:

```bash
DJANGO_SETTINGS_MODULE=vaccination_project.settings_local .venv311/bin/python manage.py check
```

Seed schedule:

```bash
DJANGO_SETTINGS_MODULE=vaccination_project.settings_local .venv311/bin/python manage.py load_final_iap_schedule --csv-file iap_final.csv
```

Seed translations:

```bash
DJANGO_SETTINGS_MODULE=vaccination_project.settings_local .venv311/bin/python manage.py import_ui_translations phase5_ui_translations.csv
```

Import education:

```bash
DJANGO_SETTINGS_MODULE=vaccination_project.settings_local .venv311/bin/python manage.py import_education education.xlsx
```

## 17. Suggested Prompt For A New Thread

If starting a fresh thread, a good kickoff prompt would be:

```text
Please use /Users/inditech-tech/Documents/Vaccine/vaccinesystem-codex/docs/PROJECT_HANDOVER.md as the primary project context file before doing anything else. Work only in the original repo at /Users/inditech-tech/Documents/Vaccine/vaccinesystem-codex. Review the current working tree, preserve existing local bootstrap changes unless they conflict with the task, and call out any mismatch between the product brief and the current implementation before making major changes.
```
