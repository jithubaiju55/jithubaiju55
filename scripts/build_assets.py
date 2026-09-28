#!/usr/bin/env python3
"""Builds the static bento SVGs (hero, about, stack, 4 project cards) into ../assets."""
import os
from html import escape as E

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUT, exist_ok=True)
S = "'Inter','SF Pro Display','Segoe UI',system-ui,-apple-system,sans-serif"
M = "'JetBrains Mono','Fira Code',ui-monospace,Menlo,Consolas,monospace"
BG, CARD, LINE = "#06070b", "#0b0d13", "#1c2030"
TEAL, INDIGO, PINK, AMBER = "#5eead4", "#818cf8", "#f472b6", "#fbbf24"

CSS = f""".s{{font-family:{S}}}.m{{font-family:{M}}}
.f{{opacity:0;animation:in .8s cubic-bezier(.2,.8,.2,1) forwards}}
@keyframes in{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}"""

def svg(w, h, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">'
            f'<defs>{defs}</defs><style>{CSS}</style>{body}</svg>')

def save(name, s):
    open(os.path.join(OUT, name), "w").write(s)

def frame(w, h, accent, r=22):
    return (f'<rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="{r}" fill="{CARD}" stroke="url(#bd)" stroke-width="1.5"/>'
            f'<rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="{r}" fill="url(#gl)"/>')

def frame_defs(accent):
    return (f'<linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{accent}" stop-opacity=".7"/><stop offset=".6" stop-color="{LINE}"/></linearGradient>'
            f'<radialGradient id="gl" cx="0" cy="0" r="1"><stop offset="0" stop-color="{accent}" stop-opacity=".13"/><stop offset=".7" stop-color="{accent}" stop-opacity="0"/></radialGradient>')

# ───────────────────────── HERO ─────────────────────────
def hero():
    W, H = 900, 300
    cx, cy = 730, 150
    d = f'''<linearGradient id="nm" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff"/><stop offset=".55" stop-color="{TEAL}"/><stop offset="1" stop-color="{INDIGO}"/></linearGradient>
<linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{TEAL}" stop-opacity=".6"/><stop offset=".5" stop-color="{LINE}"/><stop offset="1" stop-color="{PINK}" stop-opacity=".5"/></linearGradient>
<filter id="bl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="55"/></filter>
<pattern id="gr" width="34" height="34" patternUnits="userSpaceOnUse"><path d="M34 0H0V34" stroke="#fff" stroke-opacity=".035"/></pattern>
<clipPath id="cp"><rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="24"/></clipPath>
<filter id="gw" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'''
    b = [f'<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="24" fill="{BG}"/><g clip-path="url(#cp)">',
         f'<g filter="url(#bl)" opacity=".55"><circle cx="120" cy="40" r="110" fill="{TEAL}" opacity=".55"><animate attributeName="cx" values="120;230;120" dur="14s" repeatCount="indefinite"/></circle>'
         f'<circle cx="470" cy="300" r="120" fill="{INDIGO}" opacity=".6"><animate attributeName="cy" values="300;240;300" dur="11s" repeatCount="indefinite"/></circle>'
         f'<circle cx="800" cy="30" r="100" fill="{PINK}" opacity=".4"><animate attributeName="cx" values="800;700;800" dur="16s" repeatCount="indefinite"/></circle></g>',
         f'<rect width="{W}" height="{H}" fill="url(#gr)"/></g>',
         f'<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="24" stroke="url(#bd)" stroke-width="1.5"/>']
    b.append(f'<g class="f" style="animation-delay:.1s"><rect x="48" y="46" width="290" height="30" rx="15" fill="#ffffff" fill-opacity=".05" stroke="#ffffff" stroke-opacity=".1"/>'
             f'<circle cx="67" cy="61" r="4" fill="{TEAL}" style="animation:pulse 2s infinite"/>'
             f'<text x="80" y="65" class="m" font-size="11" fill="#cbd5e1">Exploring production-grade LLM apps</text></g>')
    b.append(f'<text x="48" y="134" class="m f" style="animation-delay:.25s" font-size="12" letter-spacing="3.5" fill="{TEAL}">ML ENGINEER  ·  AI DEVELOPER</text>')
    b.append(f'<text x="46" y="212" class="s f" style="animation-delay:.4s" font-size="78" font-weight="800" letter-spacing="-3" fill="url(#nm)">Jithu Baiju</text>')
    b.append(f'<text x="48" y="252" class="s f" style="animation-delay:.6s" font-size="17" fill="#94a3b8">Agents, RAG systems and vision models — built to ship.</text>')
    # orbit
    for r, dash in [(62, "2 6"), (102, "2 8"), (136, "2 10")]:
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="#fff" stroke-opacity=".12" stroke-dasharray="{dash}"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="22" fill="{TEAL}" fill-opacity=".12" stroke="{TEAL}" stroke-opacity=".6"/>'
             f'<circle cx="{cx}" cy="{cy}" r="7" fill="{TEAL}" filter="url(#gw)"><animate attributeName="r" values="6;9;6" dur="3s" repeatCount="indefinite"/></circle>')
    def orbit(r, label, dur, off, col):
        p = f"M{cx+r},{cy} a{r},{r} 0 1,1 {-2*r},0 a{r},{r} 0 1,1 {2*r},0"
        return (f'<g><animateMotion path="{p}" dur="{dur}s" begin="-{off}s" repeatCount="indefinite"/>'
                f'<circle r="5" fill="{col}" filter="url(#gw)"/><text x="10" y="4" class="m" font-size="10" letter-spacing="1" fill="#e2e8f0">{label}</text></g>')
    b += [orbit(62, "RAG", 14, 0, TEAL), orbit(102, "AGENTS", 24, 0, INDIGO), orbit(102, "VISION", 24, 12, PINK), orbit(136, "LLM", 34, 6, AMBER)]
    save("hero.svg", svg(W, H, "".join(b), d))

# ───────────────────────── ABOUT ─────────────────────────
def about():
    W, H = 900, 176
    d = frame_defs(TEAL).replace('id="bd"', 'id="bd"')
    cards = [(0, 440), (460, 210), (690, 210)]
    b = []
    def card(x, w, i, inner):
        b.append(f'<g class="f" style="animation-delay:{i*.12}s"><svg x="{x}" y="0" width="{w}" height="{H}" viewBox="0 0 {w} {H}">{frame(w,H,TEAL)}{inner}</svg></g>')
    items = [("Agentic AI", "multi-step reasoning agents"), ("RAG", "local, low-latency retrieval"),
             ("Computer Vision", "from dataset to deployment"), ("GenAI", "LLM-powered applications")]
    inner = f'<text x="26" y="38" class="m" font-size="10" letter-spacing="2.5" fill="{TEAL}">WHAT I BUILD</text>'
    for i, (a, t) in enumerate(items):
        y = 70 + i * 26
        inner += f'<circle cx="30" cy="{y-4}" r="3" fill="{TEAL}"/><text x="44" y="{y}" class="s" font-size="14" fill="#e2e8f0" font-weight="600">{a}<tspan fill="#64748b" font-weight="400">  {t}</tspan></text>'
    card(0, 440, 0, inner)
    card(460, 210, 1, f'<text x="24" y="38" class="m" font-size="10" letter-spacing="2.5" fill="{INDIGO}">BASED IN</text>'
         f'<text x="24" y="92" class="s" font-size="34" font-weight="800" fill="#f1f5f9">Kerala</text>'
         f'<text x="24" y="122" class="s" font-size="13" fill="#94a3b8">India</text>'
         f'<text x="24" y="148" class="s" font-size="13" fill="#64748b">B.Sc. CS · Class of 2025</text>')
    card(690, 210, 2, f'<text x="24" y="38" class="m" font-size="10" letter-spacing="2.5" fill="{PINK}">CURRENTLY</text>'
         f'<text x="24" y="86" class="s" font-size="26" font-weight="800" fill="#f1f5f9">Exploring</text>'
         f'<text x="24" y="116" class="s" font-size="13" fill="#94a3b8">production-grade</text>'
         f'<text x="24" y="136" class="s" font-size="13" fill="#94a3b8">LLM applications</text>')
    save("about.svg", svg(W, H, "".join(b), d))

# ───────────────────────── STACK MARQUEE ─────────────────────────
def stack():
    W, H = 900, 122
    row1 = [("Python", TEAL), ("PyTorch", "#f97316"), ("TensorFlow", AMBER), ("scikit-learn", AMBER), ("OpenCV", INDIGO), ("NumPy", INDIGO),
            ("Pandas", INDIGO), ("LangChain", TEAL), ("Ollama", "#e2e8f0"), ("Hugging Face", AMBER), ("Groq", "#f97316")]
    row2 = [("FastAPI", TEAL), ("Spring Boot", "#4ade80"), ("Streamlit", PINK), ("PostgreSQL", INDIGO), ("MySQL", INDIGO), ("SQLite", "#38bdf8"),
            ("AWS", AMBER), ("Linux", "#e2e8f0"), ("Git", "#f97316"), ("Power BI", AMBER), ("C", "#38bdf8"), ("Go", TEAL), ("Java", "#f97316")]
    def seq(items):
        x, out = 0, []
        for n, c in items:
            w = 46 + len(n) * 7.4
            out.append(f'<rect x="{x:.1f}" y="0" width="{w:.1f}" height="36" rx="18" fill="#0d1017" stroke="{LINE}"/>'
                       f'<circle cx="{x+20:.1f}" cy="18" r="4" fill="{c}"/><text x="{x+32:.1f}" y="23" class="s" font-size="13" fill="#cbd5e1">{E(n)}</text>')
            x += w + 12
        return "".join(out), x
    b = []
    for i, (items, y, rev, dur) in enumerate([(row1, 12, False, 46), (row2, 66, True, 52)]):
        s, T = seq(items)
        a = f'from="{-T:.1f} 0" to="0 0"' if rev else f'from="0 0" to="{-T:.1f} 0"'
        b.append(f'<g transform="translate(0,{y})"><g><animateTransform attributeName="transform" type="translate" {a} dur="{dur}s" repeatCount="indefinite"/>'
                 f'{s}<g transform="translate({T:.1f},0)">{s}</g><g transform="translate({2*T:.1f},0)">{s}</g></g></g>')
    d = f'<linearGradient id="mg"><stop offset="0" stop-color="#000"/><stop offset=".1" stop-color="#fff"/><stop offset=".9" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient><mask id="mk"><rect width="{W}" height="{H}" fill="url(#mg)"/></mask>'
    save("stack.svg", svg(W, H, f'<g mask="url(#mk)">{"".join(b)}</g>', d))

# ───────────────────────── PROJECT CARDS ─────────────────────────
def project(n, accent, cat, title, desc, metric, mlabel, tags, visual):
    W, H = 440, 250
    b = [frame(W, H, accent),
         f'<text x="24" y="40" class="m" font-size="10" letter-spacing="2.5" fill="{accent}">{cat}</text>'
         f'<text x="{W-24}" y="40" text-anchor="end" class="m" font-size="11" fill="#334155">0{n}</text>'
         f'<text x="24" y="76" class="s" font-size="22" font-weight="700" fill="#f1f5f9">{E(title)}</text>']
    for i, l in enumerate(desc):
        b.append(f'<text x="24" y="{102+i*19}" class="s" font-size="13" fill="#94a3b8">{E(l)}</text>')
    b.append(f'<text x="24" y="184" class="s" font-size="38" font-weight="800" fill="{accent}">{E(metric)}</text>'
             f'<text x="25" y="202" class="m" font-size="10" letter-spacing="1.5" fill="#64748b">{E(mlabel)}</text>')
    x = 24
    for t in tags:
        w = len(t) * 6.6 + 20
        b.append(f'<rect x="{x}" y="212" width="{w:.1f}" height="24" rx="12" fill="{accent}" fill-opacity=".08" stroke="{accent}" stroke-opacity=".3"/>'
                 f'<text x="{x+w/2:.1f}" y="228" text-anchor="middle" class="m" font-size="10.5" fill="{accent}">{E(t)}</text>')
        x += w + 8
    b.append(visual)
    save(f"project-{n}.svg", svg(W, H, "".join(b), frame_defs(accent)))

def v_agent(c):
    xs = [268, 314, 360, 406]; labs = ["plan", "search", "read", "report"]
    o = f'<line x1="{xs[0]}" y1="160" x2="{xs[-1]}" y2="160" stroke="{c}" stroke-opacity=".3" stroke-dasharray="3 4"/>'
    for i, (x, l) in enumerate(zip(xs, labs)):
        o += (f'<circle cx="{x}" cy="160" r="8" fill="{CARD}" stroke="{c}" stroke-width="2"><animate attributeName="fill" values="{CARD};{c};{CARD}" dur="4s" begin="{i}s" repeatCount="indefinite"/></circle>'
              f'<text x="{x}" y="186" text-anchor="middle" class="m" font-size="9" fill="#64748b">{l}</text>')
    return o + f'<circle r="3" fill="#fff"><animateMotion path="M{xs[0]},160 L{xs[-1]},160" dur="4s" repeatCount="indefinite"/></circle>'

def v_rag(c):
    o = ""
    for i in range(3):
        o += f'<rect x="{254+i*4}" y="{150-i*4}" width="22" height="28" rx="3" fill="{CARD}" stroke="{c}" stroke-opacity="{.4+i*.25}"/>'
    o += f'<path d="M292 164h22m-6-5l6 5-6 5" stroke="{c}" stroke-opacity=".6"/>'
    hot = {(1, 1), (2, 3), (3, 2)}
    for r in range(4):
        for k in range(5):
            x, y = 330 + k * 17, 148 + r * 14
            if (r, k) in hot:
                o += f'<circle cx="{x}" cy="{y}" r="4" fill="{c}"><animate attributeName="r" values="3;5.5;3" dur="2.4s" begin="{r*.3}s" repeatCount="indefinite"/></circle>'
            else:
                o += f'<circle cx="{x}" cy="{y}" r="2.5" fill="{c}" fill-opacity=".25"/>'
    return o

def v_road(c):
    o = ""
    for i, (l, v) in enumerate([("crack", 70), ("pothole", 38), ("normal", 118)]):
        y = 148 + i * 18
        o += (f'<text x="252" y="{y+8}" class="m" font-size="9" fill="#64748b">{l}</text><rect x="304" y="{y}" width="120" height="9" rx="4.5" fill="#141824"/>'
              f'<rect x="304" y="{y}" width="0" height="9" rx="4.5" fill="{c}"><animate attributeName="width" from="0" to="{v}" dur="1.4s" begin="{.3+i*.25}s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1"/></rect>')
    return o

def v_attr(c):
    o = ""
    for i, h in enumerate([50, 40, 31, 22, 15, 10]):
        x = 292 + i * 20
        o += (f'<rect x="{x}" y="194" width="12" height="0" rx="3" fill="{c}" fill-opacity="{1-i*.13:.2f}"><animate attributeName="height" from="0" to="{h}" dur="1.2s" begin="{.3+i*.12}s" fill="freeze"/>'
              f'<animate attributeName="y" from="194" to="{194-h}" dur="1.2s" begin="{.3+i*.12}s" fill="freeze"/></rect>')
    return o + f'<text x="292" y="207" class="m" font-size="9" fill="#64748b" style="display:none">importance</text>'

def projects():
    project(1, TEAL, "AGENTIC AI", "AI Research Agent", ["LangChain ReAct + Llama 3.3 70B agent that plans", "multi-step web searches and writes structured reports."], "~70%", "LESS MANUAL RESEARCH TIME", ["LangChain", "Groq", "Streamlit"], v_agent(TEAL))
    project(2, INDIGO, "RAG · LOCAL", "RAG Knowledge Base Chatbot", ["Ollama embeddings + SQLite vector store with", "real-time SSE streaming. Zero external APIs."], "<2s", "RESPONSE LATENCY", ["Ollama", "FastAPI", "SQLite"], v_rag(INDIGO))
    project(3, PINK, "COMPUTER VISION", "Road Damage Classifier", ["ResNet18 transfer learning to classify cracks,", "potholes and normal surfaces. Deployed as an app."], "80%", "TEST ACCURACY", ["PyTorch", "ResNet18", "Streamlit"], v_road(PINK))
    project(4, AMBER, "MACHINE LEARNING", "Employee Attrition Prediction", ["Random Forest on HR analytics data with feature", "importance and live probability scores."], "82%", "ACCURACY", ["scikit-learn", "Pandas", "Streamlit"], v_attr(AMBER))

if __name__ == "__main__":
    hero(); about(); stack(); projects()
    print("built:", sorted(os.listdir(OUT)))
