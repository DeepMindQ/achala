"""Vectorize achala_logo.png into crisp multi-layer SVG (Wave 1, CHG-002/004).

Layers:
  orange  #d20000 -> the block (with white 'achala' cut out) + the 'o' dot of 'software'
  navy    #2b5672 -> the 'software' wordmark letters
Outputs:
  public/logo.svg (full color), public/logo-white.svg (reversed: white wordmark),
  public/logo-mono.svg (single navy), plus the viewBox metadata JSON used by Logo.tsx.
"""
import json
import numpy as np
from PIL import Image
from skimage import measure

ORANGE = (210, 0, 0)
NAVY = (43, 86, 114)

img = Image.open("/home/z/my-project/upload/achala_logo.png").convert("RGBA")
arr = np.asarray(img).astype(int)
h, w = arr.shape[:2]

# alpha compositing over white for robust masks
a = arr[..., 3:4] / 255.0
rgb = arr[..., :3] * a + 255 * (1 - a)

def mask_near(color, tol=60):
    d = np.abs(rgb - np.array(color)).sum(axis=2)
    return d < tol

orange_m = mask_near(ORANGE)
navy_m = mask_near(NAVY, tol=90)

def contours_to_paths(mask, eps=0.9):
    """Return SVG path 'd' for all filled regions of mask (holes handled by even-odd)."""
    padded = np.pad(mask.astype(float), 1)
    cs = measure.find_contours(padded, 0.5)
    paths = []
    for c in cs:
        c = measure.approximate_polygon(c, eps)
        if len(c) < 3:
            continue
        pts = [(x - 1, y - 1) for y, x in c]  # find_contours returns (row, col)
        seg = "M" + " L".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts) + " Z"
        paths.append(seg)
    return paths

def poly_area(path_pts):
    x = path_pts[:, 1] - 1
    y = path_pts[:, 0] - 1
    return 0.5 * abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

# split orange layer: the block (plus letter holes inside it) vs the 'o' dot of 'software'
orange_cs = [c for c in measure.find_contours(np.pad(orange_m.astype(float), 1), 0.5)]
block_paths, dot_paths = [], []
BLOCK_RIGHT = 460  # block spans x 40..428; wordmark starts ~490
for c in orange_cs:
    cs = measure.approximate_polygon(c, 0.9)
    if len(cs) < 3:
        continue
    area = poly_area(cs)
    ys, xs = cs[:, 0] - 1, cs[:, 1] - 1
    cx = (xs.min() + xs.max()) / 2
    seg = "M" + " L".join(f"{p:.1f},{q:.1f}" for q, p in zip(ys, xs)) + " Z"
    if area > (h * w * 0.08):
        block_paths.append(seg)          # the block itself
    elif cx < BLOCK_RIGHT:
        block_paths.append(seg)          # letter holes / glyphs inside the block
    else:
        dot_paths.append(seg)            # the orange 'o' dot of 'software'

navy_paths = contours_to_paths(navy_m)

def svg(paths_orange, paths_dot, paths_navy, navy_fill="#2b5672"):
    body = []
    if paths_orange:
        body.append(
            f'<path fill="#d20000" fill-rule="evenodd" d="{" ".join(paths_orange)}"/>'
        )
    if paths_dot:
        body.append(
            f'<g class="logo-dot"><path fill="#d20000" d="{" ".join(paths_dot)}"/></g>'
        )
    if paths_navy:
        body.append(
            f'<path fill="{navy_fill}" fill-rule="evenodd" d="{" ".join(paths_navy)}"/>'
        )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="Achala IT Solutions">\n  ' + "\n  ".join(body) + "\n</svg>\n"
    )

out = "/home/z/my-project/public/"
full = svg(block_paths, dot_paths, navy_paths)
reversed_white = svg(block_paths, dot_paths, navy_paths, navy_fill="#FFFFFF")
mono = svg([], dot_paths, navy_paths, navy_fill="#2b5672")  # mono navy: navy only
# mono variant: navy block silhouette is not available; use navy for both layers
mono = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="Achala IT Solutions">\n  <path fill="#2b5672" fill-rule="evenodd" d="{" ".join(block_paths)}"/><path fill="#2b5672" d="{" ".join(navy_paths)}"/>\n</svg>\n'

open(out + "logo.svg", "w").write(full)
open(out + "logo-white.svg", "w").write(reversed_white)
open(out + "logo-mono.svg", "w").write(mono)

meta = {
    "viewBox": f"0 0 {w} {h}",
    "block": block_paths,
    "dot": dot_paths,
    "navy": navy_paths,
}
json.dump(meta, open("/home/z/my-project/scripts/achalasolutions/logo_trace.json", "w"))
print(f"block paths: {len(block_paths)}, dot paths: {len(dot_paths)}, navy paths: {len(navy_paths)}, viewBox 0 0 {w} {h}")
import os
for f in ["logo.svg", "logo-white.svg", "logo-mono.svg"]:
    print(f, os.path.getsize(out + f), "bytes")
