#!/usr/bin/env python3
"""Generate the aurora-glass animated GitHub profile README + SVG assets."""
import os, re, math, random

HERE = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(HERE, "icons")
OUT = HERE
ASSETS = os.path.join(OUT, "assets")
os.makedirs(ASSETS, exist_ok=True)

# ---------------------------------------------------------------- palette
BG0, BG1, BG2 = "#05060B", "#0A0E20", "#070A16"
CYAN, BLUE, VIOLET, ICE = "#22D3EE", "#3B82F6", "#8B5CF6", "#7CC4FF"
HEAD = "#EAF1FF"
SUB  = "#9DB2DA"

SPRING = "cubic-bezier(.34,1.56,.64,1)"
SMOOTH = "cubic-bezier(.16,1,.3,1)"

# every section sits on its own dark panel so it looks identical on light & dark themes
TITLE_H = 58
PANEL_TOP, PANEL_BOT = "#0B1020", "#080B16"

def panel_defs():
    return ('<linearGradient id="pnl" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{PANEL_TOP}"/><stop offset="1" stop-color="{PANEL_BOT}"/></linearGradient>'
            '<linearGradient id="stx" x1="0" y1="0" x2="1" y2="0">'
            f'<stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".5" stop-color="{ICE}"/>'
            f'<stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></linearGradient>'
            '<linearGradient id="pbr" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{CYAN}" stop-opacity=".38"/>'
            '<stop offset=".5" stop-color="#ffffff" stop-opacity=".07"/>'
            f'<stop offset="1" stop-color="{VIOLET}" stop-opacity=".38"/></linearGradient>'
            '<pattern id="pdots" width="24" height="24" patternUnits="userSpaceOnUse">'
            '<circle cx="2" cy="2" r="1" fill="#9FC4FF" opacity=".05"/></pattern>'
            '<linearGradient id="phl" x1="0" y1="0" x2="1" y2="0">'
            '<stop offset="0" stop-color="#fff" stop-opacity="0"/>'
            '<stop offset=".5" stop-color="#fff" stop-opacity=".30"/>'
            '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')

def title_css():
    return (f'.stt{{opacity:0;animation:stfu .8s {SPRING} .1s forwards}}'
            '@keyframes stfu{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}'
            f'.stl{{transform-origin:center;transform:scaleX(0);animation:stg 1s {SMOOTH} .35s forwards}}'
            '@keyframes stg{to{transform:scaleX(1)}}')

def panel_rect(W, H):
    return (f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="26" fill="url(#pnl)"/>'
            f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="26" fill="url(#pdots)"/>'
            f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="26" fill="none" '
            'stroke="url(#pbr)" stroke-width="1.2"/>'
            f'<rect x="{W*0.2:.0f}" y="1.2" width="{W*0.6:.0f}" height="1.6" rx="1" fill="url(#phl)"/>')

def title_block(W, label, y=40):
    return (f'<text class="stt" x="{W/2}" y="{y}" text-anchor="middle" '
            'font-family="Segoe UI,Helvetica,Arial,sans-serif" font-size="24" font-weight="800" '
            f'letter-spacing="4" fill="{HEAD}">{label}</text>'
            f'<rect class="stl" x="{W/2-150}" y="{y+12}" width="300" height="2.5" rx="2" fill="url(#stx)"/>')

# ---------------------------------------------------------------- icon io
def load_icon(name):
    """Return (inner_svg, viewbox_max) with monochrome marks recoloured."""
    with open(os.path.join(ICON_DIR, name + ".svg"), "r", encoding="utf-8") as f:
        s = f.read()
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s)
    vmax = float(vb.group(1)) if vb else 128.0
    inner = re.sub(r'^.*?<svg[^>]*>', '', s, count=1, flags=re.S)
    inner = re.sub(r'</svg>\s*$', '', inner, flags=re.S)
    inner = re.sub(r'<title>.*?</title>', '', inner, flags=re.S)
    if name == "github":          # near-black -> white on dark
        inner = inner.replace("#181616", "#ffffff").replace("#181717", "#ffffff")
    if name == "aws":             # monochrome path -> brand amber
        inner = '<g fill="#FF9D2E">' + inner + '</g>'
    if name == "linux":           # monochrome Tux -> brand gold
        inner = '<g fill="#FFD23F">' + inner + '</g>'
    return inner, vmax

STACK = [
    ("cpp","C++"), ("python","Python"), ("pytorch","PyTorch"), ("js","JavaScript"),
    ("react","React"), ("nodejs","Node.js"), ("html","HTML5"), ("css","CSS3"),
    ("linux","Linux"), ("aws","AWS"), ("git","Git"), ("github","GitHub"),
    ("docker","Docker"), ("vscode","VS Code"), ("mysql","MySQL"), ("mongodb","MongoDB"),
]

# ---------------------------------------------------------------- shared defs
def aurora_defs(idp):
    """Reusable gradients / filters / blurred aurora orbs + starfield."""
    random.seed(7)
    stars = []
    for i in range(46):
        x = round(random.uniform(0, 1000), 1)
        y = round(random.uniform(0, 100), 1)  # placeholder, scaled by caller via %
        r = round(random.uniform(0.5, 1.6), 2)
        d = round(random.uniform(0, 4), 2)
        dur = round(random.uniform(2.4, 5.0), 2)
        stars.append((x, y, r, d, dur))
    return stars

# ============================================================ HEADER
def build_header():
    W, H = 1000, 185
    g = []
    g.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
             f'width="100%" role="img" aria-label="Hi, I am Dushyant">')
    g.append('<defs>')
    g.append(f'''<linearGradient id="hbg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#070912"/><stop offset=".5" stop-color="#0B1022"/>
      <stop offset="1" stop-color="#06070F"/></linearGradient>''')
    g.append(f'''<linearGradient id="name" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#2EE6F5"/><stop offset=".35" stop-color="#5FA8FF"/>
      <stop offset=".68" stop-color="#8E8CFF"/><stop offset="1" stop-color="#C07CFF"/></linearGradient>''')
    g.append('<filter id="soft" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="58"/></filter>')
    g.append('<filter id="rsoft" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="20"/></filter>')
    g.append('<filter id="nglow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="7.5"/></filter>')
    g.append('<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">'
             '<circle cx="2" cy="2" r="1" fill="#9FC4FF" opacity=".06"/></pattern>')
    g.append(f'<clipPath id="hclip"><rect width="{W}" height="{H}" rx="22"/></clipPath>')
    g.append(f'''<radialGradient id="vig" cx=".5" cy=".5" r=".7">
      <stop offset=".42" stop-color="#05060B" stop-opacity="0"/>
      <stop offset="1" stop-color="#05060B" stop-opacity=".88"/></radialGradient>''')
    g.append(f'''<linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset=".5" stop-color="#fff" stop-opacity=".8"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>''')
    g.append(f'''<clipPath id="tclip"><text x="{W/2}" y="102" text-anchor="middle"
      font-family="Segoe UI,Helvetica,Arial,sans-serif" font-size="70"
      font-weight="800" letter-spacing="1">Hi, I'm Dushyant</text></clipPath>''')
    g.append('</defs>')

    g.append('<style>')
    g.append(f'''
    .orb{{filter:url(#soft);animation:drift 18s ease-in-out infinite}}
    .o2{{animation-duration:24s;animation-delay:-8s}}
    .o3{{animation-duration:30s;animation-delay:-15s}}
    @keyframes drift{{0%,100%{{transform:translate(0,0)}}33%{{transform:translate(30px,12px)}}
      66%{{transform:translate(-24px,-9px)}}}}
    .star{{fill:#cfe3ff;animation:tw 3.2s ease-in-out infinite}}
    @keyframes tw{{0%,100%{{opacity:.12}}50%{{opacity:.9}}}}
    .title{{opacity:0;animation:fadeUp 1s {SPRING} .15s forwards}}
    @keyframes fadeUp{{from{{opacity:0;transform:translateY(16px)}}to{{opacity:1;transform:translateY(0)}}}}
    .nglow{{animation:bre 4.5s ease-in-out infinite}}
    @keyframes bre{{0%,100%{{opacity:.22}}50%{{opacity:.5}}}}
    .shine{{animation:sweep 5s {SMOOTH} 1.2s infinite}}
    @keyframes sweep{{0%{{transform:translateX(-700px)}}55%,100%{{transform:translateX(700px)}}}}
    .rule{{transform-origin:center;animation:grow 1.1s {SMOOTH} .55s forwards;transform:scaleX(0)}}
    @keyframes grow{{to{{transform:scaleX(1)}}}}
    .rib{{filter:url(#rsoft);animation:ribm 26s ease-in-out infinite}}
    .rib2{{animation-duration:34s;animation-delay:-14s}}
    @keyframes ribm{{0%,100%{{transform:translateX(0)}}50%{{transform:translateX(-46px)}}}}
    .spk{{transform-box:fill-box;transform-origin:center;animation:spt 4.2s ease-in-out infinite}}
    @keyframes spt{{0%,100%{{transform:scale(.45);opacity:.15}}50%{{transform:scale(1);opacity:.95}}}}
    .rdot{{animation:rd 4.2s ease-in-out 1.7s infinite}}
    @keyframes rd{{0%,100%{{transform:translateX(0);opacity:0}}12%,88%{{opacity:1}}50%{{transform:translateX(272px)}}}}
    ''')
    g.append('</style>')

    g.append(f'<rect width="{W}" height="{H}" rx="22" fill="url(#hbg)"/>')
    # dot-grid texture + smooth aurora wash + stars + vignette frame — all clipped
    g.append('<g clip-path="url(#hclip)">')
    g.append(f'<rect width="{W}" height="{H}" fill="url(#dots)"/>')
    g.append(f'<circle class="orb"  cx="410" cy="96"  r="190" fill="{VIOLET}" opacity=".24"/>')
    g.append(f'<circle class="orb o3" cx="512" cy="116" r="170" fill="{BLUE}" opacity=".18"/>')
    g.append(f'<circle class="orb o2" cx="614" cy="96"  r="190" fill="{CYAN}" opacity=".22"/>')
    # aurora ribbons — soft flowing bands behind the name
    g.append(f'<path class="rib" d="M-60,132 C180,84 360,158 520,112 C680,66 860,140 1060,92" '
             f'fill="none" stroke="url(#name)" stroke-width="34" opacity=".10"/>')
    g.append(f'<path class="rib rib2" d="M-60,70 C220,120 420,44 620,96 C780,136 920,72 1060,108" '
             f'fill="none" stroke="url(#name)" stroke-width="22" opacity=".08"/>')
    for x, y, r, d, dur in aurora_defs("h"):
        yy = round(y / 100 * H, 1)
        g.append(f'<circle class="star" cx="{x}" cy="{yy}" r="{r}" '
                 f'style="animation-delay:{d}s;animation-duration:{dur}s"/>')
    # four-point sparkles
    spk = "M0 -6 L1.4 -1.4 L6 0 L1.4 1.4 L0 6 L-1.4 1.4 L-6 0 L-1.4 -1.4 Z"
    for sx, sy, sc, sd in ((150, 52, 1.0, 0), (855, 60, .8, 1.3), (245, 138, .7, 2.1),
                           (760, 132, .9, .6), (500, 34, .65, 2.8)):
        g.append(f'<g transform="translate({sx},{sy}) scale({sc})">'
                 f'<path class="spk" style="animation-delay:{sd}s" d="{spk}" fill="#BFE3FF"/></g>')
    g.append(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')
    g.append('</g>')
    # gradient hairline frame
    g.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="21" fill="none" '
             'stroke="url(#name)" stroke-opacity=".28" stroke-width="1.4"/>')
    # title: soft glow halo + crisp gradient + shine sweep + underline
    g.append('<g class="title">')
    g.append(f'''<text class="nglow" x="{W/2}" y="102" text-anchor="middle" filter="url(#nglow)"
      font-family="Segoe UI,Helvetica,Arial,sans-serif" font-size="70" font-weight="800"
      letter-spacing="1" fill="#3CC9FF">Hi, I'm Dushyant</text>''')
    g.append(f'''<text x="{W/2}" y="102" text-anchor="middle"
      font-family="Segoe UI,Helvetica,Arial,sans-serif" font-size="70" font-weight="800"
      letter-spacing="1" fill="url(#name)">Hi, I'm Dushyant</text>''')
    g.append('<g clip-path="url(#tclip)">'
             f'<rect class="shine" x="0" y="38" width="240" height="90" fill="url(#shine)"/></g>')
    g.append(f'<rect class="rule" x="{W/2-140}" y="126" width="280" height="3" rx="2" fill="url(#name)"/>')
    g.append(f'<circle class="rdot" cx="{W/2-136}" cy="127.5" r="3" fill="#EAF6FF"/>')
    g.append('</g>')
    g.append('</svg>')
    return "\n".join(g)

# ============================================================ SECTION TITLE helper
def section_title(label, w=1000):
    H = 56
    g = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {H}" width="100%" role="img" aria-label="{label}">']
    g.append('<defs>'
             f'<linearGradient id="st" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0" stop-color="{CYAN}" stop-opacity="0"/>'
             f'<stop offset=".5" stop-color="{ICE}"/>'
             f'<stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></linearGradient>'
             '</defs>')
    g.append(f'''<style>
    .t{{opacity:0;animation:fu .8s {SPRING} .1s forwards}}
    @keyframes fu{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:translateY(0)}}}}
    .ln{{transform-origin:center;transform:scaleX(0);animation:g 1s {SMOOTH} .35s forwards}}
    @keyframes g{{to{{transform:scaleX(1)}}}}
    </style>''')
    g.append(f'''<text class="t" x="{w/2}" y="30" text-anchor="middle"
      font-family="Segoe UI,Helvetica,Arial,sans-serif" font-size="26" font-weight="800"
      letter-spacing="4" fill="{HEAD}">{label}</text>''')
    g.append(f'<rect class="ln" x="{w/2-170}" y="44" width="340" height="2.5" rx="2" fill="url(#st)"/>')
    g.append('</svg>')
    return "\n".join(g)

# ============================================================ ACADEMIC
def cap_path():
    # graduation cap glyph (viewBox 0 0 24 24)
    return ('<path d="M11.7 2.1 1.6 6.4c-.5.2-.5.9 0 1.1l10.1 4.3c.2.1.4.1.6 0l8.1-3.4v4.9c-.6.3-1 .9-1 1.7 0 .6.3 1.1.7 1.5l-.9 2.7c-.1.3.1.6.4.6h1.6c.3 0 .5-.3.4-.6l-.9-2.7c.4-.4.7-.9.7-1.5 0-.6-.3-1.1-.7-1.5V7.6l1-.4c.5-.2.5-.9 0-1.1L12.3 2.1c-.2-.1-.4-.1-.6 0Z"/>'
            '<path d="M5 11.2v3.1c0 1.6 3.1 2.9 7 2.9s7-1.3 7-2.9v-3.1l-6.6 2.8c-.3.1-.5.1-.8 0L5 11.2Z"/>')

def build_academic():
    W, CH = 1000, 210
    H = CH + TITLE_H
    cards = [
        ("ABV-IIITM Gwalior", "Integrated M.Tech", "Information Technology", CYAN, BLUE),
        ("IIT Madras",        "BS Degree",         "Data Science &amp; Applications", VIOLET, "#C084FC"),
    ]
    cw, ch, gap = 440, 150, 40
    x0 = (W - (cw * 2 + gap)) / 2
    g = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Academic Journey">']
    g.append('<defs>')
    g.append('<filter id="cshadow" x="-30%" y="-30%" width="160%" height="160%">'
             '<feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000" flood-opacity=".45"/></filter>')
    g.append(panel_defs())
    for i,(_,_,_,c1,c2) in enumerate(cards):
        g.append(f'<linearGradient id="acc{i}" x1="0" y1="0" x2="0" y2="1">'
                 f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>')
        g.append(f'<radialGradient id="ag{i}" cx="0" cy="0" r="1" '
                 f'gradientTransform="translate(40 40) scale(120)">'
                 f'<stop offset="0" stop-color="{c1}" stop-opacity=".22"/>'
                 f'<stop offset="1" stop-color="{c1}" stop-opacity="0"/></radialGradient>')
    g.append('</defs>')
    g.append(f'''<style>
    .card{{opacity:0;animation:in 1s {SPRING} forwards}}
    .c0{{animation-delay:.15s}} .c1{{animation-delay:.35s}}
    @keyframes in{{from{{opacity:0;transform:translateY(22px)}}to{{opacity:1;transform:translateY(0)}}}}
    .acc{{transform-origin:center;animation:bar 3.6s ease-in-out infinite}}
    @keyframes bar{{0%,100%{{opacity:.7}}50%{{opacity:1}}}}
    .cap{{transform-box:fill-box;transform-origin:center;animation:sway 4.5s ease-in-out infinite}}
    @keyframes sway{{0%,100%{{transform:rotate(-6deg)}}50%{{transform:rotate(6deg)}}}}
    .ring{{transform-box:fill-box;transform-origin:center;animation:sp 14s linear infinite;opacity:.5}}
    @keyframes sp{{to{{transform:rotate(360deg)}}}}
    {title_css()}
    </style>''')
    g.append(panel_rect(W, H))
    g.append(title_block(W, "ACADEMIC JOURNEY"))
    g.append(f'<g transform="translate(0,{TITLE_H})">')
    for i,(name, deg, field, c1, c2) in enumerate(cards):
        x = x0 + i * (cw + gap)
        g.append(f'<g class="card c{i}">')
        g.append(f'<rect x="{x}" y="20" width="{cw}" height="{ch}" rx="20" fill="rgba(255,255,255,.04)" '
                 f'stroke="rgba(255,255,255,.10)" stroke-width="1.2" filter="url(#cshadow)"/>')
        g.append(f'<rect x="{x}" y="20" width="{cw}" height="{ch}" rx="20" fill="url(#ag{i})"/>')
        # accent bar
        g.append(f'<rect class="acc" x="{x+14}" y="36" width="5" height="{ch-32}" rx="3" fill="url(#acc{i})"/>')
        # emblem
        ecx, ecy = x + 70, 20 + ch/2
        g.append(f'<circle class="ring" cx="{ecx}" cy="{ecy}" r="30" fill="none" '
                 f'stroke="{c1}" stroke-width="1.6" stroke-dasharray="6 7"/>')
        g.append(f'<circle cx="{ecx}" cy="{ecy}" r="24" fill="rgba(255,255,255,.05)" stroke="{c1}" stroke-opacity=".5"/>')
        g.append(f'<g transform="translate({ecx-14},{ecy-14}) scale(1.18)" fill="{c1}">'
                 f'<g class="cap">{cap_path()}</g></g>')
        # text
        tx = x + 116
        g.append(f'<text x="{tx}" y="{20+ch/2-22}" font-family="Segoe UI,Helvetica,Arial,sans-serif" '
                 f'font-size="22" font-weight="800" fill="{HEAD}">{name}</text>')
        g.append(f'<text x="{tx}" y="{20+ch/2+4}" font-family="Segoe UI,Helvetica,Arial,sans-serif" '
                 f'font-size="14.5" font-weight="700" letter-spacing="1.5" fill="{c2}">{deg.upper()}</text>')
        g.append(f'<text x="{tx}" y="{20+ch/2+28}" font-family="Segoe UI,Helvetica,Arial,sans-serif" '
                 f'font-size="14" font-weight="500" fill="{SUB}">{field}</text>')
        g.append('</g>')
    g.append('</g>')
    g.append('</svg>')
    return "\n".join(g)

# ============================================================ TECH STACK
def build_tech():
    cols, rows = 8, 2
    W = 1000
    mx = 36                       # side margin
    cell_w = (W - 2*mx) / cols
    card = 96
    icon_box = 46
    cell_h = 150
    top = 24
    CH = top + rows * cell_h + 10
    H = CH + TITLE_H

    g = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Tech Stack">']
    g.append('<defs>')
    g.append(f'<linearGradient id="tcard" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="#ffffff" stop-opacity=".14"/>'
             f'<stop offset="1" stop-color="#ffffff" stop-opacity=".035"/></linearGradient>')
    g.append(f'<linearGradient id="tpanel" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="#ffffff" stop-opacity=".045"/>'
             f'<stop offset="1" stop-color="#ffffff" stop-opacity=".015"/></linearGradient>')
    BRAND = ["#659AD2","#FFD845","#EE4C2C","#F7DF1E","#61DAFB","#83CD29","#E44D26","#2965F1",
             "#FFD23F","#FF9D2E","#F05033","#E6EDF3","#2496ED","#22A7F2","#3E9BCD","#4FAA41"]
    for bi, bc in enumerate(BRAND):
        g.append(f'<radialGradient id="tg{bi}" cx=".5" cy=".5" r=".5">'
                 f'<stop offset="0" stop-color="{bc}" stop-opacity=".55"/>'
                 f'<stop offset="1" stop-color="{bc}" stop-opacity="0"/></radialGradient>')
    g.append('<filter id="ts" x="-40%" y="-40%" width="180%" height="180%">'
             '<feDropShadow dx="0" dy="5" stdDeviation="7" flood-color="#000" flood-opacity=".45"/></filter>')
    g.append(panel_defs())
    g.append('</defs>')

    css = [f'''
    .tile{{opacity:0;animation:pop .75s {SPRING} forwards}}
    @keyframes pop{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:translateY(0)}}}}
    .float{{animation:fl 3.4s ease-in-out infinite}}
    @keyframes fl{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-7px)}}}}
    .ico{{transform-box:fill-box;transform-origin:center;animation:sw 5s ease-in-out infinite}}
    @keyframes sw{{0%,100%{{transform:rotate(-5deg)}}50%{{transform:rotate(5deg)}}}}
    .halo{{transform-box:fill-box;transform-origin:center;animation:br 3.6s ease-in-out infinite}}
    @keyframes br{{0%,100%{{opacity:.0;transform:scale(.7)}}50%{{opacity:.8;transform:scale(1)}}}}
    .lbl{{opacity:0;animation:lf .6s ease forwards}}
    @keyframes lf{{to{{opacity:1}}}}
    ''']
    bodies = []
    for idx,(key,label) in enumerate(STACK):
        col = idx % cols
        row = idx // cols
        cx = mx + col*cell_w + cell_w/2
        cy = top + row*cell_h + cell_h/2 - 6
        inner, vmax = load_icon(key)
        s = icon_box / vmax
        ix = cx - icon_box/2
        iy = cy - 14 - icon_box/2
        d_enter = round(0.08*idx + 0.1, 2)
        d_float = round(-0.16*idx, 2)
        d_sway  = round(-0.22*idx, 2)
        d_halo  = round(0.12*idx, 2)
        css.append(f'.e{idx}{{animation-delay:{d_enter}s}}'
                   f'.f{idx}{{animation-delay:{d_float}s}}'
                   f'.s{idx}{{animation-delay:{d_sway}s}}'
                   f'.h{idx}{{animation-delay:{d_halo}s}}'
                   f'.l{idx}{{animation-delay:{round(d_enter+0.35,2)}s}}')
        b = [f'<g class="tile e{idx}">']
        b.append(f'<g class="float f{idx}">')
        # card
        b.append(f'<rect x="{cx-card/2:.1f}" y="{cy-card/2-8:.1f}" width="{card}" height="{card}" rx="22" '
                 f'fill="url(#tcard)" stroke="rgba(255,255,255,.20)" stroke-width="1.2" filter="url(#ts)"/>')
        b.append(f'<rect x="{cx-card/2+16:.1f}" y="{cy-card/2-6:.1f}" width="{card-32}" height="2" rx="1" '
                 f'fill="#ffffff" opacity=".22"/>')
        # halo
        b.append(f'<circle class="halo h{idx}" cx="{cx:.1f}" cy="{cy-14:.1f}" r="34" fill="url(#tg{idx})"/>')
        # icon (positioned via attribute transform; inner sway via css child)
        b.append(f'<g transform="translate({ix:.2f},{iy:.2f}) scale({s:.4f})">'
                 f'<g class="ico s{idx}">{inner}</g></g>')
        # label
        b.append(f'<text class="lbl l{idx}" x="{cx:.1f}" y="{cy+card/2-6:.1f}" text-anchor="middle" '
                 f'font-family="Segoe UI,Helvetica,Arial,sans-serif" font-size="12.5" font-weight="700" '
                 f'letter-spacing=".4" fill="{SUB}">{label}</text>')
        b.append('</g></g>')
        bodies.append("\n".join(b))
    g.append('<style>' + "\n".join(css) + title_css() + '</style>')
    g.append(panel_rect(W, H))
    g.append(title_block(W, "TECH STACK"))
    g.append(f'<g transform="translate(0,{TITLE_H})">')
    g.extend(bodies)
    g.append('</g>')
    g.append('</svg>')
    return "\n".join(g)

# ============================================================ FOOTER WAVE
def build_footer():
    W, H = 1000, 96
    g = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="">']
    g.append('<defs>'
             f'<linearGradient id="wv" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0" stop-color="{VIOLET}"/><stop offset=".5" stop-color="{BLUE}"/>'
             f'<stop offset="1" stop-color="{CYAN}"/></linearGradient>'
             + panel_defs() +
             f'<clipPath id="fclip"><rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="26"/></clipPath></defs>')
    g.append('''<style>
    .w{animation:mv 9s linear infinite}
    .w2{animation:mv 13s linear infinite reverse;opacity:.5}
    .w3{animation:mv 19s linear infinite;opacity:.3}
    @keyframes mv{from{transform:translateX(0)}to{transform:translateX(-500px)}}
    </style>''')
    g.append(panel_rect(W, H))
    wave = ("M0,54 C125,28 250,78 500,54 C750,28 875,78 1000,54 "
            "C1250,28 1375,78 1500,54 L1500,96 L0,96 Z")
    g.append('<g clip-path="url(#fclip)">')
    g.append(f'<path class="w" d="{wave}" fill="url(#wv)" opacity=".85"/>')
    g.append(f'<path class="w2" d="{wave}" fill="url(#wv)"/>')
    wave3 = ("M0,64 C125,44 250,84 500,64 C750,44 875,84 1000,64 "
             "C1250,44 1375,84 1500,64 L1500,96 L0,96 Z")
    g.append(f'<path class="w3" d="{wave3}" fill="url(#wv)"/>')
    g.append('</g>')
    g.append('</svg>')
    return "\n".join(g)

# ============================================================ FOCUS
def glyph(kind):
    # simple line-art icons in a 0 0 24 24 box, stroke=currentColor
    if kind == "ml":   # neural net
        return ('<g fill="none" stroke-width="1.6" stroke-linecap="round">'
                '<circle cx="4" cy="6" r="2"/><circle cx="4" cy="18" r="2"/>'
                '<circle cx="12" cy="12" r="2.2"/><circle cx="20" cy="6" r="2"/>'
                '<circle cx="20" cy="18" r="2"/>'
                '<path d="M6 6.8 10 11M6 17.2 10 13M14 11 18 6.8M14 13 18 17.2"/></g>')
    if kind == "data": # bars
        return ('<g stroke-width="1.6" stroke-linecap="round" fill="none">'
                '<path d="M4 20V11M10 20V5M16 20V14M22 20V8"/></g>')
    if kind == "sys":  # stacked layers
        return ('<g fill="none" stroke-width="1.6" stroke-linejoin="round">'
                '<path d="M12 3 22 8 12 13 2 8Z"/><path d="M2 13 12 18 22 13"/>'
                '<path d="M2 17 12 22 22 17"/></g>')
    if kind == "ai":   # sparkle — generative AI
        return ('<g fill="none" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round">'
                '<path d="M11 2.5 C11.6 8.2 14.3 10.9 20 11.5 C14.3 12.1 11.6 14.8 11 20.5 '
                'C10.4 14.8 7.7 12.1 2 11.5 C7.7 10.9 10.4 8.2 11 2.5 Z"/>'
                '<path d="M19 3 C19.2 4.9 19.6 5.3 21.5 5.5 C19.6 5.7 19.2 6.1 19 8 '
                'C18.8 6.1 18.4 5.7 16.5 5.5 C18.4 5.3 18.8 4.9 19 3 Z"/></g>')
    if kind == "doc":  # research paper
        return ('<g fill="none" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round">'
                '<path d="M6 3h8l4 4v14H6Z"/><path d="M14 3v4h4"/>'
                '<path d="M9 12h6M9 15h6M9 18h4"/></g>')
    # oss: git branch
    return ('<g fill="none" stroke-width="1.6" stroke-linecap="round">'
            '<circle cx="6" cy="5" r="2.2"/><circle cx="6" cy="19" r="2.2"/>'
            '<circle cx="18" cy="8" r="2.2"/>'
            '<path d="M6 7.2V17M6 12c8 0 10-1.4 10-4"/></g>')

def build_focus():
    items = [
        ("Machine Learning",    "models &amp; PyTorch", CYAN, "ml"),
        ("Generative AI",       "LLMs &amp; RAG",       BLUE, "ai"),
        ("Data Science",        "geospatial analytics", VIOLET, "data"),
        ("Distributed Systems", "swarms &amp; edge",    "#C084FC", "sys"),
    ]
    W, CH = 1000, 156
    H = CH + TITLE_H
    n = len(items)
    mx, gap = 30, 22
    cw = (W - 2*mx - gap*(n-1)) / n
    ch, y0 = 116, 20
    g = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Focus Areas">']
    g.append('<defs>')
    g.append('<filter id="fsh" x="-30%" y="-30%" width="160%" height="160%">'
             '<feDropShadow dx="0" dy="5" stdDeviation="8" flood-color="#000" flood-opacity=".4"/></filter>')
    g.append(panel_defs())
    for i,(_,_,c,_2) in enumerate(items):
        g.append(f'<radialGradient id="fg{i}" cx="1" cy="0" r="1.2" gradientTransform="translate(0 0)">'
                 f'<stop offset="0" stop-color="{c}" stop-opacity=".20"/>'
                 f'<stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>')
    g.append('</defs>')
    g.append(f'''<style>
    .fc{{opacity:0;animation:fin .9s {SPRING} forwards}}
    @keyframes fin{{from{{opacity:0;transform:translateY(20px)}}to{{opacity:1;transform:translateY(0)}}}}
    .fbar{{transform-origin:center;animation:fb 3.4s ease-in-out infinite}}
    @keyframes fb{{0%,100%{{opacity:.65}}50%{{opacity:1}}}}
    .fg{{transform-box:fill-box;transform-origin:center;animation:ff 4.6s ease-in-out infinite}}
    @keyframes ff{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-5px)}}}}
    {title_css()}
    </style>''')
    g.append(panel_rect(W, H))
    g.append(title_block(W, "FOCUS AREAS"))
    g.append(f'<g transform="translate(0,{TITLE_H})">')
    for i,(title, sub, c, k) in enumerate(items):
        x = mx + i*(cw+gap)
        g.append(f'<g class="fc" style="animation-delay:{round(.12*i+.1,2)}s">')
        g.append(f'<rect x="{x:.1f}" y="{y0}" width="{cw:.1f}" height="{ch}" rx="18" '
                 f'fill="rgba(255,255,255,.05)" stroke="rgba(255,255,255,.12)" stroke-width="1.1" filter="url(#fsh)"/>')
        g.append(f'<rect x="{x:.1f}" y="{y0}" width="{cw:.1f}" height="{ch}" rx="18" fill="url(#fg{i})"/>')
        g.append(f'<rect class="fbar" x="{x+13:.1f}" y="{y0+14}" width="4" height="{ch-28}" rx="2" fill="{c}"/>')
        # glyph
        gx, gy = x + cw - 46, y0 + 18
        g.append(f'<g transform="translate({gx:.1f},{gy}) scale(1.25)" stroke="{c}" color="{c}">'
                 f'<g class="fg" style="animation-delay:{round(-0.3*i,2)}s">{glyph(k)}</g></g>')
        g.append(f'<text x="{x+30:.1f}" y="{y0+ch-42}" font-family="Segoe UI,Helvetica,Arial,sans-serif" '
                 f'font-size="17.5" font-weight="800" fill="{HEAD}">{title}</text>')
        g.append(f'<text x="{x+30:.1f}" y="{y0+ch-20}" font-family="Segoe UI,Helvetica,Arial,sans-serif" '
                 f'font-size="12.5" font-weight="600" letter-spacing=".3" fill="{SUB}">{sub}</text>')
        g.append('</g>')
    g.append('</g>')
    g.append('</svg>')
    return "\n".join(g)

# ============================================================ CONNECT
def build_connect():
    W, H = 1000, 86
    g = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Let us connect">']
    g.append('<defs>' + panel_defs() + '</defs>')
    g.append(f'<style>{title_css()}</style>')
    g.append(panel_rect(W, H))
    g.append(title_block(W, "LET'S CONNECT", y=46))
    g.append('</svg>')
    return "\n".join(g)

# ---------------------------------------------------------------- write
STATIC_OVERRIDE = (
    "*{animation:none!important}"
    ".tile,.title,.tag,.lbl,.card,.t,.star,.dot,.fc,.stt{opacity:1!important}"
    ".rule,.ln,.stl{transform:scaleX(1)!important}"
    ".halo{opacity:.55!important}.shine{opacity:0!important}.orb{opacity:.5!important}"
)
ASSETS_STATIC = os.path.join(OUT, "assets_static")
os.makedirs(ASSETS_STATIC, exist_ok=True)

def w(path, content):
    with open(os.path.join(ASSETS, path), "w", encoding="utf-8") as f:
        f.write(content)
    static = content.replace(
        "</style>",
        STATIC_OVERRIDE + '</style><rect width="100%" height="100%" fill="#0d1117"/>', 1)
    with open(os.path.join(ASSETS_STATIC, path), "w", encoding="utf-8") as f:
        f.write(static)

w("header.svg", build_header())
w("academic.svg", build_academic())
w("tech.svg", build_tech())
w("focus.svg", build_focus())
w("connect.svg", build_connect())
w("footer.svg", build_footer())

USER = "medushyant"
# themed dynamic-card params (transparent bg → blends with profile dark)
TITLE_C, TEXT_C, ICON_C, ACCENT = "22D3EE", "9DB2DA", "8B5CF6", "7CC4FF"
stats = (f"https://github-readme-stats.vercel.app/api?username={USER}"
         f"&show_icons=true&count_private=true&include_all_commits=true"
         f"&bg_color=00000000&title_color={TITLE_C}&text_color={TEXT_C}&icon_color={ICON_C}&hide_border=true")
langs = (f"https://github-readme-stats.vercel.app/api/top-langs/?username={USER}"
         f"&layout=compact&langs_count=10&bg_color=00000000&title_color={TITLE_C}&text_color={TEXT_C}&hide_border=true")
streak = (f"https://github-readme-streak-stats.herokuapp.com/?user={USER}"
          f"&background=00000000&hide_border=true&stroke={ICON_C}&ring={TITLE_C}&fire={ICON_C}"
          f"&currStreakLabel={TITLE_C}&sideLabels={TEXT_C}&dates=64748B&currStreakNum=EAF1FF&sideNums=EAF1FF&dayNums={TEXT_C}")
graph = (f"https://github-readme-activity-graph.vercel.app/graph?username={USER}"
         f"&bg_color=00000000&color={ACCENT}&line={ICON_C}&point={TITLE_C}&area_color={ICON_C}&area=true&hide_border=true&custom_title=Contribution%20Activity")
trophy = (f"https://github-profile-trophy.vercel.app/?username={USER}"
          f"&theme=onedark&no-frame=true&no-bg=true&column=7&margin-w=6&margin-h=6")
views = (f"https://komarev.com/ghpvc/?username={USER}&color=8b5cf6&style=for-the-badge&label=PROFILE+VIEWS")
followers = (f"https://img.shields.io/github/followers/{USER}?style=for-the-badge&color=22d3ee&labelColor=05060B&logo=github&logoColor=22d3ee")
stars = (f"https://img.shields.io/github/stars/{USER}?style=for-the-badge&color=8b5cf6&labelColor=05060B&logo=github&logoColor=8b5cf6&label=TOTAL+STARS")
EMAIL = "imt_2023032@iiitm.ac.in"
_mail_msg = EMAIL.replace("_", "__").replace("@", "%40")   # shields.io escaping
b_gh = "https://img.shields.io/badge/GitHub-medushyant-22d3ee?style=for-the-badge&logo=github&logoColor=white&labelColor=05060B"
b_mail = f"https://img.shields.io/badge/{_mail_msg}-8b5cf6?style=for-the-badge&logo=gmail&logoColor=white&labelColor=05060B"
snake = f"https://raw.githubusercontent.com/{USER}/{USER}/output/github-snake-dark.svg"
# Snake needs the GitHub Action in .github/workflows/snake.yml (requires a token with
# `workflow` scope to push, or add it via the GitHub web UI). Flip to True once enabled.
INCLUDE_SNAKE = False
snake_block = (f'<img src="{snake}" alt="Contribution snake" width="96%"/>\n\n<br/>\n\n'
               if INCLUDE_SNAKE else "")

readme = f'''<div align="center">

<img src="./assets/header.svg" alt="Hi, I'm Dushyant" width="100%"/>

<img src="./assets/academic.svg" alt="Academic Journey" width="100%"/>

<img src="./assets/tech.svg" alt="Tech Stack" width="100%"/>

<img src="./assets/focus.svg" alt="Focus Areas" width="100%"/>

<img src="./assets/connect.svg" alt="Let's Connect" width="100%"/>

<a href="https://github.com/{USER}"><img src="{b_gh}" alt="GitHub"/></a>
&nbsp;&nbsp;
<a href="mailto:{EMAIL}"><img src="{b_mail}" alt="Email"/></a>

<img src="./assets/footer.svg" alt="" width="100%"/>

</div>
'''
with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme)

print("built:", sorted(os.listdir(ASSETS)))
print("readme bytes:", len(readme))
