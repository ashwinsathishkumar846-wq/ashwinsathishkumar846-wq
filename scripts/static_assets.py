#!/usr/bin/env python3
"""Build the narrative SVG assets - the parts that do not change with API data.

Content here is editorial (identity, domains, skills, philosophy) rather than
statistical. Anything with a number in it lives in generate_profile.py instead.

Run:  python scripts/static_assets.py
"""

import base64
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import (BG, PANEL, PANEL_2, GRID, HAIR, STROKE, TEXT, MUTED, DIM, FAINT,
                   CYAN, VIOLET, INDIGO, TEAL, AMBER, MONO, SANS, W,
                   esc, head, brackets, chamfer, panel, label, pulse, svg, write)

OUT = "assets"
AVATAR = "https://avatars.githubusercontent.com/u/271384237?v=4&s=200"


# --------------------------------------------------------------------- hero
def build_hero():
    """Identity module: bevelled glass card, avatar, orbital rings, six domain nodes."""
    try:
        req = urllib.request.Request(AVATAR, headers={"User-Agent": "profile-generator"})
        b64 = base64.b64encode(urllib.request.urlopen(req, timeout=30).read()).decode()
        face = ('<image href="data:image/jpeg;base64,%s" x="306" y="178" width="84" height="84" '
                'clip-path="url(#face)" preserveAspectRatio="xMidYMid slice"/>' % b64)
    except Exception as e:                                    # fail safe: monogram
        print("  ! avatar unavailable (%s) - using monogram" % e)
        face = ('<circle cx="348" cy="220" r="42" fill="%s"/>'
                '<text x="348" y="230" text-anchor="middle" font-family="%s" font-size="26" '
                'font-weight="700" fill="%s">AS</text>' % (PANEL_2, SANS, CYAN))

    nodes = [("AI", 120, 96, CYAN), ("ML", 780, 96, CYAN),
             ("SOFTWARE", 68, 220, VIOLET), ("DATA", 832, 220, TEAL),
             ("SECURITY", 152, 348, AMBER), ("SYSTEMS", 748, 348, INDIGO)]
    wires, chips = [], []
    for i, (t, x, y, c) in enumerate(nodes):
        wires.append('<line x1="%d" y1="%d" x2="450" y2="220" stroke="%s" stroke-opacity=".20" stroke-width="1"/>'
                     % (x, y, c))
        bw = len(t) * 7.3 + 32
        chips.append(
            '<g><rect x="%.1f" y="%d" width="%.1f" height="27" rx="13.5" fill="%s" stroke="%s" stroke-opacity=".42"/>'
            '<circle cx="%.1f" cy="%d" r="3" fill="%s">'
            '<animate attributeName="opacity" values="1;.25;1" dur="%.1fs" repeatCount="indefinite"/></circle>'
            '<text x="%.1f" y="%d" font-family="%s" font-size="10.5" letter-spacing="1.2" fill="#c8d6ee">%s</text></g>'
            % (x - bw / 2, y - 13.5, bw, PANEL, c, x - bw / 2 + 14, y, c, 2.8 + i * .45,
               x - bw / 2 + 24, y + 4, MONO, t))

    body = (
        '<ellipse cx="450" cy="220" rx="420" ry="210" fill="url(#halo)"/>'
        # orbital rings
        '<g fill="none">'
        '<ellipse cx="450" cy="220" rx="330" ry="150" stroke="%s" stroke-opacity=".55" stroke-dasharray="3 8"/>'
        '<ellipse cx="450" cy="220" rx="392" ry="192" stroke="%s" stroke-opacity=".45" stroke-dasharray="2 10"/>'
        '<circle cx="450" cy="220" r="196" stroke="%s" stroke-opacity=".35" stroke-dasharray="4 10">'
        '<animateTransform attributeName="transform" type="rotate" from="0 450 220" to="360 450 220" '
        'dur="60s" repeatCount="indefinite"/></circle></g>'
        '%s%s%s'
        # identity card
        '<g>'
        '<path d="%s" fill="%s" filter="url(#bloom)" opacity=".9"/>'
        '<path d="%s" fill="url(#card)"/>'
        '<path d="%s" fill="none" stroke="url(#rim)" stroke-opacity=".7" stroke-width="1.3"/>'
        '<rect x="286" y="126.2" width="128" height="1.8" fill="url(#rim)"/>'
        '<circle cx="348" cy="220" r="47" fill="none" stroke="%s" stroke-opacity=".3"/>'
        '<circle cx="348" cy="220" r="47" fill="none" stroke="%s" stroke-width="1.6" '
        'stroke-dasharray="46 250" stroke-linecap="round">'
        '<animateTransform attributeName="transform" type="rotate" from="0 348 220" to="360 348 220" '
        'dur="11s" repeatCount="indefinite"/></circle>'
        '%s'
        '<text x="414" y="186" font-family="%s" font-size="33" font-weight="700" letter-spacing="3.6" '
        'fill="url(#ink)">ASHWIN S</text>'
        '<text x="416" y="208" font-family="%s" font-size="9.6" letter-spacing="2.4" fill="%s">'
        'COMPUTER SCIENCE ENGINEER</text>'
        '<line x1="416" y1="222" x2="624" y2="222" stroke="%s"/>'
        '<text x="416" y="243" font-family="%s" font-size="10.5" letter-spacing="1.4" fill="%s">AI'
        '<tspan fill="%s"> / </tspan><tspan fill="%s">SOFTWARE</tspan></text>'
        '<text x="416" y="263" font-family="%s" font-size="10.5" letter-spacing="1.4" fill="%s">DATA'
        '<tspan fill="%s"> / </tspan><tspan fill="%s">SYSTEMS</tspan></text>'
        '</g>'
        '<text x="450" y="424" text-anchor="middle" font-family="%s" font-size="9.5" letter-spacing="2.8" '
        'fill="%s">BUILDING SYSTEMS THAT TURN DATA INTO DECISIONS</text>'
        % (STROKE, "#16203a", "#1a2540",
           "".join(wires), brackets(440), "".join(chips),
           chamfer(250, 127, 400, 186, 16), "#0a0f1e",
           chamfer(250, 127, 400, 186, 16),
           chamfer(250, 127, 400, 186, 16),
           CYAN, CYAN, face,
           SANS, MONO, DIM, "#243350",
           MONO, CYAN, FAINT, VIOLET,
           MONO, TEAL, FAINT, TEXT,
           MONO, "#4d5b78")
    )
    extra = ('<radialGradient id="halo" cx="50%" cy="50%" r="50%">'
             '<stop offset="0%" stop-color="#1d4ed8" stop-opacity=".30"/>'
             '<stop offset="55%" stop-color="#7c3aed" stop-opacity=".10"/>'
             '<stop offset="100%" stop-color="#060910" stop-opacity="0"/></radialGradient>'
             '<linearGradient id="card" x1="0" y1="0" x2="1" y2="1">'
             '<stop offset="0%" stop-color="#141d35"/><stop offset="100%" stop-color="#0a0f1e"/></linearGradient>'
             '<clipPath id="face"><circle cx="348" cy="220" r="42"/></clipPath>')
    write(os.path.join(OUT, "hero.svg"),
          svg("hero", 440, body,
              "Ashwin S, Computer Science Engineer. Domains: AI, ML, software, data, security, systems.",
              extra_defs=(extra,)))


# ---------------------------------------------------------------- hierarchy
def build_hierarchy():
    """The one-glance answer: what this person does, in three verbs."""
    cols = [("BUILDING", "PROJECTS", "full-stack systems, shipped", CYAN, 178),
            ("SOLVING", "LEETCODE", "data structures + algorithms", TEAL, 450),
            ("EXPLORING", "AI / ML", "applied intelligence", VIOLET, 722)]
    parts, ROOT_Y, BOX_Y = [], 78, 150
    for verb, noun, sub, c, x in cols:
        parts.append('<path d="M450 %d V%d Q450 %d %d %d V%d" fill="none" stroke="%s" '
                     'stroke-opacity=".3" stroke-width="1.2"/>'
                     % (ROOT_Y + 16, 116, 132, x, 132, BOX_Y, c))
        parts.append(panel(x - 116, BOX_Y, 232, 78, c))
        parts.append(label(x, BOX_Y + 26, verb, 12.5, c, MONO, "middle", "700", "2.6"))
        parts.append(label(x, BOX_Y + 46, noun, 10, TEXT, MONO, "middle", None, "1.6"))
        parts.append(label(x, BOX_Y + 63, sub, 8.4, DIM, MONO, "middle"))
        parts.append('<path d="M%d %d V%d Q%d %d %d %d V%d" fill="none" stroke="%s" '
                     'stroke-opacity=".3" stroke-width="1.2"/>'
                     % (x, BOX_Y + 78, 250, x, 266, 450, 266, 282, c))
    body = ('%s%s'
            '<g><rect x="366" y="%d" width="168" height="32" rx="16" fill="%s" stroke="%s" stroke-opacity=".7"/>'
            '<text x="450" y="%d" text-anchor="middle" font-family="%s" font-size="12" font-weight="700" '
            'letter-spacing="3" fill="%s">ASHWIN S</text></g>'
            '%s'
            '<g><rect x="330" y="282" width="240" height="30" rx="15" fill="%s" stroke="%s" stroke-opacity=".45"/>'
            '<text x="450" y="301" text-anchor="middle" font-family="%s" font-size="9.6" letter-spacing="2.4" '
            'fill="%s">ENGINEERING SYSTEMS</text></g>'
            % (head("AT A GLANCE", "THREE VERBS"), "".join(parts),
               ROOT_Y - 16, PANEL_2, CYAN, ROOT_Y + 5, SANS, TEXT,
               "", PANEL, INDIGO, MONO, MUTED))
    write(os.path.join(OUT, "hierarchy.svg"),
          svg("hierarchy", 340, body,
              "At a glance: Ashwin S builds projects, solves algorithm problems, and explores AI and ML, "
              "converging on engineering systems."))


# --------------------------------------------------------------- system map
def build_system_map():
    """Neural-style architecture: root, three domains with capabilities, one sink."""
    doms = [("INTELLIGENCE", VIOLET, 168, ["ML / NLP", "Applied AI", "Agentic AI"]),
            ("SOFTWARE", CYAN, 450, ["React / API", "Backend", "Systems"]),
            ("DATA", TEAL, 732, ["Analytics", "SQL", "Modelling"])]
    ROOT, DY, LY, STEP = 100, 180, 378, 32
    parts = []
    for i, (name, c, x, items) in enumerate(doms):
        parts.append('<path d="M450 %d C450 %d %d %d %d %d" fill="none" stroke="%s" '
                     'stroke-opacity=".34" stroke-width="1.4" id="s%d"/>'
                     % (ROOT + 18, ROOT + 62, x, DY - 52, x, DY - 14, c, i))
        parts.append('<circle r="3" fill="%s"><animateMotion dur="%.1fs" repeatCount="indefinite">'
                     '<mpath href="#s%d"/></animateMotion>'
                     '<animate attributeName="opacity" values="0;1;1;0" dur="%.1fs" repeatCount="indefinite"/>'
                     '</circle>' % (c, 3.6 + i * .7, i, 3.6 + i * .7))
        parts.append(panel(x - 118, DY - 14, 236, 40, c, PANEL_2))
        parts.append(label(x, DY + 12, name, 12, c, MONO, "middle", "700", "2.4"))
        for j, it in enumerate(items):
            iy = DY + 60 + j * STEP
            parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-opacity=".22"/>'
                         % (x, DY + 26 if j == 0 else iy - STEP + 11, x, iy - 11, c))
            parts.append('<rect x="%d" y="%d" width="196" height="24" rx="12" fill="%s" stroke="%s" '
                         'stroke-opacity=".25"/>' % (x - 98, iy - 12, PANEL, STROKE))
            parts.append('<circle cx="%d" cy="%d" r="2.6" fill="%s" opacity=".8"/>' % (x - 82, iy, c))
            parts.append(label(x + 8, iy + 3.6, it, 9, MUTED, MONO, "middle"))
        last = DY + 60 + (len(items) - 1) * STEP + 12
        parts.append('<path d="M%d %d C%d %d 450 %d 450 %d" fill="none" stroke="%s" '
                     'stroke-opacity=".28" stroke-width="1.3"/>'
                     % (x, last, x, LY - 30, LY - 44, LY - 14, c))

    body = ('%s'
            '<ellipse cx="450" cy="200" rx="380" ry="170" fill="url(#neb)"/>'
            '%s'
            '<g><path d="%s" fill="%s" stroke="url(#rim)" stroke-opacity=".75" stroke-width="1.3"/>'
            '<text x="450" y="%d" text-anchor="middle" font-family="%s" font-size="17" font-weight="700" '
            'letter-spacing="3.4" fill="%s">ASHWIN S</text></g>'
            '<g><rect x="306" y="%d" width="288" height="38" rx="19" fill="%s" stroke="%s" stroke-opacity=".6"/>'
            '<text x="450" y="%d" text-anchor="middle" font-family="%s" font-size="10.5" letter-spacing="2.8" '
            'fill="%s">ENGINEERING SYSTEMS</text></g>'
            % (head("SYSTEM MAP", "NEURAL ARCHITECTURE"),
               "".join(parts),
               chamfer(354, ROOT - 20, 192, 44, 12), PANEL_2, ROOT + 8, SANS, TEXT,
               LY - 14, PANEL_2, INDIGO, LY + 11, MONO, TEXT))
    extra = ('<radialGradient id="neb" cx="50%" cy="40%" r="60%">'
             '<stop offset="0%" stop-color="#312e81" stop-opacity=".26"/>'
             '<stop offset="100%" stop-color="#060910" stop-opacity="0"/></radialGradient>')
    write(os.path.join(OUT, "system-map.svg"),
          svg("system-map", LY + 62, body,
              "System map: Ashwin S branching into intelligence, software and data capabilities, "
              "converging on engineering systems.", extra_defs=(extra,)))


# ------------------------------------------------------------------- skills
def build_skills():
    """Two honest tiers: proven by the public repos, versus portfolio experience."""
    verified = ["JavaScript", "Java", "Python", "React", "Vite", "Tailwind", "Express",
                "Node.js", "REST", "SQLite", "JWT", "bcrypt", "Helmet", "HTML", "CSS",
                "Docker", "Git", "Vercel"]
    portfolio = ["Machine Learning", "NLP", "Agentic AI", "TensorFlow", "Scikit-learn",
                 "CatBoost", "Pandas", "NumPy", "FastAPI", "SQLAlchemy", "PostgreSQL",
                 "MySQL", "Data Analytics", "Cybersecurity", "Linux", "C"]

    def chips(items, x0, y0, maxw, c, solid):
        out, cx, cy = [], x0, y0
        for name in items:
            bw = len(name) * 6.2 + 28
            if cx + bw > x0 + maxw:
                cx, cy = x0, cy + 27
            if solid:
                out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="21" rx="10.5" fill="%s" '
                           'fill-opacity=".10" stroke="%s" stroke-opacity=".45"/>'
                           % (cx, cy - 10.5, bw, c, c))
                out.append('<circle cx="%.1f" cy="%.1f" r="3" fill="%s"/>' % (cx + 12, cy, c))
                col = "#dbe6f7"
            else:
                out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="21" rx="10.5" fill="%s" '
                           'stroke="%s" stroke-opacity=".38" stroke-dasharray="4 3"/>'
                           % (cx, cy - 10.5, bw, PANEL, c))
                out.append('<circle cx="%.1f" cy="%.1f" r="2.8" fill="none" stroke="%s" stroke-width="1.1"/>'
                           % (cx + 12, cy, c))
                col = "#9aa9c4"
            out.append(label(cx + 21, cy + 3.6, name, 8.8, col))
            cx += bw + 7
        return "".join(out), cy

    def tier(y_top, title, meta, colour, items, solid):
        """One labelled tier: panel, heading, hairline, chips. Returns bottom edge."""
        body_svg, last_row = chips(items, 44, y_top + 66, 812, colour, solid)
        h_panel = (last_row + 22) - y_top
        out = [
            '<rect x="26" y="%d" width="848" height="%.1f" rx="12" fill="%s" stroke="%s" '
            'stroke-opacity=".3"/>' % (y_top, h_panel, PANEL, colour),
            '<rect x="26" y="%d" width="3.5" height="%.1f" rx="1.7" fill="%s" opacity="%s"/>'
            % (y_top, h_panel, colour, ".85" if solid else ".6"),
            label(44, y_top + 26, title, 11.5, colour, MONO, None, "700", "2.4"),
            label(856, y_top + 26, meta, 8.4, FAINT, MONO, "end"),
            '<line x1="44" y1="%d" x2="856" y2="%d" stroke="%s"/>' % (y_top + 38, y_top + 38, HAIR),
            body_svg,
        ]
        return "".join(out), y_top + h_panel

    v_svg, v_bottom = tier(60, "VERIFIED ON GITHUB", "PRESENT IN THE PUBLIC REPOSITORIES",
                           CYAN, verified, True)
    p_svg, p_bottom = tier(v_bottom + 26, "PORTFOLIO / WORKING KNOWLEDGE",
                           "COURSEWORK AND PROJECTS OUTSIDE GITHUB", VIOLET, portfolio, False)
    h = p_bottom + 46

    body = "".join([
        head("SKILL MAP", "TWO TIERS, HONESTLY LABELLED"),
        v_svg, p_svg,
        label(450, h - 20,
              "solid = evidenced in this account's repositories   /   "
              "outlined = experience, not yet published here",
              8.4, FAINT, MONO, "middle"),
    ])
    write(os.path.join(OUT, "skills.svg"),
          svg("skills", h, body,
              "Skill map in two tiers: technologies verified in the public repositories, and portfolio "
              "or working knowledge from coursework and projects outside GitHub."))


# ---------------------------------------------------------------- portfolio
def build_portfolio():
    """Off-GitHub work - labelled unmistakably so nobody mistakes it for a repo."""
    items = [("WORKFORCE CONTRIBUTION MONITOR",
              "Full-stack system measuring real employee impact,",
              "using a scoring algorithm built to reduce bias",
              "React / FastAPI"),
             ("SATELLITE WATER QUALITY PREDICTION",
              "CatBoost model predicting water quality from",
              "satellite and geospatial data, automated pipeline",
              "CatBoost / Python"),
             ("AI CUSTOMER FEEDBACK INTELLIGENCE",
              "Transformer sentiment analysis feeding a",
              "churn-prediction and retention pipeline",
              "Transformers / NLP")]
    cards = []
    for i, (n, l1, l2, tech) in enumerate(items):
        y = 108 + i * 104
        cards.append(panel(26, y, 848, 88, VIOLET, PANEL, 13, dashed=True, op=".34"))
        cards.append('<rect x="26" y="%d" width="3.5" height="88" rx="1.7" fill="%s" opacity=".5"/>' % (y, VIOLET))
        cards.append('<g><rect x="694" y="%d" width="160" height="19" rx="9.5" fill="%s" fill-opacity=".12" '
                     'stroke="%s" stroke-opacity=".5"/>'
                     '<text x="774" y="%d" text-anchor="middle" font-family="%s" font-size="7.6" '
                     'letter-spacing="1.5" fill="%s">PORTFOLIO PROJECT</text></g>'
                     % (y + 14, VIOLET, VIOLET, y + 27, MONO, VIOLET))
        cards.append(label(46, y + 30, n, 12.5, TEXT, SANS, None, "700", "1.2"))
        cards.append(label(46, y + 51, l1, 8.8, MUTED))
        cards.append(label(46, y + 65, l2, 8.8, MUTED))
        cards.append(label(46, y + 81, tech, 8.4, VIOLET))
        cards.append(label(854, y + 81, "no public repository", 7.8, FAINT, MONO, "end"))

    body = ('%s'
            '<rect x="26" y="60" width="848" height="34" rx="10" fill="%s" fill-opacity=".07" '
            'stroke="%s" stroke-opacity=".35" stroke-dasharray="5 4"/>'
            '<circle cx="48" cy="77" r="4" fill="%s"/>'
            '<text x="62" y="81" font-family="%s" font-size="9" letter-spacing="1.4" fill="%s">'
            'These are coursework and hackathon builds, not repositories on this account. '
            'No source links are offered because none exist.</text>'
            '%s'
            % (head("BEYOND GITHUB", "SELECTED WORK"),
               VIOLET, VIOLET, VIOLET, MONO, MUTED, "".join(cards)))
    write(os.path.join(OUT, "portfolio.svg"),
          svg("portfolio", 108 + 3 * 104 + 16, body,
              "Selected work built outside GitHub: three portfolio projects, clearly marked as having "
              "no public repository."))


# ------------------------------------------------------------------- vector
def build_vector():
    """Where the work is heading - six areas along a single directional axis."""
    areas = [("AGENTIC AI", VIOLET), ("PRODUCTION AI", VIOLET), ("MACHINE LEARNING", CYAN),
             ("SOFTWARE ENG", CYAN), ("DATA ANALYTICS", TEAL), ("CYBERSECURITY", AMBER)]
    AY = 138
    parts = ['<line x1="52" y1="%d" x2="820" y2="%d" stroke="url(#vec)" stroke-width="1.6"/>'
             '<path d="M820 %d l-11 -5 v10 z" fill="%s"/>' % (AY, AY, AY, AMBER)]
    for i, (t, c) in enumerate(areas):
        x = 100 + i * 130
        up = i % 2 == 0
        ty = AY - 30 if up else AY + 42
        parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-opacity=".3"/>'
                     % (x, AY, x, ty + (10 if up else -12), c))
        parts.append(pulse(x, AY, 4, c, 2.8 + i * .4))
        parts.append(label(x, ty, t, 9.4, c, MONO, "middle", "700", "1.2"))
    body = ('%s%s'
            '<text x="450" y="216" text-anchor="middle" font-family="%s" font-size="8.6" letter-spacing="2" '
            'fill="%s">DIRECTION OF TRAVEL, NOT A CLAIM OF MASTERY</text>'
            % (head("CURRENT VECTOR", "WHERE THIS IS GOING"), "".join(parts), MONO, FAINT))
    extra = ('<linearGradient id="vec" x1="0" y1="0" x2="1" y2="0">'
             '<stop offset="0%" stop-color="#8b5cf6"/><stop offset="50%" stop-color="#22d3ee"/>'
             '<stop offset="100%" stop-color="#f59e0b"/></linearGradient>')
    write(os.path.join(OUT, "vector.svg"),
          svg("vector", 240, body,
              "Current vector: agentic AI, production AI, machine learning, software engineering, "
              "data analytics, cybersecurity.", extra_defs=(extra,)))


# --------------------------------------------------------------- philosophy
def build_philosophy():
    """BUILD - LEARN - SHIP - MEASURE - ITERATE as a closed loop."""
    import math
    steps = [("BUILD", CYAN), ("LEARN", VIOLET), ("SHIP", TEAL), ("MEASURE", INDIGO), ("ITERATE", AMBER)]
    cx, cy, r = 450, 176, 96
    parts = ['<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-opacity=".45" '
             'stroke-dasharray="3 7"/>' % (cx, cy, r, STROKE)]
    pts = []
    for i, (t, c) in enumerate(steps):
        a = -math.pi / 2 + i * 2 * math.pi / len(steps)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        pts.append((x, y, t, c))
    for i, (x, y, t, c) in enumerate(pts):
        nx, ny, _, _ = pts[(i + 1) % len(pts)]
        parts.append('<path d="M%.1f %.1f A%d %d 0 0 1 %.1f %.1f" fill="none" stroke="%s" '
                     'stroke-opacity=".38" stroke-width="1.4"/>' % (x, y, r, r, nx, ny, c))
    for i, (x, y, t, c) in enumerate(pts):
        tw = len(t) * 6.6 + 26
        parts.append('<rect x="%.1f" y="%.1f" width="%.1f" height="24" rx="12" fill="%s" stroke="%s" '
                     'stroke-opacity=".55"/>' % (x - tw / 2, y - 12, tw, PANEL_2, c))
        parts.append(label(x, y + 4, t, 9.6, c, MONO, "middle", "700", "1.6"))
    body = ('%s%s'
            '<text x="%d" y="%d" text-anchor="middle" font-family="%s" font-size="10" font-weight="700" '
            'letter-spacing="2.4" fill="%s">LOOP</text>'
            '<text x="%d" y="%d" text-anchor="middle" font-family="%s" font-size="8" letter-spacing="1.4" '
            'fill="%s">not a checklist</text>'
            % (head("BUILD PHILOSOPHY", "HOW THE WORK MOVES"), "".join(parts),
               cx, cy - 2, MONO, TEXT, cx, cy + 14, MONO, FAINT))
    write(os.path.join(OUT, "philosophy.svg"),
          svg("philosophy", 320, body,
              "Build philosophy loop: build, learn, ship, measure, iterate."))


# -------------------------------------------------------------- achievements
def build_achievements():
    awards = [("1ST PRIZE", "HackTIDE Hackathon", "2026", AMBER),
              ("1ST PRIZE", "IDEATHON Hackathon", "2026", AMBER),
              ("RUNNER-UP", "CRYPTERA", "2025", CYAN)]
    certs = [("ServiceNow AI Essentials", VIOLET), ("Agentic AI (ServiceNow)", VIOLET),
             ("Celonis Foundations", INDIGO), ("IBM LinuxONE", INDIGO)]
    parts = []
    for i, (a, b, yr, c) in enumerate(awards):
        x, y = 26 + i * 288, 72
        parts.append(panel(x, y, 268, 92, c, PANEL, 12, op=".4"))
        parts.append('<path d="M%d %d l6-10 6 10 11 2-8 8 2 11-11-6-11 6 2-11-8-8z" fill="%s" opacity=".85"/>'
                     % (x + 18, y + 32, c))
        parts.append(label(x + 18, y + 62, a, 13.5, c, SANS, None, "700", "1.3"))
        parts.append(label(x + 18, y + 80, b, 8.8, "#c8d6ee"))
        parts.append(label(x + 250, y + 32, yr, 8, DIM, MONO, "end"))
    for i, (t, c) in enumerate(certs):
        x, y = 26 + i * 216, 190
        parts.append('<rect x="%d" y="%d" width="196" height="56" rx="11" fill="%s" stroke="%s" '
                     'stroke-opacity=".45"/>' % (x, y, PANEL, STROKE))
        parts.append('<circle cx="%d" cy="%d" r="7" fill="none" stroke="%s" stroke-opacity=".7"/>' % (x + 20, y + 28, c))
        parts.append('<path d="M%.1f %d l3 3 5-6" fill="none" stroke="%s" stroke-width="1.6" '
                     'stroke-linecap="round"/>' % (x + 16.5, y + 28, c))
        parts.append(label(x + 36, y + 25, t, 8.4, "#dbe6f7"))
        parts.append(label(x + 36, y + 39, "certification", 7.6, FAINT))
    body = ('%s%s%s' % (head("ACHIEVEMENTS", "AWARDS + CERTIFICATIONS"), "".join(parts),
                        label(26, 274, "AWARDS AND CERTIFICATIONS ARE SELF-REPORTED FROM THE PROFILE, "
                                       "NOT VERIFIABLE THROUGH THE GITHUB API", 8, FAINT, MONO, None, None, "1.3")))
    write(os.path.join(OUT, "achievements.svg"),
          svg("achievements", 292, body,
              "Achievements: two first prizes, one runner-up, and four certifications, all self-reported."))


# ------------------------------------------------------------------- footer
def build_footer():
    links = [("GITHUB", "ashwinsathishkumar846-wq", CYAN),
             ("LINKEDIN", "ashwin-s--", INDIGO),
             ("EMAIL", "ashwinsathishkumar846@gmail.com", TEAL),
             ("LEETCODE", "ashwin1122", AMBER)]
    cols = []
    for i, (t, v, c) in enumerate(links):
        x = 40 + i * 208
        cols.append('<rect x="%d" y="98" width="188" height="62" rx="11" fill="%s" stroke="%s" '
                    'stroke-opacity=".38"/>' % (x, PANEL, c))
        cols.append('<circle cx="%d" cy="129" r="4" fill="%s">'
                    '<animate attributeName="opacity" values="1;.3;1" dur="%.1fs" repeatCount="indefinite"/>'
                    '</circle>' % (x + 18, c, 2.6 + i * .4))
        cols.append(label(x + 32, 123, t, 9.4, c, MONO, None, "700", "1.8"))
        cols.append(label(x + 32, 139, v, 7.4, MUTED))
    body = ('<rect width="900" height="232" rx="14" fill="url(#fh)"/>'
            '<rect x="330" y="0" width="240" height="2.4" fill="url(#rim)"/>'
            '<text x="450" y="54" text-anchor="middle" font-family="%s" font-size="26" font-weight="700" '
            'letter-spacing="7" fill="%s">LET&#39;S BUILD</text>'
            '<text x="450" y="76" text-anchor="middle" font-family="%s" font-size="8.8" letter-spacing="2.6" '
            'fill="%s">OPEN TO AI / ML AND SOFTWARE ENGINEERING INTERNSHIPS</text>'
            '%s<line x1="26" y1="186" x2="874" y2="186" stroke="%s"/>'
            '<text x="450" y="208" text-anchor="middle" font-family="%s" font-size="9" letter-spacing="3.4" '
            'fill="%s">AI<tspan fill="%s"> / </tspan><tspan fill="%s">SYSTEMS</tspan>'
            '<tspan fill="%s"> / </tspan><tspan fill="%s">SOFTWARE</tspan>'
            '<tspan fill="%s"> / </tspan><tspan fill="%s">INNOVATION</tspan></text>'
            % (SANS, TEXT, MONO, DIM, "".join(cols), HAIR, MONO, CYAN,
               FAINT, VIOLET, FAINT, TEAL, FAINT, AMBER))
    extra = ('<radialGradient id="fh" cx="50%" cy="0%" r="90%">'
             '<stop offset="0%" stop-color="#1d4ed8" stop-opacity=".24"/>'
             '<stop offset="100%" stop-color="#060910" stop-opacity="0"/></radialGradient>')
    write(os.path.join(OUT, "footer.svg"),
          svg("footer", 232, body,
              "Contact: GitHub, LinkedIn, email and LeetCode links for Ashwin S.", extra_defs=(extra,)))


def main():
    os.makedirs(OUT, exist_ok=True)
    print("building static assets:")
    build_hero()
    build_hierarchy()
    build_system_map()
    build_skills()
    build_portfolio()
    build_vector()
    build_philosophy()
    build_achievements()
    build_footer()


if __name__ == "__main__":
    main()
