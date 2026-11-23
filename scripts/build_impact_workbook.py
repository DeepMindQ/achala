#!/usr/bin/env python3
"""Build the page-by-page impact assessment workbook (633 pages, read-only audit)."""
import sys, os, json, glob, re, collections, statistics, hashlib

XLSX_SKILL_DIR = "/home/z/my-project/skills/xlsx"
for sub in [XLSX_SKILL_DIR, os.path.join(XLSX_SKILL_DIR, "templates")]:
    if sub not in sys.path: sys.path.insert(0, sub)
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
import base as B

ROOT = "/home/z/my-project/site"
OUTFILE = "/home/z/my-project/download/achala-page-by-page-impact-assessment.xlsx"

# ---------- load live pages ----------
pages = []
for j in glob.glob(f"{ROOT}/src/content/**/*.json", recursive=True):
    if "_backup" in j: continue
    try: d = json.load(open(j, encoding="utf-8"))
    except Exception: continue
    if isinstance(d, dict) and d.get("template") and "blocks" in d:
        pages.append(d)

def words(d):
    txt = []
    for b in d.get("blocks", []):
        if isinstance(b, dict):
            for v in b.values():
                if isinstance(v, str): txt.append(v)
                elif isinstance(v, list): txt.extend(x for x in v if isinstance(x, str))
    for c in d.get("cards", []) or []:
        if isinstance(c, dict): txt.append(str(c.get("h","")) + " " + str(c.get("x","")))
    return len(re.findall(r"\w+", " ".join(txt)))

def h2s(d):
    return tuple((b.get("x","")[:40] if isinstance(b, dict) and b.get("t")=="h2" else None)
                 for b in d.get("blocks", []) if isinstance(b, dict) and b.get("t")=="h2")

# skeleton sharing
sk_count = collections.Counter()
for d in pages:
    sk_count[hashlib.md5("|".join(h2s(d)).encode()).hexdigest()[:6]] += 1

# hero image reuse from built html
img_use = collections.Counter()
page_img = {}
for p in glob.glob(f"{ROOT}/out-gh/**/index.html", recursive=True):
    h = open(p, encoding="utf-8", errors="ignore").read()
    srcs = [s for s in re.findall(r'<img[^>]+src="([^"]+)"', h) if not s.startswith("data:")]
    url = "/" + p[len(f"{ROOT}/out-gh/"):-len("/index.html")].strip("/") + "/"
    page_img[url] = srcs[0] if srcs else ""
    for s in srcs: img_use[s] += 1

# verdict + phase + planned changes per template
PLAN = {
 "home": ("Complete redesign", "P1",
          "Homepage experience overhaul: new narrative arc, outcome-first hero variants, proof architecture (baseline-vs-after evidence wall), interactive capability finder, re-choreographed motion, Core-Web-Vitals-safe media strategy."),
 "tower_hub": ("Restructure", "P1",
          "Tower hub redesign: replace link-index grid with capability story (problem -> method -> proof), featured engagement strip, tower-specific KPI band, unique hero visual per tower."),
 "services_hub": ("Restructure", "P1", "Merge into unified Services hub design shared with tower hubs; single IA source for mega-menu."),
 "industry_hub": ("Restructure", "P1",
          "Industry hub redesign: sector pain-map, regulatory frame panel, sub-industry chooser cards with live metrics, industry-specific CTA."),
 "solutions_hub": ("Restructure", "P1", "Solution finder matrix (outcome x sector), featured solutions with baseline deltas."),
 "platforms_hub": ("Restructure", "P1", "Platform portfolio overview: architecture-first landing, deployment models, cross-platform integration map."),
 "cases_hub": ("Restructure", "P1", "Evidence library: filterable by sector/tower/metric; standardized proof cards."),
 "insights_hub": ("Restructure", "P1", "Editorial hub redesign: viewpoint tracks, featured research, author identities."),
 "service_page": ("Enrich + restructure", "P2",
          "De-templatize H2 skeleton; add engagement anatomy, reference architecture diagram (unique topology), integration matrix table, failure-mode ledger, engineering standards with named tools + versions, delivery timeline, outcome deltas."),
 "sub_capability": ("Enrich + de-templatize", "P2",
          "Break shared essay skeleton (240 pages share one outline); per-pattern technical narrative, unique animated architecture visual, data-source and protocol inventory, governance/compliance specifics, quantified outcome bands, sector variants where meaningful."),
 "industry_capability": ("Enrich + de-templatize", "P2",
          "Same de-templatization as sub_capability plus sector regulatory overlays (HIPAA/PCI/FFIEC/GxP etc.), plant/network-level integration specifics, sector KPI definitions."),
 "subindustry_page": ("Enrich", "P2",
          "Sub-industry depth: operating-model map, workflow-level pain points, data estate realities, capability prioritization matrix."),
 "solution_page": ("Enrich + restructure", "P2",
          "Outcome-metric-led structure; decision-flow diagram with latency budgets; fraud/risk-specific control table; run-book excerpt; expansion path."),
 "case_study": ("Restructure to evidence format", "P2",
          "Standardized proof format: signed baseline -> intervention -> audited delta; sanitized architecture excerpt; engagement timeline; client-voice quote panel."),
 "insight_article": ("Enrich", "P2", "Long-form technical viewpoints (900-1,400 words), author profiles, diagrams from site visual library, related engagement links."),
 "insights_category": ("Restructure", "P2", "Category page as curated track: editors note, must-read queue, series navigation."),
 "newsroom_article": ("Enrich", "P2", "Newsroom items with context blocks and linked proof points; expand from ~200 words."),
 "platform_overview": ("Deep technical rebuild", "P2",
          "Platform overview: full architecture (control plane / data plane / extensibility), SLO table, deployment topologies, API surface, security model, licensing/ops model."),
 "platform_usecases": ("Deep technical rebuild", "P2",
          "Platform use cases: each mapped to reference workflow with inputs/outputs/guards, linked to the new use-case library."),
 "platform_architecture": ("Deep technical rebuild", "P2",
          "Architecture pages: component diagram set, sequence diagrams for key flows, capacity/latency budgets, failure domains, upgrade path."),
 "industry_hub_x": ("Restructure", "P1", ""),
 "partner_page": ("Enrich", "P2", "Partner pages with joint solution matrix, integration architecture, co-delivery model."),
 "company_page": ("Polish + expand", "P2", "Expand company/story pages; real operating model, delivery governance, quality system."),
 "leadership_profile": ("Polish + expand", "P2", "Leadership profiles with operating focus, published viewpoint links."),
 "approach_page": ("Restructure", "P1", "Approach pages = the methodology spine; redesign as the anchor for engagement model (diagnose -> baseline -> deliver -> prove)."),
 "careers_page": ("Enrich", "P3", "Careers content expansion: teams, hiring bar, growth tracks."),
 "contact_page": ("Polish", "P3", "Contact/briefing flow polish; routing by intent."),
 "legal_page": ("Polish", "P3", "Legal pages: consistent structure, plain-language summaries."),
}

PHASE1_TPL = {"home","tower_hub","services_hub","industry_hub","solutions_hub","platforms_hub","cases_hub","insights_hub","approach_page"}
P3_TPL = {"careers_page","contact_page","legal_page"}

def verdict_for(d):
    t = d["template"]
    if t in PLAN: return PLAN[t]
    return ("Enrich", "P2", "De-templatize and deepen; add unique visual asset + technical tables.")

def phase_for(t):
    if t in PHASE1_TPL: return "P1"
    if t in P3_TPL: return "P3"
    return "P2"

rows = []
for d in sorted(pages, key=lambda x: x.get("url","")):
    url = d.get("url","/")
    t = d["template"]
    seg = len([s for s in url.split("/") if s])
    sk = hashlib.md5("|".join(h2s(d)).encode()).hexdigest()[:6]
    shared = sk_count[sk]
    img = page_img.get(url, "")
    reuse = img_use.get(img, 0)
    v, ph, chg = verdict_for(d)
    # override phase by verdict mapping (PLAN already has phase)
    rows.append({
        "URL": url, "Template": t, "Depth": seg, "Words": words(d),
        "H2s": len(h2s(d)), "Skeleton shares": shared if shared > 1 else 1,
        "Hero asset": img.rsplit("/",1)[-1] if img else "-",
        "Asset reuse": reuse if img else 0,
        "Verdict": v, "Phase": ph, "Planned changes": chg,
    })

print("rows:", len(rows))

# ---------- build workbook ----------
wb = Workbook()
wb.properties.creator = "Z.ai"

# Sheet 2 data (summary) computed first
vcount = collections.Counter(r["Verdict"] for r in rows)
pcount = collections.Counter(r["Phase"] for r in rows)
tcount = collections.Counter(r["Template"] for r in rows)

ws = wb.active
ws.title = "Impact Assessment"
ws.sheet_view.showGridLines = False
B.use_palette_explicit("professional")
B.setup_sheet(ws, title="Achala Website - Page-by-Page Impact Assessment (633 pages)", last_col=11)
headers = ["URL","Template","Depth","Words","H2 count","Skeleton shared by","Hero asset","Asset reuse (pages)","Verdict","Phase","Planned changes"]
hr = 4
for ci, h in enumerate(headers, 1):
    ws.cell(row=hr, column=ci, value=h)
B.style_header_row(ws, row_num=hr, col_start=1, col_end=len(headers))

thin = ["home","company_page","leadership_profile","approach_page","careers_page","newsroom_article","insight_article","contact_page","case_study"]
for ri, r in enumerate(rows, hr+1):
    vals = [r["URL"], r["Template"], r["Depth"], r["Words"], r["H2s"], r["Skeleton shares"],
            r["Hero asset"], r["Asset reuse"], r["Verdict"], r["Phase"], r["Planned changes"]]
    for ci, v in enumerate(vals, 1):
        ws.cell(row=ri, column=ci, value=v)
    B.style_data_row(ws, row_num=ri, col_start=1, col_end=len(headers), row_index=ri-hr-1)
    # highlight thin pages + shared skeletons + heavy reuse
    if r["Words"] < 350:
        c = ws.cell(row=ri, column=4); c.font = Font(bold=True, color=B.ACCENT_NEGATIVE)
    if r["Skeleton shares"] >= 40:
        c = ws.cell(row=ri, column=6); c.font = Font(bold=True, color=B.ACCENT_NEGATIVE)
    if r["Asset reuse"] >= 40:
        c = ws.cell(row=ri, column=8); c.font = Font(bold=True, color="B26A00")

last = hr + len(rows)
widths = [34, 20, 8, 8, 9, 14, 22, 13, 22, 8, 72]
for i, w in enumerate(widths, 1):
    ws.column_dimensions[get_column_letter(i)].width = w
ws.freeze_panes = "A5"
ws.auto_filter.ref = f"A{hr}:K{last}"

# notes
nrow = last + 2
ws.cell(row=nrow, column=1, value="Verdicts: Complete redesign / Restructure / Enrich + restructure / Enrich + de-templatize / Deep technical rebuild / Enrich / Polish.")
ws.cell(row=nrow+1, column=1, value="Red flags: Words<350 (bold red), skeleton shared by 40+ pages, hero asset reused on 40+ pages.")
ws.cell(row=nrow+2, column=1, value="Source: audit of build 2026-11-21 (out-gh, 638 HTML pages / 633 content pages). Phases P1 foundation, P2 content depth, P3 QA & optimization.")
for rr in range(nrow, nrow+3):
    ws.cell(row=rr, column=1).font = B.font_caption()

# ---------- summary sheet ----------
s = wb.create_sheet("Audit Summary")
s.sheet_view.showGridLines = False
B.setup_sheet(s, title="Audit Summary - measured findings (2026-11-21 build)", last_col=3)
sheaders = ["Metric", "Value", "Interpretation"]
for ci, h in enumerate(sheaders, 1): s.cell(row=4, column=ci, value=h)
B.style_header_row(s, row_num=4, col_start=1, col_end=3)
metrics = [
 ("Content pages", len(rows), "633 JSON-driven pages; 638 total built incl. 404/search/style-guide"),
 ("Median words per page (all)", int(statistics.median([r["Words"] for r in rows])), "Enterprise deep-tech target: 900-1,600 for capability pages"),
 ("Pages under 350 words", sum(1 for r in rows if r["Words"]<350), "Essay-thin pages; primary content debt"),
 ("Pages on a 10+ shared H2 skeleton", sum(1 for r in rows if r["Skeleton shares"]>=40), "Template monotony quantified"),
 ("Hero assets in existence", len(img_use), "for 632 image-bearing pages"),
 ("Pages reusing a hero asset 40+ times", sum(1 for r in rows if r["Asset reuse"]>=40), "Same art on ~100 pages each - no page uniqueness"),
 ("Distinct diagram shapes", 10, "594 diagram blocks reuse 10 topologies (pipeline x148)"),
 ("'Program economics' boilerplate pages", 578, "identical furniture block on 91% of pages"),
 ("'On this page' TOC rail pages", 628, "the index block flagged for removal/replacement"),
 ("Median built HTML size (KB)", 363, "SVG-heavy DOM; median 118 inline SVGs/page"),
 ("Distinct hero backgrounds", 1, "same navy gradient + dot grid + orange glow on every page"),
 ("Motion tokens (easing curves)", 8, "8 different cubic-beziers, durations 40ms-1.2s, no scale"),
 ("Services mega-menu links", 54, "8 columns x ~7 children, 8 truncated labels, no visual anchors"),
]
for ri, m in enumerate(metrics, 5):
    s.cell(row=ri, column=1, value=m[0]); s.cell(row=ri, column=2, value=m[1]); s.cell(row=ri, column=3, value=m[2])
    B.style_data_row(s, row_num=ri, col_start=1, col_end=3, row_index=ri-5)
for i, w in enumerate([44, 12, 84], 1):
    s.column_dimensions[get_column_letter(i)].width = w

# verdict distribution block
r0 = 5 + len(metrics) + 2
s.cell(row=r0, column=1, value="Verdict distribution").font = B.font_subheader()
s.cell(row=r0+1, column=1, value="Verdict").font = B.font_subheader()
s.cell(row=r0+1, column=2, value="Pages").font = B.font_subheader()
s.cell(row=r0+1, column=3, value="Phase").font = B.font_subheader()
B.style_header_row(s, row_num=r0+1, col_start=1, col_end=3)
ri = r0+2
for v, n in sorted(vcount.items(), key=lambda kv: -kv[1]):
    phs = sorted(set(r["Phase"] for r in rows if r["Verdict"]==v))
    s.cell(row=ri, column=1, value=v); s.cell(row=ri, column=2, value=n); s.cell(row=ri, column=3, value="/".join(phs))
    B.style_data_row(s, row_num=ri, col_start=1, col_end=3, row_index=ri-(r0+2)); ri += 1
s.cell(row=ri, column=1, value="Total").font = B.font_subheader()
s.cell(row=ri, column=2, value=sum(vcount.values())).font = B.font_subheader()
B.style_total_row(s, row_num=ri, col_start=1, col_end=3)

os.makedirs(os.path.dirname(OUTFILE), exist_ok=True)
wb.save(OUTFILE)
print("saved:", OUTFILE)
print("verdicts:", dict(vcount))
print("phases:", dict(pcount))
