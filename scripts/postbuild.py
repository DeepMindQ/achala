#!/usr/bin/env python3
"""Post-export fixes:
   1. /why-achala-soft/ -> /why-achala/ redirect stub (meta refresh + canonical)
   2. Verify gen images exist in out/ (basePath regression guard)
   Usage: python3 scripts/postbuild.py [outdir]"""
import os, re, sys

out = sys.argv[1] if len(sys.argv) > 1 else '/home/z/my-project/site/out'

# 1. redirect stub (basePath-aware)
bp = '/achala' if os.path.basename(os.path.normpath(out)) == 'out-gh' else ''
rd = os.path.join(out, 'why-achala-soft')
os.makedirs(rd, exist_ok=True)
with open(os.path.join(rd, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Redirecting… | Achala IT Solutions</title>
<meta name="robots" content="noindex,follow">
<link rel="canonical" href="https://www.achalasolutions.com/why-achala/">
<meta http-equiv="refresh" content="0; url={bp}/why-achala/">
<script>window.location.replace('{bp}/why-achala/');</script>
</head><body>
<p>This page moved to <a href="{bp}/why-achala/">{bp}/why-achala/</a>.</p>
</body></html>""")
print('redirect stub written:', os.path.join(rd, 'index.html'))

# 2. gen image guard
gen = os.path.join(out, 'images', 'gen')
pngs = [f for f in os.listdir(gen) if f.endswith('.png')] if os.path.isdir(gen) else []
assert len(pngs) >= 25, f'gen images missing in {out}: found {len(pngs)}'
print(f'gen image guard OK ({len(pngs)} images)')

# 3. all internal HTML img srcs resolve (regression: images-not-rendering bug)
import glob
htmls = glob.glob(os.path.join(out, '**', '*.html'), recursive=True)
bad = 0
checked = 0
for h in htmls:
    src = open(h, encoding='utf-8', errors='ignore').read()
    for m in re.finditer(r'<img[^>]*?src="([^"]+)"', src):
        s = m.group(1)
        checked += 1
        if s.startswith('http'):
            continue
        rel = s.lstrip('/').split('?')[0]
        if rel.startswith('achala/'):
            rel = rel[len('achala/'):]  # gh-pages basePath: URL /achala/x maps to repo-root x
        fp = os.path.join(out, rel)
        if not os.path.exists(fp):
            bad += 1
            print('BROKEN:', h.replace(out, ''), '->', s)
print(f'img src check: {checked} refs, {bad} broken')
assert bad == 0
print('POSTBUILD OK')
