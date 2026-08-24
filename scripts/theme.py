"""Shared design system for the profile SVG assets.

One palette, one type scale, one set of panel primitives - so every asset in
assets/ reads as part of the same interface rather than a pile of graphics.
"""

# ----------------------------------------------------------------- palette
BG      = "#060910"   # page ground - dark graphite
PANEL   = "#0a1020"   # panel fill
PANEL_2 = "#0d1426"   # raised panel fill
GRID    = "#111a2c"   # technical grid
HAIR    = "#1b2740"   # hairline rules
STROKE  = "#22304e"   # neutral panel border

TEXT    = "#e8eef9"
MUTED   = "#93a1bd"
DIM     = "#5d6b87"
FAINT   = "#3a4763"

CYAN    = "#22d3ee"
VIOLET  = "#8b5cf6"
INDIGO  = "#6366f1"
TEAL    = "#2dd4bf"
AMBER   = "#f59e0b"

MONO = "'JetBrains Mono','Consolas','SF Mono',Menlo,monospace"
SANS = "'Segoe UI',system-ui,-apple-system,Helvetica,Arial,sans-serif"

W = 900  # every asset shares one canvas width so they stack as a single column


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def defs(*extra):
    """Grid pattern plus the gradients every asset shares."""
    return (
        '<defs>'
        '<pattern id="grid" width="34" height="34" patternUnits="userSpaceOnUse">'
        '<path d="M34 0H0V34" fill="none" stroke="%s" stroke-width="1"/></pattern>'
        '<linearGradient id="rim" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0%%" stop-color="%s"/><stop offset="50%%" stop-color="%s"/>'
        '<stop offset="100%%" stop-color="%s"/></linearGradient>'
        '<linearGradient id="ink" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0%%" stop-color="#ffffff"/><stop offset="100%%" stop-color="#7dd3fc"/></linearGradient>'
        '<filter id="bloom" x="-70%%" y="-70%%" width="240%%" height="240%%">'
        '<feGaussianBlur stdDeviation="9"/></filter>'
        '%s</defs>' % (GRID, CYAN, INDIGO, VIOLET, "".join(extra))
    )


def ground(h, w=W):
    """Background plate: graphite fill + technical grid."""
    return ('<rect width="%d" height="%d" rx="14" fill="%s"/>'
            '<rect width="%d" height="%d" rx="14" fill="url(#grid)"/>' % (w, h, BG, w, h))


def head(title, right="", w=W):
    """Section eyebrow: '// TITLE' left, meta right, hairline under."""
    out = ('<text x="26" y="34" font-family="%s" font-size="10" letter-spacing="2.6" fill="%s">// %s</text>'
           % (MONO, FAINT, title))
    if right:
        out += ('<text x="%d" y="34" text-anchor="end" font-family="%s" font-size="10" '
                'letter-spacing="2" fill="%s">%s</text>' % (w - 26, MONO, FAINT, right))
    out += '<line x1="26" y1="46" x2="%d" y2="46" stroke="%s"/>' % (w - 26, HAIR)
    return out


def brackets(h, w=W, colour=CYAN, inset=18, size=26, op=".55"):
    """HUD corner brackets."""
    return ('<g stroke="%s" stroke-width="1.5" fill="none" opacity="%s">'
            '<path d="M%d %dV%dh%d"/><path d="M%d %dV%dh-%d"/>'
            '<path d="M%d %dv%dh%d"/><path d="M%d %dv%dh-%d"/></g>'
            % (colour, op,
               inset, inset + size, inset, size,
               w - inset, inset + size, inset, size,
               inset, h - inset - size, size, size,
               w - inset, h - inset - size, size, size))


def chamfer(x, y, w, h, c=14):
    """Path for a bevelled-corner HUD panel."""
    return ("M%.1f %.1f H%.1f L%.1f %.1f V%.1f L%.1f %.1f H%.1f L%.1f %.1f V%.1f Z"
            % (x + c, y, x + w - c, x + w, y + c, y + h - c,
               x + w - c, y + h, x + c, x, y + h - c, y + c))


def panel(x, y, w, h, accent=None, fill=PANEL, rx=12, dashed=False, op=".38"):
    """Standard glass panel with an optional accent edge on the left."""
    dash = ' stroke-dasharray="5 4"' if dashed else ''
    stroke = accent or STROKE
    out = ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%d" fill="%s" '
           'stroke="%s" stroke-opacity="%s"%s/>' % (x, y, w, h, rx, fill, stroke, op, dash))
    if accent:
        out += ('<rect x="%.1f" y="%.1f" width="3.5" height="%.1f" rx="1.7" fill="%s" opacity=".85"/>'
                % (x, y, h, accent))
    return out


def label(x, y, s, size=8.8, fill=None, family=None, anchor=None, weight=None, ls=None):
    a = ' text-anchor="%s"' % anchor if anchor else ''
    wt = ' font-weight="%s"' % weight if weight else ''
    sp = ' letter-spacing="%s"' % ls if ls else ''
    return ('<text x="%.1f" y="%.1f" font-family="%s" font-size="%s" fill="%s"%s%s%s>%s</text>'
            % (x, y, family or MONO, size, fill or MUTED, a, wt, sp, esc(s)))


def pulse(cx, cy, r, colour, dur=3.0):
    """A dot with an expanding ring - the shared 'live node' motif."""
    return ('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>'
            '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-opacity=".45">'
            '<animate attributeName="r" values="%.1f;%.1f;%.1f" dur="%.1fs" repeatCount="indefinite"/>'
            '<animate attributeName="stroke-opacity" values=".5;0;.5" dur="%.1fs" repeatCount="indefinite"/>'
            '</circle>' % (cx, cy, r, colour, cx, cy, r * 2, colour, r * 1.6, r * 3.4, r * 1.6, dur, dur))


def svg(name, h, body, aria, w=W, extra_defs=()):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
            'role="img" aria-label="%s">%s%s%s</svg>'
            % (w, h, w, h, esc(aria), defs(*extra_defs), ground(h, w), body))


def write(path, content):
    open(path, "w", encoding="utf-8").write(content)
    print("  %-34s %6d b" % (path, len(content)))
