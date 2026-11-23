# Backlog data: P4 Content overhaul + P5 Imagery/Icons/Diagrams.
# Row shape: (phase, workstream, change_item, where, acceptance_dod, impact, effort, status)

TOWERS = ["Applied AI & Generative AI", "Agentic AI & Hyperautomation", "Data, Analytics & Lakehouse",
          "Cybersecurity & Zero-Trust", "Cloud, Edge & Platform Engineering", "Quantum & Advanced Compute",
          "Blockchain & Digital Trust", "IoT, Digital Twin & Robotics"]
INDUSTRIES = ["Banking & Financial Services", "Insurance & Risk", "Healthcare & Life Sciences",
              "Manufacturing & Industrial", "Retail & Consumer Goods", "Telecom, Media & Entertainment",
              "Energy & Utilities", "Logistics & Supply Chain", "Public Sector & Government",
              "Education & Research", "Technology & SaaS", "Agriculture & Food Systems"]
PLATFORMS = ["Achala Nexus", "Achala Forge", "Achala Swarm", "Achala Sentinel",
             "Achala Twinverse", "Achala Quanta", "Achala Ledger", "Achala Compass"]

def eng(kind, label, count, dod):
    return ("P4", "Cluster rewrites", f"Rewrite {kind} '{label}' ({count} pages): new hero (no formula), 600+ word body, concrete numbers, 3+ inline cross-links, mapped visuals", label, dod, "High", "M", "")

P4 = [
    ("P4", "Engine rules", "Ban-list expansion to 40+ tells: 'not by slide', 'regulatory teeth', 'fail quietly', 'governed autonomy', 'decision velocity', 'X, not Y' constructions, 'Intelligence, Engineered', epigram bullets '[Label] - punchline'", "content engine + audit script", "audit v2 reports tell counts per cluster; target 0 at 50% gate", "High", "S", ""),
    ("P4", "Engine rules", "Hero formula killer: 462 pages share one broken hero pattern - replace with per-page value line + 'who it is for' + proof chip", "renderer hero blocks", "0 pages share identical hero first sentence", "High", "L", ""),
    ("P4", "Engine rules", "Epigram-bullet killer: 541 pages use identical '[Label] - punchline' bullets; replace with 2-3 sentence explanatory items with examples", "content blocks", "audit v2 epigram count = 0", "High", "L", ""),
    ("P4", "Engine rules", "Sentence texture rule: mix lengths (max 28 words), one concrete noun+number per paragraph, zero nested em-dash chains", "engine", "Readability spot-check on 30 pages passes", "Med", "M", ""),
    ("P4", "Engine rules", "'So-what' test: every section ends with a business implication line (cost, risk, speed, compliance)", "engine + editor pass", "30-page sample: every H2 section has implication line", "High", "M", ""),
    ("P4", "Engine rules", "Concrete-number density: each page >=5 grounded figures (windows, volumes, roles, SLA shapes) from the honest assumption registry", "engine", "Number density report >=5/page", "Med", "M", ""),
    ("P4", "Engine rules", "Terminology table: canonical terms (Achala IT Solutions, towers, platforms, methods) with approved synonyms; engine enforces", "engine config", "0 off-brand variants in build", "Med", "S", ""),
    ("P4", "Engine rules", "US English + headline case rules applied engine-wide", "engine", "Spellcheck pass; heading case consistent", "Low", "S", ""),
    ("P4", "Engine rules", "Tone guide: deep-tech consultancy voice - declarative, evidence-first, zero hype adjectives; 3 exemplar paragraphs per template in the guide", "docs/tone_guide", "Guide signed; used by rewrite batches", "High", "S", ""),
    ("P4", "Engine rules", "Per-template paragraph minimums: body >=600 words (content pages), >=350 (legal), hubs >=800", "engine", "Word-count report per template passes", "High", "M", ""),
    ("P4", "Engine rules", "First-person plural 'we' voice with named roles ('delivery lead', 'model risk reviewer') - no 'our team of experts' fluff", "engine", "Sample pass on 20 pages", "Med", "S", ""),
    ("P4", "Engine rules", "Kill 'Achala IT Solutions was founded on a simple observation...' style origin-story filler on hubs; lead with the offer", "index/about content", "About + hubs rewritten leads", "Med", "S", ""),
    ("P4", "Engine rules", "Quote-attribution cleanup: no invented executive quotes; use role-based anonymized types consistently", "content", "0 fabricated named quotes", "Med", "S", ""),
    ("P4", "Engine rules", "Glossary: 40 terms with 2-line definitions; terms auto-linked on first use per page", "glossary content + linker", "Glossary page live; >=60% of pages link >=1 term", "Med", "M", ""),
] + [
    eng("tower hub", t, 1, "Hub lists its services with outcome tags; industry strip; 2 visuals; 800+ words") for t in TOWERS
] + [
    eng("tower detail batch", t, "~6 service pages", "6-7 pages per batch fully rewritten + linked into tower hub") for t in TOWERS
] + [
    eng("sub-capability batch", t, "30 pages", "0 epigram bullets; each page defines, scopes and links to sibling services") for t in TOWERS
] + [
    eng("industry hub", i, 1, "Hub: pressures, regulations, data estate, 3 priority capabilities with links, 1 industry visual") for i in INDUSTRIES
] + [
    eng("industry capability batch", i, "8 pages", "Capability-in-industry pages carry regulation callouts + cross-links to services") for i in INDUSTRIES
] + [
    eng("subindustry batch", INDUSTRIES[k], 8, "Sub-vertical pages state what differs vs parent + own proof points") for k in range(6)
] + [
    eng("solution batch", "Solutions set A (operations & automation)", 8, "Solution pages: problem->architecture->outcomes->next step; diagram each") ,
    eng("solution batch", "Solutions set B (data & intelligence)", 8, "Same pattern; diagrams + KPI tables"),
    eng("solution batch", "Solutions set C (trust & infrastructure)", 8, "Same pattern; compliance callouts"),
    ("P4", "Cluster rewrites", "Rewrite solutions hub: solution finder (3-question picker) + full solution index with outcome tags", "solutions hub", "Picker returns 3 solutions; index lists all 24", "High", "M", ""),
] + [
    eng("platform set", p, "3 pages (overview/architecture/usecases)", "Overview states KPIs; architecture page gets diagram; use cases carry industry links") for p in PLATFORMS
] + [
    eng("case-study batch", "Case studies 1-6", 6, "Fixed structure: context, baseline table, intervention, delta table, artifacts, quote"),
    eng("case-study batch", "Case studies 7-12", 6, "Same structure; each links to its industry + tower pages"),
    eng("case-study batch", "Case studies 13-18", 6, "Same; add 'what made it work' section"),
    eng("case-study batch", "Case studies 19-24", 6, "Same; add metrics chip row"),
    eng("case-study batch", "Case studies 25-30", 6, "Same; add timeline visual"),
    eng("case-study batch", "Case studies 31-36", 6, "Same; add method-family mapping (capability language only)"),
    eng("insight batch", "Insight articles 1-6", 6, "Thesis + evidence + 'what to do Monday' + 2 visuals"),
    eng("insight batch", "Insight articles 7-12", 6, "Same; add vendor-questions box"),
    eng("insight batch", "Insight articles 13-18", 6, "Same; add reading path links"),
    eng("insight batch", "Insight articles 19-24", 6, "Same; add glossary links"),
    ("P4", "Cluster rewrites", "Rewrite 8 insights category pages: theme intro + ordered reading path + 2 featured articles each", "insights_category template", "8 categories live with paths", "Med", "M", ""),
    ("P4", "Cluster rewrites", "Rewrite newsroom set (8 pages): press-format correctness, dated, factual, no marketing gloss", "newsroom_article", "8 pages pass format check", "Low", "M", ""),
    ("P4", "Cluster rewrites", "Rewrite partner pages (12): alliance value, joint offer, delivery proof, contact route", "partner_page", "12 pages consistent structure", "Med", "M", ""),
    ("P4", "Cluster rewrites", "Rewrite company pages (8): story, facts from brand.json, delivery centers, credentials - all claims sourced to brand.json", "company_page", "0 unsourced claims", "Med", "M", ""),
    ("P4", "Cluster rewrites", "Rewrite leadership profiles (8): mandate, background focus, accountability line - no invented bios", "leadership_profile", "8 profiles consistent; roles match org", "Med", "S", ""),
    ("P4", "Cluster rewrites", "Rewrite approach pages (4): operating model, gates, artifacts, sample steering pack visuals", "approach_page", "4 pages carry gate table + pack mock", "Med", "M", ""),
    ("P4", "Cluster rewrites", "Rewrite legal pages (6) in plain language with correct entity name", "legal_page", "Reviewed copy; no template filler", "Med", "S", ""),
    ("P4", "Cluster rewrites", "Rewrite contact/booking pages (3): what happens next timeline + expectations", "contact_page", "Booking flow documented on page", "Med", "S", ""),
] + [
    ("P4", "Cross-linking", "Inline link rule: >=3 contextual inline links per 500 words with varied anchors; linker scans and injects from URL map", "engine linker", "Link-density report passes on 633 pages", "High", "L", ""),
    ("P4", "Cross-linking", "Hub-and-spoke matrix: services(54) <-> industries(12) mapping; each service page links 3 relevant industry capability pages and vice versa", "mapping table + linker", "Matrix table shipped; spot-check 20 pages shows both directions", "High", "L", ""),
    ("P4", "Cross-linking", "Solutions <-> towers matrix: each solution links its 3-4 towers; each tower links back its solutions", "mapping table", "Bidirectional links verified", "High", "M", ""),
    ("P4", "Cross-linking", "Platforms <-> towers/services matrix: platform pages link the services that deploy them and back", "mapping table", "Verified on 8 platforms", "Med", "M", ""),
    ("P4", "Cross-linking", "Method-capability mapping (indirect): each of 8 method families links into 2-3 towers + industries it strengthens - capability language, no provenance", "patented-intelligence + linker", "8 families mapped; scan shows zero source mentions", "High", "M", ""),
    ("P4", "Cross-linking", "Case-study links: every case links industry hub + tower + method used; hubs feature 3 cases each", "content + hubs", "36 cases cross-linked; hubs show cases", "Med", "M", ""),
    ("P4", "Cross-linking", "Insight links: every article links 2 services + 1 case; categories cross-link", "content", "Verified on 24 articles", "Med", "M", ""),
    ("P4", "Cross-linking", "Next-step block: every content page ends with a relevant next step (related service, briefing, case) - not a generic CTA", "renderer", "Next-step rules per template shipped", "Med", "M", ""),
    ("P4", "Cross-linking", "Orphan elimination: 7 zero-related pages fixed + link-graph check green", "link checker", "0 pages with <2 inbound links", "High", "S", ""),
    ("P4", "Cross-linking", "Anchor-text variety audit: no repeated exact-match anchors across a page", "link checker", "Checker green", "Low", "S", ""),
    ("P4", "Cross-linking", "Breadcrumbs + related + next-step + inline = 4 redundant path systems documented so users never dead-end", "IA doc", "Diagram in IA doc", "Med", "S", ""),
] + [
    ("P4", "New blocks", "FAQ block per template with FAQPage schema (6-10 real questions per page family)", "renderer + content", "Schema validates; FAQs non-generic", "High", "L", ""),
    ("P4", "New blocks", "Comparison table block (approach vs typical SI / build vs buy)", "PagePieces", "Used on 10+ pages", "Med", "M", ""),
    ("P4", "New blocks", "'What you get' deliverables list block (artifacts, owners, cadence)", "renderer", "Used on service/solution pages", "Med", "M", ""),
    ("P4", "New blocks", "KPI table block (metric, baseline shape, target band, owner, cadence)", "PagePieces", "Used on 20+ pages", "Med", "M", ""),
    ("P4", "New blocks", "Engagement timeline block (phase, gate, exit criteria)", "PagePieces", "Used on approach + service hubs", "Med", "M", ""),
    ("P4", "New blocks", "Compliance callout block (regs list per industry, mapped controls)", "renderer", "Used on all 96 industry capability pages", "Med", "M", ""),
    ("P4", "New blocks", "Tech-stack chips block (platforms + integrations per service)", "renderer", "Used on service pages", "Low", "S", ""),
    ("P4", "New blocks", "Objection-handling block ('common pushbacks + our answers') on solution pages", "renderer", "Used on 24 solution pages", "Low", "M", ""),
    ("P4", "New blocks", "RFP/procurement checklist block (what to ask any vendor, incl. us)", "renderer", "Used on 10+ pages; differentiates consultancy voice", "Low", "S", ""),
    ("P4", "New blocks", "SLA/response table block for run services", "PagePieces", "Used on run/operate services", "Low", "S", ""),
    ("P4", "New blocks", "Numbered 'how delivery runs' block with gate icons", "renderer", "Used on towers + solutions", "Med", "S", ""),
    ("P4", "New blocks", "Quote block rules: role + industry type + engagement type chips (no named people)", "PagePieces Quote", "All quotes carry chips", "Low", "S", ""),
    ("P4", "New blocks", "Updated-date + reading-time meta on articles and long pages", "renderer", "Meta renders site-wide", "Low", "S", ""),
    ("P4", "New blocks", "Assumptions & sources footnote block on pages with figures", "renderer", "Pages with numbers carry it", "Med", "S", ""),
    ("P4", "SEO copy", "633 unique meta descriptions: pattern per template + page-specific hook; 140-155 chars", "content engine", "Meta checker: 633/633 unique, in range", "High", "L", ""),
    ("P4", "SEO copy", "633 unique seo_titles: template pattern '{Capability} - {Industry context} | Achala IT Solutions' variants", "content engine", "0 duplicates; <=60 chars target", "High", "L", ""),
    ("P4", "SEO copy", "H1 uniqueness + keyword-to-page map (no cannibalization across 240 sub-capability pages)", "map doc", "Map reviewed; 0 cannibalization pairs", "High", "M", ""),
    ("P4", "SEO copy", "OG titles/descriptions per template family + OG image route per template", "OG generator", "OG tags correct on 20 sampled pages", "Med", "M", ""),
    ("P4", "SEO copy", "Internal anchor audit: anchors descriptive (never 'click here'), match target page intent", "link checker", "Audit green", "Low", "S", ""),
    ("P4", "SEO copy", "Keyword map for 12 industry hubs (commercial intent terms) + hub intros rewritten to carry them naturally", "map + content", "Hubs read naturally, not stuffed", "Med", "M", ""),
    ("P4", "SEO copy", "FAQ schema coverage: >=200 pages with FAQPage JSON-LD", "renderer", "Validator counts >=200", "Med", "S", ""),
    ("P4", "SEO copy", "Article schema for 24 insights + 36 case studies; Organization + WebSite schema on all pages", "layout/schema", "Rich-results test passes on samples", "Med", "M", ""),
]

P5 = [
    ("P5", "Icon system", "Commission flat 2px-stroke icon set, 48 icons: 8 towers + 12 industries + 8 platforms + 8 method families + 12 UI glyphs", "src/assets/icons", "Icon grid page renders all 48; consistent stroke/geometry", "High", "L", ""),
    ("P5", "Icon system", "Icon component: single <Icon name> with size tokens (16/20/24/32), brand-color mapping, dark variants", "ui-bits Icon", "All lucide ad-hoc uses replaced by set", "Med", "M", ""),
    ("P5", "Icon system", "SVG sprite build (single request) + tree-shaken imports", "build", "Icon payload <30KB gzipped", "Med", "S", ""),
    ("P5", "Icon system", "Per-tower icon semantic review (AI = graph/brain motif, Cyber = shield-lattice...) so icons are meaningful, not random", "design review", "8 mappings signed", "Med", "S", ""),
    ("P5", "Icon system", "Industry icon set: recognizable vertical motifs (bank column, factory, pipeline, tractor...) tested at 16px", "icons", "12 icons legible at small size", "Med", "M", ""),
    ("P5", "Icon system", "Method-family icons: 8 capability glyphs for patent band chips", "icons", "Rendered on patented-intelligence + homepage", "Low", "S", ""),
    ("P5", "Icon system", "Icon usage rules doc: what may/may not be recolored, spacing, pairing with text", "docs", "Doc live", "Low", "S", ""),
    ("P5", "Diagrams", "DiagramFrame component: titled, footnoted, animated draw-in, print-safe - same chrome as ChartFrame", "DataVisuals/Diagrams.tsx", "Shares tokens with ChartFrame v2", "High", "M", ""),
    ("P5", "Diagrams", "Layered architecture diagram (5-layer stack with labeled bands) - reusable for platforms and solutions", "Diagrams.tsx", "Used on 8 platform architecture pages", "High", "L", ""),
    ("P5", "Diagrams", "Data-flow diagram (sources -> ingestion -> lakehouse -> decision apps) with animated particles", "Diagrams.tsx", "Used on data tower + solutions", "High", "L", ""),
    ("P5", "Diagrams", "Agent topology diagram (orchestrator, workers, guardrails, human gates)", "Diagrams.tsx", "Used on agentic tower + solution pages", "Med", "M", ""),
    ("P5", "Diagrams", "Zero-trust zone diagram (identity plane, workload plane, data plane, controls)", "Diagrams.tsx", "Used on cyber tower + industry BFSI", "Med", "M", ""),
    ("P5", "Diagrams", "Medallion lakehouse diagram (bronze/silver/gold with governance spine)", "Diagrams.tsx", "Used on data tower pages", "Med", "M", ""),
    ("P5", "Diagrams", "Integration bus diagram (ERP/CRM/core systems connectors)", "Diagrams.tsx", "Used on enterprise integration services", "Low", "M", ""),
    ("P5", "Diagrams", "Deployment topology diagram (cloud/edge/on-prem zones with failover)", "Diagrams.tsx", "Used on cloud tower + platform pages", "Med", "M", ""),
    ("P5", "Diagrams", "8 per-tower signature diagrams (one motif per tower, reused across its pages)", "Diagrams.tsx + content", "Every tower hub + detail pages embed its diagram", "High", "L", ""),
    ("P5", "Diagrams", "12 industry value-flow diagrams (regulatory inputs, decisions, outcomes for each vertical)", "Diagrams.tsx + content", "Industry hubs embed own flow", "Med", "L", ""),
    ("P5", "Diagrams", "Diagram placement rules per template: which page gets which diagram, at what section depth", "renderer mapping", "Mapping table + linter like charts", "Med", "S", ""),
    ("P5", "Diagrams", "Diagram a11y: role=img + text alternative listing layers/flows", "Diagrams.tsx", "Screen-reader walk passes", "Med", "S", ""),
    ("P5", "Diagrams", "Diagram animation: sequential band reveal + connector draw; reduced-motion static", "Diagrams.tsx", "60fps; instant fallback", "Med", "S", ""),
    ("P5", "Imagery", "Art direction: abstract brand-gradient panels (orange/navy mesh, dot matrices) as section backdrops - no stock photos of handshakes", "public art + CSS", "Art tokens defined; homepage adopts", "Med", "M", ""),
    ("P5", "Imagery", "Industry card art: subtle geometric motif per industry (12 variants) from the flat icon system enlarged", "art + CSS", "Industry cards get motifs", "Low", "M", ""),
    ("P5", "Imagery", "OG image generator per template family (1200x630, brand field + title + Q-dot mark)", "build script", "OG PNGs generated for 8 families", "Med", "M", ""),
    ("P5", "Imagery", "Hero art: engineered 'signal field' canvas (deterministic, seeded) replacing flat gradient blocks", "hero", "Hero art loads <40KB; seeded stable", "Med", "M", ""),
    ("P5", "Imagery", "Case-study cover art: metric-motif cards (baseline/delta glyphs) per industry", "art + CSS", "36 cases get covers", "Low", "M", ""),
    ("P5", "Imagery", "Insight article covers: thesis-glyph system (3 motif families x colors)", "art + CSS", "24 articles get covers", "Low", "M", ""),
    ("P5", "Imagery", "Image pipeline: WebP/AVIF, width srcset, lazy below fold, priority for hero", "next/image config", "Lighthouse image audit green", "High", "S", ""),
    ("P5", "Imagery", "Alt-text policy: functional descriptions; decorative images empty alt; diagrams get structured alt", "content rules", "Alt audit script green", "Med", "S", ""),
    ("P5", "Imagery", "Illustration set for approach/methods: 6 spot illustrations (gate, ledger, mesh, shield, twin, graph)", "art", "Used on approach pages", "Low", "M", ""),
    ("P5", "Imagery", "Print/PDF-safe art variants (no transparency-heavy art)", "CSS", "Print preview clean", "Low", "S", ""),
    ("P5", "Imagery", "Asset inventory doc: every visual asset, where used, owner, license status", "docs", "Inventory complete", "Low", "S", ""),
]
