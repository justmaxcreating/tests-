"""Detailseite einer Ferienwohnung – eine Vorlage für alle zwölf Wohnungen (Inhalte in data.py)."""
import json
from urllib.parse import quote

from cards import card
from data import APARTMENTS, OAK, RULES_THUE, RULES_WUE, meters, nearest
from maps import city_map, region_map
from parts import *

CITY = {"wuerzburg": ("Würzburg", "wuerzburg/"), "thuengen": ("Thüngen", "thuengen/")}


def features(a):
    out = list(a["highlights"])
    if a["city"] == "wuerzburg":
        near = nearest(a)
        out.append(("walk", "Zu Fuß unterwegs", "Zu Fuß: " + ", ".join(f"{n.split(' (')[0]} ca. {m} Min." for n, m, _, _ in near)))
        if a["parking"] == "talavera":
            out.append(("car", "Kostenlos parken", "Auf der Talavera am Mainufer – ohne Parkhausgebühren."))
    else:
        if a["pets"]:
            out.append(("paw", "Hunde willkommen", "Ihre Fellnase ist genauso willkommen wie Sie – Wiesen, Wald und Weinberge vor der Tür."))
        if a["parking"] == "own" and len(out) < 3:
            out.append(("car", "Parkplatz am Haus", "Kostenloser hauseigener Parkplatz direkt vor der Wohnung."))
    if len(out) < 4:
        out.append(OAK)
    return out[:4]


def amenities(a):
    beds = dict(a["beds"])
    items = [("wifi", "Kostenloses WLAN", "")]
    items.append(("kitchen", a["kitchen"], ""))
    items.append(("bed", "Separates Schlafzimmer" if a["bedrooms"] == 1 else f"{a['bedrooms']} separate Schlafzimmer", ""))
    if "Schlafcouch" in beds:
        items.append(("sofa", "Ausziehbare Schlafcouch" if beds["Schlafcouch"] == 1 else f"{beds['Schlafcouch']} Schlafcouches", ""))
    items.append(("bath" if "Badewanne" in a["bath"] else "shower", a["bath"], ""))
    if a["washer"]:
        items.append(("washer", a["washer"], ""))
    if a["parking"] == "own":
        items.append(("parking", "Kostenloser Parkplatz am Haus", ""))
    if a["pets"]:
        items.append(("paw", "Hunde willkommen", ""))
    for ic, t in a.get("extra_amen", []):
        items.append((ic, t, ""))
    if a["id"] != "thue-blauer-reiter":
        items += [("tv", "Flat-TV", ""), ("baby", "Babybett vorhanden", "")]
    items.append(("leaf", "Möbel und Unikate aus eigener Eiche", ""))
    items.append(("key", "Schlüssel liegt zur Check-in-Zeit bereit" if a["city"] == "wuerzburg" else "Schlüsselübergabe nach Absprache", ""))
    if a.get("floor_level") == "0":
        items.append(("door", "Erdgeschoss – keine Treppen", ""))
    if a["elevator"] is False:
        items.append(("stairs", f"Kein Aufzug ({a['floor'].split(',')[0]})", "no"))
    if a["pets"] is False:
        items.append(("nopaw", "Keine Haustiere", "no"))
    items.append(("smoke", "Nichtraucherwohnung", ""))
    # die ersten 8 sichtbar, Rest hinter „Alle anzeigen“; Einschränkungen immer ans Ende
    pos = [i for i in items if i[2] != "no"]
    neg = [i for i in items if i[2] == "no"]
    ordered = pos + neg
    return [(ic, t, c if n < 8 else (c + " extra").strip()) for n, (ic, t, c) in enumerate(ordered)]


def faq(a):
    q = []
    total = a["guests"]
    sleep = ", ".join(f"{r}: {b}" for r, b, _ in a["sleep"] if not r.startswith("Weitere"))
    q.append((f"Für wie viele Personen ist die Wohnung geeignet?",
              f"Für {'bis zu ' if total > 2 else ''}{total} Personen. {sleep}."
              + (" Ein Babybett ist vorhanden." if a["id"] != "thue-blauer-reiter" else " Mehr Gäste? Sprechen Sie uns gern an.")))
    if a["parking"] == "own" and a["city"] == "wuerzburg":
        q.append(("Gibt es einen Parkplatz?", "Ja – ein kostenloser, hauseigener Parkplatz steht direkt vor der Wohnung."))
    elif a["parking"] == "own":
        q.append(("Gibt es einen Parkplatz?", "Ja, Sie parken kostenlos direkt am Haus."))
    elif a["parking"] == "talavera":
        q.append(("Wo parke ich in der Nähe?", "Kostenlos parken Sie auf der Talavera am Mainufer, gegenüber der Innenstadt. Daneben gibt es kostenpflichtige Parkhäuser und Parkflächen in der Umgebung."))
    if a["elevator"] is False:
        q.append(("Gibt es einen Aufzug?", f"Nein. Die Wohnung liegt im {a['floor'].split(',')[0]}, einen Aufzug gibt es nicht."))
    elif a.get("floor_level") == "0":
        q.append(("Muss ich Treppen steigen?", "Nein, die Wohnung liegt im Erdgeschoss."))
    if a["pets"] is True:
        q.append(("Darf mein Hund mit?", "Ja, Hunde sind in unseren Ferienwohnungen in Thüngen herzlich willkommen."))
    elif a["pets"] is False:
        q.append(("Sind Haustiere erlaubt?", "In dieser Wohnung leider nicht. Mit Hund empfehlen wir unsere <a class=\"u-link\" href=\"../../thuengen/\">Ferienwohnungen in Thüngen</a> – dort sind Hunde willkommen."))
    if a["city"] == "wuerzburg":
        d = {k: (m, mm) for _, m, mm, k in a["distances"]}
        q.append(("Wie weit ist es zu Dom, Residenz und Bahnhof?",
                  f"Zu Fuß sind es zum Dom etwa {d['dom'][0]} Minuten, zur Residenz etwa {d['residenz'][0]} Minuten und zum Hauptbahnhof etwa {d['hbf'][0]} Minuten."))
    else:
        q.append(("Wie weit ist es nach Würzburg?", "Thüngen liegt rund 25 km nördlich von Würzburg im Fränkischen Weinland. Bamberg mit seiner sehenswerten Altstadt ist etwa 85 km entfernt."))
    q.append(("Wann kann ich anreisen?", (a.get("checkin") or "Check-in ist ab 15 Uhr") + ", Check-out bis 11 Uhr. Kommen Sie später an, sagen Sie uns Bescheid – wir finden eine Lösung."))
    q.append(("Wie funktioniert die Buchung?", "Sie senden uns eine unverbindliche Anfrage mit Wunschzeitraum. Wir melden uns persönlich mit Verfügbarkeit und Preis. Erst wenn Sie zusagen, ist die Buchung fest."))
    return q


def rules(a):
    arrive = RULES_WUE if a["city"] == "wuerzburg" else RULES_THUE
    if a.get("checkin"):
        arrive = [a["checkin"], "Check-out bis 11:00 Uhr", "Schlüsselübergabe nach Absprache"]
    house = [f"Maximal {a['guests']} Gäste"]
    if a["pets"] is True:
        house.append("Hunde willkommen")
    elif a["pets"] is False:
        house.append("Keine Haustiere")
    house += ["Nichtraucherwohnung", "Keine Partys"]
    building = [a["floor"].replace(", ", " · ")]
    if a["parking"] == "own":
        building.append("Kostenloser Parkplatz am Haus")
    elif a["parking"] == "talavera":
        building.append("Kostenlos parken: Talavera")
    if a["id"] != "thue-blauer-reiter":
        building.append("Babybett vorhanden")
    building.append("Bei Buchung bitte Anschrift angeben")
    return [("Anreise &amp; Abreise", arrive), ("Hausregeln", house), ("Das Haus", building)]


def jsonld(a, faq_items):
    city_name, city_path = CITY[a["city"]]
    beds = [{"@type": "BedDetails", "typeOfBed": t, "numberOfBeds": n} for t, n in a["beds"]]
    amen = [("wifi", True), ("kitchen", True), ("tv", a["id"] != "thue-blauer-reiter"), ("crib", a["id"] != "thue-blauer-reiter")]
    if a["washer"]:
        amen.append(("washerDryer", True))
    if a["parking"] == "own":
        amen.append(("freeParking", True))
    if a["elevator"] is False:
        amen.append(("elevator", False))
    if a["pets"] is not None:
        amen.append(("petsAllowed", a["pets"]))
    place = {"@type": "Accommodation", "additionalType": "EntirePlace", "numberOfBedrooms": a["bedrooms"], "numberOfBathroomsTotal": 1,
             "occupancy": {"@type": "QuantitativeValue", "maxValue": a["guests"]}, "bed": beds,
             "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": n, "value": v} for n, v in amen]}
    if a["size"]:
        place["floorSize"] = {"@type": "QuantitativeValue", "value": a["size"], "unitCode": "MTK"}
    if a.get("floor_level") is not None:
        place["floorLevel"] = a["floor_level"]
    addr = {"@type": "PostalAddress", "postalCode": a["zip"], "addressLocality": a["town"], "addressRegion": "Bayern", "addressCountry": "DE"}
    if a["street"] != "Haus Kämpf":
        addr["streetAddress"] = a["street"]
    rental = {"@type": "VacationRental", "@id": f"{SITE}/{a['path']}#rental", "identifier": a["id"], "name": f"{a['h1']} – Ferienwohnung in {city_name}",
              "description": a["desc"], "url": f"{SITE}/{a['path']}", "image": [photo_url(s) for s, _ in a["slots"][:8]],
              "telephone": "+49 9360 99183", "address": addr,
              "latitude": a["geo"][0], "longitude": a["geo"][1],
              "checkinTime": "15:00", "checkoutTime": "11:00", "containsPlace": place,
              "brand": {"@id": f"{SITE}/#host"}}
    if a["pets"] is not None:
        rental["petsAllowed"] = a["pets"]
    crumbs = [("Ferienwohnungen", ""), (f"Ferienwohnungen {city_name}", city_path), (a["name"], a["path"])]
    return [rental, ld_breadcrumbs(crumbs), ld_faq(faq_items)]


def similar(a, n=3):
    others = [o for o in APARTMENTS if o["id"] != a["id"] and o["city"] == a["city"]]
    others.sort(key=lambda o: meters(a["geo"], o["geo"]) if a["city"] == "wuerzburg" else 0)
    picks = others[:n]
    if len(picks) < n:  # Thüngen hat nur 4 – ergänzen mit Würzburg
        picks += [o for o in APARTMENTS if o["city"] != a["city"]][: n - len(picks)]
    return picks


def build(a):
    P = "../../"
    city_name, city_path = CITY[a["city"]]
    faq_items = faq(a)
    slots = a["slots"]
    photos_json = esc(json.dumps([{"src": photo_src(P, s, large=True), "alt": t} for s, t in slots], ensure_ascii=False))

    if len(slots) >= 5:
        grid = "".join(
            f'<button type="button" data-photo="{i}" aria-label="Foto vergrößern: {esc(t)}">{img(P, s, t, "(min-width: 760px) 50vw, 100vw" if i == 0 else "25vw", eager=(i == 0))}</button>'
            for i, (s, t) in enumerate(slots[:5]))
        grid_cls = "gallery-grid"
    else:
        grid = "".join(f'<button type="button" data-photo="{i}" aria-label="Foto vergrößern: {esc(t)}">{img(P, s, t, "100vw", eager=(i == 0))}</button>' for i, (s, t) in enumerate(slots))
        grid_cls = "gallery-grid gallery-grid--one"
    mobile = slider(P, slots, "100vw")

    meta = []
    if a["rating"]:
        meta.append(f'<span class="rating">{icon("star", 14)} {a["rating"][0]} · {a["rating"][1].split(" · ")[0]}</span>')
    meta.append(f'<span>{a["street"] + ", " if a["street"] != "Haus Kämpf" else "Haus Kämpf, "}{a["town"]}</span>')
    meta.append(f"<span>{a['floor'].split(',')[0]}</span>")

    beds_short = " + ".join(f"{n} {t}" if n > 1 else t for t, n in a["beds"])
    summary_line = " · ".join(([f"{a['guests_label']}"] + [f"{a['bedrooms']} Schlafzimmer", beds_short, "1 Bad"] + ([f"{a['size']} m²"] if a["size"] else [])))
    score = ""
    if a["rating"]:
        src = a["rating"][1]
        note = "Bewertung für das ganze Haus „Wohnen am Schlossberg“." if "Schlossberg" in src else "Sehr gut bewertet von Gästen."
        score = f"""<div class="score-box">
          <div class="big">{a["rating"][0]}<small>von 10</small></div>
          <p><strong>Auf {src.split(" · ")[0]}.</strong><br>{note}</p>
          {icon("sparkle", 28)}
        </div>"""

    feats = "".join(f'<div class="feature">{icon(i, 26)}<div><strong>{t}</strong><p>{d}</p></div></div>' for i, t, d in features(a))
    about = "".join(f"<p>{p}</p>" for p in a["about"])

    def room(r, b, n):
        if n:
            s = f"fewo/{a['id']}/{n}"
            alt = dict(a["photos"]).get(n, r)
            media = img(P, s, alt, "300px")
        else:
            media = f'<div class="media room-ph" aria-hidden="true">{icon("bed" if "Schlaf" in r else "sofa", 34)}</div>'
        return f'<div class="room">{media}<strong>{r}</strong><span>{b}</span></div>'

    rooms = "".join(room(*s) for s in a["sleep"])
    amen = amenities(a)
    amen_html = "".join(f'<li class="{c}">{icon(i, 24)}<span>{t}</span></li>' for i, t, c in amen)
    more_btn = f'<button class="btn btn--light" type="button" data-amenities="amen">Alle {len(amen)} Merkmale anzeigen</button>' if len(amen) > 8 else ""

    if a["city"] == "wuerzburg":
        dist = a["distances"][:6] + [d for d in a["distances"][6:] if d[3] == "talavera"]
        dist_html = "".join(f"<li><span>{n}</span><span>ca. {m} Min. · {mm:,} m</span></li>".replace(",", ".") for n, m, mm, _ in dist)
        map_svg = city_map(P, a)
        address = f"{a['street']}, {a['zip']} Würzburg"
        dist_note = '<p class="map-note">Gehzeiten geschätzt (Luftlinie + 30 %). Kartendaten © OpenStreetMap-Mitwirkende.</p>'
    else:
        dist_html = "".join(f"<li><span>{n}</span><span>{v}</span></li>" for n, v in [
            ("Würzburg", "ca. 25 km"), ("Bamberg", "ca. 85 km"), ("Weinberge &amp; Werntal-Radweg", "ab Haustür")]
            + ([("Schloss Thüngen", "nebenan")] if a["street"] != "Haus Kämpf" else []))
        map_svg = region_map()
        address = f"{a['street']}, {a['zip']} Thüngen" if a["street"] != "Haus Kämpf" else "97289 Thüngen"
        dist_note = '<p class="map-note">Schematische Karte. Kartendaten © OpenStreetMap-Mitwirkende.</p>'
    route = "https://www.openstreetmap.org/search?query=" + quote(address)

    story = ""
    if a.get("story"):
        s = a["story"]
        paras = "".join(("<p class=\"muted\">" if i else "<p>") + t + "</p>" for i, t in enumerate(s["text"]))
        story = f"""
      <section aria-labelledby="h-story">
        <h2 id="h-story">{s["title"]}</h2>
        <div class="history">
          {img(P, s["photo"], s["photo_alt"], "220px")}
          <div><div class="year">{s["year"]}</div>{paras}</div>
        </div>
      </section>"""
    elif a["city"] == "thuengen":
        story = f"""
      <section aria-labelledby="h-story">
        <h2 id="h-story">Rund ums Haus</h2>
        <div class="history">
          {img(P, "fewo/thue-haus/02", "Garten mit Wiese hinter dem Haus am Schlossberg", "220px")}
          <div><div class="year">Wern</div>
            <p>Über einen Steg über den kleinen Bach Wern erreichen Sie den Garten. Malerisch, mit kleinem Wasserfall, fließt die Wern noch immer unter dem alten Sägewerksgebäude hindurch.</p>
            <p class="muted">Nicht selten sieht man einen Silberreiher auf der Suche nach Bachforellen, und eine Wildgänsefamilie brütet jedes Jahr im alten Stock der Schlossanlage.</p></div>
        </div>
      </section>"""

    rules_html = "".join(f"<div><h3>{h}</h3><ul>{''.join(f'<li>{x}</li>' for x in items)}</ul></div>" for h, items in rules(a))
    guest_note = f"Maximal {a['guests']} Gäste. Kleinkinder zählen nicht mit." if a["guests"] > 2 else "Für 2 Gäste. Mehr Personen? Bitte kurz anfragen."
    book_rating = f'<span class="rating">{icon("star", 13)} {a["rating"][0]}</span>' if a["rating"] else ""
    sims = "\n".join(card(P, o, i * 0.06) for i, o in enumerate(similar(a)))
    more_title = f"Weitere Wohnungen in {city_name}" if a["city"] == "wuerzburg" else "Weitere Wohnungen"

    return f"""{head(P, a["title"], a["desc"], a["path"], a["cover"], jsonld(a, faq_items))}
<body data-max-guests="{a["guests"]}" class="has-mobile-bar">
{sprite()}
<a class="skip-link" href="#main">Zum Inhalt springen</a>
{header(P, a["city"])}

<main id="main" class="container">
  <div class="detail-head">
    {crumbs(P, [("Ferienwohnungen", ""), (city_name, city_path), (a["name"], None)])}
    <div class="detail-title">
      <div>
        <p class="kicker">{a["kicker"]}</p>
        <h1>{a["h1"]}</h1>
        <div class="detail-meta">{"".join(meta)}</div>
      </div>
      <div class="title-actions">
        <button class="text-btn" type="button" data-share>{icon("share", 18)}<span>Teilen</span></button>
        <button class="text-btn save-inline" type="button" data-save="{a["id"]}" aria-pressed="false">{icon("heart", 18)}<span>Merken</span></button>
      </div>
    </div>
  </div>

  <div class="gallery">
    <div class="{grid_cls}">{grid}</div>
    <button class="btn btn--light btn--sm show-all" type="button" data-photo="0">{icon("grid", 16)} Alle {len(slots)} Fotos</button>
    <div class="gallery-mobile">{mobile}<span class="gallery-count">1 / {len(slots)}</span></div>
  </div>

  <div class="detail-layout">
    <div class="detail-main">
      <section class="summary">
        <h2>Ganze Wohnung in {city_name}</h2>
        <p class="muted">{summary_line}</p>
        {score}
      </section>

      <section>
        <div class="host-row">{avatars(P)}<div><strong>Ihre Gastgeber: Carolin &amp; Stefan</strong><div class="muted" style="font-size:.92rem">Familienbetrieb aus Thüngen · antworten persönlich</div></div></div>
      </section>

      <section>
        <div class="feature-list">{feats}</div>
      </section>

      <section aria-labelledby="h-about">
        <h2 id="h-about">Über die Wohnung</h2>
        <div class="readmore" id="about">{about}</div>
        <button class="text-btn readmore-btn" type="button" data-readmore="about"><span>Mehr anzeigen</span>{icon("right", 16)}</button>
      </section>

      <section aria-labelledby="h-rooms">
        <h2 id="h-rooms">Wo Sie schlafen</h2>
        <div class="rooms">{rooms}</div>
      </section>

      <section aria-labelledby="h-amen">
        <h2 id="h-amen">Was die Wohnung bietet</h2>
        <ul class="amenities" id="amen">{amen_html}</ul>
        {more_btn}
      </section>

      <section aria-labelledby="h-cal" id="kalender">
        <h2 id="h-cal" style="margin-bottom:4px"><span data-show="nights" data-empty="Zeitraum wählen">Zeitraum wählen</span></h2>
        <p class="muted" style="margin-bottom:20px"><span data-show="range" data-empty="Wählen Sie An- und Abreise – wir prüfen die Verfügbarkeit persönlich.">Wählen Sie An- und Abreise</span></p>
        <div class="cal two" data-cal></div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:16px"><button class="text-btn" type="button" data-clear-dates><span>Daten löschen</span></button><a class="btn btn--sm" href="#buchen" data-requires-dates hidden>Weiter zur Anfrage {icon("arrow", 16, "go")}</a></div>
      </section>

      <section aria-labelledby="h-lage" id="lage">
        <h2 id="h-lage">Lage</h2>
        <p class="muted" style="margin:-8px 0 20px">{address}{" – " + a["place"].split(" · ")[1] if a["city"] == "wuerzburg" else ""}</p>
        <figure class="map-card" style="margin:0">
          {map_svg}
          <div class="map-actions">
            <button class="btn btn--light btn--sm" type="button" data-copy="{address}" data-toast="Adresse kopiert">{icon("copy", 16)} Adresse</button>
            <a class="btn btn--sm" href="{route}" target="_blank" rel="noopener">Route {icon("arrow", 14, "go")}</a>
          </div>
        </figure>
        <ul class="distances">{dist_html}</ul>
        {dist_note}
      </section>
{story}
      <section aria-labelledby="h-rules">
        <h2 id="h-rules">Gut zu wissen</h2>
        <div class="rules">{rules_html}</div>
      </section>

      <section aria-labelledby="h-faq" id="faq">
        <h2 id="h-faq">Häufige Fragen</h2>
        <div class="faq">{faq_list(faq_items)}</div>
      </section>
    </div>

    <aside class="book" id="buchen" aria-label="Verfügbarkeit anfragen">
      <form class="book-card" name="anfrage-wohnung" method="POST" data-netlify="true" netlify-honeypot="bot-field" data-inquiry data-book novalidate>
        <input type="hidden" name="form-name" value="anfrage-wohnung">
        <input type="hidden" name="wohnung" value="{a["unit"]}">
        <input type="hidden" name="anreise" data-bind="start">
        <input type="hidden" name="abreise" data-bind="end">
        <input type="hidden" name="gaeste" data-bind="guests">
        <p class="hp"><label>Nicht ausfüllen: <input name="bot-field"></label></p>
        <div class="book-head"><h2>Persönliches Angebot</h2>{book_rating}</div>
        <div class="book-fields">
          <button type="button" data-open="pop-book-cal" data-sheet="sheet-cal"><span class="label">Anreise</span><span class="value" data-show="start" data-empty="Datum">Datum</span></button>
          <button type="button" data-open="pop-book-cal" data-sheet="sheet-cal"><span class="label">Abreise</span><span class="value" data-show="end" data-empty="Datum">Datum</span></button>
          <button class="full" type="button" data-open="pop-book-guests" data-sheet="sheet-guests"><span style="display:grid;gap:1px"><span class="label">Gäste</span><span class="value is-set" data-show="guests">2 Gäste</span></span>{icon("down", 18)}</button>
          <div class="popover popover--cal" id="pop-book-cal">{cal_panel()}</div>
          <div class="popover popover--guests" id="pop-book-guests">{guests_panel(a["guests"], guest_note)}</div>
        </div>
        <div class="book-lines" data-requires-dates hidden>
          <div><span>Aufenthalt</span><span data-show="nights"></span></div>
          <div><span>Preis</span><span>persönlich per Angebot</span></div>
        </div>
        <div class="book-more" inert><div><div class="form">
          <div class="field"><label for="b-name">Name</label><input id="b-name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="b-mail">E-Mail</label><input id="b-mail" name="email" type="email" autocomplete="email" required></div>
          <div class="field"><label for="b-msg">Nachricht <span class="muted">(optional)</span></label><textarea id="b-msg" name="nachricht" rows="3" style="min-height:90px" placeholder="Anreisezeit, Babybett …"></textarea></div>
          <label class="check"><input type="checkbox" name="datenschutz" required><span>Einverstanden mit der Verarbeitung gemäß <a class="u-link" href="{P}datenschutz/">Datenschutz</a>.</span></label>
        </div></div></div>
        <button class="btn btn--accent btn--lg btn--block" type="submit" data-book-next><span class="btn-label">Verfügbarkeit anfragen</span></button>
        <p class="book-note">Unverbindlich · noch keine Zahlung</p>
        {status_box()}
      </form>
      <div class="book-alt">{icon("phone", 20)}<span>Lieber sprechen? <a class="u-link" href="tel:{PHONE}">{PHONE_LABEL}</a></span></div>
    </aside>
  </div>
</main>

<section class="section" aria-labelledby="more-title">
  <div class="container">
    <div class="sec-head"><div><span class="kicker">Noch nicht das Richtige?</span><h2 id="more-title">{more_title}</h2></div>
      <a class="btn btn--light" href="{P}{city_path}">Alle in {city_name} {icon("arrow", 16, "go")}</a></div>
    <div class="listings">
{sims}
    </div>
  </div>
</section>

{footer(P)}

<div class="mobile-bar">
  <div><strong>Persönliches Angebot</strong><button class="dates" type="button" data-open="pop-none" data-sheet="sheet-cal"><span data-show="range" data-empty="Zeitraum wählen">Zeitraum wählen</span></button></div>
  <a class="btn btn--accent" href="#buchen">Anfragen</a>
</div>

{sheets(a["guests"], guest_note)}

<dialog class="lightbox" aria-label="Fotos" data-photos="{photos_json}">
  <div class="lb-top"><span class="lb-count">1 / {len(slots)}</span><button class="icon-btn" type="button" data-lb-close aria-label="Schließen">{icon("x", 16)}</button></div>
  <div class="lb-stage"><div><img src="" alt=""><p class="lb-caption"></p></div></div>
  <div class="lb-bottom"><button class="icon-btn" type="button" data-lb-prev aria-label="Vorheriges Foto">{icon("left", 16)}</button><button class="icon-btn" type="button" data-lb-next aria-label="Nächstes Foto">{icon("right", 16)}</button></div>
</dialog>
<script src="{P}js/main.js" defer></script>
</body>
</html>
"""
