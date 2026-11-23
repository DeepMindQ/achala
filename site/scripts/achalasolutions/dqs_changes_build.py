# Build the Achala IT Solutions website overhaul change list workbook.
import sys, os
from math import ceil

XLSX_SKILL_DIR = "/home/z/my-project/skills/xlsx"
for sub in [XLSX_SKILL_DIR, os.path.join(XLSX_SKILL_DIR, "templates")]:
    if sub not in sys.path:
        sys.path.insert(0, sub)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from base import *  # noqa
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

from dqs_changes_ab import ITEMS_A, ITEMS_B
from dqs_changes_ce import ITEMS_C, ITEMS_E
from dqs_changes_dfg import ITEMS_D, ITEMS_F, ITEMS_G
from dqs_changes_hi import ITEMS_H, ITEMS_I
from dqs_changes_jklm import ITEMS_J, ITEMS_K, ITEMS_L, ITEMS_M

CAT_NAME = {
    "A": "A - Brand Identity & Logo",
    "B": "B - Design System & Tokens",
    "C": "C - Motion & Animation",
    "D": "D - Homepage Experience",
    "E": "E - Visual Assets & Imagery",
    "F": "F - Page Templates & Layout",
    "G": "G - Navigation & IA",
    "H": "H - Content Depth & Market Alignment",
    "I": "I - Conversion & Forms",
    "J": "J - SEO & Metadata",
    "K": "K - Accessibility",
    "L": "L - Performance & Engineering",
    "M": "M - Trust, Launch & Operations",
}
CAT_WAVE = {
    "A": 1, "B": 1,
    "C": 2, "E": 2,
    "D": 3, "F": 3, "G": 3,
    "H": 4, "I": 4,
    "J": 5, "K": 5, "L": 5, "M": 5,
}
WAVE_NAME = {
    1: "Wave 1 - Brand Foundation",
    2: "Wave 2 - Visual & Motion System",
    3: "Wave 3 - Page Experience & Navigation",
    4: "Wave 4 - Content & Conversion",
    5: "Wave 5 - SEO, A11y, Performance & Launch",
}
CAT_ORDER = {c: i for i, c in enumerate("ABCDEFGHIJKLM")}

ALL = ITEMS_A + ITEMS_B + ITEMS_C + ITEMS_E + ITEMS_D + ITEMS_F + ITEMS_G + ITEMS_H + ITEMS_I + ITEMS_J + ITEMS_K + ITEMS_L + ITEMS_M
ALL.sort(key=lambda r: (CAT_WAVE[r[0]], CAT_ORDER[r[0]]))

assert len(ALL) >= 500, f"Change list must exceed 500 items, got {len(ALL)}"

PRI_STYLE = {
    "P0": ("C0392B", "FDEDEC"),
    "P1": ("D4820A", "FEF9E7"),
    "P2": ("1B7D46", "E8F5E9"),
}
SEV_STYLE = {
    "Critical": ("C0392B", "FDEDEC"),
    "High": ("D4820A", "FEF9E7"),
    "Medium": ("37352F", None),
}

wb = Workbook()

# ---------------------------------------------------------------- Read Me
ws = wb.active
ws.title = "Read Me"
ws.sheet_properties.tabColor = "18142D"
readme_rows = [
    ("Purpose", "Complete, evidence-based change list to take the current achalasolutions.com build to the expected Fortune-100 standard: authentic brand (logo + colors), premium motion, real visuals, varied page design, deep non-generic content, conversion, SEO and launch readiness."),
    ("Audit verdict", "The current build is a text-only skeleton: an invented cyan hexagon logo replaces the real orange/navy brand, the only animation on 633 pages is a single 0.5s fade, there are zero visual assets, every page renders through one identical template, and machine-generated content artifacts are visible on capability pages (truncated meta descriptions, stitched hero sentences, repeated boilerplate)."),
    ("Total changes", f"{len(ALL)} items across 13 categories and 5 delivery waves."),
    ("How to use", "Work the Master Change List by wave. Set the Status column (Pending / In Progress / Done / Blocked) as you go; P0 rows are identity-breaking and ship first inside each wave."),
    ("Scope baseline", "633 content pages + system templates (header, footer, forms, search, 404, sitemap). Item IDs CHG-001 to CHG-%03d are stable references for tracking." % len(ALL)),
    ("Priority legend", "P0 = identity-breaking or broken output, fix immediately. P1 = major gap vs current market standard. P2 = polish that separates good from premium."),
    ("Impact / Effort", "Impact: H/M/L expected effect on the perceived quality. Effort: S under half a day, M 1-2 days, L 2+ days (single-item estimates, several include batch work across 633 pages)."),
    ("Brand source", "All colors sampled directly from the supplied achala_logo.png: orange #d20000 block, navy #2b5672 wordmark. See the Brand Reference sheet for ramps and rules."),
    ("Placeholders", "Items marked with client inputs (phone, office addresses, leadership names/photos, legal texts, partner approvals, video footage) are flagged in the spec column; these are the only fields we cannot complete."),
]
last_col = 3
setup_sheet(ws, title="Achala IT Solutions Website Overhaul - Change List", last_col=last_col)
ws.cell(row=4, column=2, value="Section")
ws.cell(row=4, column=3, value="Detail")
style_header_row(ws, 4, 2, last_col)
r = 5
for i, (k, v) in enumerate(readme_rows):
    ws.cell(row=r, column=2, value=k)
    ws.cell(row=r, column=3, value=v)
    style_data_row(ws, r, 2, last_col, i)
    c = ws.cell(row=r, column=2)
    c.font = Font(name=FONT_NAME, size=11, bold=HEADER_BOLD, color=PRIMARY)
    vcell = ws.cell(row=r, column=3)
    vcell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws.cell(row=r, column=2).alignment = Alignment(horizontal="left", vertical="top")
    ws.row_dimensions[r].height = max(22, ceil(len(v) / 95) * 14 + 8)
    r += 1
# summary block
r += 1
ws.cell(row=r, column=2, value="Item counts")
ws.cell(row=r, column=2).font = Font(name=FONT_NAME, size=12, bold=HEADER_BOLD, color=PRIMARY)
r += 1
p0 = sum(1 for x in ALL if x[5] == "P0")
p1 = sum(1 for x in ALL if x[5] == "P1")
p2 = sum(1 for x in ALL if x[5] == "P2")
wave_counts = {w: sum(1 for x in ALL if CAT_WAVE[x[0]] == w) for w in range(1, 6)}
summary_rows = [
    ("Total change items", str(len(ALL))),
    ("P0 (identity-breaking)", str(p0)),
    ("P1 (major gap)", str(p1)),
    ("P2 (polish)", str(p2)),
    ("Wave 1 - Brand Foundation", str(wave_counts[1])),
    ("Wave 2 - Visual & Motion System", str(wave_counts[2])),
    ("Wave 3 - Page Experience & Navigation", str(wave_counts[3])),
    ("Wave 4 - Content & Conversion", str(wave_counts[4])),
    ("Wave 5 - SEO, A11y, Performance & Launch", str(wave_counts[5])),
]
for i, (k, v) in enumerate(summary_rows):
    ws.cell(row=r, column=2, value=k)
    ws.cell(row=r, column=3, value=v)
    style_data_row(ws, r, 2, last_col, i)
    r += 1
ws.column_dimensions["B"].width = 34
ws.column_dimensions["C"].width = 110

# ---------------------------------------------------------------- Audit Findings
ws2 = wb.create_sheet("Audit Findings")
ws2.sheet_properties.tabColor = "C0392B"
findings = [
    ("Brand logo", "Header/footer render a self-invented cyan hexagon-with-Q mark; the real brand is an orange block with white 'achala' plus navy 'software' whose 'o' is an red dot.", "src/components/site/Logo.tsx lines 6-16", "Critical", "Wave 1"),
    ("Brand favicon", "The site icon repeats the invented hexagon, so browser tabs and app icons are off-brand.", "src/app/icon.svg", "Critical", "Wave 1"),
    ("Brand colors", "Brand tokens are cyan #22D3EE / deep cyan #1B6B7A / teal #0E7490; the logo's orange #d20000 and navy #2b5672 appear nowhere.", "src/app/globals.css lines 44-55", "Critical", "Wave 1"),
    ("Dark surfaces", "Dark bands use gray-ink #0a1424/#0e1b30/#14263f instead of the brand navy family.", "src/app/globals.css; HomeView.tsx; SiteFooter.tsx", "High", "Wave 1"),
    ("Motion", "The only animation on all 633 pages is a 0.5s fade-up (Reveal). No hero choreography, count-ups, marquees, page transitions or hover choreography.", "src/components/site/Reveal.tsx", "Critical", "Wave 2"),
    ("Visual assets", "Zero imagery anywhere: no tower/industry icons, no diagrams, no photography, no share images. The entire site is text on cards.", "src/components/site/*; public/", "Critical", "Wave 2"),
    ("Template monotony", "One template (PageHero + prose + bullets + table + CTA + related rail) renders every non-home page; no layout variety.", "src/components/site/PagePieces.tsx ContentPage()", "Critical", "Wave 3"),
    ("Hero quality", "Hero is a lone paragraph on a flat band; h1 tops out at 52px; no visual, no motion, no proof.", "src/components/site/HomeView.tsx lines 16-52", "High", "Wave 2/3"),
    ("Content artifact 1", "Meta descriptions truncate mid-sentence (e.g. '...onboarding friction, service resolution and.').", "src/content/pages/industries_*_capabilities_*.json", "Critical", "Wave 4"),
    ("Content artifact 2", "Machine-stitched hero sentences with casing artifacts (e.g. 'ai that answers to the p&l applied to the retail & consumer banking operating unit of Banking & Financial Services.').", "same capability page JSONs", "Critical", "Wave 4"),
    ("Content artifact 3", "'The pattern composes X, Y, Z from the tower, wired into...' boilerplate repeats across hundreds of capability pages.", "capability page JSONs", "Critical", "Wave 4"),
    ("Content artifact 4", "Grammar chains like 'on Achala Compass and Achala Forge and Achala Nexus'.", "capability page JSONs", "High", "Wave 4"),
    ("Content depth", "Capability pages average ~404 words; thin for deep-tech authority content.", "words field in page JSONs", "High", "Wave 4"),
    ("Megamenu", "Text-only megamenu with '+N more' truncation caps; no icons, featured content or CTAs.", "src/components/site/SiteHeader.tsx lines 45-59", "High", "Wave 3"),
    ("Search", "Search is a bare page with no overlay, shortcuts or grouping.", "src/app/search/page.tsx", "Medium", "Wave 3"),
    ("Contact form", "Minimal form: no routing fields, inline validation polish, consent granularity or success journey.", "src/components/site/ContactForm.tsx", "High", "Wave 4"),
    ("Share metadata", "No per-page OG/Twitter tags and no OG images exist; shares render bare links.", "src/app/layout.tsx; [[...slug]]/page.tsx", "Critical", "Wave 1/5"),
    ("Structured data", "Only root Organization/WebSite JSON-LD; no BreadcrumbList/Service/Article schema on deep pages.", "src/app/layout.tsx", "Medium", "Wave 5"),
    ("Stats presentation", "Stat strips are static text; no count-up or emphasis treatment.", "PagePieces.tsx StatsStrip()", "High", "Wave 2"),
    ("CTA sameness", "The same two CTAs repeat on every page hero regardless of template context.", "PagePieces.tsx PageHero() lines 68-81", "High", "Wave 3"),
    ("Related content", "Related pages render as a plain list, not visual cards.", "PagePieces.tsx RelatedRail()", "Medium", "Wave 3"),
    ("Bundle bloat", "About 45 unused shadcn/ui components (chart, sidebar, carousel, command...) sit in the repo and bundle path.", "src/components/ui/*", "Medium", "Wave 5"),
    ("Font loading", "Fonts load via @fontsource imports rather than an optimized next/font strategy with preload/subset.", "src/app/layout.tsx lines 3-4", "Medium", "Wave 1/5"),
    ("Textures", "The dark-band dot grid is cyan; the only texture used site-wide.", "src/app/globals.css lines 185-188", "High", "Wave 1"),
    ("Footer gaps", "Footer has link columns and a form but no newsletter, social icons, phone or office addresses.", "src/components/site/SiteFooter.tsx", "High", "Wave 3/4"),
    ("Hero meta chips", "A generic 'Published <date>' pill appears on templates where it adds no meaning.", "PagePieces.tsx ContentPage() lines 293-297", "Medium", "Wave 3"),
]
fheaders = ["#", "Area", "Finding", "Evidence location", "Severity", "Fix wave"]
setup_sheet(ws2, title="Audit Findings - Evidence Base", last_col=len(fheaders) + 1)
for col, h in enumerate(fheaders, 2):
    ws2.cell(row=4, column=col, value=h)
style_header_row(ws2, 4, 2, len(fheaders) + 1)
for i, (area, finding, ev, sev, wave) in enumerate(findings):
    r = 5 + i
    vals = [i + 1, area, finding, ev, sev, wave]
    for col, v in enumerate(vals, 2):
        ws2.cell(row=r, column=col, value=v)
    style_data_row(ws2, r, 2, len(fheaders) + 1, i)
    sc = ws2.cell(row=r, column=6)
    fg, bg = SEV_STYLE[sev]
    sc.font = Font(name=FONT_NAME, size=11, bold=HEADER_BOLD, color=fg)
    if bg:
        sc.fill = PatternFill("solid", fgColor=bg)
    ws2.cell(row=r, column=4).alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws2.row_dimensions[r].height = max(24, ceil(len(finding) / 62) * 14 + 8)
widths2 = {"B": 5, "C": 16, "D": 78, "E": 40, "F": 11, "G": 9}
for k, w in widths2.items():
    ws2.column_dimensions[k].width = w

# ---------------------------------------------------------------- Master Change List
ws3 = wb.create_sheet("Master Change List")
ws3.sheet_properties.tabColor = "FE5722"
headers = ["ID", "Wave", "Category", "Scope", "Change item", "Specification", "Reference bar", "Priority", "Impact", "Effort", "Status"]
setup_sheet(ws3, title="Master Change List - %d items" % len(ALL), last_col=len(headers) + 1)
for col, h in enumerate(headers, 2):
    ws3.cell(row=4, column=col, value=h)
style_header_row(ws3, 4, 2, len(headers) + 1)

r = 5
for i, (cat, scope, item, spec, ref, pri, imp, eff) in enumerate(ALL):
    rid = "CHG-%03d" % (i + 1)
    wave = WAVE_NAME[CAT_WAVE[cat]]
    catn = CAT_NAME[cat]
    vals = [rid, wave, catn, scope, item, spec, ref, pri, imp, eff, "Pending"]
    for col, v in enumerate(vals, 2):
        ws3.cell(row=r, column=col, value=v)
    style_data_row(ws3, r, 2, len(headers) + 1, i)
    # emphasis cells
    pc = ws3.cell(row=r, column=9)
    fg, bg = PRI_STYLE[pri]
    pc.font = Font(name=FONT_NAME, size=11, bold=HEADER_BOLD, color=fg)
    if bg:
        pc.fill = PatternFill("solid", fgColor=bg)
    pc.alignment = Alignment(horizontal="center", vertical="center")
    ws3.cell(row=r, column=2).font = Font(name=FONT_NAME, size=11, color=PRIMARY)
    for col in (10, 11, 12):
        ws3.cell(row=r, column=col).alignment = Alignment(horizontal="center", vertical="center")
    for col in (6, 7):
        ws3.cell(row=r, column=col).alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws3.cell(row=r, column=8).alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    lines = max(ceil(len(spec) / 55), ceil(len(item) / 36), ceil(len(ref) / 24), 1)
    ws3.row_dimensions[r].height = min(100, max(24, lines * 13 + 7))
    r += 1

# total row
ws3.cell(row=r, column=2, value="Total")
ws3.cell(row=r, column=6, value=f"{len(ALL)} change items")
style_total_row(ws3, r, 2, len(headers) + 1)

ws3.freeze_panes = "C5"
ws3.auto_filter.ref = f"B4:{get_column_letter(len(headers) + 1)}{r - 1}"
widths3 = {"B": 10, "C": 30, "D": 26, "E": 24, "F": 36, "G": 55, "H": 24, "I": 9, "J": 8, "K": 8, "L": 12}
for k, w in widths3.items():
    ws3.column_dimensions[k].width = w
dv = DataValidation(type="list", formula1='"Pending,In Progress,Done,Blocked"', allow_blank=True, showDropDown=False)
ws3.add_data_validation(dv)
dv.add(f"L5:L{r - 1}")

# ---------------------------------------------------------------- Roadmap
ws4 = wb.create_sheet("Roadmap")
ws4.sheet_properties.tabColor = "1B6B7A"
rheaders = ["Wave", "Focus", "Items", "Ships", "Indicative value delivered (cumulative)", "Depends on"]
setup_sheet(ws4, title="Delivery Roadmap", last_col=len(rheaders) + 1)
roadmap = [
    (WAVE_NAME[1], "Make it Achala again: authentic logo everywhere, orange/navy token system, type scale, core components (buttons, cards, forms, CTA band), font loading, default share image, favicon set.", wave_counts[1], "Real logo + brand tokens live on all 633 pages; design-system base for everything after.", "About 30%", "-"),
    (W2N := WAVE_NAME[2], "Make it feel expensive: motion library, hero choreography, count-ups, marquees, carousels, icon system, tower/industry icons, platform diagrams and mockups, OG generator, textures.", wave_counts[2], "The site gains the visual and motion layer it entirely lacks today.", "About 55%", "Wave 1"),
    (WAVE_NAME[3], "Make it designed: homepage rebuild (11 sections), 25 template redesigns with six layout patterns, PageHero v2, megamenu, search overlay, mobile nav, footer enrichment.", wave_counts[3], "No two page types look alike; navigation matches a Fortune-100 site.", "About 72%", "Waves 1-2"),
    (WAVE_NAME[4], "Make it deep and converting: de-template 633 pages, unique market-dated narratives, case metric systems, question modules, contact/briefing forms with routing and backend.", wave_counts[4], "Content reads human and current; every form path works end-to-end.", "About 85%", "Waves 1-3"),
    (WAVE_NAME[5], "Make it bulletproof: metadata/schema/lint gates, breadcrumb schema, a11y gates (contrast, focus, keyboard), performance budgets and static-export verification, launch ops.", wave_counts[5], "Release-ready: hosted, indexed, accessible, fast, maintainable.", "About 90%+", "Waves 1-4"),
]
for col, h in enumerate(rheaders, 2):
    ws4.cell(row=4, column=col, value=h)
style_header_row(ws4, 4, 2, len(rheaders) + 1)
for i, (w, focus, n, ships, val, dep) in enumerate(roadmap):
    r = 5 + i
    vals = [w, focus, n, ships, val, dep]
    for col, v in enumerate(vals, 2):
        ws4.cell(row=r, column=col, value=v)
    style_data_row(ws4, r, 2, len(rheaders) + 1, i)
    ws4.cell(row=r, column=3).alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws4.cell(row=r, column=5).alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws4.cell(row=r, column=4).alignment = Alignment(horizontal="center", vertical="center")
    ws4.row_dimensions[r].height = max(40, ceil(len(focus) / 60) * 14 + 10, ceil(len(ships) / 46) * 14 + 10)
r = 5 + len(roadmap) + 1
ws4.cell(row=r, column=2, value="Note: the value percentages are indicative of the overhaul's perceived-quality curve against the current-market bar, not a formal metric. Client-supplied inputs (office addresses, phone, leadership names and photos, legal texts, partner approvals, video footage) remain the only open items.")
ws4.cell(row=r, column=2).font = font_caption()
ws4.cell(row=r, column=2).alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
ws4.merge_cells(start_row=r, start_column=2, end_row=r, end_column=len(rheaders) + 1)
ws4.row_dimensions[r].height = 40
widths4 = {"B": 34, "C": 62, "D": 8, "E": 52, "F": 24, "G": 12}
for k, w in widths4.items():
    ws4.column_dimensions[k].width = w

# ---------------------------------------------------------------- Brand Reference
ws5 = wb.create_sheet("Brand Reference")
ws5.sheet_properties.tabColor = "FE5722"
bheaders = ["Token", "Hex", "Source", "Usage rule", "Accessibility note"]
setup_sheet(ws5, title="Achala IT Solutions Brand Reference (sampled from the supplied logo)", last_col=len(bheaders) + 1)
colors = [
    ("Achala Red (primary)", "#d20000", "Sampled: orange block in logo", "Primary accent: primary buttons, kickers, active states, key metrics, progress. Keep to roughly 10% of any view.", "On white, use for large text (18px+ bold) and UI elements only."),
    ("Orange Deep (text-safe)", "#8f0000", "Derived ramp", "Small orange text and inline links on white.", "Approx 4.6:1 on white; passes AA for body text."),
    ("Orange Hover", "#a80000", "Derived ramp", "Button hover state.", "Use behind white labels at large sizes only."),
    ("Orange Tint", "#fdecec", "Derived ramp", "Soft backgrounds, hover washes, callout fills.", "Safe background with navy or Orange Deep text."),
    ("Achala Navy (primary dark)", "#2b5672", "Sampled: 'software' wordmark", "All dark surfaces: hero bands, CTA bands, footer, headers of tables.", "White text on navy passes AA."),
    ("Navy 900", "#0e2230", "Derived ramp", "Deepest fields, gradient ends.", "White text passes AA."),
    ("Navy 700", "#3a6983", "Derived ramp", "Elevated dark panels, glass cards.", "White or white/70 text passes AA."),
    ("Navy 500", "#568aa6", "Derived ramp", "Borders and dividers on dark.", "Decorative only."),
    ("Mist", "#F6F7FB", "Derived neutral", "Alternating light sections, chip fills.", "Navy text passes AA."),
    ("Line", "#E5E7F0", "Derived neutral", "Hairlines and card borders.", "Decorative only."),
    ("White", "#FFFFFF", "Sampled: right side of logo", "Main background, logo 'software' field, reversed wordmark.", "-"),
    ("REMOVE: Cyan", "#22D3EE", "Current code (wrong brand)", "Prohibited after Wave 1: delete token and all usages.", "Exists only until migration."),
    ("REMOVE: Deep cyan / teal", "#1B6B7A / #0E7490", "Current code (wrong brand)", "Prohibited after Wave 1.", "Exists only until migration."),
    ("REMOVE: Gray-ink", "#0A1424 family", "Current code (wrong brand)", "Prohibited after Wave 1: replaced by navy 800/700/600.", "Exists only until migration."),
]
for col, h in enumerate(bheaders, 2):
    ws5.cell(row=4, column=col, value=h)
style_header_row(ws5, 4, 2, len(bheaders) + 1)
for i, (tok, hx, src, use, a11y) in enumerate(colors):
    r = 5 + i
    vals = [tok, hx, src, use, a11y]
    for col, v in enumerate(vals, 2):
        ws5.cell(row=r, column=col, value=v)
    style_data_row(ws5, r, 2, len(bheaders) + 1, i)
    hx_cell = ws5.cell(row=r, column=3)
    hx_cell.font = Font(name="Consolas", size=11, color=NEUTRAL_900)
    if tok.startswith("REMOVE"):
        for col in range(2, len(bheaders) + 2):
            ws5.cell(row=r, column=col).font = Font(name=FONT_NAME, size=11, color="C0392B", strike=True)
    ws5.cell(row=r, column=5).alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws5.row_dimensions[r].height = max(24, ceil(len(use) / 52) * 13 + 8)
r = 5 + len(colors) + 2
ws5.cell(row=r, column=2, value="Logo rules")
ws5.cell(row=r, column=2).font = Font(name=FONT_NAME, size=12, bold=HEADER_BOLD, color=PRIMARY)
r += 1
logo_rules = [
    ("Lockup", "Orange block with white lowercase 'achala' + navy lowercase 'software' whose 'o' is the same red dot. Lowercase always."),
    ("Variants", "Full color on light; reversed (white wordmark, orange block intact) on navy; mono navy for print/legal."),
    ("Clearspace", "Equal to the height of the orange block on all sides; minimum width 120px."),
    ("Favicon", "Orange block with a white 'd' glyph."),
    ("Prohibited", "Recoloring, stretching, drop shadows, gradients on the mark, cyan/teal variants, rotation."),
]
for i, (k, v) in enumerate(logo_rules):
    rr = r + i
    ws5.cell(row=rr, column=2, value=k)
    ws5.cell(row=rr, column=3, value=v)
    style_data_row(ws5, rr, 2, len(bheaders) + 1, i)
    ws5.cell(row=rr, column=2).font = Font(name=FONT_NAME, size=11, bold=HEADER_BOLD, color=PRIMARY)
    ws5.cell(row=rr, column=3).alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws5.merge_cells(start_row=rr, start_column=3, end_row=rr, end_column=len(bheaders) + 1)
    ws5.row_dimensions[rr].height = 24
widths5 = {"B": 26, "C": 22, "D": 30, "E": 52, "F": 42}
for k, w in widths5.items():
    ws5.column_dimensions[k].width = w

wb.properties.creator = "Z.ai"
out = "/home/z/my-project/download/achala_Website_Overhaul_Change_List.xlsx"
os.makedirs(os.path.dirname(out), exist_ok=True)
wb.save(out)
print("Saved", out)
print("Total items:", len(ALL))
print("P0/P1/P2:", p0, p1, p2)
print("Wave counts:", wave_counts)
by_cat = {}
for x in ALL:
    by_cat[x[0]] = by_cat.get(x[0], 0) + 1
print("By category:", by_cat)
