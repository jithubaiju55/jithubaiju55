#!/usr/bin/env python3
"""Builds assets/stats.svg: contribution total, streaks, 12-month heatmap and language bar.
Zero dependencies. Uses GITHUB_TOKEN if set; otherwise falls back to public pages."""
import json, os, re, sys, urllib.request
from datetime import date
from html import escape as E

USER = os.environ.get("GH_USER", "jithubaiju55")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "stats.svg")
LANG = {"Python": "#3572A5", "Jupyter Notebook": "#DA5B0B", "JavaScript": "#f1e05a", "TypeScript": "#3178c6", "HTML": "#e34c26",
        "CSS": "#8b5cf6", "Java": "#b07219", "Go": "#00ADD8", "C": "#8a8a8a", "C++": "#f34b7d", "Shell": "#89e051"}
S = "'Inter','SF Pro Display','Segoe UI',system-ui,-apple-system,sans-serif"
M = "'JetBrains Mono','Fira Code',ui-monospace,Menlo,Consolas,monospace"
TEAL, INDIGO = "#5eead4", "#818cf8"

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

def build(days, total, cur, longest, langs):
    W, H = 900, 304
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:6]; s = sum(v for _, v in top) or 1
    mx = max([v for _, v in days] + [1])
    ramp = ["#12151d", "#134e4a", "#0f766e", "#14b8a6", TEAL]
    def lvl(v):
        if v == 0: return 0
        q = v / mx
        return 1 if q <= .25 else 2 if q <= .5 else 3 if q <= .75 else 4
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none"><defs>'
         f'<linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{TEAL}" stop-opacity=".6"/><stop offset=".6" stop-color="#1c2030"/></linearGradient>'
         f'<linearGradient id="nm" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="{TEAL}"/></linearGradient>'
         f'<radialGradient id="gl" cx="0" cy="0" r="1"><stop offset="0" stop-color="{TEAL}" stop-opacity=".12"/><stop offset=".7" stop-color="{TEAL}" stop-opacity="0"/></radialGradient>'
         f'<clipPath id="lb"><rect x="24" y="0" width="0" height="8" rx="4"><animate attributeName="width" from="0" to="852" dur="1.4s" begin=".6s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1"/></rect></clipPath></defs>'
         f'<style>.s{{font-family:{S}}}.m{{font-family:{M}}}.f{{opacity:0;animation:in .8s cubic-bezier(.2,.8,.2,1) forwards}}'
         f'@keyframes in{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}'
         f'.c{{opacity:0;animation:cf .5s ease-out forwards}}@keyframes cf{{to{{opacity:1}}}}</style>']
    def card(x, y, w, h): return (f'<rect x="{x+.75}" y="{y+.75}" width="{w-1.5}" height="{h-1.5}" rx="22" fill="#0b0d13" stroke="url(#bd)" stroke-width="1.5"/>'
                                  f'<rect x="{x+.75}" y="{y+.75}" width="{w-1.5}" height="{h-1.5}" rx="22" fill="url(#gl)"/>')
    # left
    o.append('<g class="f">' + card(0, 0, 290, 170) +
             f'<text x="26" y="36" class="m" font-size="10" letter-spacing="2.5" fill="{TEAL}">CONTRIBUTIONS</text>'
             f'<text x="24" y="98" class="s" font-size="58" font-weight="800" letter-spacing="-2" fill="url(#nm)">{total:,}</text>'
             f'<text x="26" y="120" class="s" font-size="12" fill="#64748b">in the last 12 months</text>'
             f'<text x="26" y="150" class="s" font-size="18" font-weight="700" fill="#f1f5f9">{cur}<tspan class="m" font-size="9" fill="#64748b" letter-spacing="1.5">  DAY STREAK</tspan></text>'
             f'<text x="160" y="150" class="s" font-size="18" font-weight="700" fill="#f1f5f9">{longest}<tspan class="m" font-size="9" fill="#64748b" letter-spacing="1.5">  BEST</tspan></text></g>')
    # heatmap
    o.append('<g class="f" style="animation-delay:.15s">' + card(306, 0, 594, 170) +
             f'<text x="330" y="36" class="m" font-size="10" letter-spacing="2.5" fill="{INDIGO}">DAILY ACTIVITY</text>')
    first = date.fromisoformat(days[0][0]); off = (first.weekday() + 1) % 7
    step = 10.35
    for idx, (d, v) in enumerate(days):
        pos = idx + off; col, row = divmod(pos, 7)
        o.append(f'<rect class="c" style="animation-delay:{.3+col*.018:.2f}s" x="{330+col*step:.1f}" y="{52+row*step:.1f}" width="8.4" height="8.4" rx="2" fill="{ramp[lvl(v)]}"/>')
    lx = 900 - 24 - 5 * 12 - 60
    o.append(f'<text x="{lx}" y="152" text-anchor="end" class="m" font-size="9" fill="#64748b">LESS</text>' +
             "".join(f'<rect x="{lx+8+i*12}" y="144" width="8.4" height="8.4" rx="2" fill="{c}"/>' for i, c in enumerate(ramp)) +
             f'<text x="{lx+8+5*12+4}" y="152" class="m" font-size="9" fill="#64748b">MORE</text></g>')
    # languages
    o.append('<g class="f" style="animation-delay:.3s">' + card(0, 186, 900, 118) +
             f'<text x="26" y="222" class="m" font-size="10" letter-spacing="2.5" fill="#f472b6">TOP LANGUAGES</text>'
             '<g transform="translate(0,236)"><rect x="24" y="0" width="852" height="8" rx="4" fill="#141824"/><g clip-path="url(#lb)">')
    x = 24.0
    for n, v in top:
        w = 852 * v / s
        o.append(f'<rect x="{x:.1f}" y="0" width="{w+.6:.1f}" height="8" fill="{LANG.get(n, "#8b949e")}"/>'); x += w
    o.append('</g></g>')
    lx = 26.0
    for n, v in top:
        p = f"{100*v/s:.1f}%"
        o.append(f'<circle cx="{lx+4:.1f}" cy="273" r="4" fill="{LANG.get(n, "#8b949e")}"/>'
                 f'<text x="{lx+14:.1f}" y="277" class="s" font-size="12"><tspan fill="#cbd5e1">{E(n)}</tspan> <tspan fill="#64748b">{p}</tspan></text>')
        lx += 14 + (len(n) + 1 + len(p)) * 7 + 26
    o.append('</g></svg>')
    return "".join(o)

if __name__ == "__main__":
    days, total, cur, longest = contributions()
    langs = languages()
    print("total", total, "streak", cur, "best", longest, "langs", langs)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write(build(days, total, cur, longest, langs))
