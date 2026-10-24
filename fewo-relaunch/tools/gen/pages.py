"""Inhaltsseiten: Ausflüge, Kongress & Geschäftsreise, Anreise & Kontakt, Impressum, Datenschutz, 404."""
from cards import card
from data import APARTMENTS, LANDMARKS, walk
from hub import cta
from maps import region_map
from parts import *

P = "../"


def page_head(prefix, crumb_name, kicker, h1, lead):
    return f"""<div class="container page-head">
    {crumbs(prefix, [("Ferienwohnungen", ""), (crumb_name, None)])}
    <span class="kicker">{kicker}</span>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
  </div>"""


def nearest_apartment(key):
    """Nächste Würzburger Wohnung zu einem Ort – für interne Links bei den Ausflugstipps."""
    lat, lon = LANDMARKS[key][1:]
    best = min((a for a in APARTMENTS if a["city"] == "wuerzburg"), key=lambda a: walk(a["geo"], (lat, lon))[1])
    return best, walk(best["geo"], (lat, lon))[0]


# (Foto, Titel, Text, Orts-Schlüssel für „nächste Wohnung“ oder None)
SIGHTS_WUE = [
    ("wue-residenz", "Residenz Würzburg", "UNESCO-Welterbe seit 1981: Die barocke Schlossanlage verdankt ihren Weltruhm Baumeister Balthasar Neumann und Giovanni Battista Tiepolo, dessen Deckenfresko über dem Treppenhaus zu den größten der Welt zählt.", "residenz"),
    ("wue-festung", "Festung Marienberg", "Das Wahrzeichen Würzburgs. Eine schöne Wanderung führt über die Alte Mainbrücke und durch den Burggraben hinauf – oben wartet der weiteste Blick über Stadt und Weinberge.", "festung"),
    ("wue-bridge", "Alte Mainbrücke", "Die Steinbrücke mit ihren Heiligenfiguren ist ein Highlight der Stadt. Ein Glas Wein auf der Brücke – der „Brückenschoppen“ – gehört zu den schönsten Nebensachen Würzburgs.", "bruecke"),
    ("wue-kaeppele", "Käppele", "Entlang eines Stationswegs mit 14 Kapellen steigen Sie hinauf zur Wallfahrtskirche – schon allein wegen der Architektur von Balthasar Neumann sehr empfehlenswert.", None),
    ("wue-falkenhaus", "Falkenhaus am Marktplatz", "Das „Haus zum Falken“ besitzt eine der eindrucksvollsten Rokokofassaden Süddeutschlands. Heute ist hier die Tourist-Information untergebracht.", "markt"),
    ("wue-kranen", "Alter Kranen", "Der barocke Hafenkran von 1773 am Mainkai ist ein besonderer Ort – hier scheint die Abendsonne am längsten.", "kranen"),
    ("wue-kulturspeicher", "Museum im Kulturspeicher", "Im ehemaligen Speicher am Alten Hafen zeigt das Museum Kunst vom 19. bis zum 21. Jahrhundert – ein Treffpunkt für alle Kunstinteressierten.", "kulturspeicher"),
    ("veits-hofgarten", "Schiffstour nach Veitshöchheim", "Mit dem Schiff den Main hinab zum Rokokogarten von Veitshöchheim – mit Panoramablick vom Wasser und Einkehr an Bord.", None),
]
SIGHTS_LAND = [
    ("thue-werntal", "Werntal", "Wandern und Radeln auf dem Werntal-Radweg – los geht es direkt an unseren Ferienwohnungen in Thüngen."),
    ("goessenheim-homburg", "Burgruine Homburg", "Die Ruine bei Gössenheim thront über dem Werntal – ein lohnendes Ziel für eine Wanderung."),
    ("fewo/thue-haus/12", "Edelweiß bei Karlstadt", "Kalkfelsen über dem Maintal mit Klettersteig – für Schwindelfreie ein Erlebnis, für alle anderen ein Aussichtspunkt."),
    ("karlstadt-karlsburg", "Karlsburg", "Die Burgruine liegt hoch über dem Main bei Karlstadt – besonders schön im Herbst."),
    ("volkach-mainschleife", "Volkach &amp; Mainschleife", "Das idyllische Weindorf an der Mainschleife ist vor allem für seine kulinarische Vielfalt bekannt."),
    ("wein-stein", "Würzburger Stein", "Die berühmte Weinlage direkt über der Stadt – ideal für einen Spaziergang durch die Reben mit Blick auf Würzburg."),
]


def build_ausfluege():
    def sight(s, t, d, key):
        near = ""
        if key:
            a, m = nearest_apartment(key)
            near = f'<p class="near">{icon("walk", 16)} Nächste Wohnung: <a class="u-link" href="{P}{a["path"]}">{a["name"]}</a> · ca. {m} Min.</p>'
        alt = t.replace("&amp;", "&")
        return f'<article class="tile tile--wide">{img(P, s, alt, "(min-width: 900px) 30vw, 100vw")}<h3>{t}</h3><p>{d}</p>{near}</article>'

    wue = "\n".join(sight(*x) for x in SIGHTS_WUE)
    land = "\n".join(sight(s, t, d, None) for s, t, d in SIGHTS_LAND)
    graph = [
        {"@type": "WebPage", "@id": f"{SITE}/ausfluege/#page", "url": f"{SITE}/ausfluege/", "name": "Ausflüge und Sehenswürdigkeiten in Würzburg und im Fränkischen Weinland", "isPartOf": {"@id": f"{SITE}/#website"}},
        ld_breadcrumbs([("Ferienwohnungen", ""), ("Ausflüge", "ausfluege/")]),
    ]
    return f"""{head(P, "Würzburg Sehenswürdigkeiten &amp; Ausflüge ins Weinland",
                "Tipps der Gastgeber: Residenz, Festung Marienberg, Alte Mainbrücke, Käppele, Schiffstour nach Veitshöchheim, Werntal, Karlsburg und Volkach.",
                "ausfluege/", "wue-festung", graph)}
<body>
{sprite()}
<a class="skip-link" href="#main">Zum Inhalt springen</a>
{header(P, "ausfluege")}
<main id="main">
  {page_head(P, "Ausflüge", "Ausflüge &amp; Sehenswürdigkeiten", "Was Sie in Würzburg und im Weinland nicht verpassen sollten.", "Unsere persönlichen Tipps – von der Residenz bis zum Weinberg. Bei jedem Ziel in Würzburg sehen Sie, welche unserer Wohnungen am nächsten liegt.")}

  <section class="section section--tight" id="wuerzburg" aria-labelledby="w-title">
    <div class="container">
      <div class="sec-head"><div><span class="kicker">{icon("church", 16)} In der Stadt</span><h2 id="w-title">Sehenswürdigkeiten in Würzburg</h2></div>
        <a class="btn btn--light" href="{P}wuerzburg/">Ferienwohnungen in Würzburg {icon("arrow", 16, "go")}</a></div>
      <div class="tiles">
{wue}
      </div>
    </div>
  </section>

  <section class="section section--flush" id="weinland" aria-labelledby="l-title">
    <div class="container">
      <div class="sec-head"><div><span class="kicker">{icon("wine", 16)} Auf dem Land</span><h2 id="l-title">Ausflüge ins Fränkische Weinland</h2></div>
        <a class="btn btn--light" href="{P}thuengen/">Ferienwohnungen in Thüngen {icon("arrow", 16, "go")}</a></div>
      <div class="tiles">
{land}
      </div>
      <p class="muted" style="margin-top:28px;max-width:70ch">Weiter weg, aber eine Reise wert: Bamberg mit seiner sehenswerten Altstadt liegt etwa 85 km von Thüngen entfernt.</p>
    </div>
  </section>

  {cta(P)}
</main>
{page_end(P)}"""


def build_kongress():
    wue = [a for a in APARTMENTS if a["city"] == "wuerzburg"]
    ccw = LANDMARKS["ccw"][1:]
    ranked = sorted(wue, key=lambda a: walk(a["geo"], ccw)[1])
    rows = "".join(
        f'<li><a href="{P}{a["path"]}"><span><strong>{a["name"]}</strong><small>{a["street"]} · {a["guests_label"]}</small></span>'
        f'<span>CCW ca. {walk(a["geo"], ccw)[0]} Min. · Bahnhof ca. {walk(a["geo"], LANDMARKS["hbf"][1:])[0]} Min.</span></a></li>' for a in ranked)
    cards = "\n".join(card(P, a, i * 0.06) for i, a in enumerate(ranked[:3]))
    faq = [
        ("Welche Wohnung liegt am nächsten am Congress Centrum?", f"{ranked[0]['name']} ({ranked[0]['street']}) – zu Fuß etwa {walk(ranked[0]['geo'], ccw)[0]} Minuten. Ebenfalls sehr nah: {ranked[1]['name']} und {ranked[2]['name']}."),
        ("Gibt es eine Wohnung mit Parkplatz?", "Ja, die Wohnung <a class=\"u-link\" href=\"../wuerzburg/am-kulturspeicher/\">Am Kulturspeicher</a> hat einen kostenlosen Parkplatz vor der Tür – und liegt nur wenige Minuten vom Congress Centrum entfernt."),
        ("Kann ich spät anreisen?", "Check-in ist ab 15 Uhr, der Schlüssel liegt zur Check-in-Zeit bereit. Kommen Sie später an, sagen Sie uns Bescheid – wir finden eine Lösung."),
        ("Gibt es WLAN und eine Waschmaschine?", "Ja, alle Würzburger Wohnungen haben kostenloses WLAN und eine Waschmaschine (Am Ringpark im Keller)."),
    ]
    graph = [
        {"@type": "WebPage", "@id": f"{SITE}/kongress-geschaeftsreise/#page", "url": f"{SITE}/kongress-geschaeftsreise/", "name": "Unterkunft für Kongress und Geschäftsreise in Würzburg", "isPartOf": {"@id": f"{SITE}/#website"}},
        ld_breadcrumbs([("Ferienwohnungen", ""), ("Kongress & Geschäftsreise", "kongress-geschaeftsreise/")]),
        ld_faq(faq),
    ]
    return f"""{head(P, "Unterkunft Würzburg für Kongress &amp; Geschäftsreise",
                "Ferienwohnungen statt Hotel: zentral in Würzburg, wenige Gehminuten zum Congress Centrum. WLAN, Küche, Waschmaschine, Parkplatz am Kulturspeicher.",
                "kongress-geschaeftsreise/", "wue-kulturspeicher", graph)}
<body>
{sprite()}
<a class="skip-link" href="#main">Zum Inhalt springen</a>
{header(P)}
<main id="main">
  {page_head(P, "Kongress &amp; Geschäftsreise", "Universitäts- und Kongressstadt Würzburg", "Zum Kongress zu Fuß. Abends Ruhe.", "Menschen aus aller Welt treffen sich in Würzburg zu Kongressen, Tagungen und an der Universität. Unsere zentral gelegenen Ferienwohnungen bringen Sie schnell ins Congress Centrum – und bieten nach einem langen Tag genau die Ruhe, die man sucht.")}

  <section class="section section--tight" aria-labelledby="r-title">
    <div class="container">
      <div class="feature-grid">
        <div class="feature">{icon("walk", 26)}<div><strong>Kurze Wege</strong><p>Congress Centrum, Universität und Hauptbahnhof erreichen Sie ohne großen Zeitaufwand zu Fuß.</p></div></div>
        <div class="feature">{icon("wifi", 26)}<div><strong>Arbeiten wie zu Hause</strong><p>Kostenloses WLAN, ein großer Tisch aus Eiche und eine eigene Küche.</p></div></div>
        <div class="feature">{icon("washer", 26)}<div><strong>Auch für längere Aufenthalte</strong><p>Jede Würzburger Wohnung hat eine Waschmaschine.</p></div></div>
        <div class="feature">{icon("car", 26)}<div><strong>Mit dem Auto?</strong><p>Am Kulturspeicher parken Sie kostenlos vor der Tür, sonst kostenlos auf der Talavera.</p></div></div>
      </div>
    </div>
  </section>

  <section class="section section--flush" aria-labelledby="d-title">
    <div class="container">
      <div class="sec-head"><div><span class="kicker">Entfernungen</span><h2 id="d-title">So nah liegt das Congress Centrum.</h2></div></div>
      <ol class="rank-list">{rows}</ol>
      <p class="map-note">Gehzeiten geschätzt (Luftlinie + 30 %).</p>
    </div>
  </section>

  <section class="section" aria-labelledby="c-title">
    <div class="container">
      <div class="sec-head"><div><span class="kicker">Am nächsten am Congress Centrum</span><h2 id="c-title">Unsere Empfehlungen</h2></div>
        <a class="btn btn--light" href="{P}wuerzburg/">Alle in Würzburg {icon("arrow", 16, "go")}</a></div>
      <div class="listings">
{cards}
      </div>
    </div>
  </section>

  <section class="section section--flush" id="faq" aria-labelledby="f-title">
    <div class="container faq-grid">
      <div class="sec-head" style="display:grid;align-content:start"><div><span class="kicker">Häufige Fragen</span><h2 id="f-title">Gut zu wissen.</h2></div></div>
      <div class="faq">{faq_list(faq)}</div>
    </div>
  </section>

  {cta(P)}
</main>
{page_end(P)}"""


def build_kontakt(form_html):
    wue = [a for a in APARTMENTS if a["city"] == "wuerzburg"]
    hbf = LANDMARKS["hbf"][1:]
    bahn = "".join(f'<li><span><a class="u-link" href="{P}{a["path"]}">{a["name"]}</a></span><span>ca. {walk(a["geo"], hbf)[0]} Min. zu Fuß</span></li>'
                   for a in sorted(wue, key=lambda a: walk(a["geo"], hbf)[1]))
    graph = [
        {"@type": "ContactPage", "@id": f"{SITE}/anreise-kontakt/#page", "url": f"{SITE}/anreise-kontakt/", "name": "Anreise und Kontakt", "isPartOf": {"@id": f"{SITE}/#website"}},
        ld_breadcrumbs([("Ferienwohnungen", ""), ("Anreise & Kontakt", "anreise-kontakt/")]),
    ]
    return f"""{head(P, "Anreise &amp; Kontakt | Ferienwohnungen Würzburg &amp; Thüngen",
                "Anreise zu unseren Ferienwohnungen in Würzburg und Thüngen mit Bahn oder Auto, Parken auf der Talavera oder am Haus. Telefon: 09360 99183.",
                "anreise-kontakt/", "wue-bridge", graph)}
<body data-max-guests="8">
{sprite()}
<a class="skip-link" href="#main">Zum Inhalt springen</a>
{header(P, "kontakt")}
<main id="main">
  {page_head(P, "Anreise &amp; Kontakt", "Anreise &amp; Kontakt", "So finden Sie zu uns.", "Ob mit der Bahn nach Würzburg oder mit dem Auto aufs Land nach Thüngen – hier finden Sie alles für die Anreise. Und wenn etwas offen bleibt: Rufen Sie uns einfach an.")}

  <section class="section section--tight" aria-labelledby="a-title">
    <div class="container two-col">
      <div>
        <h2 id="a-title" class="h3">{icon("train", 22)} Nach Würzburg mit der Bahn</h2>
        <p class="muted">Vom Hauptbahnhof gehen Sie zu allen Würzburger Wohnungen zu Fuß:</p>
        <ul class="distances distances--one">{bahn}</ul>
      </div>
      <div>
        <h2 class="h3">{icon("car", 22)} Nach Würzburg mit dem Auto</h2>
        <p class="muted">Kostenlos parken Sie auf der <strong>Talavera</strong> am Mainufer, gegenüber der Innenstadt – von dort sind es wenige Minuten in die Altstadt. Daneben gibt es kostenpflichtige Parkhäuser. Die Wohnung <a class="u-link" href="{P}wuerzburg/am-kulturspeicher/">Am Kulturspeicher</a> hat einen eigenen kostenlosen Parkplatz.</p>
        <h2 class="h3" style="margin-top:36px">{icon("tree", 22)} Nach Thüngen</h2>
        <p class="muted">Thüngen liegt rund 25 km nordwestlich von Würzburg im Werntal. Am Haus „Wohnen am Schlossberg“ parken Sie kostenlos direkt vor der Wohnung.</p>
        <figure class="map-card" style="margin:20px 0 0">{region_map()}</figure>
      </div>
    </div>
  </section>

  <section class="section" id="anfrage" aria-labelledby="k-title">
    <div class="container inquiry">
      <div style="display:grid;gap:24px">
        <div style="display:grid;gap:12px"><span class="kicker">Kontakt</span><h2 id="k-title">Schreiben Sie uns.</h2>
          <p class="lead">Wir antworten persönlich – meist noch am selben Tag.</p></div>
        {host_card(P)}
      </div>
      {form_html}
    </div>
  </section>
</main>
{page_end(P, sheets(8, "In Thüngen bis 6, in Würzburg bis 8 Gäste (Annastraße)."))}"""


def host_card(prefix):
    return f"""<div class="host-card">
          <div class="host-head"><div class="avatars" aria-hidden="true"><span>C</span><span>S</span></div><div><strong>Carolin &amp; Stefan Voll</strong><div class="muted" style="font-size:.9rem">Ihre Gastgeber in Würzburg &amp; Thüngen</div></div></div>
          <ul class="host-facts">
            <li>{icon("chat")} Persönliche Antwort, kein Callcenter</li>
            <li>{icon("receipt")} Keine Servicegebühr eines Buchungsportals</li>
            <li>{icon("check")} Unverbindlich – Sie entscheiden nach dem Angebot</li>
          </ul>
          <div class="contact-links">
            <a href="tel:{PHONE}"><span><small>Telefon</small>{PHONE_LABEL}</span>{icon("phone", 18)}</a>
            <button type="button" data-copy="{HOST_ADDRESS}" data-toast="Adresse kopiert"><span><small>Adresse</small>{HOST_ADDRESS}</span>{icon("copy", 18)}</button>
          </div>
        </div>"""


def build_impressum():
    graph = [ld_breadcrumbs([("Ferienwohnungen", ""), ("Impressum", "impressum/")])]
    return f"""{head(P, "Impressum | Ferienwohnungen Voll", "Impressum der Ferienwohnungen Voll in Würzburg und Thüngen.", "impressum/", "wue-hero", graph, indexable=False)}
<body>
{sprite()}
<a class="skip-link" href="#main">Zum Inhalt springen</a>
{header(P)}
<main id="main">
  {page_head(P, "Impressum", "Rechtliches", "Impressum", "Angaben gemäß § 5 Digitale-Dienste-Gesetz (DDG).")}
  <div class="container prose">
    <h2>Anbieter</h2>
    <p>Carolin &amp; Stefan Voll<br>Ferienwohnungen<br>Retzstadter Str. 1<br>97289 Thüngen</p>
    <h2>Kontakt</h2>
    <p>Telefon: <a class="u-link" href="tel:{PHONE}">+49 (0) 9360 99183</a><br>E-Mail: <mark>[E-Mail-Adresse ergänzen]</mark></p>
    <h2>Steuernummer</h2>
    <p>231/191/27718</p>
    <h2>Unternehmensgegenstand</h2>
    <p>Vermietung von Ferienwohnungen</p>
    <h2>Bildnachweise</h2>
    <p>Fotos der Ferienwohnungen: Carolin &amp; Stefan Voll. Orts- und Landschaftsfotos: Wikimedia Commons, Urheber und Lizenzen siehe „Bildnachweise“ im Fußbereich jeder Seite. Kartendaten: © OpenStreetMap-Mitwirkende (ODbL).</p>
    <p class="note">Entwurf – Angaben vor Veröffentlichung prüfen: Auf der bisherigen Seite stehen zwei Adressen (Retzstadter Str. 1 im Impressum, Gartenstraße 11 bei Kontakt), die E-Mail-Adresse fehlt hier noch.</p>
  </div>
</main>
{page_end(P)}"""


def build_datenschutz():
    graph = [ld_breadcrumbs([("Ferienwohnungen", ""), ("Datenschutz", "datenschutz/")])]
    return f"""{head(P, "Datenschutz | Ferienwohnungen Voll", "Datenschutzerklärung der Ferienwohnungen Voll.", "datenschutz/", "wue-hero", graph, indexable=False)}
<body>
{sprite()}
<a class="skip-link" href="#main">Zum Inhalt springen</a>
{header(P)}
<main id="main">
  {page_head(P, "Datenschutz", "Rechtliches", "Datenschutz", "Die vollständige Datenschutzerklärung wird vor Veröffentlichung ergänzt.")}
  <div class="container prose">
    <p class="note">Platzhalter – bitte vor Go-live durch eine geprüfte Datenschutzerklärung ersetzen (z. B. über einen Generator oder eine Kanzlei). Die Stichpunkte unten beschreiben, was die Website technisch tut, und helfen beim Ausfüllen.</p>
    <h2>Was diese Website technisch tut</h2>
    <ul>
      <li>Keine Cookies, kein Tracking, keine Analyse-Tools.</li>
      <li>Schriften und Fotos werden selbst gehostet – keine Verbindung zu Google Fonts oder anderen Drittanbietern beim Seitenaufruf.</li>
      <li>Keine eingebettete Google-Map; die Lagekarten sind statische Grafiken. Der Link „Route“ öffnet OpenStreetMap erst nach Klick.</li>
      <li>Hosting bei Netlify (Server-Logfiles beim Hoster).</li>
      <li>Anfrageformulare werden über Netlify Forms übertragen und gespeichert (Name, E-Mail, Zeitraum, Gäste, Nachricht).</li>
      <li>Im Browser gespeichert (nur lokal): gemerkte Wohnungen (localStorage) und der gewählte Zeitraum während des Besuchs (sessionStorage).</li>
    </ul>
  </div>
</main>
{page_end(P)}"""


def build_404():
    return f"""{head("/", "Seite nicht gefunden | Ferienwohnungen Voll", "Diese Seite gibt es nicht (mehr).", "404.html", "wue-hero", [], indexable=False)}
<body>
{sprite()}
{header("/")}
<main id="main">
  <div class="container page-head" style="padding-bottom:var(--section)">
    <span class="kicker">Fehler 404</span>
    <h1>Diese Seite gibt es nicht (mehr).</h1>
    <p class="lead">Vielleicht hat sich die Adresse beim Umzug unserer Website geändert. Hier geht es weiter:</p>
    <div class="cta-actions" style="margin-top:12px">
      <a class="btn btn--accent" href="/wuerzburg/">Ferienwohnungen Würzburg</a>
      <a class="btn btn--light" href="/thuengen/">Ferienwohnungen Thüngen</a>
      <a class="btn btn--light" href="/">Startseite</a>
    </div>
  </div>
</main>
{page_end("/")}"""
