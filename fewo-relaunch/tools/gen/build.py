"""Erzeugt alle Seiten, sitemap.xml und _redirects aus den Inhalten in data.py & Co.

Aufruf (aus dem Ordner fewo-relaunch):  python3 tools/gen/build.py
Inhalte: Wohnungen in data.py, Startseite in home.py, Übersichten in hub.py, weitere Seiten in pages.py.
Gemeinsame Bausteine (Header, Footer, Icons, Bilder) in parts.py, Karten in maps.py.
"""
import datetime
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import detail, home, hub, pages  # noqa: E402
from data import APARTMENTS  # noqa: E402
from parts import INDEXABLE, SITE  # noqa: E402

OUT = os.path.abspath(os.path.join(HERE, "..", ".."))


def write(path, content):
    full = os.path.join(OUT, path, "index.html") if not path.endswith(".html") else os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    return path


written = [
    write("", home.build()),
    write("wuerzburg/", hub.build_wuerzburg()),
    write("thuengen/", hub.build_thuengen()),
    write("ausfluege/", pages.build_ausfluege()),
    write("kongress-geschaeftsreise/", pages.build_kongress()),
    write("anreise-kontakt/", pages.build_kontakt(home.inquiry_form("../"))),
]
written += [write(a["path"], detail.build(a)) for a in APARTMENTS]
write("impressum/", pages.build_impressum())
write("datenschutz/", pages.build_datenschutz())
write("404.html", pages.build_404())

# Alte Prototyp-URL aufräumen (jetzt /wuerzburg/herzstueck-der-altstadt/)
old = os.path.join(OUT, "wuerzburg", "altstadt")
if os.path.isdir(old):
    shutil.rmtree(old)

# ---------- sitemap.xml ----------
today = datetime.date.today().isoformat()
urls = "".join(f"  <url>\n    <loc>{SITE}/{p}</loc>\n    <lastmod>{today}</lastmod>\n  </url>\n" for p in written)
with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')

# ---------- _redirects (Netlify): alte fewo-urlaub.com-URLs → neue Seiten, 301 ----------
OLD = "/ferienwohnungen-fraenkisches-weinland"
rules = [
    (f"{OLD}/ferienwohnungen-wuerzburg", "/wuerzburg/"),
    *[(f"{OLD}/ferienwohnungen-wuerzburg/{o}", "/" + a["path"]) for a in APARTMENTS if a["city"] == "wuerzburg" for o in a["old"]],
    (f"{OLD}/ferienwohnung-thuengen/ferienwohnung-thuengen-unterfranken", "/thuengen/blauer-reiter/"),
    (f"{OLD}/ferienwohnung-thuengen", "/thuengen/"),
    (f"{OLD}/unterkunftsanfrage", "/anreise-kontakt/"),
    ("/ferien-fraenkisches-weinland", "/thuengen/"),
    ("/staedtereise-wuerzburg/ausfluege-empfehlungen-stadturlaub", "/ausfluege/"),
    ("/staedtereise-wuerzburg", "/wuerzburg/"),
    ("/universitaet-kongress", "/kongress-geschaeftsreise/"),
    ("/kontakt-ferienwohnungen/anreise-thuengen", "/anreise-kontakt/"),
    ("/kontakt-ferienwohnungen/eichenholz-produke-thuengen", "/#eiche"),
    ("/kontakt-ferienwohnungen/impressum-kaempf", "/impressum/"),
    ("/kontakt-ferienwohnungen", "/anreise-kontakt/"),
    (OLD, "/"),
    ("/wuerzburg/altstadt", "/wuerzburg/herzstueck-der-altstadt/"),  # Prototyp-URL
]
lines = ["# 301-Weiterleitungen von der alten fewo-urlaub.com-Struktur (Netlify-Format). Erzeugt von tools/gen/build.py.",
         "# Erhält Rankings & Backlinks. Vor Go-live mit dem Search-Console-Export der alten URLs abgleichen.", ""]
w = max(len(s) for s, _ in rules) + 6
for src, dst in rules:
    for variant in (src, src + ".html", src + "/"):
        lines.append(f"{variant:<{w}} {dst:<40} 301")
with open(os.path.join(OUT, "_redirects"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"{len(written)} Seiten in der Sitemap, {len(rules) * 3} Weiterleitungen, indexierbar: {INDEXABLE}")

from reviews import CHECKS  # noqa: E402
open_checks = sum(len(v) for v in CHECKS.values())
if open_checks:
    print(f"ACHTUNG: {open_checks} offene Prüfpunkte in tools/gen/reviews.py (CHECKS) – vor Go-live mit den Gastgebern klären:")
    for page, items in CHECKS.items():
        for t in items:
            print(f"  · {page}: {t}")
