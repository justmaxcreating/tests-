import json
from parts import *

P = ""

LISTINGS = [
    dict(id="wue-altstadt", href="wuerzburg/altstadt/", place="Würzburg · Altstadt", name="Das Herzstück der Altstadt",
         facts="50 m² · 1 Schlafzimmer · 2–4 Gäste", rating="9,6", rating_title="FeWo-direkt", badge="Im Riemenschneider-Haus",
         tags="wuerzburg familie", cta="Wohnung ansehen",
         photos=[("int-living-2", "Wohnbereich mit Küchenzeile"), ("int-bath-1", "Bad mit Dusche"), ("wue-bridge", "Alte Mainbrücke, wenige Gehminuten entfernt")]),
    dict(id="thue-elefant", unit="Thüngen – Elefant", place="Thüngen · Schlossberg", name="Elefant",
         facts="65 m² · bis 6 Gäste · Hund willkommen", rating="9,1", rating_title="Booking.com, Wohnen am Schlossberg", badge="Hunde willkommen",
         tags="thuengen hund familie gruppe", cta="Anfragen",
         photos=[("int-living-3", "Wohnzimmer mit Parkett"), ("int-kitchen-1", "Küche"), ("thue-schloss", "Schloss Thüngen, um die Ecke")]),
    dict(id="thue-zebra", unit="Thüngen – Zebra", place="Thüngen · Schlossberg", name="Zebra",
         facts="65 m² · bis 6 Gäste · Hund willkommen", rating="9,1", rating_title="Booking.com, Wohnen am Schlossberg", badge="",
         tags="thuengen hund familie gruppe", cta="Anfragen",
         photos=[("int-living-1", "Wohnzimmer"), ("int-dining-1", "Essbereich"), ("wein-stein", "Weinberge im Fränkischen Weinland")]),
    dict(id="thue-giraffe", unit="Thüngen – Giraffe", place="Thüngen · Schlossberg", name="Giraffe",
         facts="65 m² · bis 4 Gäste · Hund willkommen", rating="9,1", rating_title="Booking.com, Wohnen am Schlossberg", badge="",
         tags="thuengen hund familie", cta="Anfragen",
         photos=[("int-bedroom-1", "Wohnbereich"), ("int-bath-1", "Bad"), ("thue-schloss", "Schloss Thüngen")]),
    dict(id="thue-blauer-reiter", unit="Thüngen – Blauer Reiter", place="Thüngen · Haus Kämpf", name="Blauer Reiter",
         facts="65 m² · Schlafzimmer mit Doppelbett", rating="9,1", rating_title="Booking.com, Wohnen am Schlossberg", badge="Eichen-Unikate",
         tags="thuengen hund", cta="Anfragen",
         photos=[("int-bedroom-2", "Schlafzimmer mit Doppelbett"), ("oak-wood", "Eichenholz aus dem eigenen Sägewerk"), ("wein-stein", "Weinberge")]),
]

SIZES_CARD = "(min-width: 1100px) 400px, (min-width: 640px) 50vw, 100vw"


def card(l):
    badge = f'<span class="badge">{l["badge"]}</span>' if l["badge"] else ""
    extra = badge + f'<button class="save-btn" type="button" data-save="{l["id"]}" aria-label="{l["name"]} merken" aria-pressed="false">{HEART}</button>'
    if l.get("href"):
        cover = f'<a class="cover" href="{l["href"]}" aria-label="{l["name"]} ansehen"></a>'
    else:
        cover = f'<a class="cover" href="#anfrage" data-unit="{l["unit"]}" aria-label="{l["name"]} anfragen"></a>'
    return f"""<article class="listing reveal" data-tags="{l["tags"]}">
  {cover}
  {slider(P, l["photos"], SIZES_CARD, extra)}
  <div class="listing-body">
    <div class="listing-top"><h3>{l["name"]}</h3><span class="rating" title="{l["rating_title"]}">{icon("star", 13)} {l["rating"]}</span></div>
    <p>{l["place"]}</p>
    <p class="facts">{l["facts"]}</p>
    <p class="listing-cta"><strong>{l["cta"]}</strong> · Preis auf Anfrage</p>
  </div>
</article>"""


REGION = [
    ("wue-residenz", "Residenz Würzburg", "UNESCO-Welterbe mit Tiepolos berühmtem Deckenfresko."),
    ("wue-bridge", "Brückenschoppen", "Ein Glas Silvaner auf der Alten Mainbrücke, die Festung im Abendlicht."),
    ("wue-festung", "Festung Marienberg", "Hoch über der Stadt – der schönste Blick auf Würzburg."),
    ("wein-stein", "Würzburger Stein", "Weinwandern zwischen den Steillagen direkt über dem Main."),
    ("wue-main", "Am Mainufer", "Spazieren, Schiffe schauen, Radeln am Main-Radweg."),
    ("thue-schloss", "Schloss Thüngen", "Ruhig, ländlich, mitten im Fränkischen Weinland."),
]

# Bewertungen: nur belegbare Angaben. Echte Gästezitate später in "quote" eintragen
# (z. B. mit Einverständnis aus Booking.com/FeWo-direkt übernommen), "summary" dann auf False setzen.
REVIEWS = [
    dict(score="9,1", source="Booking.com", place="Wohnen am Schlossberg, Thüngen", count="26 Bewertungen",
         quote="Besonders oft gelobt: die Gastgeber.", summary=True),
    dict(score="9,6", source="FeWo-direkt", place="Tilman-Riemenschneider-Haus, Würzburg", count="",
         quote="Für die Altstadtwohnung im Haus des Bildhauers Tilman Riemenschneider.", summary=False),
    dict(score="8,6", source="Gîtes.fr", place="Wohnen am Schlossberg, Thüngen", count="34 Bewertungen",
         quote="Auch auf dem französischen Ferienportal gut bewertet.", summary=False),
]
MARQUEE = ["Check-in ab 15 Uhr", "Hunde in Thüngen willkommen", "Kostenloses WLAN", "Parken am Haus in Thüngen",
           "Babybett in Würzburg", "Persönliche Schlüsselübergabe", "Möbel aus eigener Eiche", "Direkt beim Gastgeber"]

FAQ = [
    ("Wann kann ich anreisen und abreisen?", "Check-in ist ab 15 Uhr, Check-out bis 11 Uhr. Kommen Sie später an, sagen Sie uns einfach Bescheid – wir stimmen die Schlüsselübergabe mit Ihnen ab."),
    ("Darf mein Hund mit?", "In unseren Ferienwohnungen in Thüngen sind Hunde herzlich willkommen. In der Altstadtwohnung in Würzburg sind Haustiere leider nicht erlaubt."),
    ("Wo parke ich in Würzburg?", "Kostenlos parken Sie auf der Talavera am Mainufer. Von dort sind es wenige Minuten zu Fuß in die Altstadt."),
    ("Sind Kinder willkommen?", "Sehr gern. In Würzburg steht ein Babybett bereit, in Thüngen haben die größeren Wohnungen Platz für bis zu sechs Personen."),
    ("Wie funktioniert die Buchung?", "Sie senden uns eine unverbindliche Anfrage mit Wunschzeitraum. Wir melden uns persönlich mit Verfügbarkeit und Preis. Erst wenn Sie zusagen, ist die Buchung fest."),
    ("Gibt es WLAN?", "Ja, in allen Ferienwohnungen gibt es kostenloses WLAN."),
]

JSONLD = json.dumps({
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "WebSite", "@id": "https://www.fewo-urlaub.com/#website", "url": "https://www.fewo-urlaub.com/", "name": "Ferienwohnungen Voll", "inLanguage": "de-DE", "publisher": {"@id": "https://www.fewo-urlaub.com/#host"}},
        {"@type": "LodgingBusiness", "@id": "https://www.fewo-urlaub.com/#host", "name": "Ferienwohnungen Voll – Würzburg & Thüngen", "url": "https://www.fewo-urlaub.com/",
         "telephone": "+49 9360 99183", "image": "https://www.fewo-urlaub.com/assets/photos/wue-hero-1920.jpg",
         "address": {"@type": "PostalAddress", "streetAddress": "Gartenstraße 11", "postalCode": "97289", "addressLocality": "Thüngen", "addressRegion": "Bayern", "addressCountry": "DE"},
         "checkinTime": "15:00", "checkoutTime": "11:00", "petsAllowed": "Hunde in den Ferienwohnungen in Thüngen willkommen",
         "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": "Kostenloses WLAN", "value": True}, {"@type": "LocationFeatureSpecification", "name": "Kostenlose Parkplätze am Haus (Thüngen)", "value": True}],
         "founder": [{"@type": "Person", "name": "Carolin Voll"}, {"@type": "Person", "name": "Stefan Voll"}], "sameAs": ["https://hugokaempf.de/"]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
    ],
}, ensure_ascii=False, indent=2)


def review_card(r):
    note = '<span class="rv-note">Zusammenfassung</span>' if r.get("summary") else ""
    count = f' · {r["count"]}' if r["count"] else ""
    return f"""            <figure class="rv-card">
              <div class="rv-score"><strong>{r["score"]}</strong><span>/ 10</span>{icon("star", 14)}</div>
              <blockquote>{r["quote"]}</blockquote>
              <figcaption><span class="rv-src">{r["source"][0]}</span><span><strong>{r["source"]}</strong><br>{r["place"]}{count}</span>{note}</figcaption>
            </figure>"""


def build():
    cards = "\n".join(card(l) for l in LISTINGS)
    reviews = "\n".join(review_card(r) for r in REVIEWS)
    marquee = "".join(f'<span>{icon("check", 16)}{m}</span>' for m in MARQUEE * 2)
    marquee_label = "Auf einen Blick: " + ", ".join(MARQUEE)
    region = "\n".join(
        f'<article class="tile zoom">{img(P, s, t, "300px")}<h3>{t}</h3><p>{d}</p></article>' for s, t, d in REGION
    )
    faq = "\n".join(
        f'<details name="faq"{" open" if i == 0 else ""}><summary>{q}{icon("down", 18)}</summary><div class="answer">{a}</div></details>'
        for i, (q, a) in enumerate(FAQ)
    )
    return f"""{head(P, "Ferienwohnungen Würzburg Altstadt &amp; Thüngen | Direkt beim Gastgeber", "Ferienwohnungen mitten in der Würzburger Altstadt und am Schlossberg in Thüngen. Eingerichtet mit Eiche aus dem eigenen Sägewerk, Hunde in Thüngen willkommen. Direkt beim Gastgeber anfragen.", "https://www.fewo-urlaub.com/", "wue-hero", JSONLD)}
<body data-max-guests="6">
{sprite()}
<a class="skip-link" href="#main">Zum Inhalt springen</a>
{header(P, "home")}

<main id="main">
  <!-- HERO -->
  <section class="hero" aria-labelledby="hero-title">
    <div class="hero-frame">
      {img(P, "wue-hero", "Blick von der Festung Marienberg auf die Alte Mainbrücke und die Würzburger Altstadt", "100vw", eager=True)}
      <div class="hero-content">
        <span class="kicker">{icon("pin", 16)} Würzburg &amp; Thüngen<span class="hide-sm">&nbsp;· Fränkisches Weinland</span></span>
        <h1 id="hero-title">Franken wohnen.<br>Nicht nur besuchen.</h1>
        <p class="lead">Fünf Ferienwohnungen – mitten in der Würzburger Altstadt oder ruhig am Schlossberg. Persönlich vermietet von einer Familie, die seit Generationen mit Eichenholz arbeitet.</p>
      </div>
    </div>
  </section>

  <div class="search-wrap">
    <form class="search" data-search aria-label="Verfügbarkeit anfragen">
      <label class="search-field">
        <span class="label">Ort</span>
        <span class="value" data-show="place" data-empty="Würzburg oder Thüngen">Würzburg oder Thüngen</span>
        <select name="ort" data-place aria-label="Ort wählen"><option value="">Würzburg oder Thüngen</option><option value="wuerzburg">Würzburg · Altstadt</option><option value="thuengen">Thüngen · Schlossberg</option></select>
      </label>
      <button class="search-field" type="button" data-open="pop-cal" data-sheet="sheet-cal"><span class="label">Anreise</span><span class="value" data-show="start" data-empty="Datum wählen">Datum wählen</span></button>
      <button class="search-field" type="button" data-open="pop-cal" data-sheet="sheet-cal"><span class="label">Abreise</span><span class="value" data-show="end" data-empty="Datum wählen">Datum wählen</span></button>
      <button class="search-field" type="button" data-open="pop-guests" data-sheet="sheet-guests"><span class="label">Gäste</span><span class="value is-set" data-show="guests">2 Gäste</span></button>
      <button class="btn btn--accent" type="submit">{icon("search", 18)} Anfragen</button>
      <div class="popover popover--cal" id="pop-cal" data-after-range="pop-guests">{cal_panel()}</div>
      <div class="popover popover--guests" id="pop-guests">{guests_panel(6, "In Thüngen bis 6, in Würzburg bis 4 Gäste.")}</div>
    </form>
  </div>

  <div class="container">
    <div class="trust">
      <div><strong>{icon("star", 18)} 9,1</strong><span>Booking.com · Thüngen</span></div>
      <div><strong>{icon("star", 18)} 9,6</strong><span>FeWo-direkt · Würzburg</span></div>
      <div><strong>150+ Jahre</strong><span>Familienbetrieb in Thüngen</span></div>
      <div><strong>Direkt</strong><span>ohne Portal-Servicegebühr</span></div>
    </div>
  </div>

  <!-- UNTERKÜNFTE -->
  <section class="section" id="unterkuenfte" aria-labelledby="u-title">
    <div class="container">
      <div class="sec-head">
        <div><span class="kicker">Unsere Unterkünfte</span><h2 id="u-title">Fünf Wohnungen, zwei Welten.</h2></div>
      </div>
      <div class="chips" role="group" aria-label="Unterkünfte filtern">
        <button class="chip" type="button" data-filter="alle" aria-pressed="true">Alle</button>
        <button class="chip" type="button" data-filter="wuerzburg" aria-pressed="false">{icon("church", 16)} Würzburg Altstadt</button>
        <button class="chip" type="button" data-filter="thuengen" aria-pressed="false">{icon("wine", 16)} Thüngen</button>
        <button class="chip" type="button" data-filter="hund" aria-pressed="false">{icon("paw", 16)} Mit Hund</button>
        <button class="chip" type="button" data-filter="familie" aria-pressed="false">{icon("baby", 16)} Für Familien</button>
        <button class="chip" type="button" data-filter="gruppe" aria-pressed="false">{icon("users", 16)} Bis 6 Personen</button>
      </div>
      <p class="filter-count" data-filter-count aria-live="polite"></p>
      <div class="listings">
{cards}
        <aside class="advice reveal" data-tags="wuerzburg thuengen hund familie gruppe">
          <span class="kicker">Unsicher, welche passt?</span>
          <h3>Sagen Sie uns, wer mitkommt. Wir sagen Ihnen, welche Wohnung passt.</h3>
          <p class="muted">Paar auf Städtereise, Familie mit Hund oder Wandergruppe – wir kennen jede Wohnung persönlich.</p>
          <a class="btn btn--light" href="#anfrage">Beratung anfragen {icon("arrow", 16, "go")}</a>
        </aside>
      </div>
    </div>
  </section>

  <!-- ORTE -->
  <section class="section section--flush" id="orte" aria-labelledby="o-title">
    <div class="container">
      <div class="sec-head"><div><span class="kicker">Zwei Orte</span><h2 id="o-title">Stadt am Morgen, Weinberg am Abend.</h2></div>
        <p class="lead" style="max-width:44ch">Würzburg und Thüngen liegen nah beieinander – und fühlen sich doch ganz verschieden an.</p></div>
      <div class="places">
        <article class="place reveal">
          {img(P, "wue-festung", "Festung Marienberg über Würzburg", "(min-width: 900px) 50vw, 100vw")}
          <div class="place-body">
            <span class="kicker" style="color:rgba(255,255,255,.8)">Würzburg · Altstadt</span>
            <h3>Die Altstadt vor der Haustür.</h3>
            <p>Wohnen im Haus, in dem Tilman Riemenschneider lebte – zwischen Dom und Alter Mainbrücke. Das Auto bleibt stehen.</p>
            <div class="place-tags"><span>2–4 Gäste</span><span>50 m²</span><span>Historisches Haus</span></div>
            <a class="btn btn--white" href="wuerzburg/altstadt/">Zur Wohnung {icon("arrow", 16, "go")}</a>
          </div>
        </article>
        <article class="place reveal" style="--d:.08s">
          {img(P, "wein-stein", "Weinberge im Fränkischen Weinland im Herbst", "(min-width: 900px) 50vw, 100vw")}
          <div class="place-body">
            <span class="kicker" style="color:rgba(255,255,255,.8)">Thüngen · Schlossberg</span>
            <h3>Ruhe am Schlossberg, Wein vor der Tür.</h3>
            <p>Vier Wohnungen im Haus Kämpf, nordwestlich von Würzburg. Zu Fuß in die Weinberge, mit dem Rad an den Main.</p>
            <div class="place-tags"><span>Bis 6 Gäste</span><span>Hunde willkommen</span><span>Parken am Haus</span></div>
            <a class="btn btn--white" href="#unterkuenfte" data-filter-link="thuengen">Wohnungen ansehen {icon("arrow", 16, "go")}</a>
          </div>
        </article>
      </div>
    </div>
  </section>

  <!-- EICHE -->
  <section class="section" id="eiche" aria-labelledby="e-title">
    <div class="container story">
      <div class="story-media reveal">
        {img(P, "oak-wood", "Eichenholz aus dem Sägewerk Hugo Kämpf", "(min-width: 960px) 360px, 60vw")}
        {img(P, "thue-schloss", "Thüngen mit Schloss", "(min-width: 960px) 260px, 40vw")}
      </div>
      <div class="story-text reveal" style="--d:.08s">
        <span class="kicker">Hugo Kämpf · Sägewerk in Thüngen</span>
        <h2 id="e-title">Ihr Esstisch hat eine Herkunft. Sie liegt nebenan.</h2>
        <p class="lead">Hinter den Ferienwohnungen steht Hugo Kämpf – ein Sägewerk für Eichenschnittholz, seit Generationen in Thüngen. Tische, Waschtische, Wandverkleidungen aus Altholz: Vieles, was Sie bei uns anfassen, ist hier entstanden.</p>
        <div class="facts-row">
          <div><strong>150+</strong><span>Jahre Eiche aus Thüngen</span></div>
          <div><strong>FSC®</strong><span>zertifizierte Lieferkette seit 2004</span></div>
          <div><strong>Unikate</strong><span>aus eigenem Holz gefertigt</span></div>
        </div>
        <a class="btn btn--light" href="https://hugokaempf.de/" rel="noopener" target="_blank">Das Sägewerk kennenlernen {icon("arrow", 16, "go")}</a>
      </div>
    </div>
  </section>

  <!-- REGION -->
  <section class="section section--flush" id="region" aria-labelledby="r-title">
    <div class="container">
      <div class="sec-head">
        <div><span class="kicker">Ausflüge &amp; Region</span><h2 id="r-title">Was Sie nicht verpassen sollten.</h2></div>
        <div class="scroller-nav" data-scroller="region-track">
          <button class="icon-btn" type="button" aria-label="Zurück">{icon("left", 16)}</button>
          <button class="icon-btn" type="button" aria-label="Weiter">{icon("right", 16)}</button>
        </div>
      </div>
      <div class="scroller" id="region-track">
{region}
      </div>
    </div>
  </section>

  <!-- BEWERTUNGEN (Aufbau nach 21st.dev „Testimonials Section with Logo Marquee“) -->
  <section class="section" aria-labelledby="b-title">
    <div class="container">
      <div class="rv reveal">
        <div class="rv-head">
          <span class="rv-tag">Bewertungen</span>
          <h2 id="b-title">Was Gäste sagen,<br><span class="rv-muted">in Zahlen.</span></h2>
        </div>
        <div class="rv-frame">
          <div class="rv-track" id="rv-track" tabindex="0" aria-label="Bewertungen – mit Pfeiltasten blättern" data-rv>
{reviews}
          </div>
          <div class="rv-nav">
            <button class="icon-btn" type="button" data-rv-prev aria-label="Vorherige Bewertungen">{icon("left", 16)}</button>
            <div class="rv-dots" data-rv-dots></div>
            <button class="icon-btn" type="button" data-rv-next aria-label="Nächste Bewertungen">{icon("right", 16)}</button>
          </div>
        </div>
        <div class="rv-marquee" role="group" aria-label="{marquee_label}">
          <div class="rv-marquee-row" aria-hidden="true">{marquee}</div>
        </div>
      </div>
    </div>
  </section>

  <!-- FAQ -->
  <section class="section section--flush" id="faq" aria-labelledby="f-title">
    <div class="container faq-grid">
      <div class="sec-head" style="display:grid;align-content:start"><div><span class="kicker">Häufige Fragen</span><h2 id="f-title">Gut zu wissen.</h2>
        <p class="muted">Ihre Frage ist nicht dabei? Rufen Sie uns an: <a class="u-link" href="tel:+49936099183">09360 99183</a></p></div></div>
      <div class="faq">
{faq}
      </div>
    </div>
  </section>

  <!-- ANFRAGE -->
  <section class="section" id="anfrage" aria-labelledby="a-title">
    <div class="container inquiry">
      <div style="display:grid;gap:24px">
        <div style="display:grid;gap:12px"><span class="kicker">Direkt beim Gastgeber</span><h2 id="a-title">Wann dürfen wir Sie begrüßen?</h2>
          <p class="lead">Schreiben Sie uns Ihren Wunschzeitraum – wir antworten persönlich mit Verfügbarkeit und Preis.</p></div>
        <div class="host-card">
          <div class="host-head"><div class="avatars" aria-hidden="true"><span>C</span><span>S</span></div><div><strong>Carolin &amp; Stefan Voll</strong><div class="muted" style="font-size:.9rem">Ihre Gastgeber in Würzburg &amp; Thüngen</div></div></div>
          <ul class="host-facts">
            <li>{icon("chat")} Persönliche Antwort, kein Callcenter</li>
            <li>{icon("receipt")} Keine Servicegebühr eines Buchungsportals</li>
            <li>{icon("check")} Unverbindlich – Sie entscheiden nach dem Angebot</li>
          </ul>
          <div class="contact-links">
            <a href="tel:+49936099183"><span><small>Telefon</small>09360 99183</span>{icon("phone", 18)}</a>
            <button type="button" data-copy="Gartenstraße 11, 97289 Thüngen" data-toast="Adresse kopiert"><span><small>Adresse</small>Gartenstraße 11, 97289 Thüngen</span>{icon("copy", 18)}</button>
          </div>
        </div>
      </div>

      <form class="form" id="anfrage-form" name="anfrage" method="POST" data-netlify="true" netlify-honeypot="bot-field" data-inquiry novalidate>
        <input type="hidden" name="form-name" value="anfrage">
        <input type="hidden" name="gaeste" data-bind="guests">
        <p class="hp"><label>Nicht ausfüllen: <input name="bot-field"></label></p>
        <div class="field"><label for="f-unit">Unterkunft</label>
          <select id="f-unit" name="wohnung">
            <option>Noch offen – bitte beraten</option>
            <option>Würzburg – Das Herzstück der Altstadt</option>
            <option>Thüngen – egal welche</option>
            <option>Thüngen – Elefant</option>
            <option>Thüngen – Zebra</option>
            <option>Thüngen – Giraffe</option>
            <option>Thüngen – Blauer Reiter</option>
          </select></div>
        <div class="form-row">
          <div class="field"><label for="f-in">Anreise</label><input id="f-in" name="anreise" type="date" data-bind="start" required></div>
          <div class="field"><label for="f-out">Abreise</label><input id="f-out" name="abreise" type="date" data-bind="end" required></div>
        </div>
        <div class="form-row">
          <div class="field"><span class="label">Gäste</span><button class="field-btn" type="button" data-open="pop-guests-form" data-sheet="sheet-guests" style="display:flex;justify-content:space-between;align-items:center;min-height:52px;padding:0 16px;border-radius:var(--r-md);box-shadow:inset 0 0 0 1px var(--line-strong);background:var(--surface);width:100%"><span data-show="guests">2 Gäste</span>{icon("down", 18)}</button></div>
          <div class="field"><label for="f-dog">Hund dabei?</label><select id="f-dog" name="hund"><option>Nein</option><option>Ja</option></select></div>
        </div>
        <div class="form-row">
          <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="f-mail">E-Mail</label><input id="f-mail" name="email" type="email" autocomplete="email" required></div>
        </div>
        <div class="field"><label for="f-msg">Nachricht <span class="muted">(optional)</span></label><textarea id="f-msg" name="nachricht" placeholder="Anlass, Anreisezeit, besondere Wünsche …"></textarea></div>
        <label class="check"><input type="checkbox" name="datenschutz" required><span>Ich bin einverstanden, dass meine Angaben zur Bearbeitung der Anfrage gespeichert werden (<a class="u-link" href="datenschutz/">Datenschutz</a>).</span></label>
        <button class="btn btn--accent btn--lg btn--block" type="submit">Unverbindlich anfragen {icon("arrow", 18, "go")}</button>
        <p class="form-note">Noch keine Buchung und keine Zahlung. Wir antworten persönlich.</p>
        {status_box()}
      </form>
    </div>
  </section>
</main>

{footer(P)}
{sheets(6, "In Thüngen bis 6, in Würzburg bis 4 Gäste.")}
<script src="js/main.js" defer></script>
</body>
</html>
"""
