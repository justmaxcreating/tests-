"""Inhalte aller Ferienwohnungen – hier ändern, dann `python3 tools/gen/build.py`.

Quelle der Fakten: fewo-urlaub.com (Stand Okt. 2026). Was dort fehlt oder sich widerspricht,
steht im README unter „Inhalte zum Gegenprüfen“ – nichts davon ist hier erfunden.
Fotos: assets/fewo/<id>/NN.jpg (echte Fotos der Gastgeber, Reihenfolge = Reihenfolge hier).
"""
import math

# ---------- Orte für Entfernungen und Karten (per Nominatim ermittelt) ----------
LANDMARKS = {
    "dom": ("Dom St. Kilian", 49.79341, 9.93231),
    "markt": ("Marktplatz", 49.79414, 9.92942),
    "bruecke": ("Alte Mainbrücke", 49.79298, 9.92566),
    "residenz": ("Residenz (UNESCO-Welterbe)", 49.79281, 9.93918),
    "kranen": ("Alter Kranen am Main", 49.79568, 9.92645),
    "hbf": ("Hauptbahnhof", 49.80152, 9.93598),
    "ccw": ("Congress Centrum", 49.79899, 9.92532),
    "kulturspeicher": ("Museum im Kulturspeicher", 49.80121, 9.92258),
    "theater": ("Mainfranken Theater", 49.79543, 9.93667),
    "festung": ("Festung Marienberg", 49.78980, 9.91924),
    "talavera": ("Parken Talavera (kostenlos)", 49.79941, 9.91923),
}
THUENGEN = (49.94232, 9.85871)  # Schloss Thüngen / Gartenstraße
WUERZBURG = (49.79380, 9.92950)


def meters(a, b):
    """Luftlinie in Metern zwischen zwei (lat, lon)."""
    lat = math.radians((a[0] + b[0]) / 2)
    dx = (b[1] - a[1]) * 111320 * math.cos(lat)
    dy = (b[0] - a[0]) * 111200
    return math.hypot(dx, dy)


def walk(a, b):
    """Geschätzter Fußweg: Luftlinie × 1,3, 80 m pro Minute. Gibt (Minuten, Meter) zurück."""
    m = meters(a, b) * 1.3
    return max(1, round(m / 80)), int(round(m / 50.0) * 50) or 50


# ---------- Gemeinsame Bausteine ----------
OAK = ("leaf", "Möbel aus eigener Eiche", "Der Live-Edge-Tisch und die massiven Wohnelemente sind in Thüngen aus Eichen des eigenen Sägewerks entstanden.")
RULES_WUE = ["Check-in ab 15:00 Uhr", "Check-out bis 11:00 Uhr", "Schlüssel liegt zur Check-in-Zeit bereit"]
HOUSE_WUE = ["Nichtraucherwohnung", "Keine Partys", "Keine Haustiere"]
RULES_THUE = ["Check-in ab 15:00 Uhr", "Check-out bis 11:00 Uhr", "Schlüssel liegt zur Check-in-Zeit bereit"]

# Fotos: (Datei-Nummer, Alt-Text). Das erste Foto ist Titelbild.
# sleep: (Raum, Betten, Foto-Nummer oder None)

APARTMENTS = [
    # ======================= WÜRZBURG =======================
    dict(
        id="wue-herzstueck", city="wuerzburg", path="wuerzburg/herzstueck-der-altstadt/",
        name="Herzstück der Altstadt", h1="Herzstück der Altstadt",
        kicker="Ferienwohnung im Tilman-Riemenschneider-Haus",
        title="Ferienwohnung Würzburg Altstadt im Riemenschneider-Haus",
        desc="Ferienwohnung im Haus von Tilman Riemenschneider, zwischen Dom und Alter Mainbrücke. 50 m², 2–4 Gäste, WLAN, Waschmaschine. Direkt beim Gastgeber anfragen.",
        street="Franziskanergasse 1A", zip="97070", town="Würzburg", geo=(49.79226, 9.93063),
        floor="2. Stock, kein Aufzug", floor_level="2", elevator=False,
        size=50, guests=4, bedrooms=1, beds=[("Doppelbett", 1), ("Schlafcouch", 1)],
        sleep=[("Schlafzimmer", "1 Doppelbett", None), ("Wohnzimmer", "Ausziehbare Schlafcouch", "02")],
        pets=False, parking="talavera", rating=("9,6", "FeWo-direkt"), badge="Im Riemenschneider-Haus",
        tags="wuerzburg",
        lead="Wohnen im Haus des Bildhauers Tilman Riemenschneider – zwischen Dom und Alter Mainbrücke.",
        highlights=[("church", "Wohnen mit Geschichte", "Der Bildhauer Tilman Riemenschneider lebte und arbeitete in diesem Haus.")],
        about=[
            "Aus der Haustür, um die Ecke – und Sie stehen vor dem Dom. Ein paar Schritte weiter wartet die Alte Mainbrücke mit Blick auf die Festung Marienberg. Marktplatz, Weinstuben, Residenz: Alles liegt auf Ihrem Weg, nichts braucht ein Auto.",
            "Die neu renovierte Wohnung hat ein separates Schlafzimmer, ein Wohnzimmer mit ausziehbarer Schlafcouch, eine Küchenzeile mit Kochfeld, Kühlschrank und Filter- oder Espressokaffee sowie ein modernes Bad mit Dusche. Dazu Waschmaschine, WLAN und Flat-TV. Den Charakter geben Möbel aus eigener Fertigung: Live-Edge-Tisch, massive Eichenelemente und Landhausdiele.",
            "Die Wohnung liegt im 2. Stock eines historischen Altstadthauses ohne Aufzug. Kinder sind herzlich willkommen, ein Babybett steht bereit. Haustiere sind hier leider nicht erlaubt – mit Hund empfehlen wir unsere Wohnungen in Thüngen.",
        ],
        kitchen="Küchenzeile mit Kochfeld, Kühlschrank, Filter- oder Espressokaffee", bath="Bad mit Dusche &amp; Föhn", washer="Waschmaschine",
        story=dict(year="1483", title="Die Geschichte des Hauses", photo="fewo/wue-herzstueck/05", photo_alt="Tilman-Riemenschneider-Figur am Frankoniabrunnen vor der Residenz",
                   text=["In diesem Jahr zog der Bildhauer und Holzschnitzer <strong>Tilman Riemenschneider</strong> in das Haus an der Franziskanergasse. Hier lebte er fast fünfzig Jahre, hier betrieb er seine Werkstatt, hier starb er 1531.",
                         "Ein Holzbildhauer – und heute eine Wohnung, eingerichtet von einer Familie, die seit Generationen mit Eichenholz arbeitet. Wir finden: Das passt."]),
        photos=[("02", "Wohnzimmer mit ausziehbarer Schlafcouch und großem Fenster"), ("07", "Baumscheibe aus Eiche als Couchtisch neben der Schlafcouch"),
                ("03", "Küchenzeile mit Kochfeld, Backofen und Dunstabzug"), ("04", "Bad mit Glasdusche"),
                ("01", "Historisches Altstadthaus in der Franziskanergasse"), ("05", "Tilman-Riemenschneider-Figur am Frankoniabrunnen vor der Residenz")],
        old=["ferienwohnung-altstadt-wuerzburg"],
    ),
    dict(
        id="wue-im-herzen", city="wuerzburg", path="wuerzburg/im-herzen-der-altstadt/",
        name="Im Herzen der Altstadt", h1="Im Herzen der Altstadt",
        kicker="Ferienwohnung am Inneren Graben, nahe Marktplatz",
        title="Ferienwohnung Würzburg Altstadt am Marktplatz | 60 m²",
        desc="60 m² mitten in der Würzburger Altstadt, zwischen Marktplatz und Altem Kranen: Schlafzimmer, Schlafcouch, WLAN, Waschmaschine. Direkt beim Gastgeber anfragen.",
        street="Innerer Graben 12", zip="97070", town="Würzburg", geo=(49.79627, 9.92880),
        floor="2. Stock, kein Aufzug", floor_level="2", elevator=False,
        size=60, guests=4, bedrooms=1, beds=[("Doppelbett", 1), ("Schlafcouch", 1)],
        sleep=[("Schlafzimmer", "1 Doppelbett", "05"), ("Wohnzimmer", "Ausziehbare Schlafcouch", "02")],
        pets=False, parking="talavera", rating=None, badge="Am Marktplatz",
        tags="wuerzburg",
        lead="Zwischen Marktplatz, Juliuspromenade und Altem Kranen – 60 m² mitten im Geschehen.",
        highlights=[("area", "Viel Platz für die Stadt", "60 m² mit separatem Schlafzimmer, Wohnzimmer und eigenem Essplatz am Fenster.")],
        about=[
            "„Mitten drin in Würzburg“ trifft es genau: Die Wohnung liegt zwischen Marktplatz, Juliuspromenade und dem Alten Kranen am Main. Morgens Bäcker und Markt, abends ein Schoppen am Mainufer – alles in wenigen Gehminuten.",
            "Die vollständig sanierte Wohnung bietet ein separates Schlafzimmer mit Doppelbett, ein Wohnzimmer mit ausziehbarer Schlafcouch, einen Essplatz am Fenster, eine Küchenzeile mit Kochfeld, Kühlschrank und Filterkaffeemaschine sowie ein modernes Bad mit Dusche. Waschmaschine, WLAN und Flat-TV sind selbstverständlich. Live-Edge-Tisch und Eichen-Landhausdiele stammen aus eigener Fertigung.",
            "Die Wohnung liegt im 2. Stock ohne Aufzug. Kinder sind willkommen, ein Babybett ist vorhanden. Haustiere sind nicht erlaubt.",
        ],
        kitchen="Küchenzeile mit Kochfeld, Kühlschrank &amp; Filterkaffeemaschine", bath="Bad mit Dusche &amp; Föhn", washer="Waschmaschine",
        photos=[("02", "Wohnzimmer mit Ecksofa und Kuhfellteppich"), ("03", "Essplatz mit roten Freischwingern und Flat-TV"),
                ("05", "Schlafzimmer mit Doppelbett und Eichenholz über dem Kopfteil"), ("04", "Schmale Küchenzeile mit Bartheke"),
                ("06", "Bad mit Dusche"), ("01", "Bemaltes Altstadthaus am Inneren Graben")],
        old=["ferienwohnung-wuerzburg-altstadt"],
    ),
    dict(
        id="wue-julius-1", city="wuerzburg", path="wuerzburg/juliuspromenade-1/",
        name="Juliuspromenade I", h1="Juliuspromenade I",
        kicker="Kompakte Stadtwohnung zwischen Juliuspromenade und Main",
        title="Ferienwohnung Würzburg Juliuspromenade I | 35 m², 2–3 Gäste",
        desc="Kompakte, stilvoll sanierte Ferienwohnung im Würzburger Zentrum, wenige Schritte zum Main. 35 m², 2–3 Gäste, Schlafzimmer, WLAN, Waschmaschine.",
        street="Bärengasse 2", zip="97070", town="Würzburg", geo=(49.79693, 9.92670),
        floor="2. Stock rechts, kein Aufzug", floor_level="2", elevator=False,
        size=35, guests=3, bedrooms=1, beds=[("Doppelbett", 1), ("Einzelbett in der Leseecke", 1)],
        sleep=[("Schlafzimmer", "1 Doppelbett", "05"), ("Leseecke", "1 Einzelbett für die 3. Person", None)],
        pets=False, parking="talavera", rating=None, badge="Ideal für Paare",
        tags="wuerzburg",
        lead="Kompakt, stilvoll, zentral: zwischen Juliuspromenade und Altem Kranen am Main.",
        highlights=[("briefcase", "Für Städtetrip und Dienstreise", "Kompakte 35 m² mit allem, was man für ein paar Tage in der Stadt braucht – bis zur Waschmaschine.")],
        about=[
            "Mit wenigen Schritten sind Sie am Alten Kranen und am Mainufer, die Juliuspromenade liegt direkt vor der Tür. Ideal für einen Städtetrip zu zweit oder eine Geschäftsreise nach Würzburg.",
            "Die vollständig sanierte Wohnung hat ein separates Schlafzimmer mit Doppelbett und ein drittes Bett in der Leseecke. Dazu eine Küchenzeile mit Kochfeld, Kühlschrank und Filterkaffeemaschine, ein modernes Bad mit Dusche, Waschmaschine, WLAN und Flat-TV. Der Live-Edge-Tisch und die massiven Eichenelemente stammen aus eigener Fertigung.",
            "Die Wohnung liegt im 2. Stock rechts ohne Aufzug. Kinder sind willkommen, ein Babybett ist vorhanden. Haustiere sind nicht erlaubt.",
        ],
        kitchen="Küchenzeile mit Kochfeld, Kühlschrank &amp; Filterkaffeemaschine", bath="Bad mit Dusche &amp; Föhn", washer="Waschmaschine",
        photos=[("02", "Küchenzeile mit Keramikspüle, dahinter der Essplatz am Fenster"), ("01", "Essplatz am Fenster mit Eichentisch und roten Stühlen"),
                ("05", "Schlafzimmer mit Doppelbett"), ("04", "Gedeckter Tisch aus Eiche mit Live-Edge-Kante"),
                ("03", "Kochfeld mit Espressokanne und Filterkaffeemaschine"), ("06", "Bad mit Dusche und Waschmaschine")],
        old=["baerengasse-ferienwohnung"],
    ),
    dict(
        id="wue-julius-2", city="wuerzburg", path="wuerzburg/juliuspromenade-2/",
        name="Juliuspromenade II", h1="Juliuspromenade II",
        kicker="Stadtwohnung mit Wohnzimmer zwischen Juliuspromenade und Main",
        title="Ferienwohnung Würzburg Juliuspromenade II | 50 m², 4 Gäste",
        desc="Ferienwohnung im Würzburger Zentrum zwischen Juliuspromenade und Altem Kranen: 50 m², 2–4 Gäste, Schlafzimmer, Schlafcouch, Eichentisch, WLAN.",
        street="Bärengasse 2", zip="97070", town="Würzburg", geo=(49.79693, 9.92670),
        floor="2. Stock links, kein Aufzug", floor_level="2", elevator=False,
        size=50, guests=4, bedrooms=1, beds=[("Doppelbett", 1), ("Schlafcouch", 1)],
        sleep=[("Schlafzimmer", "1 Doppelbett", "06"), ("Wohnzimmer", "Ausziehbare Schlafcouch", "02")],
        pets=False, parking="talavera", rating=None, badge="",
        tags="wuerzburg",
        lead="Mehr Platz im selben Haus: 50 m² mit Wohnzimmer, Schlafcouch und langem Eichentisch.",
        highlights=[("users", "Platz für vier", "Separates Schlafzimmer plus Wohnzimmer mit Schlafcouch – gut für Familien oder zwei Paare.")],
        about=[
            "Erleben Sie Würzburg in seiner Mitte: Zwischen Juliuspromenade und dem Alten Kranen am Main liegt diese neu renovierte Stadtwohnung. Mainufer, Marktplatz und Congress Centrum erreichen Sie zu Fuß.",
            "Die Wohnung hat ein separates Schlafzimmer mit Doppelbett, ein Wohnzimmer mit ausziehbarer Schlafcouch und einen langen Esstisch aus Eiche. Die Küchenzeile ist mit Kochfeld, Kühlschrank und Filterkaffeemaschine ausgestattet, das moderne Bad hat eine Dusche. Waschmaschine, WLAN und Flat-TV gehören dazu. Eichen-Landhausdiele und Möbel stammen aus eigener Fertigung.",
            "Die Wohnung liegt im 2. Stock links ohne Aufzug. Kinder sind willkommen, ein Babybett ist vorhanden. Haustiere sind nicht erlaubt.",
        ],
        kitchen="Küchenzeile mit Kochfeld, Kühlschrank &amp; Filterkaffeemaschine", bath="Bad mit Dusche &amp; Föhn", washer="Waschmaschine",
        photos=[("02", "Wohnzimmer mit Ecksofa, Kuhfellteppich und Esstisch aus Eiche"), ("03", "Offener Wohn- und Essbereich mit Küchenzeile"),
                ("06", "Schlafzimmer mit Doppelbett und Kleiderschrank"), ("04", "Küchenzeile mit Keramikspüle und Holzfronten"),
                ("05", "Esstisch aus Eiche mit roten Stühlen"), ("01", "Schlafnische mit Matratze vor rotem Wandbild"), ("07", "Bad mit Dusche und Waschmaschine")],
        old=["ferienwohnung-juliuspromenade"],
    ),
    dict(
        id="wue-kulturspeicher", city="wuerzburg", path="wuerzburg/am-kulturspeicher/",
        name="Am Kulturspeicher", h1="Am Kulturspeicher",
        kicker="Loft-Wohnung mit Parkplatz am Congress Centrum",
        title="Ferienwohnung Würzburg mit Parkplatz | Am Kulturspeicher",
        desc="Loft-Wohnung mit 3,70 m Deckenhöhe am Kulturspeicher: kostenloser Parkplatz, Loggia, Erdgeschoss, wenige Schritte zum Congress Centrum. 60 m², 2–4 Gäste.",
        street="Veitshöchheimer Straße 6", zip="97080", town="Würzburg", geo=(49.80076, 9.92445),
        floor="Erdgeschoss rechts", floor_level="0", elevator=None,
        size=60, guests=4, bedrooms=1, beds=[("Doppelbett", 1), ("Matratze", 1)],
        sleep=[("Schlafzimmer", "1 Doppelbett", "04"), ("Wohnzimmer", "Matratze für die 3. und 4. Person", "03")],
        pets=False, parking="own", rating=None, badge="Mit Parkplatz",
        tags="wuerzburg parkplatz",
        lead="Loft-Charakter mit 3,70 m Deckenhöhe, ruhige Loggia und eigener Parkplatz – direkt am Congress Centrum.",
        highlights=[("car", "Kostenloser Parkplatz", "Hauseigener Stellplatz direkt vor der Wohnung – in Würzburg eine Seltenheit."),
                    ("door", "Erdgeschoss mit Loggia", "Keine Treppen mit dem Gepäck, dazu eine ruhige Loggia zum Hinterhaus.")],
        about=[
            "Im traditionellen „Haus der Schifffahrt“ liegt diese renovierte Wohnung – zwischen Congress Centrum, Kulturspeicher und Mainufer. Im Loft-Stil eingerichtet, mit 3,70 m Deckenhöhe und starken alten Mauern: Hier spürt man den Glanz früherer Zeiten.",
            "Die Wohnung hat ein separates Schlafzimmer mit Doppelbett, im Wohnzimmer liegt eine Matratze für die dritte und vierte Person bereit. Dazu kommen eine Küchenzeile mit Kochfeld, Kühlschrank und Filterkaffeemaschine, ein modernes Bad mit Dusche, Waschmaschine, WLAN und Flat-TV. Live-Edge-Tisch, Eichenklötze und Landhausdiele stammen aus eigener Fertigung.",
            "Die Wohnung liegt im Erdgeschoss rechts mit ruhiger Loggia zum Hinterhaus, ein kostenloser hauseigener Parkplatz steht vor der Tür. Kinder sind willkommen, ein Babybett ist vorhanden. Haustiere sind nicht erlaubt.",
        ],
        kitchen="Küchenzeile mit Kochfeld, Kühlschrank &amp; Filterkaffeemaschine", bath="Bad mit Glasdusche &amp; Föhn", washer="Waschmaschine",
        extra_amen=[("sparkle", "Loft-Stil mit 3,70 m Deckenhöhe"), ("door", "Ruhige Loggia zum Hinterhaus")],
        photos=[("01", "Küchenzeile und Essplatz unter hohen Decken"), ("02", "Esstisch aus Eiche mit Rattanstühlen"),
                ("03", "Wohnbereich mit Ledersofa und Flat-TV"), ("04", "Schlafzimmer mit Doppelbett"),
                ("05", "Schlafzimmer mit Kronleuchter und Schreibtisch"), ("06", "Bad mit Glasdusche und Waschmaschine"),
                ("07", "Rotwein und Gläser auf einem Brett aus Eiche")],
        old=["ferienwohnung-kulturspeicher"],
    ),
    dict(
        id="wue-ringpark", city="wuerzburg", path="wuerzburg/am-ringpark/",
        name="Am Ringpark", h1="Am Ringpark",
        kicker="Ferienwohnung an der Sanderglacisstraße",
        title="Ferienwohnung Würzburg am Ringpark | 50 m², bis 4 Gäste",
        desc="Renovierte Ferienwohnung direkt am Würzburger Ringpark: 50 m², 2–4 Gäste, Schlafzimmer, Schlafcouch, WLAN. Rund 15 Minuten zu Fuß zu Dom und Residenz.",
        street="Sanderglacisstraße 3", zip="97072", town="Würzburg", geo=(49.78557, 9.93140),
        floor="1. Halbetage links", floor_level="1", elevator=False,
        size=50, guests=4, bedrooms=1, beds=[("Doppelbett", 1), ("Schlafcouch", 1)],
        sleep=[("Schlafzimmer", "1 Doppelbett", "05"), ("Wohnbereich", "Ausziehbare Schlafcouch", "02")],
        pets=False, parking="talavera", rating=None, badge="Am Park",
        tags="wuerzburg",
        lead="Grün vor der Tür, die Altstadt in einer Viertelstunde: 50 m² direkt am Würzburger Ringpark.",
        highlights=[("tree", "Der Ringpark vor der Tür", "Morgens eine Runde durch den Park, der sich wie ein grüner Gürtel um die Altstadt legt.")],
        about=[
            "Die Wohnung liegt an der Sanderglacisstraße, direkt am Ringpark. Von hier spazieren Sie durch das Grün in die Altstadt, zur Residenz oder hinunter an den Main.",
            "Die geschmackvoll renovierte Wohnung hat ein separates Schlafzimmer mit Doppelbett und einen Wohnbereich mit ausziehbarer Schlafcouch. Die Küchenzeile ist mit Kochfeld, Kühlschrank und Filterkaffeemaschine ausgestattet, das moderne Bad hat eine Dusche. Eine Waschmaschine steht im Keller, WLAN und Flat-TV gibt es in der Wohnung. Live-Edge-Tisch, Eichenklötze und Landhausdiele stammen aus eigener Fertigung.",
            "Die Wohnung liegt in der 1. Halbetage links. Kinder sind willkommen, ein Babybett ist vorhanden. Haustiere sind nicht erlaubt.",
        ],
        kitchen="Küchenzeile mit Kochfeld, Kühlschrank &amp; Filterkaffeemaschine", bath="Bad mit Dusche &amp; Föhn", washer="Waschmaschine im Keller",
        photos=[("03", "Wohn- und Essbereich mit Schlafsofa und roten Stühlen"), ("02", "Wohnbereich mit Schlafsofa und Küchenzeile"),
                ("05", "Schlafzimmer mit Doppelbett vor roter Wand"), ("04", "Küchenzeile mit Barhocker"),
                ("06", "Bad mit Waschbecken"), ("01", "Flur mit Garderobe aus Altholz")],
        old=["ferienwohnung-sanderglacisstrasse-ringpark"],
    ),
    dict(
        id="wue-baeckerbrunnen", city="wuerzburg", path="wuerzburg/am-baeckerbrunnen/",
        name="Am Bäckerbrunnen", h1="Am Bäckerbrunnen",
        kicker="Ferienwohnung in der Semmelstraße",
        title="Ferienwohnung Würzburg Innenstadt | Am Bäckerbrunnen, 60 m²",
        desc="Moderne Ferienwohnung in der Semmelstraße, nahe Theater, Marktplatz und Hauptbahnhof: 60 m², 2–4 Gäste, offener Wohnbereich, Schlafzimmer, WLAN.",
        street="Semmelstraße 43", zip="97070", town="Würzburg", geo=(49.79755, 9.93732),
        floor="2. Stock rechts, kein Aufzug", floor_level="2", elevator=False,
        size=60, guests=4, bedrooms=1, beds=[("Doppelbett", 1), ("Schlafcouch", 1)],
        sleep=[("Schlafzimmer", "1 Doppelbett", "05"), ("Wohnzimmer", "Ausziehbare Schlafcouch", "01")],
        pets=False, parking="talavera", rating=None, badge="Nah am Bahnhof",
        tags="wuerzburg",
        lead="60 m² mit offenem Wohnbereich – zwischen Marktplatz, Theater und Hauptbahnhof.",
        highlights=[("train", "Mit der Bahn bequem", "Vom Hauptbahnhof sind es nur wenige Gehminuten – das Auto kann zu Hause bleiben.")],
        about=[
            "Die Wohnung liegt in der Semmelstraße am Bäckerbrunnen, mitten in der Innenstadt. Marktplatz, Mainfranken Theater und Hauptbahnhof erreichen Sie in wenigen Minuten zu Fuß.",
            "Herzstück ist der offene Wohnbereich mit ausziehbarer Schlafcouch, Essplatz und Küchenzeile mit Kochfeld, Kühlschrank und Filterkaffeemaschine. Dazu ein separates Schlafzimmer mit Doppelbett und ein modernes Bad mit Dusche. Waschmaschine, WLAN und Flat-TV sind vorhanden. Live-Edge-Tisch, massive Eichenelemente und Landhausdiele stammen aus eigener Fertigung.",
            "Die Wohnung liegt im 2. Stock rechts ohne Aufzug. Kinder sind willkommen, ein Babybett ist vorhanden. Haustiere sind nicht erlaubt.",
        ],
        kitchen="Küchenzeile mit Kochfeld, Kühlschrank &amp; Filterkaffeemaschine", bath="Bad mit Dusche &amp; Föhn", washer="Waschmaschine",
        photos=[("01", "Offener Wohnbereich mit Schlafsofa, Essplatz und Küchenzeile"), ("02", "Esstisch mit roten Stühlen vor großem Mohnblumen-Bild"),
                ("05", "Schlafzimmer mit Doppelbett und Eichenbalken"), ("03", "Kochfeld mit Espressokanne und rotem Wasserkocher"),
                ("04", "Couchtisch aus einem Eichenstamm auf Rollen"), ("06", "Bad mit bodengleicher Dusche und Waschmaschine")],
        old=["ferienwohnung-semmelstrasse"],
    ),
    dict(
        id="wue-annastrasse", city="wuerzburg", path="wuerzburg/annastrasse/",
        name="Annastraße", h1="Annastraße – für bis zu 8 Gäste",
        kicker="Große Ferienwohnung in ruhiger Zentrumslage hinter der Residenz",
        title="Ferienwohnung Würzburg für 8 Personen | Nähe Residenz",
        desc="Große Ferienwohnung für Familien und Gruppen bis 8 Personen, ruhig hinter der Würzburger Residenz: zwei Schlafzimmer, Wohnküche, Erdgeschoss.",
        street="Annastraße 26", zip="97072", town="Würzburg", geo=(49.79262, 9.94649),
        floor="Erdgeschoss links", floor_level="0", elevator=None,
        size=None, guests=8, bedrooms=2, beds=[("Doppelbett", 2)],
        sleep=[("Schlafzimmer 1", "1 großes Doppelbett", None), ("Schlafzimmer 2", "1 großes Doppelbett", None), ("Weitere Schlafplätze", "Für bis zu 8 Gäste – Details auf Anfrage", None)],
        pets=False, parking="talavera", rating=None, badge="Bis 8 Gäste",
        tags="wuerzburg gruppe",
        lead="Die große Wohnung für Familien und Gruppen: zwei Schlafzimmer und Wohnküche – ruhig gelegen hinter der Residenz.",
        highlights=[("users", "Für Familien und Gruppen", "Bis zu 8 Gäste, zwei Schlafzimmer mit großem Doppelbett und eine gemütliche Wohnküche für alle."),
                    ("door", "Erdgeschoss", "Kein Treppensteigen mit Gepäck oder Kinderwagen.")],
        about=[
            "Zwischen Ringpark und Residenz liegt diese vollständig und modern sanierte Ferienwohnung – in einer ruhigen Straße hinter dem UNESCO-Welterbe.",
            "Die Wohnung ist für bis zu 8 Personen buchbar: Zwei separate Schlafzimmer haben je ein großes Doppelbett und einen Schrank. Treffpunkt ist die gemütliche Wohnküche mit langem Eichentisch, Kochfeld, Kühlschrank und Filterkaffeemaschine. Das moderne Bad hat eine begehbare Dusche. Waschmaschine, WLAN und Flat-TV sind vorhanden.",
            "Die Wohnung liegt im Erdgeschoss links. Familien und Kinder sind herzlich willkommen, ein Babybett ist vorhanden. Haustiere sind nicht erlaubt.",
        ],
        kitchen="Wohnküche mit Kochfeld, Kühlschrank &amp; Filterkaffeemaschine", bath="Bad mit begehbarer Dusche &amp; Föhn", washer="Waschmaschine",
        photos=[("01", "Wohnküche mit langem Esstisch aus Eiche und Wandbild eines Hochlandrinds")],
        old=["ferienwohnung-wuerzburg-annastrasse"],
    ),
    # ======================= THÜNGEN =======================
    dict(
        id="thue-elefant", city="thuengen", path="thuengen/elefant/",
        name="Elefant", h1="Ferienwohnung Elefant",
        kicker="Wohnen am Schlossberg · Thüngen",
        title="Ferienwohnung Thüngen mit Hund: Elefant | bis 6 Gäste",
        desc="Ferienwohnung Elefant am Schlossberg in Thüngen, 25 km von Würzburg: 65 m², bis 6 Gäste, Hunde willkommen, Parkplatz am Haus, Garten am Bach.",
        street="Gartenstraße 11", zip="97289", town="Thüngen", geo=THUENGEN,
        floor="1. oder 2. Etage, kein Aufzug", floor_level=None, elevator=False,
        size=65, guests=6, bedrooms=1, beds=[("Doppelbett", 1), ("Schlafcouch", 2)],
        sleep=[("Schlafzimmer", "1 Doppelbett, großer Schrank", "05"), ("Wohnzimmer", "2 Schlafcouches", "04")],
        pets=True, parking="own", rating=("9,1", "Booking.com · Haus am Schlossberg"), badge="Hunde willkommen",
        tags="thuengen hund gruppe parkplatz",
        lead="65 m² für bis zu sechs – mit Hund, Garten am Bach und Weinbergen vor der Tür.",
        highlights=[("users", "Platz für die ganze Familie", "Schlafzimmer mit Doppelbett, dazu zwei Schlafcouches im großen Wohnzimmer.")],
        about=[
            "Die Ferienwohnung Elefant liegt im Haus „Wohnen am Schlossberg“ in Thüngen – ruhig, hell und großzügig, mitten im Fränkischen Weinland und nur 25 km von Würzburg entfernt.",
            "Auf 65 m² gibt es ein Schlafzimmer mit Doppelbett und großem Schrank sowie ein Wohnzimmer mit zwei Schlafcouches – Platz für bis zu sechs Personen. Die Küchenzeile hat Kochfeld, Kühlschrank und Filterkaffeemaschine, das moderne Bad eine Badewanne. Couchtisch und Möbel sind Unikate aus Eiche aus eigener Herstellung. WLAN und Flat-TV sind vorhanden.",
            "Hunde sind herzlich willkommen, ein kostenloser Parkplatz steht direkt am Haus. Über einen Steg über die Wern erreichen Sie den Garten. Die Wohnungen liegen in der 1. bzw. 2. Etage, einen Aufzug gibt es nicht.",
        ],
        kitchen="Küchenzeile mit Kochfeld, Kühlschrank &amp; Filterkaffeemaschine", bath="Bad mit Badewanne &amp; Föhn", washer=None,
        photos=[("02", "Wohnzimmer mit roter Wand und Elefanten-Motiv"), ("04", "Wohnzimmer mit Ecksofa und rotem Sessel"),
                ("03", "Wohnzimmer mit Kontrabass und Couchtisch aus Eiche"), ("05", "Schlafzimmer mit Doppelbett"),
                ("06", "Bad mit Badewanne und Waschtisch aus Altholz"), ("01", "Couchtisch aus einer Eichenbohle mit Geige")],
        old=[],
    ),
    dict(
        id="thue-zebra", city="thuengen", path="thuengen/zebra/",
        name="Zebra", h1="Ferienwohnung Zebra",
        kicker="Wohnen am Schlossberg · Thüngen",
        title="Ferienwohnung Thüngen mit Hund: Zebra | bis 6 Gäste",
        desc="Ferienwohnung Zebra am Schlossberg in Thüngen bei Würzburg: 65 m², bis 6 Gäste, langer Esstisch, Hunde willkommen, Parkplatz am Haus, Garten.",
        street="Gartenstraße 11", zip="97289", town="Thüngen", geo=THUENGEN,
        floor="1. oder 2. Etage, kein Aufzug", floor_level=None, elevator=False,
        size=65, guests=6, bedrooms=1, beds=[("Doppelbett", 1), ("Schlafcouch", 2)],
        sleep=[("Schlafzimmer", "1 Doppelbett, großer Schrank", "05"), ("Wohnzimmer", "2 Schlafcouches", "01")],
        pets=True, parking="own", rating=("9,1", "Booking.com · Haus am Schlossberg"), badge="",
        tags="thuengen hund gruppe parkplatz",
        lead="Langer Tisch für sechs, viel Licht und der Garten an der Wern – Familienurlaub am Schlossberg.",
        highlights=[("users", "Ein Tisch für alle", "Am langen Esstisch aus Eiche finden sechs Personen bequem Platz.")],
        about=[
            "Die Ferienwohnung Zebra liegt im Haus „Wohnen am Schlossberg“ in Thüngen – absolut ruhig, hell und großzügig. Würzburg ist 25 km entfernt, die Weinberge beginnen direkt am Ort.",
            "Auf 65 m² gibt es ein Schlafzimmer mit Doppelbett und großem Schrank, ein Wohnzimmer mit zwei Schlafcouches und einen langen Esstisch aus Eiche. Die Küchenzeile hat Kochfeld, Kühlschrank und Filterkaffeemaschine, das moderne Bad eine Badewanne. WLAN und Flat-TV sind vorhanden, die Möbel sind Unikate aus eigener Herstellung.",
            "Hunde sind herzlich willkommen, ein kostenloser Parkplatz steht direkt am Haus, der Garten liegt jenseits des kleinen Bachs Wern. Die Wohnungen liegen in der 1. bzw. 2. Etage, einen Aufzug gibt es nicht.",
        ],
        kitchen="Küchenzeile mit Kochfeld, Kühlschrank &amp; Filterkaffeemaschine", bath="Bad mit Badewanne &amp; Föhn", washer=None,
        photos=[("02", "Wohnzimmer mit Zebra-Motiv, dahinter der Essbereich"), ("01", "Wohnzimmer mit zwei Sofas und Kuhfellteppich"),
                ("04", "Langer Esstisch aus Eiche mit roten Stühlen"), ("03", "Küchenzeile mit Eichenfronten"),
                ("05", "Schlafzimmer mit Doppelbett"), ("06", "Bad mit holzverkleideter Badewanne")],
        old=[],
    ),
    dict(
        id="thue-giraffe", city="thuengen", path="thuengen/giraffe/",
        name="Giraffe", h1="Ferienwohnung Giraffe",
        kicker="Wohnen am Schlossberg · Thüngen",
        title="Ferienwohnung Thüngen mit Hund: Giraffe | bis 4 Gäste",
        desc="Ferienwohnung Giraffe am Schlossberg in Thüngen: 65 m² unter Holzbalken, bis 4 Gäste, Hunde willkommen, Parkplatz am Haus. 25 km bis Würzburg.",
        street="Gartenstraße 11", zip="97289", town="Thüngen", geo=THUENGEN,
        floor="1. oder 2. Etage, kein Aufzug", floor_level=None, elevator=False,
        size=65, guests=4, bedrooms=1, beds=[("Doppelbett", 1), ("Schlafcouch", 1)],
        sleep=[("Schlafzimmer", "1 Doppelbett, großer Schrank", "04"), ("Wohnzimmer", "1 Schlafcouch", "02")],
        pets=True, parking="own", rating=("9,1", "Booking.com · Haus am Schlossberg"), badge="",
        tags="thuengen hund parkplatz",
        lead="Holzbalken, viel Licht und Platz für vier – mit Hund, Garten und Parkplatz am Haus.",
        highlights=[("sparkle", "Unter alten Holzbalken", "Ein offener Wohn- und Essbereich mit sichtbaren Balken und Eichen-Unikaten.")],
        about=[
            "Die Ferienwohnung Giraffe liegt im Haus „Wohnen am Schlossberg“ in Thüngen – ruhig, hell und mit viel Holz. Würzburg ist 25 km entfernt, Weinberge und Wanderwege beginnen vor der Tür.",
            "Auf 65 m² gibt es ein Schlafzimmer mit Doppelbett und großem Schrank sowie einen offenen Wohn- und Essbereich mit Schlafcouch – ideal für bis zu vier Personen. Die Küchenzeile hat Kochfeld, Kühlschrank und Filterkaffeemaschine, das Bad Badewanne und Dusche. WLAN und Flat-TV sind vorhanden.",
            "Hunde sind herzlich willkommen, ein kostenloser Parkplatz steht direkt am Haus, der Garten liegt jenseits der Wern. Die Wohnungen liegen in der 1. bzw. 2. Etage, einen Aufzug gibt es nicht.",
        ],
        kitchen="Küchenzeile mit Kochfeld, Kühlschrank &amp; Filterkaffeemaschine", bath="Bad mit Badewanne, Dusche &amp; Föhn", washer=None,
        photos=[("02", "Wohnbereich mit Giraffen-Motiv unter Holzbalken"), ("01", "Wohn- und Essbereich mit Kronleuchter und Holzbalken"),
                ("03", "Küchenzeile mit Ablage aus Eiche"), ("04", "Schlafzimmer mit Doppelbett und Altholzwand"),
                ("06", "Bad mit Badewanne und Glasdusche"), ("05", "Gedeckter Tisch mit Frankenwein")],
        old=[],
    ),
    dict(
        id="thue-blauer-reiter", city="thuengen", path="thuengen/blauer-reiter/",
        name="Blauer Reiter", h1="Ferienwohnung Blauer Reiter",
        kicker="Im Haus Kämpf · Thüngen",
        title="Ferienwohnung Blauer Reiter in Thüngen | 65 m² im Haus Kämpf",
        desc="Ferienwohnung Blauer Reiter im Haus Kämpf in Thüngen bei Würzburg: 65 m², Schlafzimmer, Wohnbereich mit Küchenzeile, Unikate aus Eichenholz, WLAN.",
        street="Haus Kämpf", zip="97289", town="Thüngen", geo=THUENGEN,
        floor="2. Stock links", floor_level="2", elevator=None,
        size=65, guests=2, bedrooms=1, beds=[("Doppelbett", 1)],
        sleep=[("Schlafzimmer", "1 Doppelbett", "18")],
        pets=None, parking=None, rating=None, badge="Eichen-Unikate",
        tags="thuengen",
        lead="Franz Marcs blaues Pferd an der Wand, Eiche überall: 65 m² im Haus der Sägewerksfamilie.",
        highlights=[("sparkle", "Benannt nach einem Bild", "Im Wohnbereich hängt ein großes Wandbild nach Franz Marcs „Blauem Pferd“ – Marc gründete 1911 den „Blauen Reiter“ mit.")],
        about=[
            "Die Ferienwohnung „Blauer Reiter“ liegt im Haus Kämpf in Thüngen, im 2. Stock links – im Haus der Familie, der das Sägewerk Hugo Kämpf gehört.",
            "Auf 65 m² gibt es ein separates Schlafzimmer mit Doppelbett und einen offenen Wohnbereich mit Küchenzeile, langem Esstisch und Sofa. Das moderne Bad hat eine Duschkabine. Überall finden Sie handgefertigte Unikate aus Eichenholz – von der Arbeitsplatte bis zur Wandverkleidung aus Altholz. WLAN ist vorhanden.",
            "Check-in ist zwischen 15 und 19 Uhr. Rauchen, Veranstaltungen und Partys sind in der Wohnung nicht erlaubt.",
        ],
        kitchen="Küchenzeile mit Arbeitsplatte aus Eiche", bath="Bad mit Duschkabine &amp; Föhn", washer=None,
        checkin="Check-in von 15:00 bis 19:00 Uhr",
        story=dict(year="1911", title="Warum „Blauer Reiter“?", photo="fewo/thue-blauer-reiter/23", photo_alt="Wandbild nach Franz Marcs „Blauem Pferd“ neben dem roten Sofa",
                   text=["In diesem Jahr gründeten Franz Marc und Wassily Kandinsky in München den <strong>„Blauen Reiter“</strong> – eine der wichtigsten Künstlergruppen der Moderne.",
                         "Marcs blaue Pferde sind ihr bekanntestes Motiv. Eines davon begrüßt Sie hier als großes Wandbild im Wohnbereich."]),
        photos=[("02", "Wohnbereich mit Wandbild nach Franz Marcs „Blauem Pferd“ und rotem Sofa"), ("06", "Wohnbereich mit rotem Sofa und langem Esstisch"),
                ("03", "Langer Esstisch aus Eiche vor der salbeigrünen Küchenzeile"), ("18", "Schlafzimmer mit Doppelbett und Altholzwand"),
                ("05", "Essbereich mit Küchenzeile und Fenster"), ("19", "Doppelbett mit Leselampe und Altholzwand"),
                ("17", "Bad mit Duschkabine"), ("01", "Arbeitsplatte aus Eiche mit Spüle und Kräutern"), ("16", "Blick ins Bad mit alter Holzleiter"),
                ("07", "Espressokanne auf einem Holzbrett"), ("08", "Gedeckter Esstisch mit Frankenwein"), ("09", "Wandobjekt aus einer Eichenscheibe"),
                ("13", "Leselampe vor einer Obstschale"), ("14", "Kleiner Weintisch mit Lederstuhl"), ("12", "Buch über alte Eichen auf dem roten Sofa"),
                ("26", "Alte Holzleiter vor Pflanzentapete")],
        old=["ferienwohnung-thuengen/ferienwohnung-thuengen-unterfranken"],
    ),
]

BY_ID = {a["id"]: a for a in APARTMENTS}


def finalize(a):
    """Abgeleitete Felder: Fotopfade, Eckdaten-Zeile, Entfernungen."""
    a["slots"] = [(f"fewo/{a['id']}/{n}", alt) for n, alt in a["photos"]]
    a["cover"] = a["slots"][0][0]
    if a["city"] == "wuerzburg":
        a["place"] = "Würzburg · " + ("Altstadt" if a["id"] in ("wue-herzstueck", "wue-im-herzen") else "Innenstadt")
    else:
        a["place"] = "Thüngen · " + ("Haus Kämpf" if a["street"] == "Haus Kämpf" else "Schlossberg")
    g = f"{a['guests']} Gäste" if a["guests"] <= 2 else (f"2–{a['guests']} Gäste" if a["city"] == "wuerzburg" and a["guests"] <= 4 else f"bis {a['guests']} Gäste")
    a["guests_label"] = g
    parts = ([f"{a['size']} m²"] if a["size"] else []) + [f"{a['bedrooms']} Schlafzimmer" if a["bedrooms"] == 1 else f"{a['bedrooms']} Schlafzimmer", g]
    a["facts"] = " · ".join(parts)
    a["unit"] = ("Würzburg – " if a["city"] == "wuerzburg" else "Thüngen – ") + a["name"]
    if a["city"] == "wuerzburg":
        keys = ["dom", "markt", "bruecke", "residenz", "kranen", "hbf", "ccw", "theater"] + ([] if a["parking"] == "own" else ["talavera"])
        d = [(LANDMARKS[k][0], *walk(a["geo"], LANDMARKS[k][1:]), k) for k in keys]
        a["distances"] = sorted(d, key=lambda x: x[2])
    else:
        a["distances"] = []
    return a


for _a in APARTMENTS:
    finalize(_a)


def nearest(a, n=3, skip=("talavera",)):
    return [d for d in a["distances"] if d[3] not in skip][:n]
