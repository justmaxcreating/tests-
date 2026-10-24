// Lädt die Fotos lokal (wie das Netlify-Plugin beim Build), damit die Seite auch auf dem Laptop Bilder zeigt.
// Aufruf (aus dem Ordner fewo-relaunch):  node tools/fetch-photos-local.js
const path = require("path");
const plugin = require("../plugins/fetch-photos/index.js");
const noop = async () => {};
plugin
  .onPreBuild({
    constants: { PUBLISH_DIR: path.join(__dirname, "..") },
    utils: { cache: { restore: noop, save: noop }, status: { show: ({ summary }) => console.log(summary) } },
  })
  .catch((e) => { console.error(e); process.exit(1); });
