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

const POOLS = {
  living: ["1502672260266-1c1ef2d93688", "1522708323590-d24dbb6b0267", "1493809842364-78817add7ffb", "1586023492125-27b2c045efd7", "1560448204-e02f11c3d0e2", "1600210492486-724fe5c67fb0"],
  bedroom: ["1505691938895-1758d7feb511", "1540518614846-7eded433c457", "1616594039964-ae9021a400a0", "1631049307264-da0ec9d70304", "1522771739844-6a9f6d5f14af"],
  kitchen: ["1556911220-bff31c812dba", "1484154218962-a197022b5858", "1556909114-f6e7ad7d3136", "1565538810643-b5bdb714032a"],
  bath: ["1552321554-5fefe8c9ef14", "1584622650111-993a426fbf0a", "1620626011761-996317b8d101"],
  dining: ["1617806118233-18e1de247200", "1615874959474-d609969a20ed", "1604578762246-41134e37f9cc"],
};
const pool = (name, ...fallback) => [...POOLS[name], ...fallback.flatMap((f) => POOLS[f])].map(u);

const SLOTS = {
  "wue-hero": [c("Würzburg, Festung Marienberg, Blick auf die Altstadt -- 2018 -- 0323.jpg"), c("Würzburg, die Alte Mainbrücke.JPG"), c("Wurzburg Marienberg Fortress on the Main in Würzburg.jpg")],
  "wue-bridge": [c("Alte Mainbrücke Würzburg 20180521 004.jpg"), c("View of the old bridge over Main in Wurzburg 01.jpg"), c("Würzburg, die Alte Mainbrücke.JPG")],
  "wue-festung": [c("Wurzburg Marienberg Fortress on the Main in Würzburg.jpg"), c("Würzburg; Festung Marienberg.jpg"), c("Marienberg wuerzburg.jpg")],
  "wue-residenz": [c("Würzburg Residenz Weltkulturerbe und Hofgarten.jpg"), c("Wuerzburger Residenz vom Hofgarten.jpg"), c("Residenz Wuerzburg Hofgarten.jpg")],
  "wue-hofgarten": [c("Würzburg, Residenz, Hofgarten -- 2018 -- 0181.jpg"), c("Orangerie Hofgarten Wuerzburg-1.jpg")],
  "wue-main": [c("Main Kutter Würzburg.jpg"), c("View of the old bridge over Main in Wurzburg 01.jpg")],
  "wein-stein": [c("Würzburger Stein.jpg"), u("1506377247377-2a5b3b417ebb")],
  "wein-bocksbeutel": [c("Franken Silvaner in Bocksbeutel.jpg"), c("Bocksbeutel.jpg"), u("1510812431401-41d2bd2722f3")],
  "thue-schloss": [c("Schloss Thüngen April 2021 05.jpg"), c("Thüngen, Schloss-001.jpg"), c("Schloss Thüngen.jpg")],
  "oak-wood": [c("Eiche (Holz).JPG"), c("Eichenholz.jpg")],
  // Innenräume = Beispielbilder, bis echte Fotos der Wohnungen vorliegen
  "int-living-1": pool("living"),
  "int-living-2": pool("living"),
  "int-living-3": pool("living", "dining"),
  "int-bedroom-1": pool("bedroom"),
  "int-bedroom-2": pool("bedroom"),
  "int-bedroom-3": pool("bedroom"),
  "int-kitchen-1": pool("kitchen"),
  "int-kitchen-2": pool("kitchen", "dining"),
  "int-bath-1": pool("bath"),
  "int-dining-1": pool("dining", "kitchen"),
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
        if (used.has(key) && slot.startsWith("int-")) continue; // Innenräume nicht doppelt
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
    fs.writeFileSync(creditsFile, JSON.stringify(credits, null, 2));
    await utils.cache.save(OUT);
    const total = Object.keys(SLOTS).length;
    const summary = `${total - missing.length}/${total} Fotos geladen.` + (missing.length ? ` Fehlend (Platzhalter): ${missing.join(", ")}` : "");
    console.log(summary);
    const report = [];
    // Optional: Fotos zur visuellen Kontrolle in eine Figma-Datei hochladen (einmalige Upload-URLs per Env-Var)
    if (process.env.PHOTO_CHECK_URLS) {
      const urls = JSON.parse(process.env.PHOTO_CHECK_URLS);
      const slots = Object.keys(SLOTS).filter((sl) => fs.existsSync(path.join(OUT, `${sl}-${SIZES[0]}.jpg`)));
      await Promise.all(slots.slice(0, urls.length).map(async (sl, i) => {
        try {
          const form = new FormData();
          form.append("file", new Blob([fs.readFileSync(path.join(OUT, `${sl}-${SIZES[0]}.jpg`))], { type: "image/jpeg" }), `${sl}.jpg`);
          const r = await fetch(urls[i], { method: "POST", body: form });
          report.push(`${sl}:${r.status}${r.ok ? "" : " " + (await r.text()).slice(0, 120)}`);
        } catch (e) {
          report.push(`${sl}:ERR ${e.message}`);
        }
      }));
    }
    utils.status.show({ title: "Fotos", summary, text: JSON.stringify(credits) });
    // Diagnose: Build bewusst abbrechen, damit das Ergebnis in der Deploy-Fehlermeldung steht (Live-Seite bleibt unverändert)
    if (process.env.PHOTO_REPORT) utils.build.failBuild(`REPORT ${summary} | Figma: ${report.join("; ") || "keine URLs"} | Credits: ${Object.entries(credits).map(([k, v]) => k + "=" + v.title).join("; ")}`);
  },
};
