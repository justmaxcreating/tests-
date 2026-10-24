"""Übersichtsseiten /wuerzburg/ und /thuengen/ – die wichtigsten Einstiegsseiten für die Google-Suche."""
from cards import card, compare_table
from data import APARTMENTS, BY_ID
from reviews import CHECKS, SOURCE, THUENGEN as THUE_RV
from maps import city_map, region_map
from parts import *

P = "../"

WUE_FAQ = [
    ("Wie viele Ferienwohnungen gibt es in Würzburg?", "Acht – sieben davon in der Altstadt und Innenstadt zwischen Dom, Marktplatz und Main, dazu die große Wohnung in der Annastraße für bis zu 8 Personen, ruhig gelegen hinter der Residenz."),
    ("Wo parke ich in Würzburg?", "Kostenlos parken Sie auf der Talavera am Mainufer, gegenüber der Innenstadt. Die Wohnung <a class=\"u-link\" href=\"am-kulturspeicher/\">Am Kulturspeicher</a> hat einen eigenen, kostenlosen Parkplatz vor der Tür."),
    ("Welche Wohnung eignet sich für Familien oder Gruppen?", "Für bis zu 8 Personen die <a class=\"u-link\" href=\"annastrasse/\">Annastraße</a> mit zwei Schlafzimmern. Bis zu 4 Personen finden in fast allen anderen Wohnungen Platz – mit Schlafzimmer und Schlafcouch. In allen Würzburger Wohnungen steht ein Babybett bereit."),
    ("Welche Wohnung liegt am nächsten am Congress Centrum?", "Am nächsten liegen <a class=\"u-link\" href=\"am-kulturspeicher/\">Am Kulturspeicher</a> und die beiden Wohnungen an der Juliuspromenade – jeweils nur wenige Gehminuten entfernt."),
    ("Darf ich meinen Hund mitbringen?", "In den Würzburger Wohnungen leider nicht. In unseren <a class=\"u-link\" href=\"../thuengen/\">Ferienwohnungen in Thüngen</a>, 25 km entfernt, sind Hunde herzlich willkommen."),
    ("Gibt es einen Aufzug?", "Nein. Wer keine Treppen steigen möchte, wählt die Wohnungen Am Kulturspeicher oder Annastraße – beide liegen im Erdgeschoss."),
]

THUE_FAQ = [
    ("Darf mein Hund mit in die Ferienwohnung?", "Ja. In den Wohnungen am Schlossberg – Elefant, Zebra und Giraffe – ist Ihre Fellnase genauso willkommen wie Sie."),
    ("Wie weit ist Thüngen von Würzburg entfernt?", "Rund 25 km. Thüngen liegt nordwestlich von Würzburg im Werntal, mitten im Fränkischen Weinland. Bamberg ist etwa 85 km entfernt."),
    ("Gibt es Parkplätze?", "Ja, am Haus „Wohnen am Schlossberg“ parken Sie kostenlos direkt vor der Wohnung."),
    ("Für wie viele Personen sind die Wohnungen?", "Elefant und Zebra bieten Platz für bis zu 6 Personen, Giraffe für bis zu 4. Alle drei haben 65 m² mit Schlafzimmer und Schlafcouch im Wohnzimmer."),
    ("Was kann man rund um Thüngen unternehmen?", "Wandern und Radeln im Werntal, Weinproben direkt in den Weinbergen, Ausflüge zur Burgruine Homburg, zur Karlsburg und auf das Edelweiß bei Karlstadt, an die Mainschleife bei Volkach – oder einen Tag in Würzburg. Mehr in unseren <a class=\"u-link\" href=\"../ausfluege/\">Ausflugstipps</a>."),
    ("Gibt es einen Garten?", "Ja. Über einen Steg über den kleinen Bach Wern erreichen Sie den Garten, der allen Gästen offensteht."),
]


def item_list(apts):
    return {"@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": f"{SITE}/{a['path']}", "name": a["name"]} for i, a in enumerate(apts)]}


def build_wuerzburg():
    apts = [a for a in APARTMENTS if a["city"] == "wuerzburg"]
    cards = "\n".join(card(P, a, (i % 3) * 0.06) for i, a in enumerate(apts))
    markt = [m for a in apts for _, m, _, k in a["distances"] if k == "markt"]
    markt_min, markt_max = min(markt), max(markt)
    legend = "".join(f'<li><a href="{P}{a["path"]}"><span class="num">{i}</span><span><strong>{a["name"]}</strong><small>{a["street"]} · {a["guests_label"]}</small></span></a></li>'
                     for i, a in enumerate(apts, 1))
    graph = [
        {"@type": "CollectionPage", "@id": f"{SITE}/wuerzburg/#page", "url": f"{SITE}/wuerzburg/", "name": "Ferienwohnungen in Würzburg", "isPartOf": {"@id": f"{SITE}/#website"}},
        item_list(apts),
        ld_breadcrumbs([("Ferienwohnungen", ""), ("Ferienwohnungen Würzburg", "wuerzburg/")]),
        ld_faq(WUE_FAQ),
    ]
    tips = [("wue-residenz", "Residenz", "UNESCO-Welterbe"), ("wue-bridge", "Alte Mainbrücke", "Brückenschoppen"),
            ("wue-festung", "Festung Marienberg", "Blick über die Stadt"), ("wue-kranen", "Alter Kranen", "Abendsonne am Main")]
    tiles = "".join(f'<a class="tile zoom" href="{P}ausfluege/#wuerzburg">{img(P, s, t, "300px")}<h3>{t}</h3><p>{d}</p></a>' for s, t, d in tips)
    return f"""{head(P, "Ferienwohnung Würzburg Altstadt &amp; Zentrum | 8 Wohnungen",
                "Acht Ferienwohnungen mitten in Würzburg: Altstadt, Juliuspromenade, Kulturspeicher, Ringpark. 2 bis 8 Gäste, zu Fuß zu Dom und Main. Direkt beim Gastgeber.",
                "wuerzburg/", "wue-hero", graph)}
<body data-max-guests="8">
{sprite()}
<a class="skip-link" href="#main">Zum Inhalt springen</a>
{header(P, "wuerzburg")}

<main id="main">
  <div class="container page-top">{crumbs(P, [("Ferienwohnungen", ""), ("Würzburg", None)])}</div>
  <section class="hero hero--page" aria-labelledby="hero-title">
    <div class="hero-frame">
      {img(P, "wue-hero", "Blick von der Festung Marienberg auf die Alte Mainbrücke und die Würzburger Altstadt", "100vw", eager=True)}
      <div class="hero-content">
        <span class="kicker">{icon("pin", 16)} Würzburg · Altstadt &amp; Innenstadt</span>
        <h1 id="hero-title">Ferienwohnungen in Würzburg</h1>
        <p class="lead">Acht Stadtwohnungen zwischen Dom, Marktplatz und Main – für den Städtetrip, den Kongress oder die ganze Familie. Alles zu Fuß, persönlich vermietet.</p>
      </div>
    </div>
  </section>

  <div class="container">
    <div class="trust">
      <div><strong>8</strong><span>Wohnungen in der Stadt</span></div>
      <div><strong>35–60 m²</strong><span>2 bis 8 Gäste</span></div>
      <div><strong>{icon("star", 18)} {BY_ID["wue-herzstueck"]["review"]["score"]}</strong><span>{SOURCE} · Herzstück der Altstadt</span></div>
      <div><strong>Direkt</strong><span>ohne Portal-Servicegebühr</span></div>
    </div>
  </div>

  <section class="section" id="wohnungen" aria-labelledby="w-title">
    <div class="container">
      <div class="sec-head"><div><span class="kicker">Unsere Wohnungen in Würzburg</span><h2 id="w-title">Mitten in der Stadt. Ruhig geschlafen.</h2></div></div>
      <div class="listings">
{cards}
      </div>
    </div>
  </section>

  <section class="section section--flush" id="karte" aria-labelledby="k-title">
    <div class="container">
      <div class="sec-head"><div><span class="kicker">Lage</span><h2 id="k-title">Alle Wohnungen auf einen Blick.</h2></div>
        <p class="lead" style="max-width:44ch">Die meisten liegen in der Altstadt zwischen Dom und Main – zum Marktplatz sind es je nach Wohnung {markt_min} bis {markt_max} Minuten zu Fuß.</p></div>
      <div class="map-split">
        <figure class="map-card" style="margin:0">{city_map(P)}</figure>
        <ol class="map-legend">{legend}</ol>
      </div>
      <p class="map-note">Kartendaten © OpenStreetMap-Mitwirkende. Pins antippen öffnet die Wohnung.</p>
    </div>
  </section>

  <section class="section" id="vergleich" aria-labelledby="v-title">
    <div class="container">
      <div class="sec-head"><div><span class="kicker">Vergleich</span><h2 id="v-title">Welche Wohnung passt zu Ihnen?</h2></div></div>
      {compare_table(P, apts)}
    </div>
  </section>

  <section class="section section--flush" aria-labelledby="s-title">
    <div class="container story">
      <div class="story-text reveal">
        <span class="kicker">Städtereise Würzburg</span>
        <h2 id="s-title">Barock, Wein und eine Stadt am Main.</h2>
        <p class="lead">Würzburg ist immer eine Reise wert: Barockbauten mit der Handschrift von Tilman Riemenschneider und Balthasar Neumann, die Residenz als UNESCO-Welterbe seit 1981, Weinstuben und ein lebendiges Mainufer.</p>
        <p class="muted">Die Stadt begeistert alle Generationen – mit Spielplätzen, Badeseen, Skatepark und Botanischem Garten genauso wie mit Kultur und Frankenwein. Aus unseren zentral gelegenen Ferienwohnungen planen Sie Ihre Touren ganz unabhängig. Und wer zum Kongress oder an die Universität kommt, ist in wenigen Minuten dort – <a class="u-link" href="{P}kongress-geschaeftsreise/">mehr zur Geschäftsreise</a>.</p>
        <a class="btn btn--light" href="{P}ausfluege/">Unsere Ausflugstipps {icon("arrow", 16, "go")}</a>
      </div>
      <div class="tiles-2 reveal" style="--d:.08s">{tiles}</div>
    </div>
  </section>

  <section class="section" id="faq" aria-labelledby="f-title">
    <div class="container faq-grid">
      <div class="sec-head" style="display:grid;align-content:start"><div><span class="kicker">Häufige Fragen</span><h2 id="f-title">Gut zu wissen.</h2>
        <p class="muted">Ihre Frage ist nicht dabei? Rufen Sie uns an: <a class="u-link" href="tel:{PHONE}">{PHONE_LABEL}</a></p></div></div>
      <div class="faq">{faq_list(WUE_FAQ)}</div>
    </div>
  </section>

  {cta(P)}
</main>
{page_end(P)}"""


def build_thuengen():
    apts = [a for a in APARTMENTS if a["city"] == "thuengen"]
    cards = "\n".join(card(P, a, i * 0.06) for i, a in enumerate(apts))
    graph = [
        {"@type": "CollectionPage", "@id": f"{SITE}/thuengen/#page", "url": f"{SITE}/thuengen/", "name": "Ferienwohnungen in Thüngen", "isPartOf": {"@id": f"{SITE}/#website"}},
        item_list(apts),
        ld_breadcrumbs([("Ferienwohnungen", ""), ("Ferienwohnungen Thüngen", "thuengen/")]),
        ld_faq(THUE_FAQ),
    ]
    tips = [("thue-werntal", "Werntal", "Wandern und Radeln ab Haustür"), ("goessenheim-homburg", "Burgruine Homburg", "Bei Gössenheim"),
            ("karlstadt-karlsburg", "Karlsburg", "Ruine hoch über dem Main"), ("volkach-mainschleife", "Mainschleife", "Weindorf Volkach")]
    tiles = "".join(f'<a class="tile zoom" href="{P}ausfluege/#weinland">{img(P, s, t, "300px")}<h3>{t}</h3><p>{d}</p></a>' for s, t, d in tips)
    return f"""{head(P, "Ferienwohnung Thüngen mit Hund | Fränkisches Weinland",
                "Ferienwohnungen am Schlossberg in Thüngen, 25 km von Würzburg: 65 m², bis 6 Gäste, Hunde willkommen, Parkplatz und Garten am Bach. Direkt beim Gastgeber.",
                "thuengen/", "thue-schloss", graph)}
<body data-max-guests="6">
{sprite()}
<a class="skip-link" href="#main">Zum Inhalt springen</a>
{header(P, "thuengen")}

<main id="main">
  <div class="container page-top">{crumbs(P, [("Ferienwohnungen", ""), ("Thüngen", None)])}{checks_box(CHECKS.get("thuengen", []))}</div>
  <section class="hero hero--page" aria-labelledby="hero-title">
    <div class="hero-frame">
      {img(P, "thue-schloss", "Schloss Thüngen über dem Ort im Werntal", "100vw", eager=True)}
      <div class="hero-content">
        <span class="kicker">{icon("pin", 16)} Thüngen · Fränkisches Weinland</span>
        <h1 id="hero-title">Ferienwohnungen in Thüngen</h1>
        <p class="lead">Wohnen am Schlossberg: großzügige Wohnungen für Familien, Wanderer und Hundefreunde – 25 km von Würzburg, mitten im Fränkischen Weinland.</p>
      </div>
    </div>
  </section>

  <div class="container">
    <div class="trust">
      <div><strong>{icon("star", 18)} {THUE_RV["score"]}</strong><span>{SOURCE} · {THUE_RV["count"]} Bewertungen</span></div>
      <div><strong>65 m²</strong><span>bis 6 Gäste</span></div>
      <div><strong>{icon("paw", 18)} Ja</strong><span>Hunde willkommen</span></div>
      <div><strong>25 km</strong><span>bis Würzburg</span></div>
    </div>
  </div>

  <section class="section" id="wohnungen" aria-labelledby="w-title">
    <div class="container">
      <div class="sec-head"><div><span class="kicker">Unsere Wohnungen in Thüngen</span><h2 id="w-title">Platz für Familie, Freunde und Hund.</h2></div></div>
      <div class="listings">
{cards}
      </div>
    </div>
  </section>

  <section class="section section--flush" aria-labelledby="h-title">
    <div class="container story">
      <div class="story-media reveal">
        {img(P, "fewo/thue-haus/01", "Das Haus „Wohnen am Schlossberg“ in Thüngen", "(min-width: 960px) 360px, 60vw")}
        {img(P, "fewo/thue-haus/02", "Garten mit Wiese hinter dem Haus am Schlossberg", "(min-width: 960px) 260px, 40vw")}
      </div>
      <div class="story-text reveal" style="--d:.08s">
        <span class="kicker">Rund ums Haus</span>
        <h2 id="h-title">Ein Garten am Bach, ein Schloss nebenan.</h2>
        <p class="lead">Die Wohnungen am Schlossberg sind absolut ruhig gelegen, hell und großzügig – eingerichtet mit Unikatmöbeln aus Eiche.</p>
        <p class="muted">Über einen Steg über den kleinen Bach Wern erreichen Sie den Garten. Malerisch, mit kleinem Wasserfall, fließt die Wern noch immer unter dem Sägewerksgebäude hindurch. Nicht selten sieht man einen Silberreiher auf der Suche nach Bachforellen, und eine Wildgänsefamilie brütet jedes Jahr im alten Stock der Schlossanlage.</p>
      </div>
    </div>
  </section>

  <section class="section" id="hund" aria-labelledby="d-title">
    <div class="container">
      <div class="sec-head"><div><span class="kicker">{icon("paw", 16)} Urlaub mit Hund</span><h2 id="d-title">Die Fellnase ist genauso willkommen wie Sie.</h2></div>
        <p class="lead" style="max-width:46ch">Raus in die frische Natur, die voller gemeinsamer Abenteuer steckt: Wiesen, Wald und Weinberge beginnen direkt am Ort.</p></div>
      <div class="dog-grid">
        {img(P, "fewo/thue-haus/06", "Hund im Körbchen in der Ferienwohnung", "(min-width: 900px) 40vw, 100vw")}
        {img(P, "fewo/thue-haus/08", "Hund auf einer Mauer über den Feldern bei Thüngen", "(min-width: 900px) 30vw, 50vw")}
        {img(P, "fewo/thue-haus/07", "Zwei Hunde auf einem Eichenblock", "(min-width: 900px) 30vw, 50vw")}
      </div>
    </div>
  </section>

  <section class="section section--flush" id="weinland" aria-labelledby="r-title">
    <div class="container story">
      <div class="story-text reveal">
        <span class="kicker">Urlaub im Fränkischen Weinland</span>
        <h2 id="r-title">Landurlaub mit Stadt in Reichweite.</h2>
        <p class="lead">Im Herzen der Weinregionen zwischen Spessart, Rhön, Steigerwald und Taubertal treffen Geselligkeit und Kulturreichtum aufeinander.</p>
        <p class="muted">Verkosten Sie bei einer Wanderung oder einer Radtour entlang des Werntal-Radwegs ein Glas Frankenwein direkt in den Weinbergen – los geht es direkt an der Ferienwohnung. Empfehlenswerte Ziele sind die Burgruine Homburg bei Gössenheim, das Edelweiß bei Karlstadt mit Klettersteig, die Karlsburg über dem Main oder das Weindorf Volkach. Würzburg liegt 25 km entfernt, Bamberg etwa 85 km.</p>
        <a class="btn btn--light" href="{P}ausfluege/#weinland">Alle Ausflugstipps {icon("arrow", 16, "go")}</a>
      </div>
      <div class="tiles-2 reveal" style="--d:.08s">{tiles}</div>
    </div>
  </section>

  <section class="section" id="karte" aria-labelledby="k-title">
    <div class="container">
      <div class="sec-head"><div><span class="kicker">Lage</span><h2 id="k-title">So liegt Thüngen.</h2></div>
        <p class="lead" style="max-width:44ch">Im Werntal nordwestlich von Würzburg – mit dem Auto rund eine halbe Stunde in die Stadt.</p></div>
      <figure class="map-card" style="margin:0">{region_map()}</figure>
      <p class="map-note">Schematische Karte. Kartendaten © OpenStreetMap-Mitwirkende.</p>
    </div>
  </section>

  <section class="section section--flush" id="faq" aria-labelledby="f-title">
    <div class="container faq-grid">
      <div class="sec-head" style="display:grid;align-content:start"><div><span class="kicker">Häufige Fragen</span><h2 id="f-title">Gut zu wissen.</h2>
        <p class="muted">Ihre Frage ist nicht dabei? Rufen Sie uns an: <a class="u-link" href="tel:{PHONE}">{PHONE_LABEL}</a></p></div></div>
      <div class="faq">{faq_list(THUE_FAQ)}</div>
    </div>
  </section>

  {cta(P)}
</main>
{page_end(P)}"""


def cta(prefix):
    return f"""<section class="section" aria-labelledby="cta-title">
    <div class="container">
      <div class="cta-band reveal">
        <div><span class="kicker">Direkt beim Gastgeber</span><h2 id="cta-title">Wann dürfen wir Sie begrüßen?</h2>
          <p class="lead">Schreiben Sie uns Ihren Wunschzeitraum – wir antworten persönlich mit Verfügbarkeit und Preis. Ohne Servicegebühr.</p></div>
        <div class="cta-actions"><a class="btn btn--accent btn--lg" href="{prefix}#anfrage">Unverbindlich anfragen {icon("arrow", 18, "go")}</a>
          <a class="btn btn--light btn--lg" href="tel:{PHONE}">{icon("phone", 18)} {PHONE_LABEL}</a></div>
      </div>
    </div>
  </section>"""
