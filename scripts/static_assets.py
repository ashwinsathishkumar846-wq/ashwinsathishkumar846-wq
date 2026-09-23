#!/usr/bin/env python3
"""Render the editorial (hand-curated) panels of the profile.

Everything written here is transcribed from three sources and nothing else:
  - the resume (projects, awards, certifications, publication, education)
  - the portfolio at ashwin-portfolio-tan.vercel.app
  - the public repositories on GitHub (checked by hand for the "in public repos"
    markers in the stack panel)

Live numbers (repositories, contributions, commits, LeetCode) are NOT here; they
belong to scripts/generate_profile.py, which reads them from APIs on a schedule.

Run:  python scripts/static_assets.py
"""

import base64
import math
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import (BG, PANEL, PANEL_2, LINE, LINE_2, TEXT, MUTED, DIM, FAINT, RED, CYAN, BLUE,  # noqa: E402
                   VIOLET, TEAL, GOLD, SILVER, BRONZE, SANS, MONO, WIDE, NARROW,
                   t, lines, chip, chips, panel, brackets, node, flow, packet, header, iso_box,
                   stars, wordmark, wordmark_width, svg, write, wrap, text_w, ellipse_pt, esc)

OUT = "assets"
AVATAR = "https://avatars.githubusercontent.com/u/271384237?v=4&s=460"


def emit(name, builder):
    """Render one panel at both widths: assets/<name>.svg and assets/m/<name>.svg."""
    write(os.path.join(OUT, name + ".svg"), builder(WIDE))
    write(os.path.join(OUT, "m", name + ".svg"), builder(NARROW))


def centred_chips(cx, y, items, size=10.5, gap=8):
    """One centred row of chips."""
    widths = [text_w(s, size, True, 0.6) + 20 for s, _, _ in items]
    x = cx - (sum(widths) + gap * (len(items) - 1)) / 2
    out = ""
    for (s, col, filled), w in zip(items, widths):
        out += chip(x, y, s, col, size, filled)[0]
        x += w + gap
    return out


def arrow_head(x, y, colour, direction="right", s=5):
    if direction == "right":
        d = "M%.1f %.1fl-%d -%d v%d z" % (x, y, s, s * .8, s * 1.6)
    elif direction == "down":
        d = "M%.1f %.1fl-%.1f -%d h%.1f z" % (x, y, s * .8, s, s * 1.6)
    else:
        d = "M%.1f %.1fl%d -%.1f v%.1f z" % (x, y, s, s * .8, s * 1.6)
    return '<path d="%s" fill="%s"/>' % (d, colour)


# ======================================================================= HERO
def _avatar():
    try:
        req = urllib.request.Request(AVATAR, headers={"User-Agent": "profile-generator"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return base64.b64encode(r.read()).decode()
    except Exception as e:                                          # noqa: BLE001
        print("  ! avatar unavailable (%s) - rendering the core without it" % e)
        return None


AVATAR_B64 = None


def hero_defs(px, py, pw, ph):
    return (
        # Cutout: alpha from inverse brightness, so the photo's white studio
        # background drops out and only the portrait remains. Pixels are not
        # recoloured - the person is shown exactly as photographed.
        '<filter id="cut" x="0" y="0" width="100%%" height="100%%" color-interpolation-filters="sRGB">'
        '<feColorMatrix in="SourceGraphic" type="matrix" result="a" '
        'values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  -6 -6 -6 0 15.6"/>'
        '<feMorphology in="a" operator="erode" radius="1" result="e"/>'
        '<feGaussianBlur in="e" stdDeviation=".6" result="s"/>'
        '<feComposite in="SourceGraphic" in2="s" operator="in"/></filter>'
        '<radialGradient id="fadeb" cx=".5" cy=".36" r=".62">'
        '<stop offset=".62" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>'
        '<mask id="pm"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="url(#fadeb)"/></mask>'
        '<radialGradient id="halo" cx="50%%" cy="50%%" r="50%%">'
        '<stop offset="0" stop-color="%s" stop-opacity=".32"/><stop offset=".5" stop-color="%s" stop-opacity=".10"/>'
        '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="halo2" cx="50%%" cy="50%%" r="50%%">'
        '<stop offset="0" stop-color="%s" stop-opacity=".22"/><stop offset="1" stop-color="%s" stop-opacity="0"/>'
        '</radialGradient>'
        '<linearGradient id="namefill" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#c9ccd3"/></linearGradient>'
        '<linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="%s" stop-opacity="0"/><stop offset="1" stop-color="%s"/></linearGradient>'
        % (px, py, pw, ph, RED, RED, RED, CYAN, CYAN, BG, BG))


def portrait(cx, top, size):
    """The GitHub avatar as a cut-out portrait, lit from behind."""
    o = '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="url(#halo)"/>' % (cx, top + size * .42, size * .62)
    o += '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="url(#halo2)"/>' % (cx + size * .22, top + size * .3, size * .4)
    # one thin ring behind the head - the only orbital gesture left
    r = size * .43
    o += ('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-opacity=".35" '
          'stroke-dasharray="2 6" class="orbit"/>' % (cx, top + size * .4, r, TEXT))
    o += ('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-opacity=".12"/>'
          % (cx, top + size * .4, r + 16, TEXT))
    o += node(cx + r * math.cos(math.radians(-38)), top + size * .4 + r * math.sin(math.radians(-38)), 3, RED, True)
    if AVATAR_B64:
        o += ('<g mask="url(#pm)"><image x="%.1f" y="%.1f" width="%.1f" height="%.1f" filter="url(#cut)" '
              'preserveAspectRatio="xMidYMid slice" href="data:image/jpeg;base64,%s"/></g>'
              % (cx - size / 2, top, size, size, AVATAR_B64))
        # The face itself is drawn again unfiltered, so a bright skin highlight
        # can never be mistaken for background and punched out.
        o += ('<clipPath id="face"><ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f"/></clipPath>'
              '<image x="%.1f" y="%.1f" width="%.1f" height="%.1f" clip-path="url(#face)" '
              'preserveAspectRatio="xMidYMid slice" href="data:image/jpeg;base64,%s"/>'
              % (cx, top + size * .41, size * .125, size * .165, cx - size / 2, top, size, size, AVATAR_B64))
    return o


FACTS = [("EDUCATION", "B.E. CSE · 2024–28"), ("HACKATHONS", "2× FIRST PRIZE"), ("RESEARCH", "IEEE ICCPCT 2026")]
DISCIPLINES = "AI / ML   ·   NLP   ·   SOFTWARE   ·   DATA   ·   SYSTEMS"
TAG1, TAG2 = "Building practical intelligent systems", "for real-world problems."


def name(x, y, size, width):
    """The name in the display face, pinned to an exact width with textLength so
    it lands identically whichever system font renders it. The red full stop
    is the portfolio's signature mark."""
    return ('<text x="%d" y="%d" font-family="%s" font-size="%d" font-weight="800" fill="url(#namefill)" '
            'textLength="%d" lengthAdjust="spacingAndGlyphs">ASHWIN S</text>'
            '<text x="%d" y="%d" font-family="%s" font-size="%d" font-weight="800" fill="%s">.</text>'
            % (x, y, SANS, size, width, x + width + 4, y, SANS, size, RED))


def hero(W):
    b = []
    if W == WIDE:
        H = 460
        pcx, ptop, psz = 712, 30, 440
        b.append(stars(W, H, 50, 5, "#b9c2d0"))
        b.append(portrait(pcx, ptop, psz))
        b.append('<rect x="0" y="%d" width="%d" height="90" fill="url(#ground)"/>' % (H - 90, W))
        b.append(t(44, 58, "PORTFOLIO // 2026", 10, DIM, MONO, None, "600", 3))
        b.append('<rect x="44" y="96" width="22" height="2" fill="%s"/>' % RED)
        b.append(t(76, 101, "THIRD-YEAR CSE · SREC, COIMBATORE", 10.5, MUTED, MONO, None, None, 2))
        b.append(name(40, 196, 96, 450))
        b.append(t(44, 232, "COMPUTER SCIENCE ENGINEER", 16, TEXT, SANS, None, "600", 6))
        b.append(t(44, 282, TAG1, 22, TEXT, SANS, None, "300"))
        b.append(t(44, 310, TAG2, 22, DIM, SANS, None, "300"))
        b.append(t(44, 344, DISCIPLINES, 10.5, CYAN, MONO, None, "600", 1.6))
        y = 372
        b.append('<rect x="44" y="%d" width="480" height="1" fill="%s"/>' % (y, LINE_2))
        for i, (k, v) in enumerate(FACTS):
            x = 44 + i * 164
            if i:
                b.append('<rect x="%d" y="%d" width="1" height="42" fill="%s"/>' % (x - 12, y + 12, LINE_2))
            b.append(t(x, y + 28, k, 9, DIM, MONO, None, "600", 2))
            b.append(t(x, y + 50, v, 12, GOLD if i == 1 else TEXT, MONO, None, "700", .6))
    else:
        pcx, ptop, psz = 220, 34, 330
        b.append(stars(W, 700, 40, 5, "#b9c2d0"))
        b.append(portrait(pcx, ptop, psz))
        b.append(t(24, 42, "PORTFOLIO // 2026", 10, DIM, MONO, None, "600", 2.4))
        y0 = ptop + psz + 18
        b.append('<rect x="24" y="%d" width="18" height="2" fill="%s"/>' % (y0 - 4, RED))
        b.append(t(50, y0, "THIRD-YEAR CSE · SREC COIMBATORE", 10.5, MUTED, MONO, None, None, 1.4))
        b.append(name(20, y0 + 78, 72, 360))
        b.append(t(24, y0 + 108, "COMPUTER SCIENCE ENGINEER", 14, TEXT, SANS, None, "600", 4.4))
        b.append(t(24, y0 + 146, TAG1, 19, TEXT, SANS, None, "300"))
        b.append(t(24, y0 + 170, TAG2, 19, DIM, SANS, None, "300"))
        b.append(t(24, y0 + 200, "AI/ML · NLP · SOFTWARE · DATA · SYSTEMS", 10.5, CYAN, MONO, None, "600", 1))
        y = y0 + 220
        b.append('<rect x="24" y="%d" width="%d" height="1" fill="%s"/>' % (y, W - 48, LINE_2))
        cw = (W - 48) / 3.0
        for i, (k, v) in enumerate(FACTS):
            x = 24 + i * cw
            b.append(t(x, y + 22, k, 8.5, DIM, MONO, None, "600", 1.4))
            b.append(t(x, y + 40, v.replace(" · ", " "), 10, GOLD if i == 1 else TEXT, MONO, None, "700"))
        H = int(y + 62)
    return svg(W, H, "".join(b),
               "Ashwin S, Computer Science Engineer. Third-year B.E. CSE student at Sri Ramakrishna Engineering "
               "College, Coimbatore, 2024 to 2028. AI and ML, NLP, software, data and systems. Building practical "
               "intelligent systems for real-world problems. Two hackathon first prizes; IEEE ICCPCT 2026 paper.",
               hero_defs(pcx - psz / 2, ptop, psz, psz))


# ============================================================ LINK BUTTONS
def button(label, w, primary=False):
    h = 44
    col = RED if primary else LINE_2
    fill = "#1a0c0c" if primary else PANEL
    body = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" role="img" '
            'aria-label="%s"><title>%s</title>' % (w, h, w, h, esc(label), esc(label)))
    body += ('<defs><linearGradient id="e" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
             '<stop offset=".5" stop-color="#fff" stop-opacity=".25"/><stop offset="1" stop-color="#fff" '
             'stop-opacity="0"/></linearGradient></defs>')
    body += ('<rect x=".5" y=".5" width="%d" height="%d" rx="10" fill="%s" stroke="%s"/>'
             '<rect x="12" y=".5" width="%d" height="1" fill="url(#e)"/>' % (w - 1, h - 1, fill, col, w - 24))
    body += '<circle cx="18" cy="22" r="3" fill="%s"/>' % (RED if primary else CYAN)
    body += t(30, 26.5, label, 11.5, TEXT, MONO, None, "600", 2)
    body += ('<path d="M%d 27l8-8M%d 19h6v6" fill="none" stroke="%s" stroke-width="1.6"/>'
             % (w - 26, w - 22, TEXT if primary else MUTED))
    return body + "</svg>"


# ========================================================= ENGINEERING CORE
SUBSYSTEMS = [
    ("SYS.01", "ARTIFICIAL INTELLIGENCE", VIOLET, "Transformer NLP · sentiment and behavioral modeling", "RESUME"),
    ("SYS.02", "MACHINE LEARNING", CYAN, "CatBoost regression · predictive and geospatial analytics", "RESUME"),
    ("SYS.03", "AGENTIC AI", VIOLET, "multi-agent decision framework · ServiceNow AI Agents", "RESUME"),
    ("SYS.04", "SOFTWARE ENGINEERING", BLUE, "React · FastAPI · Express · Next.js, shipped to Vercel", "RESUME + GITHUB"),
    ("SYS.05", "DATA SYSTEMS", TEAL, "SQL · PostgreSQL · SQLite · Pandas · NumPy pipelines", "RESUME + GITHUB"),
    ("SYS.06", "SECURITY / SYSTEMS", RED, "hardened API: Helmet · JWT · rate limits · Docker", "GITHUB"),
]


def processor(cx, cy, k):
    """Isometric core: a three-tier platter stack with a floating chip on top."""
    out = []
    for rx, ry in ((175, 46), (135, 35), (95, 25)):
        out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="none" stroke="%s" '
                   'stroke-opacity=".35" class="orbit"/>' % (cx, cy + 70 * k, rx * k, ry * k, CYAN))
    for i, (rx, ry, h) in enumerate(((118, 32, 16), (98, 26, 14), (78, 21, 12))):
        top = cy + (44 - i * 26) * k
        rx, ry, h = rx * k, ry * k, h * k
        out.append('<path d="M%.1f %.1fv%.1fa%.1f %.1f 0 0 0 %.1f 0v-%.1f" fill="#0b0f16" stroke="%s" '
                   'stroke-opacity=".8"/>' % (cx - rx, top, h, rx, ry, 2 * rx, h, LINE_2))
        out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" stroke-opacity="%s"/>'
                   % (cx, top, rx, ry, PANEL_2, [CYAN, BLUE, VIOLET][i], [".45", ".55", ".7"][i]))
    # chip: iso diamond with side faces
    s, hh = 46 * k, 12 * k
    ty = cy - 30 * k
    out.append('<path d="M%.1f %.1fl%.1f %.1fv%.1fl-%.1f %.1fz" fill="#0d1a2b" stroke="%s" stroke-opacity=".6"/>'
               % (cx - s, ty, s, s / 2, hh, s, -s / 2, CYAN))
    out.append('<path d="M%.1f %.1fl%.1f %.1fv%.1fl%.1f %.1fz" fill="#091220" stroke="%s" stroke-opacity=".6"/>'
               % (cx + s, ty, -s, s / 2, hh, s, -s / 2, CYAN))
    out.append('<path d="M%.1f %.1fl%.1f %.1fl%.1f %.1fl%.1f %.1fz" fill="#0f2238" stroke="%s" stroke-width="1.3"/>'
               % (cx, ty - s / 2, s, s / 2, -s, s / 2, -s, -s / 2, CYAN))
    out.append('<path d="M%.1f %.1fl%.1f %.1fl%.1f %.1fl%.1f %.1fz" fill="none" stroke="%s" stroke-opacity=".5"/>'
               % (cx, ty - s / 4, s / 2, s / 4, -s / 2, s / 4, -s / 2, -s / 4, CYAN))
    out.append('<g transform="translate(%.1f %.1f) scale(1 .5) rotate(45)">%s</g>'
               % (cx, ty, t(0, 3.5, "CORE", 10 * k, TEXT, MONO, "middle", "700", 2)))
    # light column
    out.append('<rect x="%.1f" y="%.1f" width="2" height="%.1f" fill="url(#col)"/>' % (cx - 1, ty - 120 * k, 110 * k))
    out.append(node(cx, ty - 122 * k, 3.4, CYAN))
    return "".join(out)


def core(W):
    defs = ('<linearGradient id="col" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s" stop-opacity="0"/>'
            '<stop offset="1" stop-color="%s" stop-opacity=".9"/></linearGradient>'
            '<radialGradient id="aura"><stop offset="0" stop-color="%s" stop-opacity=".18"/>'
            '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (CYAN, CYAN, BLUE, BLUE))
    b = []
    if W == WIDE:
        H = 520
        cx, cy = 450, 300
        b.append(header(W, "02", "ENGINEERING CORE", "SIX SUBSYSTEMS · EACH TIED TO EVIDENCE"))
        b.append('<circle cx="%d" cy="%d" r="230" fill="url(#aura)"/>' % (cx, cy))
        cw, ch = 238, 96
        for i, (sid, name, col, ev, src) in enumerate(SUBSYSTEMS):
            left = i < 3
            x = 28 if left else W - 28 - cw
            y = 88 + (i % 3) * 128
            mx = x + cw if left else x
            my = y + ch / 2
            ex = cx - 70 if left else cx + 70
            d = "M%.1f %.1fC%.1f %.1f %.1f %.1f %.1f %.1f" % (mx, my, (mx + ex) / 2, my, (mx + ex) / 2, cy, ex, cy)
            b.append(flow(d, col, ".6"))
            b.append(panel(x, y, cw, ch, col))
            b.append(t(x + 18, y + 26, sid, 10, DIM, MONO, None, None, 1.6))
            b.append(t(x + cw - 16, y + 26, src, 9, col, MONO, "end", "600", 1.2))
            b.append(t(x + 18, y + 50, name, 13.5, TEXT, SANS, None, "700", 1.1))
            b.append(lines(x + 18, y + 70, wrap(ev, 32), 10.5, MUTED, MONO, 15))
            b.append(node(mx, my, 3, col, False))
        b.append(packet("M266 136C340 136 340 300 380 300", VIOLET, 3.2))
        b.append(packet("M634 392C560 392 560 300 520 300", TEAL, 3.6, begin="1.2s"))
        b.append(processor(cx, cy, 1.0))
        b.append(t(cx, 462, "ASHWIN // ENGINEERING CORE", 11.5, TEXT, MONO, "middle", "600", 3))
        b.append(t(cx, 482, "AI · SOFTWARE · DATA · SYSTEMS", 10, DIM, MONO, "middle", None, 2.4))
    else:
        cx, cy = 220, 200
        b.append(header(W, "02", "ENGINEERING CORE", "", x=20))
        b.append('<circle cx="%d" cy="%d" r="170" fill="url(#aura)"/>' % (cx, cy))
        b.append(processor(cx, cy, 0.86))
        b.append(t(cx, 312, "ASHWIN // ENGINEERING CORE", 11, TEXT, MONO, "middle", "600", 2.6))
        y0, ch, gap = 340, 92, 12
        bus_x = 24
        last_mid = y0 + 5 * (ch + gap) + ch / 2
        b.append(flow("M%d 262C%d 262 %d 300 %d 330V%.1f" % (cx - 60, bus_x + 20, bus_x, bus_x, last_mid), CYAN))
        for i, (sid, name, col, ev, src) in enumerate(SUBSYSTEMS):
            y = y0 + i * (ch + gap)
            x, cw = 44, W - 64
            b.append('<path d="M%d %.1fH%d" stroke="%s" stroke-opacity=".6"/>' % (bus_x, y + ch / 2, x, col))
            b.append(node(bus_x, y + ch / 2, 3, col, False))
            b.append(panel(x, y, cw, ch, col))
            b.append(t(x + 16, y + 24, sid, 10, DIM, MONO, None, None, 1.4))
            b.append(t(x + cw - 14, y + 24, src, 9, col, MONO, "end", "600", 1))
            b.append(t(x + 16, y + 48, name, 13.5, TEXT, SANS, None, "700", 1))
            b.append(lines(x + 16, y + 68, wrap(ev, 44), 10.5, MUTED, MONO, 15))
        H = int(y0 + 6 * (ch + gap) + 20)
    return svg(W, H, "".join(b),
               "Engineering core: six subsystems. Artificial intelligence (Transformer NLP), machine learning "
               "(CatBoost, predictive and geospatial analytics), agentic AI (multi-agent decision framework), "
               "software engineering (React, FastAPI, Express, Next.js), data systems (SQL, PostgreSQL, SQLite, "
               "Pandas, NumPy) and security/systems (hardened Express API).", defs)


# ==================================================== PROJECT CONSTELLATION
# Edges are only the relationships the resume states (a project's stack/domain),
# plus the publication's shared domain with the satellite project.
CONST_NODES = {
    # id: (label, kind, colour, wide xy, narrow xy)
    "P01": ("WORKFORCE CONTRIBUTION MONITOR", "project", CYAN, (170, 185), (150, 235)),
    "P02": ("SATELLITE WATER QUALITY", "project", TEAL, (400, 345), (240, 500)),
    "P03": ("AI FEEDBACK INTELLIGENCE", "project", VIOLET, (735, 185), (200, 760)),
    "SW": ("SOFTWARE", "domain", BLUE, (455, 105), (320, 125)),
    "DATA": ("DATA", "domain", TEAL, (318, 250), (350, 290)),
    "ML": ("MACHINE LEARNING", "domain", CYAN, (565, 262), (110, 400)),
    "NLP": ("NLP", "domain", VIOLET, (852, 112), (370, 700)),
    "AG": ("AGENTIC AI", "domain", VIOLET, (650, 80), (70, 680)),
    "GEO": ("GEOSPATIAL", "domain", TEAL, (175, 365), (70, 560)),
    "PUB": ("IEEE ICCPCT 2026", "research", GOLD, (660, 395), (345, 440)),
    "GH": ("PUBLIC REPOSITORIES", "repos", RED, (270, 70), (100, 110)),
}
CONST_EDGES = [("P01", "SW"), ("P01", "DATA"), ("P01", "ML"),
               ("P02", "ML"), ("P02", "DATA"), ("P02", "GEO"), ("P02", "PUB"),
               ("P03", "NLP"), ("P03", "AG"), ("P03", "SW"), ("P03", "DATA"),
               ("GH", "SW")]
CONST_SUB = {"P01": "React · FastAPI · SQLAlchemy", "P02": "CatBoost · Pandas · NumPy",
             "P03": "Transformers · FastAPI · PostgreSQL", "PUB": "research paper",
             "GH": "live apps · see below"}


def constellation(W):
    wide = W == WIDE
    H = 500 if wide else 900
    pos = {k: (v[3] if wide else v[4]) for k, v in CONST_NODES.items()}
    b = [stars(W, H, 110 if wide else 120, 11)]
    b.append(header(W, "04", "PROJECT CONSTELLATION", "PROJECTS · DOMAINS · RESEARCH" if wide else "",
                    x=28 if wide else 20))
    for a, c in CONST_EDGES:
        (x1, y1), (x2, y2) = pos[a], pos[c]
        col = CONST_NODES[a][2]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - 18
        d = "M%.1f %.1fQ%.1f %.1f %.1f %.1f" % (x1, y1, mx, my, x2, y2)
        if c == "PUB":
            b.append(flow(d, GOLD, ".85", 1.4, "flow"))
            b.append(t(mx, my - 4, "SHARED DOMAIN", 9.5, GOLD, MONO, "middle", "600", 1.6))
        else:
            b.append(flow(d, col, ".45", 1, "flow-slow", ".16"))
    for key, (label, kind, col, _, _) in CONST_NODES.items():
        x, y = pos[key]
        if kind == "project":
            b.append('<circle cx="%.1f" cy="%.1f" r="46" fill="%s" opacity=".08" filter="url(#glow)"/>' % (x, y, col))
            b.append('<circle cx="%.1f" cy="%.1f" r="34" fill="none" stroke="%s" stroke-opacity=".5" class="orbit"/>'
                     % (x, y, col))
            b.append('<circle cx="%.1f" cy="%.1f" r="22" fill="%s" stroke="%s" stroke-width="1.4"/>' % (x, y, PANEL, col))
            b.append(t(x, y + 4.5, key, 12, col, MONO, "middle", "700", 1))
            nm = wrap(label, 18)
            ly = y + 54
            for i, row in enumerate(nm):
                b.append(t(x, ly + i * 16, row, 11.5, TEXT, MONO, "middle", "600", 1.2))
            b.append(t(x, ly + len(nm) * 16 + 2, CONST_SUB[key], 10, DIM, MONO, "middle"))
        elif kind == "domain":
            b.append(node(x, y, 4, col, True, "d2"))
            b.append(t(x, y - 12, label, 10.5, col, MONO, "middle", "600", 1.6))
        elif kind == "research":
            b.append('<path d="M%.1f %.1fl12 12-12 12-12-12z" fill="%s" fill-opacity=".15" stroke="%s" '
                     'stroke-width="1.4"/>' % (x, y - 12, GOLD, GOLD))
            b.append(t(x, y + 32, label, 11, GOLD, MONO, "middle", "700", 1.4))
            b.append(t(x, y + 47, CONST_SUB[key], 10, DIM, MONO, "middle"))
        else:
            b.append('<rect x="%.1f" y="%.1f" width="20" height="20" rx="4" fill="%s" fill-opacity=".12" stroke="%s" '
                     'stroke-width="1.3" transform="rotate(45 %.1f %.1f)"/>' % (x - 10, y - 10, RED, RED, x, y))
            b.append(t(x + (0 if not wide else 0), y + 32, label, 10.5, TEXT, MONO, "middle", "600", 1.4))
            b.append(t(x, y + 47, CONST_SUB[key], 10, DIM, MONO, "middle"))
    ly = H - 22
    if wide:
        b.append('<rect x="28" y="%d" width="%d" height="1" fill="url(#hair)"/>' % (ly - 20, W - 56))
        b.append(t(28, ly, "● PROJECT   ○ DOMAIN   ◆ RESEARCH   ◇ GITHUB", 10, DIM, MONO, None, None, 1.2))
        b.append(t(W - 28, ly, "EDGES = STACK AND DOMAINS STATED FOR EACH PROJECT", 10, FAINT, MONO, "end", None, 1.2))
    else:
        b.append(t(20, ly, "● PROJECT  ○ DOMAIN  ◆ RESEARCH  ◇ GITHUB", 10, DIM, MONO, None, None, 1))
    return svg(W, H, "".join(b),
               "Project constellation. Project 01 Workforce Contribution Monitor links to software, data and "
               "machine learning. Project 02 Satellite Water Quality links to machine learning, data and geospatial "
               "analytics, and shares its domain with the IEEE ICCPCT 2026 paper. Project 03 AI Customer Feedback "
               "Intelligence links to NLP, agentic AI, software and data. Public GitHub repositories link to software.")


# ============================================================ PROJECT CARDS
PROJECTS = {
    "project-01": dict(
        idx="01", colour=CYAN, title=("WORKFORCE", "CONTRIBUTION MONITOR"),
        kicker="MEASURING IMPACT, NOT PRESENCE",
        problem="Conventional productivity tools equate online presence with real output, producing biased "
                "reviews that overlook the actual impact of an employee's work.",
        built="Full-stack system scoring task completion and work impact from multi-source, real-time data.",
        stack=["Python", "React.js", "FastAPI", "SQLAlchemy", "SQL", "Machine Learning", "Data Analytics"],
        viz="WORKFORCE INTELLIGENCE CORE"),
    "project-02": dict(
        idx="02", colour=TEAL, title=("SATELLITE WATER QUALITY", "MONITORING & PREDICTION"),
        kicker="WATER QUALITY WITHOUT FIELD SAMPLING",
        problem="Ground-based water quality assessment is slow, spatially sparse, and hard to scale across "
                "large regions and long time periods.",
        built="CatBoost pipeline predicting water-quality parameters from satellite imagery and geospatial data.",
        stack=["Python", "CatBoost", "Pandas", "NumPy", "Geospatial Analytics"],
        viz="ORBITAL SENSING PIPELINE"),
    "project-03": dict(
        idx="03", colour=VIOLET, title=("AI CUSTOMER FEEDBACK", "INTELLIGENCE & RETENTION"),
        kicker="CATCHING CHURN BEFORE IT HAPPENS",
        problem="Businesses lose revenue when dissatisfied customers churn silently, and manual review is too "
                "slow to intervene.",
        built="Transformer NLP flags churn risk; a multi-agent framework recommends refunds, escalations or offers.",
        stack=["Python", "NLP · Transformers", "FastAPI", "React", "PostgreSQL", "WhatsApp API"],
        viz="RETENTION DECISION ENGINE"),
}


def box(x, y, w, h, label, col, sub=None, size=10.5):
    out = iso_box(x, y, w, h, 8, PANEL_2, "#080a0e", "#171b25")
    out += '<rect x="%.1f" y="%.1f" width="%.1f" height="2" fill="%s" opacity=".85"/>' % (x, y, w, col)
    ty = y + h / 2 + (size * .36 if not sub else -2)
    out += t(x + w / 2, ty, label, size, TEXT, MONO, "middle", "600", 1)
    if sub:
        out += t(x + w / 2, ty + 15, sub, 9.5, DIM, MONO, "middle")
    return out


def viz_workforce(ox, oy):
    """Sources -> ingest -> normalise -> scoring (activity vs impact) -> dashboard."""
    c = CYAN
    o = []
    o.append(box(ox, oy + 40, 104, 40, "COMMS", c, "platform data"))
    o.append(box(ox, oy + 108, 104, 40, "EXECUTION", c, "platform data"))
    o.append(box(ox + 156, oy + 72, 110, 44, "INGESTION", c, "real-time"))
    o.append(box(ox + 318, oy + 72, 130, 44, "NORMALIZATION", c, "multi-source"))
    for sy in (60, 128):
        o.append(flow("M%d %dC%d %d %d %d %d %d" % (ox + 112, oy + sy, ox + 136, oy + sy, ox + 136, oy + 94,
                                                    ox + 154, oy + 94), c))
    o.append(flow("M%d %dH%d" % (ox + 274, oy + 94, ox + 316), c))
    o.append(arrow_head(ox + 316, oy + 94, c))
    # scoring engine
    sx, sy = ox + 238, oy + 170
    o.append(flow("M%d %dV%d" % (ox + 383, oy + 124, sy - 2), c))
    o.append(arrow_head(ox + 383, sy - 2, c, "down"))
    o.append(iso_box(sx, sy, 210, 76, 8, PANEL_2, "#080a0e", "#171b25"))
    o.append('<rect x="%d" y="%d" width="210" height="2" fill="%s"/>' % (sx, sy, c))
    o.append(t(sx + 12, sy + 20, "CUSTOM SCORING", 10.5, TEXT, MONO, None, "600", 1.2))
    for i, (lab, col) in enumerate((("ACTIVITY", DIM), ("IMPACT", c))):
        yy = sy + 38 + i * 20
        o.append(t(sx + 12, yy + 4, lab, 9.5, col, MONO, None, "600", 1))
        segs = "".join('<rect x="%d" y="%d" width="8" height="8" rx="1.5" fill="%s" opacity="%s"/>'
                       % (sx + 82 + j * 11, yy - 4, col, ".9" if i else ".45") for j in range(10))
        o.append(segs)
    o.append(t(sx + 200, sy + 56, "≠", 16, RED, SANS, "end", "700"))
    # dashboard
    dx, dy = ox, oy + 178
    o.append(flow("M%d %dH%d" % (sx - 2, sy + 38, dx + 184), c))
    o.append(arrow_head(dx + 184, sy + 38, c, "left"))
    o.append(iso_box(dx, dy, 184, 68, 8, PANEL_2, "#080a0e", "#171b25"))
    o.append(t(dx + 10, dy + 16, "REACT DASHBOARD", 9.5, TEXT, MONO, None, "600", 1))
    for i in range(3):
        o.append('<rect x="%d" y="%d" width="50" height="34" rx="3" fill="none" stroke="%s" stroke-opacity=".45"/>'
                 % (dx + 10 + i * 57, dy + 25, c))
    o.append('<path d="M%d %dl10-8 10 4 10-12 10 6" fill="none" stroke="%s" stroke-width="1.4"/>'
             % (dx + 15, dy + 50, c))
    o.append(packet("M%d %dC%d %d %d %d %d %dH%d V%d" % (ox + 112, oy + 60, ox + 136, oy + 60, ox + 136, oy + 94,
                                                        ox + 154, oy + 94, ox + 383, sy), c, 4))
    return "".join(o)


def viz_water(ox, oy):
    """Satellite over a spectral raster, feeding a CatBoost pipeline."""
    c = TEAL
    o = []
    # orbit arc + satellite
    o.append('<path d="M%d %dQ%d %d %d %d" fill="none" stroke="%s" stroke-opacity=".5" class="orbit"/>'
             % (ox, oy + 58, ox + 120, oy - 6, ox + 250, oy + 40, CYAN))
    sx, sy = ox + 104, oy + 30
    o.append('<g transform="translate(%d %d) rotate(-12)">'
             '<rect x="-9" y="-7" width="18" height="14" rx="2" fill="%s" stroke="%s"/>'
             '<rect x="-34" y="-5" width="22" height="10" fill="#0c2a3a" stroke="%s" stroke-opacity=".8"/>'
             '<rect x="12" y="-5" width="22" height="10" fill="#0c2a3a" stroke="%s" stroke-opacity=".8"/>'
             '<path d="M-34 0H-12M12 0H34M-23 -5V5M23 -5V5" stroke="%s" stroke-opacity=".5"/></g>'
             % (sx, sy, PANEL_2, CYAN, CYAN, CYAN, CYAN))
    o.append(node(sx, sy, 2.2, RED, True))
    # scan beam onto raster
    rx, ry, rw, rh = ox + 20, oy + 120, 180, 96
    o.append('<path d="M%d %dL%d %dH%dz" fill="url(#scanbeam)"/>' % (sx, sy + 8, rx, ry, rx + rw))
    shades = ["#0b3b4a", "#0e5566", "#127080", "#1a8d95", "#27a9a2", "#0a2f40"]
    cells, s = [], 5
    for j in range(6):
        for i in range(12):
            s = (s * 1103515245 + 12345) & 0x7FFFFFFF
            cells.append('<rect x="%d" y="%d" width="14" height="15" fill="%s"/>'
                         % (rx + i * 15, ry + j * 16, shades[s % len(shades)]))
    o.append('<g opacity=".85">%s</g>' % "".join(cells))
    o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s" stroke-opacity=".6"/>'
             % (rx - 1, ry - 1, rw + 1, rh + 1, c))
    o.append('<rect x="%d" y="%d" width="3" height="%d" fill="%s" opacity=".9" class="scan"/>' % (rx, ry, rh, CYAN))
    o.append(t(rx, ry + rh + 20, "SPECTRAL + ENVIRONMENTAL SIGNALS", 9.5, MUTED, MONO, None, None, .8))
    o.append('<path d="M%d %dq10-6 20 0t20 0 20 0 20 0 20 0 20 0 20 0 20 0 20 0" fill="none" stroke="%s" '
             'stroke-opacity=".6"/>' % (rx, ry + rh + 36, CYAN))
    # pipeline
    steps = [("FEATURE ENGINEERING", "spectral · environmental"), ("CATBOOST REGRESSOR", "gradient boosting"),
             ("WATER-QUALITY PARAMS", "predicted"), ("SPATIAL · TEMPORAL", "trend analysis")]
    px, pw = ox + 268, 196
    for i, (a, bsub) in enumerate(steps):
        y = oy + 10 + i * 62
        o.append(box(px, y, pw, 44, a, c if i != 1 else CYAN, bsub, 10))
        if i:
            o.append(flow("M%d %dV%d" % (px + pw / 2, y - 16, y - 2), c))
            o.append(arrow_head(px + pw / 2, y - 2, c, "down"))
    o.append(flow("M%d %dC%d %d %d %d %d %d" % (rx + rw, ry + 30, px - 30, ry + 30, px - 40, oy + 32, px - 2, oy + 32), c))
    o.append(arrow_head(px - 2, oy + 32, c))
    o.append(packet("M%d %dC%d %d %d %d %d %dH%dV%d" % (rx + rw, ry + 30, px - 30, ry + 30, px - 40, oy + 32, px - 2,
                                                       oy + 32, px + pw / 2, oy + 220), c, 5))
    return "".join(o)


def viz_feedback(ox, oy):
    """Feedback -> Transformer lattice -> sentiment/behaviour -> churn gauge -> agents -> actions."""
    c = VIOLET
    o = []
    # input streams
    for i, lab in enumerate(("FEEDBACK", "FEEDBACK", "FEEDBACK")):
        y = oy + 40 + i * 30
        o.append(flow("M%d %dH%d" % (ox, y, ox + 46), c, ".6"))
    o.append(t(ox, oy + 2, "MULTI-CHANNEL FEEDBACK", 9.5, MUTED, MONO, None, "600", 1))
    # transformer lattice (attention-style)
    lx, ly = ox + 58, oy + 26
    o.append(iso_box(lx - 8, ly - 8, 108, 92, 8, PANEL_2, "#080a0e", "#171b25"))
    pts = [(lx + 8 + i * 22, ly + 8 + j * 18) for j in range(5) for i in range(5)] if False else []
    cols = [[(lx + 8 + i * 22, ly + 6 + j * 17) for j in range(5)] for i in range(5)]
    edges = []
    for i in range(4):
        for a in cols[i]:
            for bpt in cols[i + 1]:
                edges.append("M%.1f %.1fL%.1f %.1f" % (a[0], a[1], bpt[0], bpt[1]))
    o.append('<path d="%s" stroke="%s" stroke-opacity=".13"/>' % ("".join(edges), c))
    for i, col in enumerate(cols):
        for j, (x, y) in enumerate(col):
            o.append('<circle cx="%.1f" cy="%.1f" r="2.6" fill="%s" class="blink d%d"/>' % (x, y, c, (i + j) % 4 + 1))
    o.append(t(lx + 46, ly + 104, "TRANSFORMER NLP", 9.5, TEXT, MONO, "middle", "600", 1))
    # sentiment / behaviour
    o.append(box(ox + 200, oy + 20, 112, 34, "SENTIMENT", c, None, 10))
    o.append(box(ox + 200, oy + 76, 112, 34, "BEHAVIOR", c, None, 10))
    for y in (37, 93):
        o.append(flow("M%d %dC%d %d %d %d %d %d" % (lx + 102, oy + 66, lx + 122, oy + 66, lx + 122, oy + y, ox + 198,
                                                    oy + y), c))
    # churn gauge
    gx, gy, gr = ox + 402, oy + 92, 50
    segs = [(180, 240, TEAL, "LOW"), (240, 300, GOLD, "MED"), (300, 360, RED, "HIGH")]
    for a0, a1, col, lab in segs:
        p0 = (gx + gr * math.cos(math.radians(a0)), gy + gr * math.sin(math.radians(a0)))
        p1 = (gx + gr * math.cos(math.radians(a1 - 3)), gy + gr * math.sin(math.radians(a1 - 3)))
        o.append('<path d="M%.1f %.1fA%d %d 0 0 1 %.1f %.1f" fill="none" stroke="%s" stroke-width="7"/>'
                 % (p0[0], p0[1], gr, gr, p1[0], p1[1], col))
        am = math.radians((a0 + a1) / 2)
        o.append(t(gx + (gr + 16) * math.cos(am), gy + (gr + 16) * math.sin(am) + 3, lab, 8.5, col, MONO,
                   "middle", "600"))
    o.append('<g><path d="M%d %dL%d %d" stroke="%s" stroke-width="2" stroke-linecap="round">'
             '<animateTransform attributeName="transform" type="rotate" values="-50 %d %d;40 %d %d;-50 %d %d" '
             'dur="6s" repeatCount="indefinite"/></path></g>' % (gx, gy, gx, gy - gr + 12, TEXT, gx, gy, gx, gy, gx, gy))
    o.append('<circle cx="%d" cy="%d" r="4" fill="%s"/>' % (gx, gy, TEXT))
    o.append(t(gx, gy + 20, "CHURN RISK", 9.5, TEXT, MONO, "middle", "600", 1.2))
    for y in (37, 93):
        o.append(flow("M%d %dC%d %d %d %d %d %d" % (ox + 320, oy + y, ox + 336, oy + y, ox + 336, oy + 70,
                                                    gx - gr - 6, oy + 70), c, ".5"))
    # multi-agent decision
    ax, ay = ox + 110, oy + 190
    agents = [(ax, ay), (ax + 70, ay - 26), (ax + 140, ay)]
    o.append(flow("M%d %dC%d %d %d %d %d %d" % (gx, gy + 28, gx, gy + 64, ax + 170, ay - 10, ax + 150, ay - 4), c))
    o.append('<path d="M%d %dL%d %dL%d %dZ" fill="%s" fill-opacity=".06" stroke="%s" stroke-opacity=".5"/>'
             % (agents[0] + agents[1] + agents[2] + (c, c)))
    for i, (x, y) in enumerate(agents):
        o.append('<circle cx="%d" cy="%d" r="12" fill="%s" stroke="%s" stroke-width="1.3"/>' % (x, y, PANEL, c))
        o.append(t(x, y + 3.5, "A%d" % (i + 1), 9, TEXT, MONO, "middle", "700"))
    o.append(t(ax + 70, ay + 30, "MULTI-AGENT DECISION", 9.5, TEXT, MONO, "middle", "600", 1.2))
    # actions
    acts = [("REFUND", GOLD), ("ESCALATE", RED), ("RETENTION OFFER", TEAL)]
    for i, (lab, col) in enumerate(acts):
        y = oy + 150 + i * 30
        o.append(flow("M%d %dC%d %d %d %d %d %d" % (ax + 152, ay, ax + 190, ay, ax + 190, y + 11, ox + 318, y + 11),
                      col, ".6"))
        o.append(chip(ox + 320, y, lab, col, 9.5, True)[0])
    o.append(t(ox + 452, oy + 250, "→ EMAIL · WHATSAPP FOLLOW-UPS", 9.5, MUTED, MONO, "end", None, .4))
    o.append(packet("M%d %dH%dC%d %d %d %d %d %d" % (ox, oy + 70, ox + 50, lx + 122, oy + 66, lx + 122, oy + 37,
                                                     ox + 198, oy + 37), c, 3.4))
    return "".join(o)


VIZ = {"project-01": viz_workforce, "project-02": viz_water, "project-03": viz_feedback}


def project_card(key):
    p = PROJECTS[key]

    def build(W):
        col = p["colour"]
        defs = ('<linearGradient id="scanbeam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s" '
                'stop-opacity=".35"/><stop offset="1" stop-color="%s" stop-opacity=".02"/></linearGradient>'
                '<radialGradient id="aura"><stop offset="0" stop-color="%s" stop-opacity=".14"/>'
                '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (CYAN, CYAN, col, col))
        b = []
        if W == WIDE:
            b.append('<circle cx="640" cy="210" r="260" fill="url(#aura)"/>')
            b.append(t(28, 44, "PROJECT %s" % p["idx"], 11, RED, MONO, None, "700", 2.4))
            b.append(t(140, 44, "// " + p["viz"], 10.5, DIM, MONO, None, None, 1.8))
            b.append('<rect x="28" y="58" width="%d" height="1" fill="url(#hair)"/>' % (W - 56))
            b.append(t(28, 94, p["title"][0], 23, TEXT, SANS, None, "700", .6))
            b.append(t(28, 122, p["title"][1], 23, TEXT, SANS, None, "700", .6))
            b.append(t(28, 148, p["kicker"], 10.5, col, MONO, None, "600", 1.6))
            b.append(t(28, 180, "PROBLEM", 9.5, DIM, MONO, None, "600", 2))
            pr = wrap(p["problem"], 50)
            b.append(lines(28, 198, pr, 12.5, MUTED, SANS, 18))
            y = 198 + len(pr) * 18 + 8
            b.append(t(28, y, "BUILT", 9.5, DIM, MONO, None, "600", 2))
            bl = wrap(p["built"], 50)
            b.append(lines(28, y + 18, bl, 12.5, TEXT, SANS, 18))
            s, bottom = chips(28, y + 18 + len(bl) * 18 - 2, p["stack"], 340, col, 10)
            b.append(s)
            H = max(390, int(bottom + 48))
            b.append('<rect x="392" y="74" width="1" height="%d" fill="%s"/>' % (H - 110, LINE))
            b.append(VIZ[key](420, 88))
            b.append(t(W - 28, H - 18, "CASE STUDY ON PORTFOLIO · SOURCE NOT PUBLIC", 9.5, FAINT, MONO, "end", None, 1.2))
            b.append(brackets(12, 12, W - 24, H - 24, col, 12, ".3"))
        else:
            b.append(t(20, 40, "PROJECT %s" % p["idx"], 11, RED, MONO, None, "700", 2.4))
            b.append(t(W - 20, 40, p["viz"].split()[0], 10, DIM, MONO, "end", None, 1.6))
            b.append('<rect x="20" y="54" width="%d" height="1" fill="url(#hair)"/>' % (W - 40))
            b.append(t(20, 86, p["title"][0], 21, TEXT, SANS, None, "700", .4))
            b.append(t(20, 112, p["title"][1], 21, TEXT, SANS, None, "700", .4))
            b.append(t(20, 136, p["kicker"], 10.5, col, MONO, None, "600", 1.2))
            b.append(t(20, 166, "PROBLEM", 9.5, DIM, MONO, None, "600", 2))
            pr = wrap(p["problem"], 54)
            b.append(lines(20, 184, pr, 12.5, MUTED, SANS, 18))
            y = 184 + len(pr) * 18 + 10
            b.append(t(20, y, "BUILT", 9.5, DIM, MONO, None, "600", 2))
            bl = wrap(p["built"], 54)
            b.append(lines(20, y + 18, bl, 12.5, TEXT, SANS, 18))
            y += 18 + len(bl) * 18 + 4
            s, y = chips(20, y, p["stack"], W - 40, col, 10)
            b.append(s)
            vy = y + 24
            b.append('<rect x="20" y="%d" width="%d" height="1" fill="%s"/>' % (vy - 8, W - 40, LINE))
            k = (W - 40) / 480.0
            b.append('<circle cx="220" cy="%d" r="220" fill="url(#aura)"/>' % (vy + 140))
            b.append('<g transform="translate(20 %d) scale(%.4f)">%s</g>' % (vy + 14, k, VIZ[key](0, 10)))
            H = int(vy + 14 + 280 * k + 44)
            b.append(t(W / 2, H - 18, "CASE STUDY ON PORTFOLIO · SOURCE NOT PUBLIC", 9.5, FAINT, MONO, "middle", None, .8))
            b.append(brackets(8, 8, W - 16, H - 16, col, 12, ".3"))
        return svg(W, H, "".join(b),
                   "Project %s: %s %s. Problem: %s Built: %s Stack: %s."
                   % (p["idx"], p["title"][0].title(), p["title"][1].title(), p["problem"], p["built"],
                      ", ".join(p["stack"])), defs)
    return build


# ============================================================ AI ARCHITECTURE
ARCH = [
    ("DATA", CYAN, ["satellite imagery", "feedback streams", "platform activity"]),
    ("PROCESSING", CYAN, ["Pandas · NumPy", "ingestion", "normalization"]),
    ("FEATURES", TEAL, ["spectral signals", "sentiment", "behavior"]),
    ("MODELS", VIOLET, ["CatBoost", "Transformers", "impact scoring"]),
    ("AGENTS", VIOLET, ["multi-agent", "decision", "framework"]),
    ("DECISION", RED, ["refund", "escalate", "retain"]),
    ("APPLICATION", BLUE, ["React · FastAPI", "PostgreSQL", "email · WhatsApp"]),
]


def architecture(W):
    b = []
    if W == WIDE:
        H = 380
        b.append(header(W, "06", "AI SYSTEM ARCHITECTURE", "COMPOSED FROM THE THREE PROJECTS"))
        bw, bh, step = 104, 58, 120
        bands = [(0, 3, CYAN, "SENSE"), (3, 5, VIOLET, "REASON"), (5, 7, RED, "ACT")]
        for a, z, col, lab in bands:
            x0, x1 = 36 + a * step, 36 + (z - 1) * step + bw + 10
            b.append('<path d="M%d 92V86H%dV92" fill="none" stroke="%s" stroke-opacity=".6"/>' % (x0, x1, col))
            b.append(t((x0 + x1) / 2, 80, lab, 10, col, MONO, "middle", "700", 3))
        pts = []
        for i, (name, col, tech) in enumerate(ARCH):
            x = 36 + i * step
            y = 178 - i * 10
            b.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" opacity=".08" filter="url(#glow)"/>'
                     % (x, y, bw, bh, col))
            b.append(iso_box(x, y, bw, bh, 10, PANEL_2, "#080a0e", "#171b25"))
            b.append('<rect x="%d" y="%d" width="%d" height="2" fill="%s"/>' % (x, y, bw, col))
            b.append(t(x + 10, y + 20, "L%d" % (i + 1), 9.5, col, MONO, None, "700", 1))
            b.append(t(x + bw / 2, y + 42, name, 10.5 if len(name) < 11 else 9.8, TEXT, MONO, "middle", "700", 1))
            for j, row in enumerate(tech):
                b.append(t(x + 2, 272 + j * 17, row, 10.5, MUTED if j else TEXT, MONO, None, None))
            b.append('<path d="M%d %dV%d" stroke="%s" stroke-opacity=".35" stroke-dasharray="2 3"/>'
                     % (x + 2, y + bh + 4, 258, col))
            pts.append((x, y))
        d = "M%d %d" % (pts[0][0] + bw, pts[0][1] + bh / 2)
        for i in range(1, len(pts)):
            d += "L%d %d" % (pts[i][0], pts[i][1] + bh / 2)
            if i < len(pts) - 1:
                d += "M%d %d" % (pts[i][0] + bw, pts[i][1] + bh / 2)
        b.append(flow(d, CYAN, ".8", 1.4))
        whole = "M%d %d" % (pts[0][0] + bw, pts[0][1] + bh / 2) + "".join(
            "L%d %d" % (p[0] + (bw if i else 0), p[1] + bh / 2) for i, p in enumerate(pts[1:], 1))
        b.append(packet("M%d %d" % (pts[0][0], pts[0][1] + bh / 2) + "".join(
            "L%d %dL%d %d" % (p[0], p[1] + bh / 2, p[0] + bw, p[1] + bh / 2) for p in pts), RED, 6, 3))
        b.append('<rect x="28" y="%d" width="%d" height="1" fill="url(#hair)"/>' % (H - 44, W - 56))
        b.append(t(28, H - 20, "EVERY LAYER NAMES COMPONENTS THE PROJECTS ACTUALLY USE", 10, DIM, MONO, None, None, 1.4))
    else:
        b.append(header(W, "06", "AI SYSTEM ARCHITECTURE", "", x=20))
        y0, rh = 80, 70
        for i, (name, col, tech) in enumerate(ARCH):
            y = y0 + i * rh
            b.append(iso_box(30, y, 132, 48, 8, PANEL_2, "#080a0e", "#171b25"))
            b.append('<rect x="30" y="%d" width="132" height="2" fill="%s"/>' % (y, col))
            b.append(t(40, y + 29, "L%d" % (i + 1), 9.5, col, MONO, None, "700"))
            b.append(t(64, y + 29, name, 10.5, TEXT, MONO, None, "700", .8))
            b.append(t(186, y + 21, tech[0], 11, TEXT, MONO))
            b.append(t(186, y + 38, " · ".join(tech[1:]), 10.5, MUTED, MONO))
            if i:
                b.append(flow("M96 %dV%d" % (y - rh + 56, y - 10), col, ".8"))
                b.append(arrow_head(96, y - 10, col, "down"))
        H = y0 + len(ARCH) * rh + 20
    return svg(W, H, "".join(b),
               "AI system architecture in seven layers: data (satellite imagery, feedback streams, platform "
               "activity), processing (Pandas, NumPy, ingestion, normalization), features (spectral signals, "
               "sentiment, behavior), models (CatBoost, Transformers, impact scoring), agents (multi-agent decision "
               "framework), decision (refund, escalate, retain) and application (React, FastAPI, PostgreSQL, email "
               "and WhatsApp).")


# ============================================================ STACK NETWORK
# True = present in a public repository (checked by hand):
#   ashwin-portfolio   Next.js, TypeScript, React, Three.js (R3F), GSAP, Tailwind
#   dsa-placement-tracker  React, TypeScript, Vite, Tailwind
#   dji-dronic-world   React, Vite, Tailwind, Express, Node.js, SQLite, JWT, bcrypt, Docker, REST
#   LeetCode-Solution  Java          profile repo  Python, GitHub Actions
# False = from the resume's skills and project stacks.
STACK = [
    ("INTERFACE", CYAN, [("React", True), ("Next.js", True), ("TypeScript", True), ("JavaScript", True),
                         ("Tailwind CSS", True), ("Vite", True), ("Three.js", True), ("GSAP", True),
                         ("HTML / CSS", True)]),
    ("INTELLIGENCE", VIOLET, [("Machine Learning", False), ("NLP · Transformers", False), ("CatBoost", False),
                              ("Agentic AI", False), ("Predictive Analytics", False),
                              ("Geospatial Analytics", False)]),
    ("BACKEND", BLUE, [("FastAPI", False), ("SQLAlchemy", False), ("Express", True), ("Node.js", True),
                       ("REST APIs", True), ("JWT · bcrypt", True), ("WhatsApp API", False)]),
    ("DATA", TEAL, [("Pandas", False), ("NumPy", False), ("Matplotlib", False), ("SQL", False), ("MySQL", False),
                    ("PostgreSQL", False), ("SQLite", True)]),
    ("LANGUAGES", GOLD, [("Python", True), ("Java", True), ("C", False), ("C++", False)]),
    ("PLATFORMS", RED, [("Git", True), ("GitHub Actions", True), ("Docker", True), ("Vercel", True),
                        ("VS Code", False), ("ServiceNow AI", False), ("Celonis", False)]),
]


def stack(W):
    b = []
    wide = W == WIDE
    x0 = 28 if wide else 20
    b.append(header(W, "03", "TECHNOLOGY NETWORK · ENGINEERING STACK", "" if not wide else "", x=x0))
    ly = 84
    lg1, w1 = chip(x0, ly - 15, "Name", MUTED, 9.5, True)
    b.append(lg1 + t(x0 + w1 + 8, ly, "filled = found in a public repository", 10, MUTED, MONO))
    lx = x0 + (330 if wide else 0)
    lyy = ly if wide else ly + 30
    lg2, w2 = chip(lx, lyy - 15, "Name", MUTED, 9.5, False)
    b.append(lg2 + t(lx + w2 + 8, lyy, "outline = resume / project stack", 10, MUTED, MONO))
    if not wide:
        ly += 30
    y = ly + 28
    for i, (name, col, items) in enumerate(STACK):
        if wide:
            sx, sw = 200, W - 228 - 10
            it = [(n, col, v) for n, v in items]
            rows_svg, bottom = chips(sx + 18, y + 16, it, sw - 36, col, 10.5)
            h = bottom - y + 12
            b.append(iso_box(sx, y, sw, h, 10, PANEL_2, "#080a0e", "#161a23"))
            b.append('<rect x="%d" y="%d" width="3" height="%d" fill="%s"/>' % (sx, y, h, col))
            b.append(rows_svg)
            b.append(t(x0 + 30, y + h / 2 - 3, "L%d" % (i + 1), 9.5, col, MONO, None, "700", 1))
            b.append(t(x0 + 30, y + h / 2 + 14, name, 11, TEXT, MONO, None, "700", 1.8))
            b.append(node(x0 + 12, y + h / 2, 3.2, col, i == 1, "d%d" % (i % 4 + 1)))
            b.append(flow("M%d %dH%d" % (x0 + 150, y + h / 2, sx - 2), col, ".5", 1, "flow-slow"))
            y += h + 22
        else:
            b.append(node(x0 + 6, y + 10, 3, col, False))
            b.append(t(x0 + 18, y + 14, "L%d · %s" % (i + 1, name), 11, TEXT, MONO, None, "700", 1.6))
            y += 26
            sx, sw = x0 + 10, W - 2 * x0 - 20
            it = [(n, col, v) for n, v in items]
            rows_svg, bottom = chips(sx + 14, y + 14, it, sw - 28, col, 10.5)
            h = bottom - y + 10
            b.append(iso_box(sx, y, sw, h, 8, PANEL_2, "#080a0e", "#161a23"))
            b.append('<rect x="%d" y="%d" width="3" height="%d" fill="%s"/>' % (sx, y, h, col))
            b.append(rows_svg)
            y += h + 22
    if wide:
        b.append('<path d="M%d %dV%d" stroke="%s" stroke-opacity=".5" stroke-dasharray="2 4"/>' % (x0 + 12, ly + 40, y - 40, LINE_2))
    H = int(y + 20)
    names = "; ".join("%s: %s" % (n, ", ".join(i for i, _ in it)) for n, _, it in STACK)
    return svg(W, H, "".join(b), "Technology network in six layers. Filled chips appear in public repositories, "
               "outlined chips come from the resume. " + names + ".")


# ================================================================== JOURNEY
def journey(W):
    b = []
    if W == WIDE:
        H = 390
        b.append(header(W, "07", "DEVELOPMENT JOURNEY", "TWO TRACKS · ONLY REAL DATES"))
        ay = 200
        month = lambda m: 380 + (m - 1) * 55.0          # noqa: E731  Jan..Sep 2026
        b.append('<path d="M40 %dH848" stroke="%s" stroke-width="2"/>' % (ay, LINE_2))
        b.append('<path d="M380 %dH%d" stroke="%s" stroke-width="6" stroke-opacity=".12"/>' % (ay, month(9), CYAN))
        for m in range(1, 10):
            b.append('<path d="M%.1f %dv6" stroke="%s"/>' % (month(m), ay - 3, LINE_2))
        years = [(70, "2022"), (180, "2024"), (280, "2025"), (380, "2026")]
        for x, yr in years:
            b.append('<rect x="%d" y="%d" width="44" height="18" rx="9" fill="%s" stroke="%s"/>'
                     % (x - 22, ay - 9, BG, LINE_2))
            b.append(t(x, ay + 4, yr, 10, TEXT, MONO, "middle", "700", 1))
        b.append(t(40, 78, "BUILD TRACK", 10, CYAN, MONO, None, "700", 2.4))
        b.append(t(40, 94, "dated by the GitHub API", 10, DIM, MONO))
        build = [(3, 132, "MAR 2026", "GITHUB ONLINE", "account opened"),
                 (5, 84, "MAY 2026", "FIRST FULL-STACK SHIP", "dji-dronic-world"),
                 (8, 132, "AUG 2026", "DSA SYSTEM", "LeetCode-Solution"),
                 (9, 84, "SEP 2026", "PORTFOLIO + TRACKER LIVE", "ashwin-portfolio · dsa tracker")]
        for m, ly, date, title, sub in build:
            x = month(m)
            anchor = "end" if m in (5, 9) else "middle"
            tx = x + 8 if m in (5, 9) else x
            b.append('<path d="M%.1f %dV%d" stroke="%s" stroke-opacity=".5"/>' % (x, ay - 6, ly + 22, CYAN))
            b.append(node(x, ay, 4, CYAN, True, "d%d" % (m % 4 + 1)))
            b.append(t(tx, ly - 20, date, 9.5, CYAN, MONO, anchor, "700", 1.4))
            b.append(t(tx, ly - 4, title, 11, TEXT, MONO, anchor, "700", 1))
            b.append(t(tx, ly + 12, sub, 10, MUTED, MONO, anchor))
        b.append(t(40, H - 40, "RECORD TRACK", 10, GOLD, MONO, None, "700", 2.4))
        b.append(t(40, H - 24, "dated by year on the resume", 10, DIM, MONO))
        rec = [(70, 250, "FOUNDATION", "HSC · computer science", "start"),
               (180, 296, "B.E. CSE BEGINS", "SREC · Anna University", "middle"),
               (280, 250, "FIRST PODIUM", "Cryptera 2025 runner-up", "middle")]
        for x, ly, title, sub, anchor in rec:
            tx = 40 if anchor == "start" else x
            b.append('<path d="M%d %dV%d" stroke="%s" stroke-opacity=".5"/>' % (x, ay + 9, ly - 16, GOLD))
            b.append(t(tx, ly, title, 11, TEXT, MONO, anchor, "700", 1))
            b.append(t(tx, ly + 16, sub, 10, MUTED, MONO, anchor))
        bx0, bx1, by = 380, month(9), 234
        b.append('<path d="M%d %dv8H%.1fv-8" fill="none" stroke="%s" stroke-opacity=".7"/>' % (bx0, by, bx1, GOLD))
        b.append('<path d="M%.1f %dV%d" stroke="%s" stroke-opacity=".5"/>' % ((bx0 + bx1) / 2, ay + 9, by, GOLD))
        b.append(t(bx0, by + 30, "2026 · RECOGNITION", 11, GOLD, MONO, None, "700", 1.6))
        b.append(t(bx1, by + 30, "month not listed", 9.5, DIM, MONO, "end"))
        recs = ["HackTIDE — 1st prize", "IDEATHON — 1st prize", "VeloHack2k26 — 3rd prize",
                "IEEE ICCPCT 2026 — paper", "ServiceNow AI × 2", "Celonis Academy × 2"]
        for i, r in enumerate(recs):
            b.append(t(bx0 + (i // 3) * 232, by + 54 + (i % 3) * 18, "▸ " + r, 10.5, MUTED, MONO))
        b.append(node(872, ay, 5, RED, True))
        b.append(t(872, ay - 16, "NOW", 10, RED, MONO, "middle", "700", 2))
        b.append(t(872, ay + 26, "agentic", 9.5, DIM, MONO, "middle"))
        b.append(t(872, ay + 40, "AI", 9.5, DIM, MONO, "middle"))
    else:
        b.append(header(W, "07", "DEVELOPMENT JOURNEY", "", x=20))
        items = [("2022", "FOUNDATION", "HSC · computer science", GOLD),
                 ("2024", "B.E. CSE BEGINS", "SREC · Anna University", GOLD),
                 ("2025", "FIRST PODIUM", "Cryptera 2025 runner-up", GOLD),
                 ("MAR 2026", "GITHUB ONLINE", "account opened", CYAN),
                 ("MAY 2026", "FIRST FULL-STACK SHIP", "dji-dronic-world", CYAN),
                 ("AUG 2026", "DSA SYSTEM", "LeetCode-Solution", CYAN),
                 ("SEP 2026", "PORTFOLIO + TRACKER LIVE", "ashwin-portfolio · dsa tracker", CYAN),
                 ("2026", "RECOGNITION", "HackTIDE 1st · IDEATHON 1st|VeloHack2k26 3rd · IEEE paper|"
                                         "ServiceNow AI × 2 · Celonis × 2", GOLD),
                 ("NOW", "CURRENT FOCUS", "agentic AI · ML systems", RED)]
        y = 86
        b.append('<path d="M40 %dV%d" stroke="%s" stroke-opacity=".45" stroke-width="2"/>' % (y, y + 8 * 66 + 60, CYAN))
        for date, title, sub, col in items:
            subs = sub.split("|")
            b.append(node(40, y + 6, 4, col, date == "NOW"))
            b.append(t(60, y + 2, date, 9.5, col, MONO, None, "700", 1.4))
            b.append(t(60, y + 20, title, 12, TEXT, MONO, None, "700", 1))
            for j, s in enumerate(subs):
                b.append(t(60, y + 37 + j * 16, s, 10.5, MUTED, MONO))
            y += 50 + len(subs) * 16
        H = y + 10
        b.append(t(20, H - 16, "cyan = GitHub-dated · gold = year on resume", 9.5, DIM, MONO))
        H += 10
    return svg(W, H, "".join(b),
               "Development journey. Record track: 2022 HSC in computer science; 2024 B.E. CSE begins at SREC; "
               "2025 Cryptera runner-up; 2026 HackTIDE and IDEATHON first prizes, VeloHack2k26 third prize, IEEE "
               "ICCPCT 2026 paper and four certifications. Build track dated by GitHub: March 2026 account opened, "
               "May 2026 dji-dronic-world, August 2026 LeetCode-Solution, September 2026 portfolio and DSA tracker.")


# ============================================================= ACHIEVEMENTS
AWARDS = [
    ("REC-01", "FIRST PRIZE", "1", "gold", GOLD, "HackTIDE", "AMRITA VISHWA VIDYAPEETHAM",
     "24-HOUR HACKATHON · 2026", "₹25,000 CASH PRIZE"),
    ("REC-02", "FIRST PRIZE", "1", "gold", GOLD, "IDEATHON", "KGiSL INSTITUTE OF TECHNOLOGY",
     "HACKATHON · 2026", None),
    ("REC-03", "3RD PRIZE", "3", "bronze", BRONZE, "VeloHack2k26", "VEL TECH UNIVERSITY",
     "TEAM: LET ME TRY", "₹16,000 CASH PRIZE"),
    ("REC-04", "RUNNER-UP", "2", "silver", SILVER, "Cryptera 2025", "“LiFi: The Saviour”", "2025", None),
]


def emblem(cx, cy, numeral, grad, col):
    def hexa(r):
        return "M" + "L".join("%.1f %.1f" % (cx + r * math.cos(math.radians(60 * i - 90)),
                                              cy + r * math.sin(math.radians(60 * i - 90))) for i in range(6)) + "Z"
    o = '<circle cx="%d" cy="%d" r="46" fill="%s" opacity=".10" filter="url(#glow)"/>' % (cx, cy, col)
    o += '<path d="%s" fill="none" stroke="url(#%s)" stroke-width="2"/>' % (hexa(44), grad)
    o += '<path d="%s" fill="%s" stroke="url(#%s)" stroke-opacity=".6"/>' % (hexa(34), PANEL, grad)
    o += '<path d="%s" fill="none" stroke="%s" stroke-opacity=".35" class="orbit"/>' % (hexa(52), col)
    # laurel ticks
    for side in (-1, 1):
        for i in range(5):
            a = math.radians(110 + i * 18) if side < 0 else math.radians(70 - i * 18)
            x1, y1 = cx + 38 * math.cos(a), cy + 38 * math.sin(a)
            o += ('<ellipse cx="%.1f" cy="%.1f" rx="4.5" ry="2" fill="%s" opacity=".55" transform="rotate(%.1f %.1f %.1f)"/>'
                  % (x1, y1, col, math.degrees(a) + 90 * side, x1, y1))
    o += t(cx, cy + 13, numeral, 36, "url(#%s)" % grad, SANS, "middle", "800")
    return o


def award_card(x, y, w, h, a):
    rid, placing, num, grad, col, name, org, detail, prize = a
    o = panel(x, y, w, h, None)
    o += '<rect x="%d" y="%d" width="%d" height="2" fill="url(#%s)"/>' % (x + 1, y, w - 2, grad)
    o += emblem(x + 66, y + h / 2, num, grad, col)
    tx = x + 132
    o += t(tx, y + 32, placing, 11, col, MONO, None, "700", 2.6)
    o += t(x + w - 16, y + 32, rid, 9.5, DIM, MONO, "end", None, 1.4)
    o += t(tx, y + 64, name, 24, TEXT, SANS, None, "700", .2)
    italic = org.startswith("“")
    o += t(tx, y + 88, org, 13 if italic else 10.5, MUTED, SANS if italic else MONO, None, None, None if italic else 1.2,
           extra=' font-style="italic"' if italic else "")
    o += t(tx, y + 108, detail, 10.5, DIM, MONO, None, None, 1.2)
    if prize:
        o += chip(tx, y + 120, prize, col, 10.5, True)[0]
    # circuit trace in the corner
    o += ('<path d="M%d %dh-40l-12 12h-30" fill="none" stroke="%s" stroke-opacity=".3"/>'
          '<circle cx="%d" cy="%d" r="2" fill="%s" opacity=".5"/>'
          % (x + w - 12, y + h - 18, col, x + w - 94, y + h - 6, col))
    return o


def achievements(W):
    b = []
    if W == WIDE:
        b.append(header(W, "10", "ACHIEVEMENTS · HALL OF RECORDS", "4 ENTRIES · AS LISTED ON RESUME"))
        cw, ch = 414, 158
        for i, a in enumerate(AWARDS):
            b.append(award_card(28 + (i % 2) * (cw + 16), 76 + (i // 2) * (ch + 18), cw, ch, a))
        H = 76 + 2 * (ch + 18) + 14
    else:
        b.append(header(W, "10", "HALL OF RECORDS", "", x=20))
        ch = 158
        for i, a in enumerate(AWARDS):
            b.append(award_card(20, 72 + i * (ch + 14), W - 40, ch, a))
        H = 72 + 4 * (ch + 14) + 10
    return svg(W, H, "".join(b),
               "Achievements. First prize at HackTIDE, a 24-hour hackathon at Amrita Vishwa Vidyapeetham, 2026, "
               "25,000 rupee cash prize. First prize at IDEATHON, KGiSL Institute of Technology, 2026. Third prize "
               "at VeloHack2k26, Vel Tech University, team Let Me Try, 16,000 rupee cash prize. Runner-up at "
               "Cryptera 2025 for LiFi: The Saviour.")


# ================================================================= RESEARCH
PUB_TITLE = ("A High-Resolution Data Fusion Framework for Water Body Assessment Using Sentinel-2 and "
             "Gradient Boosting")
PUB_STEPS = [("SENTINEL-2", CYAN), ("DATA FUSION", BLUE), ("GEOSPATIAL FEATURES", TEAL),
             ("GRADIENT BOOSTING", VIOLET), ("WATER BODY ASSESSMENT", GOLD)]


def paper(x, y, w, h, wrap_at):
    o = ""
    for i in (2, 1):
        o += ('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s" stroke="%s" opacity=".7"/>'
              % (x + i * 6, y + i * 6, w, h, PANEL, LINE_2))
    o += panel(x, y, w, h, GOLD)
    o += '<path d="M%d %dh22v22" fill="none" stroke="%s" stroke-opacity=".6"/>' % (x + w - 34, y + 12, GOLD)
    o += t(x + 20, y + 34, "PUBLISHED · 2026", 10, GOLD, MONO, None, "700", 2)
    rows = wrap(PUB_TITLE, wrap_at)
    o += lines(x + 20, y + 66, rows, 16.5, TEXT, SANS, 23, weight="600")
    yy = y + 66 + len(rows) * 23 + 8
    o += t(x + 20, yy, "ICCPCT 2026 · IEEE CONFERENCE", 10.5, MUTED, MONO, None, None, 1.4)
    return o


def pub_pipeline(x, y, step, label_x_off=22):
    o = '<path d="M%d %dV%d" stroke="%s" stroke-width="1.6"/>' % (x, y, y + step * (len(PUB_STEPS) - 1), LINE_2)
    o += '<path d="M%d %dV%d" stroke="%s" class="flow" stroke-width="1.6"/>' % (x, y, y + step * (len(PUB_STEPS) - 1), CYAN)
    for i, (s, col) in enumerate(PUB_STEPS):
        yy = y + i * step
        o += ('<rect x="%d" y="%d" width="14" height="14" rx="3" fill="%s" stroke="%s" '
              'transform="rotate(45 %d %d)"/>' % (x - 7, yy - 7, PANEL, col, x, yy))
        o += '<circle cx="%d" cy="%d" r="2.5" fill="%s" class="blink d%d"/>' % (x, yy, col, i % 4 + 1)
        o += t(x + label_x_off, yy + 4, "%02d  %s" % (i + 1, s), 11.5, TEXT, MONO, None, "600", 1.2)
    return o


def research(W):
    b = []
    if W == WIDE:
        H = 360
        b.append(header(W, "11", "RESEARCH · PUBLICATION", "IEEE CONFERENCE · ICCPCT 2026"))
        b.append(paper(28, 78, 420, 190, 40))
        b.append(pub_pipeline(500, 96, 44))
        # earth limb + satellite, decorative
        b.append('<path d="M700 300A260 260 0 0 1 872 190" fill="none" stroke="%s" stroke-opacity=".35"/>' % CYAN)
        b.append('<path d="M740 300A220 220 0 0 1 872 222" fill="none" stroke="%s" stroke-opacity=".18"/>' % TEAL)
        b.append('<g transform="translate(820 110) rotate(-20)"><rect x="-8" y="-6" width="16" height="12" rx="2" '
                 'fill="%s" stroke="%s"/><rect x="-30" y="-4" width="19" height="8" fill="#0c2a3a" stroke="%s"/>'
                 '<rect x="11" y="-4" width="19" height="8" fill="#0c2a3a" stroke="%s"/></g>' % (PANEL_2, CYAN, CYAN, CYAN))
        b.append('<path d="M820 118L780 250M820 118L860 250" stroke="%s" stroke-opacity=".25" stroke-dasharray="2 4"/>' % CYAN)
        b.append('<rect x="28" y="%d" width="%d" height="1" fill="url(#hair)"/>' % (H - 44, W - 56))
        b.append(t(28, H - 20, "◆ LINKED NODE → PROJECT 02 · SATELLITE WATER QUALITY", 10.5, GOLD, MONO, None, "600", 1.2))
        b.append(t(W - 28, H - 20, "SHARED DOMAIN: SATELLITE IMAGERY + GRADIENT BOOSTING", 10, DIM, MONO, "end", None, 1))
    else:
        b.append(header(W, "11", "RESEARCH · PUBLICATION", "", x=20))
        b.append(paper(20, 74, W - 52, 232, 38))
        b.append(pub_pipeline(44, 360, 40))
        H = 360 + 4 * 40 + 80
        b.append(t(20, H - 40, "◆ LINKED → PROJECT 02 · WATER QUALITY", 10.5, GOLD, MONO, None, "600", 1))
        b.append(t(20, H - 22, "shared domain: satellite imagery + gradient boosting", 10, DIM, MONO))
    return svg(W, H, "".join(b),
               "Publication: " + PUB_TITLE + ". Published at ICCPCT 2026, an IEEE conference, 2026. Method outline: "
               "Sentinel-2, data fusion, geospatial features, gradient boosting, water body assessment. Shares its "
               "domain with project 02, satellite-based water quality monitoring.")


# =========================================================== CERTIFICATIONS
CERTS = [("01", "ServiceNow AI Essentials", "SERVICENOW", VIOLET),
         ("02", "AI Agents & Agentic AI", "SERVICENOW", VIOLET),
         ("03", "Celonis Foundations", "CELONIS ACADEMY", TEAL),
         ("04", "Get Data into Celonis", "CELONIS ACADEMY", TEAL)]


def cert_module(x, y, w, h, c):
    idx, title, issuer, col = c
    o = panel(x, y, w, h, col)
    o += '<path d="M%d %dh10l6 6v10" fill="none" stroke="%s" stroke-opacity=".7"/>' % (x + w - 30, y + 10, col)
    o += t(x + 16, y + 28, idx, 10, RED, MONO, None, "700", 1.4)
    o += t(x + 40, y + 28, issuer, 9.5, col, MONO, None, "700", 1.4)
    o += lines(x + 16, y + 54, wrap(title, 22 if w > 200 else 20), 14, TEXT, SANS, 19, weight="600")
    o += t(x + 16, y + h - 14, "2026", 10, DIM, MONO, None, None, 1.4)
    o += ('<path d="M%d %dl3 3 6-7" fill="none" stroke="%s" stroke-width="1.6"/>' % (x + w - 26, y + h - 18, col))
    return o


def certifications(W):
    b = []
    if W == WIDE:
        b.append(header(W, "12", "CERTIFICATIONS", "FOUR MODULES · AS LISTED ON RESUME"))
        mw, mh = 203, 118
        for i, c in enumerate(CERTS):
            b.append(cert_module(28 + i * (mw + 12), 76, mw, mh, c))
        H = 76 + mh + 26
    else:
        b.append(header(W, "12", "CERTIFICATIONS", "", x=20))
        mw, mh = (W - 52) / 2, 118
        for i, c in enumerate(CERTS):
            b.append(cert_module(20 + (i % 2) * (mw + 12), 72 + (i // 2) * (mh + 12), mw, mh, c))
        H = 72 + 2 * (mh + 12) + 14
    return svg(W, H, "".join(b),
               "Certifications, 2026: ServiceNow AI Essentials (ServiceNow); AI Agents and Agentic AI (ServiceNow); "
               "Celonis Foundations (Celonis Academy); Get Data into Celonis (Celonis Academy).")


# ================================================================== MISSION
STATUS = {"ACTIVE": ("●", TEAL), "BUILDING": ("◐", CYAN), "RESEARCHING": ("◇", VIOLET), "EXPLORING": ("○", GOLD)}
MISSION = [("AGENTIC AI", "BUILDING", "multi-agent decisions · ServiceNow AI Agents"),
           ("MACHINE LEARNING", "ACTIVE", "CatBoost pipelines · predictive analytics"),
           ("NLP", "ACTIVE", "Transformer sentiment · behavioral modeling"),
           ("GEOSPATIAL AI", "RESEARCHING", "Sentinel-2 · IEEE ICCPCT 2026"),
           ("SOFTWARE SYSTEMS", "ACTIVE", "React · FastAPI · Next.js · Express"),
           ("DSA", "ACTIVE", "LeetCode in Java · 12-week tracker"),
           ("CYBERSECURITY", "EXPLORING", "API hardening: Helmet · JWT · rate limits"),
           ("PROCESS INTELLIGENCE", "EXPLORING", "Celonis · ServiceNow platforms")]


def mission_module(x, y, w, h, i, m):
    area, status, ev = m
    glyph, col = STATUS[status]
    o = panel(x, y, w, h, None)
    o += t(x + 14, y + 24, "[%02d]" % (i + 1), 10, DIM, MONO, None, None, 1)
    o += chip(x + w - 12, y + 10, glyph + " " + status, col, 9, True, 20, anchor="end")[0]
    o += t(x + 14, y + 52, area, 12 if len(area) < 18 else 11, TEXT, MONO, None, "700", 1.2)
    o += lines(x + 14, y + 72, wrap(ev, 28), 10.5, MUTED, MONO, 15)
    return o


def mission(W):
    b = []
    if W == WIDE:
        b.append(header(W, "13", "CURRENT MISSION · 2026", "STATUS, NOT SCORES"))
        mw, mh = 203, 106
        for i, m in enumerate(MISSION):
            b.append(mission_module(28 + (i % 4) * (mw + 12), 74 + (i // 4) * (mh + 12), mw, mh, i, m))
        H = 74 + 2 * (mh + 12) + 44
        lx = 28
    else:
        b.append(header(W, "13", "CURRENT MISSION · 2026", "", x=20))
        mw, mh = (W - 52) / 2, 110
        for i, m in enumerate(MISSION):
            b.append(mission_module(20 + (i % 2) * (mw + 12), 70 + (i // 2) * (mh + 12), mw, mh, i, m))
        H = 70 + 4 * (mh + 12) + 44
        lx = 20
    x = lx
    for s, (g, col) in STATUS.items():
        b.append(t(x, H - 20, g + " " + s, 10, col, MONO, None, "600", 1.2))
        x += text_w(g + " " + s, 10, True, 1.2) + (22 if W == WIDE else 10)
    return svg(W, H, "".join(b),
               "Current mission, 2026. " + "; ".join("%s: %s (%s)" % m for m in MISSION) + ".")


# =================================================================== FOOTER
def footer(W):
    b = []
    wide = W == WIDE
    defs = ('<linearGradient id="hl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="%s"/>'
            '<stop offset="1" stop-color="%s"/></linearGradient>'
            '<radialGradient id="aura"><stop offset="0" stop-color="%s" stop-opacity=".16"/>'
            '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (CYAN, VIOLET, RED, RED))
    if wide:
        H = 360
        b.append(stars(W, H, 60, 3))
        b.append('<ellipse cx="450" cy="250" rx="360" ry="160" fill="url(#aura)"/>')
        b.append(t(28, 40, "14", 11, RED, MONO, None, "700", 2))
        b.append(t(54, 40, "// CONNECT", 11.5, TEXT, MONO, None, "600", 3))
        b.append(t(450, 102, "LET'S BUILD SOMETHING", 34, TEXT, SANS, "middle", "800", 1))
        b.append(t(450, 144, "INTELLIGENT.", 34, "url(#hl)", SANS, "middle", "800", 3))
        b.append(t(450, 176, "Open to internships and collaboration in AI/ML, software and data.", 14, MUTED, SANS,
                   "middle"))
        cols = [(170, "PORTFOLIO", "who I am", CYAN), (450, "GITHUB", "what I build", RED),
                (730, "LINKEDIN", "career record", VIOLET)]
        for x, name, sub, col in cols:
            b.append(flow("M%d 238Q%d 270 450 286" % (x, x), col, ".6"))
            b.append(node(x, 232, 4, col, True))
            b.append(t(x, 216, name, 11, TEXT, MONO, "middle", "700", 2.4))
            b.append(t(x, 202, sub, 10, DIM, MONO, "middle", None, 1))
        wm = 0.3
        b.append(wordmark(450 - wordmark_width(scale=wm) / 2, 292, wm, extrude=2, mid="wf"))
        b.append(t(450, 344, "// ENGINEERING THE NEXT SYSTEM", 10.5, DIM, MONO, "middle", None, 3))
        b.append(brackets(12, 12, W - 24, H - 24, RED, 14, ".35"))
    else:
        H = 440
        b.append(stars(W, H, 50, 3))
        b.append('<ellipse cx="220" cy="300" rx="220" ry="160" fill="url(#aura)"/>')
        b.append(t(20, 38, "14", 11, RED, MONO, None, "700", 2))
        b.append(t(46, 38, "// CONNECT", 11.5, TEXT, MONO, None, "600", 3))
        b.append(t(220, 96, "LET'S BUILD", 30, TEXT, SANS, "middle", "800", 1))
        b.append(t(220, 130, "SOMETHING", 30, TEXT, SANS, "middle", "800", 1))
        b.append(t(220, 166, "INTELLIGENT.", 30, "url(#hl)", SANS, "middle", "800", 2))
        b.append(t(220, 198, "Open to internships and collaboration", 13, MUTED, SANS, "middle"))
        b.append(t(220, 216, "in AI/ML, software and data.", 13, MUTED, SANS, "middle"))
        cols = [(80, "PORTFOLIO", "who I am", CYAN), (220, "GITHUB", "what I build", RED),
                (360, "LINKEDIN", "career record", VIOLET)]
        for x, name, sub, col in cols:
            b.append(flow("M%d 282Q%d 320 220 336" % (x, x), col, ".6"))
            b.append(node(x, 276, 4, col, True))
            b.append(t(x, 260, name, 10.5, TEXT, MONO, "middle", "700", 1.6))
            b.append(t(x, 246, sub, 9.5, DIM, MONO, "middle"))
        wm = 0.3
        b.append(wordmark(220 - wordmark_width(scale=wm) / 2, 346, wm, extrude=2, mid="wf"))
        b.append(t(220, 400, "// ENGINEERING THE NEXT SYSTEM", 10, DIM, MONO, "middle", None, 2))
        b.append(brackets(10, 10, W - 20, H - 20, RED, 14, ".35"))
    return svg(W, H, "".join(b),
               "Let's build something intelligent. Open to internships and collaboration in AI/ML, software and "
               "data. Portfolio: who I am. GitHub: what I build. LinkedIn: career record. Ashwin S, engineering the "
               "next system.", defs)


# ===================================================================== MAIN
def main():
    global AVATAR_B64
    os.makedirs(os.path.join(OUT, "m"), exist_ok=True)
    AVATAR_B64 = _avatar()
    print("rendering editorial panels:")
    emit("hero", hero)
    emit("engineering-core", core)
    emit("technology-network", stack)
    emit("project-constellation", constellation)
    for key in PROJECTS:
        emit(key, project_card(key))
    emit("ai-architecture", architecture)
    emit("timeline", journey)
    emit("achievement-hall", achievements)
    emit("research", research)
    emit("certifications", certifications)
    emit("current-mission", mission)
    emit("footer", footer)
    for name, label, w, primary in (("portfolio", "VIEW PORTFOLIO", 212, True), ("linkedin", "LINKEDIN", 150, False),
                                    ("leetcode", "LEETCODE", 150, False), ("email", "EMAIL", 124, False)):
        write(os.path.join(OUT, "btn", name + ".svg"), button(label, w, primary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
