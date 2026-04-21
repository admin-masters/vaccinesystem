#!/bin/zsh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="$ROOT_DIR/.venv311/bin/python"
PIP_BIN="$ROOT_DIR/.venv311/bin/pip"
SETTINGS="vaccination_project.settings_local"
PORT="${DOCS_PORT:-8010}"
BASE_URL="http://127.0.0.1:${PORT}"
LOG_DIR="$ROOT_DIR/tmp/docs/logs"
mkdir -p "$LOG_DIR"

if [ ! -x "$PYTHON_BIN" ]; then
  echo "Missing .venv311. Run ./bootstrap_local.sh first."
  exit 1
fi

"$PIP_BIN" install -r "$ROOT_DIR/tmp/docs/requirements.txt" >/dev/null

export DJANGO_SETTINGS_MODULE="$SETTINGS"

"$PYTHON_BIN" manage.py check
"$PYTHON_BIN" manage.py import_education education.xlsx >"$LOG_DIR/import_education.log" 2>&1 || true
"$PYTHON_BIN" "$ROOT_DIR/tmp/docs/seed_demo_data.py"

"$PYTHON_BIN" manage.py runserver "127.0.0.1:${PORT}" >"$LOG_DIR/runserver.log" 2>&1 &
SERVER_PID=$!
trap 'kill $SERVER_PID >/dev/null 2>&1 || true' EXIT

for _ in {1..20}; do
  if curl -s "$BASE_URL" >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

DOCS_BASE_URL="$BASE_URL" "$PYTHON_BIN" "$ROOT_DIR/tmp/docs/capture_user_flow_screenshots.py"
"$PYTHON_BIN" "$ROOT_DIR/tmp/docs/generate_user_flow_pack.py"
"$ROOT_DIR/tmp/docs/render_decks_for_qa.sh"

echo "Training pack build complete."
echo "Decks: $ROOT_DIR/output/doc/user-flow-decks"
echo "Manuals: $ROOT_DIR/docs/product-user-flows"
