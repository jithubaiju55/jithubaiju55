#!/usr/bin/env python3
"""Builds assets/training.svg from your LIVE GitHub data: cumulative-contribution 'training curve',
metrics, daily heatmap and language mixture. Zero dependencies.
Uses GITHUB_TOKEN if present, otherwise falls back to public pages."""
import json, os, re, sys, urllib.request
from datetime import date
from html import escape as E

USER = os.environ.get("GH_USER", "jithubaiju55")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "training.svg")
S = "'Inter','SF Pro Display','Segoe UI',Helvetica,Arial,sans-serif"
M = "'JetBrains Mono','SF Mono','Fira Code',ui-monospace,Menlo,Consolas,monospace"
BG, PANEL, HAIR, DIM, INK, LIME = "#05060a", "#08090d", "#23262f", "#6b7280", "#f5f5f0", "#c8ff2e"
LANG = {"Python": "#3572A5", "Jupyter Notebook": "#DA5B0B", "JavaScript": "#f1e05a", "TypeScript": "#3178c6", "HTML": "#e34c26",
        "CSS": "#8b5cf6", "Java": "#b07219", "Go": "#00ADD8", "C": "#8a8a8a", "C++": "#f34b7d", "Shell": "#89e051"}

def get(url, api=False):
    h = {"User-Agent": "Mozilla/5.0"}
    if api:
        h["Accept"] = "application/vnd.github+json"
        if TOKEN: h["Authorization"] = f"Bearer {TOKEN}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=30) as r:
        return r.read().decode()

def contributions():
    html = get(f"https://github.com/users/{USER}/contributions")
    tips = {a: b for a, b in re.findall(r'for="([^"]+)"[^>]*>\s*(No|\d+)\s+contribution', html)}
    days = {}
    for td in re.findall(r"<td[^>]*ContributionCalendar-day[^>]*>", html):
        d = re.search(r'data-date="([\d-]+)"', td); i = re.search(r'id="([^"]+)"', td)
        if d and i:
            n = tips.get(i.group(1), "0"); days[d.group(1)] = 0 if n == "No" else int(n)
    days = sorted(days.items())
    longest = run = 0
    for _, v in days:
        run = run + 1 if v else 0; longest = max(longest, run)
    cur, i = 0, len(days) - 1
    if i >= 0 and days[i][1] == 0: i -= 1
    while i >= 0 and days[i][1] > 0: cur += 1; i -= 1
    return days, sum(v for _, v in days), cur, longest

def languages():
    try:
        agg = {}
        for r in json.loads(get(f"https://api.github.com/users/{USER}/repos?per_page=100", api=True)):
            if r.get("fork"): continue
            for k, v in json.loads(get(r["languages_url"], api=True)).items(): agg[k] = agg.get(k, 0) + v
        if agg: return agg
    except Exception as e:
        print("API unavailable, using page fallback:", e, file=sys.stderr)
    agg = {}
    for l in re.findall(r'itemprop="programmingLanguage">([^<]+)<', get(f"https://github.com/{USER}?tab=repositories")):
        agg[l.strip()] = agg.get(l.strip(), 0) + 1
    return agg

def build(days, total, cur, best, langs):
    W, H = 900, 370
    N = len(days); vals = [v for _, v in days]
    cum, c = [], 0
    for v in vals: c += v; cum.append(c)
    tot = max(cum[-1], 1)
    ramp = ["#14161c", "#2f3f0c", "#5a7a10", "#8fc21a", LIME]
    mx = max(vals + [1])
    lvl = lambda v: 0 if v == 0 else 1 if v/mx <= .25 else 2 if v/mx <= .5 else 3 if v/mx <= .75 else 4

    def marks(w, h, i=10, s=4):
        return "".join(f'<path d="M{x-s} {y}H{x+s}M{x} {y-s}V{y+s}" stroke="#3a3f4d"/>' for x, y in [(i, i), (w-i, i), (i, h-i), (w-i, h-i)])
    def panel(x, y, w, h, title, delay, inner):
        return (f'<g class="f" style="animation-delay:{delay}s"><g transform="translate({x},{y})">'
                f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="3" fill="{PANEL}" stroke="{HAIR}"/>{marks(w, h)}'
                f'<text x="24" y="30" class="m" font-size="10" letter-spacing="2.5" fill="{LIME}">{title}</text>{inner}</g></g>')

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none"><defs>'
         f'<linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{LIME}" stop-opacity=".32"/><stop offset="1" stop-color="{LIME}" stop-opacity="0"/></linearGradient>'
         f'<filter id="gw" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
         f'<style>.s{{font-family:{S}}}.m{{font-family:{M}}}.f{{opacity:0;animation:in .9s cubic-bezier(.2,.8,.2,1) forwards}}'
         f'@keyframes in{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}.c{{opacity:0;animation:cf .5s ease-out forwards}}@keyframes cf{{to{{opacity:1}}}}</style>']

    # A — training curve
    cx0, cw, top, base = 24, 552, 62, 166
    px = lambda i: cx0 + i * cw / max(N - 1, 1)
    py = lambda i: base - cum[i] / tot * (base - top)
    pts = " L".join(f"{px(i):.1f},{py(i):.1f}" for i in range(N))
    line = f"M{pts}"; area = f"{line} L{px(N-1):.1f},{base} L{cx0},{base} Z"
    a = "".join(f'<line x1="{cx0}" y1="{y}" x2="{cx0+cw}" y2="{y}" stroke="{HAIR}" stroke-dasharray="2 4"/><text x="{cx0+4}" y="{y-4}" class="m" font-size="9" fill="{DIM}">{lab}</text>'
                for y, lab in [(base, "0"), ((base+top)/2, f"{tot//2:,}"), (top, f"{tot:,}")])
    for i, (d, _) in enumerate(days):
        if d.endswith("-01") and 40 < px(i) < cx0 + cw - 20:
            a += f'<path d="M{px(i):.1f} {base}v4" stroke="#3a3f4d"/><text x="{px(i):.1f}" y="{base+18}" text-anchor="middle" class="m" font-size="9" fill="{DIM}">{date.fromisoformat(d).strftime("%b").upper()}</text>'
    a += (f'<path d="{area}" fill="url(#ar)" opacity="0"><animate attributeName="opacity" from="0" to="1" dur="1s" begin="2s" fill="freeze"/></path>'
          f'<path d="{line}" pathLength="1" class="cv" stroke="{LIME}" stroke-width="2" stroke-linejoin="round" stroke-dasharray="1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" from="1" to="0" dur="2.4s" begin=".4s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".3 .7 .2 1"/></path>'
          f'<circle cx="{px(N-1):.1f}" cy="{py(N-1):.1f}" r="4" fill="{LIME}" filter="url(#gw)"/>'
          f'<circle cx="{px(N-1):.1f}" cy="{py(N-1):.1f}" r="4" stroke="{LIME}"><animate attributeName="r" values="4;14" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0" dur="2s" repeatCount="indefinite"/></circle>')
    o.append(panel(0, 0, 600, 204, "TRAINING RUN · CUMULATIVE CONTRIBUTIONS · 12 MO", 0, a))
    # B — metrics
    bm = (f'<text x="24" y="66" class="m" font-size="9" letter-spacing="1.5" fill="{DIM}">TOTAL CONTRIBUTIONS</text>'
          f'<text x="22" y="118" class="s" font-size="56" font-weight="800" letter-spacing="-2" fill="{LIME}">{total:,}</text>'
          f'<text x="24" y="152" class="m" font-size="9" letter-spacing="1.5" fill="{DIM}">CURRENT STREAK</text>'
          f'<text x="24" y="180" class="s" font-size="24" font-weight="800" fill="{INK}">{cur}<tspan class="m" font-size="10" font-weight="400" fill="{DIM}"> days</tspan></text>'
          f'<text x="150" y="152" class="m" font-size="9" letter-spacing="1.5" fill="{DIM}">BEST STREAK</text>'
          f'<text x="150" y="180" class="s" font-size="24" font-weight="800" fill="{INK}">{best}<tspan class="m" font-size="10" font-weight="400" fill="{DIM}"> days</tspan></text>')
    o.append(panel(620, 0, 280, 204, "METRICS", .12, bm))
    # C — heatmap
    first = date.fromisoformat(days[0][0]); off = (first.weekday() + 1) % 7; st = cw / 53
    h = ""
    for i, (d, v) in enumerate(days):
        col, row = divmod(i + off, 7)
        h += f'<rect class="c" style="animation-delay:{.4+col*.02:.2f}s" x="{cx0+col*st:.1f}" y="{48+row*st:.1f}" width="{st-2:.1f}" height="{st-2:.1f}" rx="1.5" fill="{ramp[lvl(v)]}"/>'
    lx = cx0 + cw - 100
    h += (f'<text x="{lx-6}" y="{48+7*st+22:.1f}" text-anchor="end" class="m" font-size="9" fill="{DIM}">LESS</text>' +
          "".join(f'<rect x="{lx+i*13}" y="{48+7*st+14:.1f}" width="9" height="9" rx="1.5" fill="{c}"/>' for i, c in enumerate(ramp)) +
          f'<text x="{lx+70}" y="{48+7*st+22:.1f}" class="m" font-size="9" fill="{DIM}">MORE</text>')
    o.append(panel(0, 220, 600, 150, "ACTIVITY · DAILY", .24, h))
    # D — language mixture
    top5 = sorted(langs.items(), key=lambda kv: -kv[1])[:5]; s = sum(langs.values()) or 1; m = top5[0][1] / s if top5 else 1
    l = ""
    for i, (n, v) in enumerate(top5):
        y = 58 + i * 18; p = v / s
        nm = "Jupyter" if n == "Jupyter Notebook" else n
        l += (f'<text x="24" y="{y}" class="m" font-size="10" fill="#cbd5e1">{E(nm)}</text><rect x="100" y="{y-7}" width="118" height="5" rx="2.5" fill="{HAIR}"/>'
              f'<rect x="100" y="{y-7}" width="0" height="5" rx="2.5" fill="{LANG.get(n, "#8b949e")}"><animate attributeName="width" from="0" to="{118*p/m:.1f}" dur="1.2s" begin="{.5+i*.1:.1f}s" fill="freeze"/></rect>'
              f'<text x="256" y="{y}" text-anchor="end" class="m" font-size="10" fill="{DIM}">{100*p:.1f}%</text>')
    o.append(panel(620, 220, 280, 150, "DATA MIXTURE · LANGUAGES", .36, l))
    o.append("</svg>")
    return "".join(o)

if __name__ == "__main__":
    days, total, cur, best = contributions()
    langs = languages()
    print("total", total, "streak", cur, "best", best, "langs", langs)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write(build(days, total, cur, best, langs))
