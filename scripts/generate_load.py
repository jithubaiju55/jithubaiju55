#!/usr/bin/env python3
"""Builds assets/load.svg — 'system load' panel from LIVE GitHub contribution data.
Zero dependencies. Uses GITHUB_TOKEN if present, else falls back to public pages."""
import os, re, sys, urllib.request
from datetime import date
from html import escape as E

USER = os.environ.get("GH_USER", "jithubaiju55")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "load.svg")
S = "'Inter','SF Pro Display','Segoe UI',Helvetica,Arial,sans-serif"
M = "'JetBrains Mono','SF Mono','Fira Code',ui-monospace,Menlo,Consolas,monospace"
BG, ROW, HAIR, DIM, INK, GREEN = "#08090b", "#0d0f13", "#20242f", "#7d8494", "#f2f4f8", "#22e07a"

def get(url):
    h = {"User-Agent": "Mozilla/5.0"}
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

def build(days, total, cur, best):
    W, H = 900, 168
    last = days[-84:]  # ~12 weeks
    mx = max(v for _, v in last) or 1
    n = len(last); cw = 700; x0 = 170
    pts = [(x0 + i * cw / (n - 1), 40 + (1 - v / mx) * 78) for i, (_, v) in enumerate(last)]
    d_line = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = f"{d_line} L{pts[-1][0]:.1f},118 L{pts[0][0]:.1f},118 Z"
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none"><defs>'
         f'<linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity=".28"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></linearGradient>'
         f'<filter id="gw" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
         f'<style>.s{{font-family:{S}}}.m{{font-family:{M}}}.f{{opacity:0;animation:in .8s cubic-bezier(.2,.8,.2,1) forwards}}'
         f'@keyframes in{{from{{opacity:0;transform:translateY(7px)}}to{{opacity:1;transform:none}}}}</style>']
    o.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="8" fill="{BG}" stroke="{HAIR}"/>')
    o.append(f'<text x="24" y="30" class="m" font-size="10" letter-spacing="2.5" fill="{GREEN}">SYSTEM LOAD</text>'
             f'<text x="{W-24}" y="30" text-anchor="end" class="m" font-size="10" fill="{DIM}">github commits · last 12 weeks</text>')
    o.append(f'<g class="f"><text x="24" y="70" class="s" font-size="34" font-weight="800" fill="{INK}">{total:,}</text>'
             f'<text x="24" y="90" class="m" font-size="9" fill="{DIM}">CONTRIBUTIONS</text>'
             f'<text x="24" y="122" class="s" font-size="20" font-weight="800" fill="{GREEN}">{cur}<tspan class="m" font-size="9" font-weight="400" fill="{DIM}"> day streak</tspan></text>'
             f'<text x="24" y="144" class="s" font-size="14" font-weight="700" fill="{INK}">{best}<tspan class="m" font-size="9" font-weight="400" fill="{DIM}"> best streak</tspan></text></g>')
    o.append(f'<g class="f" style="animation-delay:.15s"><path d="{area}" fill="url(#ar)"/>'
             f'<path d="{d_line}" pathLength="1" stroke="{GREEN}" stroke-width="2" stroke-linejoin="round" stroke-dasharray="1" stroke-dashoffset="1">'
             f'<animate attributeName="stroke-dashoffset" from="1" to="0" dur="2s" begin=".3s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".25 .8 .3 1"/></path>'
             f'<circle cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r="4" fill="{GREEN}" filter="url(#gw)"/></g>')
    o.append(f'<line x1="{x0}" y1="136" x2="{x0+cw}" y2="136" stroke="{HAIR}"/>')
    o.append("</svg>")
    return "".join(o)

if __name__ == "__main__":
    days, total, cur, best = contributions()
    print("total", total, "streak", cur, "best", best)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write(build(days, total, cur, best))
