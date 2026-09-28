#!/usr/bin/env python3
"""Builds hero.svg, architecture.svg, eval.svg into ../assets  (python3 scripts/build_assets.py)"""
import math, os, random
from html import escape as E

OUT = os.path.join(os.path.dirname(__file__), "..", "assets"); os.makedirs(OUT, exist_ok=True)
S = "'Inter','SF Pro Display','Segoe UI',Helvetica,Arial,sans-serif"
M = "'JetBrains Mono','SF Mono','Fira Code',ui-monospace,Menlo,Consolas,monospace"
BG, PANEL, HAIR, DIM, INK = "#05060a", "#08090d", "#23262f", "#6b7280", "#f5f5f0"
LIME, CYAN, MAG, ORG, VIO = "#c8ff2e", "#38e1ff", "#ff4fd8", "#ff9d2e", "#8b7cff"

CSS = f""".s{{font-family:{S}}}.m{{font-family:{M}}}
.f{{opacity:0;animation:in .9s cubic-bezier(.2,.8,.2,1) forwards}}
@keyframes in{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
@keyframes blink{{50%{{opacity:.2}}}}"""

def svg(w, h, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">'
            f'<defs>{defs}</defs><style>{CSS}</style>{body}</svg>')

def marks(w, h, c="#3a3f4d", i=12, s=5):
    o = ""
    for x, y in [(i, i), (w-i, i), (i, h-i), (w-i, h-i)]:
        o += f'<path d="M{x-s} {y}H{x+s}M{x} {y-s}V{y+s}" stroke="{c}"/>'
    return o

def timeline(pts):
    out, last = [], -1.0
    for t, v in pts:
        t = min(1.0, max(0.0, t))
        if t <= last: t = min(1.0, last + 1e-4)
        out.append((t, v)); last = t
    if out[0][0] != 0: out.insert(0, (0.0, out[0][1]))
    if out[-1][0] < 1: out.append((1.0, out[-1][1]))
    return ";".join(f"{t:.4f}" for t, _ in out), ";".join(str(v) for _, v in out)

def save(n, s): open(os.path.join(OUT, n), "w").write(s)

# ═════════════════════════ HERO — latent space with live k-NN retrieval ═════════════════════════
def hero():
    random.seed(11)
    W, H, DUR = 900, 440, 30
    C = [("AGENTS", LIME, (655, 118)), ("RAG", CYAN, (808, 212)), ("VISION", MAG, (612, 292)),
         ("ML", ORG, (748, 344)), ("SERVE", VIO, (470, 148))]
    d = "".join(f'<radialGradient id="c{i}"><stop offset="0" stop-color="{col}" stop-opacity=".22"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>' for i, (_, col, _) in enumerate(C))
    d += f'<linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{LIME}" stop-opacity=".55"/><stop offset=".45" stop-color="{HAIR}"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".4"/></linearGradient>'
    d += '<radialGradient id="vg" cx=".7" cy=".45" r=".8"><stop offset="0" stop-color="#0d1017"/><stop offset="1" stop-color="#05060a"/></radialGradient>'
    d += '<filter id="gw" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    b = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="6" fill="url(#vg)"/>']
    # faint contour rings
    for r in (120, 210, 300, 400):
        b.append(f'<circle cx="700" cy="230" r="{r}" stroke="#fff" stroke-opacity=".03"/>')
    # ambient scatter
    for _ in range(90):
        x, y = random.uniform(14, W-14), random.uniform(14, H-14)
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{random.uniform(.6,1.2):.1f}" fill="#fff" fill-opacity="{random.uniform(.06,.18):.2f}"/>')
    pts = []
    for i, (name, col, (cx, cy)) in enumerate(C):
        b.append(f'<circle cx="{cx}" cy="{cy}" r="105" fill="url(#c{i})"/>')
        n = 0
        while n < 56:
            x, y = random.gauss(cx, 34), random.gauss(cy, 30)
            if not (14 < x < W-14 and 14 < y < H-14) or (x < 570 and y > 255): continue
            pts.append((x, y, i)); n += 1
    for x, y, i in pts:
        col = C[i][1]; r = random.uniform(1.2, 2.5)
        tw = (f'<animate attributeName="opacity" values=".35;1;.35" dur="{random.uniform(3,7):.1f}s" begin="-{random.uniform(0,6):.1f}s" repeatCount="indefinite"/>' if random.random() < .4 else "")
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{col}" fill-opacity=".8">{tw}</circle>')
    for name, col, (cx, cy) in C:
        b.append(f'<text x="{cx}" y="{cy-64}" text-anchor="middle" class="m" font-size="10" letter-spacing="4" fill="{col}" fill-opacity=".85">{name}</text>')
    # k-NN query sequence
    for qi, (name, col, (cx, cy)) in enumerate(C):
        own = [p for p in pts if p[2] == qi]
        q = sorted(own, key=lambda p: (p[0]-cx)**2 + (p[1]-cy)**2)[len(own)*2//3]
        nn = sorted((p for p in pts if p is not q), key=lambda p: (p[0]-q[0])**2 + (p[1]-q[1])**2)[:7]
        s, e = qi / len(C), (qi + 1) / len(C)
        kt, vv = timeline([(0, 0), (s, 0), (s + .015, 1), (e - .025, 1), (e, 0), (1, 0)])
        g = [f'<g opacity="0" class="q"><animate attributeName="opacity" values="{vv}" keyTimes="{kt}" dur="{DUR}s" repeatCount="indefinite"/>']
        for p in nn:
            g.append(f'<line x1="{q[0]:.1f}" y1="{q[1]:.1f}" x2="{p[0]:.1f}" y2="{p[1]:.1f}" stroke="{col}" stroke-width="1" stroke-opacity=".85"/>'
                     f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="6.5" stroke="{col}" stroke-width="1.2" filter="url(#gw)"/>')
        g.append(f'<circle cx="{q[0]:.1f}" cy="{q[1]:.1f}" r="4" fill="#fff" filter="url(#gw)"/>')
        tx = q[0] + 12 if q[0] < 780 else q[0] - 12
        anc = "start" if q[0] < 780 else "end"
        g.append(f'<text x="{tx:.1f}" y="{q[1]-12:.1f}" text-anchor="{anc}" class="m" font-size="9" fill="{col}">query · top-7 neighbours</text></g>')
        b.append("".join(g))
        rk, rv = timeline([(0, 0), (s, 0), (s + .15, 90), (1, 90)])
        ok, ov = timeline([(0, 0), (s, 0), (s + .004, .9), (s + .15, 0), (1, 0)])
        b.append(f'<circle cx="{q[0]:.1f}" cy="{q[1]:.1f}" r="0" stroke="{col}" stroke-width="1.2" opacity="0">'
                 f'<animate attributeName="r" values="{rv}" keyTimes="{rk}" dur="{DUR}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="{ov}" keyTimes="{ok}" dur="{DUR}s" repeatCount="indefinite"/></circle>')
    # text block
    b.append(f'<g class="f"><rect x="48.5" y="36.5" width="96" height="24" rx="3" stroke="{LIME}"/>'
             f'<text x="96.5" y="52.5" text-anchor="middle" class="m" font-size="11" letter-spacing="2.5" fill="{LIME}">MODEL CARD</text>'
             f'<text x="160" y="52.5" class="m" font-size="12" fill="{DIM}">jithubaiju55 / jithu-baiju-2025</text></g>')
    b.append(f'<text x="44" y="322" class="s f" style="animation-delay:.15s" font-size="82" font-weight="800" letter-spacing="-3" fill="{INK}">Jithu <tspan fill="{LIME}">Baiju</tspan></text>')
    b.append(f'<text x="48" y="360" class="s f" style="animation-delay:.3s" font-size="19" font-weight="600" fill="{INK}">ML Engineer · AI Developer</text>'
             f'<text x="48" y="384" class="s f" style="animation-delay:.4s" font-size="14" fill="#8b909c">Agents, RAG and vision systems built to ship.</text>')
    x = 48; chips = []
    for t in ["agentic-ai", "rag", "computer-vision", "pytorch", "langchain"]:
        w = len(t) * 6.7 + 22
        chips.append(f'<rect x="{x+.5:.1f}" y="401.5" width="{w:.1f}" height="22" rx="11" stroke="#2f3340"/><text x="{x+w/2:.1f}" y="416" text-anchor="middle" class="m" font-size="10.5" fill="#a3a8b5">{t}</text>')
        x += w + 8
    b.append('<g class="f" style="animation-delay:.5s">' + "".join(chips) + '</g>')
    b.append(f'<text x="{W-24}" y="{H-18}" text-anchor="end" class="m" font-size="9" fill="#3f4451">latent space · illustrative</text>')
    b.append(f'<circle cx="{W-100}" cy="30" r="3.5" fill="{LIME}" style="animation:blink 2s infinite"/><text x="{W-88}" y="34" class="m" font-size="10" letter-spacing="2" fill="#9aa0ac">RETRIEVING</text>')
    b.append(marks(W, H) + f'<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="6" stroke="url(#bd)" stroke-width="1.5"/>')
    save("hero.svg", svg(W, H, "".join(b), d))

# ═════════════════════════ ARCHITECTURE — forward pass ═════════════════════════
def architecture():
    W, H = 852, 352
    cols = [("01", "DATA", "ingest · clean · store", LIME, ["NumPy · Pandas", "Matplotlib", "PostgreSQL · MySQL", "SQLite · Power BI"]),
            ("02", "REPRESENT", "learn features", CYAN, ["PyTorch", "TensorFlow", "scikit-learn", "OpenCV"]),
            ("03", "REASON", "agents · retrieval", MAG, ["LangChain", "Ollama", "Hugging Face", "Groq API"]),
            ("04", "SERVE", "ship it", ORG, ["FastAPI", "Spring Boot", "Streamlit", "AWS"])]
    cw = 180; gap = (W - 4 * cw) / 3
    d = '<filter id="gw" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    b = []
    # skip connection
    x1, x4 = cw / 2, 3 * (cw + gap) + cw / 2
    path = f"M{x1:.1f},80 V52 Q{x1:.1f},38 {x1+14:.1f},38 H{x4-14:.1f} Q{x4:.1f},38 {x4:.1f},52 V80"
    b.append(f'<path d="{path}" stroke="{LIME}" stroke-opacity=".5" stroke-dasharray="4 5"><animate attributeName="stroke-dashoffset" from="18" to="0" dur="1.4s" repeatCount="indefinite"/></path>')
    b.append(f'<rect x="{W/2-118:.1f}" y="28" width="236" height="20" fill="{BG}"/><text x="{W/2}" y="42" text-anchor="middle" class="m" font-size="10" letter-spacing="2" fill="{LIME}">SKIP CONNECTION · PROTOTYPE → DEPLOY</text>')
    b.append(f'<circle r="3" fill="{LIME}" filter="url(#gw)"><animateMotion path="{path}" dur="5s" repeatCount="indefinite"/></circle>')
    # main flow line
    b.append(f'<path d="M0 186H{W}" stroke="{HAIR}" stroke-dasharray="2 5"/>')
    DUR = 9
    for i, (n, t, sub, col, items) in enumerate(cols):
        x = i * (cw + gap); xc = x + cw / 2; f = xc / W
        kt, vv = timeline([(0, HAIR), (f - .07, HAIR), (f, col), (f + .07, HAIR), (1, HAIR)])
        b.append(f'<g class="f" style="animation-delay:{i*.15}s"><g transform="translate({x:.1f},80)">'
                 f'<rect x=".5" y=".5" width="{cw-1}" height="216" rx="3" fill="{PANEL}" stroke="{HAIR}"><animate attributeName="stroke" values="{vv}" keyTimes="{kt}" dur="{DUR}s" repeatCount="indefinite"/></rect>'
                 f'<text x="18" y="38" class="m" font-size="24" font-weight="700" fill="{col}">{n}</text>'
                 f'<text x="18" y="62" class="s" font-size="15" font-weight="700" letter-spacing="1.5" fill="{INK}">{t}</text>'
                 f'<text x="18" y="80" class="m" font-size="10" fill="{DIM}">{E(sub)}</text><line x1="18" y1="94" x2="{cw-18}" y2="94" stroke="{HAIR}"/>')
        for k, it in enumerate(items):
            y = 122 + k * 28
            b.append(f'<rect x="18" y="{y-9}" width="6" height="6" fill="{col}" fill-opacity=".9"/><text x="34" y="{y-1}" class="s" font-size="13" fill="#d4d4d0">{E(it)}</text>')
        b.append('</g></g>')
        if i < 3:
            ax = x + cw + 6
            b.append(f'<path d="M{ax:.1f} 186H{ax+gap-18:.1f}m-6-5l6 5-6 5" stroke="{col}" stroke-opacity=".8"/>')
    b.append(f'<circle r="3.5" fill="#fff" filter="url(#gw)" cy="0"><animateMotion path="M0,186 H{W}" dur="{DUR}s" repeatCount="indefinite"/></circle>')
    b.append(f'<text x="0" y="334" class="m" font-size="10" letter-spacing="2" fill="{LIME}">BACKBONE</text><text x="88" y="334" class="s" font-size="13" fill="#d4d4d0">Python · C · Go · Java</text>')
    b.append(f'<text x="{W}" y="334" text-anchor="end" class="m" font-size="10" fill="{DIM}">forward pass →</text>')
    body = (f'<rect x=".5" y=".5" width="{W+47}" height="{H+40}" rx="6" fill="{BG}" stroke="{HAIR}"/>' + marks(W+48, H+41) +
            f'<g transform="translate(24,22)">' + "".join(b) + '</g>')
    save("architecture.svg", svg(W+48, H+41, body, d))

# ═════════════════════════ EVAL — dials ═════════════════════════
def evaluation():
    W, H = 900, 262
    items = [("01", "Employee Attrition", "RANDOM FOREST · HR DATA", "ACCURACY", "82%", .82, LIME),
             ("02", "Road Damage", "RESNET18 · PYTORCH", "TEST ACCURACY", "80%", .80, CYAN),
             ("03", "Research Agent", "REACT · LLAMA 3.3 70B", "LESS RESEARCH TIME", "~70%", .70, MAG),
             ("04", "Local RAG Chatbot", "OLLAMA · SQLITE · SSE", "RESPONSE LATENCY", "<2s", None, ORG)]
    pw = 210; gap = (W - 4 * pw) / 3; r = 46; C = 2 * math.pi * r
    b = []
    for i, (n, t, sub, met, val, frac, col) in enumerate(items):
        x = i * (pw + gap); cx, cy = pw / 2, 96
        g = [f'<g class="f" style="animation-delay:{i*.13}s"><g transform="translate({x:.1f},0)">',
             f'<rect x=".5" y=".5" width="{pw-1}" height="{H-1}" rx="3" fill="{PANEL}" stroke="{HAIR}"/>{marks(pw, H, i=10, s=4)}',
             f'<text x="18" y="30" class="m" font-size="10" letter-spacing="2.5" fill="{col}">EVAL {n}</text>',
             f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{HAIR}" stroke-width="5"/>']
        if frac is not None:
            g.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{col}" stroke-width="5" stroke-linecap="round" stroke-dasharray="0 {C:.1f}" transform="rotate(-90 {cx} {cy})">'
                     f'<animate attributeName="stroke-dasharray" from="0 {C:.1f}" to="{frac*C:.1f} {C:.1f}" dur="1.6s" begin=".4s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1"/></circle>')
        else:
            for k in range(12):
                a = k * 30 * math.pi / 180
                g.append(f'<line x1="{cx+(r-9)*math.sin(a):.1f}" y1="{cy-(r-9)*math.cos(a):.1f}" x2="{cx+(r-3)*math.sin(a):.1f}" y2="{cy-(r-3)*math.cos(a):.1f}" stroke="{col}" stroke-opacity=".7"/>')
            g.append(f'<g><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="2s" repeatCount="indefinite"/>'
                     f'<circle cx="{cx}" cy="{cy-r}" r="5" fill="{col}" filter="url(#gw)"/></g>')
        g.append(f'<text x="{cx}" y="{cy+10}" text-anchor="middle" class="s" font-size="28" font-weight="800" fill="{INK}">{E(val)}</text>')
        g.append(f'<text x="{cx}" y="182" text-anchor="middle" class="s" font-size="15" font-weight="700" fill="{INK}">{E(t)}</text>'
                 f'<text x="{cx}" y="203" text-anchor="middle" class="m" font-size="9.5" fill="{DIM}">{E(sub)}</text>'
                 f'<text x="{cx}" y="232" text-anchor="middle" class="m" font-size="10" letter-spacing="1.5" fill="{col}">{E(met)}</text>')
        g.append('</g></g>')
        b.append("".join(g))
    d = '<filter id="gw" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    save("eval.svg", svg(W, H, "".join(b), d))

if __name__ == "__main__":
    hero(); architecture(); evaluation(); print(sorted(os.listdir(OUT)))