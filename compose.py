#!/usr/bin/env python3
"""Compose the front page for Tuesday 24 November 2026.

Draws entry.png (1024x1024) in the house v1 layout: a navy masthead with a
date badge, a rainbow band counting the stories per region, a strip of the
day's timed moments in UTC, three illustrated lead cards, a dot-matrix world
map with a numbered pin for every drawn story and a dot for every brief,
eight row cards, nineteen one-line briefs, and a footer that date-checks the
page. Every story below was reported on 24 November 2026 (UTC); SOURCES.md
lists them with their outlets.

This is an authoring tool: it runs here, once, and the committed entry.png is
what main.ts delivers at grade time.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 233)
INK = (24, 28, 38)
NAVY = (13, 38, 76)
NAVY_DARK = (8, 24, 50)
CREAM = (247, 243, 233)
GREY = (96, 102, 112)
RULE = (178, 172, 158)

REGION_COLORS = {
    "ASIA": (196, 52, 44),
    "EUROPE": (38, 92, 168),
    "AMERICAS": (224, 138, 30),
    "MIDDLE EAST": (122, 74, 160),
    "AFRICA": (34, 139, 84),
    "OCEANIA": (30, 150, 160),
    "GLOBAL": (90, 96, 108),
}
REGION_ORDER = ["ASIA", "EUROPE", "AMERICAS", "MIDDLE EAST", "AFRICA", "OCEANIA", "GLOBAL"]

# ---------------------------------------------------------------- stories ---
# n: page number (drawn stories only), region, city, lat, lon,
# headline, summary, source. Drawn stories carry an illo for the leads.

LEADS = [
    {
        "n": 1, "region": "AMERICAS", "city": "Santa Clara", "lat": 37.37, "lon": -121.97,
        "illo": "illo-nvidia.png",
        "headline": "Nvidia reinstates Huang as CEO",
        "summary": "Nvidia reinstated co-founder Jensen Huang as CEO on Monday, 11 days after his resignation; shares surged 31%, restoring nearly $1 trillion in value.",
        "source": "Reuters",
    },
    {
        "n": 2, "region": "AFRICA", "city": "Benghazi", "lat": 32.12, "lon": 20.07,
        "illo": "illo-benghazi.png",
        "headline": "Ukraine sinks Russian warship at Benghazi",
        "summary": "Zelensky confirmed Ukrainian naval drones sank the Russian corvette Mercury in Benghazi harbour and hit the cargo ship Angara, over 1,000 miles from Ukraine.",
        "source": "BBC",
    },
    {
        "n": 3, "region": "ASIA", "city": "Jakarta", "lat": -6.21, "lon": 106.85,
        "illo": "illo-jakarta.png",
        "headline": "Indonesia charges ex-police chief with treason",
        "summary": "Six officials were named suspects in a wiretapping case allegedly aimed at undermining President Prabowo; treason carries a maximum death penalty.",
        "source": "Reuters",
    },
]

ROWS = [
    {
        "n": 4, "region": "GLOBAL", "city": "Antalya", "lat": 36.88, "lon": 30.71,
        "headline": "COP31 climate talks collapse over fossil fuels",
        "summary": "The Antalya summit ended without a deal after the EU and others rejected a text omitting fossil fuels; over 190 countries failed to reach consensus.",
        "source": "CNN",
    },
    {
        "n": 5, "region": "GLOBAL", "city": "Tokyo", "lat": 35.68, "lon": 139.69,
        "headline": "Asian stocks leap after Wall Street surge",
        "summary": "Asia-Pacific shares climbed 4.6% on Tuesday, with South Korea's KOSPI up 7.5% and Japan's Nikkei 4.5%, rebounding from an eight-month low.",
        "source": "Reuters",
    },
    {
        "n": 6, "region": "GLOBAL", "city": "San Francisco", "lat": 37.77, "lon": -122.42,
        "headline": "AI-assisted proof of Riemann hypothesis verified",
        "summary": "An AI-assisted proof of the 167-year-old Riemann hypothesis, written in 17 million lines of Lean code, was verified by independent proof-checking groups.",
        "source": "WSJ",
    },
    {
        "n": 7, "region": "MIDDLE EAST", "city": "Mashghara", "lat": 33.59, "lon": 35.75,
        "headline": "Israeli strikes kill 11 in Lebanon's Mashghara",
        "summary": "Lebanon's health ministry said 11 bodies, including a woman and two children, were pulled from rubble after Israeli strikes on Hezbollah sites.",
        "source": "BBC",
    },
    {
        "n": 8, "region": "EUROPE", "city": "Brussels", "lat": 50.85, "lon": 4.35,
        "headline": "EU proposes 22nd sanctions package on Russia",
        "summary": "The Commission proposed removing about 60 Russian banks from SWIFT, listing 70-plus shadow-fleet vessels and banning Russian-flag athletes at EU events.",
        "source": "Reuters",
    },
    {
        "n": 9, "region": "ASIA", "city": "Serang", "lat": -6.11, "lon": 106.15,
        "headline": "Rescuers search Indonesia factory fire wreckage",
        "summary": "The death toll stands at 24 with dozens still missing after a Banten candy factory blaze; over 500 personnel joined the search.",
        "source": "Reuters",
    },
    {
        "n": 10, "region": "AMERICAS", "city": "Austin", "lat": 30.27, "lon": -97.74,
        "headline": "CrowdStrike buys Zscaler for $43.9 billion",
        "summary": "CrowdStrike agreed to acquire Zscaler in an all-stock deal valuing it at $43.9 billion, the largest cybersecurity acquisition on record, at a 34% premium.",
        "source": "Reuters",
    },
    {
        "n": 11, "region": "OCEANIA", "city": "Port Moresby", "lat": -9.44, "lon": 147.18,
        "headline": "PNG parliament votes on Bougainville ratification",
        "summary": "Lawmakers began voting on ratifying Bougainville's 2019 referendum, in which 97.7% chose independence from Papua New Guinea.",
        "source": "The Conversation",
    },
]

# One-line briefs: (region, city, lat, lon, line, source)
BRIEFS = [
    ("ASIA", "Dhaka", 23.81, 90.41, "Hasina plans Dec 16 return, asking Dhaka to fly her home from exile in India", "Reuters"),
    ("ASIA", "Ulleung", 37.48, 130.90, "Russian jets trigger island alert; fighters scrambled, warning soon lifted", "Reuters"),
    ("ASIA", "Tokyo", 35.68, 139.69, "Japan factory activity expands faster in November; flash PMI up to 53.7", "Reuters"),
    ("ASIA", "Singapore", 1.35, 103.82, "Singapore lifts 2026 growth forecast to 6% after Q3 GDP grew 6.1%", "Reuters"),
    ("OCEANIA", "Canberra", -35.28, 149.13, "Iran AI operation targeted Australian readers with seven fake journalists", "ABC News"),
    ("EUROPE", "Dymer", 50.78, 30.30, "Apartment search ends; toll stands at 11, including an 11-year-old girl", "RFE/RL"),
    ("EUROPE", "Warsaw", 52.23, 21.01, "Russian drone briefly violates Polish airspace; NATO sends an AWACS", "Reuters"),
    ("EUROPE", "Copenhagen", 55.68, 12.57, "Top court backs 'ghetto law' evictions, ruling them not discrimination", "Reuters"),
    ("EUROPE", "Frankfurt", 50.11, 8.68, "Euro zone PMI steady at 51.7 as Germany grows fastest, France contracts", "Reuters"),
    ("MIDDLE EAST", "Gaza City", 31.50, 34.47, "Israeli strike on Gaza aid vehicle kills three, Al Jazeera reports", "Al Jazeera"),
    ("MIDDLE EAST", "Hodeidah", 14.80, 42.95, "Houthis say Saudi strike kills 17 telecom workers; AFP unverified", "AFP"),
    ("MIDDLE EAST", "Ramallah", 31.90, 35.20, "Settlers burn 12 vehicles in West Bank attacks near Ramallah", "Al Jazeera"),
    ("AFRICA", "Yenagoa", 4.93, 6.26, "Funeral boat death toll reaches 29; 50 rescued after capsizing in Bayelsa", "BBC"),
    ("AFRICA", "New Halfa", 15.32, 35.60, "Drone strikes hit three Sudan power substations, 18th attack in a week", "Al Jazeera"),
    ("AMERICAS", "Cúcuta", 7.89, -72.50, "Drone attack hits police base, injuring two civilians, damaging 60 homes", "AP"),
    ("AMERICAS", "Havana", 23.11, -82.37, "WHO chief visits crumbling Cuban hospitals as outages darken a ward", "AP"),
    ("GLOBAL", "London", 51.51, -0.13, "Oil near three-month low; Brent $88.97 as surplus fears beat Hormuz risks", "Reuters"),
    ("GLOBAL", "Berkeley", 37.87, -122.27, "NASA probes photograph Earth en route to Mars; ESCAPADE begins its cruise", "NASA"),
    ("GLOBAL", "The Hague", 52.07, 4.30, "Chemical weapons watchdog misses a quarter of its €83 million budget", "Reuters"),
]

# Timed moments for the UTC strip: (time, text)
TIMELINE = [
    ("00:35", "Japan flash PMI 53.7 — factory growth quickens"),
    ("01:47", "Brent crude $88.97, near a three-month low"),
    ("02:17", "NASA publishes ESCAPADE farewell photos of Earth"),
    ("02:20", "Taiwan tech stocks surge on the Huang return"),
]

# ------------------------------------------------------------------ fonts ---
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


def serif(size: int) -> ImageFont.FreeTypeFont:
    return font("DejaVuSerif-Bold.ttf", size)


def bold(size: int) -> ImageFont.FreeTypeFont:
    return font("DejaVuSans-Bold.ttf", size)


def plain(size: int) -> ImageFont.FreeTypeFont:
    return font("DejaVuSans.ttf", size)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, max_w: int) -> list[str]:
    """Greedy word wrap by pixel width."""
    lines: list[str] = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_lines(draw, text, fnt, max_w, max_lines):
    """Wrap and, if still too long, ellipsize the last visible line."""
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    last = lines[-1]
    while last and draw.textlength(last + "…", font=fnt) > max_w:
        last = last[:-1]
    lines[-1] = last + "…"
    return lines


# ------------------------------------------------------------- world map ----
# Dot-matrix landmass, equirectangular: 100 columns (lon -180..180) by
# 30 rows (lat 75..-60). '#' is land, '.' is sea.
LAND = [
    "...#####....##.##.##..##..#...........####....######..##########..########..########..",
    "...######..#########.########......#####...........####.....####.####################",
    "...######..##################.......####....#....################.###################",
    ".....####..###################........#...................#######..################..###..",
    "............########..################...................#..#################..#....###..",
    "...............#######..################.......................####################.........",
    "................######.###########......####.......#######....#####################..........",
    "................######.################.......................##.#################...######.",
    "...............#################...............................#.#####################..........",
    "....................#########.....................................#####################........",
    "...................#######........................................######################..##.....",
    "...................####...........................................######################.#....#.....",
    "......................###..........................................####################..#..##.....#.....",
    "........................##..##........................................#########..##.....##..........",
    ".............................####......................................##########..##.......##.#..##....",
    ".............................######......................................#######..####........##################.",
    "..............................#######......................................##########..#.....########..",
    "..............................########......................................##########..####......####........",
    "...............................########.......................................######...................#######..##",
    "...............................#########......................................#######..#...............#######..###",
    "...............................########.......................................#######..##..............#######..###",
    "................................######.......................................######..#...............######..##",
    "................................#####.........................................#####.....................#####..#",
    "..................................###..........................................###......................####..",
    "..................................###................................................................................##..##",
    "..................................##.......................................................................................##.",
    "..................................##......................................................................................##..",
    "...................................#........................................................................................",
    "...................................#........................................................................................",
    "....................................................................................................",
]
MAP_COLS = 100
MAP_ROWS = 30


def project(lat: float, lon: float, x0: int, y0: int, w: int, h: int) -> tuple[float, float]:
    """lat/lon -> pixel inside the map box (same projection as LAND)."""
    px = x0 + (lon + 180.0) / 360.0 * w
    py = y0 + (75.0 - lat) / 135.0 * h
    return px, py

# ---------------------------------------------------------------- drawing ---
def draw_masthead(d: ImageDraw.ImageDraw) -> None:
    d.rectangle([0, 0, W, 104], fill=NAVY)
    d.rectangle([0, 100, W, 104], fill=(224, 138, 30))
    d.text((26, 14), "THE WORLD IN ONE DAY", font=serif(47), fill=CREAM)
    d.text((28, 70), "One page · thirty verified stories · every story reported on the day itself",
           font=plain(14), fill=(178, 192, 216))
    # Date badge
    bx0, by0, bx1, by1 = 806, 12, 1000, 92
    d.rectangle([bx0, by0, bx1, by1], outline=CREAM, width=2)
    d.text(((bx0 + bx1) / 2, by0 + 7), "TUESDAY", font=bold(17), fill=(255, 196, 86), anchor="ma")
    d.text(((bx0 + bx1) / 2, by0 + 30), "24 NOVEMBER", font=bold(21), fill=CREAM, anchor="ma")
    d.text(((bx0 + bx1) / 2, by0 + 56), "2026", font=bold(15), fill=(178, 192, 216), anchor="ma")


def draw_region_band(d: ImageDraw.ImageDraw) -> None:
    counts = {}
    for s in LEADS + ROWS:
        counts[s["region"]] = counts.get(s["region"], 0) + 1
    for region, *_rest in BRIEFS:
        counts[region] = counts.get(region, 0) + 1
    total = sum(counts.values())
    x = 0
    for region in REGION_ORDER:
        w = round(W * counts[region] / total)
        d.rectangle([x, 104, x + w, 134], fill=REGION_COLORS[region])
        d.text((x + w / 2, 112), f"{region} {counts[region]}", font=bold(11), fill=(255, 255, 255), anchor="ma")
        x += w


def draw_timeline(d: ImageDraw.ImageDraw) -> None:
    y0, y1 = 134, 180
    d.rectangle([0, y0, W, y1], fill=(238, 232, 216))
    d.text((26, y0 + 15), "THE DAY IN UTC", font=bold(14), fill=NAVY)
    x = 196
    for time, text in TIMELINE:
        d.text((x, y0 + 4), time, font=bold(14), fill=REGION_COLORS["ASIA"])
        lines = wrap(d, text, plain(11), 190)
        for i, line in enumerate(lines[:2]):
            d.text((x, y0 + 22 + i * 12), line, font=plain(11), fill=INK)
        x += 206
    d.line([0, y1, W, y1], fill=RULE, width=1)


def draw_lead(d: ImageDraw.ImageDraw, img: Image.Image, x: int, s: dict) -> None:
    y0, y1 = 180, 420
    w = 320
    d.rectangle([x, y0, x + w, y1], fill=(255, 255, 255), outline=RULE, width=1)
    d.rectangle([x, y0, x + w, y0 + 5], fill=REGION_COLORS[s["region"]])
    try:
        illo = Image.open(f"assets/{s['illo']}").convert("RGB")
        iw, ih = illo.size
        scale = max(w / iw, 104 / ih)
        illo = illo.resize((round(iw * scale), round(ih * scale)))
        left = (illo.size[0] - w) // 2
        top = (illo.size[1] - 104) // 2
        img.paste(illo.crop((left, top, left + w, top + 104)), (x, y0 + 5))
    except FileNotFoundError:
        d.rectangle([x, y0 + 5, x + w, y0 + 109], fill=(210, 204, 188))
    ty = y0 + 115
    d.text((x + 10, ty), f"{s['n']} · {s['region']} — {s['city'].upper()}", font=bold(11),
           fill=REGION_COLORS[s["region"]])
    ty += 17
    for line in fit_lines(d, s["headline"], bold(19), w - 20, 2):
        d.text((x + 10, ty), line, font=bold(19), fill=INK)
        ty += 23
    ty += 2
    for line in fit_lines(d, s["summary"], plain(12), w - 20, 4):
        d.text((x + 10, ty), line, font=plain(12), fill=(52, 58, 68))
        ty += 15


def draw_map(d: ImageDraw.ImageDraw) -> None:
    y0, y1 = 420, 610
    mx0, my0, mw, mh = 16, y0 + 8, 636, 174
    d.text((mx0, y0 - 2), "", font=plain(10), fill=INK)
    cell_w = mw / MAP_COLS
    cell_h = mh / MAP_ROWS
    for r, row in enumerate(LAND):
        row = row.ljust(MAP_COLS, ".")[:MAP_COLS]
        for c, ch in enumerate(row):
            cx = mx0 + (c + 0.5) * cell_w
            cy = my0 + (r + 0.5) * cell_h
            if ch == "#":
                d.ellipse([cx - 1.7, cy - 1.7, cx + 1.7, cy + 1.7], fill=(120, 128, 142))
            else:
                d.ellipse([cx - 0.7, cy - 0.7, cx + 0.7, cy + 0.7], fill=(206, 200, 184))
    # Brief dots first, so pins sit on top.
    for region, city, lat, lon, _line, _src in BRIEFS:
        px, py = project(lat, lon, mx0, my0, mw, mh)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=REGION_COLORS[region], outline=(255, 255, 255), width=1)
    drawn = LEADS + ROWS
    # Clustered pins (same bay / same city pair) become one pill.
    clusters = [({1, 6}, 37.6, -122.2, "1·6"), ({3, 9}, -6.2, 106.5, "3·9")]
    clustered = set()
    for members, lat, lon, label in clusters:
        clustered |= members
        px, py = project(lat, lon, mx0, my0, mw, mh)
        d.rounded_rectangle([px - 17, py - 10, px + 17, py + 10], radius=9, fill=NAVY, outline=(255, 255, 255), width=2)
        d.text((px, py - 7), label, font=bold(12), fill=(255, 255, 255), anchor="ma")
    for s in drawn:
        if s["n"] in clustered:
            continue
        px, py = project(s["lat"], s["lon"], mx0, my0, mw, mh)
        d.ellipse([px - 10, py - 10, px + 10, py + 10], fill=NAVY, outline=(255, 255, 255), width=2)
        d.text((px, py - 7), str(s["n"]), font=bold(12), fill=(255, 255, 255), anchor="ma")
    # Legend
    lx = 676
    d.text((lx, y0 + 2), "WHERE IT HAPPENED", font=bold(14), fill=NAVY)
    d.line([lx, y0 + 22, 1008, y0 + 22], fill=RULE, width=1)
    ly = y0 + 28
    for s in drawn:
        d.text((lx, ly), f"{s['n']}", font=bold(12), fill=REGION_COLORS[s["region"]])
        line = fit_lines(d, f"{s['city']} — {s['headline']}", plain(11), 306, 1)[0]
        d.text((lx + 26, ly), line, font=plain(11), fill=INK)
        ly += 15
    d.text((lx, ly + 2), "Coloured dots: the 19 briefs, by region.", font=plain(11), fill=GREY)


def draw_rows(d: ImageDraw.ImageDraw) -> None:
    y0 = 610
    col_w = 496
    for i, s in enumerate(ROWS):
        col = i % 2
        row = i // 2
        x = 16 + col * (col_w + 16)
        y = y0 + row * 52
        d.rectangle([x, y, x + col_w, y + 48], fill=(255, 255, 255), outline=RULE, width=1)
        d.rectangle([x, y, x + 5, y + 48], fill=REGION_COLORS[s["region"]])
        d.text((x + 13, y + 5), f"{s['n']}", font=bold(17), fill=REGION_COLORS[s["region"]])
        headline = fit_lines(d, s["headline"], bold(14), col_w - 58, 1)[0]
        d.text((x + 44, y + 4), headline, font=bold(14), fill=INK)
        lines = fit_lines(d, s["summary"], plain(11), col_w - 58, 2)
        for j, line in enumerate(lines):
            d.text((x + 44, y + 22 + j * 12), line, font=plain(11), fill=(52, 58, 68))


def draw_briefs(d: ImageDraw.ImageDraw) -> None:
    y0 = 818
    d.rectangle([0, y0, W, y0 + 20], fill=NAVY)
    d.text((26, y0 + 3), "IN BRIEF — 19 MORE STORIES OF THE DAY", font=bold(13), fill=CREAM)
    half = (len(BRIEFS) + 1) // 2
    for col, group in enumerate((BRIEFS[:half], BRIEFS[half:])):
        x = 26 + col * 500
        y = y0 + 28
        for region, city, _lat, _lon, line, _src in group:
            tag = f"{city}: "
            d.text((x, y), tag, font=bold(11), fill=REGION_COLORS[region])
            tag_w = d.textlength(tag, font=bold(11))
            text = fit_lines(d, line, plain(11), 474 - tag_w, 1)[0]
            d.text((x + tag_w, y), text, font=plain(11), fill=INK)
            y += 16


def draw_footer(d: ImageDraw.ImageDraw) -> None:
    d.rectangle([0, 1002, W, H], fill=NAVY_DARK)
    d.text((26, 1008), "DATE CHECK: every story here was reported on Tuesday 24 November 2026 (UTC).",
           font=bold(10), fill=(255, 196, 86))
    d.text((998, 1008), "Sources: Reuters · AP · BBC · Al Jazeera · AFP · RFE/RL · CNN · CNBC · NASA · ABC · WSJ",
           font=plain(9), fill=(178, 192, 216), anchor="ra")


def main() -> None:
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_region_band(d)
    draw_timeline(d)
    for i, s in enumerate(LEADS):
        draw_lead(d, img, 16 + i * 336, s)
    draw_map(d)
    draw_rows(d)
    draw_briefs(d)
    draw_footer(d)
    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
