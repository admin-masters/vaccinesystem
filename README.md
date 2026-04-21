# Vaccine System

Local test setup for this repository uses SQLite instead of the production MySQL topology.

## Quick start

```bash
./bootstrap_local.sh
```

That script will:

- create `.venv311`
- install Python dependencies
- run migrations with `vaccination_project.settings_local`
- load the bundled IAP schedule from `iap_final.csv`
- import UI translations from `phase5_ui_translations.csv`

## Run locally

```bash
source .venv311/bin/activate
DJANGO_SETTINGS_MODULE=vaccination_project.settings_local python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Notes

- The local setup uses `local_test.sqlite3`.
- All database aliases (`default`, `masters`, `patients`) point to the same SQLite file for testing.
- Google OAuth values in `.env.test` are placeholders; OAuth login will need real credentials before that flow can be tested.
- Automatic WhatsApp sending is disabled in local settings.
