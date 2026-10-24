# Relaunch fewo-urlaub.com – Ferienwohnungen Würzburg & Thüngen

Designvorschlag für die Ferienwohnungs-Website von Carolin & Stefan Voll (Familie hinter dem Sägewerk Hugo Kämpf, Thüngen).
Umfang: **komplette Website** – Startseite, zwei Übersichtsseiten (Würzburg, Thüngen), **12 Wohnungsseiten**, Ausflüge, Kongress & Geschäftsreise, Anreise & Kontakt, Impressum, Datenschutz, 404.

Reines HTML/CSS/JS – kein Framework, keine externen Requests im Browser. Die Seiten werden mit einem kleinen Python-Generator aus den Inhalten erzeugt.

## Ansehen

**Vorschau online:** https://fewo-relaunch-vorschau.netlify.app/ (Netlify, Branch `fewo-relaunch`, per `noindex` von Suchmaschinen ausgeschlossen)

Lokal:

```bash
cd fewo-relaunch
node tools/fetch-photos-local.js   # Ortsfotos laden (einmalig, braucht Internet)
python3 -m http.server 8000         # → http://localhost:8000
```

Lokal läuft das Anfrageformular im **Demo-Modus** (zeigt die Erfolgsmeldung, verschickt nichts).

## Inhalte ändern

| Was | Wo |
|---|---|
| Wohnungen (Texte, Eckdaten, Fotos, Alt-Texte) | `tools/gen/data.py` |
| Bewertungen (Booking-Noten, Zusammenfassungen) und offene Prüfpunkte | `tools/gen/reviews.py` |
| Startseite | `tools/gen/home.py` |
| Übersichten Würzburg / Thüngen inkl. FAQ | `tools/gen/hub.py` |
| Ausflüge, Kongress, Kontakt, Impressum, Datenschutz, 404 | `tools/gen/pages.py` |
| Detailseiten-Vorlage | `tools/gen/detail.py` |
| Header, Footer, Icons, Bilder, SEO-Kopf | `tools/gen/parts.py` |
| Lagekarten | `tools/gen/maps.py` (+ Geodaten in `geo_data.py`) |

Danach `python3 tools/gen/build.py` – das erzeugt **alle Seiten, `sitemap.xml` und `_redirects`** neu. Bitte nicht direkt im HTML ändern, sonst überschreibt der nächste Build die Änderung.
Styles: `css/styles.css`, Interaktionen: `js/main.js` (beide direkt bearbeiten).

**Veröffentlichen:** Jeder Push auf den Branch `fewo-relaunch` landet automatisch auf https://fewo-relaunch-vorschau.netlify.app/.

## Struktur

```
fewo-relaunch/
├── index.html                       Startseite (alle 12 Wohnungen, Filter, Anfrage)
├── wuerzburg/index.html             Übersicht Würzburg: Karte, Vergleich, FAQ
├── wuerzburg/<wohnung>/index.html   8 Detailseiten
├── thuengen/index.html              Übersicht Thüngen: Hund, Garten, Weinland, Karte, FAQ
├── thuengen/<wohnung>/index.html    4 Detailseiten
├── ausfluege/                       Sehenswürdigkeiten + nächstgelegene Wohnung
├── kongress-geschaeftsreise/        Landingpage für Geschäftsreisende
├── anreise-kontakt/                 Anreise per Bahn/Auto + Anfrageformular
├── impressum/, datenschutz/         Entwürfe (noindex)
├── 404.html
├── css/styles.css, js/main.js
├── assets/fewo/<wohnung>/NN.jpg     echte Fotos der Gastgeber (im Repo)
├── assets/photos/                   Ortsfotos, beim Netlify-Build geladen (nicht im Repo)
├── plugins/fetch-photos/            Netlify-Build-Plugin für die Ortsfotos + Bildnachweise
├── tools/gen/                       Seiten-Generator
├── robots.txt, sitemap.xml, _redirects, _headers
└── preview/                         Screenshots des ersten Entwurfs
```

### URLs

| Seite | URL | Zielsuchbegriff |
|---|---|---|
| Startseite | `/` | Ferienwohnungen Würzburg Thüngen |
| Würzburg | `/wuerzburg/` | Ferienwohnung Würzburg (Altstadt, Zentrum) |
| Herzstück der Altstadt | `/wuerzburg/herzstueck-der-altstadt/` | Ferienwohnung Würzburg Altstadt |
| Im Herzen der Altstadt | `/wuerzburg/im-herzen-der-altstadt/` | Ferienwohnung Würzburg Marktplatz |
| Juliuspromenade I / II | `/wuerzburg/juliuspromenade-1/`, `-2/` | Ferienwohnung Würzburg Zentrum |
| Am Kulturspeicher | `/wuerzburg/am-kulturspeicher/` | Ferienwohnung Würzburg mit Parkplatz |
| Am Ringpark | `/wuerzburg/am-ringpark/` | Ferienwohnung Würzburg Ringpark |
| Am Bäckerbrunnen | `/wuerzburg/am-baeckerbrunnen/` | Ferienwohnung Würzburg Innenstadt |
| Annastraße | `/wuerzburg/annastrasse/` | Ferienwohnung Würzburg 8 Personen |
| Thüngen | `/thuengen/` | Ferienwohnung Thüngen, mit Hund, Fränkisches Weinland |
| Elefant, Zebra, Giraffe, Blauer Reiter | `/thuengen/<name>/` | Ferienwohnung Thüngen mit Hund |
| Ausflüge | `/ausfluege/` | Würzburg Sehenswürdigkeiten, Ausflüge Weinland |
| Kongress | `/kongress-geschaeftsreise/` | Unterkunft Würzburg Kongress |

## Design

Aufbau-Prinzipien von großen Buchungsplattformen übernommen, Optik eigenständig:

- **Fotos führen:** großer Foto-Hero, Wohnungskarten mit Bilder-Slider, Bento-Galerie mit Lightbox auf jeder Detailseite.
- **Scanbar:** Eckdaten in einer Zeile, Vergleichstabelle auf der Würzburg-Übersicht, Gehzeiten zu den wichtigsten Zielen.
- **Buchungsfluss:** Suchleiste mit Zeitraum-Kalender und Gäste-Auswahl (Maximum je Wohnung). Die Auswahl wird mitgenommen. Buchungskarte bleibt beim Scrollen sichtbar, mobil Leiste unten und Bottom-Sheet.
- **Filter:** Würzburg, Thüngen, Mit Hund, Ab 6 Gästen, Mit Parkplatz. Gemerkte Wohnungen (Herz) werden im Browser gespeichert.
- **Lagekarten** als eigene SVG-Grafik aus echten Koordinaten (OpenStreetMap-Daten): kein Google Maps, keine Cookies, keine externen Requests. Auf der Würzburg-Übersicht alle 8 Wohnungen nummeriert, auf den Detailseiten die Wohnung + Nachbarn als Links.
- **Gehzeiten** werden aus den Koordinaten berechnet (Luftlinie × 1,3, 80 m/min) – ehrlich statt „nur wenige Schritte“.
- Typo: Plus Jakarta Sans (selbst gehostet). Farben: Off-White `#fbfaf8`, Tinte `#16140f`, Bocksbeutel-Grün `#1f3b2d`, Eiche `#9a6a3a`.
- `prefers-reduced-motion` wird respektiert, alles ist per Tastatur bedienbar.

### Komponenten von 21st.dev

- **Bewertungen** nach „Testimonials Section with Logo Marquee“ (@kedhareswer).
- **Foto-Slider der Karten** nach „Image Swiper“ (@lukacho).

## Fotos

- **Wohnungen:** echte Fotos der Gastgeber, übernommen von fewo-urlaub.com, optimiert unter `assets/fewo/<wohnung>/NN.jpg`. Jedes Foto hat einen beschreibenden Alt-Text (`data.py`). Doppelte Fotos wurden aussortiert.
- **Orte & Ausflüge:** Wikimedia Commons (CC-Lizenzen), geladen vom Plugin `plugins/fetch-photos`. Urheber und Lizenz landen automatisch in `credits.json` und erscheinen im Footer unter „Bildnachweise“.
- **Neue Fotos einsetzen:** Datei unter `assets/fewo/<wohnung>/` ablegen (mind. 1600 px breit, JPG), in `data.py` bei der Wohnung in `photos` eintragen, Build starten. Die Maße liest der Generator aus `assets/fewo/manifest.json` – nach neuen Fotos das Manifest aktualisieren (Breite/Höhe je Datei).

## SEO-Maßnahmen (umgesetzt)

- **Eine Seite pro Wohnung** mit eigener, sprechender URL, eigenem `<title>` (≤ 60 Zeichen) und eigener Meta-Description (≤ 158 Zeichen), jeweils auf einen Suchbegriff ausgerichtet (siehe Tabelle oben).
- **Übersichtsseiten** für „Ferienwohnung Würzburg“ und „Ferienwohnung Thüngen (mit Hund)“ mit eigenem Text, Karte, Vergleich und FAQ.
- **Interne Verlinkung:** Brotkrumen, „Weitere Wohnungen in der Nähe“ auf jeder Detailseite, Kartenpins als Links, Ausflugstipps verlinken die nächstgelegene Wohnung, Footer mit allen 12 Wohnungen.
- **301-Weiterleitungen** aller alten URLs (mit und ohne `.html`, mit und ohne `/`) auf die passende neue Seite – erzeugt in `_redirects`. Erhält Rankings und Backlinks.
- **Strukturierte Daten (JSON-LD):** `VacationRental` je Wohnung (Fläche, Belegung, Betten, Ausstattung, Geo-Koordinaten, Fotos), `LodgingBusiness`, `WebSite`, `ItemList`, `CollectionPage`, `BreadcrumbList`, `FAQPage`.
  - Hinweis: FAQ-Ergebnisse zeigt Google seit 2023 nur noch für wenige Websites an, und Ferienunterkünfte erscheinen in Google über Partner-Feeds (z. B. Booking, FeWo-direkt). Die Daten helfen Google trotzdem, die Seiten zu verstehen.
  - **Bewusst ohne `aggregateRating`:** Selbst eingebundene Fremdbewertungen wertet Google als „self-serving“.
- **Semantisches HTML:** eine H1 pro Seite, Landmarks, Alt-Texte für alle Fotos, `lang="de"`.
- **Performance:** keine Frameworks, Schriften selbst gehostet, Bilder mit `width`/`height` (kein Layout-Springen) und Lazy Loading.
- **Datenschutz:** keine Google Fonts, keine eingebettete Karte, keine Cookies.
- `sitemap.xml` (18 Seiten) und `robots.txt` werden mitgebaut.

## Vor dem Go-live erledigen

1. **Indexierung freischalten:** in `tools/gen/parts.py` `INDEXABLE = True`, Build starten, `_headers` löschen.
2. **Weiterleitungen prüfen:** in der Google Search Console unter *Leistung → Seiten* alle alten URLs exportieren und mit `_redirects` abgleichen.
3. **Anfrageformular:** vorbereitet für **Netlify Forms** (`anfrage` auf Startseite/Kontakt, `anfrage-wohnung` auf den Detailseiten). Bei einem anderen Hoster die `fetch`-URL in `js/main.js` anpassen.
4. **Rechtliches:** Impressum ist ein Entwurf (E-Mail fehlt), die Datenschutzerklärung ein Platzhalter mit Stichpunkten.
5. **Markenname:** „Voll – Ferienwohnungen in Franken“ ist ein **Vorschlag**. Auf den Portalen läuft Thüngen als „Wohnen am Schlossberg“, die Domain heißt fewo-urlaub.com. Name, Adresse und Telefon sollten überall identisch sein.
6. **Hinweisbalken** „Designentwurf“ in `tools/gen/parts.py` (`header()`) entfernen.

## Bewertungen

- Noten, Anzahl und Teilnoten stammen von den **Booking.com-Inseraten** der Gastgeber (Stand Oktober 2026), gepflegt in `tools/gen/reviews.py`. Gastgeber gesamt: 9,2 aus 319 Bewertungen.
- Die Stichpunkte sind **Zusammenfassungen in eigenen Worten**, keine Zitate. Bewertungstexte von Booking wörtlich zu übernehmen ist nicht erlaubt. Echte Gästezitate nur mit Einverständnis der Gäste.
- Unter jeder Bewertung steht der **Hinweis nach § 5b UWG** (Herkunft und ob geprüft wird). Wortlaut vor Go-live rechtlich prüfen lassen.
- Keine Bewertungen gefunden für Juliuspromenade II und Annastraße (das Booking-Inserat in der Annastraße 26 gehört einem anderen Vermieter).
- Noten alle paar Monate aktualisieren: Booking zeigt ältere Bewertungen nicht mehr an, die Zahlen ändern sich.

### Offene Prüfpunkte

Widersprüche zwischen alter Website, Booking-Inseraten und Gästebewertungen stehen in `reviews.py` unter `CHECKS`. In der Vorschau erscheinen sie als **gelber Kasten** auf der betroffenen Seite, `build.py` listet sie bei jedem Build auf. Live (`INDEXABLE = True`) wird der Kasten nie gezeigt. Nach Klärung: Text in `data.py` korrigieren, Eintrag in `CHECKS` löschen.

## Inhalte zum Gegenprüfen

Alle Fakten stammen von fewo-urlaub.com (Stand Okt. 2026), die Texte sind neu geschrieben. Folgendes ist unklar oder widersprüchlich:

| Punkt | Stand / Annahme |
|---|---|
| **Adresse Thüngen** | Kontakt: Gartenstraße 11 · Thüngen-Seite: „Gärtnerstraße 11“ (gibt es laut Karte nicht) · Impressum: Retzstadter Str. 1. Verwendet: **Gartenstraße 11** (Haus am Schlossberg), Impressum: Retzstadter Str. 1 |
| **Blauer Reiter** | Genaue Adresse von „Haus Kämpf“ fehlt; max. Gäste unbekannt (vorerst 2, da nur Doppelbett genannt); Hunde, Parkplatz, TV, Babybett unbekannt → nicht erwähnt. Die 9,1 von Booking gilt für das Haus am Schlossberg, nicht für den Blauen Reiter. |
| **Annastraße** | Nur **ein** Foto vorhanden; Größe (m²) fehlt; „bis 8 Personen“ bei 2 Doppelbetten – weitere Schlafplätze unklar (Seite sagt „Details auf Anfrage“) |
| **Herzstück der Altstadt** | Fotos sehr klein (max. 640 px), kein Schlafzimmerfoto |
| **Juliuspromenade I / II** | Text von I nennt „3. Bett in der Leseecke“, das Foto der Schlafnische liegt aber auf der Seite von II. Bitte zuordnen. |
| **Am Kulturspeicher** | Original nennt 2–4 Gäste, an anderer Stelle „bestens geeignet für 2 Personen“ |
| **Elefant / Zebra / Giraffe** | Welche Wohnung in welcher Etage? Bad laut Fotos mit Badewanne |
| Thüngen: Elefant/Zebra bis 6, Giraffe bis 4 | fewo-urlaub.com (FeWo-direkt nennt Zebra bis 4) |
| Bewertungen 9,1 Booking (26) · 9,6 FeWo-direkt · 8,6 Gîtes.fr | Stand Okt. 2026, regelmäßig aktualisieren |
| „150+ Jahre“, FSC seit 2004 | hugokaempf.de (an anderer Stelle „über 145 Jahre“) |
| Gehzeiten | aus Koordinaten geschätzt (Luftlinie × 1,3) |
| Check-in 15 Uhr / Check-out 11 Uhr | fewo-urlaub.com; Blauer Reiter: Check-in 15–19 Uhr |
| Corona-Hinweis der alten Startseite | bewusst weggelassen (veraltet) |
| Wohnung „Kulturspeicher“ | auf der alten Seite noch aktiv – übernommen |
