# Additional backlog rows to complete coverage: P1/P3/P5/P7/P8 extensions.
# Row shape: (phase, workstream, change_item, where, acceptance_dod, impact, effort, status)

P1E = [
    ("P1", "Output band", "Add 'How to read this pack' microcopy row under the 4 panels (what each panel answers for a CXO)", "output band", "One-line reader guide per panel", "Med", "S", ""),
    ("P1", "Output band", "Add panel hover states: 'Open the method behind this chart' link on each card", "output band", "Links to method/approach pages", "Med", "S", ""),
    ("P1", "Towers section", "Tower cards: add 'first 90 days' chip (Diagnose->Prove->Industrialize) - makes cards informative, not labels", "towers grid", "Chip on all 8 cards", "Med", "S", ""),
    ("P1", "Industries section", "Industry cards: add regulation chip (top regulator/standard) + data-density dot scale", "industries section", "12 cards carry chips", "Med", "S", ""),
    ("P1", "Platforms section", "PlatformTabs: add status chip (production/pilot) + integration count per platform", "PlatformTabs", "8 tabs carry chips", "Low", "S", ""),
    ("P1", "Evidence band", "Evidence slides: add artifact chips (steering pack, gate report, control matrix)", "SpotlightSlider", "3 chips per slide", "Med", "S", ""),
    ("P1", "Charter section", "Charter pillars: each links to approach page anchor describing the mechanism", "PILLARS", "Links resolve to anchors", "Low", "S", ""),
    ("P1", "SEO page", "Homepage meta rewrite to match new positioning ('Achala IT Solutions | ...') with 155-char description carrying towers", "home.json", "Unique meta; title pattern approved", "Med", "S", ""),
]

P3E = [
    ("P3", "Mega menu", "Mega panel width: 4 columns aligned to container, not viewport-wide; edge alignment with trigger", "MegaPanel", "Panel aligns under header container at 1366/1920", "Med", "S", ""),
    ("P3", "Mega menu", "Mega panel scroll lock: page behind does not scroll on wheel inside panel; panel max-height with internal scroll", "globals.css", "No page scroll while hovering panel", "Med", "S", ""),
    ("P3", "Header", "Logo click behavior: root with full wordmark + dot mark; header height tokens for logo clearspace rule", "SiteHeader", "Clearspace respected at 60/72px heights", "Low", "S", ""),
    ("P3", "Header", "Right cluster: search + contact CTA + briefing CTA priority order; collapse contact on <1440", "SiteHeader", "No overflow at 1280 with CTAs present", "Med", "S", ""),
    ("P3", "Header", "Locale-ready header structure (single-locale now): hreflang placeholders documented", "SiteHeader", "Structure documented", "Low", "S", ""),
    ("P3", "In-page nav", "Related rail: add thumbnails/mini-visual per link (chart chip or icon) - visual link rail", "PagePieces", "Rail renders media for 10 sampled pages", "Med", "M", ""),
    ("P3", "In-page nav", "In-page 'on this page' for hub pages only (not detail pages) to avoid clutter", "renderer", "Hubs show TOC; details do not", "Low", "S", ""),
    ("P3", "Footer", "Footer brand block: logo + one-line positioning + certifications; separated from link columns", "Footer", "Block approved", "Low", "S", ""),
]

P5E = [
    ("P5", "Icon system", "Icon animation spec: 240ms fill/stroke transitions on hover for card icons only", "Icon component", "Spec applied to card grids", "Low", "S", ""),
    ("P5", "Diagrams", "Diagram legend: color/shape key under every diagram (consistency with charts)", "DiagramFrame", "Legend slot mandatory in linter", "Med", "S", ""),
    ("P5", "Diagrams", "Diagram tokens: band colors from navy ramp + brand accents; connector styles; node chip styles", "tokens", "No ad-hoc colors in diagrams", "Med", "S", ""),
    ("P5", "Diagrams", "Mini-diagrams for cards: 120px simplified motifs for solution cards", "Diagrams.tsx", "12 solution cards carry mini-motifs", "Med", "M", ""),
    ("P5", "Imagery", "Social share cards for insights (1200x630 auto-generated per article)", "build script", "24 article OG images generated", "Med", "M", ""),
    ("P5", "Imagery", "Favicon/context: motif-only favicon variants per section (Q-dot base)", "public", "Suite rendered", "Low", "S", ""),
]

P7E = [
    ("P7", "Grid", "Split view component: text 7fr + visual 5fr rows for capability pages (fixes narrow-line complaint)", "renderer block", "Used on 30+ pages", "High", "M", ""),
    ("P7", "Grid", "Definition-list grid: 2-3 column dl for spec/requirement content", "renderer", "Used on platform/service pages", "Low", "S", ""),
    ("P7", "Grid", "Number-band component: 4-6 inline stats with dividers, full width, used after intros", "PagePieces", "Adopted on 10+ pages", "Med", "S", ""),
    ("P7", "Typography", "Print stylesheet: clean article print (no nav, charts ink-safe)", "print css", "Print preview clean on 3 goldens", "Low", "S", ""),
    ("P7", "Typography", "Dark-surface reading floor: body on navy >= rgba(255,255,255,.75); secondary >= .62 with AA check", "globals.css", "Contrast green", "Med", "S", ""),
    ("P7", "Spacing", "Card internal density variants: comfortable (24px) / compact (16px) for chip grids", "ui-bits", "Both used appropriately", "Low", "S", ""),
    ("P7", "Density QA", "Wide-screen pass at 1920: no section looks 'lost' (centered narrow) - full-width or companion columns everywhere", "goldens", "1920 goldens reviewed", "High", "M", ""),
    ("P7", "Density QA", "Ultrawide (2560) guardrail: content caps at 1440 centered with bg field continuation", "globals.css", "2560 screenshot reviewed", "Low", "S", ""),
]

P8E = [
    ("P8", "A11y", "Focus management on route change: focus moves to h1/main (announced politely)", "router", "Screen-reader announces page title", "Med", "M", ""),
    ("P8", "A11y", "Dialog patterns (search overlay, drawer): role=dialog, aria-modal, focus restore", "components", "Matrix pass", "Med", "S", ""),
    ("P8", "A11y", "Live regions for dynamic content (search results count, form status)", "components", "Announcements verified", "Med", "S", ""),
    ("P8", "A11y", "Reduced-transparency preference honored (backdrop-blur removal)", "globals.css", "Emulation pass", "Low", "S", ""),
    ("P8", "A11y", "Text spacing tolerance: layout survives 150% text size without breakage", "goldens", "150% zoom screenshots reviewed", "Med", "S", ""),
    ("P8", "A11y", "Error pages accessible + useful (404 with search)", "404", "Axe green", "Med", "S", ""),
    ("P8", "SEO tech", "Pagination handling for insights/case lists (rel prev/next semantics via content design - no infinite scroll)", "lists", "Lists paginate or cap gracefully", "Low", "S", ""),
    ("P8", "SEO tech", "HTML validation: 0 critical validation errors across 639 pages", "validator", "Validator green", "Med", "M", ""),
    ("P8", "SEO tech", "Spec inspection of key landing pages (manual crawler view) - key content server-rendered", "renderer", "Content present without JS", "High", "S", ""),
    ("P8", "Perf", "Server-side render check for all template families (no client-only content)", "renderer", "noscript snapshot readable", "High", "S", ""),
    ("P8", "Perf", "Resource hints: preconnect for fonts/analytics only; no unused hints", "layout", "Hints audit green", "Low", "S", ""),
    ("P8", "Perf", "Memory leak audit: listeners/observers disconnected on unmount (devtools heap snapshot)", "components", "Snapshot stable over 20 navigations", "Med", "M", ""),
]

P4E = [
    ("P4", "Engine rules", "Rewrite QA protocol: each cluster batch gets a second-pass edit (fresh eyes) before marked Done", "process", "Second-pass log per batch", "Med", "S", ""),
    ("P4", "Engine rules", "Fact registry: every number on the site traceable to brand.json stats or assumption registry - no invented clients/figures", "docs", "Registry + audit green", "High", "M", ""),
    ("P4", "Engine rules", "Readability floor: Flesch 40-60 target on content pages; engine reports outliers", "audit", "Report + fixes on worst 20", "Low", "S", ""),
    ("P4", "Cluster rewrites", "Rewrite home.json body blocks (used by non-JS crawlers + PagePieces): align with new homepage sections", "home.json", "JSON body matches HomeView story", "Med", "S", ""),
    ("P4", "Cluster rewrites", "Rewrite style-guide page as internal-only doc with new tokens (rename to /system/ and noindex)", "style-guide", "Noindex + renamed", "Low", "S", ""),
    ("P4", "Cluster rewrites", "Approach page gets 'steering pack sample' section reusing homepage Pack component", "approach + HomeView", "Pack renders on approach", "Med", "S", ""),
    ("P4", "SEO copy", "Image alt texts for all new diagrams/art follow functional-description policy", "content", "Alt audit green", "Med", "S", ""),
    ("P4", "SEO copy", "Unique intro sentences: page intros must not reuse the hub intro sentence patterns (checker n-gram)", "audit", "0 duplicate intro n-grams", "Med", "M", ""),
]
