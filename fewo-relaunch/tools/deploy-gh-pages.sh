#!/bin/bash
# Baut die Seite und veröffentlicht sie auf GitHub Pages (Branch gh-pages):
#   https://justmaxcreating.github.io/tests-/
# Aufruf (aus dem Ordner fewo-relaunch):  bash tools/deploy-gh-pages.sh
# Voraussetzung: Ortsfotos liegen lokal in assets/photos/ (einmalig: node tools/fetch-photos-local.js).
# gh-pages enthält nur die fertige Seite – keine Generator-Werkzeuge, kein Plugin, kein README.
set -euo pipefail
SITE="$(cd "$(dirname "$0")/.." && pwd)"
REPO="$(git -C "$SITE" rev-parse --show-toplevel)"
REMOTE="$(git -C "$REPO" remote get-url origin)"
SRC="$(git -C "$REPO" rev-parse --short HEAD)"

[ "$(ls "$SITE/assets/photos" 2>/dev/null | wc -l)" -gt 10 ] || { echo "assets/photos fehlt – erst: node tools/fetch-photos-local.js"; exit 1; }
python3 "$SITE/tools/gen/build.py" | head -1

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
git clone -q --depth 1 --branch gh-pages "$REMOTE" "$TMP"
rsync -a --delete --exclude .git --exclude .DS_Store --exclude __pycache__ --exclude .claude \
  --exclude tools --exclude plugins --exclude preview --exclude README.md --exclude .gitignore \
  --exclude _headers --exclude _redirects "$SITE/" "$TMP/"
touch "$TMP/.nojekyll"
cd "$TMP"
git add -A
if git diff --cached --quiet; then echo "Keine Änderungen – gh-pages ist aktuell."; exit 0; fi
git -c user.name="$(git -C "$REPO" log -1 --format=%an)" -c user.email="$(git -C "$REPO" log -1 --format=%ae)" \
  commit -q -m "Vorschau aktualisiert (gebaut aus fewo-relaunch@$SRC)"
git push -q origin gh-pages
echo "Veröffentlicht: https://justmaxcreating.github.io/tests-/ (in ca. 1 Minute sichtbar)"
