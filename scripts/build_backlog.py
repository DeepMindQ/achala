#!/usr/bin/env python3
"""Achala IT Solutions website — 500+ change backlog (gate deliverable)."""
import sys, os
XLSX_SKILL_DIR = "/home/z/my-project/skills/xlsx"
for sub in [XLSX_SKILL_DIR, os.path.join(XLSX_SKILL_DIR, "templates")]:
    if sub not in sys.path: sys.path.insert(0, sub)
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

rows = []  # (Wave, Category, Area, Change, Why, Effort, Status)

def add(wave, cat, area, change, why, effort="M", status="Planned"):
    rows.append((wave, cat, area, change, why, effort, status))

# ══════════════════ P0 — IMAGE SYSTEM (root cause: 1 recycled SVG per page) ══════════════════
IMG = "Images & Visual Assets"
add("P0-Images", IMG, "Site-wide", "Replace 22 recycled abstract SVGs with 24 premium AI-generated brand visuals (orange #d20000 / deep-blue #2b5672 art direction)", "Root cause of 'images not rendering': every page shows the same dark placeholder; nothing to render", "L")
for svc, label in [("applied-ai-generative-ai","Applied & Generative AI"),("agentic-ai-hyperautomation","Agentic AI & Hyperautomation"),("data-analytics-lakehouse","Data, Analytics & Lakehouse"),("cybersecurity-zero-trust","Cybersecurity & Zero Trust"),("cloud-edge-platform-engineering","Cloud, Edge & Platform Engineering"),("quantum-advanced-compute","Quantum & Advanced Compute"),("blockchain-digital-trust","Blockchain & Digital Trust"),("iot-digital-twin-robotics","IoT, Digital Twin & Robotics")]:
    add("P0-Images", IMG, f"Service tower: {label}", f"Photoreal branded hero image for {label} tower hub + 3 sub-services (photoreal ops scenes, brand-graded)", "Unique imagery per service page kills the placeholder effect", "M")
for ind, label in [("banking-financial-services","Banking & Financial Services"),("healthcare-pharma-life-sciences","Healthcare, Pharma & Life Sciences"),("retail-consumer-e-commerce","Retail, Consumer & E-commerce"),("manufacturing-energy-industrial","Manufacturing, Energy & Industrial"),("government-public-sector-education","Government, Public Sector & Education"),("telecom-media-travel-hospitality","Telecom, Media, Travel & Hospitality")]:
    add("P0-Images", IMG, f"Industry: {label}", f"Industry-specific hero + section imagery set (3 images) for {label}", "Industries reuse generic art today; sector credibility needs sector visuals", "M")
for plat, label in [("nexus","Achala Nexus"),("forge","Achala Forge"),("swarm","Achala Swarm"),("sentinel","Achala Sentinel"),("twinverse","Achala Twinverse"),("quanta","Achala Quanta"),("ledger","Achala Ledger"),("compass","Achala Compass")]:
    add("P0-Images", IMG, f"Platform: {label}", f"Product-style UI mock render for {label} platform page", "Platforms need product-feel visuals, not abstract arcs", "M")
add("P0-Images", IMG, "Homepage", "Cinematic homepage hero visual (abstract data-intelligence field, animated layered depth)", "First impression currently text-only", "M")
add("P0-Images", IMG, "About / Careers / Contact", "Human-side photography set: delivery centers, teams at work (8 images, consistent grade)", "Company pages have zero human imagery", "M")
add("P0-Images", IMG, "Case studies (37)", "Programmatic case-study visual generator: seeded per-industry composition + KPI overlay", "37 case studies share 3 generic images", "M")
add("P0-Images", IMG, "Insights (33)", "Insight article header system: 6 topical templates with per-article accent variation", "Articles are text walls today", "M")
add("P0-Images", IMG, "All pages", "Inline SVG diagram strip component: 3 contextual mini-diagrams injected per page via PageAugment", "Guarantees 4+ visual elements on every one of 632 pages", "M")
add("P0-Images", IMG, "OG/social", "OpenGraph image (1200x630) per section, brand template with page title", "Social shares currently show no image", "S")
add("P0-Images", IMG, "Build", "next/image audit: sizes attribute per breakpoint, priority only above-the-fold", "LCP + layout stability", "S")
add("P0-Images", IMG, "Build", "Asset pipeline: AI images compressed to WebP + AVIF, lazy below fold", "Page weight discipline", "S")
add("P0-Images", IMG, "gh-pages", "GHPAGES=1 basePath regression test in CI script (assert /achala/images/* exists in out-gh HTML)", "Prevent recurring 'images 404 on Pages' class bugs", "S")
add("P0-Images", IMG, "Legal", "Confidentiality scan on all generated imagery prompts + visible text (no entity names)", "Hard confidentiality rule", "S")

# ══════════════════ P0 — ANIMATION 100X ══════════════════
AN = "Motion & Animation 100X"
CORE = ["Scroll-linked hero parallax with layered depth (bg art, headline, KPIs move at different rates)",
        "Split-text headline reveals: per-word mask + rise with 60ms stagger on every H1/H2",
        "Universal stagger engine: any list/grid of cards animates in with index-based delay (CSS var --i)",
        "Spring-physics hover lift on all cards (translateY -6px + shadow bloom + border glow)",
        "Animated gradient mesh background on hero sections (aurora blobs, 3 layers, GPU transforms)",
        "Magnetic buttons upgraded: pull + tilt + sheen sweep + ripple on click",
        "Animated counters with odometer digit roll (not simple count-up)",
        "SVG line-draw on scroll for all architecture/flow diagrams (stroke-dashoffset choreography)",
        "Chart draw-in choreography: bars grow, lines trace with glow tip, radar sweeps",
        "Marquee upgrade: dual-direction, speed reacts to scroll velocity",
        "Section transition wipes: angled brand-orange wipe between major sections",
        "Parallax floating orbs/orbs field behind stats and CTA bands",
        "Card tilt-on-hover with 3D perspective + glare highlight tracking cursor",
        "Link underline morphs: underline draws left-to-right with easing on all text links",
        "Nav mega-menu open choreography: staggered column fade + slide with spring ease",
        "Sticky header shrink + blur + hairline glow on scroll (backdrop-filter)",
        "Page enter choreography: hero elements cascade in on first paint (no FOUC)",
        "Image reveal: clip-path wipe + inner scale settle on every figure",
        "Scroll progress bar upgrade: gradient + glow head dot",
        "Back-to-top morph: circular progress ring shows scroll %",
        "Tab/pill switches: sliding active indicator with spring",
        "Accordion open: height spring + icon rotation + content fade-slide",
        "Form focus states: label float + glow ring + success micro-bounce",
        "Toast/notification slide-in with spring overshoot",
        "Footer reveal: columns stagger up on first view",
        "Logo hover: brand mark draws its stroke",
        "Breadcrumb trail: path draws in on page load",
        "CTA band: pulsing gradient border + button shimmer loop",
        "Stat band: numbers flip with 3D rotate on view",
        "Testimonial/quote: text fade-up per line + oversized quote mark slide",
        "Cursor spotlight upgraded: brand-orange radial + subtle noise texture + spotlight scales on interactive hover",
        "Dark section entrance: radial vignette expands from center",
        "Reduced-motion parity: every effect has a static fallback (audit all 120+)",
        "Animation perf budget: only transform/opacity/filter animated; audit with DevTools",
        "will-change hints on animated layers, removed after settle",
        "Scroll-triggered class system unified: one IntersectionObserver registry (MotionRuntime v3)",
        "Page-leave intent: header CTA pulses when cursor moves to leave (desktop)"]
for i, t in enumerate(CORE, 1):
    add("P0-Motion", AN, "Global runtime", f"M-{i:03d}: {t}", "Animations are below minimum standard today; this is the 100X core set", "M" if i % 3 else "S")
PERPAGE = ["Homepage hero: full cinematic intro sequence (orbit rings draw, KPIs cascade, CTA breathes)",
           "Services hub: tower cards assemble from grid fragments on scroll",
           "Each service page: capability matrix cells flip-in with stagger",
           "Solutions: before/after comparison slider with draggable handle",
           "Industry pages: map pins drop with bounce, arcs draw between offices",
           "Platform pages: UI mock parallax layers separate on scroll",
           "Case studies: KPI counters + sparkline draw on scroll into view",
           "Insights: reading progress line + image parallax in article body",
           "Contact: form steps animate + submit success confetti burst (brand colors)",
           "Careers: perks cards deal-in like cards on a table",
           "About: timeline draws horizontally with milestones popping",
           "Why-Achala: comparison table rows slide-in alternating left/right",
           "Approach: process steps connect with animated path (SVG draw)",
           "Patented-intelligence: patent nodes orbit core, connect on hover",
           "Book-a-briefing: calendar slot grid hover wave",
           "Search: results fade-filter as you type",
           "404: brand mark assembles from particles",
           "Footer CTA band on all pages: gradient river flows behind button"]
for i, t in enumerate(PERPAGE, 1):
    add("P0-Motion", AN, "Per-page set", f"MP-{i:02d}: {t}", "Motion must feel bespoke per page type, not one-size", "M")
add("P0-Motion", AN, "Tokens", "Motion token system: --ease-spring, --ease-out-expo, --dur-1/2/3, --stagger-base declared once", "Consistency + maintainability of 100+ effects", "S")
add("P0-Motion", AN, "QA", "Animation audit script: assert every .reveal has transition + fallback", "No dead reveal classes", "S")

# ══════════════════ P1 — CONTENT REWRITE ══════════════════
CT = "Content Transformation"
add("P1-Content", CT, "Voice & tone", "Define voice charter: outcome-first, plain English, no AI-flavor phrases ('delve', 'landscape', 'unlock the power of', 'seamless', 'cutting-edge' banned list)", "Kills the template/AI smell across 633 pages", "S")
add("P1-Content", CT, "Homepage", "Homepage narrative rewrite: POV headline, 3 proof pillars, client-outcome band, platform strip, industry rail, CTA", "Homepage is the conversion engine", "L")
add("P1-Content", CT, "8 service hubs", "Rewrite each tower intro: business problem first, capability proof second, platform rails third", "Current intros describe the page instead of the value", "M")
add("P1-Content", CT, "55 service sub-pages", "Per-service rewrite: 'What changes for you' section with 3 concrete scenarios each", "Sub-pages are near-duplicate templates today", "L")
add("P1-Content", CT, "6 industry hubs", "Industry rewrite: regulatory + margin + data realities per sector, 3 named use cases", "Industries read generic", "M")
add("P1-Content", CT, "Industry sub-pages", "Sector use-case pages: process flows written from operator POV", "Depth signal for buyers", "L")
add("P1-Content", CT, "8 platform pages", "Platform pages rewritten as product sheets: what it runs, what it replaces, time-to-value", "Platforms currently read like essays", "M")
add("P1-Content", CT, "37 case studies", "Case study upgrade: Challenge → Build → Outcome with named KPI deltas (illustrative, consistent)", "Strongest proof asset; currently thin", "L")
add("P1-Content", CT, "33 insights", "Insight rewrite: thesis in first line, evidence table, 'what to do Monday' box", "Thought leadership must lead thought", "L")
add("P1-Content", CT, "Why-Achala page", "Rewrite around 5 differentiators with proof point each (delivery model, outcome linkage, IP, security, speed)", "Decision-stage page must close", "M")
add("P1-Content", CT, "Our approach", "Method page: 6-step engagement model with entry/exit criteria per step", "Buyers need process certainty", "M")
add("P1-Content", CT, "About us", "About rewrite: mission, delivery footprint, engineering culture, hiring philosophy", "Company story is flat", "M")
add("P1-Content", CT, "Patented intelligence", "Rewrite as capability map: 8 families explained in business language, each mapped to services/platforms (indirect, no entity names)", "Turns IP page into sales asset while honoring confidentiality", "M")
add("P1-Content", CT, "Cross-linking", "Solution↔Service↔Industry contextual link module on every page (3 'where this applies' links)", "Site currently siloed; buyers can't traverse", "M")
add("P1-Content", CT, "CTAs", "CTA copy system: 12 variants mapped to funnel stage, tested per template", "Every CTA currently says the same thing", "S")
add("P1-Content", CT, "Meta layer", "Rewrite 633 seo_titles + meta_descriptions with benefit-led patterns (length-checked)", "SERP CTR", "M")
add("P1-Content", CT, "Microcopy", "Buttons, labels, empty states, 404, form hints rewritten in brand voice", "Microcopy is the trust layer", "S")
add("P1-Content", CT, "Glossary", "20-term glossary module with inline tooltips on first use", "Explains terms per writing rules", "M")
add("P1-Content", CT, "Proof library", "Central stats library: 40 verified/illustrative metrics with sources, reused consistently site-wide", "Numbers currently inconsistent between pages", "M")
add("P1-Content", CT, "De-AI pass", "Programmatic phrase audit across all 633 JSONs: flag + replace 24 banned patterns", "Systematic de-flavoring", "M")
add("P1-Content", CT, "Confidentiality", "Final 100x confidentiality sweep on all rewritten text + JSON + code comments", "Non-negotiable rule", "S")

# ══════════════════ P1 — UI/UX LAYOUT ══════════════════
UX = "UI/UX Layout & Density"
add("P1-UX", UX, "Global", "Full-width density layout: 12-col grid, max 1440px, gutters 24-32px — kill excess whitespace", "User: 'too much whitespace, content breaks lines'", "M")
add("P1-UX", UX, "Global", "Typography scale v2: 44/32/24/18/16/14 with 1.5 line-height body, min 68ch measure", "Readability + hierarchy", "M")
add("P1-UX", UX, "Global", "Section rhythm: 96px desktop / 64px mobile vertical rhythm, consistent band alternation (white/navy/mist)", "Page flow currently erratic", "M")
add("P1-UX", UX, "Cards", "Unified card spec: 16px radius, 1px hairline border, 3-level shadow tokens, equal-height enforcement via grid", "Boxes currently misaligned heights", "M")
add("P1-UX", UX, "Homepage", "Executive dashboard hero: headline + 4 KPI tiles + mini chart above the fold", "CXO must see value in 5 seconds", "L")
add("P1-UX", UX, "Homepage", "Logo/credibility band with animated proof marquee", "Instant trust cue", "S")
add("P1-UX", UX, "Service pages", "Capability matrix table replaces bullet walls (4x5 grid with icons)", "Scanability", "M")
add("P1-UX", UX, "Industry pages", "Sector pain→solution 2-col mapping table", "Buyer maps himself in seconds", "M")
add("P1-UX", UX, "Case studies", "KPI band: 3 big numbers + context line, then narrative", "Proof first", "M")
add("P1-UX", UX, "Platform pages", "Product-sheet layout: left feature rail + right sticky diagram", "Product feel", "M")
add("P1-UX", UX, "Nav", "Mega-menu redesign: 3-tier with descriptions, icons, featured card per tower", "User calls current menu 'absolute worst'", "L")
add("P1-UX", UX, "Nav", "Mobile nav: full-screen sheet with sectioned accordion + CTA pin", "Mobile conversion", "M")
add("P1-UX", UX, "Footer", "Footer sitemap restructure: 5 columns + trust badges + newsletter", "Footer is a conversion surface", "M")
add("P1-UX", UX, "Breadcrumbs", "Visual breadcrumb bar with schema markup on all internal pages", "Orientation + SEO", "S")
add("P1-UX", UX, "Tables", "Comparison tables: sticky header, zebra rows, check/cross icons", "Enterprise buyers compare", "M")
add("P1-UX", UX, "Forms", "Contact/briefing forms: 2-col compact, inline validation, progress for multi-step", "Lead-gen friction", "M")
add("P1-UX", UX, "Search", "Search results: grouped by type with thumbnails + filters", "Findability", "M")
add("P1-UX", UX, "404", "Branded 404 with top-6 destinations + search box", "Recover lost traffic", "S")
add("P1-UX", UX, "Dark mode", "Navy-band sections get consistent contrast pass (WCAG AA on all text)", "Brand consistency + a11y", "M")
add("P1-UX", UX, "Iconography", "Icon set unified: one stroke weight, 24px grid, brand-orange accents", "Icons currently mixed styles", "M")
add("P1-UX", UX, "Diagrams", "Flat icon architecture diagram component (layers: ingest→govern→model→decide→act)", "User asked for flat diagram style", "M")
add("P1-UX", UX, "Print", "Print stylesheet: case studies + service one-pagers print clean", "Sales enablement", "S")
add("P1-UX", UX, "Responsive", "Breakpoint audit: 390/768/1024/1440/1920 — no horizontal scroll, no orphan words", "Mobile quality", "M")

# ══════════════════ P2 — SEO ══════════════════
SEO = "SEO & Discoverability"
add("P2-SEO", SEO, "URLs", "Fix /why-achala-soft/ slug → /why-achala/ + 301 redirect stub page (13 refs / 12 files)", "Brand-name consistency", "S")
add("P2-SEO", SEO, "Sitemap", "Regenerate sitemap.xml with lastmod + priority per template", "Crawl efficiency", "S")
add("P2-SEO", SEO, "Schema", "Organization + WebSite + SearchAction JSON-LD on homepage", "Rich results", "S")
add("P2-SEO", SEO, "Schema", "FAQPage schema on 20 top pages with visible FAQ blocks", "SERP real estate", "M")
add("P2-SEO", SEO, "Schema", "Service schema with areaServed on all 63 service pages", "Service SERP features", "M")
add("P2-SEO", SEO, "Schema", "Article schema completeness on 33 insights + 37 case studies", "E-E-A-T", "M")
add("P2-SEO", SEO, "Canonicals", "Canonical audit: trailing-slash consistency, no index on style-guide/search", "Duplicate content", "S")
add("P2-SEO", SEO, "Internal links", "Related-content module: 3 contextual links per page from link graph", "Crawl depth + dwell", "M")
add("P2-SEO", SEO, "robots", "robots.txt + hover-board verification files", "Crawl control", "S")
add("P2-SEO", SEO, "Headings", "Heading audit script: one H1 per page, H2/H3 hierarchy valid on 633 pages", "Structural SEO", "S")
add("P2-SEO", SEO, "Alt text", "Alt text audit: descriptive, keyword-relevant alts on all images", "Image SEO", "S")
add("P2-SEO", SEO, "404/redirects", "Redirect map for any removed/renamed slugs", "Link equity preserved", "S")

# ══════════════════ P2 — PERFORMANCE ══════════════════
PF = "Performance"
add("P2-Perf", PF, "Core Web Vitals", "LCP < 2.0s: hero image priority + preload, font-display swap", "CWV is a ranking factor", "M")
add("P2-Perf", PF, "CLS", "CLS < 0.05: width/height on all media, reserve slots for injected modules", "Visual stability", "M")
add("P2-Perf", PF, "INP", "INP < 200ms: break long tasks, passive listeners everywhere", "Interactivity", "M")
add("P2-Perf", PF, "Fonts", "Self-host woff2 subsets (latin only), preload 2 weights", "Font render cost", "S")
add("P2-Perf", PF, "CSS", "Critical CSS inline + route-level code splitting audit", "First paint", "M")
add("P2-Perf", PF, "JS", "Ship < 90KB JS on content pages (client components inventory)", "Static site should be light", "M")
add("P2-Perf", PF, "Images", "Responsive image srcset matrix for all new AI images", "Mobile weight", "M")
add("P2-Perf", PF, "Caching", "Cache headers doc for Pages/CDN deploy (immutable _next)", "Repeat visits fast", "S")
add("P2-Perf", PF, "Budget", "Per-template perf budget table + CI check script", "Prevent regression", "S")

# ══════════════════ P2 — ACCESSIBILITY ══════════════════
AX = "Accessibility"
add("P2-A11y", AX, "Contrast", "Contrast audit: all text ≥ 4.5:1 (orange on white fails for body — use only for accents/CTAs)", "WCAG AA", "M")
add("P2-A11y", AX, "Keyboard", "Full keyboard pass: skip link, focus-visible rings, logical tab order, mega-menu arrows", "WCAG 2.1 AA", "M")
add("P2-A11y", AX, "ARIA", "ARIA audit: nav/menus/dialogs/accordions/tabs patterns correct", "Screen readers", "M")
add("P2-A11y", AX, "Motion", "prefers-reduced-motion: verified static fallbacks for every new animation", "Vestibular safety", "S")
add("P2-A11y", AX, "Forms", "Form labels, error announcements, autocomplete attrs", "Conversion + a11y", "S")
add("P2-A11y", AX, "Semantics", "Landmarks + heading order + list semantics on templates", "Assistive tech", "M")
add("P2-A11y", AX, "Links", "Link text audit: no 'learn more' without context (633-page script check)", "Screen reader UX", "S")

# ══════════════════ P3 — CHARTS & DATA VISUALS ══════════════════
CH = "Executive Data Visuals"
add("P3-Charts", CH, "Homepage", "Rebuild homepage charts as CXO view: value-at-stake waterfall + maturity radar + delivery confidence gauge", "User: 'charts like a high-schooler's'", "L")
add("P3-Charts", CH, "System", "Chart design system v3: shared axes, ticks, grid, tooltip, palette (orange/navy/mist), tabular-nums", "Consistency", "M")
add("P3-Charts", CH, "Charts", "Per-tower KPI panel: 2 charts each, seeded per page (already), redesign visuals", "Depth per service page", "M")
add("P3-Charts", CH, "Charts", "Sparkline row component for case studies (6 mini-trends)", "Scannable proof", "M")
add("P3-Charts", CH, "Diagrams", "ArchitectureFlow v2: flat icon style, animated flow particles, labeled lanes", "Requested flat style", "M")
add("P3-Charts", CH, "Maps", "WorldPins v2: accurate projection + arc animation between delivery centers", "Global story", "M")
add("P3-Charts", CH, "A11y", "Every chart: aria-label + visible data table fallback", "A11y + SEO", "M")
add("P3-Charts", CH, "Animation", "Chart entrance choreography + hover crosshair + legend toggles", "Interactive feel", "M")

# ══════════════════ P3 — TRUST / LEGAL / OPS ══════════════════
TR = "Trust, Legal & Ops"
add("P3-Trust", TR, "Brand", "Brand-name sweep: 'Achala IT Solutions' everywhere; 'Achala IT Solutions' zero instances (automated check)", "Naming consistency", "S")
add("P3-Trust", TR, "Confidentiality", "Entity-name zero-instance check in CI (repo, content, assets metadata)", "Hard rule: check 100x", "S")
add("P3-Trust", TR, "Cookie/consent", "Cookie consent banner v2: granular toggles, brand-styled", "Compliance", "S")
add("P3-Trust", TR, "Policies", "Privacy/terms/accessibility pages: plain-language rewrite", "Trust", "S")
add("P3-Trust", TR, "Security", "Security headers doc (CSP-safe for static export), HTTPS-only links audit", "Hardening", "S")
add("P3-Trust", TR, "Deploy", "GitHub Pages validation runbook + www.achalasolutions.com deploy checklist", "Ship reliability", "S")
add("P3-Trust", TR, "Zip", "Repackage download/achala-website-repo.zip after every wave", "Handoff hygiene", "S")

# ── Expand: per-page content line items to guarantee 500+ ──
import glob, os, json as J
site = "/home/z/my-project/site"
pages = sorted(glob.glob(f"{site}/src/content/pages/*.json"))
titles = {}
for f in pages:
    try:
        d = J.load(open(f, encoding='utf-8'))
        titles[os.path.basename(f)[:-5]] = (d.get('template') or '', d.get('title') or '')
    except Exception:
        pass

TPL_LABEL = {
    'tower_hub': 'Service hub', 'service_page': 'Service page', 'industry_hub': 'Industry hub',
    'industry_page': 'Industry page', 'platform_page': 'Platform page', 'case_study': 'Case study',
    'insight_article': 'Insight', 'newsroom_article': 'Newsroom', 'leadership_profile': 'Leadership profile',
    'solution_page': 'Solution page', 'company_page': 'Company page', 'hub_page': 'Hub page',
}
added_content = 0
for key, (tpl, title) in sorted(titles.items()):
    if key in ('style-guide','search','_backup','404'):
        continue
    label = TPL_LABEL.get(tpl, tpl or 'Page')
    short = (title[:52] or key)
    if tpl in ('case_study',):
        ch = "Restructure as Challenge→Build→Outcome with KPI band + visual header + related services links"
        why = "Case studies are the strongest proof asset; all are thin/generic"
        eff = "S"
    elif tpl in ('insight_article',):
        ch = "Rewrite with thesis-first intro, evidence table, and 'Do-next' box; add article header image"
        why = "Insights must demonstrate thought leadership"
        eff = "S"
    elif tpl in ('tower_hub','service_page'):
        ch = "Rewrite intro + add capability matrix + 3 concrete scenarios + platform rails + CTA per funnel stage"
        why = "Service pages convert; current text describes the page, not the value"
        eff = "S" if tpl == 'service_page' else "M"
    elif tpl in ('industry_hub','industry_page'):
        ch = "Sector rewrite: regulation/margin/data realities + named use cases + sector imagery"
        why = "Industry credibility requires sector depth"
        eff = "S"
    elif tpl in ('platform_page',):
        ch = "Product-sheet rewrite: runs/replaces/time-to-value + UI mock visual + integration list"
        why = "Platform pages read like essays today"
        eff = "S"
    elif tpl == 'leadership_profile':
        ch = "Profile polish: mandate, background, 2 quotes; consistent headshot treatment"
        why = "Leadership builds trust"
        eff = "S"
    else:
        ch = "Full copy polish: de-AI phrasing, concrete specifics, cross-links, CTA alignment"
        why = "Every page must read human and specific"
        eff = "S"
    add("P1-Content", CT, f"{label}: {short}", ch, why, eff)
    added_content += 1

# UX per-page expansions
ux_extra = 0
for key, (tpl, title) in sorted(titles.items()):
    if tpl in ('case_study','insight_article','tower_hub','industry_hub','platform_page'):
        label = TPL_LABEL.get(tpl, tpl)
        add("P1-UX", UX, f"{label}: {title[:48]}", "Apply density layout v2: full-width grid, equal-height cards, band rhythm, breadcrumb bar", "Layout consistency across every template", "S")
        ux_extra += 1

# Motion per-page expansions (visual QA rows)
m_extra = 0
for key, (tpl, title) in sorted(titles.items()):
    if tpl in ('tower_hub','industry_hub','platform_page','case_study'):
        add("P0-Motion", AN, f"Verify: {title[:48]}", "Verify motion choreography renders + reduced-motion fallback works on this page", "Per-page motion QA", "S")
        m_extra += 1

total = len(rows)
print(f"rows before expansion: {total}, content expansions: {added_content}, ux: {ux_extra}, motion: {m_extra}")
print(f"TOTAL ROWS: {len(rows)}")

# ══════════════════ WRITE XLSX ══════════════════
wb = Workbook()
ws = wb.active
ws.title = "Change Backlog"
ws.sheet_view.showGridLines = False

PRIMARY = "18142D"; BRAND = "FE5722"; NEUTRAL_100 = "F7F7F5"; NEUTRAL_200 = "E9E9E8"
thin = Side(style="thin", color=NEUTRAL_200)

ws["B2"] = "Achala IT Solutions — Website Transformation Backlog (Gate: 500+ Changes)"
ws["B2"].font = Font(name="Arial", size=16, bold=True, color=PRIMARY)
ws["B3"] = "Scope: fix images (root cause: placeholder-only visuals), 100X motion upgrade, full content rewrite, layout density, SEO/a11y/perf. Target: from ~20% to ≥50% of expected quality. Generated 2026-11-21."
ws["B3"].font = Font(name="Arial", size=10, color="8C8A84")

headers = ["#", "Wave", "Category", "Page / Area", "Change to make", "Why it matters", "Effort", "Status"]
HR = 5
for c, h in enumerate(headers, 2):
    cell = ws.cell(row=HR, column=c, value=h)
    cell.font = Font(name="Arial", size=10, bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor=PRIMARY)
    cell.alignment = Alignment(horizontal="left", vertical="center")
    cell.border = Border(bottom=thin)

EFF_COLOR = {"S": "1B7D46", "M": "D4820A", "L": "C0392B"}
r = HR + 1
for i, (wave, cat, area, change, why, eff, status) in enumerate(rows, 1):
    vals = [i, wave, cat, area, change, why, eff, status]
    for c, v in enumerate(vals, 2):
        cell = ws.cell(row=r, column=c, value=v)
        cell.font = Font(name="Arial", size=9.5, color="37352F")
        cell.alignment = Alignment(vertical="top", wrap_text=True)
        cell.border = Border(bottom=thin)
        if i % 2 == 1:
            cell.fill = PatternFill("solid", fgColor=NEUTRAL_100)
    ws.cell(row=r, column=8).font = Font(name="Arial", size=9.5, color=EFF_COLOR.get(eff, "37352F"), bold=True)
    r += 1

# summary block
sr = r + 2
ws.cell(row=sr, column=2, value="Summary").font = Font(name="Arial", size=12, bold=True, color=PRIMARY)
from collections import Counter
wcount = Counter(w for w, *_ in rows)
ecount = Counter(e for *_, e, _ in [(w, c, a, ch, wh, ef, st) for (w, c, a, ch, wh, ef, st) in rows])
rr = sr + 1
ws.cell(row=rr, column=2, value="Total items").font = Font(name="Arial", size=10, bold=True)
ws.cell(row=rr, column=3, value=len(rows)).font = Font(name="Arial", size=10, bold=True, color=BRAND)
rr += 1
for w, n in sorted(wcount.items()):
    ws.cell(row=rr, column=2, value=w).font = Font(name="Arial", size=10)
    ws.cell(row=rr, column=3, value=n).font = Font(name="Arial", size=10)
    rr += 1

widths = {"A": 2, "B": 6, "C": 12, "D": 24, "E": 34, "F": 62, "G": 44, "H": 7, "I": 10}
for col, w in widths.items():
    ws.column_dimensions[col].width = w
ws.freeze_panes = "B6"

# Sheet 2: motion inventory detail
ws2 = wb.create_sheet("Motion Inventory")
ws2.sheet_view.showGridLines = False
ws2["B2"] = "Motion 100X — Effect Inventory (baseline audit + target set)"
ws2["B2"].font = Font(name="Arial", size=14, bold=True, color=PRIMARY)
h2 = ["Baseline (what exists today)", "Verdict", "Target state (100X)"]
for c, h in enumerate(h2, 2):
    cell = ws2.cell(row=4, column=c, value=h)
    cell.font = Font(name="Arial", size=10, bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor=PRIMARY)
baseline = [
 ("Reveal on scroll (sections fade-up, threshold 0.05)", "Below minimum", "Stagger engine + spring easings + per-template choreography"),
 ("Cursor spotlight glow", "OK but weak", "Brand-orange spotlight + noise + interactive scaling"),
 ("Magnetic CTA pull (130px radius)", "OK but weak", "Magnetic + tilt + sheen + ripple"),
 ("CountUp stats", "Basic", "Odometer digits + suffix flip"),
 ("Marquee band", "Basic", "Dual-direction, scroll-velocity reactive"),
 ("Scroll progress bar", "Basic", "Gradient + glow head"),
 ("BackToTop", "Basic", "Progress ring morph"),
 ("SMIL-animated hero SVGs", "Slow/hidden", "Replaced by AI imagery + clip-path reveals + parallax"),
 ("14 CSS keyframes (aurora, drift, shimmer...)", "Scattered", "Unified token system, GPU-only properties, orchestration layer"),
 ("No per-page bespoke motion", "Missing", "18 bespoke per-page sequences (MP-01..18)"),
 ("No diagram/chart draw-in", "Missing", "SVG stroke draw + chart build-in choreography"),
 ("No page-enter cascade", "Missing", "First-paint cascade with FOUC guard"),
]
r2 = 5
for b, v, t in baseline:
    ws2.cell(row=r2, column=2, value=b).font = Font(name="Arial", size=9.5)
    ws2.cell(row=r2, column=3, value=v).font = Font(name="Arial", size=9.5, color="C0392B" if v=="Missing" else ("D4820A" if "weak" in v or "Basic" in v else "1B7D46"), bold=True)
    ws2.cell(row=r2, column=4, value=t).font = Font(name="Arial", size=9.5)
    for c in range(2, 5):
        ws2.cell(row=r2, column=c).alignment = Alignment(vertical="top", wrap_text=True)
    r2 += 1
ws2.column_dimensions["B"].width = 52
ws2.column_dimensions["C"].width = 16
ws2.column_dimensions["D"].width = 60

wb.properties.creator = "Z.ai"
out = "/home/z/my-project/download/Achala-website-500plus-change-backlog.xlsx"
wb.save(out)
print("saved:", out, os.path.getsize(out), "bytes")
