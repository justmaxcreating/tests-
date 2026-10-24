"""Lagekarten als Inline-SVG – aus echten Koordinaten, ohne externe Kartendienste (DSGVO, Ladezeit)."""
from geo_data import RIVER_CITY, RIVER_REGION
from data import APARTMENTS, LANDMARKS, THUENGEN, WUERZBURG
from parts import esc

FONT = 'font-family="Jakarta, sans-serif"'


class Proj:
    def __init__(self, lat_top, lat_bottom, lon_left, lon_right, width=800):
        import math
        self.lt, self.lb, self.ll, self.lr = lat_top, lat_bottom, lon_left, lon_right
        k = math.cos(math.radians((lat_top + lat_bottom) / 2))
        self.w = width
        self.h = round(width * (lat_top - lat_bottom) / ((lon_right - lon_left) * k))

    def __call__(self, lat, lon):
        x = (lon - self.ll) / (self.lr - self.ll) * self.w
        y = (self.lt - lat) / (self.lt - self.lb) * self.h
        return round(x, 1), round(y, 1)

    def path(self, pts):
        return "M" + " L".join(f"{x} {y}" for x, y in (self(*p) for p in pts))


CITY = Proj(49.8032, 49.7838, 9.9130, 9.9520)
REGION = Proj(49.9900, 49.7800, 9.6200, 10.0600)

# Beschriftung: (dx, dy, text-anchor)
LABEL = {
    "dom": (12, 4, "start"), "markt": (-12, -6, "end"), "bruecke": (-16, 5, "end"), "residenz": (12, 4, "start"),
    "kranen": (-16, 4, "end"), "hbf": (12, 4, "start"), "ccw": (12, 4, "start"), "kulturspeicher": (12, -8, "start"),
    "theater": (12, 4, "start"), "festung": (0, 24, "middle"), "talavera": (-12, 4, "end"),
}
SHORT = {"residenz": "Residenz", "kranen": "Alter Kranen", "talavera": "Talavera (P)", "kulturspeicher": "Kulturspeicher", "ccw": "Congress Centrum", "theater": "Theater"}


def _landmarks(proj, keys):
    out = []
    for k in keys:
        name, lat, lon = LANDMARKS[k]
        x, y = proj(lat, lon)
        dx, dy, anchor = LABEL[k]
        out.append(f'<g transform="translate({x} {y})"><circle r="6" fill="#fff" stroke="#3b3730" stroke-width="2"/>'
                   f'<text x="{dx}" y="{dy}" text-anchor="{anchor}">{SHORT.get(k, name)}</text></g>')
    return f'<g {FONT} font-size="13" font-weight="600" fill="#3b3730" paint-order="stroke" stroke="#ece7dd" stroke-width="4" stroke-linejoin="round">{"".join(out)}</g>'


def _river_city():
    bx1, by1 = CITY(49.79298, 9.9238)
    bx2, by2 = CITY(49.79298, 9.9276)
    return (f'<path d="{CITY.path(RIVER_CITY)}" stroke="#c3d2d0" stroke-width="44" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<line x1="{bx1}" y1="{by1}" x2="{bx2}" y2="{by2}" stroke="#cdb79a" stroke-width="9" stroke-linecap="round"/>'
            f'<text x="{CITY(49.7870, 9.9205)[0]}" y="{CITY(49.7870, 9.9205)[1]}" {FONT} font-size="13" font-style="italic" fill="#7c938f">Main</text>')


def _pin(x, y, title, sub, obstacles=()):
    """Pin mit Etikett. Das Etikett geht nach rechts oder links – dorthin, wo kein Orientierungspunkt verdeckt wird."""
    w = max(len(title), len(sub)) * 7.2 + 34

    def free(bx):
        x0, x1, y0, y1 = x + bx - 12, x + bx + w + 12, y - 54 - 12, y - 6 + 12
        return 8 <= x + bx and x + bx + w <= CITY.w - 8 and not any(x0 <= ox <= x1 and y0 <= oy <= y1 for ox, oy in obstacles)

    bx = next((c for c in (30, -30 - w) if free(c)), 30 if x + 30 + w <= CITY.w - 8 else -30 - w)
    return f"""<g transform="translate({x} {y})">
  <circle class="pulse" r="16" fill="#1f3b2d" opacity=".35"/>
  <g class="pin"><path d="M0 0c-16-18-22-28-22-38a22 22 0 0 1 44 0c0 10-6 20-22 38z" fill="#1f3b2d"/><circle cy="-38" r="8" fill="#fff"/></g>
  <g transform="translate({bx:.0f} -54)"><rect width="{w:.0f}" height="48" rx="14" fill="#fff" filter="drop-shadow(0 6px 14px rgba(22,20,15,.16))"/>
    <text x="16" y="21" {FONT} font-size="13" font-weight="700" fill="#16140f">{esc(title)}</text>
    <text x="16" y="37" {FONT} font-size="11.5" fill="#736d64">{esc(sub)}</text></g>
</g>"""


def city_map(prefix, focus=None):
    """Karte der Würzburger Innenstadt. focus = Wohnung (dict) → Pin mit Label; sonst alle Wohnungen nummeriert."""
    wue = [a for a in APARTMENTS if a["city"] == "wuerzburg"]
    keys = ["dom", "markt", "bruecke", "residenz", "kranen", "hbf", "ccw", "kulturspeicher", "festung"] + (["talavera"])
    if focus:
        keys = [k for k in keys if k != "kulturspeicher" or focus["id"] != "wue-kulturspeicher"]
    pins, seen = [], set()
    for i, a in enumerate(wue, 1):
        if focus and a["id"] == focus["id"]:
            continue
        x, y = CITY(*a["geo"])
        if (x, y) in seen:  # zwei Wohnungen im selben Haus (Bärengasse 2): Pin leicht versetzen
            x, y = x + 18, y - 14
        seen.add((x, y))
        if focus:
            pins.append(f'<a href="{prefix}{a["path"]}" aria-label="{esc(a["name"])}"><title>{esc(a["name"])}</title>'
                        f'<circle cx="{x}" cy="{y}" r="7" fill="#3b3730" stroke="#fff" stroke-width="2.5"/></a>')
        else:
            pins.append(f'<a href="{prefix}{a["path"]}" class="map-num" aria-label="{i}: {esc(a["name"])}"><title>{esc(a["name"])}</title>'
                        f'<circle cx="{x}" cy="{y}" r="14" fill="#1f3b2d" stroke="#fff" stroke-width="2.5"/>'
                        f'<text x="{x}" y="{y + 4.5}" text-anchor="middle" {FONT} font-size="12.5" font-weight="700" fill="#fff">{i}</text></a>')
    focus_svg = ""
    if focus:
        x, y = CITY(*focus["geo"])
        focus_svg = _pin(x, y, "Ihre Wohnung", focus["street"], [CITY(*LANDMARKS[k][1:]) for k in keys])
    label = f"Karte der Würzburger Innenstadt mit Lage der Ferienwohnung {focus['name']}" if focus else "Karte der Würzburger Innenstadt mit allen acht Ferienwohnungen"
    return f"""<svg viewBox="0 0 {CITY.w} {CITY.h}" role="img" aria-label="{esc(label)}">
  <rect width="{CITY.w}" height="{CITY.h}" fill="#ece7dd"/>
  {_river_city()}
  {_landmarks(CITY, keys)}
  {"".join(pins)}
  {focus_svg}
</svg>"""


TOWNS = [("Würzburg", WUERZBURG, 14, "start"), ("Veitshöchheim", (49.8317, 9.8800), -12, "end"),
         ("Karlstadt", (49.9606, 9.7722), -12, "end"), ("Arnstein", (49.9776, 9.9703), 12, "start")]


def region_map():
    rivers = "".join(f'<path d="{REGION.path(seg)}" stroke="#c3d2d0" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' for seg in RIVER_REGION)
    tx, ty = REGION(*THUENGEN)
    wx, wy = REGION(*WUERZBURG)
    towns = "".join(
        f'<g transform="translate({REGION(*p)[0]} {REGION(*p)[1]})"><circle r="{7 if n == "Würzburg" else 5}" fill="#fff" stroke="#3b3730" stroke-width="2"/>'
        f'<text x="{dx}" y="5" text-anchor="{an}" font-size="{15 if n == "Würzburg" else 13}">{n}</text></g>'
        for n, p, dx, an in TOWNS)
    mx, my = (tx + wx) / 2, (ty + wy) / 2
    return f"""<svg viewBox="0 0 {REGION.w} {REGION.h}" role="img" aria-label="Karte: Lage von Thüngen im Fränkischen Weinland, rund 25 km nördlich von Würzburg">
  <rect width="{REGION.w}" height="{REGION.h}" fill="#ece7dd"/>
  {rivers}
  <text x="{REGION(49.905, 9.800)[0]}" y="{REGION(49.905, 9.800)[1]}" {FONT} font-size="13" font-style="italic" fill="#7c938f">Main</text>
  <path d="M{tx} {ty} L{wx} {wy}" stroke="#1f3b2d" stroke-width="2" stroke-dasharray="6 7" fill="none"/>
  <g transform="translate({mx:.0f} {my:.0f})"><rect x="-44" y="-14" width="88" height="28" rx="14" fill="#fff"/><text y="5" text-anchor="middle" {FONT} font-size="12.5" font-weight="700" fill="#1f3b2d">ca. 25 km</text></g>
  <g {FONT} font-weight="600" fill="#3b3730" paint-order="stroke" stroke="#ece7dd" stroke-width="4" stroke-linejoin="round">{towns}</g>
  {_pin_region(tx, ty)}
</svg>"""


def _pin_region(x, y):
    return f"""<g transform="translate({x} {y})">
  <circle class="pulse" r="16" fill="#1f3b2d" opacity=".35"/>
  <g class="pin"><path d="M0 0c-16-18-22-28-22-38a22 22 0 0 1 44 0c0 10-6 20-22 38z" fill="#1f3b2d"/><circle cy="-38" r="8" fill="#fff"/></g>
  <g transform="translate(30 -54)"><rect width="168" height="48" rx="14" fill="#fff" filter="drop-shadow(0 6px 14px rgba(22,20,15,.16))"/>
    <text x="16" y="21" {FONT} font-size="13" font-weight="700" fill="#16140f">Thüngen</text>
    <text x="16" y="37" {FONT} font-size="11.5" fill="#736d64">Wohnen am Schlossberg</text></g>
</g>"""
