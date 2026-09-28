#!/usr/bin/env python3
"""Builds assets/load.svg — a CRT-style 'power meter' from LIVE GitHub contribution data.
Standalone (no local imports) so it runs cleanly in CI. Uses GITHUB_TOKEN if present."""
import os, re, sys, urllib.request

USER = os.environ.get("GH_USER", "jithubaiju55")
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "load.svg")
S = "'Inter','SF Pro Display','Segoe UI',Helvetica,Arial,sans-serif"
M = "'JetBrains Mono','SF Mono','Fira Code',ui-monospace,Menlo,Consolas,monospace"
BG, HAIR, DIM, INK, GREEN, CYAN = "#05060a", "#20263a", "#7d8494", "#f2f4f8", "#22e07a", "#2fe6ff"

def get(url):
    h = {"User-Agent": "Mozilla/5.0"}
    with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=30) as r:
        return r.read().decode()

def contributions():
    try:
        html = get(f"https://github.com/users/{USER}/contributions")
    except Exception as e:
        print(f"warn: could not fetch contributions — {e}", file=sys.stderr)
        return [], 0, 0, 0

    days = {}
    # Primary: parse data-date + data-count attributes (GitHub's current markup)
    for td in re.findall(r'<td[^>]+class="[^"]*ContributionCalendar-day[^"]*"[^>]*>', html):
        d = re.search(r'data-date="([\d-]+)"', td)
        # data-count is the most direct signal
        c = re.search(r'data-count="(\d+)"', td)
        if not c:
            # fallback: data-level 0 means 0, 1-4 means contributed
            lv = re.search(r'data-level="(\d)"', td)
            c_val = 0 if (not lv or lv.group(1) == '0') else 1
        else:
            c_val = int(c.group(1))
        if d:
            days[d.group(1)] = c_val

    if not days:
        # Last-resort fallback: tooltip labels (old GitHub markup)
        tips = {a: b for a, b in re.findall(r'for="([^"]+)"[^>]*>\s*(No|\d+)\s+contribution', html)}
        for td in re.findall(r'<td[^>]*ContributionCalendar-day[^>]*>', html):
            d = re.search(r'data-date="([\d-]+)"', td)
            i = re.search(r'id="([^"]+)"', td)
            if d and i:
                n = tips.get(i.group(1), "0")
                days[d.group(1)] = 0 if n == "No" else int(n)

    days = sorted(days.items())
    longest = run = 0
    for _, v in days:
        run = run + 1 if v else 0; longest = max(longest, run)
    cur, i = 0, len(days) - 1
    if i >= 0 and days[i][1] == 0: i -= 1
    while i >= 0 and days[i][1] > 0: cur += 1; i -= 1
    return days, sum(v for _, v in days), cur, longest

def build(days, total, cur, best):
    W, H = 900, 176
    last = days[-84:]
    if len(last) < 2:
        # Not enough data to draw a line — emit a minimal placeholder
        last = [("0000-00-00", 0), ("0000-00-01", 0)]
    mx = max(v for _, v in last) or 1
    n = len(last); cw = 690; x0 = 178
    pts = [(x0 + i * cw / (n - 1), 44 + (1 - v / mx) * 80) for i, (_, v) in enumerate(last)]
    d_line = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = f"{d_line} L{pts[-1][0]:.1f},124 L{pts[0][0]:.1f},124 Z"
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none"><defs>'
         f'<linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity=".3"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></linearGradient>'
         f'<pattern id="sl" width="3" height="3" patternUnits="userSpaceOnUse"><rect width="3" height="1.1" fill="#000" fill-opacity=".05"/></pattern>'
         f'<filter id="gw" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
         f'<style>.s{{font-family:{S}}}.m{{font-family:{M}}}.f{{opacity:0;animation:in .8s cubic-bezier(.2,.8,.2,1) forwards}}'
         f'@keyframes in{{from{{opacity:0;transform:translateY(7px)}}to{{opacity:1;transform:none}}}}'
         f'@keyframes pulse2{{0%{{transform:scale(.85);opacity:.9}}70%,100%{{transform:scale(2.4);opacity:0}}}}</style>']
    o.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="8" fill="{BG}" stroke="{HAIR}"/>')
    o.append(f'<text x="24" y="30" class="m" font-size="10" letter-spacing="2.5" fill="{GREEN}">POWER METER · LIVE</text>'
             f'<text x="{W-24}" y="30" text-anchor="end" class="m" font-size="10" fill="{DIM}">github commits · last 12 weeks</text>')
    o.append(f'<g class="f"><text x="24" y="76" class="s" font-size="38" font-weight="800" fill="{INK}">{total:,}</text>'
             f'<text x="24" y="96" class="m" font-size="9" fill="{DIM}">CONTRIBUTIONS</text>'
             f'<text x="24" y="128" class="s" font-size="20" font-weight="800" fill="{GREEN}">{cur}<tspan class="m" font-size="9" font-weight="400" fill="{DIM}"> day streak</tspan></text>'
             f'<text x="24" y="150" class="s" font-size="14" font-weight="700" fill="{INK}">{best}<tspan class="m" font-size="9" font-weight="400" fill="{DIM}"> best streak</tspan></text></g>')
    o.append(f'<g class="f" style="animation-delay:.15s"><path d="{area}" fill="url(#ar)"/>'
             f'<path d="{d_line}" pathLength="1" stroke="{GREEN}" stroke-width="2" stroke-linejoin="round" stroke-dasharray="1" stroke-dashoffset="1">'
             f'<animate attributeName="stroke-dashoffset" from="1" to="0" dur="2s" begin=".3s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".25 .8 .3 1"/></path>'
             f'<circle cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r="4" fill="{GREEN}" filter="url(#gw)"/>'
             f'<circle cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r="4" fill="none" stroke="{GREEN}" style="transform-origin:{pts[-1][0]:.1f}px {pts[-1][1]:.1f}px;animation:pulse2 2.2s ease-out infinite"/></g>')
    o.append(f'<line x1="{x0}" y1="124" x2="{x0+cw}" y2="124" stroke="{HAIR}"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#sl)" rx="8"/>')
    o.append("</svg>")
    return "".join(o)

if __name__ == "__main__":
    days, total, cur, best = contributions()
    if not days:
        print("error: no contribution data scraped — skipping SVG update", file=sys.stderr)
        sys.exit(0)  # soft exit so CI marks step green
    print("total", total, "streak", cur, "best", best)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write(build(days, total, cur, best))
