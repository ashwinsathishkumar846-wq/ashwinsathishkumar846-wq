#!/usr/bin/env python3
"""Generate the live, data-driven panels of the profile.

Pipeline:  fetch -> validate -> render -> write

  assets/github-command-center.svg   (+ assets/m/...)   GITHUB // SYSTEM STATUS
  assets/shipped-repos.svg           (+ assets/m/...)   code that is public on GitHub

Every number is read at run time; nothing is estimated or hard-coded:
  - profile, repositories, languages, authored commits   GitHub REST API
  - contribution calendar                                 GitHub GraphQL API (needs a token;
                                                           the Actions GITHUB_TOKEN works). Without a
                                                           token - e.g. a local run - it falls back to
                                                           the public calendar page and says so.
  - LeetCode solved count                                 LeetCode's public GraphQL endpoint, falling
                                                           back to the count stated in the
                                                           LeetCode-Solution README
A figure that cannot be read is shown as a dash, never guessed. If the core
GitHub data is missing or implausible the script exits non-zero and leaves the
existing panels untouched rather than writing an empty dashboard over good ones.

Run:  python scripts/generate_profile.py
Env:  GITHUB_TOKEN (optional locally, provided in Actions)
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
from theme import (PANEL, PANEL_2, LINE, LINE_2, TEXT, MUTED, DIM, FAINT, RED, CYAN, BLUE,  # noqa: E402
                   VIOLET, TEAL, GOLD, SANS, MONO, WIDE, NARROW,
                   t, lines, chip, chips, panel, node, header, svg, write, wrap, text_w, esc)

USER = "ashwinsathishkumar846-wq"
OUT = "assets"
API = "https://api.github.com"
UA = {"User-Agent": "ashwin-profile-generator"}

# Editorial one-liners, reviewed by hand against each repository's own README.
# A repo that gains a real GitHub description uses that instead (see summary()).
BLURBS = {
    "dji-dronic-world": "Full-stack drone service-centre platform: parts catalog, booking flow, delivery "
                        "tracking and a JWT admin dashboard, on a hardened Express API.",
    "dsa-placement-tracker": "12-week, 141-problem DSA preparation tracker with progress, streaks, filters "
                             "and a daily target. No backend: state lives in localStorage.",
    "ashwin-portfolio": "Cinematic personal portfolio: a Three.js scene, GSAP scroll choreography and "
                        "a Next.js app router build.",
    "LeetCode-Solution": "Accepted LeetCode solutions in Java, organised by topic and synced from the "
                         "account with LeetHub.",
    "webassignment": "Frontend Mentor bento-grid challenge, built with CSS Grid placement and "
                     "responsive breakpoints.",
}
STACKS = {
    "dji-dronic-world": ["React", "Vite", "Tailwind", "Express", "SQLite", "JWT", "Docker"],
    "dsa-placement-tracker": ["React", "TypeScript", "Vite", "Tailwind"],
    "ashwin-portfolio": ["Next.js", "TypeScript", "Three.js", "GSAP", "Tailwind"],
    "LeetCode-Solution": ["Java", "LeetHub"],
    "webassignment": ["HTML", "CSS Grid"],
}
ORDER = ["dji-dronic-world", "dsa-placement-tracker", "ashwin-portfolio", "LeetCode-Solution", "webassignment"]
LANG_COLOR = {"JavaScript": "#f1e05a", "TypeScript": "#3178c6", "Java": "#b07219", "Python": "#3572A5",
              "CSS": "#663399", "HTML": "#e34c26", "Dockerfile": "#384d54", "Procfile": "#6b7a99",
              "Shell": "#89e051"}


# ------------------------------------------------------------------- fetch
def request(url, data=None, headers=None, retries=3):
    """Returns (body, response headers). Raises on 404 immediately, retries the rest."""
    hdrs = dict(UA)
    hdrs.update(headers or {})
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=data, headers=hdrs)
            with urllib.request.urlopen(req, timeout=45) as r:
                return r.read().decode("utf-8", "replace"), r.headers
        except urllib.error.HTTPError as e:
            if e.code in (401, 403, 404):
                raise
            last = e
        except Exception as e:                                        # noqa: BLE001
            last = e
        if attempt < retries - 1:
            time.sleep(2 * (attempt + 1))
    raise RuntimeError("request failed after %d attempts: %s (%s)" % (retries, url, last))


def gh(path, raw=False):
    hdrs = {"Accept": "application/vnd.github+json"}
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        hdrs["Authorization"] = "Bearer " + tok
    body, h = request(path if path.startswith("http") else API + path, headers=hdrs)
    return (body, h) if raw else json.loads(body)


def human_commits(repo):
    """Commits on the default branch, excluding bots (the profile repo's own
    refresh commits, Actions, Dependabot). Counted by listing rather than by
    ?author=, because commits made from an email not linked to the account have
    no GitHub author and would silently be dropped."""
    n, page = 0, 1
    while True:
        try:
            batch = gh("/repos/%s/%s/commits?per_page=100&page=%d" % (USER, repo, page))
        except urllib.error.HTTPError:
            return n                                   # empty repository
        for c in batch:
            login = ((c.get("author") or {}).get("login") or "")
            name = c["commit"]["author"]["name"] or ""
            if not (login.endswith("[bot]") or name.endswith("[bot]")):
                n += 1
        if len(batch) < 100:
            return n
        page += 1


def calendar():
    """Contribution calendar for the last year: (total, [(date, count), ...], source)."""
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        q = ("query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{"
             "totalContributions weeks{contributionDays{date contributionCount}}}}}}")
        body, _ = request(API + "/graphql", json.dumps({"query": q, "variables": {"login": USER}}).encode(),
                          {"Authorization": "Bearer " + tok, "Content-Type": "application/json"})
        cal = json.loads(body)["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        days = [(d["date"], d["contributionCount"]) for w in cal["weeks"] for d in w["contributionDays"]]
        return cal["totalContributions"], days, "GRAPHQL"
    # Local fallback: the public calendar page. Undocumented markup, so every
    # parse is cross-checked against the page's own headline total.
    html, _ = request("https://github.com/users/%s/contributions" % USER)
    ids = dict(re.findall(r'data-date="(\d{4}-\d\d-\d\d)" id="(contribution-day-component-\d+-\d+)"', html))
    ids = {v: k for k, v in ids.items()}
    days = {}
    for comp, txt in re.findall(r'<tool-tip[^>]*for="(contribution-day-component-\d+-\d+)"[^>]*>([^<]+)<', html):
        m = re.match(r"(\d+) contribution", txt)
        if comp in ids:
            days[ids[comp]] = int(m.group(1)) if m else 0
    head = re.search(r"([\d,]+)\s+contributions?\s+in the last year", html)
    total = int(head.group(1).replace(",", "")) if head else None
    if total is None or total != sum(days.values()):
        raise ValueError("public calendar parse did not reconcile with its headline total")
    return total, sorted(days.items()), "PUBLIC CALENDAR"


def leetcode(md_fallback):
    try:
        q = '{ matchedUser(username: "ashwin1122") { submitStatsGlobal { acSubmissionNum { difficulty count } } } }'
        body, _ = request("https://leetcode.com/graphql", json.dumps({"query": q}).encode(),
                          {"Content-Type": "application/json", "Referer": "https://leetcode.com"}, retries=2)
        stats = json.loads(body)["data"]["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"]
        by = {s["difficulty"]: s["count"] for s in stats}
        return {"solved": by["All"], "easy": by["Easy"], "medium": by["Medium"], "hard": by["Hard"],
                "source": "LEETCODE"}
    except Exception as e:                                            # noqa: BLE001
        print("  ! LeetCode API unavailable (%s) - using the repository README" % e)
    m = re.search(r"Total LeetCode problems solved[^|]*\|\s*(\d+)", md_fallback or "")
    return {"solved": int(m.group(1)) if m else None, "source": "REPO README"}


def fetch():
    user = gh("/users/%s" % USER)
    repos = [r for r in gh("/users/%s/repos?per_page=100&sort=pushed" % USER) if not r["fork"]]
    langs, commits = {}, {}
    for r in repos:
        if r["size"] == 0:
            continue
        for k, v in gh(r["languages_url"]).items():
            langs[k] = langs.get(k, 0) + v
        commits[r["name"]] = human_commits(r["name"])

    md = files = None
    try:
        md, _ = gh("https://raw.githubusercontent.com/%s/LeetCode-Solution/main/README.md" % USER, raw=True)
        m = re.search(r"Java solutions in this repo\*\*\s*\|\s*\*\*(\d+)", md)
        files = int(m.group(1)) if m else None
    except Exception as e:                                            # noqa: BLE001
        print("  ! LeetCode-Solution README unreadable (%s)" % e)

    try:
        total, days, cal_src = calendar()
    except Exception as e:                                            # noqa: BLE001
        print("  ! contribution calendar unavailable (%s) - omitted" % e)
        total, days, cal_src = None, [], None

    return {"user": user, "repos": repos, "langs": langs, "commits": commits,
            "cal": {"total": total, "days": days, "source": cal_src},
            "lc": dict(leetcode(md), files=files), "today": dt.datetime.now(dt.timezone.utc).date()}


# ---------------------------------------------------------------- validate
def validate(d):
    u, problems = d["user"], []
    if u.get("login") != USER:
        problems.append("unexpected login")
    if not d["repos"]:
        problems.append("no repositories")
    if not d["langs"]:
        problems.append("no languages")
    if not sum(d["commits"].values()):
        problems.append("no commits")
    if d["cal"]["total"] is not None and d["cal"]["total"] < 0:
        problems.append("negative contribution total")
    if problems:
        raise ValueError("validation failed: " + "; ".join(problems))
    print("  validated: %d repos, %d languages, %d commits (bots excluded), calendar=%s, leetcode=%s"
          % (len(d["repos"]), len(d["langs"]), sum(d["commits"].values()), d["cal"]["source"],
             d["lc"]["source"]))


def fmt(v):
    return "—" if v is None else "{:,}".format(v)


def status_of(d):
    # The profile repo is pushed by its own bot every day, so it cannot count as activity.
    last = max((r for r in d["repos"] if r["name"] != USER), key=lambda r: r["pushed_at"])
    pushed = dt.date.fromisoformat(last["pushed_at"][:10])
    age = (d["today"] - pushed).days
    return ("ACTIVE" if age <= 14 else "IDLE"), pushed, last["name"]


# ------------------------------------------------------ command center.svg
def weekly(days, n=26):
    """Sum the calendar into the last n calendar weeks (Sunday-start, like GitHub)."""
    weeks = {}
    for ds, c in days:
        d = dt.date.fromisoformat(ds)
        start = d - dt.timedelta(days=(d.weekday() + 1) % 7)
        weeks[start] = weeks.get(start, 0) + c
    keys = sorted(weeks)[-n:]
    return [(k, weeks[k]) for k in keys]


def tile(x, y, w, h, label, value, colour, note=""):
    o = panel(x, y, w, h, None)
    o += '<rect x="%.1f" y="%.1f" width="3" height="%.1f" fill="%s" opacity=".8"/>' % (x, y + 14, h - 28, colour)
    o += t(x + 16, y + 24, label, 9.5, DIM, MONO, None, "600", 1.4)
    o += t(x + 16, y + h - 18, value, 26, TEXT if value != "—" else DIM, SANS, None, "700")
    if note:
        o += t(x + w - 12, y + h - 18, note, 9.5, colour, MONO, "end", None, .6)
    return o


def signal(x, y, w, h, wk, colour):
    """Weekly contribution bars from the real calendar."""
    o = ""
    if not wk:
        return t(x, y + h / 2, "calendar unavailable on this run", 10, DIM, MONO)
    peak = max(c for _, c in wk) or 1
    bw = w / float(len(wk))
    o += '<path d="M%.1f %.1fH%.1f" stroke="%s"/>' % (x, y + h, x + w, LINE_2)
    for i, (k, c) in enumerate(wk):
        bh = 2 if c == 0 else max(4, (h - 14) * c / peak)
        o += ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="1.5" fill="%s" opacity="%s"/>'
              % (x + i * bw + 1.5, y + h - bh, bw - 3, bh, colour if c else LINE_2, ".9" if c else "1"))
        if c == peak and c:
            o += t(x + i * bw + bw / 2, y + h - bh - 6, str(c), 9.5, colour, MONO, "middle", "700")
    o += t(x, y + h + 16, wk[0][0].strftime("%d %b").upper(), 9.5, DIM, MONO)
    o += t(x + w, y + h + 16, "THIS WEEK", 9.5, DIM, MONO, "end")
    return o


def lang_bar(x, y, w, langs, cols):
    total = float(sum(langs.values())) or 1
    ordered = sorted(langs.items(), key=lambda kv: -kv[1])
    o = '<clipPath id="lb"><rect x="%.1f" y="%.1f" width="%.1f" height="10" rx="5"/></clipPath><g clip-path="url(#lb)">' % (x, y, w)
    cx = x
    for name, b in ordered:
        bw = w * b / total
        o += '<rect x="%.1f" y="%.1f" width="%.1f" height="10" fill="%s"/>' % (cx, y, max(bw, 1.5), LANG_COLOR.get(name, "#6b7a99"))
        cx += bw
    o += "</g>"
    cw = w / cols
    for i, (name, b) in enumerate(ordered):
        lx, ly = x + (i % cols) * cw, y + 34 + (i // cols) * 20
        o += '<rect x="%.1f" y="%.1f" width="9" height="9" rx="2.5" fill="%s"/>' % (lx, ly - 8.5, LANG_COLOR.get(name, "#6b7a99"))
        o += t(lx + 15, ly, name, 10.5, "#d7dbe3", MONO)
        o += t(lx + cw - 18, ly, "%.1f%%" % (100 * b / total), 10.5, DIM, MONO, "end")
    rows = (len(ordered) + cols - 1) // cols
    return o, y + 34 + (rows - 1) * 20


def render_command_center(d, W):
    u, cal, lc = d["user"], d["cal"], d["lc"]
    state, pushed, last_repo = status_of(d)
    active_days = sum(1 for _, c in cal["days"] if c) if cal["days"] else None
    commits = sum(d["commits"].values())
    wk = weekly(cal["days"])
    created = dt.date.fromisoformat(u["created_at"][:10])
    stc = TEAL if state == "ACTIVE" else GOLD
    tiles = [("REPOSITORIES", fmt(u["public_repos"]), BLUE, "public"),
             ("ACTIVE DAYS", fmt(active_days), CYAN, "12 mo"),
             ("COMMITS", fmt(commits), VIOLET, "no bots"),
             ("LEETCODE SOLVED", fmt(lc["solved"]), GOLD, "live" if lc["source"] == "LEETCODE" else "repo"),
             ("LANGUAGES", fmt(len(d["langs"])), TEAL, "by bytes"),
             ("FOLLOWERS", fmt(u["followers"]), RED, "")]
    b = []
    wide = W == WIDE
    x0 = 28 if wide else 20
    b.append(header(W, "08", "GITHUB · SYSTEM STATUS", "LIVE · REBUILT DAILY FROM THE API" if wide else "", x=x0))

    def hero_panel(x, y, w, h):
        o = panel(x, y, w, h, CYAN, glow=True)
        o += '<circle cx="%.1f" cy="%.1f" r="5" fill="%s" class="blink"/>' % (x + 22, y + 26, stc)
        o += t(x + 36, y + 30, "STATUS: " + state, 11, stc, MONO, None, "700", 2)
        o += t(x + 20, y + 62, "CONTRIBUTIONS · LAST 12 MONTHS", 9.5, DIM, MONO, None, "600", 1.4)
        o += ('<text x="%.1f" y="%.1f" font-family="%s" font-size="54" font-weight="800" fill="url(#ink)">%s</text>'
              % (x + 18, y + 118, SANS, esc(fmt(cal["total"]))))
        o += '<path d="M%.1f %.1fH%.1f" stroke="%s"/>' % (x + 20, y + 136, x + w - 20, LINE)
        o += t(x + 20, y + 156, "last push   %s · %s" % (pushed.strftime("%d %b %Y"), last_repo), 10, MUTED, MONO)
        o += t(x + 20, y + 174, "online since  %s" % created.strftime("%b %Y"), 10, MUTED, MONO)
        return o

    if wide:
        b.append(hero_panel(28, 76, 300, 192))
        tw, th = 172, 88
        for i, (lab, val, col, note) in enumerate(tiles):
            b.append(tile(344 + (i % 3) * (tw + 8), 76 + (i // 3) * (th + 16), tw, th, lab, val, col, note))
        y = 300
        b.append(t(28, y, "WEEKLY SIGNAL", 10, TEXT, MONO, None, "700", 2))
        b.append(t(W - 28, y, "CONTRIBUTIONS PER WEEK · LAST 26 WEEKS", 9.5, DIM, MONO, "end", None, 1.2))
        b.append(signal(28, y + 14, W - 56, 64, wk, CYAN))
        y += 124
        b.append(t(28, y, "LANGUAGE DISTRIBUTION", 10, TEXT, MONO, None, "700", 2))
        b.append(t(W - 28, y, "BY BYTES IN PUBLIC REPOSITORIES", 9.5, DIM, MONO, "end", None, 1.2))
        s, bottom = lang_bar(28, y + 14, W - 56, d["langs"], 4)
        b.append(s)
        H = int(bottom + 52)
    else:
        b.append(hero_panel(20, 70, W - 40, 192))
        tw, th = (W - 48) / 2, 84
        for i, (lab, val, col, note) in enumerate(tiles):
            b.append(tile(20 + (i % 2) * (tw + 8), 278 + (i // 2) * (th + 10), tw, th, lab, val, col, note))
        y = 278 + 3 * (th + 10) + 26
        b.append(t(20, y, "WEEKLY SIGNAL · 26 WEEKS", 10, TEXT, MONO, None, "700", 1.6))
        b.append(signal(20, y + 14, W - 40, 60, wk, CYAN))
        y += 116
        b.append(t(20, y, "LANGUAGES · BY BYTES", 10, TEXT, MONO, None, "700", 1.6))
        s, bottom = lang_bar(20, y + 14, W - 40, d["langs"], 2)
        b.append(s)
        H = int(bottom + 52)
    src = "GITHUB REST + %s · LEETCODE %s" % (cal["source"] or "NO CALENDAR", "API" if lc["source"] == "LEETCODE" else "REPO")
    b.append(t(x0, H - 20, "GENERATED %s · %s" % (d["today"].strftime("%d %b %Y").upper(), src if wide else "SEE WORKFLOW"),
               9, FAINT, MONO, None, None, 1.1))
    ink = ('<linearGradient id="ink" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff"/>'
           '<stop offset="1" stop-color="%s"/></linearGradient>' % CYAN)
    return svg(W, H, "".join(b),
               "GitHub system status, generated %s. Status %s, last push %s. %s contributions in the last 12 "
               "months across %s active days. %s public repositories, %s commits excluding bots, %s languages, %s "
               "followers, %s LeetCode problems solved."
               % (d["today"].isoformat(), state, pushed.isoformat(), fmt(cal["total"]), fmt(active_days),
                  fmt(u["public_repos"]), fmt(commits), fmt(len(d["langs"])), fmt(u["followers"]),
                  fmt(lc["solved"])), ink)


# --------------------------------------------------------- shipped-repos.svg
def summary(r):
    return (r.get("description") or "").strip() or BLURBS.get(r["name"], "")


def repo_card(x, y, w, h, r, d, wrap_at):
    live = r.get("homepage") or ("https://%s.github.io/%s/" % (USER, r["name"]) if r.get("has_pages") else "")
    col = {0: CYAN, 1: TEAL, 2: VIOLET, 3: GOLD}.get(ORDER.index(r["name"]) if r["name"] in ORDER else 9, BLUE)
    o = panel(x, y, w, h, col)
    o += t(x + 18, y + 34, r["name"], 16, TEXT, SANS, None, "700", .3)
    if live:
        o += chip(x + w - 14, y + 18, "● LIVE", TEAL, 9.5, True, 20, anchor="end")[0]
        o += t(x + 18, y + 54, live.replace("https://", "").rstrip("/") + " ↗", 10, col, MONO)
    else:
        o += t(x + 18, y + 54, "github.com/%s/%s" % (USER, r["name"]), 10, DIM, MONO)
    o += lines(x + 18, y + 80, wrap(summary(r), wrap_at)[:3], 11.5, MUTED, SANS, 17)
    s, _ = chips(x + 18, y + h - 84, STACKS.get(r["name"], [r.get("language") or "code"]), w - 36, col, 9.5, row_h=26)
    o += s
    n = d["commits"].get(r["name"])
    foot = "updated %s · %s commit%s" % (r["pushed_at"][:10], fmt(n), "" if n == 1 else "s")
    if r["name"] == "LeetCode-Solution":
        lc = d["lc"]
        foot = "%s Java solutions · %s solved on LeetCode" % (fmt(lc.get("files")), fmt(lc.get("solved")))
    o += t(x + 18, y + h - 16, foot, 10, GOLD if r["name"] == "LeetCode-Solution" else DIM, MONO)
    return o


def render_shipped(d, W):
    by = {r["name"]: r for r in d["repos"] if r["size"] > 0 and r["name"] != USER}
    names = [n for n in ORDER if n in by] + sorted(n for n in by if n not in ORDER)
    rs = [by[n] for n in names]
    b = []
    if W == WIDE:
        b.append(header(W, "05", "SHIPPED ON GITHUB", "%d PUBLIC REPOSITORIES WITH CODE" % len(rs)))
        cw, ch = 414, 214
        y = 76
        for i, r in enumerate(rs):
            full = i == len(rs) - 1 and len(rs) % 2 == 1
            x = 28 + (i % 2) * (cw + 16)
            b.append(repo_card(x, y + (i // 2) * (ch + 16), W - 56 if full else cw, 168 if full else ch, r, d,
                               110 if full else 58))
        H = y + ((len(rs) + 1) // 2) * (ch + 16) + 10 - (ch - 168 if len(rs) % 2 else 0)
    else:
        b.append(header(W, "05", "SHIPPED ON GITHUB", "", x=20))
        ch = 220
        for i, r in enumerate(rs):
            b.append(repo_card(20, 72 + i * (ch + 14), W - 40, ch, r, d, 56))
        H = 72 + len(rs) * (ch + 14) + 10
    return svg(W, H, "".join(b),
               "Shipped on GitHub: " + "; ".join("%s: %s" % (r["name"], summary(r)) for r in rs))


def main():
    try:
        print("fetching...")
        data = fetch()
        validate(data)
    except Exception as e:                                            # noqa: BLE001
        print("ERROR: %s" % e, file=sys.stderr)
        print("existing panels left untouched.", file=sys.stderr)
        return 1
    print("rendering live panels:")
    for name, fn in (("github-command-center", render_command_center), ("shipped-repos", render_shipped)):
        write(os.path.join(OUT, name + ".svg"), fn(data, WIDE))
        write(os.path.join(OUT, "m", name + ".svg"), fn(data, NARROW))
    return 0


if __name__ == "__main__":
    sys.exit(main())
