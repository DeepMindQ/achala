"""p2_consulting — build the Consulting hub + 13 service pages, update
index.json, and perform the nav surgery:
  - main menu: Case Studies OUT, Consulting IN (mega with 4 groups)
  - Case Studies becomes an Insights mega group.
"""
import sys, os, json, hashlib
sys.path.insert(0, os.path.dirname(__file__))
from p2_consulting_data import CONSULTING, CONSULTING_GROUPS
from p2_build import _h

ROOT = "/home/z/my-project/site"
PAGES = os.path.join(ROOT, "src/content/pages")
INDEX = os.path.join(ROOT, "src/content/index.json")
NAV = os.path.join(ROOT, "src/content/nav.json")

BRAND = [
    ("Achala\\s*Soft(ware)?", "Achala IT Solutions"),
    ("Achala IT Solutions", "Achala IT Solutions"),
    ("(?<![A-Za-z])Achala(?![A-Za-z])", "Achala"),
]
import re
def brand_fix(s):
    for pat, rep in BRAND:
        s = re.sub(pat, rep, s)
    return s

def crumbs(names_urls):
    return [{"name": n, "url": u} for n, u in names_urls]

def build_consulting_page(svc):
    pid = f"CONS-{svc['slug']}"
    url = f"/consulting/{svc['slug']}/"
    blocks = []
    blocks.append({"t": "hero", "x": f"{svc['name']}: {svc['promise']} "
                   f"This page is the practice as it works — method, toolchain, artifacts and the architecture we deploy."})
    blocks.append({"t": "h2", "x": "What this practice does"})
    blocks.append({"t": "p", "x": svc["overview"][0]})
    blocks.append({"t": "p", "x": svc["overview"][1]})
    blocks.append({"t": "h2", "x": "The method, named"})
    blocks.append({"t": "bullets", "items": [[m[0], m[1]] for m in svc["method"]]})
    # unique architecture per service
    counts, nodes = {}, []
    for (r, ln, lbl, *ht) in svc["arch_nodes"]:
        k = counts.get(r, 0)
        counts[r] = k + 1
        nodes.append({"id": f"{r}{k}", "lane": ln, "label": lbl, "hot": bool(ht)})
    blocks.append({"t": "arch",
                   "title": f"Reference architecture — {svc['name']}",
                   "lanes": svc["arch_lanes"],
                   "nodes": nodes,
                   "edges": [{"a": a, "b": b} for a, b in svc["arch_edges"]],
                   "note": "Nodes and lanes are this practice's actual build — drawn once, per service, not shared."})
    blocks.append({"t": "h2", "x": "The toolchain we bring"})
    blocks.append({"t": "table", "caption": "Tooling by layer",
                   "headers": ["Layer", "Tools & frameworks"],
                   "rows": [[g[0], ", ".join(g[1])] for g in svc["tools"]]})
    blocks.append({"t": "h2", "x": "What changes hands"})
    blocks.append({"t": "bullets", "items": [[d, "Named artifact with a walkthrough when it lands."] for d in svc["deliverables"]]})
    blocks.append({"t": "p", "x": "Engagements open with a two-week diagnostic: the estate baselined, the outcomes scoped in writing, and the gate criteria agreed before any build begins. If the diagnostic shows the delta does not justify the work, you keep the baseline and the measurement design."})
    blocks.append({"t": "cta", "x": f"Book a {svc['name']} briefing — 45 minutes with the practice lead, your estate, and a straight answer on feasibility."})
    words = sum(len(str(b.get("x", "")).split()) for b in blocks) + 180
    page = {
        "id": pid, "title": svc["name"], "url": url, "template": "consulting_service",
        "breadcrumb": "Consulting", "seo_title": f"{svc['name']} — Consulting | Achala IT Solutions",
        "meta_description": f"{svc['name']}: {svc['promise']} Method, toolchain and delivered artifacts — engineered under outcome-gated engagement.",
        "blocks": blocks, "words": words,
        "section": "Consulting", "l1": "Consulting", "l2": svc["name"], "l3": "", "l4": "",
        "crumbs": crumbs([("Home", "/"), ("Consulting", "/consulting/"), (svc["name"], url)]),
        "related": [], "cards": [],
    }
    return page


def build_hub():
    pid = "CONSHUB"
    url = "/consulting/"
    blocks = [
        {"t": "hero", "x": "Thirteen consulting and engineering practices, one governed delivery system. "
         "Data migration, software development, testing, application modernization, experience design, IT services, "
         "analytics, transformation programs, managed capacity, end-user support, cybersecurity, Azure cloud and ERP — "
         "each with a named method, a real toolchain and artifacts that change hands."},
        {"t": "h2", "x": "How the practices are organized"},
        {"t": "p", "x": "The section is organized the way engagements are actually staffed: data and analytics practices build "
         "the decision substrate; engineering and quality practices ship the systems; cloud and operations practices run the "
         "estate; advisory practices frame the programs that hold it all together. Practices compose — a transformation program "
         "draws on all four groups without changing the delivery mechanics."},
        {"t": "h2", "x": "The common contract"},
        {"t": "p", "x": "Every practice runs on the same engagement discipline: a two-week diagnostic that prices the work against "
         "your baseline, gate criteria written with your team, evidence generated by running the system, and handover with "
         "runbooks rather than folklore. If a diagnostic shows the delta does not justify the build, you keep the baseline."},
        {"t": "cta", "x": "Book a consulting briefing — describe the problem, and we will map it to the practice, the method and the team shape in 45 minutes."},
    ]
    page = {
        "id": pid, "title": "Consulting Services", "url": url, "template": "consulting_hub",
        "breadcrumb": "Consulting", "seo_title": "Consulting Services — 13 Practices | Achala IT Solutions",
        "meta_description": "Thirteen IT consulting & engineering practices — data migration, software development, testing, analytics, cybersecurity, Azure, ERP and more — under one outcome-gated delivery system.",
        "blocks": blocks,
        "words": sum(len(str(b.get("x","")).split()) for b in blocks) + 60,
        "section": "Consulting", "l1": "Consulting", "l2": "", "l3": "", "l4": "",
        "crumbs": crumbs([("Home", "/"), ("Consulting", url)]),
        "related": [], "cards": [],
    }
    return page


def write_index(pages):
    idx = json.load(open(INDEX))
    have = {r["url"] for r in idx}
    for p in pages:
        if p["url"] in have:
            continue
        idx.append({
            "url": p["url"], "file": p["url"].strip("/").replace("/", "_"),
            "title": p["title"], "template": p["template"], "section": p["section"],
            "l1": p["l1"], "l2": p["l2"], "l3": p["l3"], "l4": p["l4"],
            "seoTitle": p["seo_title"], "metaDescription": p["meta_description"],
            "words": p["words"],
        })
    json.dump(idx, open(INDEX, "w"), indent=1, ensure_ascii=False)


def nav_surgery():
    nav = json.load(open(NAV))
    primary = nav["nav"]["primary"]
    # 1. remove Case Studies from primary
    primary = [x for x in primary if x["label"] != "Case Studies"]
    # 2. add Consulting mega (place where Case Studies sat: before Insights)
    svc_by_slug = {s["slug"]: s for s in CONSULTING}
    mega = []
    for gname, slugs in CONSULTING_GROUPS:
        mega.append({
            "label": gname,
            "url": "/consulting/",
            "children": [
                {"label": svc_by_slug[s]["name"], "url": f"/consulting/{s}/", "children": []}
                for s in slugs
            ],
        })
    cons_item = {"label": "Consulting", "url": "/consulting/", "mega": mega}
    # insert before Insights
    idx = next(i for i, x in enumerate(primary) if x["label"] == "Insights")
    primary.insert(idx, cons_item)
    nav["nav"]["primary"] = primary
    # 3. Case Studies group inside Insights mega
    ins = next(x for x in nav["nav"]["primary"] if x["label"] == "Insights")
    ins["mega"].append({
        "label": "Case Studies",
        "url": "/case-studies/",
        "children": [
            {"label": "All case studies", "url": "/case-studies/", "children": []},
            {"label": "AI, Data & Analytics engagements", "url": "/case-studies/", "children": []},
            {"label": "Banking fraud decisioning (top-10 EU bank)", "url": "/case-studies/bank-01/", "children": []},
            {"label": "Retail demand & waste (top-3 grocer)", "url": "/case-studies/ret-01/", "children": []},
            {"label": "Healthcare prior-auth turnaround", "url": "/case-studies/hc-01/", "children": []},
        ],
    })
    json.dump(nav, open(NAV, "w"), indent=1, ensure_ascii=False)


def main():
    pages = [build_hub()] + [build_consulting_page(s) for s in CONSULTING]
    for p in pages:
        fp = os.path.join(PAGES, p["url"].strip("/").replace("/", "_") + ".json")
        json.dump(brand_fix_obj(p), open(fp, "w"), indent=1, ensure_ascii=False)
        print("wrote", fp)
    write_index(pages)
    nav_surgery()
    print("index + nav updated")

def brand_fix_obj(o):
    if isinstance(o, str):
        return brand_fix(o)
    if isinstance(o, dict):
        return {k: brand_fix_obj(v) for k, v in o.items()}
    if isinstance(o, list):
        return [brand_fix_obj(v) for v in o]
    return o

if __name__ == "__main__":
    main()
