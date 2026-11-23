#!/usr/bin/env python3
"""Phase-0 quantitative audit of the Achala site (read-only)."""
import glob, json, os, re, collections, statistics, html as htmlmod

ROOT = "/home/z/my-project/site"
OUT = {}

# ---------- 1. page inventory from built HTML ----------
pages = sorted(glob.glob(f"{ROOT}/out-gh/**/index.html", recursive=True))
paths = ["https://gh/" + p[len(f"{ROOT}/out-gh/"):-len("/index.html")].strip("/") + "/" for p in pages]
depth = collections.Counter(p.count("/") - 2 for p in paths)  # /a/ =1, /a/b/ =2 ...
print("PAGES:", len(pages))
print("DEPTH HISTOGRAM:", dict(sorted(depth.items())))

# ---------- 2. template distribution from content JSONs ----------
tpl = collections.Counter()
jroot = f"{ROOT}/src/content"
jsons = [j for j in glob.glob(f"{jroot}/**/*.json", recursive=True)]
print("JSON FILES:", len(jsons))
page_jsons = []
for j in jsons:
    try:
        d = json.load(open(j, encoding="utf-8"))
    except Exception:
        continue
    if isinstance(d, dict) and d.get("template") and "blocks" in d:
        page_jsons.append((j, d))
        tpl[d["template"]] += 1
print("PAGE JSONS:", len(page_jsons))
print("TEMPLATES:", dict(tpl.most_common()))

# ---------- 3. word counts ----------
def block_words(d):
    txt = []
    for b in d.get("blocks", []):
        for v in (b if isinstance(b, dict) else {}).values():
            if isinstance(v, str):
                txt.append(v)
            elif isinstance(v, list):
                txt.extend(x for x in v if isinstance(x, str))
    # cards too
    for c in d.get("cards", []) or []:
        if isinstance(c, dict):
            txt.append(str(c.get("h", "")))
            txt.append(str(c.get("x", "")))
    return len(re.findall(r"\w+", " ".join(txt)))

wc = [(j, block_words(d)) for j, d in page_jsons]
counts = sorted(w for _, w in wc)
print("WORDS/PAGE  min:", counts[0], "p10:", counts[len(counts)//10], "median:", statistics.median(counts),
      "p90:", counts[9*len(counts)//10], "max:", counts[-1])
thin = [(j.replace(jroot+"/",""), w) for j, w in wc if w < 350]
print("PAGES UNDER 350 WORDS:", len(thin))
thin.sort(key=lambda x: x[1])
for t in thin[:8]: print("   THIN:", t)

# ---------- 4. h2 skeleton analysis (essay-template detection) ----------
skeleton = collections.Counter()
h2count = []
for j, d in page_jsons:
    h2s = tuple((b.get("x", "")[:48] if isinstance(b, dict) and b.get("t") == "h2" else None) for b in d.get("blocks", []) if isinstance(b, dict) and b.get("t") == "h2")
    h2s = tuple(x for x in h2s if x)
    h2count.append(len(h2s))
    if len(h2s) >= 5:
        skeleton[h2s] += 1
print("H2 PER PAGE  min:", min(h2count), "median:", statistics.median(h2count), "max:", max(h2count))
print("DISTINCT H2 SKELETONS (5+ h2):", len(skeleton), "| pages covered by top-10 skeletons:",
      sum(c for _, c in skeleton.most_common(10)), "of", sum(skeleton.values()))
for sk, c in skeleton.most_common(3):
    print(f"   x{c}: {list(sk)[:4]} ...")

# most repeated h2 strings across pages
h2freq = collections.Counter()
for j, d in page_jsons:
    for b in d.get("blocks", []):
        if isinstance(b, dict) and b.get("t") == "h2":
            h2freq[b.get("x", "").strip()] += 1
print("TOP REPEATED H2 HEADINGS:")
for h, c in h2freq.most_common(12):
    print(f"   x{c}: {h[:70]}")

# ---------- 5. card-title repetition (cross-page boilerplate) ----------
cardh = collections.Counter()
for j, d in page_jsons:
    seen = set()
    for c in d.get("cards", []) or []:
        if isinstance(c, dict):
            t = str(c.get("h", "")).strip().lower()
            if t and t not in seen:
                seen.add(t); cardh[t] += 1
    # also cards inside blocks
    for b in d.get("blocks", []):
        if isinstance(b, dict) and b.get("t") == "cards":
            items = b.get("cards") or []
            for c in items:
                if isinstance(c, dict):
                    t = str(c.get("h", "")).strip().lower()
                    if t: cardh[t] += 1
print("TOP REPEATED CARD TITLES (pages containing):")
for h, c in cardh.most_common(14):
    print(f"   x{c}: {h[:60]}")

# ---------- 6. near-duplicate sentence shingles across pages ----------
sent_re = re.compile(r"[^.!?]+[.!?]")
def sents(d):
    out = set()
    for b in d.get("blocks", []):
        if isinstance(b, dict):
            for v in b.values():
                if isinstance(v, str) and len(v) > 60:
                    for s in sent_re.findall(v):
                        s2 = re.sub(r"\s+", " ", s).strip().lower()
                        # normalize page-name interpolation
                        s2 = re.sub(r"\b(fraud & financial crime decisioning|Achala IT Solutions)\b", "X", s2)
                        if 40 < len(s2) < 400:
                            out.add(s2)
    return out
by_page = {j: sents(d) for j, d in page_jsons}
all_s = collections.Counter()
for s in by_page.values():
    for x in s: all_s[x] += 1
cross = {x: c for x, c in all_s.items() if c >= 3}
print("SENTENCES APPEARING ON 3+ PAGES (normalized):", len(cross))
for x, c in sorted(cross.items(), key=lambda kv: -kv[1])[:10]:
    print(f"   x{c}: {x[:90]}")

# ---------- 7. diagrams + images coverage in built HTML ----------
diag_pages = img_pages = 0
diag_total = 0
for p in pages:
    h = open(p, encoding="utf-8", errors="ignore").read()
    n = len(re.findall(r"dqd-|schematic|LIVE SCHEMATIC|TechDiagram", h, re.I))
    # count svg with animated dash
    d = len(re.findall(r"<svg", h))
    if d: diag_pages += 1
    diag_total += d
    if "<img" in h: img_pages += 1
print(f"HTML: pages with svg: {diag_pages}/{len(pages)} | svg total: {diag_total} | pages with <img>: {img_pages}")

# ---------- 8. boilerplate furniture headings ----------
furn = ["What a program of this type targets", "On this page"]
for f in furn:
    c = sum(1 for p in pages if f.lower() in open(p, encoding="utf-8", errors="ignore").read().lower())
    print(f"FURNITURE '{f}' on {c}/{len(pages)} pages")

# ---------- 9. nav structure ----------
navj = glob.glob(f"{jroot}/**/nav*.json", recursive=True) + glob.glob(f"{jroot}/**/*nav*.json", recursive=True)
print("NAV JSONS:", navj[:5])
for n in navj[:1]:
    d = json.load(open(n, encoding="utf-8"))
    prim = d.get("primary", [])
    print("PRIMARY ITEMS:", len(prim))
    for it in prim:
        mega = it.get("mega") or []
        kids = sum(len(c.get("children", [])) for c in mega)
        print(f"   {it.get('label')}: cols={len(mega)} children={kids}")
