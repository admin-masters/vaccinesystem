#!/bin/zsh
set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-/opt/homebrew/bin/python3.11}"
VENV_DIR="${VENV_DIR:-.venv311}"

if [ ! -x "$PYTHON_BIN" ]; then
  echo "Python 3.11 is required. Set PYTHON_BIN to a Python 3.11 executable."
  exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

export DJANGO_SETTINGS_MODULE=vaccination_project.settings_local

"$VENV_DIR/bin/pip" install -r requirements.txt

"$VENV_DIR/bin/python" manage.py migrate
"$VENV_DIR/bin/python" manage.py load_final_iap_schedule --csv-file iap_final.csv
"$VENV_DIR/bin/python" manage.py import_ui_translations phase5_ui_translations.csv

cat <<'EOF'

Local test environment is ready.

Activate:
  source .venv311/bin/activate

Run server:
  DJANGO_SETTINGS_MODULE=vaccination_project.settings_local python manage.py runserver
EOF
