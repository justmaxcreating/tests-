"""Gemeinsame Bausteine für alle Seiten."""
import html as H
import json
import os

SITE = "https://www.fewo-urlaub.com"
PHONE, PHONE_LABEL = "+49936099183", "09360 99183"
HOST_ADDRESS = "Gartenstraße 11, 97289 Thüngen"

# Vorschau: noindex. Vor Go-live auf True setzen (und _headers löschen), dann neu bauen.
INDEXABLE = False

ICONS = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "left": '<path d="M15 6l-6 6 6 6"/>',
    "right": '<path d="M9 6l6 6-6 6"/>',
    "down": '<path d="M6 9l6 6 6-6"/>',
    "search": '<circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4-4"/>',
    "share": '<path d="M12 15V3.5M7.5 8 12 3.5 16.5 8"/><path d="M5 12v6.5A2 2 0 0 0 7 20.5h10a2 2 0 0 0 2-2V12"/>',
    "heart": '<path d="M12 20s-7.5-4.6-7.5-10.2A4.3 4.3 0 0 1 12 7a4.3 4.3 0 0 1 7.5 2.8C19.5 15.4 12 20 12 20z"/>',
    "grid": '<rect x="3.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.5"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18.5 14.5A6.5 6.5 0 0 1 21.5 20"/>',
    "area": '<rect x="3.5" y="3.5" width="17" height="17" rx="3"/><path d="M8 3.5v4M3.5 12h4M16 20.5v-4M20.5 12h-4"/>',
    "bed": '<path d="M3 19v-9M21 19v-5a3 3 0 0 0-3-3h-8v6M3 17h18"/><circle cx="6.5" cy="13" r="1.8"/>',
    "sofa": '<path d="M5 11V8a3 3 0 0 1 3-3h8a3 3 0 0 1 3 3v3"/><path d="M3 13a2 2 0 0 1 4 0v2h10v-2a2 2 0 0 1 4 0v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    "stairs": '<path d="M3 20h5v-5h5v-5h5V5h3"/>',
    "wifi": '<path d="M2.5 9a14 14 0 0 1 19 0M5.5 12.5a9.5 9.5 0 0 1 13 0M8.5 16a5 5 0 0 1 7 0"/><path d="M12 19.2h.01"/>',
    "tv": '<rect x="2.5" y="4.5" width="19" height="12.5" rx="2"/><path d="M8 20.5h8"/>',
    "kitchen": '<rect x="3.5" y="3.5" width="17" height="17" rx="2.5"/><circle cx="9" cy="10" r="2.5"/><circle cx="15.5" cy="10" r="2"/><path d="M3.5 15h17"/>',
    "washer": '<rect x="4" y="2.5" width="16" height="19" rx="2.5"/><circle cx="12" cy="13.5" r="4.5"/><path d="M7.5 6h.01M10.5 6h.01"/>',
    "shower": '<path d="M4 21V7a4 4 0 0 1 8 0"/><path d="M9 9h6a3 3 0 0 0-6 0zM10 14v1M13 13v1M16 14v1M11.5 17.5v1M14.5 17.5v1"/>',
    "bath": '<path d="M3.5 12h17v3a4 4 0 0 1-4 4h-9a4 4 0 0 1-4-4z"/><path d="M6 12V6a2 2 0 0 1 4 0M7 19l-1 2M17 19l1 2"/>',
    "baby": '<path d="M4 9h16v8H4zM4 9V6M20 9V6M4 17v3M20 17v3M8 9v8M12 9v8M16 9v8"/>',
    "paw": '<circle cx="7" cy="9" r="1.9"/><circle cx="11" cy="6.3" r="1.9"/><circle cx="15.5" cy="6.8" r="1.9"/><circle cx="18.6" cy="10.8" r="1.7"/><path d="M12.4 11.3c2.6 0 5.3 3.6 5.3 6 0 2-1.7 2.6-3 2.2-1.2-.4-1.6-.7-2.6-.7s-1.4.3-2.6.7c-1.3.4-3-.2-3-2.2 0-2.4 3.3-6 5.9-6z"/>',
    "nopaw": '<circle cx="12" cy="12" r="9"/><path d="M5.6 5.6l12.8 12.8"/>',
    "leaf": '<path d="M12 3c5 3.5 7 7.5 7 11a7 7 0 0 1-14 0c0-3.5 2-7.5 7-11z"/><path d="M12 9v12M12 14l-3-2.5M12 17l3.5-3"/>',
    "tree": '<path d="M12 21v-5"/><path d="M12 3 6.5 10.5h3L5 16h14l-4.5-5.5h3z"/>',
    "phone": '<path d="M5 3.5h3.5l1.8 4.6-2.3 1.5a11 11 0 0 0 6.4 6.4l1.5-2.3 4.6 1.8V19a1.9 1.9 0 0 1-2 1.9A16.5 16.5 0 0 1 3.1 5.5 1.9 1.9 0 0 1 5 3.5z"/>',
    "copy": '<rect x="8.5" y="8.5" width="12" height="12" rx="2.5"/><path d="M15.5 8.5V6a2.5 2.5 0 0 0-2.5-2.5H6A2.5 2.5 0 0 0 3.5 6v7A2.5 2.5 0 0 0 6 15.5h2.5"/>',
    "key": '<circle cx="8" cy="15" r="4.5"/><path d="M11.2 11.8 20 3M16.5 6.5 19 9M14 9l2 2"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "car": '<path d="M4 16.5V12l2-5h12l2 5v4.5"/><path d="M3 12h18v4.5H3z"/><circle cx="7.5" cy="16.5" r="1.8"/><circle cx="16.5" cy="16.5" r="1.8"/>',
    "parking": '<rect x="3.5" y="3.5" width="17" height="17" rx="3.5"/><path d="M9.5 17V7.5h3.5a3 3 0 0 1 0 6H9.5"/>',
    "train": '<rect x="5" y="3" width="14" height="13" rx="3"/><path d="M5 10h14M8.5 19.5 7 21M15.5 19.5 17 21M8.5 13.2h.01M15.5 13.2h.01"/>',
    "briefcase": '<rect x="3.5" y="7" width="17" height="12.5" rx="2.5"/><path d="M9 7V5.5A1.5 1.5 0 0 1 10.5 4h3A1.5 1.5 0 0 1 15 5.5V7M3.5 12.5h17"/>',
    "church": '<path d="M12 2.5v4M10 4.5h4M7 21V11l5-4.5 5 4.5v10M3.5 21h17M10.5 21v-4a1.5 1.5 0 0 1 3 0v4"/>',
    "walk": '<circle cx="13" cy="4.5" r="1.8"/><path d="M10 21l2-6 3 3v3M8 12l2.5-4.5 4 1.5 2 3M12 15l-1.5-4"/>',
    "chat": '<path d="M4 5.5h16v10.5H9l-5 4z"/>',
    "receipt": '<path d="M6 2.5h12v19l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "x": '<path d="M6 6l12 12M18 6 6 18"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "user": '<circle cx="12" cy="8.5" r="3.8"/><path d="M4.5 20.5a7.5 7.5 0 0 1 15 0"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    "wine": '<path d="M7 3h10l-.6 5.5a4.4 4.4 0 0 1-8.8 0z"/><path d="M12 13v8M8.5 21h7"/>',
    "door": '<path d="M5 21V4.5A1.5 1.5 0 0 1 6.5 3h11A1.5 1.5 0 0 1 19 4.5V21M3 21h18M15 12h.01"/>',
    "sparkle": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>',
    "smoke": '<circle cx="12" cy="12" r="9"/><path d="M5.6 5.6l12.8 12.8M7 13.5h7M16 13.5h1"/>',
}
STAR = '<symbol id="i-star" viewBox="0 0 24 24"><path fill="currentColor" d="M12 3.2l2.6 5.5 6 .7-4.4 4.1 1.1 6-5.3-3-5.3 3 1.1-6L3.4 9.4l6-.7z"/></symbol>'


def sprite():
    syms = "".join(
        f'<symbol id="i-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{v}</symbol>'
        for k, v in ICONS.items()
    )
    return f'<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true"><defs>{syms}{STAR}</defs></svg>'


def icon(name, size=20, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg width="{size}" height="{size}"{c} aria-hidden="true"><use href="#i-{name}"/></svg>'


def esc(s):
    return H.escape(s, quote=True)


# ---------- Bilder ----------
# Zwei Arten von Motiven:
#  "wue-hero"            → Ortsfoto aus dem Foto-Plugin: assets/photos/<slot>-960.jpg / -1920.jpg
#  "fewo/<wohnung>/02"   → echtes Foto der Gastgeber: assets/fewo/<wohnung>/02.jpg (Maße aus manifest.json)
_MANIFEST = json.load(open(os.path.join(os.path.dirname(__file__), "..", "..", "assets", "fewo", "manifest.json"), encoding="utf-8"))
_SIZES = {f"fewo/{slug}/{it['file'][:-4]}": (it["w"], it["h"]) for slug, items in _MANIFEST.items() for it in items}


def is_own(slot):
    return slot.startswith("fewo/")


def photo_src(prefix, slot, large=False):
    if is_own(slot):
        return f"{prefix}assets/{slot}.jpg"
    return f"{prefix}assets/photos/{slot}-{1920 if large else 960}.jpg"


def photo_url(slot):
    return SITE + "/" + photo_src("", slot, large=True)


def img(prefix, slot, alt, sizes="100vw", eager=False, cls=""):
    a = esc(alt)
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    c = f" {cls}" if cls else ""
    if is_own(slot):
        w, h = _SIZES[slot]
        tag = f'<img src="{photo_src(prefix, slot)}" alt="{a}" width="{w}" height="{h}" {load} decoding="async">'
    else:
        base = f"{prefix}assets/photos/{slot}"
        tag = (f'<img src="{base}-960.jpg" srcset="{base}-960.jpg 960w, {base}-1920.jpg 1920w" '
               f'sizes="{sizes}" alt="{a}" width="960" height="720" {load} decoding="async">')
    return f'<div class="media{c}" data-label="{a}">{tag}</div>'


def slider(prefix, photos, sizes, extra=""):
    slides = "".join(img(prefix, s, a, sizes) for s, a in photos)
    dots = "".join("<i></i>" for _ in photos)
    return (
        f'<div class="slider" data-slider>{extra}<div class="slider-track">{slides}</div>'
        f'<button class="slider-btn prev" type="button" aria-label="Vorheriges Foto">{icon("left", 16)}</button>'
        f'<button class="slider-btn next" type="button" aria-label="Nächstes Foto">{icon("right", 16)}</button>'
        f'<div class="dots" aria-hidden="true">{dots}</div><span class="slider-count" aria-hidden="true">1 / {len(photos)}</span></div>'
    )


def avatars(prefix):
    """Kleine Fotos der Gastgeber – rein schmückend, der Name steht im Text daneben."""
    return ('<div class="avatars" aria-hidden="true">'
            f'<img src="{prefix}assets/fewo/gastgeber/2.jpg" alt="" width="160" height="160" loading="lazy" decoding="async">'
            f'<img src="{prefix}assets/fewo/gastgeber/1.jpg" alt="" width="160" height="160" loading="lazy" decoding="async"></div>')


HEART = '<svg width="26" height="26" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20s-7.5-4.6-7.5-10.2A4.3 4.3 0 0 1 12 7a4.3 4.3 0 0 1 7.5 2.8C19.5 15.4 12 20 12 20z"/></svg>'


# ---------- Kopf, Navigation, Footer ----------
def header(prefix, current=""):
    def cur(k):
        return ' aria-current="page"' if k == current else ""

    return f"""<div class="preview-bar"><strong>Designentwurf</strong> · Inhalte und Fotos vor Veröffentlichung mit den Gastgebern abstimmen</div>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="{prefix or './'}" aria-label="Ferienwohnungen Voll – Startseite">
      <span class="brand-mark">{icon("leaf", 18)}</span>
      <span>Voll<small>Ferienwohnungen in Franken</small></span>
    </a>
    <nav class="nav" aria-label="Hauptnavigation">
      <a href="{prefix}#unterkuenfte"{cur("home")}>Unterkünfte</a>
      <a href="{prefix}wuerzburg/"{cur("wuerzburg")}>Würzburg</a>
      <a href="{prefix}thuengen/"{cur("thuengen")}>Thüngen</a>
      <a href="{prefix}ausfluege/"{cur("ausfluege")}>Ausflüge</a>
      <a href="{prefix}anreise-kontakt/"{cur("kontakt")}>Kontakt</a>
    </nav>
    <div class="header-actions">
      <a class="btn btn--sm" href="{prefix}#anfrage">Direkt anfragen</a>
      <button class="menu-btn" type="button" data-menu aria-expanded="false" aria-label="Menü">{icon("menu", 18)}<span class="avatar">{icon("user", 16)}</span></button>
      <div class="menu-pop" role="menu">
        <a href="{prefix}#unterkuenfte">Alle Unterkünfte</a>
        <a href="{prefix}wuerzburg/">Würzburg · 8 Wohnungen</a>
        <a href="{prefix}thuengen/">Thüngen · 4 Wohnungen</a>
        <a href="{prefix}ausfluege/">Ausflüge &amp; Region</a>
        <a href="{prefix}kongress-geschaeftsreise/">Kongress &amp; Geschäftsreise</a>
        <hr>
        <a href="{prefix}#anfrage">Anfrage senden</a>
        <a href="tel:{PHONE}">Anrufen: {PHONE_LABEL}</a>
      </div>
    </div>
  </div>
</header>"""


def footer(prefix):
    from data import APARTMENTS  # spät importieren (data importiert parts)

    def links(city):
        return "".join(f'<li><a href="{prefix}{a["path"]}">{a["name"]}</a></li>' for a in APARTMENTS if a["city"] == city)

    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="brand" href="{prefix or './'}"><span class="brand-mark">{icon("leaf", 18)}</span><span>Voll<small>Ferienwohnungen in Franken</small></span></a>
        <p class="muted" style="margin-top:16px;max-width:34ch">Zwölf Ferienwohnungen in der Würzburger Innenstadt und am Schlossberg in Thüngen – von der Familie hinter dem Sägewerk Hugo Kämpf.</p>
        <ul style="margin-top:20px">
          <li>Carolin &amp; Stefan Voll</li>
          <li>{HOST_ADDRESS}</li>
          <li><a href="tel:{PHONE}">{PHONE_LABEL}</a></li>
        </ul>
      </div>
      <div><h3><a href="{prefix}wuerzburg/">Ferienwohnungen Würzburg</a></h3><ul>{links("wuerzburg")}</ul></div>
      <div><h3><a href="{prefix}thuengen/">Ferienwohnungen Thüngen</a></h3><ul>{links("thuengen")}</ul></div>
      <div><h3>Entdecken</h3><ul>
        <li><a href="{prefix}ausfluege/">Ausflüge &amp; Sehenswürdigkeiten</a></li>
        <li><a href="{prefix}kongress-geschaeftsreise/">Kongress &amp; Geschäftsreise</a></li>
        <li><a href="{prefix}anreise-kontakt/">Anreise &amp; Kontakt</a></li>
        <li><a href="{prefix}#eiche">Eiche aus Thüngen</a></li>
        <li><a href="https://hugokaempf.de/" rel="noopener" target="_blank">Sägewerk Hugo Kämpf</a></li>
      </ul></div>
    </div>
    <details class="credits" data-credits="{prefix}assets/photos/credits.json"><summary>Bildnachweise</summary><ul><li>Fotos der Wohnungen: Carolin &amp; Stefan Voll</li><li>Kartendaten: © OpenStreetMap-Mitwirkende (ODbL)</li></ul></details>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> Ferienwohnungen Voll · Würzburg &amp; Thüngen</span>
      <nav aria-label="Rechtliches"><a href="{prefix}impressum/">Impressum</a><a href="{prefix}datenschutz/">Datenschutz</a></nav>
    </div>
  </div>
</footer>
<div class="toast" role="status" aria-live="polite"></div>"""


def guests_panel(max_guests, note=""):
    n = f'<p class="guest-note">{note}</p>' if note else ""
    return f"""<div class="guest-row"><div><strong>Erwachsene</strong><small>ab 13 Jahren</small></div>
  <div class="stepper" data-guest="adults"><button type="button" aria-label="Weniger Erwachsene">−</button><output aria-live="polite">2</output><button type="button" aria-label="Mehr Erwachsene">+</button></div></div>
<div class="guest-row"><div><strong>Kinder</strong><small>2–12 Jahre</small></div>
  <div class="stepper" data-guest="children"><button type="button" aria-label="Weniger Kinder">−</button><output aria-live="polite">0</output><button type="button" aria-label="Mehr Kinder">+</button></div></div>
<div class="guest-row"><div><strong>Kleinkinder</strong><small>unter 2 Jahren</small></div>
  <div class="stepper" data-guest="infants"><button type="button" aria-label="Weniger Kleinkinder">−</button><output aria-live="polite">0</output><button type="button" aria-label="Mehr Kleinkinder">+</button></div></div>{n}"""


def cal_panel(after=""):
    a = f' data-after-range="{after}"' if after else ""
    return f"""<div class="cal-title"><strong data-show="nights" data-empty="Anreise wählen"></strong><span data-show="range" data-empty="Wählen Sie An- und Abreise"></span></div>
<div class="cal two" data-cal{a}></div>
<div class="popover-foot"><button class="text-btn" type="button" data-clear-dates><span>Daten löschen</span></button><button class="btn btn--sm" type="button" data-close>Fertig</button></div>"""


def sheets(max_guests, note=""):
    return f"""<div class="sheet" id="sheet-cal" role="dialog" aria-label="Zeitraum wählen"><div class="sheet-panel"><div class="sheet-grip"></div>{cal_panel()}</div></div>
<div class="sheet" id="sheet-guests" role="dialog" aria-label="Gäste wählen"><div class="sheet-panel"><div class="sheet-grip"></div><div class="sheet-head"><h2>Wer kommt mit?</h2><button class="icon-btn" type="button" data-close aria-label="Schließen">{icon("x", 16)}</button></div>{guests_panel(max_guests, note)}<div class="popover-foot" style="justify-content:flex-end"><button class="btn btn--sm" type="button" data-close>Fertig</button></div></div></div>"""


def status_box():
    return """<div class="form-status" role="status" aria-live="polite"><span class="tick"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></span><span class="status-text"></span></div>"""


def faq_list(items, first_open=True):
    return "\n".join(
        f'<details name="faq"{" open" if first_open and i == 0 else ""}><summary>{q}{icon("down", 18)}</summary><div class="answer">{a}</div></details>'
        for i, (q, a) in enumerate(items)
    )


def crumbs(prefix, items):
    """items: [(Name, Pfad oder None)], erster Eintrag = Startseite."""
    out = []
    for i, (name, path) in enumerate(items):
        if i:
            out.append(icon("right", 14))
        out.append(f'<a href="{prefix}{path}">{name}</a>' if path is not None else f'<span aria-current="page">{name}</span>')
    return f'<nav class="crumbs" aria-label="Brotkrumen">{"".join(out)}</nav>'


def ld_breadcrumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": f"{SITE}/{p}"} for i, (n, p) in enumerate(items)]}


def ld_faq(items):
    strip = lambda s: H.unescape(s.replace("<br>", " ")).replace("&amp;", "&")
    import re
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip(re.sub(r"<[^>]+>", "", q)), "acceptedAnswer": {"@type": "Answer", "text": strip(re.sub(r"<[^>]+>", "", a))}} for q, a in items]}


def jsonld(graph):
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)


def head(prefix, title, desc, path, og_image, graph, indexable=True):
    canonical = f"{SITE}/{path}"
    robots = "index, follow, max-image-preview:large" if (INDEXABLE and indexable) else "noindex, nofollow"
    note = "" if INDEXABLE else '\n  <!-- Vorschau: vor Go-live in tools/gen/parts.py INDEXABLE = True setzen, neu bauen und _headers löschen -->'
    return f"""<!doctype html>
<html lang="de" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canonical}">{note}
  <meta name="robots" content="{robots}">
  <meta name="theme-color" content="#fbfaf8">
  <link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="de_DE">
  <meta property="og:site_name" content="Ferienwohnungen Voll">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{photo_url(og_image)}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preload" href="{prefix}assets/fonts/plus-jakarta-sans-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{prefix}css/styles.css">
  <script type="application/ld+json">
{jsonld(graph)}
  </script>
</head>"""


def page_end(prefix, body_extra=""):
    return f"""{footer(prefix)}
{body_extra}
<script src="{prefix}js/main.js" defer></script>
</body>
</html>
"""
