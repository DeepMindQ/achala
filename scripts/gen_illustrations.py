#!/usr/bin/env python3
"""Generate the Achala IT Solutions brand illustration system.
22 animated SVG artworks (deep-navy canvas, brand orange, SMIL animations
so they animate inside <img> tags without JS). Flat, professional,
deep-tech motifs. Deterministic output -> public/images/.
"""
import os

OUT = "/home/z/my-project/site/public/images"
W, H = 1260, 480

ORANGE = "#d20000"
ORANGE_SOFT = "#ff8a7c"
ORANGE_PALE = "#FFC5A6"
NAVY = "#2b5672"
NAVY_DEEP = "#0C0918"
WHITE = "#FFFFFF"

svg_parts = []

def header(defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" width="{W}" height="{H}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{NAVY}"/><stop offset="1" stop-color="{NAVY_DEEP}"/>
</linearGradient>
<linearGradient id="acc" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{ORANGE}"/><stop offset="1" stop-color="{ORANGE_SOFT}"/>
</linearGradient>
<linearGradient id="accv" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{ORANGE}"/><stop offset="1" stop-color="{ORANGE_SOFT}"/>
</linearGradient>
<radialGradient id="vig" cx="0.5" cy="0.42" r="0.75">
  <stop offset="0.55" stop-color="{WHITE}" stop-opacity="0.05"/>
  <stop offset="1" stop-color="{NAVY_DEEP}" stop-opacity="0.85"/>
</radialGradient>
<filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
  <feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="glow2" x="-80%" y="-80%" width="260%" height="260%">
  <feGaussianBlur stdDeviation="12" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<pattern id="grid" width="46" height="46" patternUnits="userSpaceOnUse">
  <path d="M46 0H0V46" fill="none" stroke="{WHITE}" stroke-opacity="0.05" stroke-width="1"/>
</pattern>
{defs}
</defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<rect width="{W}" height="{H}" fill="url(#grid)"/>
<rect width="{W}" height="{H}" fill="url(#vig)"/>'''

def frame():
    return (f'<rect x="18" y="18" width="{W-36}" height="{H-36}" fill="none" '
            f'stroke="{WHITE}" stroke-opacity="0.07" stroke-width="1" rx="14"/>'
            f'<circle cx="40" cy="40" r="3" fill="{ORANGE}" opacity="0.85"/>'
            f'<rect x="52" y="38.5" width="26" height="3" rx="1.5" fill="{WHITE}" opacity="0.12"/>'
            f'<rect x="{W-100}" y="38.5" width="46" height="3" rx="1.5" fill="{WHITE}" opacity="0.12"/>')

def footer():
    return "</svg>"

def pulse_node(x, y, r=5, dur="2.6s", begin="0s", color=ORANGE, op="0.9"):
    return (f'<g filter="url(#glow)"><circle cx="{x}" cy="{y}" r="{r}" fill="{color}" opacity="{op}">'
            f'<animate attributeName="opacity" values="{op};0.25;{op}" dur="{dur}" begin="{begin}" repeatCount="indefinite"/>'
            f'</circle><circle cx="{x}" cy="{y}" r="{r+4}" fill="none" stroke="{color}" stroke-opacity="0.5">'
            f'<animate attributeName="r" values="{r};{r+14}" dur="{dur}" begin="{begin}" repeatCount="indefinite"/>'
            f'<animate attributeName="stroke-opacity" values="0.5;0;0.5" dur="{dur}" begin="{begin}" repeatCount="indefinite"/>'
            f'</circle></g>')

def flow_line(x1, y1, x2, y2, dur="3.2s", begin="0s", width=1.6, color=ORANGE, dash="5 11", op="0.55"):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-opacity="0.22" stroke-width="{width}"/>'
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-opacity="{op}" stroke-width="{width}" '
            f'stroke-dasharray="{dash}" stroke-linecap="round">'
            f'<animate attributeName="stroke-dashoffset" from="0" to="-32" dur="{dur}" begin="{begin}" repeatCount="indefinite"/>'
            f'</line>')

def glass_panel(x, y, w, h, op=0.05):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{WHITE}" fill-opacity="{op}" '
            f'stroke="{WHITE}" stroke-opacity="0.14" stroke-width="1"/>')

def drift(g, dur="9s", dy="14", dx="0", begin="0s"):
    return g + (f'<animateTransform attributeName="transform" type="translate" '
                f'values="0 0; {dx} {dy}; 0 0" dur="{dur}" begin="{begin}" repeatCount="indefinite"/>')

def scene_layers(name: str) -> str:
    """Shared depth layer for every artwork: particle field, horizon glow,
    soft orbs, scan sweep. Deterministic per filename."""
    seed = sum(ord(c) * (i + 7) for i, c in enumerate(name))
    def rnd(n):
        x = (seed * 9301 + n * 49297) % 233280
        return x / 233280.0
    b = ""
    # soft depth orbs
    for i, (cx, cy, r, op) in enumerate([(210, 90, 150, 0.05), (1050, 380, 190, 0.055), (760, 60, 110, 0.045)]):
        b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{ORANGE}" fill-opacity="{op}"/>'
    # particle field — 34 twinkling dots
    b += '<g>'
    for i in range(34):
        px = round(30 + rnd(i) * 1200, 1)
        py = round(24 + rnd(i + 50) * 432, 1)
        pr = 1 + round(rnd(i + 99) * 1.6, 2)
        dur = round(2.2 + rnd(i + 150) * 3.4, 1)
        begin = round(rnd(i + 200) * 3.2, 1)
        b += (f'<circle cx="{px}" cy="{py}" r="{pr}" fill="{WHITE}" fill-opacity="0.5">'
              f'<animate attributeName="opacity" values="0.5;0.08;0.5" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></circle>')
    b += '</g>'
    # horizon glow line
    b += (f'<rect x="40" y="{H-64}" width="{W-80}" height="1.4" fill="url(#acc)" opacity="0.35"/>'
          f'<rect x="40" y="{H-64}" width="{W-80}" height="1.4" fill="{ORANGE}" opacity="0.5">'
          f'<animate attributeName="width" values="0;{W-80};0" dur="9s" repeatCount="indefinite"/></rect>')
    # slow scan sweep
    b += (f'<rect x="-140" y="0" width="140" height="{H}" fill="url(#acc)" opacity="0.05">'
          f'<animate attributeName="x" values="-140;{W+20}" dur="11s" repeatCount="indefinite"/></rect>')
    return b

def save(name, body, extra_header=""):
    os.makedirs(OUT, exist_ok=True)
    svg = header(extra_header) + scene_layers(name) + body + footer()
    path = os.path.join(OUT, name)
    open(path, "w").write(svg)
    return os.path.getsize(path)

report = {}

# ── 1. AI neural mesh ────────────────────────────────────────────────
def neural_mesh():
    import math
    pts = [(180+i*150, 150+((i*53)%5)*52+10) for i in range(8)]
    b = ""
    for i in range(len(pts)-1):
        b += flow_line(*pts[i], *pts[i+1], dur=f"{2.6+0.35*i:.1f}s", begin=f"{i*0.3:.1f}s")
    for i,(x,y) in enumerate(pts):
        b += pulse_node(x, y, 6 if i%3==0 else 4, dur=f"{2.2+0.4*(i%4):.1f}s", begin=f"{i*0.25:.1f}s")
    b += flow_line(pts[0][0], pts[0][1], pts[3][0], pts[3][1], dur="4s", color=ORANGE_SOFT)
    b += flow_line(pts[4][0], pts[4][1], pts[7][0], pts[7][1], dur="4.6s", color=ORANGE_SOFT)
    # inference wave
    b += (f'<rect x="150" y="380" width="960" height="34" rx="17" fill="none" stroke="{ORANGE}" stroke-opacity="0.35"/>'
          f'<rect x="150" y="380" width="240" height="34" rx="17" fill="url(#acc)" opacity="0.8">'
          f'<animate attributeName="x" values="150;870;150" dur="7s" repeatCount="indefinite"/></rect>')
    return save("ai-neural-mesh.svg", b)
report["ai-neural-mesh"] = neural_mesh()

# ── 2. Agent swarm lanes ─────────────────────────────────────────────
def agent_swarm():
    b = ""
    for lane in range(4):
        y = 130 + lane*70
        b += f'<line x1="120" y1="{y}" x2="1140" y2="{y}" stroke="{WHITE}" stroke-opacity="0.07"/>'
        for k in range(4):
            x0 = 140 + k*260
            begin = f"{lane*0.7 + k*0.9:.1f}s"
            b += (f'<g><circle cx="0" cy="0" r="9" fill="url(#accv)" opacity="0.95" filter="url(#glow)"/>'
                  f'<circle cx="0" cy="0" r="16" fill="none" stroke="{ORANGE}" stroke-opacity="0.4"/>'
                  f'<animateTransform attributeName="transform" type="translate" '
                  f'from="{x0} {y}" to="{x0+220} {y}" dur="6.5s" begin="{begin}" repeatCount="indefinite"/></g>')
        b += f'<path d="M{120+lane*10} {y-16} q 130 -30 260 0 t 260 0 t 260 0 t 240 0" fill="none" stroke="{ORANGE}" stroke-opacity="0.18" stroke-dasharray="2 8"/>'
    b += glass_panel(480, 60, 300, 46, 0.06)
    b += (f'<circle cx="505" cy="83" r="5" fill="{ORANGE}"><animate attributeName="opacity" values="1;0.3;1" dur="1.6s" repeatCount="indefinite"/></circle>'
          f'<rect x="525" y="72" width="120" height="6" rx="3" fill="{WHITE}" opacity="0.16"/>'
          f'<rect x="525" y="86" width="200" height="6" rx="3" fill="{WHITE}" opacity="0.1"/>')
    return save("agent-swarm-flow.svg", b)
report["agent-swarm-flow"] = agent_swarm()

# ── 3. Lakehouse layered streams ─────────────────────────────────────
def lakehouse():
    b = ""
    layers = [(300, 350, 660, 56), (250, 270, 760, 56), (200, 190, 860, 56), (150, 110, 960, 56)]
    for i,(x,y,w,h) in enumerate(layers):
        b += glass_panel(x, y, w, h, 0.05 + i*0.012)
        b += (f'<rect x="{x+18}" y="{y+h/2-2}" width="{w-160}" height="4" rx="2" fill="url(#acc)" opacity="{0.28+0.14*i}">'
              f'<animate attributeName="width" values="{w-160};{w-90};{w-160}" dur="{5+i}s" repeatCount="indefinite"/></rect>')
        for k in range(3):
            b += (f'<circle cx="{x+w-90+k*34}" cy="{y+h/2}" r="5.5" fill="{ORANGE}" opacity="0.8">'
                  f'<animate attributeName="opacity" values="0.85;0.25;0.85" dur="2.4s" begin="{k*0.4+i*0.3:.1f}s" repeatCount="indefinite"/></circle>')
    for i in range(7):
        x = 210 + i*130
        b += (f'<line x1="{x}" y1="90" x2="{x}" y2="150" stroke="{ORANGE}" stroke-opacity="0.0" stroke-width="3" stroke-dasharray="4 14">'
              f'<animate attributeName="stroke-opacity" values="0;0.7;0" dur="2.8s" begin="{i*0.35:.1f}s" repeatCount="indefinite"/></line>')
    return save("lakehouse-streams.svg", b)
report["lakehouse-streams"] = lakehouse()

# ── 4. Zero-trust radar ──────────────────────────────────────────────
def zero_trust():
    cx, cy = 630, 250
    b = ""
    for r,op in [(90,0.14),(150,0.11),(210,0.08),(270,0.06)]:
        b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ORANGE}" stroke-opacity="{op}" stroke-width="1.4"/>'
    b += (f'<g><path d="M{cx} {cy} L{cx} {cy-270} A270 270 0 0 1 {cx+234} {cy-135} Z" fill="url(#acc)" opacity="0.14">'
          f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="7.5s" repeatCount="indefinite"/></path></g>')
    b += f'<line x1="{cx}" y1="{cy}" x2="{cx+270}" y2="{cy}" stroke="{ORANGE}" stroke-opacity="0.7" stroke-width="2">'
    b += f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="7.5s" repeatCount="indefinite"/></line>'
    import math
    for ang,dist,begin in [(30,180,"0.8s"),(150,120,"2.2s"),(260,210,"3.4s"),(320,90,"1.5s")]:
        x = cx + dist*math.cos(math.radians(ang)); y = cy + dist*math.sin(math.radians(ang))
        b += pulse_node(x, y, 5, dur="1.8s", begin=begin, color=ORANGE_PALE)
    b += f'<path d="M{cx} {cy-64} l22 26 30 -52" fill="none" stroke="{ORANGE}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" filter="url(#glow2)"/>'
    b += glass_panel(930, 330, 240, 76, 0.05)
    b += f'<rect x="948" y="350" width="150" height="6" rx="3" fill="{WHITE}" opacity="0.15"/><rect x="948" y="368" width="204" height="6" rx="3" fill="{WHITE}" opacity="0.1"/>'
    return save("zero-trust-radar.svg", b)
report["zero-trust-radar"] = zero_trust()

# ── 5. Edge lattice ──────────────────────────────────────────────────
def edge_lattice():
    b = ""
    def iso(x, y, s):
        return (f'<g><path d="M{x} {y} l{s} {-s*0.5} l{s} {s*0.5} l{-s} {s*0.5} Z" fill="{ORANGE}" fill-opacity="0.16" stroke="{ORANGE}" stroke-opacity="0.55"/>'
                f'<path d="M{x} {y+s} l{s} {-s*0.5} l{s} {s*0.5} l{-s} {s*0.5} Z" fill="{WHITE}" fill-opacity="0.05" stroke="{WHITE}" stroke-opacity="0.16"/></g>')
    base = [(380,300),(520,260),(660,300),(800,260),(520,340),(660,340),(380,220),(800,180)]
    for x,y in base:
        b += iso(x, y, 34)
    for (x,y) in base:
        b += (f'<line x1="{x+34}" y1="{y+8}" x2="{x+34}" y2="{y-52}" stroke="{ORANGE}" stroke-opacity="0.5" stroke-width="2" stroke-dasharray="3 9">'
              f'<animate attributeName="stroke-dashoffset" from="24" to="0" dur="2.2s" repeatCount="indefinite"/></line>'
              f'<circle cx="{x+34}" cy="{y-56}" r="4.5" fill="{ORANGE_PALE}"><animate attributeName="opacity" values="0.9;0.2;0.9" dur="2.2s" repeatCount="indefinite"/></circle>')
    b += drift(f'<circle cx="630" cy="120" r="26" fill="none" stroke="{ORANGE}" stroke-opacity="0.5" stroke-width="2"/>', dur="6s", dy="-8")
    b += drift(f'<circle cx="630" cy="120" r="40" fill="none" stroke="{WHITE}" stroke-opacity="0.12"/>', dur="6s", dy="10", begin="1s")
    return save("edge-lattice.svg", b)
report["edge-lattice"] = edge_lattice()

# ── 6. Quantum orbits ────────────────────────────────────────────────
def quantum():
    cx, cy = 630, 240
    b = ""
    for r, dur, begin in [(80,"6s","0s"),(130,"9s","0.6s"),(185,"12s","1.2s"),(240,"16s","1.8s")]:
        b += f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{int(r*0.42)}" fill="none" stroke="{ORANGE}" stroke-opacity="0.3" stroke-width="1.4"/>'
        b += (f'<g><circle cx="{cx+r}" cy="{cy}" r="7" fill="url(#accv)" filter="url(#glow)"/>'
              f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="{dur}" repeatCount="indefinite"/></g>')
    b += pulse_node(cx, cy, 12, dur="3s", color=ORANGE)
    b += f'<circle cx="{cx}" cy="{cy}" r="30" fill="none" stroke="{WHITE}" stroke-opacity="0.25"><animate attributeName="r" values="26;40;26" dur="3s" repeatCount="indefinite"/></circle>'
    return save("quantum-orbits.svg", b)
report["quantum-orbits"] = quantum()

# ── 7. Ledger chain ──────────────────────────────────────────────────
def ledger():
    b = ""
    xs = [170, 390, 610, 830, 1050]
    for i,x in enumerate(xs):
        y = 240 if i%2==0 else 250
        b += glass_panel(x-52, y-40, 104, 80, 0.05)
        b += f'<rect x="{x-30}" y="{y-16}" width="60" height="32" rx="6" fill="url(#acc)" opacity="0.85"/>'
        b += pulse_node(x, y, 4, dur="2.4s", begin=f"{i*0.4:.1f}s")
        if i < 4:
            b += flow_line(xs[i]+52, 244, xs[i+1]-52, 246, dur="2.8s", begin=f"{i*0.3:.1f}s")
    b += (f'<circle cx="610" cy="360" r="8" fill="none" stroke="{ORANGE}" stroke-opacity="0.6"/>'
          f'<circle cx="610" cy="360" r="8" fill="none" stroke="{ORANGE}">'
          f'<animate attributeName="r" values="8;52" dur="2.8s" repeatCount="indefinite"/>'
          f'<animate attributeName="stroke-opacity" values="0.6;0" dur="2.8s" repeatCount="indefinite"/></circle>')
    return save("ledger-chain.svg", b)
report["ledger-chain"] = ledger()

# ── 8. Digital twin mirror ───────────────────────────────────────────
def twin():
    b = ""
    b += f'<path d="M170 340 v-90 l60 -44 60 44 v90 Z" fill="none" stroke="{WHITE}" stroke-opacity="0.4" stroke-width="1.6"/>'
    b += f'<path d="M420 340 v-120 l70 -52 70 52 v120 Z" fill="none" stroke="{WHITE}" stroke-opacity="0.4" stroke-width="1.6"/>'
    b += f'<path d="M690 340 v-70 l56 -40 56 40 v70 Z" fill="none" stroke="{WHITE}" stroke-opacity="0.4" stroke-width="1.6"/>'
    b += f'<path d="M880 340 v-140 l74 -56 74 56 v140 Z" fill="none" stroke="{WHITE}" stroke-opacity="0.4" stroke-width="1.6"/>'
    for x,y,begin in [(230,250,"0.4s"),(490,220,"1.2s"),(746,270,"2s"),(954,200,"2.8s")]:
        b += pulse_node(x, y, 5, dur="2.6s", begin=begin)
        b += flow_line(x, y, x+120, 130, dur="3s", begin=begin, color=ORANGE_PALE, dash="2 10", op="0.5")
    b += glass_panel(160, 370, 940, 40, 0.05)
    b += (f'<rect x="180" y="384" width="300" height="10" rx="5" fill="{WHITE}" opacity="0.1"/>'
          f'<rect x="180" y="384" width="0" height="10" rx="5" fill="url(#acc)" opacity="0.9">'
          f'<animate attributeName="width" values="0;300" dur="4.5s" repeatCount="indefinite"/></rect>')
    b += f'<line x1="150" y1="340" x2="1110" y2="340" stroke="{WHITE}" stroke-opacity="0.18"/>'
    return save("twin-mirror.svg", b)
report["twin-mirror"] = twin()

# ── 9. Decision radar bars (nexus) ───────────────────────────────────
def radar_bars():
    b = ""
    heights = [90, 150, 210, 170, 120, 190, 240]
    for i,h in enumerate(heights):
        x = 200 + i*130
        b += glass_panel(x-34, 400-h, 68, h, 0.045)
        b += (f'<rect x="{x-22}" y="{400-h+10}" width="44" height="{h-20}" rx="8" fill="url(#accv)" opacity="{0.5+0.06*i}">'
              f'<animate attributeName="height" values="{h-20};{h-52};{h-20}" dur="{3.4+0.4*i:.1f}s" repeatCount="indefinite"/>'
              f'<animate attributeName="y" values="{400-h+10};{400-h+42};{400-h+10}" dur="{3.4+0.4*i:.1f}s" repeatCount="indefinite"/></rect>')
    b += f'<line x1="150" y1="400" x2="1110" y2="400" stroke="{WHITE}" stroke-opacity="0.2"/>'
    b += pulse_node(630, 90, 7, dur="3s")
    return save("decision-bars.svg", b)
report["decision-bars"] = radar_bars()

# ── 10. Platform strata (forge) ──────────────────────────────────────
def strata():
    b = ""
    for i in range(4):
        y = 120 + i*76
        x = 210 + i*40
        w = 840 - i*80
        b += glass_panel(x, y, w, 52, 0.05)
        b += f'<rect x="{x+16}" y="{y+22}" width="10" height="10" rx="2" fill="{ORANGE}" opacity="{0.85-0.15*i}"/>'
        b += (f'<rect x="{x+40}" y="{y+24}" width="{int(w*0.4)}" height="5" rx="2.5" fill="{WHITE}" opacity="0.14"/>')
        b += (f'<rect x="{x+40}" y="{y+24}" width="0" height="5" rx="2.5" fill="url(#acc)" opacity="0.9">'
              f'<animate attributeName="width" values="0;{int(w*0.62)}" dur="{4+ i*0.8:.1f}s" begin="{i*0.5:.1f}s" repeatCount="indefinite"/></rect>')
    b += f'<path d="M1064 132 q 30 0 30 30 v 220" fill="none" stroke="{ORANGE}" stroke-opacity="0.5" stroke-width="2" stroke-dasharray="4 10">'
    b += f'<animate attributeName="stroke-dashoffset" from="40" to="0" dur="3s" repeatCount="indefinite"/></path>'
    return save("platform-strata.svg", b)
report["platform-strata"] = strata()

# ── 11. Fleet formation (swarm platform) ─────────────────────────────
def fleet():
    b = ""
    def chevron(x, y, s, op):
        return (f'<path d="M{x} {y} l{-s} {-s*0.62} l0 {s*0.34} l{s*0.72} {s*0.28} l{0.28*s*2 - s*0.72} {0} ' 
                f'l0 {-s*0.34} Z" fill="url(#accv)" opacity="{op}" filter="url(#glow)"/>')
    rows = [(330,300,26,0.95),(450,240,22,0.8),(560,320,20,0.75),(690,220,24,0.85),(820,290,19,0.7),(950,250,21,0.8)]
    for i,(x,y,s,op) in enumerate(rows):
        b += f'<g>{chevron(x,y,s,op)}<animateTransform attributeName="transform" type="translate" values="0 0; 26 -12; 0 0" dur="{4+0.5*i:.1f}s" begin="{i*0.4:.1f}s" repeatCount="indefinite"/></g>'
        b += f'<circle cx="{x}" cy="{y+42}" r="3" fill="{ORANGE_PALE}" opacity="0.6"><animate attributeName="opacity" values="0.6;0.1;0.6" dur="2s" begin="{i*0.3:.1f}s" repeatCount="indefinite"/></circle>'
    b += f'<path d="M180 380 Q 630 300 1080 380" fill="none" stroke="{WHITE}" stroke-opacity="0.12" stroke-dasharray="3 9"/>'
    return save("fleet-formation.svg", b)
report["fleet-formation"] = fleet()

# ── 12. Sentinel wall (sentinel) ─────────────────────────────────────
def sentinel():
    b = ""
    for i in range(10):
        for j in range(3):
            x = 240 + i*84; y = 170 + j*84
            lit = (i*3+j) % 4 == 0
            b += f'<rect x="{x}" y="{y}" width="64" height="64" rx="10" fill="{ORANGE if lit else WHITE}" fill-opacity="{0.14 if lit else 0.05}" stroke="{WHITE}" stroke-opacity="0.14">'
            if lit:
                b += f'<animate attributeName="fill-opacity" values="0.16;0.34;0.16" dur="2.6s" begin="{(i+j)*0.22:.1f}s" repeatCount="indefinite"/>'
            b += '</rect>'
            if lit:
                b += f'<circle cx="{x+32}" cy="{y+32}" r="7" fill="{ORANGE}" filter="url(#glow)"><animate attributeName="opacity" values="1;0.3;1" dur="2.6s" begin="{(i+j)*0.22:.1f}s" repeatCount="indefinite"/></circle>'
    b += f'<path d="M630 96 l30 36 40 -66" fill="none" stroke="{ORANGE}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" filter="url(#glow2)" opacity="0.9"/>'
    return save("sentinel-grid.svg", b)
report["sentinel-grid"] = sentinel()

# ── 13. Mirror city (twinverse) ──────────────────────────────────────
def mirror_city():
    b = ""
    import math
    for i in range(11):
        x = 190 + i*82
        h = 60 + (i*i*7) % 200
        b += f'<rect x="{x}" y="{330-h}" width="52" height="{h}" fill="none" stroke="{WHITE}" stroke-opacity="0.28" stroke-width="1.4"/>'
        b += f'<rect x="{x}" y="{330-h}" width="52" height="{h}" fill="{ORANGE}" fill-opacity="0.05"/>'
        b += f'<rect x="{x+6}" y="{330-h+8}" width="40" height="3" rx="1.5" fill="{ORANGE}" opacity="0.55"><animate attributeName="opacity" values="0.55;0.12;0.55" dur="2.8s" begin="{i*0.28:.1f}s" repeatCount="indefinite"/></rect>'
    b += f'<line x1="150" y1="330" x2="1110" y2="330" stroke="{WHITE}" stroke-opacity="0.25"/>'
    b += f'<line x1="150" y1="392" x2="1110" y2="392" stroke="{WHITE}" stroke-opacity="0.1"/>'
    b += f'<line x1="150" y1="420" x2="1110" y2="420" stroke="{WHITE}" stroke-opacity="0.06"/>'
    b += pulse_node(630, 100, 8, dur="3.4s")
    return save("mirror-city.svg", b)
report["mirror-city"] = mirror_city()

# ── 14. Orbit converge (quanta) ──────────────────────────────────────
def orbit_converge():
    cx, cy = 630, 240
    b = ""
    for i in range(5):
        r = 250 - i*46
        b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ORANGE}" stroke-opacity="{0.12+0.05*i}" stroke-dasharray="6 12">'
        b += f'<animateTransform attributeName="transform" type="rotate" from="{i*36} {cx} {cy}" to="{360+i*36} {cx} {cy}" dur="{14-2*i}s" repeatCount="indefinite"/></circle>'
        b += f'<circle cx="{cx+r}" cy="{cy}" r="5" fill="{ORANGE_PALE}" opacity="0.9">'
        b += f'<animateTransform attributeName="transform" type="rotate" from="{i*36} {cx} {cy}" to="{360+i*36} {cx} {cy}" dur="{14-2*i}s" repeatCount="indefinite"/></circle>'
    b += f'<circle cx="{cx}" cy="{cy}" r="26" fill="url(#accv)" filter="url(#glow2)"><animate attributeName="r" values="24;30;24" dur="3.6s" repeatCount="indefinite"/></circle>'
    return save("orbit-converge.svg", b)
report["orbit-converge"] = orbit_converge()

# ── 15. Trust graph (ledger platform) ────────────────────────────────
def trust_graph():
    import math
    cx, cy = 630, 240
    b = ""
    nodes = []
    for i in range(10):
        ang = i*36
        d = 150 + (i%3)*46
        x = cx + d*math.cos(math.radians(ang)); y = cy + d*0.72*math.sin(math.radians(ang))
        nodes.append((x,y))
    for i in range(len(nodes)):
        for j in (i+1, i+3):
            if j < len(nodes):
                b += flow_line(*nodes[i], *nodes[j], dur=f"{3+0.3*(i%4):.1f}s", begin=f"{0.2*(i+j):.1f}s", op="0.35")
    for i,(x,y) in enumerate(nodes):
        b += pulse_node(x, y, 5.5, dur=f"{2.2+0.3*(i%5):.1f}s", begin=f"{i*0.2:.1f}s")
    b += f'<circle cx="{cx}" cy="{cy}" r="34" fill="{ORANGE}" fill-opacity="0.16" stroke="{ORANGE}" stroke-opacity="0.7" stroke-width="2"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="12" fill="url(#accv)"/>'
    return save("trust-graph.svg", b)
report["trust-graph"] = trust_graph()

# ── 16. Governance compass (compass) ─────────────────────────────────
def compass():
    cx, cy = 630, 250
    b = ""
    b += f'<circle cx="{cx}" cy="{cy}" r="170" fill="none" stroke="{WHITE}" stroke-opacity="0.16" stroke-width="1.4"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="126" fill="none" stroke="{WHITE}" stroke-opacity="0.1"/>'
    for i in range(12):
        ang = i*30
        import math
        x1 = cx + 126*math.cos(math.radians(ang)); y1 = cy + 126*math.sin(math.radians(ang))
        x2 = cx + 170*math.cos(math.radians(ang)); y2 = cy + 170*math.sin(math.radians(ang))
        b += f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{WHITE}" stroke-opacity="0.18"/>'
    b += (f'<g><path d="M{cx} {cy-118} L{cx+26} {cy} L{cx} {cy+118} L{cx-26} {cy} Z" fill="url(#accv)" opacity="0.9" filter="url(#glow)"/>'
          f'<animateTransform attributeName="transform" type="rotate" values="-14 {cx} {cy}; 14 {cx} {cy}; -14 {cx} {cy}" dur="6.5s" repeatCount="indefinite"/></g>')
    b += f'<circle cx="{cx}" cy="{cy}" r="14" fill="{NAVY_DEEP}" stroke="{ORANGE}" stroke-width="3"/>'
    for ang,begin in [(45,"0.5s"),(135,"1.4s"),(225,"2.3s"),(315,"3.2s")]:
        import math
        x = cx + 200*math.cos(math.radians(ang)); y = cy + 200*math.sin(math.radians(ang))
        b += pulse_node(x, y, 5, dur="2.4s", begin=begin)
    return save("governance-compass.svg", b)
report["governance-compass"] = compass()

# ── 17. Global arcs (industries/global) ──────────────────────────────
def global_arcs():
    cx, cy = 630, 260
    b = ""
    b += f'<circle cx="{cx}" cy="{cy}" r="180" fill="none" stroke="{WHITE}" stroke-opacity="0.14" stroke-width="1.4"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="180" fill="{ORANGE}" fill-opacity="0.045"/>'
    import math
    for i in range(6):
        lat = -140 + i*56
        ry = 180*math.cos(math.radians(lat)) if abs(lat) < 90 else 0
        ry = abs(180*math.sin(math.radians(lat)*0.5))
        b += f'<ellipse cx="{cx}" cy="{cy+lat*0.62:.0f}" rx="{180*math.cos(math.radians(lat)):.0f}" ry="{ry*0.16:.0f}" fill="none" stroke="{WHITE}" stroke-opacity="0.1"/>'
    for i in range(10):
        ang = i*36
        x = cx + 180*math.cos(math.radians(ang)); y = cy + 180*math.sin(math.radians(ang))
        if y > cy + 150: continue
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4" fill="{ORANGE}" opacity="0.9"><animate attributeName="opacity" values="0.9;0.25;0.9" dur="{2+0.3*(i%4):.1f}s" begin="{i*0.25:.1f}s" repeatCount="indefinite"/></circle>'
    hubs = [(450,180),(700,150),(840,240),(540,300)]
    for i,(x,y) in enumerate(hubs):
        b += pulse_node(x, y, 6, dur="2.8s", begin=f"{i*0.5:.1f}s")
        if i < 3:
            x2,y2 = hubs[i+1]
            b += f'<path d="M{x} {y} Q {(x+x2)/2} {min(y,y2)-80} {x2} {y2}" fill="none" stroke="{ORANGE}" stroke-opacity="0.5" stroke-width="1.8" stroke-dasharray="4 10">'
            b += f'<animate attributeName="stroke-dashoffset" from="0" to="-28" dur="3s" begin="{i*0.4:.1f}s" repeatCount="indefinite"/></path>'
    return save("global-arcs.svg", b)
report["global-arcs"] = global_arcs()

# ── 18. Health pulse (healthcare) ────────────────────────────────────
def health():
    b = ""
    mid = 250
    pts = "150 250 320 250 360 250 390 180 430 320 470 250 640 250 680 250 710 200 750 300 790 250 960 250 1110 250"
    b += f'<polyline points="{pts}" fill="none" stroke="{ORANGE}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round" filter="url(#glow)"/>'
    b += (f'<polyline points="{pts}" fill="none" stroke="{ORANGE}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round">'
          f'<animate attributeName="stroke-dasharray" values="0 1600;1600 0;0 1600" dur="5.5s" repeatCount="indefinite"/></polyline>')
    b += f'<line x1="150" y1="{mid}" x2="1110" y2="{mid}" stroke="{WHITE}" stroke-opacity="0.1"/>'
    for x,y,begin in [(360,150,"0.6s"),(700,120,"1.8s"),(1000,190,"3s")]:
        b += pulse_node(x, y, 5, dur="2.4s", begin=begin, color=ORANGE_PALE)
    return save("health-pulse.svg", b)
report["health-pulse"] = health()

# ── 19. Retail demand (retail) ───────────────────────────────────────
def retail():
    b = ""
    pts = [(180,340),(340,300),(500,320),(660,240),(820,200),(980,150)]
    d = f'M{pts[0][0]} {pts[0][1]} ' + ' '.join(f'L{x} {y}' for x,y in pts[1:])
    b += f'<path d="{d}" fill="none" stroke="{ORANGE}" stroke-width="3.4" filter="url(#glow)"/>'
    b += (f'<path d="{d} L980 400 L180 400 Z" fill="url(#accv)" opacity="0.12"/>')
    for i,(x,y) in enumerate(pts):
        b += pulse_node(x, y, 5.5, dur=f"{2.4+0.3*(i%3):.1f}s", begin=f"{i*0.3:.1f}s")
    for i in range(3):
        x = 240 + i*330
        b += (f'<g><rect x="{x}" y="{170+i*10}" width="46" height="30" rx="8" fill="none" stroke="{WHITE}" stroke-opacity="0.35" stroke-width="2"/>'
              f'<circle cx="{x+10}" cy="{206+i*10}" r="4.5" fill="{WHITE}" fill-opacity="0.35"/><circle cx="{x+36}" cy="{206+i*10}" r="4.5" fill="{WHITE}" fill-opacity="0.35"/>'
              f'<animateTransform attributeName="transform" type="translate" values="0 0; 40 -14; 0 0" dur="{4+ i:.1f}s" begin="{i*0.7:.1f}s" repeatCount="indefinite"/></g>')
    b += f'<line x1="150" y1="400" x2="1110" y2="400" stroke="{WHITE}" stroke-opacity="0.2"/>'
    return save("retail-demand.svg", b)
report["retail-demand"] = retail()

# ── 20. Energy grid (energy/manufacturing) ───────────────────────────
def energy_grid():
    b = ""
    for i in range(6):
        x = 200 + i*180
        b += f'<line x1="{x}" y1="110" x2="{x}" y2="380" stroke="{WHITE}" stroke-opacity="0.1"/>'
    for j in range(4):
        y = 110 + j*90
        b += f'<line x1="200" y1="{y}" x2="1100" y2="{y}" stroke="{WHITE}" stroke-opacity="0.1"/>'
    for k in range(8):
        x = 200 + k*128; y = 110 + ((k*37)%4)*90
        x2 = x + 128; y2 = 110 + (((k+1)*53)%4)*90
        b += flow_line(x, y, x2, y2, dur=f"{2.6+0.2*k:.1f}s", begin=f"{k*0.35:.1f}s", dash="3 13", op="0.6")
    for x,y,begin in [(200,110,"0.2s"),(1100,380,"2.6s"),(1100,110,"1.4s"),(200,380,"3.2s")]:
        b += pulse_node(x, y, 6, dur="2.6s", begin=begin)
    b += f'<path d="M560 380 h140 v-46 h-60 v-40 h-80 Z" fill="none" stroke="{WHITE}" stroke-opacity="0.3" stroke-width="1.6"/>'
    b += f'<rect x="560" y="330" width="140" height="6" rx="3" fill="url(#acc)" opacity="0.8"><animate attributeName="opacity" values="0.8;0.3;0.8" dur="2.2s" repeatCount="indefinite"/></rect>'
    return save("energy-grid.svg", b)
report["energy-grid"] = energy_grid()

# ── 21. Capital flow (banking/finance) ───────────────────────────────
def capital_flow():
    b = ""
    cols = [(240,220),(430,180),(620,240),(810,160),(1000,210)]
    for i,(x,h) in enumerate(cols):
        b += glass_panel(x-40, 400-h-20, 80, h+20, 0.045)
        b += (f'<rect x="{x-24}" y="{400-h}" width="48" height="{h}" rx="8" fill="url(#accv)" opacity="{0.55+0.08*i}">'
              f'<animate attributeName="height" values="{h};{h-26};{h}" dur="{3+0.5*i:.1f}s" begin="{i*0.3:.1f}s" repeatCount="indefinite"/>'
              f'<animate attributeName="y" values="{400-h};{400-h+26};{400-h}" dur="{3+0.5*i:.1f}s" begin="{i*0.3:.1f}s" repeatCount="indefinite"/></rect>')
    for i in range(4):
        x1 = cols[i][0]+40; y1 = 400-cols[i][1]-10
        x2 = cols[i+1][0]-40; y2 = 400-cols[i+1][1]-10
        b += f'<path d="M{x1} {y1} C {(x1+x2)/2} {y1-60}, {(x1+x2)/2} {y2-60}, {x2} {y2}" fill="none" stroke="{ORANGE}" stroke-opacity="0.4" stroke-width="1.6" stroke-dasharray="3 9">'
        b += f'<animate attributeName="stroke-dashoffset" from="0" to="-24" dur="2.6s" begin="{i*0.3:.1f}s" repeatCount="indefinite"/></path>'
    b += f'<line x1="180" y1="400" x2="1080" y2="400" stroke="{WHITE}" stroke-opacity="0.2"/>'
    return save("capital-flow.svg", b)
report["capital-flow"] = capital_flow()

# ── 22. Public sector / governance dome ──────────────────────────────
def public_dome():
    b = ""
    cx = 630
    b += f'<path d="M{cx-260} 380 A260 260 0 0 1 {cx+260} 380" fill="none" stroke="{WHITE}" stroke-opacity="0.3" stroke-width="1.6"/>'
    for r in (60, 120, 180, 240):
        b += f'<path d="M{cx-r} 380 A{r} {r} 0 0 1 {cx+r} 380" fill="none" stroke="{ORANGE}" stroke-opacity="{0.35-r*0.001:.2f}" stroke-dasharray="5 12">'
        b += f'<animate attributeName="stroke-dashoffset" from="0" to="-34" dur="{3+r*0.01:.1f}s" repeatCount="indefinite"/></path>'
    b += f'<line x1="{cx}" y1="380" x2="{cx}" y2="140" stroke="{ORANGE}" stroke-width="2.4" stroke-opacity="0.7"/>'
    for x,y,begin in [(cx-260,380,"0.4s"),(cx+260,380,"1s"),(cx,140,"1.6s")]:
        b += pulse_node(x, y, 6, dur="2.8s", begin=begin)
    b += f'<line x1="330" y1="380" x2="930" y2="380" stroke="{WHITE}" stroke-opacity="0.25"/>'
    b += glass_panel(480, 90, 300, 40, 0.05)
    b += f'<rect x="500" y="104" width="140" height="6" rx="3" fill="{WHITE}" opacity="0.16"/><rect x="500" y="116" width="230" height="5" rx="2.5" fill="{WHITE}" opacity="0.1"/>'
    return save("public-dome.svg", b)
report["public-dome"] = public_dome()

print("Generated SVG illustrations:")
for k, v in report.items():
    print(f"  {k}.svg  {v/1024:.1f} KB")
print(f"TOTAL: {sum(report.values())/1024:.1f} KB")
