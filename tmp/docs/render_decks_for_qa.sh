#!/bin/zsh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
DECK_DIR="$ROOT_DIR/output/doc/user-flow-decks"
PDF_DIR="$DECK_DIR/qa-render/pdf"
PREVIEW_DIR="$DECK_DIR/qa-render/previews"

mkdir -p "$PDF_DIR" "$PREVIEW_DIR"

for deck in "$DECK_DIR"/*.pptx; do
  [ -f "$deck" ] || continue
  soffice --headless --convert-to pdf --outdir "$PDF_DIR" "$deck" >/dev/null
done

for pdf in "$PDF_DIR"/*.pdf; do
  [ -f "$pdf" ] || continue
  qlmanage -t -s 1400 -o "$PREVIEW_DIR" "$pdf" >/dev/null 2>&1 || true
done

echo "Rendered QA assets into:"
echo "  $PDF_DIR"
echo "  $PREVIEW_DIR"
