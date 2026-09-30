import os
W, H = 1280, 420
INK, PANEL = "#0b0e13", "#11161d"
AMBER, AMBER_DIM, TEAL, MUTED, LINE = "#ffb454", "#8a6a3c", "#5eead4", "#7d8896", "#222a35"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'DejaVu Sans Mono', 'Liberation Mono', monospace"

G = {
 "R": ["11110","10001","10001","11110","10100","10010","10001"],
 "C": ["01111","10000","10000","10000","10000","10000","01111"],
 "8": ["01110","10001","10001","01110","10001","10001","01110"],
 "9": ["01110","10001","10001","01111","00001","00001","01110"],
}
CELL, GAP = 15, 3
STEP = CELL + GAP

def word(text, x0, y0, solid):
    out, col = [], 0
    for ch in text:
        for r, row in enumerate(G[ch]):
            for c, v in enumerate(row):
                if v == "1":
                    x, y = x0 + (col + c) * STEP, y0 + r * STEP
                    d = (col + c) * 0.035 + r * 0.02
                    if solid:
                        out.append(f'<rect class="px" style="animation-delay:{d:.2f}s" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{AMBER}"/>')
                    else:
                        out.append(f'<rect class="px" style="animation-delay:{d:.2f}s" x="{x+.75}" y="{y+.75}" width="{CELL-1.5}" height="{CELL-1.5}" rx="2" fill="{TEAL}" fill-opacity=".10" stroke="{TEAL}" stroke-width="1.5"/>')
        col += 6
    return "\n".join(out), x0 + (col - 1) * STEP - GAP

# ---- trayectoria de vuelo (bezier cubicas) y su longitud
def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0], u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1])
segs = [((760,292),(850,292),(858,150),(952,158)), ((952,158),(1046,166),(1060,262),(1200,112))]
PATH = "M 760 292 C 850 292, 858 150, 952 158 S 1060 262, 1200 112"
L, prev = 0, None
for s in segs:
    for i in range(401):
        p = bez(*s, i/400)
        if prev: L += ((p[0]-prev[0])**2 + (p[1]-prev[1])**2) ** .5
        prev = p
L = round(L + 2)
wps = [(760,292,"WP1"), bez(*segs[0], .52) + ("WP2",), (952,158,"WP3"), bez(*segs[1], .55) + ("WP4",), (1200,112,"WP5")]

# ---- cinta de rumbo
labels = ["N","030","060","E","120","150","S","210","240","W","300","330"]
def tape(off):
    o = []
    for i in range(60):
        x = off + i * 20
        if i % 5 == 0:
            lab = labels[i // 5]
            card = lab in "NESW"
            o.append(f'<line x1="{x}" y1="0" x2="{x}" y2="14" stroke="{AMBER if card else MUTED}" stroke-width="1.5"/>')
            o.append(f'<text x="{x}" y="34" text-anchor="middle" font-size="12" fill="{AMBER if card else MUTED}" letter-spacing="1">{lab}</text>')
        else:
            o.append(f'<line x1="{x}" y1="0" x2="{x}" y2="7" stroke="{LINE}" stroke-width="1.5"/>')
    return "\n".join(o)

rrc, xend = word("RRC", 72, 96, True)
n898, xend2 = word("898", xend + 2 * STEP + GAP, 96, False)

wp_svg = ""
for x, y, n in wps:
    wp_svg += f'<path d="M {x:.0f} {y-6:.0f} l 6 6 l -6 6 l -6 -6 z" fill="{INK}" stroke="{MUTED}" stroke-width="1.5"/>'
    wp_svg += f'<text x="{x:.0f}" y="{y+26:.0f}" text-anchor="middle" font-size="10.5" fill="{MUTED}" letter-spacing="1.5">{n}</text>'

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d" font-family="{MONO}">
<title id="t">RRC898</title>
<desc id="d">Computer Engineering student at UPV. UAV avionics, software and AI-powered tools.</desc>
<defs>
  <clipPath id="card"><rect width="{W}" height="{H}" rx="20"/></clipPath>
  <clipPath id="tapeclip"><rect x="72" y="336" width="{W-144}" height="52"/></clipPath>
  <radialGradient id="glow" cx="18%" cy="30%" r="60%"><stop offset="0" stop-color="{AMBER}" stop-opacity=".10"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient>
  <radialGradient id="glow2" cx="82%" cy="40%" r="45%"><stop offset="0" stop-color="{TEAL}" stop-opacity=".07"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></radialGradient>
  <linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".12" stop-color="#fff"/><stop offset=".88" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <mask id="tapefade"><rect x="72" y="330" width="{W-144}" height="64" fill="url(#fade)"/></mask>
  <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1" fill="#242d3a"/></pattern>
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".22"/></pattern>
  <path id="route" d="{PATH}"/>
  <style>
    .px {{ animation: on .5s both; }}
    @keyframes on {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
    .cur {{ animation: blink 1.1s steps(1) infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    .fly {{ stroke-dasharray: {L}; stroke-dashoffset: {L}; animation: fly 11s linear infinite; }}
    @keyframes fly {{ 0% {{ stroke-dashoffset: {L}; }} 82%, 100% {{ stroke-dashoffset: 0; }} }}
    .pulse {{ animation: pulse 2.2s ease-out infinite; transform-origin: 1200px 112px; }}
    @keyframes pulse {{ from {{ opacity: .7; transform: scale(.4); }} to {{ opacity: 0; transform: scale(1.6); }} }}
    .tape {{ animation: slide 80s linear infinite; }}
    @keyframes slide {{ to {{ transform: translateX(-1200px); }} }}
    @media (prefers-reduced-motion: reduce) {{
      .px, .cur, .pulse, .tape {{ animation: none; }}
      .fly {{ animation: none; stroke-dashoffset: 0; }}
    }}
  </style>
</defs>
<g clip-path="url(#card)">
  <rect width="{W}" height="{H}" fill="{INK}"/>
  <rect width="{W}" height="{H}" fill="url(#dots)"/>
  <rect width="{W}" height="{H}" fill="url(#glow)"/>
  <rect width="{W}" height="{H}" fill="url(#glow2)"/>

  <!-- cabecera -->
  <g font-size="12" letter-spacing="2.5" fill="{MUTED}">
    <rect x="72" y="44" width="8" height="8" fill="{AMBER}"/>
    <text x="90" y="52.5">GITHUB.COM/RRC-898</text>
    <text x="{W-72}" y="52.5" text-anchor="end">VALÈNCIA · 39.48°N 0.34°W</text>
  </g>

  <!-- marca -->
  {rrc}
  {n898}

  <!-- lema -->
  <g font-size="19">
    <text x="72" y="266" fill="#e6e1d6">Computer Engineering <tspan fill="{MUTED}">@</tspan> UPV</text>
    <text x="72" y="296" fill="{MUTED}"><tspan fill="{AMBER}">&gt;</tspan> UAV avionics · software · AI-powered tools<tspan class="cur" fill="{AMBER}" dx="6">▍</tspan></text>
  </g>

  <!-- plan de vuelo -->
  <g fill="none" stroke-linecap="round">
    <use href="#route" stroke="#3d4a5c" stroke-width="2" stroke-dasharray="2 8"/>
    <use href="#route" class="fly" stroke="{TEAL}" stroke-width="2"/>
  </g>
  {wp_svg}
  <circle class="pulse" cx="1200" cy="112" r="14" fill="none" stroke="{TEAL}" stroke-width="1.5"/>
  <g fill="{TEAL}">
    <path d="M 13 0 L -9 -8 L -4 0 L -9 8 Z">
      <animateMotion dur="11s" repeatCount="indefinite" rotate="auto" keyPoints="0;1;1" keyTimes="0;0.82;1" calcMode="linear"><mpath href="#route"/></animateMotion>
    </path>
  </g>
  <g font-size="11.5" letter-spacing="1.5" fill="{MUTED}">
    <text x="760" y="104">ALT <tspan fill="#e6e1d6">120 m</tspan></text>
    <text x="760" y="124">GS  <tspan fill="#e6e1d6">18 m/s</tspan></text>
    <text x="760" y="144">HDG <tspan fill="#e6e1d6">074°</tspan></text>
  </g>

  <!-- cinta de rumbo -->
  <line x1="72" y1="336" x2="{W-72}" y2="336" stroke="{LINE}" stroke-width="1.5"/>
  <g clip-path="url(#tapeclip)" mask="url(#tapefade)">
    <g transform="translate(72 336)"><g class="tape">{tape(0)}{tape(1200)}</g></g>
  </g>
  <path d="M {W/2-7} 322 h 14 l -7 10 z" fill="{AMBER}"/>

  <rect width="{W}" height="{H}" fill="url(#scan)"/>
</g>
<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="19.25" fill="none" stroke="#2a3340" stroke-width="1.5"/>
</svg>
'''
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "banner.svg")
open(out, "w").write(svg)
print(out, len(svg), "bytes; L =", L, "; wordmark ends x =", xend2)
