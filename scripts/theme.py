"""Design system for every SVG panel on the profile.

One palette, one type scale, one set of primitives, so the README reads as a
single interface rather than a stack of unrelated graphics.

The palette is shared with the portfolio (ashwin-portfolio-tan.vercel.app):
near-black ground, bone type and one signal red, extended here with cyan and
violet for the "intelligence" layer of the command centre.

Every panel is rendered twice: WIDE (900 px canvas, desktop and tablet) and
NARROW (440 px canvas, phones). The README picks between them with
<picture><source media="(max-width: 640px)">, so text never has to shrink below
a readable size on a phone.
"""

import math

# ------------------------------------------------------------------ palette
BG      = "#07080b"   # ground, portfolio ink
PANEL   = "#0c0e13"
PANEL_2 = "#11141b"
GRIDC   = "#12151c"
LINE    = "#1d212b"
LINE_2  = "#2a303d"

TEXT    = "#edebe6"   # portfolio paper
MUTED   = "#a3a8b4"
DIM     = "#6b7180"
FAINT   = "#454b59"

RED     = "#e0473f"   # portfolio signal accent, used sparingly
CYAN    = "#3dd6f5"
BLUE    = "#4f8cff"
VIOLET  = "#9b7bff"
TEAL    = "#34d8b0"
GOLD    = "#f2b544"
SILVER  = "#c9d3e0"
BRONZE  = "#d9905f"

SANS = "'Inter Tight','Inter','Segoe UI',system-ui,-apple-system,'Helvetica Neue',Arial,sans-serif"
MONO = "'JetBrains Mono','SF Mono','Cascadia Mono',Consolas,Menlo,monospace"

WIDE, NARROW = 900, 440

# Motion is CSS wherever possible so prefers-reduced-motion can switch it off.
CSS = (
    ".flow{stroke-dasharray:3 7;animation:flow 1.8s linear infinite}"
    ".flow-slow{stroke-dasharray:2 10;animation:flow 4s linear infinite}"
    ".orbit{stroke-dasharray:1 7;animation:orbit 9s linear infinite}"
    "@keyframes flow{to{stroke-dashoffset:-20}}"
    "@keyframes orbit{to{stroke-dashoffset:-160}}"
    ".blink{animation:blink 2.8s ease-in-out infinite}"
    "@keyframes blink{0%,100%{opacity:.3}50%{opacity:1}}"
    ".ping{animation:ping 3.2s ease-out infinite;transform-box:fill-box;transform-origin:center}"
    "@keyframes ping{0%{transform:scale(.5);opacity:.8}100%{transform:scale(2.4);opacity:0}}"
    ".d1{animation-delay:.6s}.d2{animation-delay:1.2s}.d3{animation-delay:1.8s}.d4{animation-delay:2.4s}"
    ".shine{animation:shine 7s ease-in-out infinite}"
    "@keyframes shine{0%,55%{transform:translateX(-160px)}100%{transform:translateX(760px)}}"
    ".scan{animation:scan 7s linear infinite}"
    "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
)


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ------------------------------------------------------------- text metrics
def text_w(s, size, mono=True, ls=0.0, weight=400):
    """Approximate rendered width. Generous on purpose: system fonts vary."""
    per = 0.61 if mono else (0.6 if weight >= 600 else 0.54)
    return len(s) * (size * per + ls)


def wrap(s, max_chars):
    lines, cur = [], ""
    for word in s.split():
        if cur and len(cur) + 1 + len(word) > max_chars:
            lines.append(cur)
            cur = word
        else:
            cur = (cur + " " + word).strip()
    if cur:
        lines.append(cur)
    return lines


# --------------------------------------------------------------- primitives
def t(x, y, s, size=12, fill=MUTED, font=MONO, anchor=None, weight=None, ls=None,
      op=None, cls=None, extra=""):
    a = ' text-anchor="%s"' % anchor if anchor else ""
    w = ' font-weight="%s"' % weight if weight else ""
    l = ' letter-spacing="%s"' % ls if ls is not None else ""
    o = ' opacity="%s"' % op if op is not None else ""
    c = ' class="%s"' % cls if cls else ""
    return ('<text x="%.1f" y="%.1f" font-family="%s" font-size="%s" fill="%s"%s%s%s%s%s%s>%s</text>'
            % (x, y, font, size, fill, a, w, l, o, c, extra, esc(s)))


def lines(x, y, rows, size=12, fill=MUTED, font=SANS, lh=None, **kw):
    lh = lh or size * 1.45
    return "".join(t(x, y + i * lh, r, size, fill, font, **kw) for i, r in enumerate(rows))


def chip(x, y, s, colour=CYAN, size=10.5, filled=False, h=22, text_fill=None, ls=0.6, anchor="start"):
    """Pill label. Returns (svg, width)."""
    w = text_w(s, size, True, ls) + 20
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    fo = ".2" if filled else "0"
    out = ('<rect x="%.1f" y="%.1f" width="%.1f" height="%d" rx="%.1f" fill="%s" fill-opacity="%s" '
           'stroke="%s" stroke-opacity="%s"/>' % (x, y, w, h, h / 2, colour, fo, colour,
                                                   ".7" if filled else ".38"))
    out += t(x + w / 2, y + h / 2 + size * 0.36, s, size, text_fill or (colour if filled else "#d7dbe3"),
             MONO, "middle", None, ls)
    return out, w


def chips(x, y, items, max_w, colour=CYAN, size=10.5, gap=6, row_h=28, **kw):
    """Flowing chip rows. Returns (svg, bottom_y)."""
    out, cx, cy = [], x, y
    for it in items:
        label, col, filled = (it if isinstance(it, tuple) else (it, colour, False))
        w = text_w(label, size, True, kw.get("ls", 0.6)) + 20
        if cx + w > x + max_w and cx > x:
            cx, cy = x, cy + row_h
        s, w = chip(cx, cy, label, col, size, filled, **kw)
        out.append(s)
        cx += w + gap
    return "".join(out), cy + row_h - 6


def panel(x, y, w, h, accent=None, rx=12, fill="url(#pg)", op=".9", glow=False):
    """Glass panel: gradient fill, hairline border, lit top edge."""
    out = ""
    if glow and accent:
        out += ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%d" fill="%s" opacity=".10" '
                'filter="url(#soft)"/>' % (x, y, w, h, rx, accent))
    out += ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%d" fill="%s" stroke="%s" '
            'stroke-opacity="%s"/>' % (x, y, w, h, rx, fill, LINE_2, op))
    out += ('<rect x="%.1f" y="%.1f" width="%.1f" height="1" fill="url(#edge)"/>' % (x + rx, y, w - 2 * rx))
    if accent:
        out += ('<rect x="%.1f" y="%.1f" width="%.1f" height="2" rx="1" fill="%s"/>'
                % (x + 18, y - 1, min(64, w / 3), accent))
    return out


def brackets(x, y, w, h, colour=CYAN, size=14, op=".55"):
    return ('<g stroke="%s" stroke-width="1.4" fill="none" opacity="%s">'
            '<path d="M%.1f %.1fV%.1fH%.1f"/><path d="M%.1f %.1fV%.1fH%.1f"/>'
            '<path d="M%.1f %.1fV%.1fH%.1f"/><path d="M%.1f %.1fV%.1fH%.1f"/></g>'
            % (colour, op,
               x, y + size, y, x + size,
               x + w, y + size, y, x + w - size,
               x, y + h - size, y + h, x + size,
               x + w, y + h - size, y + h, x + w - size))


def node(cx, cy, r, colour, ping=True, delay=""):
    out = ('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity=".18" filter="url(#glow)"/>'
           '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>'
           % (cx, cy, r * 2.6, colour, cx, cy, r, colour))
    if ping:
        out += ('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" class="ping %s"/>'
                % (cx, cy, r * 1.4, colour, delay))
    return out


def flow(d, colour=CYAN, op=".55", width=1.2, cls="flow", base_op=".14"):
    """A connection: faint static rail with a moving dash over it."""
    return ('<path d="%s" fill="none" stroke="%s" stroke-opacity="%s" stroke-width="%s"/>'
            '<path d="%s" fill="none" stroke="%s" stroke-opacity="%s" stroke-width="%s" class="%s"/>'
            % (d, colour, base_op, width, d, colour, op, width, cls))


def packet(d, colour=CYAN, dur=5, r=2.6, begin="0s"):
    """A single light packet travelling a path (SMIL, used sparingly)."""
    return ('<circle r="%s" fill="%s"><animateMotion dur="%ss" begin="%s" repeatCount="indefinite" '
            'path="%s"/></circle>' % (r, colour, dur, begin, d))


def header(w, idx, title, meta="", y=40, x=28):
    """Section eyebrow:  06 // TITLE ................ META"""
    out = t(x, y, idx, 11, RED, MONO, None, "700", 2)
    out += t(x + 26, y, "//", 11, FAINT, MONO, None, None, 1)
    out += t(x + 48, y, title, 11.5, TEXT, MONO, None, "600", 3)
    if meta:
        out += t(w - x, y, meta, 10, DIM, MONO, "end", None, 1.6)
    out += '<rect x="%d" y="%d" width="%d" height="1" fill="url(#hair)"/>' % (x, y + 14, w - 2 * x)
    out += '<rect x="%d" y="%d" width="28" height="1" fill="%s"/>' % (x, y + 14, RED)
    return out


def iso_box(x, y, w, h, depth=10, fill=PANEL_2, side="#0a0c10", top="#161a23", stroke=LINE_2, dx=None):
    """Pseudo-3D slab: front face plus a receding top and right face."""
    dx = depth if dx is None else dx
    return ('<path d="M%.1f %.1f l%.1f %.1f h%.1f l%.1f %.1f z" fill="%s" stroke="%s" stroke-opacity=".7"/>'
            '<path d="M%.1f %.1f l%.1f %.1f v%.1f l%.1f %.1f z" fill="%s" stroke="%s" stroke-opacity=".7"/>'
            '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-opacity=".9"/>'
            % (x, y, dx, -depth, w, -dx, depth, top, stroke,
               x + w, y, dx, -depth, h, -dx, depth, side, stroke,
               x, y, w, h, fill, stroke))


def stars(w, h, n=70, seed=7, colour="#8fa3c0"):
    """Deterministic star field (same output every run, so no churn in git)."""
    out, s = [], seed
    for _ in range(n):
        s = (s * 1103515245 + 12345) & 0x7FFFFFFF
        x = s % w
        s = (s * 1103515245 + 12345) & 0x7FFFFFFF
        y = s % h
        s = (s * 1103515245 + 12345) & 0x7FFFFFFF
        r = 0.5 + (s % 100) / 100.0
        op = 0.15 + (s % 60) / 100.0
        out.append('<circle cx="%d" cy="%d" r="%.2f" fill="%s" opacity="%.2f"/>' % (x, y, r, colour, op))
    return "".join(out)


# ---------------------------------------------------------------- wordmark
# A bespoke geometric wordmark, drawn as stroked centre-lines rather than set in
# a font, so it renders identically on every OS (SVGs inside <img> cannot load
# web fonts). Glyph box: 54 x 78, stroke 13, chamfer 10.
_GLYPHS = {
    "A": ("M0 78V10L10 0H44L54 10V78M0 44H54", 54),
    "S": ("M54 0H10L0 10V29L10 39H44L54 49V68L44 78H0", 54),
    "H": ("M0 0V78M54 0V78M0 39H54", 54),
    "W": ("M0 0V68L10 78H44L54 68V0M27 32V78", 54),
    "I": ("M0 0V78", 0),
    "N": ("M0 78V0L54 78V0", 54),
    " ": ("", 14),
}
_STROKE, _GAP = 13, 13


def wordmark_width(text="ASHWIN S", scale=1.0):
    total = 0
    for ch in text:
        total += _GLYPHS[ch][1] + _STROKE + _GAP
    return (total - _GAP) * scale


def wordmark(x, y, scale=1.0, text="ASHWIN S", fill="url(#wm)", extrude=4, shine=True, mid="wmk"):
    """Returns the wordmark with a stepped extrusion (pseudo-3D) and a light sweep."""
    paths, cx = [], _STROKE / 2
    for ch in text:
        d, w = _GLYPHS[ch]
        if d:
            paths.append('<path d="%s" transform="translate(%.1f %.1f)"/>' % (d, cx, _STROKE / 2))
        cx += w + _STROKE + _GAP
    glyphs = "".join(paths)
    common = 'fill="none" stroke-width="%d" stroke-linecap="square" stroke-linejoin="miter" stroke-miterlimit="2"' % _STROKE
    out = '<g transform="translate(%.1f %.1f) scale(%.4f)">' % (x, y, scale)
    for i in range(extrude, 0, -1):          # extrusion, deepest first
        shade = ["#0b1320", "#0e1a2c", "#122238", "#172b45", "#1c3452"][min(i - 1, 4)]
        out += '<g %s stroke="%s" transform="translate(%d %d)">%s</g>' % (common, shade, i * 2, i * 2, glyphs)
    out += '<g %s stroke="%s">%s</g>' % (common, fill, glyphs)
    if shine:
        out += ('<mask id="%s"><g %s stroke="#fff">%s</g></mask>'
                '<g mask="url(#%s)"><rect class="shine" x="-40" y="-20" width="70" height="140" '
                'fill="url(#sheen)" transform="skewX(-18)"/></g>' % (mid, common, glyphs, mid))
    out += "</g>"
    return out


# -------------------------------------------------------------- document
def base_defs(w, h):
    return (
        '<pattern id="g" width="28" height="28" patternUnits="userSpaceOnUse">'
        '<path d="M28 0H0V28" fill="none" stroke="%s" stroke-width="1"/></pattern>'
        '<radialGradient id="gf" cx="50%%" cy="45%%" r="65%%">'
        '<stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>'
        '</radialGradient>'
        '<mask id="gm"><rect width="%d" height="%d" fill="url(#gf)"/></mask>'
        '<linearGradient id="pg" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#12151d"/><stop offset="1" stop-color="#0a0c11"/></linearGradient>'
        '<linearGradient id="edge" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".22"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        '<linearGradient id="hair" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="%s"/><stop offset=".7" stop-color="%s"/>'
        '<stop offset="1" stop-color="%s" stop-opacity="0"/></linearGradient>'
        '<linearGradient id="rim" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="%s"/><stop offset=".5" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
        '</linearGradient>'
        '<linearGradient id="wm" x1="0" y1="0" x2="0" y2="91" gradientUnits="userSpaceOnUse">'
        '<stop offset="0" stop-color="#ffffff"/><stop offset=".55" stop-color="%s"/>'
        '<stop offset="1" stop-color="#8fe3f5"/></linearGradient>'
        '<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".85"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        '<linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#fff1c7"/><stop offset=".45" stop-color="%s"/>'
        '<stop offset="1" stop-color="#8a5a12"/></linearGradient>'
        '<linearGradient id="silver" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#ffffff"/><stop offset=".5" stop-color="%s"/>'
        '<stop offset="1" stop-color="#5d6878"/></linearGradient>'
        '<linearGradient id="bronze" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#ffd9bd"/><stop offset=".5" stop-color="%s"/>'
        '<stop offset="1" stop-color="#6b3818"/></linearGradient>'
        '<filter id="glow" x="-100%%" y="-100%%" width="300%%" height="300%%"><feGaussianBlur stdDeviation="4"/></filter>'
        '<filter id="soft" x="-50%%" y="-50%%" width="200%%" height="200%%"><feGaussianBlur stdDeviation="18"/></filter>'
        % (GRIDC, w, h, LINE_2, LINE, LINE, CYAN, BLUE, VIOLET, TEXT, GOLD, SILVER, BRONZE)
    )


def ground(w, h):
    return ('<rect width="%d" height="%d" rx="16" fill="%s"/>'
            '<rect width="%d" height="%d" rx="16" fill="url(#g)" mask="url(#gm)"/>'
            '<rect x=".5" y=".5" width="%d" height="%d" rx="16" fill="none" stroke="%s"/>'
            % (w, h, BG, w, h, w - 1, h - 1, LINE))


def svg(w, h, body, aria, extra_defs="", extra_css=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'width="%d" height="%d" viewBox="0 0 %d %d" role="img" aria-label="%s">'
            '<title>%s</title><style>%s%s</style><defs>%s%s</defs>%s%s</svg>'
            % (w, h, w, h, esc(aria), esc(aria), CSS, extra_css, base_defs(w, h), extra_defs,
               ground(w, h), body))


def write(path, content):
    import os
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("  %-40s %7d b" % (path, len(content.encode("utf-8"))))


def ellipse_pt(cx, cy, rx, ry, rot_deg, theta_deg):
    th, ph = math.radians(theta_deg), math.radians(rot_deg)
    ex, ey = rx * math.cos(th), ry * math.sin(th)
    return cx + ex * math.cos(ph) - ey * math.sin(ph), cy + ex * math.sin(ph) + ey * math.cos(ph)
