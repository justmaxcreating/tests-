"""Bewertungen und offene Prüfpunkte.

BEWERTUNGEN: Noten und Anzahl von Booking.com, abgelesen am Stand-Datum. Regelmäßig aktualisieren (Note,
Anzahl, Teilnoten). Die Stichpunkte unter „praise“/„heads_up“ sind Zusammenfassungen IN EIGENEN WORTEN – keine
Zitate. Bewertungstexte von Booking wörtlich zu übernehmen ist nicht erlaubt; echte Zitate nur mit Einverständnis
der Gäste (dann z. B. als eigenes Feld ergänzen).

PRÜFPUNKTE (CHECKS): Widersprüche zwischen alter Website, Booking-Inserat und Gästebewertungen. Sie erscheinen in
der Vorschau als gelber Kasten, bis die Gastgeber sie bestätigt haben – dann Text in data.py korrigieren und den
Eintrag hier löschen. build.py listet offene Punkte bei jedem Build.
"""

AS_OF = "Oktober 2026"
SOURCE = "Booking.com"

# Gastgeber-Profil auf Booking.com (alle Unterkünfte zusammen)
HOST = dict(score="9,2", count=319, properties=11)

THUENGEN = dict(
    score="9,4", count=6, url="https://www.booking.com/hotel/de/wohnen-am-schlossberg.html",
    scope="für das Haus „Wohnen am Schlossberg“ mit allen vier Wohnungen",
    cats=[("Lage", "10"), ("Gastgeber", "10"), ("Komfort", "10")],
    praise=["Sehr viel Platz – drinnen und im Garten", "Helle, warme Wohnungen mit moderner Ausstattung",
            "Freundliche Gastgeber mit Tipps für Ausflüge und Wanderungen", "Gut geeignet für Gruppen und Familien"],
    heads_up=None,
)

REVIEWS = {
    "wue-herzstueck": dict(
        score="9,2", count=40, url="https://www.booking.com/hotel/de/wohnen-im-riemenschneiderhaus.html",
        cats=[("Lage", "9,9"), ("Gastgeber", "9,9"), ("WLAN", "10")],
        praise=["Mitten in der Altstadt, wenige Schritte zu Dom und Alter Mainbrücke", "Trotz der zentralen Lage ruhig",
                "Große Dusche und gut ausgestattete Küche", "Gastgeber reagieren schnell und freundlich"],
        heads_up=None),
    "wue-im-herzen": dict(
        score="8,9", count=25, url="https://www.booking.com/hotel/de/wohnen-im-herzen-der-altstadt.html",
        cats=[("Lage", "9,4"), ("Gastgeber", "9,3"), ("WLAN", "10")],
        praise=["Sehr zentral und dennoch ruhig", "Sauber und modern eingerichtet", "Große Dusche und eigene Waschmaschine",
                "Unkomplizierte Schlüsselübergabe, schnelle Antworten"],
        heads_up="Die Gegend ist abends belebt – mit heruntergelassenen Rollläden schläft man ruhig."),
    "wue-julius-1": dict(
        score="8,4", count=41, url="https://www.booking.com/hotel/de/wohnen-an-der-juliuspromenade-main.html",
        cats=[("Lage", "9,3"), ("Komfort", "8,8"), ("WLAN", "8,8")],
        praise=["Zentral zwischen Mainufer, Alter Mainbrücke und Innenstadt", "Gemütlich, mit viel Holz eingerichtet",
                "Gute Betten und Bettwäsche", "Einfacher Check-in, gepflegte Wohnung"],
        heads_up="Die Küchenzeile hat ein Kochfeld, aber keinen Backofen."),
    "wue-kulturspeicher": dict(
        score="8,4", count=59, url="https://www.booking.com/hotel/de/wohnen-am-kulturspeicher.html",
        cats=[("Lage", "9,2"), ("Gastgeber", "8,7"), ("WLAN", "8,8")],
        praise=["Parkplatz direkt vor der Tür", "Geräumig, sauber, bequeme Betten",
                "Zu Fuß am Main entlang in 10 bis 15 Minuten in der Altstadt", "Gastgeber antworten schnell"],
        heads_up="Die Fenster zur Straße gehen auf eine Hauptstraße – ruhig lüften lässt es sich über die Loggia zum Innenhof."),
    "wue-ringpark": dict(
        score="8,7", count=22, url="https://www.booking.com/hotel/de/ringpark-ferien.html",
        cats=[("Komfort", "9,2"), ("Sauberkeit", "8,5")],
        praise=["Zentral am Ringpark, Straßenbahn in wenigen Minuten", "Supermarkt um die Ecke", "Geräumig, mit schöner Dusche",
                "Gastgeber antworten auch abends sofort"],
        heads_up=None),
    "wue-baeckerbrunnen": dict(
        score="8,6", count=42, url="https://www.booking.com/hotel/de/wohnen-am-backerbrunnen-semmelstrasse.html",
        cats=[("Lage", "9,7"), ("Gastgeber", "9,1"), ("WLAN", "10")],
        praise=["Nah am Bahnhof und am Zentrum, Cafés und Bäcker vor der Tür", "Groß und modern eingerichtet, bequeme Betten",
                "Check-in über Schlüsselbox", "Freundlicher, schneller Kontakt"],
        heads_up="Bei offenem Fenster hört man Gastronomie und Bäckerei; mit geschlossenen Fenstern ist es ruhig."),
}
for _id in ("thue-elefant", "thue-zebra", "thue-giraffe", "thue-blauer-reiter"):
    REVIEWS[_id] = THUENGEN

# Gästezitate: wörtlich aus den Booking-Bewertungen, je Eintrag (Zitat, Vorname, Land).
# Das erste Zitat einer Wohnung steht groß oben auf ihrer Seite und auf der Startseite, die übrigen im
# Bereich „Was Gäste sagen“. Leere Liste = kein Zitat-Bereich. "thuengen" gilt für alle vier Thüngen-Wohnungen.
# Beispiel:  "wue-herzstueck": [("Hier der Satz aus der Bewertung.", "Vorname", "Deutschland")],
QUOTES = {
    "wue-herzstueck": [],
    "wue-im-herzen": [],
    "wue-julius-1": [],
    "wue-kulturspeicher": [],
    "wue-ringpark": [],
    "wue-baeckerbrunnen": [],
    "thuengen": [],
}

# Offene Prüfpunkte je Wohnung (Seite) – siehe Docstring
CHECKS = {
    "wue-herzstueck": ["Aufzug: Mehrere Booking-Gäste nennen einen Aufzug (für sie ausschlaggebend). Die alte Website sagt „kein Aufzug“."],
    "wue-julius-1": ["Bewertung: Das Booking-Inserat „Wohnen an der Juliuspromenade Main“ beschreibt eine großzügige Wohnung mit Schlafsofa – passt das zu Juliuspromenade I (35 m², Bett in der Leseecke) oder zu II?"],
    "wue-kulturspeicher": ["Größe und Außenbereich: Booking nennt 56 m² mit Terrasse, die alte Website 60 m² mit Loggia."],
    "wue-ringpark": ["Etage: Booking und Gäste sagen Erdgeschoss, die alte Website „1. Halbetage links“."],
    "thue-elefant": ["Hunde: Das Booking-Inserat sagt „Haustiere nicht gestattet“, alte Website und Gäste sagen hundefreundlich.",
                     "Gästezahl: Booking erlaubt bis zu 4 Gäste, die alte Website bis 6."],
    "thue-zebra": ["Hunde: Das Booking-Inserat sagt „Haustiere nicht gestattet“, alte Website und Gäste sagen hundefreundlich.",
                   "Gästezahl: Booking erlaubt bis zu 4 Gäste, die alte Website bis 6."],
    "thue-giraffe": ["Hunde: Das Booking-Inserat sagt „Haustiere nicht gestattet“, alte Website und Gäste sagen hundefreundlich."],
    "thue-blauer-reiter": ["Lage und Belegung: Booking führt den Blauen Reiter im Haus Gartenstraße 11 mit Doppelbett und Schlafsofa für bis zu 4 Gäste. Die alte Website nennt Haus Kämpf und nur ein Doppelbett."],
    "thuengen": ["Hunde: Das Booking-Inserat „Wohnen am Schlossberg“ sagt „Haustiere nicht gestattet“. Die alte Website und eine Gästin sagen hundefreundlich – diese Seite wirbt damit."],
}

UWG_NOTE = (f"Noten, Anzahl und Zitate stammen aus Bewertungen auf {SOURCE}, Stand {AS_OF}. Auf {SOURCE} können nur Gäste bewerten, "
            "die über die Plattform gebucht und übernachtet haben; eine eigene Prüfung der Bewertungen nehmen wir nicht vor. "
            "Die Stichpunkte sind unsere Zusammenfassung in eigenen Worten.")
