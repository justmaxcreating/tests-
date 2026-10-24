# Relaunch fewo-urlaub.com – Ferienwohnungen Würzburg & Thüngen

Designvorschlag für die Ferienwohnungs-Website von Carolin & Stefan Voll (Familie hinter dem Sägewerk Hugo Kämpf, Thüngen).
Umfang: **Startseite** + **Detailseite der Würzburger Altstadtwohnung** („Das Herzstück der Altstadt“, Franziskanergasse 1A).

Reines HTML/CSS/JS – kein Framework, kein Build-Schritt, keine externen Requests.

## Ansehen

```bash
cd fewo-relaunch
python3 -m http.server 8000
# → http://localhost:8000
```

Lokal läuft das Anfrageformular im **Demo-Modus** (zeigt die Erfolgsmeldung, verschickt nichts).

## Struktur

```
fewo-relaunch/
├── index.html                    Startseite
├── wuerzburg/altstadt/index.html Detailseite Würzburg (neue, sprechende URL)
├── css/styles.css                Design-System (Tokens oben in :root)
├── js/main.js                    Interaktionen
├── assets/fonts/                 Fraunces + Inter, selbst gehostet (SIL OFL)
├── assets/img/oak-grain.svg      Eichen-Maserung (Textur)
├── assets/favicon.svg
├── robots.txt, sitemap.xml
├── _redirects                    301-Weiterleitungen alte → neue URLs (Netlify)
└── preview/                      Screenshots für die Präsentation
```

## Design

- **Typo:** Fraunces (Serif, Headlines, kursive Akzente in Eichenbraun) + Inter (Text).
- **Farben:** warmes Papier `#f7f3ec`, Tinte `#1d1a16`, Eiche `#8a5a2b`, Bocksbeutel-Grün `#2f4a3a`.
- **Schatten:** mehrlagig und sehr weich (`--shadow-xs` … `--shadow-lg`), dazu feine 1-px-Innenkonturen statt harter Rahmen.
- **Micro-Interactions:**
  - Navigation: Hover-Pille gleitet mit, Header bekommt beim Scrollen einen Blur.
  - Buttons: Lichtpunkt folgt dem Cursor, Pfeil schiebt sich nach rechts.
  - Karten: heben sich beim Hover, Bilder zoomen langsam.
  - Gästezahl: Bump-Animation beim Zählen.
  - Datumsfelder: Nächte werden live berechnet, das Abreise-Datum öffnet sich automatisch.
  - Buchungskarte: Kontaktfelder klappen erst im zweiten Schritt auf.
  - FAQ: animiertes Akkordeon.
  - Lightbox: Tastatur- und Swipe-Steuerung.
  - Kartenpin: pulsiert.
  - Erfolgsmeldung: gezeichneter Haken.
  - Reveal-Animationen beim Scrollen.
- `prefers-reduced-motion` wird respektiert, alles ist per Tastatur bedienbar.

## SEO-Maßnahmen

- Eigener `<title>` und eine eigene Meta-Description pro Seite, jeweils auf das Haupt-Keyword ausgerichtet („Ferienwohnung Würzburg Altstadt“, „Ferienwohnungen Würzburg Thüngen“).
- Saubere, sprechende URL `/wuerzburg/altstadt/`. Die alten URLs (doppelte `.html`-Varianten, Tippfehler `produke`) werden per **301** weitergeleitet, siehe `_redirects`.
- Strukturierte Daten (JSON-LD):
  - `LodgingBusiness` und `WebSite` auf der Startseite
  - `VacationRental` mit Fläche, Belegung, Betten und Ausstattung auf der Detailseite
  - `BreadcrumbList`
  - `FAQPage` auf beiden Seiten
- **Bewusst ohne `aggregateRating`:** Google wertet selbst eingebundene Fremdbewertungen auf der eigenen Seite als „self-serving“. Sie würden kein Rich Result bringen und können eine manuelle Maßnahme auslösen.
- Canonical, Open Graph, `robots.txt`, `sitemap.xml`.
- Semantisches HTML: eine H1 pro Seite, Landmarks, Alt-Texte, `lang="de"`.
- **Performance:** keine Frameworks, Schriften vorgeladen und selbst gehostet. Das ist auch DSGVO-relevant: Google Fonts von Google-Servern zu laden, hat in Deutschland schon zu Abmahnungen geführt.
- **Datenschutz:** keine eingebettete Google-Map. Stattdessen gibt es eine schematische SVG-Karte mit einem Routen-Link.

## Vor dem Go-live erledigen

### Fotos
Alle Bildflächen sind **Platzhalter** (`<div class="ph ...">`). Zum Austausch ersetzt man sie durch
`<img src="..." alt="..." width=".." height=".." loading="lazy" class="ph">`. Die Hero-Bilder bekommen kein `loading="lazy"`.
Dazu braucht es zwei OG-Bilder (1200×630): `assets/img/og-home.png` und `assets/img/og-wuerzburg.png`.

### Anfrageformular
Es ist für **Netlify Forms** vorbereitet (`data-netlify="true"`, Honeypot) und funktioniert dort ohne Backend.
Bei einem anderen Hoster muss die `fetch`-URL in `js/main.js` angepasst werden.

### Rechtliches
`/impressum/` und `/datenschutz/` sind verlinkt, existieren aber noch nicht.

### Markenname
„Voll – Ferienwohnungen Franken“ ist ein **Vorschlag**. Auf den Portalen läuft Thüngen als „Wohnen am Schlossberg“, die Domain heißt fewo-urlaub.com. Der Name sollte einheitlich sein, weil das für die Google-Suche nach dem Markennamen wichtig ist.

### Inhalte zum Gegenprüfen
Die Inhalte stammen aus Suchergebnissen zu fewo-urlaub.com, Booking.com und FeWo-direkt. Die Original-Seite war aus der Arbeitsumgebung nicht direkt erreichbar. Diese Punkte bitte mit den Gastgebern abgleichen:

| Angabe | Quelle / Status |
|---|---|
| Würzburg: 50 m², 2–4 Gäste, 2. OG ohne Aufzug, Babybett, keine Haustiere | fewo-urlaub.com |
| Zweite Würzburg-Seite nennt Innerer Graben 12, 60 m² | widersprüchlich – andere Wohnung? |
| Wohnung „Kulturspeicher“ Würzburg | unklar, ob noch aktiv |
| Thüngen: Elefant/Zebra bis 6, Giraffe bis 4 Gäste | fewo-urlaub.com (FeWo-direkt nennt Zebra bis 4) |
| Blauer Reiter: max. Gästezahl | unbekannt – im Formular vorerst bis 6 |
| Check-in 15 Uhr / Check-out 11 Uhr | Booking.com + fewo-urlaub.com |
| 9,1/10 Booking.com (26 Bew.), 9,6/10 FeWo-direkt | Stand Okt. 2026, regelmäßig aktualisieren |
| „150+ Jahre“, FSC seit 2004 | hugokaempf.de (an anderer Stelle „über 145 Jahre“) |
| Gehdistanzen (Dom ca. 300 m usw.) | geschätzt – mit Routenplaner prüfen |
| Talavera kostenlos parken | fewo-urlaub.com |
| „Spät ankommen? Wir finden eine Lösung“ | Formulierung mit Gastgebern abstimmen |
