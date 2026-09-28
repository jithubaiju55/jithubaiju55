#!/usr/bin/env python3
"""Rebuilds every static arcade-theme asset into ../assets:
hero, level-1..level-8 (service tiles), pipeline (isometric), questlog, cta.
Run from the scripts/ folder: python3 build_assets.py"""
import os
from common import *

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUT, exist_ok=True)
def out(name): return os.path.join(OUT, name)

# ═════════════ HERO ═════════════
def hero():
    W, H = 900, 480
    horizon = 300
    d = (f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a0616"/><stop offset=".55" stop-color="#0d0a1c"/><stop offset="1" stop-color="{BG}"/></linearGradient>'
         f'<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{MAG}" stop-opacity=".12"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>'
         f'<radialGradient id="sun" cx=".5" cy="1" r=".55"><stop offset="0" stop-color="{CYAN}" stop-opacity=".5"/><stop offset=".7" stop-color="{MAG}" stop-opacity=".14"/><stop offset="1" stop-color="{MAG}" stop-opacity="0"/></radialGradient>'
         f'<linearGradient id="wd" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{MAG}"/></linearGradient>'
         f'<linearGradient id="bd" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}" stop-opacity=".7"/><stop offset=".5" stop-color="{HAIR}"/><stop offset="1" stop-color="{MAG}" stop-opacity=".55"/></linearGradient>'
         f'<clipPath id="cp"><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="8"/></clipPath><style>{PULSE_CSS}</style>')
    b = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="8" fill="{BG}"/><g clip-path="url(#cp)">',
         f'<rect width="{W}" height="{H}" fill="url(#sky)"/>',
         starfield(W, horizon + 20, 130, 22, [CYAN, MAG, "#fff", AMBER]),
         f'<circle cx="{W/2}" cy="{horizon}" r="150" fill="url(#sun)"/>',
         f'<rect y="{horizon}" width="{W}" height="{H-horizon}" fill="url(#floor)"/>',
         perspective_grid(W/2, horizon, W, H, CYAN, "hero", dur=4.2),
         f'<line x1="0" y1="{horizon}" x2="{W}" y2="{horizon}" stroke="{MAG}" stroke-opacity=".4"/>',
         '</g>']
    b.append(cube_badge(W - 96, 92, 34, CYAN, MAG, "h1", dur=5.5))
    b.append(f'<g class="f">{status_dot(48, 44, GREEN)}<text x="66" y="49" class="m" font-size="12" font-weight="700" letter-spacing="1.5" fill="{GREEN}">ALL SYSTEMS OPERATIONAL</text>'
             f'<text x="{W-140}" y="49" text-anchor="end" class="m" font-size="10" fill="{DIM}">auto-updated · gh actions</text></g>')
    ghost_x = ";".join(["-3", "2", "-1", "0", "0", "0", "0"])
    ghost_x2 = ";".join(["3", "-2", "1", "0", "0", "0", "0"])
    kt = "0;.05;.1;.16;.22;.6;1"
    title = "Jithu Baiju"
    b.append(f'<g><text x="47" y="242" class="s" font-size="98" font-weight="800" letter-spacing="-3.5" fill="{RED}" opacity=".65">'
             f'<animateTransform attributeName="transform" type="translate" values="{ghost_x};0" keyTimes="{kt};1" dur="1.3s" fill="freeze" additive="sum"/>{title}</text>'
             f'<text x="47" y="242" class="s" font-size="98" font-weight="800" letter-spacing="-3.5" fill="{CYAN}" opacity=".65">'
             f'<animateTransform attributeName="transform" type="translate" values="{ghost_x2};0" keyTimes="{kt};1" dur="1.3s" fill="freeze" additive="sum"/>{title}</text>'
             f'<text x="47" y="242" class="s" font-size="98" font-weight="800" letter-spacing="-3.5" fill="{INK}">{title}</text></g>')
    b.append(f'<text x="48" y="276" class="s f" style="animation-delay:.5s" font-size="17" fill="#c7c9d6">Software engineer running 8 services in production —</text>'
             f'<text x="48" y="300" class="s f" style="animation-delay:.6s" font-size="17" fill="#8a8fa3">agents, dev tools, ML and full-stack apps.</text>')
    stats = [("30+", "REPOS"), ("2", "PYPI PKGS"), ("6", "AGENT SYSTEMS")]
    x = 48
    for v, l in stats:
        b.append(f'<g class="f" style="animation-delay:.75s"><text x="{x}" y="336" class="s" font-size="17" font-weight="800" fill="{CYAN}">{E(v)}<tspan class="m" font-size="10" font-weight="400" fill="{DIM}" dx="6">{E(l)}</tspan></text></g>')
        x += (len(v) + len(l)) * 8 + 60
    b.append(f'<g class="f" style="animation-delay:.85s"><rect x="48" y="356" width="380" height="10" rx="5" fill="#161a26" stroke="{HAIR}"/>'
             f'<rect x="48" y="356" width="0" height="10" rx="5" fill="url(#wd)"><animate attributeName="width" from="0" to="380" dur="1.6s" begin="1s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1"/></rect>'
             f'<text x="48" y="380" class="m" font-size="9.5" letter-spacing="1.5" fill="{DIM}">LVL 99 · SHIPPING SINCE 2024 · XP CAP REACHED</text></g>')
    b.append(scanlines(W, H, "hero", .045))
    b.append(marks(W, H) + f'<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="8" stroke="url(#bd)" stroke-width="1.5"/>')
    open(out("hero.svg"), "w").write(svg(W, H, "".join(b), d))

# ═════════════ LEVEL TILES (services) ═════════════
LEVELS = [
    ("neuralhive", "neuralhive", "Free offline coding agent — runs 70B+ models locally.", "CLEAR", GREEN, 3, "local / offline-first"),
    ("AgenticFuzzer", "agentic-fuzzer", "Self-evolving fuzzer that finds its own mutation strategy.", "CLEAR", GREEN, 4, "swarm agents"),
    ("ClinicalAgent", "clinical-agent", "Six agents analyse cases, flag drug interactions.", "CLEAR", GREEN, 4, "6 agents"),
    ("AI-Researcher", "ai-researcher", "ReAct agent for multi-step research and reports.", "CLEAR", GREEN, 3, "~70% less research time"),
    ("RagKB", "rag-kb", "Local RAG chatbot, SSE streaming, no external APIs.", "CLEAR", GREEN, 3, "<2s p95 latency"),
    ("openenv-project", "sql-repair-env", "RL environment for agents to learn SQL repair.", "IN PROGRESS", AMBER, 3, "20 tasks · beta"),
    ("lazyload", "lazyload · pypi", "Defers heavy imports for instant startup.", "PUBLISHED", CYAN, 2, "pip install lazyload"),
    ("pytrace-live", "pytrace-live", "Traces Python execution live, flags slow code.", "PUBLISHED", CYAN, 2, "cli tool"),
]
def stars(x, y, n, lit, col):
    o = []
    for i in range(n):
        cx = x + i * 15
        o.append(f'<path d="M{cx} {y-5}l1.5 3.2 3.5.4-2.6 2.4.7 3.5-3.1-1.8-3.1 1.8.7-3.5-2.6-2.4 3.5-.4z" fill="{col}" stroke="{col}"/>')
    return "".join(o)

def level(i, repo, slug, desc, tag, col, diff, meta):
    W, H = 428, 176
    uid = f"lv{i}"
    d = (f'<linearGradient id="top{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{col}" stop-opacity=".22"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></linearGradient>'
         f'<linearGradient id="sw{uid}"><stop offset="0" stop-color="{col}" stop-opacity="0"/><stop offset=".5" stop-color="{col}" stop-opacity=".1"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></linearGradient>'
         f'<clipPath id="rc{uid}"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10"/></clipPath>')
    b = [f'<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="10" fill="{PANEL}" stroke="{col}" stroke-opacity=".45"/>',
         f'<rect x=".75" y=".75" width="{W-1.5}" height="46" rx="10" fill="url(#top{uid})"/>',
         f'<g clip-path="url(#rc{uid})"><rect x="-260" y="0" width="260" height="{H}" fill="url(#sw{uid})"><animateTransform attributeName="transform" type="translate" from="0 0" to="{W+260} 0" dur="7s" begin="{i*.8:.1f}s" repeatCount="indefinite"/></rect></g>']
    b.append(f'<text x="20" y="34" class="m" font-size="11" font-weight="700" letter-spacing="2" fill="{col}">LEVEL {i:02d}</text>')
    b.append(status_dot(W-24, 24, col, 4.5))
    b.append(f'<text x="20" y="66" class="s" font-size="21" font-weight="800" fill="{INK}">{E(slug)}</text>')
    b.append(stars(W-20-14*3, 60, diff, diff, col))
    b.append(f'<text x="20" y="90" class="s" font-size="12.5" fill="#a2a7b8">{E(desc)}</text>')
    bw = len(tag) * 6.6 + 20
    b.append(f'<rect x="20" y="106" width="{bw:.0f}" height="22" rx="11" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-opacity=".55"/>'
             f'<text x="{20+bw/2:.0f}" y="121" text-anchor="middle" class="m" font-size="10" letter-spacing="1" fill="{col}">{E(tag)}</text>')
    b.append(f'<text x="20" y="150" class="m" font-size="10.5" fill="{DIM}">{E(meta)}</text>')
    b.append(f'<text x="{W-20}" y="150" text-anchor="end" class="m" font-size="10" fill="{col}">github.com/jithubaiju55/{E(repo)} ↗</text>')
    b.append(marks(W, H, i=9, s=3.5))
    open(out(f"level-{i}.svg"), "w").write(svg(W, H, f'<g class="g" style="animation-delay:{(i-1)*.08:.2f}s">' + "".join(b) + '</g>', d))

# ═════════════ ISOMETRIC PIPELINE ═════════════
def iso_box(cx, cy, w, d, h, top_c, left_c, right_c):
    hw, hd = w/2, d/2
    T = [(cx, cy-h-hd), (cx+hw, cy-h-hd/2), (cx, cy-h), (cx-hw, cy-h-hd/2)]
    L = [(cx-hw, cy-h-hd/2), (cx, cy-h), (cx, cy), (cx-hw, cy-hd/2)]
    R = [(cx+hw, cy-h-hd/2), (cx, cy-h), (cx, cy), (cx+hw, cy-hd/2)]
    def poly(pts, fill):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        return f'<polygon points="{p}" fill="{fill}"/>'
    return poly(T, top_c) + poly(L, left_c) + poly(R, right_c)

def shade(c, f):
    c = c.lstrip('#'); r, g, bb = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    if f >= 0: r, g, bb = [int(v + (255 - v) * f) for v in (r, g, bb)]
    else: r, g, bb = [int(v * (1 + f)) for v in (r, g, bb)]
    return f"#{r:02x}{g:02x}{bb:02x}"

def pipeline():
    W, H = 900, 286
    stages = [("CLIENT", "browser / cli", DIM), ("GATEWAY", "FastAPI · Spring Boot", CYAN), ("ORCHESTRATOR", "LangChain · LangGraph", VIOLET), ("MODEL", "Llama 3.3 · PyTorch", GREEN), ("DATA", "SQLite · Postgres · Chroma", AMBER)]
    n = len(stages); xs = [110 + i * 175 for i in range(n)]
    base_y = 168
    b = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="8" fill="{BG}" stroke="{HAIR}"/>',
         f'<text x="24" y="30" class="m" font-size="10" letter-spacing="2.5" fill="{CYAN}">PIPELINE · ISOMETRIC</text>',
         f'<text x="{W-24}" y="30" text-anchor="end" class="m" font-size="10" fill="{DIM}">how a request moves through what I build</text>']
    for x in xs[:-1]:
        b.append(f'<line x1="{x+55:.1f}" y1="{base_y-38}" x2="{x+175-55:.1f}" y2="{base_y-38}" stroke="{HAIR}" stroke-dasharray="2 5"/>')
    for i, (x, (name, sub, col)) in enumerate(zip(xs, stages)):
        c = col if col != DIM else "#5a6070"
        top_c, left_c, right_c = shade(c, .35), shade(c, -.35), shade(c, -.1)
        b.append(f'<g class="g" style="animation-delay:{i*.1:.2f}s" filter="url(#gws)">' + iso_box(x, base_y, 78, 48, 60, top_c, left_c, right_c) + '</g>')
        b.append(f'<g class="g" style="animation-delay:{i*.15+.05:.2f}s"><text x="{x}" y="{base_y+40}" text-anchor="middle" class="m" font-size="11" font-weight="700" letter-spacing="1" fill="{c}">{E(name)}</text>'
                 f'<text x="{x}" y="{base_y+58}" text-anchor="middle" class="m" font-size="9.5" fill="{DIM}">{E(sub)}</text></g>')
    path = "M" + " L".join(f"{x+2:.1f},{base_y-38}" for x in xs)
    for k, delay in enumerate([0, 2.6, 5.2]):
        b.append(f'<circle r="3.4" fill="#fff" filter="url(#gw)"><animateMotion path="{path}" dur="7.8s" begin="{delay}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.04;.93;1" dur="7.8s" begin="{delay}s" repeatCount="indefinite"/></circle>')
    b.append(f'<text x="24" y="{H-14}" class="m" font-size="10" fill="{DIM}">e.g. ClinicalAgent · AI-Researcher · RagKB all follow this shape</text>')
    open(out("pipeline.svg"), "w").write(svg(W, H, "".join(b)))

# ═════════════ QUEST LOG ═════════════
LOG = [
    ("2024", "Q4", "Shipped first dev tools", "Code editor, calculator, JSON validator, auto-commenter.", DIM),
    ("2025", "Q3–Q4", "Moved into machine learning", "Attrition, student performance and road-damage models.", CYAN),
    ("2026", "Q1–Q2", "Started building agents", "ClinicalAgent, AI-Researcher, an RL env, a swarm fuzzer.", VIOLET),
    ("2026", "Q3", "Shipped to PyPI", "lazyload and pytrace-live — published for anyone to install.", GREEN),
]
def questlog():
    W, H = 900, 250
    b = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="8" fill="{BG}" stroke="{HAIR}"/>',
         f'<text x="24" y="32" class="m" font-size="10" letter-spacing="2.5" fill="{CYAN}">QUEST LOG</text>',
         f'<text x="{W-24}" y="32" text-anchor="end" class="m" font-size="10" fill="{DIM}">real repository history</text>',
         f'<line x1="98" y1="54" x2="98" y2="{H-22}" stroke="{HAIR}"/>']
    rowh = (H - 68) / len(LOG)
    for i, (yr, q, title, desc, col) in enumerate(LOG):
        y = 64 + i * rowh
        b.append(f'<g class="g" style="animation-delay:{i*.12:.2f}s">'
                 f'<text x="24" y="{y+5}" class="m" font-size="11" font-weight="700" fill="{INK}">{yr}</text>'
                 f'<text x="24" y="{y+19}" class="m" font-size="9.5" fill="{DIM}">{q}</text>'
                 f'<circle cx="98" cy="{y}" r="4.5" fill="{BG}" stroke="{col}" stroke-width="2"/><circle cx="98" cy="{y}" r="2" fill="{col}" filter="url(#gws)"/>'
                 f'<text x="120" y="{y+4}" class="s" font-size="15" font-weight="700" fill="{INK}">{E(title)}</text>'
                 f'<text x="120" y="{y+23}" class="s" font-size="12" fill="#9aa0ab">{E(desc)}</text>'
                 f'<rect x="{W-120}" y="{y-14}" width="88" height="20" rx="10" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".5"/>'
                 f'<text x="{W-76}" y="{y}" text-anchor="middle" class="m" font-size="9.5" fill="{col}">+XP UNLOCKED</text></g>')
    open(out("questlog.svg"), "w").write(svg(W, H, "".join(b)))

# ═════════════ CTA ═════════════
def cta():
    W, H = 900, 190
    d = (f'<radialGradient id="gg" cx=".08" cy="0" r="1"><stop offset="0" stop-color="{CYAN}" stop-opacity=".16"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>'
         f'<linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity=".6"/><stop offset="1" stop-color="{MAG}" stop-opacity=".45"/></linearGradient>'
         f'<linearGradient id="wd" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{MAG}"/></linearGradient><style>{PULSE_CSS}</style>')
    b = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="8" fill="{BG}"/><rect width="{W}" height="{H}" rx="8" fill="url(#gg)"/>']
    b.append(cube_badge(70, 95, 26, CYAN, MAG, "cta1", dur=4.0))
    b.append(f'<g class="f"><text x="112" y="80" class="s" font-size="27" font-weight="800" fill="{INK}">Got something worth building?</text>'
             f'<text x="112" y="114" class="s" font-size="27" font-weight="800" fill="url(#wd)">Insert coin to continue.</text></g>')
    b.append(f'<g class="f" style="animation-delay:.2s">{status_dot(114, 148, GREEN, 4)}<text x="128" y="152" class="m" font-size="10.5" letter-spacing="1" fill="{GREEN}">PRESS START · OPEN TO NEW DEPLOYMENTS</text></g>')
    b.append(f'<g class="f" style="animation-delay:.3s" text-anchor="end">'
             f'<text x="{W-24}" y="56" class="m" font-size="11" fill="#a8adba">jithubaiju124@gmail.com</text>'
             f'<text x="{W-24}" y="76" class="m" font-size="11" fill="{CYAN}">linkedin.com/in/jithubaiju</text>'
             f'<text x="{W-24}" y="96" class="m" font-size="11" fill="{CYAN}">jithubaiju55.github.io</text></g>')
    b.append(marks(W, H) + f'<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="8" stroke="url(#bd)" stroke-width="1.5"/>')
    open(out("cta.svg"), "w").write(svg(W, H, "".join(b), d))

if __name__ == "__main__":
    hero()
    for i, item in enumerate(LEVELS, 1): level(i, *item)
    pipeline(); questlog(); cta()
    print("built:", sorted(os.listdir(OUT)))
