"""Wohnungskarten (Startseite, Übersichten, „Weitere Wohnungen“)."""
from parts import HEART, esc, icon, slider

SIZES_CARD = "(min-width: 1100px) 400px, (min-width: 640px) 50vw, 100vw"


def card(prefix, a, delay=0):
    badge = f'<span class="badge">{a["badge"]}</span>' if a["badge"] else ""
    extra = badge + f'<button class="save-btn" type="button" data-save="{a["id"]}" aria-label="{esc(a["name"])} merken" aria-pressed="false">{HEART}</button>'
    rating = f'<span class="rating" title="{a["rating"][1]}">{icon("star", 13)} {a["rating"][0]}</span>' if a["rating"] else ""
    style = f' style="--d:{delay:.2f}s"' if delay else ""
    return f"""<article class="listing reveal" data-tags="{a["tags"]}"{style}>
  <a class="cover" href="{prefix}{a["path"]}" aria-label="{esc(a["name"])} ansehen"></a>
  {slider(prefix, a["slots"][:5], SIZES_CARD, extra)}
  <div class="listing-body">
    <div class="listing-top"><h3>{a["name"]}</h3>{rating}</div>
    <p>{a["place"]}</p>
    <p class="facts">{a["facts"]}</p>
    <p class="listing-cta"><strong>Wohnung ansehen</strong> · Preis auf Anfrage</p>
  </div>
</article>"""


def compare_table(prefix, apts):
    """Vergleich auf einen Blick – scanbar und für Suchmaschinen gut lesbar."""
    rows = []
    for a in apts:
        size = f'{a["size"]} m²' if a["size"] else "–"
        extra = [a["badge"]] if a["badge"] and a["badge"] != "Bis 8 Gäste" else []
        if a["parking"] == "own" and "Parkplatz" not in a["badge"]:
            extra.append("Parkplatz")
        if a["pets"] and "Hund" not in a["badge"]:
            extra.append("Hund willkommen")
        if a.get("floor_level") == "0":
            extra.append("Erdgeschoss")
        rows.append(f'<tr><th scope="row"><a class="u-link" href="{prefix}{a["path"]}">{a["name"]}</a></th>'
                    f'<td>{a["street"]}</td><td>{size}</td><td>{a["guests_label"]}</td><td>{", ".join(extra) or "–"}</td></tr>')
    return f"""<div class="table-wrap"><table class="compare">
  <caption class="sr-only">Vergleich der Ferienwohnungen</caption>
  <thead><tr><th scope="col">Wohnung</th><th scope="col">Lage</th><th scope="col">Größe</th><th scope="col">Gäste</th><th scope="col">Besonderes</th></tr></thead>
  <tbody>{"".join(rows)}</tbody>
</table></div>"""
