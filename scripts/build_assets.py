#!/usr/bin/env python3
"""Static SVGs for the status-page profile: banner, 8 service rows, flow, changelog, cta.
Run: python3 scripts/build_assets.py"""
import os
from html import escape as E

OUT = os.path.join(os.path.dirname(__file__), "..", "assets"); os.makedirs(OUT, exist_ok=True)
S = "'Inter','SF Pro Display','Segoe UI',Helvetica,Arial,sans-serif"
M = "'JetBrains Mono','SF Mono','Fira Code',ui-monospace,Menlo,Consolas,monospace"
BG, ROW, HAIR, DIM, INK = "#08090b", "#0d0f13", "#20242f", "#7d8494", "#f2f4f8"
GREEN, BLUE, AMBER, VIOLET, RED = "#22e07a", "#3b9dff", "#ffb340", "#a78bff", "#ff5c5c"

CSS = (f".s{{font-family:{S}}}.m{{font-family:{M}}}"
       ".f{opacity:0;animation:in .7s cubic-bezier(.2,.8,.2,1) forwards}"
       "@keyframes in{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:none}}"
       "@keyframes pulse{0%{transform:scale(.85);opacity:.9}70%,100%{transform:scale(2.6);opacity:0}}"
       "@keyframes blink{50%{opacity:.35}}")

def svg(w, h, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">'
            f'<defs>{defs}</defs><style>{CSS}</style>{body}</svg>')
def save(n, s): open(os.path.join(OUT, n), "w").write(s)
def status_dot(x, y, col, r=5):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" fill-opacity=".28"><animate attributeName="transform" additive="sum" values="1;1" dur="1s"/></circle>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{col}" style="transform-origin:{x}px {y}px;animation:pulse 2.4s ease-out infinite" stroke-width="1.3"/>'
            f'<circle cx="{x}" cy="{y}" r="{r-1.6}" fill="{col}"/>')
def sparkline(x, y, w, h, seed, col, delay=0):
    import random; random.seed(seed)
    n = 28; v = 50.0; pts = []
    for i in range(n):
        v += random.uniform(-14, 16); v = max(6, min(94, v))
        pts.append((x + i * w / (n - 1), y + h - v / 100 * h))
    d = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    area = f"{d} L{pts[-1][0]:.1f},{y+h} L{pts[0][0]:.1f},{y+h} Z"
    return (f'<path d="{area}" fill="{col}" fill-opacity=".08"/>'
            f'<path d="{d}" pathLength="1" stroke="{col}" stroke-width="1.6" stroke-linejoin="round" stroke-dasharray="1" stroke-dashoffset="1">'
            f'<animate attributeName="stroke-dashoffset" from="1" to="0" dur="1.6s" begin="{delay:.2f}s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".25 .8 .3 1"/></path>'
            f'<circle cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r="2.6" fill="{col}"/>')

# ═════════════ 00 · BANNER ═════════════
def banner():
    W, H = 900, 210
    d = (f'<linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity=".45"/><stop offset=".5" stop-color="{HAIR}"/><stop offset="1" stop-color="{BLUE}" stop-opacity=".35"/></linearGradient>'
         f'<radialGradient id="gg" cx="0" cy="0" r=".8"><stop offset="0" stop-color="{GREEN}" stop-opacity=".13"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></radialGradient>'
         f'<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" stroke="#fff" stroke-opacity=".025"/></pattern>')
    b = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="8" fill="{BG}"/>',
         f'<rect width="{W}" height="{H}" fill="url(#grid)" rx="8"/><rect width="{W}" height="{H}" fill="url(#gg)" rx="8"/>']
    b.append(f'<g class="f">{status_dot(48, 42, GREEN)}'
             f'<text x="66" y="47" class="m" font-size="13" font-weight="700" letter-spacing="1" fill="{GREEN}">ALL SYSTEMS OPERATIONAL</text>'
             f'<text x="{W-24}" y="47" text-anchor="end" class="m" font-size="11" fill="{DIM}">auto-updated · github actions</text></g>')
    b.append(f'<text x="47" y="130" class="s f" style="animation-delay:.12s" font-size="64" font-weight="800" letter-spacing="-2.5" fill="{INK}">Jithu Baiju</text>')
    b.append(f'<text x="48" y="160" class="s f" style="animation-delay:.24s" font-size="16" fill="#a8adba">Software engineer running 8 services in production — agents, dev tools, ML and full-stack apps.</text>')
    ch = [("30+", "repositories", GREEN), ("2", "PyPI packages", BLUE), ("6", "AI agent systems", VIOLET), ("Kerala, IN", "based in", AMBER)]
    x = 48
    for v, l, c in ch:
        b.append(f'<g class="f" style="animation-delay:.36s"><text x="{x}" y="192" class="s" font-size="15" font-weight="700" fill="{INK}">{E(v)}<tspan class="m" font-size="10.5" font-weight="400" fill="{DIM}">  {E(l)}</tspan></text></g>')
        x += (len(v) + len(l)) * 7.6 + 46
    b.append(f'<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="8" stroke="url(#bd)" stroke-width="1.5"/>')
    save("banner.svg", svg(W, H, "".join(b), d))

# ═════════════ 01 · SERVICE ROWS ═════════════
SERVICES = [
    ("neuralhive", "neuralhive", "Free offline AI coding agent — runs 70B+ models on ordinary laptops.", "OPERATIONAL", GREEN, "local", "offline-first"),
    ("AgenticFuzzer", "agentic-fuzzer", "Self-evolving swarm fuzzer — agents evolve their own mutation strategies.", "OPERATIONAL", GREEN, "swarm", "agents"),
    ("ClinicalAgent", "clinical-agent", "Six specialised agents analyse cases and check drug interactions.", "OPERATIONAL", GREEN, "6", "agents"),
    ("AI-Researcher", "ai-researcher", "ReAct agent that runs multi-step web research and writes reports.", "OPERATIONAL", GREEN, "70%", "less research time"),
    ("RagKB", "rag-kb", "Fully local RAG chatbot — SSE streaming, zero external APIs.", "OPERATIONAL", GREEN, "<2s", "p95 latency"),
    ("openenv-project", "sql-repair-env", "RL environment where agents learn to diagnose and repair broken SQL.", "BETA", AMBER, "20", "tasks"),
    ("lazyload", "lazyload · pypi", "Defers heavy imports until first use for instant startup. Zero config.", "PUBLISHED", BLUE, "pip", "install lazyload"),
    ("pytrace-live", "pytrace-live", "Traces Python execution live and flags slow functions as your code runs.", "PUBLISHED", BLUE, "cli", "install pytrace-live"),
]
def services():
    W, H = 900, 92
    for i, (repo, slug, desc, tag, col, met, metl) in enumerate(SERVICES, 1):
        d = f'<linearGradient id="sw"><stop offset="0" stop-color="{col}" stop-opacity="0"/><stop offset=".5" stop-color="{col}" stop-opacity=".07"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></linearGradient><clipPath id="rc"><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="7"/></clipPath>'
        b = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="7" fill="{ROW}" stroke="{HAIR}"/>',
             f'<g clip-path="url(#rc)"><rect x="-260" y="0" width="260" height="{H}" fill="url(#sw)"><animateTransform attributeName="transform" type="translate" from="0 0" to="1500 0" dur="10s" begin="{i*1.1:.1f}s" repeatCount="indefinite"/></rect></g>']
        b.append(status_dot(34, H/2, col, 4.5))
        b.append(f'<text x="56" y="30" class="s" font-size="17" font-weight="800" fill="{INK}">{E(slug)}</text>'
                 f'<text x="56" y="52" class="s" font-size="12.5" fill="#9aa0ab" textLength="480" lengthAdjust="spacingAndGlyphs">{E(desc)}</text>')
        b.append(sparkline(56, 62, 190, 22, hash(repo) % 9973, col, delay=i*.05))
        mx = 560
        b.append(f'<text x="{mx}" y="38" class="s" font-size="22" font-weight="800" fill="{col}">{E(met)}</text>'
                 f'<text x="{mx}" y="55" class="m" font-size="9" letter-spacing="1" fill="{DIM}">{E(metl.upper())}</text>')
        bw = len(tag) * 6.6 + 22
        bx = mx + 118
        b.append(f'<rect x="{bx:.1f}" y="18" width="{bw:.1f}" height="22" rx="11" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".5"/>'
                 f'<text x="{bx+bw/2:.1f}" y="33" text-anchor="middle" class="m" font-size="10" letter-spacing="1" fill="{col}">{E(tag)}</text>')
        b.append(f'<text x="{bx:.1f}" y="55" class="m" font-size="10" fill="{DIM}">github.com/jithubaiju55/</text>'
                 f'<text x="{bx:.1f}" y="68" class="m" font-size="10" fill="{col}">{E(repo)} ↗</text>')
        save(f"svc-{i}.svg", svg(W, H, f'<g class="f" style="animation-delay:{i*.04}s">' + "".join(b) + '</g>', d))

# ═════════════ 02 · REQUEST FLOW ═════════════
def flow():
    W, H = 900, 210
    stages = [("CLIENT", "browser / cli", DIM), ("GATEWAY", "FastAPI · Spring Boot", BLUE), ("ORCHESTRATOR", "LangChain · LangGraph", VIOLET), ("MODEL", "Llama 3.3 · PyTorch", GREEN), ("DATA", "SQLite · Postgres · Chroma", AMBER)]
    n = len(stages); bw = 148; gap = (W - n * bw) / (n - 1)
    xs = [i * (bw + gap) for i in range(n)]
    cy = 108
    d = '<filter id="gw" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    b = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="8" fill="{BG}" stroke="{HAIR}"/>',
         f'<text x="24" y="30" class="m" font-size="10" letter-spacing="2.5" fill="{GREEN}">REQUEST FLOW</text>',
         f'<text x="{W-24}" y="30" text-anchor="end" class="m" font-size="10" fill="{DIM}">how a request moves through what I build</text>']
    for x in xs[:-1]:
        b.append(f'<line x1="{x+bw:.1f}" y1="{cy}" x2="{x+bw+gap:.1f}" y2="{cy}" stroke="{HAIR}"/>')
    for i, (x, (name, sub, col)) in enumerate(zip(xs, stages)):
        b.append(f'<g class="f" style="animation-delay:{i*.1}s"><rect x="{x+.5:.1f}" y="{cy-32}" width="{bw-1:.1f}" height="64" rx="6" fill="{ROW}" stroke="{col}" stroke-opacity=".55"/>'
                 f'<text x="{x+bw/2:.1f}" y="{cy-6}" text-anchor="middle" class="m" font-size="11.5" font-weight="700" letter-spacing="1" fill="{col if col!=DIM else INK}">{E(name)}</text>'
                 f'<text x="{x+bw/2:.1f}" y="{cy+14}" text-anchor="middle" class="m" font-size="9.5" fill="{DIM}">{E(sub)}</text></g>')
    full_x = f"M{xs[0]+bw/2:.1f},{cy} " + " ".join(f"L{x+bw/2:.1f},{cy}" for x in xs[1:])
    for k, delay in enumerate([0, 2.6, 5.2]):
        b.append(f'<circle r="3.6" fill="#fff" filter="url(#gw)"><animateMotion path="{full_x}" dur="7.8s" begin="{delay}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.04;.93;1" dur="7.8s" begin="{delay}s" repeatCount="indefinite"/></circle>')
    b.append(f'<text x="24" y="{H-18}" class="m" font-size="10" fill="{DIM}">e.g. ClinicalAgent · AI-Researcher · RagKB all follow this shape</text>')
    save("flow.svg", svg(W, H, "".join(b), d))

# ═════════════ 03 · CHANGELOG ═════════════
LOG = [
    ("2024", "Q4", "Shipped first dev tools", "Code editor, calculator, JSON validator, auto-commenter — learning by building small, sharp utilities.", DIM),
    ("2025", "Q3–Q4", "Moved into machine learning", "Classification and prediction projects: attrition, student performance, road-damage detection.", BLUE),
    ("2026", "Q1–Q2", "Started building agents", "ClinicalAgent, AI-Researcher, an RL environment for SQL repair, and a swarm fuzzer that evolves its own strategy.", VIOLET),
    ("2026", "Q3", "Shipped to PyPI", "lazyload and pytrace-live — developer tools published for anyone to install.", GREEN),
]
def changelog():
    W, H = 900, 258
    d = '<filter id="gw" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="1.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    b = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="8" fill="{BG}" stroke="{HAIR}"/>',
         f'<text x="24" y="34" class="m" font-size="10" letter-spacing="2.5" fill="{GREEN}">CHANGELOG</text>',
         f'<text x="{W-24}" y="34" text-anchor="end" class="m" font-size="10" fill="{DIM}">real repository history</text>',
         f'<line x1="98" y1="56" x2="98" y2="{H-24}" stroke="{HAIR}"/>']
    rowh = (H - 70) / len(LOG)
    for i, (yr, q, title, desc, col) in enumerate(LOG):
        y = 66 + i * rowh
        b.append(f'<g class="f" style="animation-delay:{i*.12}s">'
                 f'<text x="24" y="{y+5}" class="m" font-size="11" font-weight="700" fill="{INK}">{yr}</text>'
                 f'<text x="24" y="{y+19}" class="m" font-size="9.5" fill="{DIM}">{q}</text>'
                 f'<circle cx="98" cy="{y}" r="4.5" fill="{BG}" stroke="{col}" stroke-width="2"/><circle cx="98" cy="{y}" r="2" fill="{col}" filter="url(#gw)"/>'
                 f'<text x="120" y="{y+4}" class="s" font-size="15" font-weight="700" fill="{INK}">{E(title)}</text>'
                 f'<text x="120" y="{y+23}" class="s" font-size="12" fill="#9aa0ab">{E(desc)}</text></g>')
    save("changelog.svg", svg(W, H, "".join(b), d))

# ═════════════ 04 · CTA ═════════════
def cta():
    W, H = 900, 150
    d = (f'<radialGradient id="gg" cx=".08" cy="0" r="1"><stop offset="0" stop-color="{GREEN}" stop-opacity=".14"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></radialGradient>'
         f'<linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity=".5"/><stop offset="1" stop-color="{HAIR}"/></linearGradient>')
    b = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="8" fill="{BG}"/><rect width="{W}" height="{H}" rx="8" fill="url(#gg)"/>']
    b.append(f'<g class="f">{status_dot(48, 52, GREEN)}<text x="66" y="57" class="m" font-size="11" letter-spacing="2" fill="{GREEN}">OPEN TO NEW DEPLOYMENTS</text></g>')
    b.append(f'<text x="47" y="98" class="s f" style="animation-delay:.12s" font-size="30" font-weight="800" fill="{INK}">Got something worth building?</text>')
    b.append(f'<text x="47" y="134" class="s f" style="animation-delay:.2s" font-size="30" font-weight="800" fill="{GREEN}">Let&#8217;s ship it.</text>')
    b.append(f'<g class="f" style="animation-delay:.32s"><text x="{W-24}" y="98" text-anchor="end" class="m" font-size="11" fill="#a8adba">jithubaiju124@gmail.com</text>'
             f'<text x="{W-24}" y="118" text-anchor="end" class="m" font-size="11" fill="{GREEN}">linkedin.com/in/jithubaiju</text>'
             f'<text x="{W-24}" y="138" text-anchor="end" class="m" font-size="11" fill="{GREEN}">jithubaiju55.github.io</text></g>')
    b.append(f'<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="8" stroke="url(#bd)" stroke-width="1.5"/>')
    save("cta.svg", svg(W, H, "".join(b), d))

if __name__ == "__main__":
    banner(); services(); flow(); changelog(); cta()
    print(sorted(os.listdir(OUT)))
