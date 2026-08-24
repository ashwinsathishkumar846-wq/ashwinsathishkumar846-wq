#!/usr/bin/env python3
"""Generate the data-driven profile assets from the GitHub REST API.

Pipeline:  fetch -> validate -> render -> write

Every figure rendered by this script is read from the GitHub REST API or parsed
out of a repository's own README. Nothing is estimated or hard-coded. The
contribution calendar is deliberately NOT used: it is only available by scraping
an undocumented HTML endpoint, so this builds its activity view from commit data
instead, which the REST API serves reliably.

If GitHub is unavailable or returns something implausible, the script exits
non-zero and leaves the existing assets untouched rather than writing a
half-empty dashboard over good ones.

Run:  python scripts/generate_profile.py
Env:  GITHUB_TOKEN (optional) - raises the rate limit; no private data is read.
"""

import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import (PANEL, PANEL_2, HAIR, STROKE, TEXT, MUTED, DIM, FAINT,
                   CYAN, VIOLET, INDIGO, TEAL, AMBER, MONO, SANS,
                   esc, head, panel, label, pulse, svg, write)

USER = "ashwinsathishkumar846-wq"
OUT = "assets"
API = "https://api.github.com"

# Editorial one-liners. GitHub descriptions are empty on these repos, so the
# summaries live here - reviewed by a human, not invented per run. A repo that
# gains a real GitHub description will use that instead (see summarise()).
BLURBS = {
    "dji-dronic-world": ("Drone service-centre platform: parts catalog with search and",
                         "filtering, booking flow, delivery tracking, JWT admin dashboard"),
    "LeetCode-Solution": ("Accepted Java solutions organised by topic, exported",
                          "directly from the LeetCode account"),
    "webassignment": ("Frontend Mentor bento-grid challenge, built with",
                      "CSS Grid placement and responsive breakpoints"),
}
STACKS = {
    "dji-dronic-world": ["React", "Vite", "Tailwind", "Express", "SQLite", "JWT", "Docker"],
    "LeetCode-Solution": ["Java", "Python", "JavaScript"],
    "webassignment": ["HTML", "CSS"],
}
LANG_COLOR = {"JavaScript": "#f0db4f", "Java": "#f89820", "Python": "#4b8bbe",
              "CSS": "#663399", "HTML": "#e34c26", "Dockerfile": "#2496ed",
              "Procfile": "#6b7a99", "Shell": "#89e051", "TypeScript": "#3178c6"}


# ------------------------------------------------------------------- fetch
def api(path, raw=False, retries=3):
    url = path if path.startswith("http") else API + path
    hdrs = {"User-Agent": "ashwin-profile-generator",
            "Accept": "application/vnd.github+json"}
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        hdrs["Authorization"] = "Bearer " + tok
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=hdrs)
            with urllib.request.urlopen(req, timeout=45) as r:
                body = r.read().decode("utf-8", "replace")
            return body if raw else json.loads(body)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise
            last = e
        except Exception as e:                                    # noqa: BLE001
            last = e
        if attempt < retries - 1:
            time.sleep(2 * (attempt + 1))
    raise RuntimeError("GitHub request failed after %d attempts: %s (%s)" % (retries, url, last))


def fetch():
    """Pull everything the renderers need, in one place."""
    user = api("/users/%s" % USER)
    repos = [r for r in api("/users/%s/repos?per_page=100&sort=pushed" % USER) if not r["fork"]]

    langs, commits = {}, []
    for r in repos:
        if r["size"] == 0:                       # empty repo: no languages, no commits
            continue
        for k, v in api(r["languages_url"]).items():
            langs[k] = langs.get(k, 0) + v
        try:
            for c in api("/repos/%s/%s/commits?per_page=100" % (USER, r["name"])):
                commits.append((r["name"], c["commit"]["author"]["date"][:10]))
        except urllib.error.HTTPError:
            pass                                  # unborn default branch - skip quietly

    # LeetCode counts are stated in that repo's own README; parse rather than assume.
    solved = files = None
    try:
        md = api("https://raw.githubusercontent.com/%s/LeetCode-Solution/main/README.md" % USER, raw=True)
        m = re.search(r"\*\*(\d+)\s+Java solutions\*\*", md)
        files = int(m.group(1)) if m else None
        m = re.search(r"out of \*\*(\d+)\s+problems solved\*\*", md)
        solved = int(m.group(1)) if m else None
    except Exception as e:                                        # noqa: BLE001
        print("  ! LeetCode README unreadable (%s) - counts omitted" % e)

    return {"user": user, "repos": repos, "langs": langs, "commits": commits,
            "leetcode": {"files": files, "solved": solved},
            "generated": dt.date.today()}


# ---------------------------------------------------------------- validate
def validate(d):
    """Refuse to render from a response that is missing or obviously wrong."""
    u, repos = d["user"], d["repos"]
    problems = []
    if not u.get("login"):
        problems.append("user payload has no login")
    if u.get("public_repos") is None:
        problems.append("public_repos missing")
    if not repos:
        problems.append("no repositories returned")
    if not d["langs"]:
        problems.append("no languages resolved across repos")
    if not d["commits"]:
        problems.append("no commits resolved across repos")
    created = u.get("created_at")
    if not created:
        problems.append("created_at missing")
    elif dt.datetime.strptime(created, "%Y-%m-%dT%H:%M:%SZ").date() > dt.date.today():
        problems.append("created_at is in the future")
    if problems:
        raise ValueError("validation failed: " + "; ".join(problems))
    print("  validated: %d repos, %d languages, %d commits"
          % (len(repos), len(d["langs"]), len(d["commits"])))


def summarise(repo):
    """Prefer a real GitHub description; fall back to the reviewed blurb."""
    desc = (repo.get("description") or "").strip()
    if desc:
        words, lines, cur = desc.split(), [], ""
        for w in words:
            if len(cur) + len(w) + 1 > 62:
                lines.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
        return (lines + ["", ""])[:2]
    return BLURBS.get(repo["name"], ("", ""))


# ------------------------------------------------------- constellation.svg
def render_constellation(d):
    by_name = {r["name"]: r for r in d["repos"]}
    live = [r for r in d["repos"] if r["size"] > 0 and r["name"] != USER]
    empty = [r for r in d["repos"] if r["size"] == 0]
    lc = d["leetcode"]

    primary = by_name.get("dji-dronic-world")
    others = [r for r in live if r is not primary]
    # Substance first, byte-size second: a solutions repo outranks a CSS exercise.
    rank = {"LeetCode-Solution": 0, "webassignment": 1}
    others.sort(key=lambda r: (rank.get(r["name"], 9), -r["size"]))

    parts = []

    # ---- primary node
    if primary:
        px, py, pw, ph = 210, 70, 480, 162
        parts.append('<ellipse cx="450" cy="150" rx="330" ry="130" fill="url(#pri)"/>')
        parts.append('<rect x="%d" y="%d" width="%d" height="%d" rx="15" fill="%s" filter="url(#bloom)" '
                     'opacity=".85"/>' % (px, py, pw, ph, PANEL))
        parts.append('<rect x="%d" y="%d" width="%d" height="%d" rx="15" fill="%s" stroke="url(#rim)" '
                     'stroke-opacity=".75" stroke-width="1.3"/>' % (px, py, pw, ph, PANEL_2))
        parts.append('<rect x="%d" y="%.1f" width="150" height="2" fill="url(#rim)"/>' % (px + 40, py - 1))
        parts.append(label(px + 24, py + 26, "PRIMARY", 8, FAINT, MONO, None, None, "2.2"))
        badge = "LIVE" if primary.get("homepage") else "ACTIVE"
        bw = len(badge) * 6.4 + 20
        parts.append('<rect x="%.1f" y="%d" width="%.1f" height="19" rx="9.5" fill="%s" fill-opacity=".14" '
                     'stroke="%s" stroke-opacity=".55"/>' % (px + pw - 24 - bw, py + 14, bw, TEAL, TEAL))
        parts.append(label(px + pw - 24 - bw / 2, py + 27, badge, 7.8, TEAL, MONO, "middle", None, "1.2"))
        parts.append(label(px + 24, py + 58, primary["name"], 20, TEXT, SANS, None, "700", "1"))
        l1, l2 = summarise(primary)
        parts.append(label(px + 24, py + 82, l1, 9, MUTED))
        parts.append(label(px + 24, py + 96, l2, 9, MUTED))
        cx = px + 24
        for t in STACKS.get(primary["name"], []):
            bw2 = len(t) * 6.1 + 20
            parts.append('<rect x="%.1f" y="%d" width="%.1f" height="20" rx="10" fill="%s" fill-opacity=".10" '
                         'stroke="%s" stroke-opacity=".4"/>' % (cx, py + 110, bw2, CYAN, CYAN))
            parts.append(label(cx + bw2 / 2, py + 124, t, 8.2, "#cfe0f5", MONO, "middle"))
            cx += bw2 + 6
        parts.append(label(px + 24, py + 150, "github.com/%s/%s" % (USER, primary["name"]), 8, FAINT))
        if primary.get("homepage"):
            parts.append(label(px + pw - 24, py + 150, primary["homepage"].replace("https://", "") + "  ↗",
                               8, TEAL, MONO, "end"))
        parts.append(pulse(450, py - 2, 4.5, CYAN, 3.4))

    # ---- secondary nodes
    SY, SW, SH = 262, 414, 132
    for i, r in enumerate(others[:2]):
        x = 26 + i * (SW + 20)
        col = TEAL if i == 0 else INDIGO
        parts.append('<path d="M450 %d C450 %d %.1f %d %.1f %d" fill="none" stroke="%s" stroke-opacity=".28" '
                     'stroke-width="1.2"/>' % (232, 250, x + SW / 2, 244, x + SW / 2, SY, col))
        parts.append(panel(x, SY, SW, SH, col, PANEL, 13))
        parts.append(label(x + 20, SY + 26, "0%d" % (i + 2), 8, FAINT))
        pushed = r["pushed_at"][:7]
        parts.append(label(x + SW - 20, SY + 26, pushed, 8, FAINT, MONO, "end"))
        parts.append(label(x + 20, SY + 52, r["name"], 14.5, TEXT, SANS, None, "700", "0.8"))
        l1, l2 = summarise(r)
        parts.append(label(x + 20, SY + 73, l1, 8.6, MUTED))
        parts.append(label(x + 20, SY + 86, l2, 8.6, MUTED))
        if r["name"] == "LeetCode-Solution" and lc["files"] and lc["solved"]:
            parts.append(label(x + 20, SY + 105, "%d solution files  /  %d problems solved"
                               % (lc["files"], lc["solved"]), 8.4, col))
        elif r["name"] == "webassignment" and r.get("has_pages"):
            parts.append(label(x + 20, SY + 105, "published via GitHub Pages", 8.4, col))
        else:
            parts.append(label(x + 20, SY + 105, " / ".join(STACKS.get(r["name"], [])), 8.4, col))
        parts.append(label(x + 20, SY + 121, "github.com/%s/%s" % (USER, r["name"]), 7.8, FAINT))
        parts.append(pulse(x + SW / 2, SY - 2, 3.6, col, 3.0 + i * .6))

    # ---- experiments strip (empty repos, deliberately quiet)
    EY = SY + SH + 26
    if empty:
        parts.append('<line x1="26" y1="%d" x2="874" y2="%d" stroke="%s"/>' % (EY, EY, HAIR))
        parts.append(label(26, EY + 22, "EXPERIMENTS", 8.4, FAINT, MONO, None, None, "2"))
        cx = 150
        for r in empty:
            bw = len(r["name"]) * 6.2 + 26
            parts.append('<rect x="%.1f" y="%d" width="%.1f" height="20" rx="10" fill="none" stroke="%s" '
                         'stroke-opacity=".35" stroke-dasharray="3 3"/>' % (cx, EY + 8, bw, STROKE))
            parts.append(label(cx + bw / 2, EY + 22, r["name"], 8, "#66748f", MONO, "middle"))
            cx += bw + 8
        parts.append(label(874, EY + 22, "initialised, no content yet", 7.8, FAINT, MONO, "end"))

    h = EY + 48
    extra = ('<radialGradient id="pri" cx="50%" cy="50%" r="50%">'
             '<stop offset="0%" stop-color="#1d4ed8" stop-opacity=".26"/>'
             '<stop offset="100%" stop-color="#060910" stop-opacity="0"/></radialGradient>')
    body = head("PROJECT CONSTELLATION", "%d REPOSITORIES ON GITHUB" % len(d["repos"])) + "".join(parts)
    write(os.path.join(OUT, "constellation.svg"),
          svg("constellation", h, body,
              "Project constellation of the verified GitHub repositories, with dji-dronic-world as the "
              "primary project.", extra_defs=(extra,)))


# ------------------------------------------------------------ build-log.svg
def render_build_log(d):
    u = d["user"]
    created = dt.datetime.strptime(u["created_at"], "%Y-%m-%dT%H:%M:%SZ").date()
    today = d["generated"]
    # Whole months elapsed, plus the leftover days - rounded to the nearest month
    # for the headline so "4 months 29 days" does not read as 4.
    whole = (today.year - created.year) * 12 + (today.month - created.month)
    if today.day < created.day:
        whole -= 1
    whole = max(whole, 0)
    anchor = created
    for _ in range(whole):                       # walk forward `whole` months
        y, m = anchor.year + (anchor.month == 12), anchor.month % 12 + 1
        day = min(anchor.day, [31, 29 if y % 4 == 0 and (y % 100 or y % 400 == 0) else 28,
                               31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])
        anchor = dt.date(y, m, day)
    extra_days = (today - anchor).days
    months = whole + (1 if extra_days >= 15 else 0)

    days = sorted({c[1] for c in d["commits"]})
    stars = sum(r["stargazers_count"] for r in d["repos"])

    stats = [("REPOSITORIES", u["public_repos"]),
             ("COMMITS", len(d["commits"])),
             ("ACTIVE DAYS", len(days)),
             ("LANGUAGES", len(d["langs"])),
             ("FOLLOWERS", u["followers"]),
             ("STARS", stars)]

    parts = []

    # ---- the framing, given the most visual weight
    parts.append(panel(26, 62, 300, 202, CYAN, PANEL, 13))
    parts.append(label(46, 88, "ACCOUNT AGE", 8.6, FAINT, MONO, None, None, "2.2"))
    parts.append('<text x="46" y="152" font-family="%s" font-size="58" font-weight="700" fill="url(#ink)">'
                 '%02d</text>' % (SANS, months))
    parts.append(label(150, 152, "MONTHS", 15, DIM, MONO, None, "700", "2"))
    parts.append('<line x1="46" y1="172" x2="306" y2="172" stroke="%s"/>' % HAIR)
    parts.append(label(46, 192, "opened         %s  (%dm %dd)"
                       % (created.strftime("%d %b %Y"), whole, extra_days), 8.2, MUTED))
    parts.append(label(46, 208, "first commit   %s" % (days[0] if days else "-"), 8.2, MUTED))
    parts.append(label(46, 224, "latest commit  %s" % (days[-1] if days else "-"), 8.2, MUTED))
    parts.append('<rect x="46" y="236" width="150" height="20" rx="10" fill="%s" fill-opacity=".14" '
                 'stroke="%s" stroke-opacity=".55"/>' % (TEAL, TEAL))
    parts.append('<circle cx="60" cy="246" r="3.5" fill="%s">'
                 '<animate attributeName="opacity" values="1;.25;1" dur="2.6s" repeatCount="indefinite"/>'
                 '</circle>' % TEAL)
    parts.append(label(72, 250, "EARLY STAGE / BUILDING", 7.6, TEAL, MONO, None, None, "1.1"))

    # ---- the numbers, deliberately smaller than the framing
    for i, (name, val) in enumerate(stats):
        x = 346 + (i % 3) * 178
        y = 62 + (i // 3) * 96
        parts.append('<rect x="%d" y="%d" width="164" height="82" rx="11" fill="%s" stroke="%s" '
                     'stroke-opacity=".38"/>' % (x, y, PANEL, STROKE))
        parts.append(label(x + 16, y + 26, name, 7.8, FAINT, MONO, None, None, "1.6"))
        parts.append('<text x="%d" y="%d" font-family="%s" font-size="27" font-weight="700" fill="%s">%02d</text>'
                     % (x + 16, y + 62, SANS, TEXT if val else DIM, val))

    # ---- commit timeline, from real commit dates
    TY = 292
    parts.append('<line x1="26" y1="%d" x2="874" y2="%d" stroke="%s"/>' % (TY - 22, TY - 22, HAIR))
    parts.append(label(26, TY - 4, "BUILD LOG", 8.6, FAINT, MONO, None, None, "2.2"))
    parts.append(label(874, TY - 4, "EVERY COMMIT DAY IN THIS ACCOUNT", 7.8, FAINT, MONO, "end"))
    if days:
        first = dt.date.fromisoformat(days[0])
        span = max((today - first).days, 1)
        AXIS = TY + 46
        parts.append('<line x1="60" y1="%d" x2="840" y2="%d" stroke="%s" stroke-width="1.4"/>' % (AXIS, AXIS, STROKE))
        counts = {}
        for _, day in d["commits"]:
            counts[day] = counts.get(day, 0) + 1
        for day, n in sorted(counts.items()):
            dx = 60 + 780.0 * (dt.date.fromisoformat(day) - first).days / span
            hgt = 8 + min(n, 8) * 4.0
            parts.append('<rect x="%.1f" y="%.1f" width="7" height="%.1f" rx="3.5" fill="%s" opacity=".9"/>'
                         % (dx - 3.5, AXIS - hgt, hgt, CYAN))
            parts.append(label(dx, AXIS - hgt - 6, str(n), 7.4, CYAN, MONO, "middle"))
        parts.append(label(60, AXIS + 18, first.strftime("%d %b %Y").upper(), 7.6, DIM))
        parts.append(label(840, AXIS + 18, today.strftime("%d %b %Y").upper(), 7.6, DIM, MONO, "end"))

    # ---- language split
    LY = TY + 96
    total = sum(d["langs"].values()) or 1
    ordered = sorted(d["langs"].items(), key=lambda kv: -kv[1])
    parts.append(label(26, LY, "LANGUAGE DISTRIBUTION", 8.6, FAINT, MONO, None, None, "2"))
    parts.append(label(874, LY, "BY BYTES IN PUBLIC REPOSITORIES", 7.8, FAINT, MONO, "end"))
    cx = 26.0
    bars = []
    for name, b in ordered:
        bw = 848.0 * b / total
        bars.append('<rect x="%.1f" y="%d" width="%.1f" height="13" fill="%s"/>'
                    % (cx, LY + 12, max(bw, 1.2), LANG_COLOR.get(name, "#6b7a99")))
        cx += bw
    parts.append('<clipPath id="bc"><rect x="26" y="%d" width="848" height="13" rx="6.5"/></clipPath>' % (LY + 12))
    parts.append('<g clip-path="url(#bc)">%s</g>' % "".join(bars))
    for i, (name, b) in enumerate(ordered):
        lx = 26 + (i % 4) * 214
        ly = LY + 50 + (i // 4) * 20
        parts.append('<rect x="%d" y="%d" width="9" height="9" rx="2.5" fill="%s"/>'
                     % (lx, ly - 8, LANG_COLOR.get(name, "#6b7a99")))
        parts.append(label(lx + 15, ly, name, 8.6, "#c8d6ee"))
        parts.append(label(lx + 148, ly, "%.1f%%" % (100.0 * b / total), 8.6, DIM))

    h = LY + 50 + ((len(ordered) - 1) // 4) * 20 + 42
    parts.append(label(26, h - 16, "GENERATED FROM THE GITHUB REST API ON %s / NO THIRD-PARTY SERVICE"
                       % today.strftime("%d %b %Y").upper(), 7.8, FAINT, MONO, None, None, "1.2"))
    body = head("BUILD LOG", "YOUNG ACCOUNT, ACTIVE BUILDER") + "".join(parts)
    write(os.path.join(OUT, "build-log.svg"),
          svg("build-log", h, body,
              "Build log: account age %d months, %d repositories, %d commits across %d active days."
              % (months, u["public_repos"], len(d["commits"]), len(days))))


def main():
    os.makedirs(OUT, exist_ok=True)
    try:
        print("fetching GitHub data...")
        data = fetch()
        validate(data)
    except Exception as e:                                        # noqa: BLE001
        print("ERROR: %s" % e, file=sys.stderr)
        print("existing assets left untouched.", file=sys.stderr)
        return 1
    print("rendering:")
    render_constellation(data)
    render_build_log(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
