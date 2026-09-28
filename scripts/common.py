"""Shared helpers for the arcade-theme SVG builders. Not imported at runtime by the
CI workflow (generate_load.py stays standalone) — used only by build_assets.py."""
import random
from html import escape as E

S = "'Inter','SF Pro Display','Segoe UI',Helvetica,Arial,sans-serif"
M = "'JetBrains Mono','SF Mono','Fira Code',ui-monospace,Menlo,Consolas,monospace"
BG, PANEL, HAIR, DIM, INK = "#05060a", "#0a0c12", "#20263a", "#7d8494", "#f2f4f8"
GREEN, CYAN, MAG, AMBER, VIOLET, RED = "#22e07a", "#2fe6ff", "#ff3ec8", "#ffb340", "#8b7bff", "#ff4d5e"

CSS = (f".s{{font-family:{S}}}.m{{font-family:{M}}}"
       ".f{opacity:0;animation:in .8s cubic-bezier(.2,.8,.2,1) forwards}"
       "@keyframes in{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}"
       ".g{opacity:0;animation:pop .6s cubic-bezier(.34,1.56,.64,1) forwards}"
       "@keyframes pop{from{opacity:0;transform:scale(.7)}to{opacity:1;transform:scale(1)}}"
       ".flk{animation:flicker 6s infinite}"
       "@keyframes flicker{0%,93%,100%{opacity:.04}94%{opacity:.12}95%{opacity:.02}96%{opacity:.1}97%{opacity:.03}}"
       "@keyframes blink{50%{opacity:.15}}"
       "@keyframes pulse2{0%{transform:scale(.85);opacity:.9}70%,100%{transform:scale(2.5);opacity:0}}")

GLOW = '<filter id="gw" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
GLOWS = '<filter id="gws" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="1.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'

def svg(w, h, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">'
            f'<defs>{defs}{GLOW}{GLOWS}</defs><style>{CSS}</style>{body}</svg>')

def scanlines(w, h, uid, opacity=.05):
    """CRT scanline overlay + faint flicker + vignette. Purely decorative, tied to one clip."""
    return (f'<pattern id="sl{uid}" width="3" height="3" patternUnits="userSpaceOnUse">'
            f'<rect width="3" height="1.1" fill="#000" fill-opacity="{opacity}"/></pattern>'
            f'<radialGradient id="vg{uid}" cx=".5" cy=".45" r=".75"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>'
            f'<rect width="{w}" height="{h}" fill="url(#sl{uid})"/><rect width="{w}" height="{h}" fill="url(#vg{uid})"/>'
            f'<rect class="flk" width="{w}" height="{h}" fill="#fff" opacity=".04"/>')

def starfield(w, h, n, seed, cols=None):
    random.seed(seed); cols = cols or ["#fff"]
    o = []
    for _ in range(n):
        x, y = random.uniform(0, w), random.uniform(0, h)
        r = random.uniform(.5, 1.6); c = random.choice(cols)
        dur = random.uniform(60, 130); dx = random.uniform(-40, -14)
        tw = random.uniform(2.5, 6)
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{c}" fill-opacity="{random.uniform(.3,.9):.2f}">'
                  f'<animateTransform attributeName="transform" type="translate" from="0 0" to="{dx:.0f} 0" dur="{dur:.0f}s" repeatCount="indefinite"/>'
                  f'<animate attributeName="opacity" values="{random.uniform(.2,.5):.2f};1;{random.uniform(.2,.5):.2f}" dur="{tw:.1f}s" begin="-{random.uniform(0,tw):.1f}s" repeatCount="indefinite"/></circle>')
    return "".join(o)

def perspective_grid(cx, horizon_y, w, h, col, uid, n_v=13, n_h=7, dur=5.5):
    """Tron-style floor grid converging on a vanishing point, with lines drifting toward
    camera to fake forward motion. Clip to the area below the horizon by the caller."""
    o = [f'<clipPath id="pg{uid}"><rect x="0" y="{horizon_y}" width="{w}" height="{h-horizon_y}"/></clipPath><g clip-path="url(#pg{uid})">']
    span = w * 1.4
    for i in range(n_v + 1):
        fx = -0.2 + i / n_v * 1.4
        x_far = cx + fx * span * 0.14
        x_near = cx + fx * span * 0.62
        o.append(f'<line x1="{x_far:.1f}" y1="{horizon_y:.1f}" x2="{x_near:.1f}" y2="{h}" stroke="{col}" stroke-opacity=".22"/>')
    for k in range(n_h):
        o.append(f'<line x1="0" y1="0" x2="{w}" y2="0" stroke="{col}" stroke-opacity="0">'
                  f'<animate attributeName="y1" values="{horizon_y:.0f};{h}" dur="{dur:.1f}s" begin="-{k*dur/n_h:.2f}s" repeatCount="indefinite"/>'
                  f'<animate attributeName="y2" values="{horizon_y:.0f};{h}" dur="{dur:.1f}s" begin="-{k*dur/n_h:.2f}s" repeatCount="indefinite"/>'
                  f'<animate attributeName="stroke-opacity" values="0;.35;0" dur="{dur:.1f}s" begin="-{k*dur/n_h:.2f}s" repeatCount="indefinite"/></line>')
    o.append('</g>')
    return "".join(o)

def cube_badge(cx, cy, size, col1, col2, uid, dur=5.0):
    """Pseudo-3D cube that reads as continuously rotating: classic 2D 'card flip' trick —
    scaleX animates 1 -> 0 -> -1 -> 0 -> 1 while the two faces crossfade at the 0-width instant."""
    s = size
    top = f'{cx-s},{cy-s*.55} {cx},{cy-s} {cx+s},{cy-s*.55} {cx},{cy-s*.1}'
    return (f'<g style="transform-origin:{cx}px {cy}px" filter="url(#gw)">'
            f'<animateTransform attributeName="transform" additive="sum" type="scale" '
            f'values="1 1;0.05 1;1 1" dur="{dur:.1f}s" repeatCount="indefinite"/>'
            f'<polygon points="{top}" fill="{col1}" fill-opacity=".9"/>'
            f'<polygon points="{cx-s},{cy-s*.55} {cx},{cy-s*.1} {cx},{cy+s*.75} {cx-s},{cy+s*.2}" fill="{col1}" fill-opacity=".55"/>'
            f'<polygon points="{cx+s},{cy-s*.55} {cx},{cy-s*.1} {cx},{cy+s*.75} {cx+s},{cy+s*.2}" fill="{col2}" fill-opacity=".7"/>'
            f'</g>')

def marks(w, h, c="#2a3040", i=12, s=5):
    return "".join(f'<path d="M{x-s} {y}H{x+s}M{x} {y-s}V{y+s}" stroke="{c}"/>' for x, y in [(i, i), (w-i, i), (i, h-i), (w-i, h-i)])

def status_dot(x, y, col, r=5):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{col}" style="transform-origin:{x}px {y}px;animation:pulse2 2.2s ease-out infinite" stroke-width="1.3"/>'
            f'<circle cx="{x}" cy="{y}" r="{r-1.6}" fill="{col}"/>')
PULSE_CSS = "@keyframes pulse2{0%{transform:scale(.85);opacity:.9}70%,100%{transform:scale(2.5);opacity:0}}"
