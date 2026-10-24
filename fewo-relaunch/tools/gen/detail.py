import json
from parts import *

P = "../../"

GALLERY = [
    ("int-living-2", "Wohnbereich mit Küchenzeile und Sitzecke"),
    ("int-bedroom-2", "Schlafzimmer mit Doppelbett"),
    ("wue-bridge", "Die Alte Mainbrücke, wenige Gehminuten von der Wohnung"),
    ("int-bath-1", "Bad mit Dusche"),
    ("wue-main", "Mainufer mit Blick auf die Festung Marienberg"),
]

FAQ = [
    ("Wo parke ich in der Nähe?", "Kostenlos parken Sie auf der Talavera am Mainufer. Zum Ausladen können Sie kurz vor dem Haus halten – sprechen Sie uns gern an."),
    ("Gibt es einen Aufzug?", "Nein. Die Wohnung liegt im 2. Stock eines historischen Altstadthauses ohne Aufzug."),
    ("Für wie viele Personen ist die Wohnung geeignet?", "Für 2 bis 4 Personen: Im Schlafzimmer steht ein Doppelbett, im Wohnzimmer eine ausziehbare Schlafcouch. Ein Babybett ist vorhanden."),
    ("Sind Haustiere erlaubt?", "In dieser Wohnung leider nicht. Mit Hund empfehlen wir unsere Ferienwohnungen in Thüngen – dort sind Hunde willkommen."),
]

JSONLD = json.dumps({
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "VacationRental", "@id": "https://www.fewo-urlaub.com/wuerzburg/altstadt/#rental",
         "name": "Das Herzstück der Altstadt – Ferienwohnung im Tilman-Riemenschneider-Haus",
         "description": "Ferienwohnung in der Würzburger Altstadt zwischen Dom und Alter Mainbrücke, im Haus des Bildhauers Tilman Riemenschneider. 50 m², separates Schlafzimmer, Schlafcouch, Küchenzeile, Bad mit Dusche, Waschmaschine, WLAN.",
         "url": "https://www.fewo-urlaub.com/wuerzburg/altstadt/",
         "image": [f"https://www.fewo-urlaub.com/assets/photos/{s}-1920.jpg" for s, _ in GALLERY],
         "telephone": "+49 9360 99183",
         "address": {"@type": "PostalAddress", "streetAddress": "Franziskanergasse 1A", "postalCode": "97070", "addressLocality": "Würzburg", "addressRegion": "Bayern", "addressCountry": "DE"},
         "checkinTime": "15:00", "checkoutTime": "11:00", "petsAllowed": False,
         "containsPlace": {"@type": "Accommodation", "additionalType": "EntirePlace",
                           "floorSize": {"@type": "QuantitativeValue", "value": 50, "unitCode": "MTK"},
                           "numberOfBedrooms": 1, "numberOfBathroomsTotal": 1,
                           "occupancy": {"@type": "QuantitativeValue", "minValue": 2, "maxValue": 4}, "floorLevel": "2",
                           "bed": [{"@type": "BedDetails", "typeOfBed": "Doppelbett", "numberOfBeds": 1}, {"@type": "BedDetails", "typeOfBed": "Schlafcouch", "numberOfBeds": 1}],
                           "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": n, "value": v} for n, v in
                                              [("wifi", True), ("tv", True), ("kitchen", True), ("washerDryer", True), ("crib", True), ("elevator", False), ("petsAllowed", False)]]},
         "provider": {"@id": "https://www.fewo-urlaub.com/#host"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Ferienwohnungen", "item": "https://www.fewo-urlaub.com/"},
            {"@type": "ListItem", "position": 2, "name": "Das Herzstück der Altstadt", "item": "https://www.fewo-urlaub.com/wuerzburg/altstadt/"}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
    ],
}, ensure_ascii=False, indent=2)

AMEN = [
    ("wifi", "Kostenloses WLAN", ""), ("kitchen", "Küchenzeile mit Kochfeld &amp; Kühlschrank", ""),
    ("bed", "Schlafzimmer mit Doppelbett", ""), ("sofa", "Ausziehbare Schlafcouch", ""),
    ("shower", "Bad mit Dusche &amp; Föhn", ""), ("washer", "Waschmaschine", ""),
    ("tv", "Flat-TV", "extra"), ("baby", "Babybett auf Anfrage", "extra"),
    ("key", "Selbstständige Schlüsselübergabe nach Absprache", "extra"),
    ("stairs", "Kein Aufzug (2. Stock)", "no extra"), ("nopaw", "Keine Haustiere", "no extra"),
]


def build():
    photos_json = json.dumps([{"src": f"{P}assets/photos/{s}-1920.jpg", "alt": a} for s, a in GALLERY], ensure_ascii=False).replace('"', "&quot;")
    grid = "".join(
        f'<button type="button" data-photo="{i}" aria-label="Foto vergrößern: {a}">{img(P, s, a, "(min-width: 760px) 50vw, 100vw" if i == 0 else "25vw", eager=(i == 0))}</button>'
        for i, (s, a) in enumerate(GALLERY)
    )
    mobile = slider(P, GALLERY, "100vw")
    amen = "".join(f'<li class="{c}">{icon(i, 24)}<span>{t}</span></li>' for i, t, c in AMEN)
    faq = "".join(
        f'<details name="faq"{" open" if i == 0 else ""}><summary>{q}{icon("down", 18)}</summary><div class="answer">{a}</div></details>'
        for i, (q, a) in enumerate(FAQ)
    )
    return f"""{head(P, "Ferienwohnung Würzburg Altstadt im Riemenschneider-Haus | 50 m², 2–4 Gäste", "Ferienwohnung mitten in der Würzburger Altstadt, im Haus von Tilman Riemenschneider zwischen Dom und Alter Mainbrücke. 50 m², 2–4 Gäste, WLAN, Waschmaschine. Direkt beim Gastgeber anfragen.", "https://www.fewo-urlaub.com/wuerzburg/altstadt/", "int-living-2", JSONLD)}
<body data-max-guests="4" class="has-mobile-bar">
{sprite()}
<a class="skip-link" href="#main">Zum Inhalt springen</a>
{header(P, "wue")}

<main id="main" class="container">
  <div class="detail-head">
    <nav class="crumbs" aria-label="Brotkrumen"><a href="{P}">Ferienwohnungen</a>{icon("right", 14)}<a href="{P}#orte">Würzburg</a>{icon("right", 14)}<span aria-current="page">Das Herzstück der Altstadt</span></nav>
    <div class="detail-title">
      <div>
        <h1>Das Herzstück der Altstadt</h1>
        <div class="detail-meta"><span class="rating">{icon("star", 14)} 9,6 · FeWo-direkt</span><span>Franziskanergasse 1A, Würzburg</span><span>Im Riemenschneider-Haus</span></div>
      </div>
      <div class="title-actions">
        <button class="text-btn" type="button" data-share>{icon("share", 18)}<span>Teilen</span></button>
        <button class="text-btn save-inline" type="button" data-save="wue-altstadt" aria-pressed="false">{icon("heart", 18)}<span>Merken</span></button>
      </div>
    </div>
  </div>

  <div class="gallery">
    <div class="gallery-grid">{grid}</div>
    <button class="btn btn--light btn--sm show-all" type="button" data-photo="0">{icon("grid", 16)} Alle Fotos</button>
    <div class="gallery-mobile">{mobile}<span class="gallery-count">1 / {len(GALLERY)}</span></div>
  </div>

  <div class="detail-layout">
    <div class="detail-main">
      <section class="summary">
        <h2>Ganze Wohnung in der Würzburger Altstadt</h2>
        <p class="muted">2–4 Gäste · 1 Schlafzimmer · Doppelbett + Schlafcouch · 1 Bad · 50 m²</p>
        <div class="score-box">
          <div class="big">9,6<small>von 10</small></div>
          <p><strong>Sehr gut bewertet auf FeWo-direkt.</strong><br>Mitten in der Altstadt, im Haus von Tilman Riemenschneider.</p>
          {icon("sparkle", 28)}
        </div>
      </section>

      <section>
        <div class="host-row"><div class="avatars" aria-hidden="true"><span>C</span><span>S</span></div><div><strong>Ihre Gastgeber: Carolin &amp; Stefan</strong><div class="muted" style="font-size:.92rem">Familienbetrieb aus Thüngen · antworten persönlich</div></div></div>
      </section>

      <section>
        <div class="feature-list">
          <div class="feature">{icon("church", 26)}<div><strong>Wohnen mit Geschichte</strong><p>Der Bildhauer Tilman Riemenschneider lebte von 1483 bis 1531 in diesem Haus.</p></div></div>
          <div class="feature">{icon("walk", 26)}<div><strong>Alles zu Fuß erreichbar</strong><p>Dom, Marktplatz und Alte Mainbrücke liegen wenige Gehminuten entfernt.</p></div></div>
          <div class="feature">{icon("car", 26)}<div><strong>Kostenlos parken</strong><p>Auf der Talavera am Mainufer – ohne Parkhausgebühren.</p></div></div>
        </div>
      </section>

      <section aria-labelledby="h-about">
        <h2 id="h-about">Über die Wohnung</h2>
        <div class="readmore" id="about">
          <p>Aus der Haustür, um die Ecke – und Sie stehen vor dem Dom. Ein paar Schritte weiter wartet die Alte Mainbrücke mit Blick auf die Festung Marienberg. Marktplatz, Weinstuben, Residenz: Alles liegt auf Ihrem Weg, nichts braucht ein Auto.</p>
          <p>Die Wohnung selbst ist ein ruhiger Rückzugsort in einer Seitengasse: ein separates Schlafzimmer mit Doppelbett, ein Wohnzimmer mit ausziehbarer Schlafcouch, eine Küchenzeile mit Kochfeld und Kühlschrank und ein Bad mit Dusche. Dazu Waschmaschine, WLAN und Flat-TV – für ein Wochenende genauso gut wie für eine ganze Woche.</p>
          <p>Die Wohnung liegt im 2. Stock eines historischen Altstadthauses ohne Aufzug. Kinder sind herzlich willkommen, ein Babybett steht bereit. Haustiere sind hier leider nicht erlaubt – mit Hund empfehlen wir unsere Wohnungen in Thüngen.</p>
        </div>
        <button class="text-btn readmore-btn" type="button" data-readmore="about"><span>Mehr anzeigen</span>{icon("right", 16)}</button>
      </section>

      <section aria-labelledby="h-rooms">
        <h2 id="h-rooms">Wo Sie schlafen</h2>
        <div class="rooms">
          <div class="room">{img(P, "int-bedroom-2", "Schlafzimmer mit Doppelbett", "300px")}<strong>Schlafzimmer</strong><span>1 Doppelbett</span></div>
          <div class="room">{img(P, "int-living-2", "Wohnzimmer mit Schlafcouch", "300px")}<strong>Wohnzimmer</strong><span>1 Schlafcouch für 2</span></div>
        </div>
      </section>

      <section aria-labelledby="h-amen">
        <h2 id="h-amen">Was die Wohnung bietet</h2>
        <ul class="amenities" id="amen">{amen}</ul>
        <button class="btn btn--light" type="button" data-amenities="amen">Alle 11 Merkmale anzeigen</button>
      </section>

      <section aria-labelledby="h-cal" id="kalender">
        <h2 id="h-cal" style="margin-bottom:4px"><span data-show="nights" data-empty="Zeitraum wählen">Zeitraum wählen</span></h2>
        <p class="muted" style="margin-bottom:20px"><span data-show="range" data-empty="Wählen Sie An- und Abreise – wir prüfen die Verfügbarkeit persönlich.">Wählen Sie An- und Abreise</span></p>
        <div class="cal two" data-cal></div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:16px"><button class="text-btn" type="button" data-clear-dates><span>Daten löschen</span></button><a class="btn btn--sm" href="#buchen" data-requires-dates hidden>Weiter zur Anfrage {icon("arrow", 16, "go")}</a></div>
      </section>

      <section aria-labelledby="h-lage" id="lage">
        <h2 id="h-lage">Lage</h2>
        <p class="muted" style="margin:-8px 0 20px">Franziskanergasse 1A, 97070 Würzburg – mitten in der Altstadt, in einer ruhigen Seitengasse.</p>
        <figure class="map-card" style="margin:0">
          <svg viewBox="0 0 800 440" role="img" aria-label="Schematische Karte der Würzburger Altstadt mit Lage der Ferienwohnung">
            <rect width="800" height="440" fill="#ece7dd"/>
            <path d="M0 0h185c-18 90-8 170 10 240 16 72 8 140-10 200H0z" fill="#dfe3d0"/>
            <g stroke="#cfd6bb" stroke-width="3" fill="none" stroke-linecap="round"><path d="M20 40c40 10 90 0 130 20M15 90c50 8 100-2 150 16M18 140c50 10 100 0 148 18M25 320c45 6 95-4 140 12M20 370c50 8 100-4 150 14"/></g>
            <path d="M258 -10c-32 108-22 196 8 284 22 70 18 124-4 176" stroke="#c3d2d0" stroke-width="58" fill="none" stroke-linecap="round"/>
            <path d="M330 40c160-30 330-10 420 60 40 120 30 240-40 320-140 36-280 26-380-10z" fill="#e6dfd2" stroke="#ddd4c4" stroke-width="10"/>
            <g stroke="#fbfaf8" stroke-linecap="round"><path d="M236 218H640" stroke-width="10"/><path d="M470 60v350M360 120l250 210M560 90 420 370" stroke-width="7"/></g>
            <rect x="212" y="208" width="90" height="20" rx="4" fill="#cdb79a"/>
            <g font-family="Jakarta, sans-serif" font-size="13" font-weight="600" fill="#3b3730">
              <g transform="translate(92 196)"><circle r="8" fill="#fff" stroke="#3b3730" stroke-width="2"/><text x="-56" y="28">Festung Marienberg</text></g>
              <g transform="translate(257 186)"><circle r="7" fill="#fff" stroke="#3b3730" stroke-width="2"/><text x="-52" y="-14">Alte Mainbrücke</text></g>
              <g transform="translate(470 136)"><circle r="7" fill="#fff" stroke="#3b3730" stroke-width="2"/><text x="14" y="5">Marktplatz</text></g>
              <g transform="translate(520 212)"><circle r="7" fill="#fff" stroke="#3b3730" stroke-width="2"/><text x="14" y="-8">Dom St. Kilian</text></g>
              <g transform="translate(688 200)"><circle r="7" fill="#fff" stroke="#3b3730" stroke-width="2"/><text x="-30" y="28">Residenz</text></g>
              <g transform="translate(70 66)"><circle r="7" fill="#fff" stroke="#3b3730" stroke-width="2"/><text x="14" y="5">Talavera (P)</text></g>
            </g>
            <g transform="translate(470 278)">
              <circle class="pulse" r="16" fill="#1f3b2d" opacity=".35"/>
              <g class="pin"><path d="M0 0c-16-18-22-28-22-38a22 22 0 0 1 44 0c0 10-6 20-22 38z" fill="#1f3b2d"/><circle cy="-38" r="8" fill="#fff"/></g>
              <g transform="translate(30 -54)"><rect width="168" height="48" rx="14" fill="#fff" filter="drop-shadow(0 6px 14px rgba(22,20,15,.16))"/>
                <text x="16" y="21" font-family="Jakarta, sans-serif" font-size="13" font-weight="700" fill="#16140f">Ihre Wohnung</text>
                <text x="16" y="37" font-family="Jakarta, sans-serif" font-size="11.5" fill="#736d64">Franziskanergasse 1A</text></g>
            </g>
          </svg>
          <span class="map-tag">Schematisch, nicht maßstabsgetreu</span>
          <div class="map-actions">
            <button class="btn btn--light btn--sm" type="button" data-copy="Franziskanergasse 1A, 97070 Würzburg" data-toast="Adresse kopiert">{icon("copy", 16)} Adresse</button>
            <a class="btn btn--sm" href="https://www.openstreetmap.org/search?query=Franziskanergasse%201A%2C%2097070%20W%C3%BCrzburg" target="_blank" rel="noopener">Route {icon("arrow", 14, "go")}</a>
          </div>
        </figure>
        <ul class="distances">
          <li><span>Dom St. Kilian</span><span>ca. 300 m</span></li>
          <li><span>Alte Mainbrücke</span><span>ca. 400 m</span></li>
          <li><span>Marktplatz</span><span>ca. 500 m</span></li>
          <li><span>Residenz (UNESCO)</span><span>ca. 900 m</span></li>
          <li><span>Hauptbahnhof</span><span>ca. 1,5 km</span></li>
          <li><span>Parken Talavera</span><span>ca. 1,5 km</span></li>
        </ul>
      </section>

      <section aria-labelledby="h-haus">
        <h2 id="h-haus">Die Geschichte des Hauses</h2>
        <div class="history">
          {img(P, "wue-festung", "Würzburg mit Festung Marienberg", "220px")}
          <div>
            <div class="year">1483</div>
            <p>In diesem Jahr zog der Bildhauer und Holzschnitzer <strong>Tilman Riemenschneider</strong> in das Haus an der Franziskanergasse. Hier lebte er fast fünfzig Jahre, hier betrieb er seine Werkstatt, hier starb er 1531.</p>
            <p class="muted">Ein Holzbildhauer – und heute eine Wohnung, eingerichtet von einer Familie, die seit Generationen mit Eichenholz arbeitet. Wir finden: Das passt.</p>
          </div>
        </div>
      </section>

      <section aria-labelledby="h-rules">
        <h2 id="h-rules">Gut zu wissen</h2>
        <div class="rules">
          <div><h3>Anreise &amp; Abreise</h3><ul><li>Check-in ab 15:00 Uhr</li><li>Check-out bis 11:00 Uhr</li><li>Schlüsselübergabe nach Absprache</li></ul></div>
          <div><h3>Hausregeln</h3><ul><li>Maximal 4 Gäste</li><li>Keine Haustiere</li><li>Kinder willkommen</li></ul></div>
          <div><h3>Das Haus</h3><ul><li>2. Stock, kein Aufzug</li><li>Ruhige Seitengasse</li><li>Babybett vorhanden</li></ul></div>
        </div>
      </section>

      <section aria-labelledby="h-faq" id="faq">
        <h2 id="h-faq">Häufige Fragen</h2>
        <div class="faq">{faq}</div>
      </section>
    </div>

    <!-- Buchungskarte -->
    <aside class="book" id="buchen" aria-label="Verfügbarkeit anfragen">
      <form class="book-card" name="anfrage-wuerzburg" method="POST" data-netlify="true" netlify-honeypot="bot-field" data-inquiry data-book novalidate>
        <input type="hidden" name="form-name" value="anfrage-wuerzburg">
        <input type="hidden" name="wohnung" value="Würzburg – Das Herzstück der Altstadt">
        <input type="hidden" name="anreise" data-bind="start">
        <input type="hidden" name="abreise" data-bind="end">
        <input type="hidden" name="gaeste" data-bind="guests">
        <p class="hp"><label>Nicht ausfüllen: <input name="bot-field"></label></p>
        <div class="book-head"><h2>Persönliches Angebot</h2><span class="rating">{icon("star", 13)} 9,6</span></div>
        <div class="book-fields">
          <button type="button" data-open="pop-book-cal" data-sheet="sheet-cal"><span class="label">Anreise</span><span class="value" data-show="start" data-empty="Datum">Datum</span></button>
          <button type="button" data-open="pop-book-cal" data-sheet="sheet-cal"><span class="label">Abreise</span><span class="value" data-show="end" data-empty="Datum">Datum</span></button>
          <button class="full" type="button" data-open="pop-book-guests" data-sheet="sheet-guests"><span style="display:grid;gap:1px"><span class="label">Gäste</span><span class="value is-set" data-show="guests">2 Gäste</span></span>{icon("down", 18)}</button>
          <div class="popover popover--cal" id="pop-book-cal">{cal_panel()}</div>
          <div class="popover popover--guests" id="pop-book-guests">{guests_panel(4, "Maximal 4 Gäste. Kleinkinder zählen nicht mit.")}</div>
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
      <div class="book-alt">{icon("phone", 20)}<span>Lieber sprechen? <a class="u-link" href="tel:+49936099183">09360 99183</a></span></div>
    </aside>
  </div>
</main>

<section class="section" aria-labelledby="more-title">
  <div class="container">
    <div class="sec-head"><div><span class="kicker">Mit Hund oder mehr Platz?</span><h2 id="more-title">Ruhiger wohnen in Thüngen.</h2></div>
      <a class="btn btn--light" href="{P}#unterkuenfte">Alle Unterkünfte {icon("arrow", 16, "go")}</a></div>
    <div class="places">
      <article class="place reveal">
        {img(P, "thue-schloss", "Schloss Thüngen", "(min-width: 900px) 50vw, 100vw")}
        <div class="place-body"><span class="kicker" style="color:rgba(255,255,255,.8)">Thüngen · Schlossberg</span><h3>Vier Wohnungen mit Platz für bis zu sechs.</h3><p>Hunde willkommen, Parken am Haus, Weinberge vor der Tür.</p><a class="btn btn--white" href="{P}#unterkuenfte">Wohnungen ansehen {icon("arrow", 16, "go")}</a></div>
      </article>
      <article class="place reveal" style="--d:.08s">
        {img(P, "wue-residenz", "Würzburger Residenz mit Hofgarten", "(min-width: 900px) 50vw, 100vw")}
        <div class="place-body"><span class="kicker" style="color:rgba(255,255,255,.8)">Ausflüge</span><h3>Residenz, Festung, Weinberge.</h3><p>Unsere Tipps für Würzburg und das Fränkische Weinland.</p><a class="btn btn--white" href="{P}#region">Zu den Tipps {icon("arrow", 16, "go")}</a></div>
      </article>
    </div>
  </div>
</section>

{footer(P)}

<div class="mobile-bar">
  <div><strong>Persönliches Angebot</strong><button class="dates" type="button" data-open="pop-none" data-sheet="sheet-cal"><span data-show="range" data-empty="Zeitraum wählen">Zeitraum wählen</span></button></div>
  <a class="btn btn--accent" href="#buchen">Anfragen</a>
</div>

{sheets(4, "Maximal 4 Gäste. Kleinkinder zählen nicht mit.")}

<dialog class="lightbox" aria-label="Fotos" data-photos="{photos_json}">
  <div class="lb-top"><span class="lb-count">1 / {len(GALLERY)}</span><button class="icon-btn" type="button" data-lb-close aria-label="Schließen">{icon("x", 16)}</button></div>
  <div class="lb-stage"><div><img src="" alt=""><p class="lb-caption"></p></div></div>
  <div class="lb-bottom"><button class="icon-btn" type="button" data-lb-prev aria-label="Vorheriges Foto">{icon("left", 16)}</button><button class="icon-btn" type="button" data-lb-next aria-label="Nächstes Foto">{icon("right", 16)}</button></div>
</dialog>
<script src="{P}js/main.js" defer></script>
</body>
</html>
"""
