import re, os, json, urllib.request

BASE = "https://www.achalasolutions.com"
DIR = "/home/z/my-project/achala/.research"
os.makedirs(DIR, exist_ok=True)

req = urllib.request.Request(BASE + "/", headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"})
html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", errors="ignore")
open(os.path.join(DIR, "home.html"), "w").write(html)
print("homepage size:", len(html))

def uniq(seq):
    seen, out = set(), []
    for s in seq:
        if s not in seen:
            seen.add(s); out.append(s)
    return out

# links
hrefs = uniq(re.findall(r'href=["\']([^"\']+)["\']', html))
internal = [h for h in hrefs if (h.startswith("/") or "achalasolutions.com" in h) and not any(x in h for x in ["wp-content/uploads/20", ".png", ".jpg", ".jpeg", ".webp", ".svg", ".pdf", "#"])]
print("\nINTERNAL LINKS (%d):" % len(internal))
for h in internal[:60]:
    print(" ", h)

# images
imgs = uniq(re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html))
print("\nIMAGES (%d):" % len(imgs))
for i in imgs[:40]:
    print(" ", i)

# stylesheets
css = uniq(re.findall(r'<link[^>]+rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)["\']', html))
css += uniq(re.findall(r'<link[^>]+href=["\']([^"\']+\.css[^"\']*)["\']', html))
print("\nSTYLESHEETS:")
for c in uniq(css):
    print(" ", c)

# meta images / favicon
for pat in [r'property=["\']og:image["\'][^>]*content=["\']([^"\']+)', r'content=["\']([^"\']+)["\'][^>]*property=["\']og:image["\']',
            r'rel=["\'](?:icon|apple-touch-icon|shortcut icon)["\'][^>]*href=["\']([^"\']+)', r'href=["\']([^"\']+)["\'][^>]*rel=["\'](?:icon|apple-touch-icon)["\']']:
    m = re.findall(pat, html)
    if m:
        print("\nMETA/ICON:", uniq(m)[:6])

# colors inline
colors = re.findall(r'#[0-9a-fA-F]{6}\b', html)
from collections import Counter
print("\nINLINE HEX COLORS:", Counter(c.lower() for c in colors).most_common(15))

# socials
soc = [h for h in hrefs if any(s in h.lower() for s in ["linkedin", "twitter", "facebook", "instagram", "youtube", "x.com"])]
print("\nSOCIAL:", uniq(soc))

# emails / phones
print("\nEMAILS:", uniq(re.findall(r'[\w.+-]+@[\w-]+\.[\w.]+', html)))
print("\nPHONES:", uniq(re.findall(r'\+91[\s\d-]{8,14}|\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b', html)))

# title / og
m = re.search(r'<title>(.*?)</title>', html, re.S)
print("\nTITLE:", m.group(1).strip() if m else None)
for prop in ["og:description", "og:site_name", "description"]:
    m = re.search(r'(?:property|name)=["\']%s["\'][^>]*content=["\']([^"\']+)' % prop, html) or re.search(r'content=["\']([^"\']+)["\'][^>]*(?:property|name)=["\']%s["\']' % prop, html)
    if m:
        print(prop.upper() + ":", m.group(1)[:200])
