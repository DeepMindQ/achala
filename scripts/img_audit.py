#!/usr/bin/env python3
"""Audit image references across the built static site.
Checks every <img src>, srcset entry, og:image and CSS url() found in HTML,
then verifies whether each target file exists in:
  - out/    (root-context build served on port 4173)
  - out-gh/ (basePath=/achala build served on github.io/achala/)
Reports missing files grouped by path.
"""
import os, re, sys, json
from collections import Counter
from html.parser import HTMLParser

OUT = "/home/z/my-project/site/out"
OUT_GH = "/home/z/my-project/site/out-gh"

class ImgParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.imgs = []      # (tag, attrs dict)
    def handle_starttag(self, tag, attrs):
        if tag in ("img", "source", "image"):
            d = dict(attrs)
            self.imgs.append((tag, d))

def extract(html):
    p = ImgParser()
    try:
        p.feed(html)
    except Exception:
        pass
    refs = []
    for tag, d in p.imgs:
        for k in ("src", "xlink:href", "href", "srcset"):
            v = d.get(k)
            if v and not v.startswith(("#", "data:", "javascript:")):
                refs.append(v.split()[0] if k == "srcset" else v)
    # og:image / twitter:image meta
    for m in re.finditer(r'(?:property|name)="(?:og:image|twitter:image)"[^>]*content="([^"]+)"', html):
        refs.append(m.group(1))
    # css url()
    for m in re.finditer(r'url\((["\']?)([^)"\']+)\1\)', html):
        u = m.group(2)
        if not u.startswith(("data:", "#")):
            refs.append(u)
    return refs

def main():
    img_re = re.compile(r"\.(png|jpe?g|webp|avif|gif|svg|ico)(\?|$)", re.I)
    missing_root, missing_gh = Counter(), Counter()
    total_refs, pages_with_imgs, files_seen = 0, set(), Counter()
    examples = {}
    count = 0
    for dirpath, _, files in os.walk(OUT):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            count += 1
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, OUT)
            html = open(path, encoding="utf-8", errors="ignore").read()
            refs = [r for r in extract(html) if img_re.search(r)]
            if refs:
                pages_with_imgs.add(rel)
            for r in refs:
                total_refs += 1
                base = r.split("?")[0].split("#")[0]
                # resolve relative refs against page dir
                if base.startswith("/"):
                    cand_root = OUT + base
                else:
                    cand_root = os.path.normpath(os.path.join(os.path.dirname(path), base))
                if not os.path.exists(cand_root):
                    key = base
                    missing_root[key] += 1
                    examples.setdefault(key, rel)
                # gh context: root-absolute URLs need the /achala prefix to be served
                if base.startswith("/") and not base.startswith("/achala/"):
                    gh_path = OUT_GH + base  # unprefixed -> 404 on github.io/achala/
                    if not os.path.exists(gh_path.replace("/out-gh", "/out-gh")):
                        pass  # file presence in out-gh at unprefixed path is irrelevant; URL is broken regardless
                    missing_gh["UNPREFIXED:" + base] += 1
    print(f"scanned pages: {count}")
    print(f"pages containing image refs: {len(pages_with_imgs)}")
    print(f"total image-ish refs: {total_refs}")
    print(f"\nMISSING under ROOT build (out/): {sum(missing_root.values())} refs, {len(missing_root)} distinct")
    for k, v in missing_root.most_common(40):
        print(f"  {v:5d}  {k}   (e.g. {examples[k]})")
    print(f"\nBROKEN on gh-pages (unprefixed absolute URLs -> 404 at github.io root): {sum(missing_gh.values())} refs, {len(missing_gh)} distinct")
    for k, v in missing_gh.most_common(20):
        print(f"  {v:5d}  {k}")
    # what's actually in public/
    pub = "/home/z/my-project/site/public"
    print("\npublic/ contents:")
    for dp, _, fs in os.walk(pub):
        for f in fs:
            p = os.path.join(dp, f)
            print("  ", os.path.relpath(p, pub), os.path.getsize(p))

if __name__ == "__main__":
    main()
