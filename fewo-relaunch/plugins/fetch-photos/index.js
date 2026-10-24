// Lädt beim Netlify-Build freie Fotos (Wikimedia Commons / Unsplash) und hostet sie selbst.
// Hintergrund: keine Hotlinks zu Drittanbietern (Ladezeit, DSGVO). Fehlt ein Foto,
// zeigt die Seite automatisch den Farbverlauf-Platzhalter.
// Ersetzen durch echte Fotos: Dateien nach assets/photos/<slot>-960.jpg / -1920.jpg legen
// und den Slot unten entfernen – vorhandene Dateien werden nicht überschrieben.
const fs = require("fs");
const path = require("path");

let OUT;
const UA = "fewo-relaunch-build/1.0 (Netlify build; static site photo fetch)";
const SIZES = [960, 1920];

const c = (title) => ({ commons: title });
const u = (id) => ({ unsplash: id });

// Die Wohnungsfotos selbst liegen als echte Fotos der Gastgeber unter assets/fewo/ (im Repo).
// Hier nur Orts- und Ausflugsmotive.
const SLOTS = {
  "wue-hero": [c("Würzburg, Festung Marienberg, Blick auf die Altstadt -- 2018 -- 0323.jpg"), c("Würzburg, die Alte Mainbrücke.JPG"), c("Wurzburg Marienberg Fortress on the Main in Würzburg.jpg")],
  "wue-bridge": [c("Alte Mainbrücke Würzburg 20180521 004.jpg"), c("View of the old bridge over Main in Wurzburg 01.jpg"), c("Würzburg, die Alte Mainbrücke.JPG")],
  "wue-festung": [c("Wurzburg Marienberg Fortress on the Main in Würzburg.jpg"), c("Würzburg; Festung Marienberg.jpg"), c("Marienberg wuerzburg.jpg")],
  "wue-residenz": [c("Würzburg Residenz Weltkulturerbe und Hofgarten.jpg"), c("Wuerzburger Residenz vom Hofgarten.jpg"), c("Residenz Wuerzburg Hofgarten.jpg")],
  "wue-main": [c("Main Kutter Würzburg.jpg"), c("View of the old bridge over Main in Wurzburg 01.jpg")],
  "wein-stein": [c("Würzburger Stein.jpg"), u("1506377247377-2a5b3b417ebb")],
  "thue-schloss": [c("Schloss Thüngen April 2021 05.jpg"), c("Thüngen, Schloss-001.jpg"), c("Schloss Thüngen.jpg")],
  "oak-wood": [c("Eiche (Holz).JPG"), c("Eichenholz.jpg")],
  "wue-falkenhaus": [c("Würzburg, Falkenhaus -- 2018 -- 0233.jpg"), c("Falkenhaus in Wurzburg 01.jpg")],
  "wue-kranen": [c("Alter Kranen, Würzburg, South view 20190716 1.jpg"), c("20230105 Alter Kranen Würzburg.jpg")],
  "wue-kulturspeicher": [c("20230105 Kulturspeicher Würzburg 01.jpg"), c("Würzburg - Kulturspeicher Hafenseite.jpg")],
  "wue-kaeppele": [c("Würzburg, Käppele -- 2018 -- 0280.jpg"), c("Käppele Würzburg.jpg"), c("Wuerzburg Kaeppele.jpg")],
  "veits-hofgarten": [c("Veitshöchheim - Hofgarten - großer See mit Parnass und Schloss.jpg"), c("Veitshöchheim - Hofgarten - kleiner See.jpg")],
  "volkach-mainschleife": [c("Mainschleife bei Volkach.jpg"), c("Mainschleife Weinberge Herbst 140502-Pano.jpg")],
  "karlstadt-karlsburg": [c("Ruine Karlsburg Karlstadt 20181027 001.jpg"), c("Karlstadt, Karlsburg-001.jpg")],
  "goessenheim-homburg": [c("Gössenheim, Burgruine Homburg 20170409 002.jpg"), c("Gössenheim, Burgruine Homburg 20170409 005.jpg")],
  "thue-werntal": [c("Werntal bei Thüngen Mai 2024.jpg"), c("Thüngen Werntal April 2021 04.jpg")],
};

const strip = (html = "") => html.replace(/<[^>]+>/g, "").replace(/\s+/g, " ").trim();

async function download(url, file) {
  const res = await fetch(url, { headers: { "User-Agent": UA }, redirect: "follow" });
  const type = res.headers.get("content-type") || "";
  if (!res.ok || !type.startsWith("image/")) throw new Error(`${res.status} ${type}`);
  const buf = Buffer.from(await res.arrayBuffer());
  if (buf.length < 15000) throw new Error(`zu klein (${buf.length} B)`);
  fs.writeFileSync(file, buf);
}

async function fromCommons(title, slot) {
  const api = `https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=${SIZES[1]}&titles=${encodeURIComponent("File:" + title)}`;
  const res = await fetch(api, { headers: { "User-Agent": UA } });
  const data = await res.json();
  const page = Object.values(data.query.pages)[0];
  const info = page.imageinfo && page.imageinfo[0];
  if (!info) throw new Error("nicht gefunden");
  const big = info.thumburl || info.url;
  const small = info.thumburl ? info.thumburl.replace(`/${SIZES[1]}px-`, `/${SIZES[0]}px-`) : info.url;
  await download(big, path.join(OUT, `${slot}-${SIZES[1]}.jpg`));
  await download(small, path.join(OUT, `${slot}-${SIZES[0]}.jpg`));
  const m = info.extmetadata || {};
  return { source: "Wikimedia Commons", title, author: strip(m.Artist && m.Artist.value), license: strip(m.LicenseShortName && m.LicenseShortName.value), url: info.descriptionurl };
}

async function fromUnsplash(id, slot) {
  for (const w of SIZES) {
    await download(`https://images.unsplash.com/photo-${id}?w=${w}&q=72&fm=jpg&fit=max`, path.join(OUT, `${slot}-${w}.jpg`));
  }
  return { source: "Unsplash", title: id, author: "Unsplash", license: "Unsplash License", url: `https://unsplash.com/photos/${id}`, sample: true };
}

module.exports = {
  async onPreBuild({ utils, constants }) {
    OUT = path.join(path.resolve(constants.PUBLISH_DIR || "."), "assets", "photos");
    fs.mkdirSync(OUT, { recursive: true });
    await utils.cache.restore(OUT);
    const creditsFile = path.join(OUT, "credits.json");
    const credits = fs.existsSync(creditsFile) ? JSON.parse(fs.readFileSync(creditsFile, "utf8")) : {};
    const used = new Set(Object.values(credits).map((cr) => JSON.stringify(cr.source === "Unsplash" ? { unsplash: cr.title } : { commons: cr.title })));
    const missing = [];
    for (const [slot, sources] of Object.entries(SLOTS)) {
      if (fs.existsSync(path.join(OUT, `${slot}-${SIZES[0]}.jpg`))) continue; // echtes Foto liegt schon da
      let ok = false;
      for (const src of sources) {
        const key = JSON.stringify(src);
        try {
          credits[slot] = src.commons ? await fromCommons(src.commons, slot) : await fromUnsplash(src.unsplash, slot);
          used.add(key);
          ok = true;
          break;
        } catch (e) {
          console.log(`  ${slot}: ${key} → ${e.message}`);
        }
      }
      if (!ok) missing.push(slot);
    }
    for (const slot of Object.keys(credits)) if (!SLOTS[slot]) delete credits[slot]; // nicht mehr genutzte Motive
    fs.writeFileSync(creditsFile, JSON.stringify(credits, null, 2));
    await utils.cache.save(OUT);
    const total = Object.keys(SLOTS).length;
    const summary = `${total - missing.length}/${total} Fotos geladen.` + (missing.length ? ` Fehlend (Platzhalter): ${missing.join(", ")}` : "");
    console.log(summary);
    utils.status.show({ title: "Fotos", summary, text: JSON.stringify(credits) });
  },
};
