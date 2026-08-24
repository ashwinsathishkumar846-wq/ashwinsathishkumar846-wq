#!/usr/bin/env python3
"""Generate assets/stats.svg and assets/activity.svg from live GitHub data.

Every number rendered here is read from the GitHub API or from the public
contributions calendar. Nothing is estimated, padded or hard-coded.

Usage:  python scripts/generate_stats.py
Env:    GITHUB_TOKEN (optional) - only used to raise the API rate limit.
"""

import datetime as dt
import json
import os
import re
import urllib.request

USER = "ashwinsathishkumar846-wq"
OUT = "assets"

MONO = "'JetBrains Mono','Consolas','SF Mono',Menlo,monospace"
SANS = "'Segoe UI',system-ui,-apple-system,Helvetica,Arial,sans-serif"
GRID = ('<pattern id="gg" width="34" height="34" patternUnits="userSpaceOnUse">'
        '<path d="M34 0H0V34" fill="none" stroke="#101728" stroke-width="1"/></pattern>')

# Cyan ramp, matched to the profile palette.
RAMP = ["#0d1526", "#0f4a57", "#15829a", "#22d3ee", "#8ceef9"]

LANG_COLOR = {
    "JavaScript": "#f0db4f", "Java": "#f89820", "Python": "#4b8bbe",
    "CSS": "#663399", "HTML": "#e34c26", "Dockerfile": "#2496ed",
    "Procfile": "#6b7a99", "Shell": "#89e051", "TypeScript": "#3178c6",
}


def get(url, raw=False):
    req = urllib.request.Request(url, headers={
        "User-Agent": "profile-readme-generator",
        "Accept": "text/html" if raw else "application/vnd.github+json",
    })
    tok = os.environ.get("GITHUB_TOKEN")
    if tok and not raw:
        req.add_header("Authorization", "Bearer " + tok)
    with urllib.request.urlopen(req, timeout=45) as r:
        data = r.read().decode("utf-8", "replace")
    return data if raw else json.loads(data)


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def head(title, right, w=900):
    return ('<text x="26" y="34" font-family="%s" font-size="10" letter-spacing="2.6" fill="#3f4c68">// %s</text>'
            '<text x="%d" y="34" text-anchor="end" font-family="%s" font-size="10" letter-spacing="2" fill="#3f4c68">%s</text>'
            '<line x1="26" y1="46" x2="%d" y2="46" stroke="#141d31"/>'
            % (MONO, title, w - 26, MONO, right, w - 26))


# --------------------------------------------------------------- collect
user = get("https://api.github.com/users/%s" % USER)
repos = [r for r in get("https://api.github.com/users/%s/repos?per_page=100" % USER)
         if not r["fork"]]

langs = {}
for r in repos:
    for k, v in get(r["languages_url"]).items():
        langs[k] = langs.get(k, 0) + v

html = get("https://github.com/users/%s/contributions" % USER, raw=True)
days = {}
for tip in re.findall(r"<tool-tip[^>]*>([^<]+)</tool-tip>", html):
    m = re.match(r"(No|[\d,]+) contribution[s]? on (.+?)\.?$", tip.strip())
    if m:
        days[m.group(2)] = 0 if m.group(1) == "No" else int(m.group(1).replace(",", ""))

dated = dict(re.findall(r'data-date="(\d{4}-\d\d-\d\d)"[^>]*data-level="(\d)"', html))
if not dated:
    dated = {d: l for l, d in re.findall(r'data-level="(\d)"[^>]*data-date="(\d{4}-\d\d-\d\d)"', html)}

created = dt.datetime.strptime(user["created_at"], "%Y-%m-%dT%H:%M:%SZ").date()
today = dt.date.today()

# Contribution calendar covers a rolling year; clip it to the account's lifetime
# so the panel shows real history rather than months that pre-date the account.
start = max(created, today - dt.timedelta(days=364))
cal = {d: int(l) for d, l in dated.items()
       if start <= dt.date.fromisoformat(d) <= today}

total = sum(v for k, v in days.items())
active = sum(1 for v in cal.values() if v > 0)
tracked = (today - start).days + 1


# --------------------------------------------------------------- stats.svg
kpis = [
    ("REPOSITORIES", str(user["public_repos"]), "public", "#22d3ee"),
    ("CONTRIBUTIONS", str(total), "last 12 months", "#8b5cf6"),
    ("ACTIVE DAYS", str(active), "of %d tracked" % tracked, "#2dd4bf"),
    ("LANGUAGES", str(len(langs)), "across repos", "#f59e0b"),
]
tiles = []
for i, (label, val, sub, c) in enumerate(kpis):
    x = 26 + i * 216
    tiles.append(
        '<g><rect x="%d" y="66" width="196" height="94" rx="12" fill="#080d1a" stroke="%s" stroke-opacity=".38"/>'
        '<rect x="%d" y="66" width="196" height="2" rx="1" fill="%s" opacity=".8"/>'
        '<text x="%d" y="90" font-family="%s" font-size="8.6" letter-spacing="1.6" fill="#5d6b87">%s</text>'
        '<text x="%d" y="130" font-family="%s" font-size="34" font-weight="700" fill="%s">%s</text>'
        '<text x="%d" y="149" font-family="%s" font-size="8" fill="#4d5b78">%s</text></g>'
        % (x, c, x, c, x + 16, MONO, label, x + 16, SANS, c, val, x + 16, MONO, sub))

tot_b = sum(langs.values()) or 1
ordered = sorted(langs.items(), key=lambda kv: -kv[1])
bar, legend, cx = [], [], 26.0
BAR_W = 848.0
for i, (name, b) in enumerate(ordered):
    w = BAR_W * b / tot_b
    col = LANG_COLOR.get(name, "#6b7a99")
    bar.append('<rect x="%.1f" y="206" width="%.1f" height="14" fill="%s"/>' % (cx, max(w, 1.2), col))
    cx += w
for i, (name, b) in enumerate(ordered):
    pct = 100.0 * b / tot_b
    col = LANG_COLOR.get(name, "#6b7a99")
    lx = 26 + (i % 4) * 216
    ly = 250 + (i // 4) * 22
    legend.append(
        '<g><rect x="%d" y="%d" width="9" height="9" rx="2.5" fill="%s"/>'
        '<text x="%d" y="%d" font-family="%s" font-size="8.8" fill="#c8d6ee">%s</text>'
        '<text x="%d" y="%d" font-family="%s" font-size="8.8" fill="#5d6b87">%.1f%%</text></g>'
        % (lx, ly - 8, col, lx + 15, ly, MONO, esc(name), lx + 150, ly, MONO, pct))

h = 300 + (len(ordered) // 5) * 22
svg = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="900" height="%d" viewBox="0 0 900 %d" role="img" '
    'aria-label="GitHub statistics for %s: %s public repositories, %s contributions in the last 12 months, '
    '%s active days, %d languages.">'
    '<defs>%s</defs>'
    '<rect width="900" height="%d" rx="14" fill="#05070e"/><rect width="900" height="%d" rx="14" fill="url(#gg)"/>'
    '%s%s'
    '<text x="26" y="192" font-family="%s" font-size="9" letter-spacing="2" fill="#5d6b87">LANGUAGE DISTRIBUTION</text>'
    '<text x="874" y="192" text-anchor="end" font-family="%s" font-size="8.4" fill="#3f4c68">BY BYTES IN PUBLIC REPOS</text>'
    '<clipPath id="barclip"><rect x="26" y="206" width="848" height="14" rx="7"/></clipPath>'
    '<g clip-path="url(#barclip)">%s</g>'
    '<rect x="26" y="206" width="848" height="14" rx="7" fill="none" stroke="#1b2740"/>'
    '%s'
    '<text x="26" y="%d" font-family="%s" font-size="8" letter-spacing="1.3" fill="#3a4763">'
    'GENERATED FROM THE GITHUB API / ACCOUNT OPENED %s</text>'
    '<text x="874" y="%d" text-anchor="end" font-family="%s" font-size="8" letter-spacing="1.3" fill="#3a4763">'
    'UPDATED %s</text>'
    '</svg>'
    % (h, h, USER, user["public_repos"], total, active, len(langs), GRID, h, h,
       head("GITHUB COMMAND CENTER", "LIVE TELEMETRY"), "".join(tiles), MONO, MONO,
       "".join(bar), "".join(legend),
       h - 16, MONO, created.strftime("%d %b %Y").upper(),
       h - 16, MONO, today.strftime("%d %b %Y").upper())
)
open(os.path.join(OUT, "stats.svg"), "w", encoding="utf-8").write(svg)
print("stats.svg", len(svg))


# ------------------------------------------------------------ activity.svg
CELL, GAP = 20, 5
STEP = CELL + GAP

# Column 0 starts on the Sunday on or before `start`.
first_sun = start - dt.timedelta(days=(start.weekday() + 1) % 7)
weeks = (today - first_sun).days // 7 + 1
gw = weeks * STEP - GAP
ox = (900 - gw) / 2.0
oy = 96

cells, months, seen = [], [], set()
for w in range(weeks):
    for d in range(7):
        day = first_sun + dt.timedelta(days=w * 7 + d)
        if day < start or day > today:
            continue
        iso = day.isoformat()
        lvl = cal.get(iso, 0)
        x = ox + w * STEP
        y = oy + d * STEP
        fill = RAMP[min(lvl, 4)]
        stroke = ' stroke="%s" stroke-opacity=".55"' % RAMP[4] if lvl >= 3 else ''
        cells.append('<rect x="%.1f" y="%d" width="%d" height="%d" rx="4" fill="%s"%s/>'
                     % (x, y, CELL, CELL, fill, stroke))
    m = (first_sun + dt.timedelta(days=w * 7)).strftime("%b")
    if m not in seen and w < weeks - 1:
        seen.add(m)
        months.append('<text x="%.1f" y="%d" font-family="%s" font-size="8.6" fill="#5d6b87">%s</text>'
                      % (ox + w * STEP, oy - 10, MONO, m.upper()))

for i, lbl in ((1, "MON"), (3, "WED"), (5, "FRI")):
    months.append('<text x="%.1f" y="%.1f" text-anchor="end" font-family="%s" font-size="7.6" fill="#3f4c68">%s</text>'
                  % (ox - 10, oy + i * STEP + CELL * 0.72, MONO, lbl))

key = []
for i, c in enumerate(RAMP):
    key.append('<rect x="%d" y="%d" width="11" height="11" rx="3" fill="%s"/>' % (700 + i * 16, oy + 7 * STEP + 16, c))

ah = oy + 7 * STEP + 74
svg = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="900" height="%d" viewBox="0 0 900 %d" role="img" '
    'aria-label="Activity matrix: %s contributions across %s active days since the account opened.">'
    '<defs>%s'
    '<linearGradient id="scan" x1="0" y1="0" x2="1" y2="0">'
    '<stop offset="0%%" stop-color="#22d3ee" stop-opacity="0"/><stop offset="50%%" stop-color="#22d3ee" stop-opacity=".55"/>'
    '<stop offset="100%%" stop-color="#22d3ee" stop-opacity="0"/></linearGradient></defs>'
    '<rect width="900" height="%d" rx="14" fill="#05070e"/><rect width="900" height="%d" rx="14" fill="url(#gg)"/>'
    '%s'
    '<g stroke="#22d3ee" stroke-width="1.5" fill="none" opacity=".55">'
    '<path d="M18 84V62h26"/><path d="M882 84V62h-26"/><path d="M18 %dv22h26"/><path d="M882 %dv22h-26"/></g>'
    '%s%s'
    '<rect x="26" y="%d" width="848" height="1.4" fill="url(#scan)">'
    '<animate attributeName="y" values="%d;%d;%d" dur="7s" repeatCount="indefinite"/>'
    '<animate attributeName="opacity" values=".2;.9;.2" dur="7s" repeatCount="indefinite"/></rect>'
    '<text x="26" y="%d" font-family="%s" font-size="8.8" fill="#8091ae">%s CONTRIBUTIONS / %s ACTIVE DAYS / SINCE %s</text>'
    '<text x="686" y="%d" text-anchor="end" font-family="%s" font-size="8" fill="#3f4c68">LESS</text>'
    '%s'
    '<text x="%d" y="%d" font-family="%s" font-size="8" fill="#3f4c68">MORE</text>'
    '</svg>'
    % (ah, ah, total, active, GRID, ah, ah,
       head("ACTIVITY MATRIX", "CONTRIBUTION TELEMETRY"),
       ah - 40, ah - 40,
       "".join(months), "".join(cells),
       oy, oy, oy + 7 * STEP - 6, oy,
       oy + 7 * STEP + 26, MONO, total, active, start.strftime("%d %b %Y").upper(),
       oy + 7 * STEP + 25, MONO,
       "".join(key),
       700 + 5 * 16 + 4, oy + 7 * STEP + 25, MONO)
)
open(os.path.join(OUT, "activity.svg"), "w", encoding="utf-8").write(svg)
print("activity.svg", len(svg), "| weeks", weeks, "| total", total, "| active", active)
