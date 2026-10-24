# Relaunch fewo-urlaub.com – Ferienwohnungen Würzburg & Thüngen

Designvorschlag für die Ferienwohnungs-Website von Carolin & Stefan Voll (Familie hinter dem Sägewerk Hugo Kämpf, Thüngen).
Umfang: **Startseite** + **Detailseite der Würzburger Altstadtwohnung** („Das Herzstück der Altstadt“, Franziskanergasse 1A).

Reines HTML/CSS/JS – kein Framework, keine externen Requests im Browser. Einziger Build-Schritt: ein kleines Netlify-Plugin lädt freie Fotos und hostet sie selbst (siehe *Fotos*).

## Ansehen

**Vorschau online:** https://fewo-relaunch-vorschau.netlify.app/ (Netlify, Branch `fewo-relaunch`, per `noindex` von Suchmaschinen ausgeschlossen)

Lokal:

```bash
cd fewo-relaunch
python3 -m http.server 8000
# → http://localhost:8000
```

Lokal läuft das Anfrageformular im **Demo-Modus** (zeigt die Erfolgsmeldung, verschickt nichts). Fotos gibt es lokal nur, wenn `assets/photos/` befüllt ist – sonst erscheinen Farbflächen als Platzhalter.

## Am Laptop weiterarbeiten

```bash
git clone https://github.com/justmaxcreating/tests-.git
cd tests-
git checkout fewo-relaunch
cd fewo-relaunch
node tools/fetch-photos-local.js   # Fotos laden (einmalig, braucht Internet)
python3 -m http.server 8000         # → http://localhost:8000
```

**Inhalte ändern:** Texte, Wohnungen, FAQ und Bewertungen stehen in `tools/gen/home.py` und `tools/gen/detail.py`, gemeinsame Bausteine (Header, Footer, Icons, Bilder, Kalender) in `tools/gen/parts.py`. Danach `python3 tools/gen/build.py` – das erzeugt beide HTML-Seiten neu. Bitte nicht direkt im HTML ändern, sonst überschreibt der nächste Build die Änderung.
Styles: `css/styles.css`, Interaktionen: `js/main.js` (beide direkt bearbeiten).

**Veröffentlichen:** Jeder Push auf den Branch `fewo-relaunch` landet automatisch auf https://fewo-relaunch-vorschau.netlify.app/.

## Struktur

```
fewo-relaunch/
├── index.html                    Startseite
├── wuerzburg/altstadt/index.html Detailseite Würzburg (neue, sprechende URL)
├── css/styles.css                Design-System (Tokens oben in :root)
├── js/main.js                    Interaktionen
├── assets/fonts/                 Plus Jakarta Sans, selbst gehostet (SIL OFL)
├── assets/photos/                wird beim Netlify-Build befüllt (nicht im Repo)
├── assets/favicon.svg
├── plugins/fetch-photos/         Netlify-Build-Plugin: lädt Fotos + Bildnachweise
├── tools/gen/                    Seiten-Generator (Inhalte → HTML)
├── tools/fetch-photos-local.js   Fotos lokal laden
├── robots.txt, sitemap.xml
├── _redirects                    301-Weiterleitungen alte → neue URLs (Netlify)
└── preview/                      Screenshots für die Präsentation
```

## Design

Aufbau-Prinzipien von großen Buchungsplattformen übernommen, Optik eigenständig:

- **Fotos führen:** großer Foto-Hero, Wohnungskarten mit Bilder-Slider (wischen auf dem Handy, Pfeile am Desktop), Bento-Galerie mit Lightbox auf der Detailseite.
- **Scanbar:** Eckdaten in einer Zeile (m², Gäste, Schlafzimmer), Bewertung direkt am Titel, klare Abschnitte mit Trennlinien.
- **Buchungsfluss:** Suchleiste mit echtem Zeitraum-Kalender (zwei Monate, Bereichs-Vorschau beim Hovern) und Gäste-Auswahl (Erwachsene/Kinder/Kleinkinder, Maximum je Wohnung). Die Auswahl wird von der Startseite auf die Detailseite mitgenommen. Die Buchungskarte bleibt beim Scrollen sichtbar, mobil gibt es eine Leiste am unteren Rand und ein Bottom-Sheet.
- **Filter:** Würzburg, Thüngen, Mit Hund, Für Familien, Bis 6 Personen. Gemerkte Wohnungen (Herz) werden im Browser gespeichert.
- **Typo:** eine Schrift (Plus Jakarta Sans), große, eng gesetzte Headlines.
- **Farben:** warmes Off-White `#fbfaf8`, Tinte `#16140f`, Akzent Bocksbeutel-Grün `#1f3b2d`, Eiche `#9a6a3a` nur sparsam.
- **Details:** weiche, mehrlagige Schatten, 1-px-Konturen statt harter Rahmen, Bilder blenden beim Laden ein, Herz-„Pop“, Stepper-Bump, gezeichneter Haken bei der Erfolgsmeldung.
- `prefers-reduced-motion` wird respektiert, alles ist per Tastatur bedienbar.

### Komponenten von 21st.dev

Zwei Bausteine sind nach Vorlagen von [21st.dev](https://21st.dev) gebaut und in reines HTML/CSS/JS übertragen (die Originale sind React):

- **Bewertungen** nach „Testimonials Section with Logo Marquee“ (@kedhareswer): Snap-Slider mit Pfeilen und Punkten, Tastatursteuerung, Laufband. Inhalte sind nur belegbare Noten; echte Gästezitate können später eingesetzt werden.
- **Foto-Slider der Karten** nach „Image Swiper“ (@lukacho): mit der Maus ziehbar (ab 10 px wird geblättert), Zähler beim Hovern, Klick aufs Foto öffnet die Wohnung.

## Fotos

`plugins/fetch-photos` lädt beim Netlify-Build Fotos und legt sie unter `assets/photos/<slot>-960.jpg` / `-1920.jpg` ab:

- **Würzburg, Weinberge, Schloss Thüngen, Eichenholz:** echte Motive von Wikimedia Commons (CC-Lizenzen). Urheber und Lizenz werden automatisch in `credits.json` geschrieben und im Footer unter „Bildnachweise“ angezeigt.
- **Innenräume:** **Beispielbilder von Unsplash** – nicht die echten Wohnungen. Darauf weist der Hinweisbalken oben auf der Seite hin.

**Echte Fotos einsetzen:** Datei unter dem Slot-Namen nach `assets/photos/` legen (beide Größen) und mit `git add -f` committen (der Ordner ist sonst ignoriert, damit lokal geladene Beispielbilder nicht im Repo landen) – das Plugin überschreibt vorhandene Dateien nicht. Die Fotos der Gastgeber liegen u. a. auf Booking.com und FeWo-direkt. Danach den Hinweisbalken (`.preview-bar`) entfernen.

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
Innenraum-Beispielbilder durch echte Fotos der Wohnungen ersetzen (siehe *Fotos*), Hinweisbalken entfernen.

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
| Blauer Reiter: max. Gästezahl | unbekannt – vorerst ohne Angabe |
| 9,1 (Booking.com) auf allen Thüngen-Karten | gilt für das ganze Haus „Wohnen am Schlossberg“, nicht je Wohnung |
| Check-in 15 Uhr / Check-out 11 Uhr | Booking.com + fewo-urlaub.com |
| 9,1/10 Booking.com (26 Bew.), 9,6/10 FeWo-direkt | Stand Okt. 2026, regelmäßig aktualisieren |
| „150+ Jahre“, FSC seit 2004 | hugokaempf.de (an anderer Stelle „über 145 Jahre“) |
| Gehdistanzen (Dom ca. 300 m usw.) | geschätzt – mit Routenplaner prüfen |
| Talavera kostenlos parken | fewo-urlaub.com |
| „Spät ankommen? Wir finden eine Lösung“ | Formulierung mit Gastgebern abstimmen |
