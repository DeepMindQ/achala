# -*- coding: utf-8 -*-
"""Apply the platform-suite restore + Infosys-voice copy overhaul.
Run: python3 scripts/content_overhaul.py  (from achala repo root)
- Ports 24 suite platform pages from the DataQ reference source (Dataq -> Achala)
  with rewritten heroes/intros in plain voice.
- Rewrites the 8 production-platform pages (overview / architecture / use-cases).
- Rebuilds the /platforms/ hub (blocks + 16 cards).
- Updates index.json rows and nav.json Platforms mega menu.
- Rewrites brand.json positioning + 10 hub pages.
- Global phrase cleanup over all page blocks (em-dash policy + AI-tell phrases).
"""
import json, re, sys, os

ROOT = "/home/z/my-project/achala/site"
PAGES = os.path.join(ROOT, "src/content/pages")
IDX = os.path.join(ROOT, "src/content/index.json")
NAV = os.path.join(ROOT, "src/content/nav.json")
BRANDF = os.path.join(ROOT, "src/content/brand.json")
DATAQ_PAGES = "/home/z/my-project/site/src/content/pages"

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from copy_platforms import SUITE, PHRASE_MAP as P_PHRASES
from copy_real import REAL, REAL_ORDER, REAL_SLUG_TITLE
from copy_hubs import BRAND, HUBS, PHRASE_MAP as H_PHRASES

PHRASE_MAP = {**P_PHRASES, **H_PHRASES}
stats = {"files": 0, "repl": 0}

def clean(s, dashes=True):
    for k, v in PHRASE_MAP.items():
        if k in s:
            s = s.replace(k, v); stats["repl"] += 1
    if dashes and not (s[:1].isupper() and " — " in s and s.count(" — ") == 1 and len(s) < 90):
        pass  # titles keep their dash
    return s

def clean_body(s):
    s = clean(s)
    # em-dash policy for body prose: " — " -> ", "
    s = s.replace(" — ", ", ")
    s = re.sub(r"  +", " ", s)
    return s

def clean_block(b):
    t = b.get("t")
    if t in ("p", "hero", "cta", "h2", "h3"):
        if "x" in b:
            if t in ("h2", "h3"):
                b["x"] = clean(b["x"])  # keep dash in headers (short)
            else:
                b["x"] = clean_body(b["x"])
            if "sub" in b:
                b["sub"] = clean_body(b["sub"])
    elif t == "bullets":
        b["items"] = [[i[0], clean_body(i[1])] if len(i) > 1 else clean_body(i[0]) for i in b["items"]]
    elif t == "note":
        b["x"] = clean_body(b.get("x", ""))
    elif t == "table":
        b["caption"] = clean(b.get("caption", ""))
        b["headers"] = [clean(h) for h in b.get("headers", [])]
        b["rows"] = [[clean_body(str(c)) for c in row] for row in b.get("rows", [])]
    elif t == "arch":
        b["title"] = clean(b.get("title", ""))
    return b

def wc(blocks):
    n = 0
    for b in blocks:
        for v in json.dumps(b).replace('"', ' ').replace(',', ' ').split():
            n += 1
    return n

def save(path, d):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=1, ensure_ascii=False)
    stats["files"] += 1

def related_for(name):
    return [
        {"title": f"{name} — Overview", "url": None, "desc": ""},
    ]

# ── 1. brand.json ────────────────────────────────────────────────────────────
brand = json.load(open(BRANDF))
brand.update(BRAND)
save(BRANDF, brand)

# ── 2. suite platform pages (port + rewrite) ────────────────────────────────
def dq(file):
    return json.load(open(os.path.join(DATAQ_PAGES, file + ".json")))

def rename_ds(s):
    if isinstance(s, dict):
        return {k: rename_ds(v) for k, v in s.items()}
    if isinstance(s, list):
        return [rename_ds(v) for v in s]
    if isinstance(s, str):
        s = s.replace("Dataq Software", "Achala IT Solutions")
        s = s.replace("Dataq", "Achala")
        return s
    return s

def keep_arch(b):
    b = rename_ds(json.loads(json.dumps(b)))
    b["title"] = clean(b["title"])
    for n in b.get("nodes", []):
        n["label"] = rename_ds(n["label"])
    return b

suite_rows = []
for p in SUITE:
    slug, name, sub = p["slug"], p["name"], p["subtitle"]
    title_ov = f"{name} — {sub}"

    # overview
    ov = dq(p["file"])
    blocks = [
        {"t": "hero", "x": p["hero"]},
        {"t": "h2", "x": "What it is"},
        {"t": "p", "x": p["what_p"]},
        {"t": "h2", "x": "The modules"},
        {"t": "p", "x": p["modules_p"]},
        {"t": "bullets", "items": p["bullets"]},
    ]
    arch = next((b for b in ov["blocks"] if b["t"] == "arch"), None)
    if arch:
        blocks.append(keep_arch(arch))
    blocks += [
        {"t": "h2", "x": p["audit_h2"]},
        {"t": "p", "x": p["audit_p"]},
        {"t": "bullets", "items": p["audit_bullets"]},
        {"t": "h2", "x": p["sectors_h2"]},
        {"t": "p", "x": p["sectors_p"]},
        {"t": "h2", "x": p["tech_h2"]},
        {"t": "p", "x": p["tech_p"]},
        {"t": "cta", "x": p["cta"]},
    ]
    ov["id"] = f"PLT-{slug}-ov"
    ov["title"] = title_ov
    ov["seo_title"] = f"{title_ov} | Achala IT Solutions"
    ov["meta_description"] = p["meta"]
    ov["breadcrumb"] = f"Platforms > {name} > Overview"
    ov["blocks"] = blocks
    ov["words"] = wc(blocks)
    ov["l1"], ov["l2"], ov["l3"] = "Platforms", name, "Overview"
    ov["crumbs"] = [
        {"name": "Platforms", "url": "/platforms/"},
        {"name": name, "url": None},
        {"name": "Overview", "url": f"/platforms/{slug}/"},
    ]
    ov["related"] = [
        {"title": f"{title_ov}", "url": f"/platforms/{slug}/", "desc": sub},
        {"title": f"{name} — Architecture & Trust", "url": f"/platforms/{slug}/architecture/", "desc": "Architecture, controls and evidence trails."},
        {"title": f"{name} — Industry Use Cases", "url": f"/platforms/{slug}/use-cases/", "desc": "Where the platform runs, sector by sector."},
    ]
    save(os.path.join(PAGES, p["file"] + ".json"), ov)

    # architecture
    ar = dq(p["file"] + "_architecture")
    ar_blocks = [clean_block(rename_ds(json.loads(json.dumps(b)))) for b in ar["blocks"]]
    ar_blocks[0] = {"t": "hero", "x": p["arch_hero"]}
    for b in ar_blocks:
        if b["t"] == "cta":
            b["x"] = p["cta"]
    ar["id"] = f"PLT-{slug}-ar"
    ar["title"] = f"{name} — Architecture & Trust"
    ar["seo_title"] = f"{name} — Architecture & Trust | Achala IT Solutions"
    ar["meta_description"] = p["arch_meta"]
    ar["breadcrumb"] = f"Platforms > {name} > Architecture & Trust"
    ar["blocks"] = ar_blocks
    ar["words"] = wc(ar_blocks)
    ar["l1"], ar["l2"], ar["l3"] = "Platforms", name, "Architecture & Trust"
    ar["crumbs"] = [
        {"name": "Platforms", "url": "/platforms/"},
        {"name": name, "url": None},
        {"name": "Architecture & Trust", "url": f"/platforms/{slug}/architecture/"},
    ]
    ar["related"] = ov["related"]
    save(os.path.join(PAGES, p["file"] + "_architecture.json"), ar)

    # use-cases
    uc = dq(p["file"] + "_use-cases")
    uc_blocks = [clean_block(rename_ds(json.loads(json.dumps(b)))) for b in uc["blocks"]]
    uc_blocks[0] = {"t": "hero", "x": p["uc_hero"]}
    for b in uc_blocks:
        if b["t"] == "cta":
            b["x"] = p["cta"]
    uc["id"] = f"PLT-{slug}-uc"
    uc["title"] = f"{name} — Industry Use Cases"
    uc["seo_title"] = f"{name} — Industry Use Cases | Achala IT Solutions"
    uc["meta_description"] = p["uc_meta"]
    uc["breadcrumb"] = f"Platforms > {name} > Industry Use Cases"
    uc["blocks"] = uc_blocks
    uc["words"] = wc(uc_blocks)
    uc["l1"], uc["l2"], uc["l3"] = "Platforms", name, "Industry Use Cases"
    uc["crumbs"] = [
        {"name": "Platforms", "url": "/platforms/"},
        {"name": name, "url": None},
        {"name": "Industry Use Cases", "url": f"/platforms/{slug}/use-cases/"},
    ]
    uc["related"] = ov["related"]
    save(os.path.join(PAGES, p["file"] + "_use-cases.json"), uc)

    for tmpl, url3, ttl, meta, words in [
        ("platform_overview", "", title_ov, p["meta"], ov["words"]),
        ("platform_architecture", "architecture/", f"{name} — Architecture & Trust", p["arch_meta"], ar["words"]),
        ("platform_usecases", "use-cases/", f"{name} — Industry Use Cases", p["uc_meta"], uc["words"]),
    ]:
        suite_rows.append({
            "url": f"/platforms/{slug}/{url3}", "file": p["file"] + ("" if not url3 else "_" + url3.rstrip("/")),
            "title": ttl, "template": tmpl, "section": "Platforms",
            "l1": "Platforms", "l2": name, "l3": ttl.split(" — ")[-1], "l4": "",
            "seoTitle": f"{ttl} | Achala IT Solutions", "metaDescription": meta, "words": words,
        })

# ── 3. real product pages (full rewrite) ────────────────────────────────────
real_rows = []
for slug in REAL_ORDER:
    d = REAL[slug]
    name = d["name"]
    title_ov = REAL_SLUG_TITLE[slug]
    blocks = [
        {"t": "hero", "x": d["hero"]},
        {"t": "h2", "x": d["what_h2"]},
        {"t": "p", "x": d["what_p"]},
        {"t": "h2", "x": d["cap_h2"]},
        {"t": "p", "x": "The platform's working capabilities:"},
        {"t": "bullets", "items": d["cap_bullets"]},
        {"t": "h2", "x": d["arch_h2"]},
        {"t": "p", "x": d["arch_p"]},
        {"t": "bullets", "items": d["arch_bullets"]},
        {"t": "h2", "x": d["sectors_h2"]},
        {"t": "p", "x": d["sectors_p"]},
        {"t": "cta", "x": d["cta"]},
    ]
    ov = {
        "id": f"PLT-{slug}-ov", "title": title_ov, "url": f"/platforms/{slug}/",
        "template": "platform_overview", "breadcrumb": f"Platforms > {name} > Overview",
        "seo_title": f"{title_ov} | Achala IT Solutions", "meta_description": d["meta"],
        "blocks": blocks, "words": wc(blocks), "section": "Platforms",
        "l1": "Platforms", "l2": name, "l3": "Overview", "l4": "",
        "crumbs": [{"name": "Platforms", "url": "/platforms/"}, {"name": name, "url": None}, {"name": "Overview", "url": f"/platforms/{slug}/"}],
        "related": [], "cards": [],
    }
    ov["related"] = [
        {"title": f"{title_ov}", "url": f"/platforms/{slug}/", "desc": d["card_desc"][:80]},
        {"title": f"{name} — Architecture & Security", "url": f"/platforms/{slug}/architecture/", "desc": "How it is built and controlled."},
        {"title": f"{name} — Industry Use Cases", "url": f"/platforms/{slug}/use-cases/", "desc": "Who runs it and what it delivers."},
    ]
    save(os.path.join(PAGES, d["file"] + ".json"), ov)

    ar_blocks = [
        {"t": "hero", "x": d["arch_hero"]},
        {"t": "h2", "x": d["arch_h2"]},
        {"t": "p", "x": d["arch_p"]},
        {"t": "bullets", "items": d["arch_bullets"]},
        {"t": "h2", "x": "Security and compliance"},
        {"t": "p", "x": "The platform ships with the controls below as standard, and every deployment documents them in the evidence pack your auditors receive:"},
        {"t": "bullets", "items": d["arch_bullets"]},
        {"t": "cta", "x": d["cta"]},
    ]
    ar = {
        "id": f"PLT-{slug}-ar", "title": f"{name} — Architecture & Security",
        "url": f"/platforms/{slug}/architecture/", "template": "platform_architecture",
        "breadcrumb": f"Platforms > {name} > Architecture & Security",
        "seo_title": f"{name} — Architecture & Security | Achala IT Solutions",
        "meta_description": d["arch_meta"], "blocks": ar_blocks, "words": wc(ar_blocks),
        "section": "Platforms", "l1": "Platforms", "l2": name, "l3": "Architecture & Security", "l4": "",
        "crumbs": [{"name": "Platforms", "url": "/platforms/"}, {"name": name, "url": None}, {"name": "Architecture & Security", "url": f"/platforms/{slug}/architecture/"}],
        "related": ov["related"], "cards": [],
    }
    save(os.path.join(PAGES, d["file"] + "_architecture.json"), ar)

    uc_blocks = [
        {"t": "hero", "x": d["uc_hero"]},
        {"t": "h2", "x": "Who runs it and what it delivers"},
        {"t": "p", "x": d["sectors_p"]},
        {"t": "table", "caption": f"{name} — where it runs and what it does there",
         "headers": ["Operator", "The workflow on the platform", "What the deployment delivers"],
         "rows": d["table"]},
        {"t": "cta", "x": d["cta"]},
    ]
    uc = {
        "id": f"PLT-{slug}-uc", "title": f"{name} — Industry Use Cases",
        "url": f"/platforms/{slug}/use-cases/", "template": "platform_usecases",
        "breadcrumb": f"Platforms > {name} > Industry Use Cases",
        "seo_title": f"{name} — Industry Use Cases | Achala IT Solutions",
        "meta_description": d["uc_meta"], "blocks": uc_blocks, "words": wc(uc_blocks),
        "section": "Platforms", "l1": "Platforms", "l2": name, "l3": "Industry Use Cases", "l4": "",
        "crumbs": [{"name": "Platforms", "url": "/platforms/"}, {"name": name, "url": None}, {"name": "Industry Use Cases", "url": f"/platforms/{slug}/use-cases/"}],
        "related": ov["related"], "cards": [],
    }
    save(os.path.join(PAGES, d["file"] + "_use-cases.json"), uc)

    for tmpl, url3, ttl, meta in [
        ("platform_overview", "", title_ov, d["meta"]),
        ("platform_architecture", "architecture/", f"{name} — Architecture & Security", d["arch_meta"]),
        ("platform_usecases", "use-cases/", f"{name} — Industry Use Cases", d["uc_meta"]),
    ]:
        real_rows.append({
            "url": f"/platforms/{slug}/{url3}", "file": d["file"] + ("" if not url3 else "_" + url3.rstrip("/")),
            "title": ttl, "template": tmpl, "section": "Platforms",
            "l1": "Platforms", "l2": name, "l3": ttl.split(" — ")[-1], "l4": "",
            "seoTitle": f"{ttl} | Achala IT Solutions", "metaDescription": meta, "words": wc(blocks if not url3 else (ar_blocks if tmpl == "platform_architecture" else uc_blocks)),
        })

# ── 4. platforms hub ────────────────────────────────────────────────────────
hub = json.load(open(os.path.join(PAGES, "platforms.json")))
hub["blocks"] = [
    {"t": "hero", "x": "Achala builds platforms for the decisions enterprises make at scale. Eight come from our own R&D programme and license as products; another eight run in production today for clients in healthcare, mobility, public sector and finance."},
    {"t": "h2", "x": "The platform suite from our R&D programme"},
    {"t": "p", "x": "Eight platforms, each built on a patented method family from our R&D programme and licensed as a product: decision intelligence, data engineering, agent orchestration, zero-trust security, digital twin operations, advanced compute, distributed trust and AI governance. They deploy under NDA, run on your infrastructure, and produce the evidence your auditors ask for."},
    {"t": "h2", "x": "Platforms in production"},
    {"t": "p", "x": "Eight production platforms run client operations every day: emergency response across 9 states, fleet management, KYC verification in about 5 minutes, telemedicine, queue management, patient portals, BI and analytics, and assistive smart glasses. Each one carries a published client result."},
    {"t": "h2", "x": "How a platform engagement starts"},
    {"t": "p", "x": "Most engagements begin with a 45-minute briefing on one use case. We configure the platform against your data, agree the metric it will be measured on, and scope the pilot in writing before delivery starts."},
    {"t": "cta", "x": "Book a briefing with the platform team. Bring one use case — we will show it running on the platform and leave you with a written feasibility read."},
]
cards = []
for p in SUITE:
    cards.append({"title": f"{p['name']} — {p['subtitle']}", "url": f"/platforms/{p['slug']}/", "tag": "Platform suite", "desc": p["card_desc"]})
for slug in REAL_ORDER:
    d = REAL[slug]
    cards.append({"title": REAL_SLUG_TITLE[slug], "url": f"/platforms/{slug}/", "tag": "In production", "desc": d["card_desc"]})
hub["cards"] = cards
hub["meta_description"] = "The Achala platform portfolio: eight licensed products from our R&D programme and eight production platforms running client operations today."
save(os.path.join(PAGES, "platforms.json"), hub)

# ── 5. index.json rows ──────────────────────────────────────────────────────
idx = json.load(open(IDX))
kept = [r for r in idx if not (r["url"].startswith("/platforms/") and r["url"] != "/platforms/")]
for r in kept:
    if r["url"] == "/platforms/":
        r["title"] = "Platforms Overview"
        r["metaDescription"] = hub["meta_description"]
        r["seoTitle"] = "Platforms Overview | Achala IT Solutions"
idx = kept + suite_rows + real_rows
json.dump(idx, open(IDX, "w"), indent=1, ensure_ascii=False)

# ── 6. nav.json Platforms mega ──────────────────────────────────────────────
nav = json.load(open(NAV))
mega = []
for p in SUITE:
    mega.append({
        "label": f"{p['name']} — {p['subtitle']}",
        "url": f"/platforms/{p['slug']}/",
        "children": [
            {"label": "Overview", "url": f"/platforms/{p['slug']}/"},
            {"label": "Architecture & Trust", "url": f"/platforms/{p['slug']}/architecture/"},
            {"label": "Use cases", "url": f"/platforms/{p['slug']}/use-cases/"},
        ],
    })
mega.append({
    "label": "Platforms in production",
    "url": "/platforms/",
    "children": [{"label": REAL_SLUG_TITLE[s], "url": f"/platforms/{s}/"} for s in REAL_ORDER],
})
for it in nav["nav"]["primary"]:
    if it.get("label") == "Platforms":
        it["mega"] = mega
json.dump(nav, open(NAV, "w"), indent=1, ensure_ascii=False)

# ── 7. hub page rewrites ────────────────────────────────────────────────────
for fname, spec in HUBS.items():
    path = os.path.join(PAGES, fname + ".json")
    if not os.path.exists(path):
        continue
    d = json.load(open(path))
    hero_done = False
    for b in d["blocks"]:
        if b["t"] == "hero" and not hero_done:
            b["x"] = spec["hero"]; hero_done = True
        elif "x" in b:
            for k, v in spec["repl"].items():
                if k in b.get("x", ""):
                    b["x"] = b["x"].replace(k, v); stats["repl"] += 1
    d["meta_description"] = spec["meta"]
    save(path, d)

# ── 8. global phrase + dash cleanup over ALL page blocks ───────────────────
for fn in os.listdir(PAGES):
    if not fn.endswith(".json"):
        continue
    path = os.path.join(PAGES, fn)
    d = json.load(open(path))
    changed = False
    for b in d.get("blocks", []):
        nb = clean_block(json.loads(json.dumps(b)))
        if json.dumps(nb) != json.dumps(b):
            b.clear(); b.update(nb); changed = True
    for c in d.get("cards", []) or []:
        if c.get("desc"):
            nd = clean_body(c["desc"])
            if nd != c["desc"]:
                c["desc"] = nd; changed = True
    if changed:
        save(path, d)

print(f"OK — files touched: {stats['files']}, phrase replacements: {stats['repl']}")
print(f"index rows now: {len(idx)}")
