"""Prüft alle Seiten: kaputte interne Links und Bilder, genau eine H1, gültiges JSON-LD, Länge von Titel und Beschreibung.

Aufruf (aus dem Ordner fewo-relaunch):  python3 tools/check.py
"""
import html
import json
import os
import re
import sys
from urllib.parse import urljoin, urlparse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKIP = ("tools", "preview", "plugins", ".claude")

pages = [os.path.join(dp, f) for dp, _, fs in os.walk(ROOT) for f in fs
         if f.endswith(".html") and not os.path.relpath(dp, ROOT).startswith(SKIP)]
problems = []
for p in sorted(pages):
    rel = os.path.relpath(p, ROOT)
    url = "/" if rel == "404.html" else "/" + (os.path.dirname(rel) + "/" if os.path.dirname(rel) else "")
    s = open(p, encoding="utf-8").read()
    title = html.unescape(re.search(r"<title>(.*?)</title>", s).group(1))
    desc = html.unescape(re.search(r'<meta name="description" content="(.*?)">', s).group(1))
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            json.loads(m.group(1))
        except ValueError as e:
            problems.append(f"{rel}: JSON-LD {e}")
    refs = re.findall(r'(?:href|src)="([^"#][^"]*)"', s)
    refs += [x.split(" ")[0] for ss in re.findall(r'srcset="([^"]+)"', s) for x in ss.split(", ")]
    refs += [it["src"] for ph in re.findall(r'data-photos="([^"]+)"', s) for it in json.loads(html.unescape(ph))]
    missing = set()
    for ref in refs:
        if ref.startswith(("http", "tel:", "mailto:", "data:", "//")):
            continue
        target = urlparse(urljoin(url, ref)).path
        fp = os.path.join(ROOT, target.lstrip("/"))
        if target.endswith("/"):
            fp = os.path.join(fp, "index.html")
        if not os.path.exists(fp):
            missing.add(target)
    flags = []
    if len(re.findall(r"<h1[\s>]", s)) != 1:
        flags.append("H1 nicht genau 1×")
    if len(title) > 60:
        flags.append(f"Titel {len(title)} Zeichen")
    if rel not in ("404.html", "impressum/index.html", "datenschutz/index.html") and not 110 <= len(desc) <= 158:
        flags.append(f"Beschreibung {len(desc)} Zeichen")
    print(f"{rel:<48} {' · '.join(flags) or 'ok'}")
    problems += [f"{rel}: fehlt {m}" for m in sorted(missing)]
print("\n".join(problems) or "\nKeine kaputten Links oder Bilder, JSON-LD gültig.")
sys.exit(1 if problems else 0)
