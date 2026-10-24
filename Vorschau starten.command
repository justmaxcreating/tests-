#!/bin/bash
# Doppelklick startet die Website lokal unter http://localhost:8123 und öffnet sie im Browser.
# (index.html direkt aus dem Finder zu öffnen funktioniert nicht: die Links zeigen auf Ordner wie /wuerzburg/,
#  und die liefert nur ein Webserver als Seite aus.)  Beenden: dieses Fenster schließen.
# Eigener Port 8123, damit kein anderer Server (z. B. ein alter auf 8000) versehentlich angezeigt wird.
PORT=8123
cd "$(dirname "$0")/fewo-relaunch" || exit 1
if lsof -iTCP:$PORT -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Port $PORT ist schon belegt – läuft die Vorschau bereits in einem anderen Fenster?"
  open "http://localhost:$PORT/"
  exit 0
fi
(sleep 1 && open "http://localhost:$PORT/") &
echo "Vorschau läuft auf http://localhost:$PORT – zum Beenden dieses Fenster schließen."
python3 -m http.server $PORT
