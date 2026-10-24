from cards import card
from data import APARTMENTS, BY_ID
from reviews import AS_OF, HOST, SOURCE, UWG_NOTE
from pages import host_card
from parts import *

P = ""

REGION = [
    ("wue-residenz", "Residenz Würzburg", "UNESCO-Welterbe mit Tiepolos berühmtem Deckenfresko.", "ausfluege/#wuerzburg"),
    ("wue-bridge", "Brückenschoppen", "Ein Glas Silvaner auf der Alten Mainbrücke, die Festung im Abendlicht.", "ausfluege/#wuerzburg"),
    ("wue-festung", "Festung Marienberg", "Hoch über der Stadt – der schönste Blick auf Würzburg.", "ausfluege/#wuerzburg"),
    ("veits-hofgarten", "Veitshöchheim", "Mit dem Schiff zum Rokokogarten.", "ausfluege/#wuerzburg"),
    ("thue-werntal", "Werntal", "Wandern und Radeln direkt ab Thüngen.", "ausfluege/#weinland"),
    ("karlstadt-karlsburg", "Karlsburg", "Burgruine hoch über dem Main bei Karlstadt.", "ausfluege/#weinland"),
    ("volkach-mainschleife", "Volkach", "Weindorf an der Mainschleife.", "ausfluege/#weinland"),
]

# Bewertungen: Noten von Booking.com (reviews.py), Text = Zusammenfassung in eigenen Worten, keine Zitate.
# Echte Gästezitate nur mit Einverständnis der Gäste ergänzen.
def review_items():
    seen, items = set(), []
    for a in APARTMENTS:
        rv = a["review"]
        if not rv or rv["url"] in seen:
            continue
        seen.add(rv["url"])
        name = "Wohnen am Schlossberg" if a["city"] == "thuengen" else a["name"]
        path = "thuengen/" if a["city"] == "thuengen" else a["path"]
        q = a["quotes"][0] if a["quotes"] else None
        items.append(dict(score=rv["score"], name=name, place=a["town"], count=rv["count"], path=path, quote=bool(q),
                          who=f"{q[1]} · {q[2]}" if q else "",
                          text=f"„{q[0]}“" if q else f"{rv['praise'][0]}. {rv['praise'][1]}."))
    return sorted(items, key=lambda r: (not r["quote"], -float(r["score"].replace(",", "."))))


MARQUEE = ["Check-in ab 15 Uhr", "Hunde in Thüngen willkommen", "Kostenloses WLAN", "Parken am Haus in Thüngen",
           "Babybett in allen Würzburger Wohnungen", "Waschmaschine in Würzburg", "Möbel aus eigener Eiche", "Direkt beim Gastgeber"]

FAQ = [
    ("Wann kann ich anreisen und abreisen?", "Check-in ist ab 15 Uhr, Check-out bis 11 Uhr. Kommen Sie später an, sagen Sie uns einfach Bescheid – wir stimmen die Schlüsselübergabe mit Ihnen ab."),
    ("Darf mein Hund mit?", "In unseren <a class=\"u-link\" href=\"thuengen/\">Ferienwohnungen in Thüngen</a> sind Hunde herzlich willkommen. In den Würzburger Wohnungen sind Haustiere leider nicht erlaubt."),
    ("Wo parke ich in Würzburg?", "Kostenlos parken Sie auf der Talavera am Mainufer. Von dort sind es wenige Minuten zu Fuß in die Altstadt. Die Wohnung <a class=\"u-link\" href=\"wuerzburg/am-kulturspeicher/\">Am Kulturspeicher</a> hat einen eigenen Parkplatz."),
    ("Wir sind eine große Familie oder Gruppe – welche Wohnung passt?", "In Würzburg die <a class=\"u-link\" href=\"wuerzburg/annastrasse/\">Annastraße</a> für bis zu 8 Personen, in Thüngen die Wohnungen <a class=\"u-link\" href=\"thuengen/elefant/\">Elefant</a> und <a class=\"u-link\" href=\"thuengen/zebra/\">Zebra</a> für bis zu 6."),
    ("Wie funktioniert die Buchung?", "Sie senden uns eine unverbindliche Anfrage mit Wunschzeitraum. Wir melden uns persönlich mit Verfügbarkeit und Preis. Erst wenn Sie zusagen, ist die Buchung fest."),
    ("Gibt es WLAN?", "Ja, in allen Ferienwohnungen gibt es kostenloses WLAN."),
]

JSONLD = [
    {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": "Ferienwohnungen Voll", "inLanguage": "de-DE", "publisher": {"@id": f"{SITE}/#host"}},
    {"@type": "LodgingBusiness", "@id": f"{SITE}/#host", "name": "Ferienwohnungen Voll – Würzburg & Thüngen", "url": f"{SITE}/",
     "telephone": "+49 9360 99183", "image": photo_url("wue-hero"), "priceRange": "Preis auf Anfrage",
     "address": {"@type": "PostalAddress", "streetAddress": "Gartenstraße 11", "postalCode": "97289", "addressLocality": "Thüngen", "addressRegion": "Bayern", "addressCountry": "DE"},
     "areaServed": ["Würzburg", "Thüngen", "Fränkisches Weinland"],
     "checkinTime": "15:00", "checkoutTime": "11:00", "petsAllowed": "Hunde in den Ferienwohnungen in Thüngen willkommen",
     "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": "Kostenloses WLAN", "value": True}, {"@type": "LocationFeatureSpecification", "name": "Kostenlose Parkplätze am Haus (Thüngen)", "value": True}],
     "founder": [{"@type": "Person", "name": "Carolin Voll"}, {"@type": "Person", "name": "Stefan Voll"}], "sameAs": ["https://hugokaempf.de/"]},
    {"@type": "ItemList", "name": "Ferienwohnungen in Würzburg und Thüngen", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": f"{SITE}/{a['path']}", "name": a["name"]} for i, a in enumerate(APARTMENTS)]},
    ld_faq(FAQ),
]


def review_card(r):
    return f"""            <a class="rv-card" href="{r["path"]}">
              <div class="rv-score"><strong>{r["score"]}</strong><span>/ 10</span>{icon("star", 14)}</div>
              <p class="rv-text">{r["text"]}</p>
              <span class="rv-cap"><span class="rv-src">B</span><span><strong>{r["who"] or r["name"]}</strong><br>{r["name"] + " · " if r["who"] else ""}{r["count"]} Bewertungen · {SOURCE}</span>{"" if r["quote"] else '<span class="rv-note">Zusammenfassung</span>'}</span>
            </a>"""


def inquiry_form(prefix):
    """Anfrageformular – auf der Startseite und auf „Anreise & Kontakt“."""
    def opts(city):
        return "".join(f"<option>{a['unit']}</option>" for a in APARTMENTS if a["city"] == city)

    return f"""<form class="form" id="anfrage-form" name="anfrage" method="POST" data-netlify="true" netlify-honeypot="bot-field" data-inquiry novalidate>
        <input type="hidden" name="form-name" value="anfrage">
        <input type="hidden" name="gaeste" data-bind="guests">
        <p class="hp"><label>Nicht ausfüllen: <input name="bot-field"></label></p>
        <div class="field"><label for="f-unit">Unterkunft</label>
          <select id="f-unit" name="wohnung">
            <option>Noch offen – bitte beraten</option>
            <optgroup label="Würzburg"><option>Würzburg – egal welche</option>{opts("wuerzburg")}</optgroup>
            <optgroup label="Thüngen"><option>Thüngen – egal welche</option>{opts("thuengen")}</optgroup>
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
        <label class="check"><input type="checkbox" name="datenschutz" required><span>Ich bin einverstanden, dass meine Angaben zur Bearbeitung der Anfrage gespeichert werden (<a class="u-link" href="{prefix}datenschutz/">Datenschutz</a>).</span></label>
        <button class="btn btn--accent btn--lg btn--block" type="submit">Unverbindlich anfragen {icon("arrow", 18, "go")}</button>
        <p class="form-note">Noch keine Buchung und keine Zahlung. Wir antworten persönlich.</p>
        {status_box()}
      </form>"""


def build():
    n_wue = sum(a["city"] == "wuerzburg" for a in APARTMENTS)
    n_thue = sum(a["city"] == "thuengen" for a in APARTMENTS)
    cards = "\n".join(card(P, a, (i % 3) * 0.06) for i, a in enumerate(APARTMENTS))
    reviews = "\n".join(review_card(r) for r in review_items())
    marquee = "".join(f'<span>{icon("check", 16)}{m}</span>' for m in MARQUEE * 2)
    marquee_label = "Auf einen Blick: " + ", ".join(MARQUEE)
    region = "\n".join(
        f'<a class="tile zoom" href="{h}">{img(P, s, t, "300px")}<h3>{t}</h3><p>{d}</p></a>' for s, t, d, h in REGION
    )
    return f"""{head(P, "Ferienwohnungen Würzburg &amp; Thüngen | Direkt beim Gastgeber", "Zwölf Ferienwohnungen in der Würzburger Altstadt und am Schlossberg in Thüngen – mit Eiche aus eigenem Sägewerk, Hunde in Thüngen willkommen. Direkt anfragen.", "", "wue-hero", JSONLD)}
<body data-max-guests="8">
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
        <p class="lead">Zwölf Ferienwohnungen – {n_wue} mitten in Würzburg, {n_thue} ruhig in Thüngen. Persönlich vermietet von einer Familie, die seit Generationen mit Eichenholz arbeitet.</p>
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
      <div class="popover popover--guests" id="pop-guests">{guests_panel(8, "In Würzburg bis 8 (Annastraße), in Thüngen bis 6 Gäste.")}</div>
    </form>
  </div>

  <div class="container">
    <div class="trust">
      <div><strong>{icon("star", 18)} {HOST["score"]}</strong><span>{SOURCE} · {HOST["count"]} Bewertungen</span></div>
      <div><strong>{icon("star", 18)} {BY_ID["wue-herzstueck"]["review"]["score"]}</strong><span>Herzstück der Altstadt</span></div>
      <div><strong>150+ Jahre</strong><span>Familienbetrieb in Thüngen</span></div>
      <div><strong>Direkt</strong><span>ohne Portal-Servicegebühr</span></div>
    </div>
  </div>

  <!-- UNTERKÜNFTE -->
  <section class="section" id="unterkuenfte" aria-labelledby="u-title">
    <div class="container">
      <div class="sec-head">
        <div><span class="kicker">Unsere Unterkünfte</span><h2 id="u-title">Zwölf Wohnungen, zwei Welten.</h2></div>
      </div>
      <div class="chips" role="group" aria-label="Unterkünfte filtern">
        <button class="chip" type="button" data-filter="alle" aria-pressed="true">Alle</button>
        <button class="chip" type="button" data-filter="wuerzburg" aria-pressed="false">{icon("church", 16)} Würzburg</button>
        <button class="chip" type="button" data-filter="thuengen" aria-pressed="false">{icon("wine", 16)} Thüngen</button>
        <button class="chip" type="button" data-filter="hund" aria-pressed="false">{icon("paw", 16)} Mit Hund</button>
        <button class="chip" type="button" data-filter="gruppe" aria-pressed="false">{icon("users", 16)} Ab 6 Gästen</button>
        <button class="chip" type="button" data-filter="parkplatz" aria-pressed="false">{icon("parking", 16)} Mit Parkplatz</button>
      </div>
      <p class="filter-count" data-filter-count aria-live="polite"></p>
      <div class="listings">
{cards}
        <aside class="advice reveal" data-tags="wuerzburg thuengen hund gruppe parkplatz">
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
        <p class="lead" style="max-width:44ch">Würzburg und Thüngen liegen nur 25 km auseinander – und fühlen sich doch ganz verschieden an.</p></div>
      <div class="places">
        <article class="place reveal">
          {img(P, "wue-festung", "Festung Marienberg über Würzburg", "(min-width: 900px) 50vw, 100vw")}
          <div class="place-body">
            <span class="kicker" style="color:rgba(255,255,255,.8)">Würzburg · Altstadt &amp; Innenstadt</span>
            <h3>Die Altstadt vor der Haustür.</h3>
            <p>{n_wue} Stadtwohnungen zwischen Dom, Marktplatz und Main – eine davon im Haus, in dem Tilman Riemenschneider lebte. Das Auto bleibt stehen.</p>
            <div class="place-tags"><span>2–8 Gäste</span><span>35–60 m²</span><span>Alles zu Fuß</span></div>
            <a class="btn btn--white" href="wuerzburg/">Ferienwohnungen Würzburg {icon("arrow", 16, "go")}</a>
          </div>
        </article>
        <article class="place reveal" style="--d:.08s">
          {img(P, "thue-werntal", "Das Werntal bei Thüngen mit Feldern und Wald", "(min-width: 900px) 50vw, 100vw")}
          <div class="place-body">
            <span class="kicker" style="color:rgba(255,255,255,.8)">Thüngen · Schlossberg</span>
            <h3>Ruhe am Schlossberg, Wein vor der Tür.</h3>
            <p>{n_thue} großzügige Wohnungen nordwestlich von Würzburg. Garten am Bach, zu Fuß in die Weinberge, mit dem Rad ins Werntal.</p>
            <div class="place-tags"><span>Bis 6 Gäste</span><span>Hunde willkommen</span><span>Parken am Haus</span></div>
            <a class="btn btn--white" href="thuengen/">Ferienwohnungen Thüngen {icon("arrow", 16, "go")}</a>
          </div>
        </article>
      </div>
    </div>
  </section>

  <!-- EICHE -->
  <section class="section" id="eiche" aria-labelledby="e-title">
    <div class="container story">
      <div class="story-media reveal">
        {img(P, "fewo/thue-haus/05", "Langer Esstisch aus Eiche vor dem Haus Kämpf in Thüngen", "(min-width: 960px) 360px, 60vw")}
        {img(P, "fewo/thue-elefant/01", "Couchtisch aus einer Eichenbohle", "(min-width: 960px) 260px, 40vw")}
      </div>
      <div class="story-text reveal" style="--d:.08s">
        <span class="kicker">Hugo Kämpf · Sägewerk in Thüngen</span>
        <h2 id="e-title">Ihr Esstisch hat eine Herkunft. Sie liegt nebenan.</h2>
        <p class="lead">Hinter den Ferienwohnungen steht Hugo Kämpf – ein Sägewerk für Eichenschnittholz, seit Generationen in Thüngen. Live-Edge-Tische, Waschtische, Wandverkleidungen aus Altholz: Vieles, was Sie bei uns anfassen, ist hier entstanden.</p>
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
        <div style="display:flex;gap:12px;align-items:center">
          <a class="btn btn--light btn--sm" href="ausfluege/">Alle Tipps</a>
          <div class="scroller-nav" data-scroller="region-track">
            <button class="icon-btn" type="button" aria-label="Zurück">{icon("left", 16)}</button>
            <button class="icon-btn" type="button" aria-label="Weiter">{icon("right", 16)}</button>
          </div>
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
        <p class="rv-legal">Insgesamt {HOST["score"]} von 10 aus {HOST["count"]} Bewertungen für unsere Unterkünfte auf {SOURCE}. {UWG_NOTE}</p>
      </div>
    </div>
  </section>

  <!-- FAQ -->
  <section class="section section--flush" id="faq" aria-labelledby="f-title">
    <div class="container faq-grid">
      <div class="sec-head" style="display:grid;align-content:start"><div><span class="kicker">Häufige Fragen</span><h2 id="f-title">Gut zu wissen.</h2>
        <p class="muted">Ihre Frage ist nicht dabei? Rufen Sie uns an: <a class="u-link" href="tel:{PHONE}">{PHONE_LABEL}</a></p></div></div>
      <div class="faq">
{faq_list(FAQ)}
      </div>
    </div>
  </section>

  <!-- ANFRAGE -->
  <section class="section" id="anfrage" aria-labelledby="a-title">
    <div class="container inquiry">
      <div style="display:grid;gap:24px">
        <div style="display:grid;gap:12px"><span class="kicker">Direkt beim Gastgeber</span><h2 id="a-title">Wann dürfen wir Sie begrüßen?</h2>
          <p class="lead">Schreiben Sie uns Ihren Wunschzeitraum – wir antworten persönlich mit Verfügbarkeit und Preis.</p></div>
        {host_card(P)}
      </div>

      {inquiry_form(P)}
    </div>
  </section>
</main>

{page_end(P, sheets(8, "In Würzburg bis 8 (Annastraße), in Thüngen bis 6 Gäste."))}"""

