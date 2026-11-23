"""Generate the Achala brand asset set from the real logo pulled from achalasolutions.com."""
import os
from PIL import Image, ImageDraw, ImageFont

RES = "/home/z/my-project/achala/.research"
PUB = "/home/z/my-project/achala/site/public"
os.makedirs(PUB, exist_ok=True)

src = Image.open(os.path.join(RES, "logo.png")).convert("RGBA")   # 440x171, transparent
fav = Image.open(os.path.join(RES, "favicon.png")).convert("RGBA")  # 48x48 white bg, red mark
W, H = src.size
print("logo", src.size, "favicon", fav.size)

RED = (210, 0, 0, 255)      # #d20000
GRAY = (137, 137, 137, 255) # #898989
STEEL = (43, 86, 114, 255)  # #2b5672
WHITE = (255, 255, 255, 255)


def recolor(img, map_fn):
    out = Image.new("RGBA", img.size)
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b, a = img.getpixel((x, y))
            if a == 0:
                continue
            out.putpixel((x, y), map_fn(r, g, b, a))
    return out


def is_grayish(r, g, b):
    return abs(r - g) < 30 and abs(g - b) < 30 and r > 60

# 1. canonical logo (as downloaded)
src.save(os.path.join(PUB, "achala-logo.png"))

# 2. reversed: wordmark gray -> white, red mark stays
white_v = recolor(src, lambda r, g, b, a: (255, 255, 255, a) if is_grayish(r, g, b) else (r, g, b, a))
white_v.save(os.path.join(PUB, "achala-logo-white.png"))

# 3. mono: everything -> steel blue
mono_v = recolor(src, lambda r, g, b, a: STEEL)
mono_v.save(os.path.join(PUB, "achala-logo-mono.png"))

# 4. SVG wrappers embedding the PNGs (drop-in replacements for logo.svg etc.)
def svg_wrap(png, viewBox_w, viewBox_h):
    import base64
    b64 = base64.b64encode(open(png, "rb").read()).decode()
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">'
            '<image href="data:image/png;base64,%s" width="%d" height="%d"/></svg>'
            % (viewBox_w, viewBox_h, viewBox_w, viewBox_h, b64, viewBox_w, viewBox_h))

open(os.path.join(PUB, "logo.svg"), "w").write(svg_wrap(os.path.join(PUB, "achala-logo.png"), W, H))
open(os.path.join(PUB, "logo-white.svg"), "w").write(svg_wrap(os.path.join(PUB, "achala-logo-white.png"), W, H))
open(os.path.join(PUB, "logo-mono.svg"), "w").write(svg_wrap(os.path.join(PUB, "achala-logo-mono.png"), W, H))

# 5. icon set: white rounded square + red mark (from favicon art, upscaled cleanly)
# favicon 48x48 is the mark on white; upscale to 512 with padding
mark512 = fav.resize((512, 512), Image.LANCZOS).convert("RGBA")
mark512.save(os.path.join(PUB, "icon-512.png"))
mark180 = fav.resize((180, 180), Image.LANCZOS).convert("RGBA")
mark180.save(os.path.join(PUB, "apple-touch-icon.png"))
mark256 = fav.resize((256, 256), Image.LANCZOS).convert("RGBA")
mark256.save(os.path.join(PUB, "logo-512.png"))
mark256.save(os.path.join(PUB, "logo-white-512.png"))
# favicon.ico multi-size
fav.resize((48, 48), Image.LANCZOS).save(os.path.join(PUB, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
# icon.svg embedding the 48px art
import base64
b64 = base64.b64encode(open(os.path.join(RES, "favicon.png"), "rb").read()).decode()
open(os.path.join(PUB, "icon.svg"), "w").write(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48">'
    '<image href="data:image/png;base64,%s" width="48" height="48"/></svg>' % b64)

# 6. OG image 1200x630 — white field, red mark, steel-blue tagline
og = Image.new("RGB", (1200, 630), (255, 255, 255))
d = ImageDraw.Draw(og)
d.rectangle([0, 0, 1200, 14], fill=RED)          # top brand bar
# logo centered, width 420
lw = 420
lh = round(lw * H / W)
logo_big = src.resize((lw, lh), Image.LANCZOS)
og.paste(logo_big, ((1200 - lw) // 2, 170), logo_big)
try:
    f_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 44)
    f_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 26)
except Exception:
    f_big = f_sm = ImageFont.load_default()
tag1 = "Transforming industries through AI acceleration"
w1 = d.textlength(tag1, font=f_big)
d.text(((1200 - w1) / 2, 380), tag1, font=f_big, fill=STEEL)
tag2 = "AI-first  ·  Platform-driven  ·  Full-cycle product engineering"
w2 = d.textlength(tag2, font=f_sm)
d.text(((1200 - w2) / 2, 460), tag2, font=f_sm, fill=GRAY)
og.save(os.path.join(PUB, "og-default.png"))

# 7. report
for f in sorted(os.listdir(PUB)):
    if f in {"achala-logo.png", "achala-logo-white.png", "achala-logo-mono.png", "logo.svg",
             "logo-white.svg", "logo-mono.svg", "icon-512.png", "apple-touch-icon.png",
             "logo-512.png", "logo-white-512.png", "favicon.ico", "icon.svg", "og-default.png"}:
        print("  OK %s (%d bytes)" % (f, os.path.getsize(os.path.join(PUB, f))))
