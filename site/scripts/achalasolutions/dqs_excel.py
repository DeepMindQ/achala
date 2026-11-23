# -*- coding: utf-8 -*-
"""Achala IT Solutions — Excel page inventory generator (xlsx skill compliant)."""

import sys, os, json

XLSX_SKILL_DIR = "/home/z/my-project/skills/xlsx"
for sub in [XLSX_SKILL_DIR, os.path.join(XLSX_SKILL_DIR, "templates")]:
    if sub not in sys.path:
        sys.path.insert(0, sub)

from base import (setup_sheet, style_header_row, style_data_row, style_total_row,
                  font_title, font_caption, font_body, font_subheader, FONT_NAME)
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter

OUT = "/home/z/my-project/download/achalasolutions-website-content/achala_Soft_Page_Inventory.xlsx"
INVENTORY = "/home/z/my-project/scripts/achalasolutions/out/inventory.json"

inv = json.load(open(INVENTORY, encoding="utf-8"))
assert len(inv) == 602

wb = Workbook()

# ============================ Sheet 1: Read Me ============================
ws = wb.active
ws.title = "Read Me"
setup_sheet(ws, title="Achala IT Solutions Website Content Package — Page Inventory", last_col=8)
rows = [
    ("Section", "Detail"),
    ("Purpose", "Master page inventory for www.achalasolutions.com — every page with menu level, URL, template, SEO metadata, word target and content-volume reference."),
    ("How to use", "Filter by Section or Volume to hand content batches to designers/developers. One row = one web page. The URL Path column defines the routing taxonomy."),
    ("Page count", "602 pages across 11 content volumes (V01–V11) + this workbook."),
    ("Levels", "Menu L1 (primary nav) → L2 (submenu) → L3 (sub-submenu) → L4 (leaf, where present)."),
    ("Templates", "18 template types (home, hub, service, industry, sub-industry, capability, solution, platform, case study, insight, company, approach, contact, legal)."),
    ("SEO", "SEO Title ≤ 60 chars, Meta Description ≤ 155 chars — pre-written for every page."),
    ("Priorities", "P0 = launch-critical hubs · P1 = core leaf pages · P2 = long-tail/utility."),
    ("Word targets", "Targets are editorial guidance; 'Composed Words' shows delivered draft length."),
    ("Status", "Draft complete for all pages. Review column is for your editorial workflow."),
    ("Placeholders", "【…】 marks information only you can supply (addresses, names, legal text, links)."),
    ("Source", "Rebuilt and expanded from the prior content baseline content, re-mapped to a Fortune-500-grade IA for Achala IT Solutions."),
]
r = 4
for i, (a, b) in enumerate(rows):
    r = 4 + i
    ws.cell(row=r, column=2, value=a)
    ws.cell(row=r, column=3, value=b)
    if i == 0:
        style_header_row(ws, r, 2, 3)
    else:
        style_data_row(ws, r, 2, 3, i - 1)
ws.column_dimensions["B"].width = 16
ws.column_dimensions["C"].width = 110
for rr in range(5, r + 1):
    ws.cell(row=rr, column=3).alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[rr].height = 30

# ============================ Sheet 2: Sitemap Inventory ============================
ws2 = wb.create_sheet("Sitemap Inventory")
headers = ["ID", "Section", "Menu L1", "Menu L2", "Menu L3", "Menu L4", "Page Title", "URL Path",
           "Template", "SEO Title", "Meta Description", "Word Target", "Composed Words",
           "Volume", "Priority", "Status"]
setup_sheet(ws2, title="Sitemap Inventory — 602 pages", last_col=1 + len(headers))
for ci, h in enumerate(headers, 2):
    ws2.cell(row=4, column=ci, value=h)
style_header_row(ws2, 4, 2, 1 + len(headers))
r = 5
for i, p in enumerate(inv):
    vals = [p["id"], p["section"], p["l1"] or "—", p["l2"] or "—", p["l3"] or "—", p["l4"] or "—",
            p["title"], p["url"], p["template"], p["seo_title"], p["meta_description"],
            p["word_target"], p["composed_words"], p["volume"], p["priority"], "Draft complete"]
    for ci, v in enumerate(vals, 2):
        ws2.cell(row=r, column=ci, value=v)
    style_data_row(ws2, r, 2, 1 + len(headers), i)
    r += 1
widths = [22, 15, 12, 26, 26, 22, 34, 46, 20, 46, 60, 11, 13, 9, 9, 14]
for ci, w in enumerate(widths, 2):
    ws2.column_dimensions[get_column_letter(ci)].width = w
ws2.freeze_panes = "D5"
ws2.auto_filter.ref = f"B4:{get_column_letter(1 + len(headers))}{r - 1}"

# ============================ Sheet 3: Menu Map ============================
ws3 = wb.create_sheet("Menu Map")
setup_sheet(ws3, title="Primary Navigation & Mega Menu Map", last_col=4)
menu_rows = [
    ("Level", "Item", "Links to", "Notes"),
    ("L1", "Services", "/services/", "Mega menu: 8 tower columns, each listing its services"),
    ("L2", "Services → Applied AI & Generative AI", "/services/applied-ai-generative-ai/", "Tower hub; flyout lists 7 services"),
    ("L2", "Services → Agentic AI & Hyperautomation", "/services/agentic-ai-hyperautomation/", "Tower hub; 7 services"),
    ("L2", "Services → Data, Analytics & Lakehouse", "/services/data-analytics-lakehouse/", "Tower hub; 7 services"),
    ("L2", "Services → Cybersecurity & Zero-Trust", "/services/cybersecurity-zero-trust/", "Tower hub; 7 services"),
    ("L2", "Services → Cloud, Edge & Platform Engineering", "/services/cloud-edge-platform-engineering/", "Tower hub; 7 services"),
    ("L2", "Services → Quantum & Advanced Compute", "/services/quantum-advanced-compute/", "Tower hub; 6 services"),
    ("L2", "Services → Blockchain & Digital Trust", "/services/blockchain-digital-trust/", "Tower hub; 6 services"),
    ("L2", "Services → IoT, Digital Twin & Robotics", "/services/iot-digital-twin-robotics/", "Tower hub; 7 services"),
    ("L1", "Industries", "/industries/", "Mega menu: 12 industries; industry flyout shows 4 sub-industries + 8 capability links"),
    ("L2", "Industries → Banking & Financial Services", "/industries/banking-financial-services/", "Hub → 4 sub-industries + capability grid"),
    ("L2", "Industries → Insurance & Risk", "/industries/insurance/", "Hub → 4 sub-industries"),
    ("L2", "Industries → Healthcare & Life Sciences", "/industries/healthcare-life-sciences/", "Hub → 4 sub-industries"),
    ("L2", "Industries → Manufacturing & Industrial", "/industries/manufacturing/", "Hub → 4 sub-industries"),
    ("L2", "Industries → Retail & Consumer Goods", "/industries/retail-consumer-goods/", "Hub → 4 sub-industries"),
    ("L2", "Industries → Telecom, Media & Entertainment", "/industries/telecom-media/", "Hub → 4 sub-industries"),
    ("L2", "Industries → Energy & Utilities", "/industries/energy-utilities/", "Hub → 4 sub-industries"),
    ("L2", "Industries → Logistics & Supply Chain", "/industries/logistics-supply-chain/", "Hub → 4 sub-industries"),
    ("L2", "Industries → Public Sector & Government", "/industries/public-sector/", "Hub → 4 sub-industries"),
    ("L2", "Industries → Education & Research", "/industries/education-research/", "Hub → 4 sub-industries"),
    ("L2", "Industries → Technology & SaaS", "/industries/technology-saas/", "Hub → 4 sub-industries"),
    ("L2", "Industries → Agriculture & Food Systems", "/industries/agriculture-food/", "Hub → 4 sub-industries"),
    ("L1", "Solutions", "/solutions/", "Mega menu: 4 categories (Growth, Risk, Ops, Workforce) × 6 solutions"),
    ("L1", "Platforms", "/platforms/", "Mega menu: 8 platforms; each flyout: Overview, Architecture & Trust, Industry Use Cases"),
    ("L1", "Case Studies", "/case-studies/", "Hub with industry filter; 36 anonymized engagements"),
    ("L1", "Insights", "/insights/", "Mega menu: 8 tower categories"),
    ("L1", "About Us", "/about-us/", "Flyout: About, Why Achala IT Solutions, Our Approach (4), Leadership, Global Offices, Values & Culture, Careers, Newsroom, Partner Ecosystem"),
    ("CTA", "Contact", "/contact/", "Primary CTA button: 'Book a Briefing' → /book-a-briefing/"),
    ("Footer", "Legal & utility", "/privacy-policy/ … /status/", "Privacy, Terms, Cookies, Accessibility, Sitemap, Status"),
    ("L3/L4 pattern", "Capability pages", "/industries/{industry}/capabilities/{tower}/ and /industries/{industry}/{sub}/capabilities/{tower}/", "336 capability pages form the deepest menu tier"),
]
r = 4
for i, row in enumerate(menu_rows):
    rr = 4 + i
    for ci, v in enumerate(row, 2):
        ws3.cell(row=rr, column=ci, value=v)
    if i == 0:
        style_header_row(ws3, rr, 2, 5)
    else:
        style_data_row(ws3, rr, 2, 5, i - 1)
for ci, w in zip(range(2, 6), [12, 44, 52, 62]):
    ws3.column_dimensions[get_column_letter(ci)].width = w

# ============================ Sheet 4: Summary ============================
ws4 = wb.create_sheet("Summary")
setup_sheet(ws4, title="Package Summary", last_col=5)
from collections import Counter, defaultdict
sec = Counter(p["section"] for p in inv)
vol = defaultdict(lambda: [0, 0])
for p in inv:
    vol[p["volume"]][0] += 1
    vol[p["volume"]][1] += p["composed_words"]
VOL_NAMES = {
    "V01": "Volume 01 — Home & Services", "V02": "Volume 02 — Industries A (Hubs & Sub-Industries)",
    "V03": "Volume 03 — Industries B (Hubs & Sub-Industries)", "V04": "Volume 04 — Industry Capability Pages A",
    "V05": "Volume 05 — Industry Capability Pages B", "V06": "Volume 06 — Sub-Industry Capability Pages A",
    "V07": "Volume 07 — Sub-Industry Capability Pages B", "V08": "Volume 08 — Solutions & Platforms",
    "V09": "Volume 09 — Case Studies", "V10": "Volume 10 — Company, Approach & Contact",
    "V11": "Volume 11 — Insights Library",
}
r = 4
hdr = ["Section", "Pages"]
for ci, h in enumerate(hdr, 2):
    ws4.cell(row=r, column=ci, value=h)
style_header_row(ws4, r, 2, 3)
r += 1
i = 0
for k in ["Home", "Services", "Industries", "Solutions", "Platforms", "Case Studies",
          "Company", "Approach", "Insights", "Contact & Legal"]:
    ws4.cell(row=r, column=2, value=k)
    ws4.cell(row=r, column=3, value=sec[k])
    style_data_row(ws4, r, 2, 3, i)
    r += 1
    i += 1
ws4.cell(row=r, column=2, value="Total")
ws4.cell(row=r, column=3, value=len(inv))
style_total_row(ws4, r, 2, 3)
r += 2
ws4.cell(row=r, column=2, value="Content volumes")
ws4.cell(row=r, column=2).font = font_subheader()
r += 1
for ci, h in enumerate(["Volume", "Pages", "Words"], 2):
    ws4.cell(row=r, column=ci, value=h)
style_header_row(ws4, r, 2, 4)
r += 1
i = 0
tot_w = 0
for v in sorted(vol):
    ws4.cell(row=r, column=2, value=VOL_NAMES[v])
    ws4.cell(row=r, column=3, value=vol[v][0])
    ws4.cell(row=r, column=4, value=vol[v][1])
    style_data_row(ws4, r, 2, 4, i)
    tot_w += vol[v][1]
    r += 1
    i += 1
ws4.cell(row=r, column=2, value="Total draft words")
ws4.cell(row=r, column=3, value=len(inv))
ws4.cell(row=r, column=4, value=tot_w)
style_total_row(ws4, r, 2, 4)
for ci, w in zip(range(2, 5), [50, 12, 14]):
    ws4.column_dimensions[get_column_letter(ci)].width = w

# ============================ Sheet 5: Content Guidelines ============================
ws5 = wb.create_sheet("Content Guidelines")
setup_sheet(ws5, title="Voice, Terminology & Editorial Rules", last_col=3)
guide = [
    ("Topic", "Rule"),
    ("Voice", "Direct, evidence-led, senior. Short declarative sentences. No hype adjectives without a number or an artifact behind them."),
    ("Point of view", "First person plural ('we') for Achala IT Solutions; second person ('your') for the client. Never 'solutions provider' speak."),
    ("Specificity floor", "Every page must name real things: regimes (DORA, PCI DSS 4.0, EU AI Act), technologies (Databricks, Kafka, SPIFFE), processes (KYC refresh, FNOL, OEE), and KPIs with ranges."),
    ("Banned phrases", "'cutting-edge', 'best-in-class', 'world-class', 'synergy', 'digital transformation journey', 'unlock the power of'."),
    ("Claims policy", "Invented marketing stats are marked in the Brand sheet of this package for legal review. Case-study metrics are anonymized and illustrative — validate before publication."),
    ("Placeholders", "【…】 marks must be filled before launch: street addresses, executive names, legal text, portal links."),
    ("Numbers", "Use ranges with dashes (30-45%), not 'up to X'. Never mix currencies on a page."),
    ("Reading level", "Executive-readable; assume the reader has 8 minutes. Front-load the outcome, then the mechanism."),
    ("SEO", "One H1 per page (the Page Title). H2s from the content blocks. SEO Title ≤ 60 chars, Meta ≤ 155 chars — provided per page."),
    ("CTAs", "One primary CTA per page, consistent with the CTA line in each content block. Never more than two CTAs on a page."),
    ("Sources", "the prior content baseline content was rebuilt and expanded — no copy was carried over verbatim. Voice family: deep-tech, patent/outcome-aware, audit-first."),
]
r = 4
for i, row in enumerate(guide):
    rr = 4 + i
    for ci, v in enumerate(row, 2):
        ws5.cell(row=rr, column=ci, value=v)
    if i == 0:
        style_header_row(ws5, rr, 2, 3)
    else:
        style_data_row(ws5, rr, 2, 3, i - 1)
        ws5.cell(row=rr, column=3).alignment = Alignment(wrap_text=True, vertical="top")
        ws5.row_dimensions[rr].height = 30
ws5.column_dimensions["B"].width = 20
ws5.column_dimensions["C"].width = 120

wb.properties.creator = "Z.ai"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
wb.save(OUT)
print("Saved", OUT)
print("Inventory rows:", len(inv))
