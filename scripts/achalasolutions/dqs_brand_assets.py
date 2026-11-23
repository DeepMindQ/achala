"""Generate the full Achala IT Solutions brand asset set from the traced logo (Wave 1).

Outputs in /home/z/my-project/public/:
  favicon.ico, apple-touch-icon.png, icon-512.png
  og-default.png (1200x630)
  social-linkedin.png (1128x191), social-x.png (1500x500)
  pattern-d.svg (watermark), manifest.json
And in src/app/: icon.svg (favicon: orange block + white 'd' glyph, CHG-005)
"""
import json
import cairosvg
import numpy as np
from PIL import Image
from skimage import measure

ORANGE = "#d20000"
NAVY = "#2b5672"

meta = json.load(open("/home/z/my-project/scripts/achalasolutions/logo_trace.json"))
BLOCK, DOT, NAVYP = meta["block"], meta["dot"], meta["navy"]
W, H = 1000, 184

def logo_group(scale, dx, dy, navy_fill=NAVY, mono=None):
    """Return <g> with the traced logo paths, scaled and translated."""
    mono_fill = mono or navy_fill
    parts = [f'<g transform="translate({dx},{dy}) scale({scale})">']
    parts.append(f'<path fill="{ORANGE}" fill-rule="evenodd" d="{" ".join(BLOCK)}"/>')
    parts.append(f'<path fill="{ORANGE}" d="{" ".join(DOT)}"/>')
    parts.append(f'<path fill="{mono_fill}" fill-rule="evenodd" d="{" ".join(NAVYP)}"/>')
    parts.append("</g>")
    return "".join(parts)

# ── 1. favicon 'd' glyph: trace the white 'd' region from the block crop ──
img = Image.open("/home/z/my-project/upload/achala_logo.png").convert("RGBA")
arr = np.asarray(img).astype(int)
a = arr[..., 3:4] / 255.0
rgb = arr[..., :3] * a + 255 * (1 - a)
orange_m = (np.abs(rgb - np.array([210, 0, 0])).sum(axis=2) < 60)
# 'd' occupies the left of the block: x 40..120 (bowl counter 74..112, stem ~40..56)
crop = orange_m[13:169, 41:123]
white_in_block = ~crop
# kill the antialiasing frame hugging the crop border so only the true glyph remains
white_in_block[0, :] = False
white_in_block[-1, :] = False
white_in_block[:, 0] = False
white_in_block[:, -1] = False
padded = np.pad(white_in_block.astype(float), 1)
dpaths = []
for c in measure.find_contours(padded, 0.5):
    c = measure.approximate_polygon(c, 0.8)
    if len(c) < 3:
        continue
    ys, xs = c[:, 0] - 1, c[:, 1] - 1
    # every white region inside the crop is part of the 'd' glyph (outer shape
    # incl. the ascender that touches the block edge, plus the bowl counter hole);
    # even-odd fill renders outer + hole correctly.
    if (xs.max() - xs.min()) < 8 or (ys.max() - ys.min()) < 8:
        continue  # drop antialiasing slivers only
    dpaths.append("M" + " L".join(f"{p:.1f},{q:.1f}" for q, p in zip(ys, xs)) + " Z")
print("d-glyph paths:", len(dpaths))

# scale 'd' crop (84x158) into a 512 canvas: orange rounded square + centered white d
DS = 512
glyph_scale = 300 / 158  # fit height 300px
gx = (DS - 84 * glyph_scale) / 2
gy = (DS - 158 * glyph_scale) / 2
icon_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {DS} {DS}">
  <rect width="{DS}" height="{DS}" rx="96" fill="{ORANGE}"/>
  <g transform="translate({gx:.0f},{gy:.0f}) scale({glyph_scale:.4f})">
    <path fill="#FFFFFF" fill-rule="evenodd" d="{' '.join(dpaths)}"/>
  </g>
</svg>
'''
open("/home/z/my-project/src/app/icon.svg", "w").write(icon_svg)

# PNG exports of the icon
cairosvg.svg2png(bytestring=icon_svg.encode(), write_to="/home/z/my-project/public/icon-512.png", output_width=512, output_height=512)
cairosvg.svg2png(bytestring=icon_svg.encode(), write_to="/home/z/my-project/public/apple-touch-icon.png", output_width=180, output_height=180)

# favicon.ico (16/32/48) from the 512 render
im512 = Image.open("/home/z/my-project/public/icon-512.png")
im512.save("/home/z/my-project/public/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

# ── 2. OG default image 1200x630 (CHG-018) ────────────────────────────────
def dot_grid(op=0.16):
    return (
        f'<pattern id="dg" width="22" height="22" patternUnits="userSpaceOnUse">'
        f'<circle cx="1.2" cy="1.2" r="1.2" fill="rgba(210, 0, 0,{op})"/></pattern>'
    )

og = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" font-family="DejaVu Sans">
  <defs>
    <linearGradient id="nf" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#3a6983"/><stop offset="0.55" stop-color="{NAVY}"/><stop offset="1" stop-color="#0e2230"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.82" cy="0.1" r="0.9">
      <stop offset="0" stop-color="rgba(210, 0, 0,0.28)"/><stop offset="0.55" stop-color="rgba(210, 0, 0,0)"/>
    </radialGradient>
    {dot_grid()}
  </defs>
  <rect width="1200" height="630" fill="url(#nf)"/>
  <rect width="1200" height="630" fill="url(#glow)"/>
  <rect width="1200" height="630" fill="url(#dg)"/>
  <rect x="80" y="150" width="72" height="8" rx="3" fill="{ORANGE}"/>
  {logo_group(0.52, 80, 210, navy_fill="#FFFFFF")}
  <text x="80" y="475" fill="#FFFFFF" font-size="46" font-weight="bold" letter-spacing="-1">Intelligence, engineered for outcomes.</text>
  <text x="80" y="530" fill="rgba(255,255,255,0.62)" font-size="24">Applied AI · Agentic automation · Data platforms · Cybersecurity · Emerging compute</text>
  <text x="80" y="578" fill="rgba(255,255,255,0.38)" font-size="17" letter-spacing="3">WWW.ACHALASOFT.COM</text>
</svg>
'''
cairosvg.svg2png(bytestring=og.encode(), write_to="/home/z/my-project/public/og-default.png", output_width=1200, output_height=630)

# ── 3. Social banners (CHG-021) ───────────────────────────────────────────
li = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1128 191" font-family="DejaVu Sans">
  <defs>
    <linearGradient id="nf2" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#3a6983"/><stop offset="1" stop-color="{NAVY}"/>
    </linearGradient>
    {dot_grid(0.13)}
  </defs>
  <rect width="1128" height="191" fill="url(#nf2)"/>
  <rect width="1128" height="191" fill="url(#dg)"/>
  {logo_group(0.155, 56, 50, navy_fill="#FFFFFF")}
  <rect x="560" y="72" width="5" height="46" rx="2" fill="{ORANGE}"/>
  <text x="588" y="92" fill="#FFFFFF" font-size="24" font-weight="bold">Intelligence, engineered for outcomes.</text>
  <text x="588" y="118" fill="rgba(255,255,255,0.6)" font-size="14">www.achalasolutions.com</text>
</svg>
'''
cairosvg.svg2png(bytestring=li.encode(), write_to="/home/z/my-project/public/social-linkedin.png", output_width=1128, output_height=191)

xh = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1500 500" font-family="DejaVu Sans">
  <defs>
    <linearGradient id="nf3" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#3a6983"/><stop offset="0.6" stop-color="{NAVY}"/><stop offset="1" stop-color="#0e2230"/>
    </linearGradient>
    <radialGradient id="g3" cx="0.85" cy="0.12" r="0.8">
      <stop offset="0" stop-color="rgba(210, 0, 0,0.25)"/><stop offset="0.6" stop-color="rgba(210, 0, 0,0)"/>
    </radialGradient>
    {dot_grid(0.14)}
  </defs>
  <rect width="1500" height="500" fill="url(#nf3)"/>
  <rect width="1500" height="500" fill="url(#g3)"/>
  <rect width="1500" height="500" fill="url(#dg)"/>
  {logo_group(0.42, 100, 170, navy_fill="#FFFFFF")}
  <rect x="100" y="120" width="64" height="7" rx="3" fill="{ORANGE}"/>
  <text x="100" y="400" fill="#FFFFFF" font-size="34" font-weight="bold">Intelligence, engineered for outcomes.</text>
</svg>
'''
cairosvg.svg2png(bytestring=xh.encode(), write_to="/home/z/my-project/public/social-x.png", output_width=1500, output_height=500)

# ── 4. Watermark pattern asset (CHG-033): tiled 'd' glyph, 4% opacity ────
wm = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 84 158">
  <path fill="rgba(255,255,255,0.05)" fill-rule="evenodd" d="{' '.join(dpaths)}"/>
</svg>
'''
open("/home/z/my-project/public/pattern-d.svg", "w").write(wm)

# ── 5. PWA manifest (CHG-017) ─────────────────────────────────────────────
manifest = {
    "name": "Achala IT Solutions",
    "short_name": "Achala",
    "description": "Achala IT Solutions engineers the intelligence layer of the enterprise.",
    "start_url": "/",
    "display": "browser",
    "background_color": "#FFFFFF",
    "theme_color": "#2b5672",
    "icons": [
        {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "/apple-touch-icon.png", "sizes": "180x180", "type": "image/png", "purpose": "any"},
    ],
}
json.dump(manifest, open("/home/z/my-project/public/manifest.json", "w"), indent=2)

# ── 6. 512px PNG exports of the full lockup (CHG-004) ────────────────────
cairosvg.svg2png(url="/home/z/my-project/public/logo.svg", write_to="/home/z/my-project/public/logo-512.png", output_width=512)
cairosvg.svg2png(url="/home/z/my-project/public/logo-white.svg", write_to="/home/z/my-project/public/logo-white-512.png", output_width=512)

import os
for f in sorted(os.listdir("/home/z/my-project/public")):
    print(f"{os.path.getsize('/home/z/my-project/public/' + f):>9,}  {f}")
