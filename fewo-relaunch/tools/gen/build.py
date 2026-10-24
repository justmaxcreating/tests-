"""Erzeugt index.html und wuerzburg/altstadt/index.html aus home.py / detail.py.

Aufruf (aus dem Ordner fewo-relaunch):  python3 tools/gen/build.py
Inhalte (Wohnungen, Texte, FAQ, Bewertungen) stehen in home.py und detail.py,
gemeinsame Bausteine (Header, Footer, Icons, Bilder, Kalender) in parts.py.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import home, detail  # noqa: E402

OUT = os.path.abspath(os.path.join(HERE, "..", ".."))
with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
    f.write(home.build())
with open(os.path.join(OUT, "wuerzburg", "altstadt", "index.html"), "w", encoding="utf-8") as f:
    f.write(detail.build())
print("index.html und wuerzburg/altstadt/index.html neu erzeugt")
