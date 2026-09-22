#!/usr/bin/env python3
"""Wrap the Platane/snk contribution snake in the command-centre HUD frame.

snk renders its SVG with no background (a background is a GIF-only option), so
dropped straight into a README it floats on whatever colour GitHub's theme is.
This nests the generated <svg> - untouched, animation and all - inside a framed
panel from the shared design system, producing one self-contained image that
looks the same in GitHub's light and dark themes.

The snake itself is drawn from the real contribution calendar by snk; nothing
here alters, adds or removes a single cell.

Writes <out.svg> (desktop) and <out>-m.svg (phones: the most recent 26 weeks, larger cells).

Run:  python scripts/compose_activity.py <snk-output.svg> <out.svg> <dot colours, comma-separated>
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import (LINE_2, TEXT, DIM, FAINT, RED, CYAN, MONO, WIDE, NARROW,  # noqa: E402
                   t, header, brackets, svg, write)


def frame(W, vb, inner, colours):
    vx, vy, vw, vh = [float(v) for v in vb.group(1).split()]
    wide = W == WIDE
    x0 = 28 if wide else 20
    view = vb.group(1) if wide else "%g %g %g %g" % (vx + vw / 2, vy, vw / 2, vh)
    span = vw if wide else vw / 2
    sx, sy, sw = x0 - 4, (96 if wide else 110), W - 2 * (x0 - 4)
    sh = sw * vh / span
    H = int(sy + sh + 74)
    b = [header(W, "09", "ACTIVITY MATRIX", "CONTRIBUTION · NEURAL ACTIVITY" if wide else "LAST 26 WEEKS", x=x0)]
    if wide:
        b.append(t(28, 78, "Every cell is one real day of GitHub contributions. The snake is regenerated from "
                           "the live calendar every 12 hours.", 11, DIM, MONO))
    else:
        b.append(t(20, 76, "Every cell is one real day of GitHub", 11, DIM, MONO))
        b.append(t(20, 92, "contributions, redrawn every 12 hours.", 11, DIM, MONO))
    b.append('<rect x="%d" y="%d" width="%d" height="%.1f" rx="10" fill="#0a0c10" stroke="%s"/>'
             % (sx - 8, sy - 8, sw + 16, sh + 16, LINE_2))
    b.append(brackets(sx - 8, sy - 8, sw + 16, sh + 16, CYAN, 12, ".6"))
    b.append('<svg x="%d" y="%d" width="%d" height="%.1f" viewBox="%s" overflow="%s">%s</svg>'
             % (sx, sy, sw, sh, view, "visible" if wide else "hidden", inner))
    b.append('<rect class="sweep" x="%d" y="%d" width="2" height="%.1f" fill="%s" opacity=".35"/>'
             % (sx, sy - 4, sh + 8, CYAN))
    ly = H - 26
    b.append(t(x0, ly, "LESS", 10, DIM, MONO, None, "600", 1.4))
    for i, c in enumerate(colours):
        b.append('<rect x="%d" y="%d" width="11" height="11" rx="2.5" fill="%s" stroke="%s" stroke-opacity=".4"/>'
                 % (x0 + 42 + i * 15, ly - 10, c, LINE_2))
    b.append(t(x0 + 48 + len(colours) * 15, ly, "MORE", 10, DIM, MONO, None, "600", 1.4))
    b.append('<circle cx="%d" cy="%d" r="4" fill="%s"/>' % (x0 + 162, ly - 4, RED))
    b.append(t(x0 + 172, ly, "SNAKE", 10, TEXT, MONO, None, "600", 1.4))
    if wide:
        b.append(t(W - 28, ly, "SOURCE: GITHUB CONTRIBUTION CALENDAR · RENDERED BY PLATANE/SNK", 9.5, FAINT, MONO,
                   "end", None, 1))
    css = (".sweep{animation:sweep 9s linear infinite}"
           "@keyframes sweep{from{transform:translateX(0)}to{transform:translateX(%dpx)}}" % sw)
    return svg(W, H, "".join(b),
               "Activity matrix: the GitHub contribution calendar for the %s, with a snake animation generated "
               "from it by Platane/snk." % ("last year" if wide else "last 26 weeks"), extra_css=css)


def main(src, out, dots):
    raw = open(src, encoding="utf-8").read()
    root = re.search(r"<svg\b([^>]*)>", raw)
    vb = re.search(r'viewBox="([-\d.\s]+)"', root.group(1)) if root else None
    if not root or not vb or "</svg>" not in raw:
        print("ERROR: %s is not a snk SVG" % src, file=sys.stderr)
        return 1
    inner = raw[root.end():raw.rindex("</svg>")]

    colours = [c.strip() for c in dots.split(",")][:5]
    write(out, frame(WIDE, vb, inner, colours))
    # Phones get the most recent half of the year at twice the cell size.
    write(re.sub(r"\.svg$", "-m.svg", out), frame(NARROW, vb, inner, colours))
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(*sys.argv[1:]))
