// Achala IT Solutions — Corporate Website Build & Technology Proposal (.docx)
// Cover: Recipe R1 (Pure Paragraph Left) + DM-1 Deep Cyan palette (AI/tech proposals)
// Architecture: 3 sections — Cover (no footer) / Front matter (Roman) / Body (Arabic start=1)
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, PageNumber, NumberFormat, AlignmentType, HeadingLevel,
  WidthType, BorderStyle, ShadingType, TableLayoutType, SectionType,
  TableOfContents, PageBreak, LevelFormat,
} = require("docx");
const fs = require("fs");

// ---------------------------------------------------------------- palette
const COVER = { // DM-1 Deep Cyan
  bg: "162235", titleColor: "FFFFFF", subtitleColor: "B0B8C0",
  metaColor: "90989F", footerColor: "687078", accent: "37DCF2",
};
const T = { // body tokens (DM-1 darkened for white pages)
  primary: "162235", h2: "1B6B7A", body: "000000", secondary: "5B6B7D",
  headerBg: "1B6B7A", headerText: "FFFFFF", accentLine: "1B6B7A",
  innerLine: "D8E4EC", surface: "EDF3F5",
};
const NB = { style: BorderStyle.NONE, size: 0, color: "auto" };
const allNoBorders = { top: NB, bottom: NB, left: NB, right: NB, insideHorizontal: NB, insideVertical: NB };
const noBorders = { top: NB, bottom: NB, left: NB, right: NB };
const EN_FONT = { ascii: "Times New Roman", eastAsia: "SimSun" };
const HEAD_FONT = { ascii: "Times New Roman", eastAsia: "SimHei" };

// ---------------------------------------------------------------- cover helpers
function wrapWords(t, cpl) {
  const words = t.split(" ");
  const lines = []; let cur = "";
  for (const w of words) {
    const cand = cur ? cur + " " + w : w;
    if (cand.length <= cpl) cur = cand;
    else { if (cur) lines.push(cur); cur = w; }
  }
  if (cur) lines.push(cur);
  return lines;
}
// English-calibrated title layout (proportional serif ~ pt*11 twips per char)
function calcTitleLayoutEN(title, maxWidthTwips, preferredPt = 40, minPt = 24) {
  let pt = preferredPt, lines = null;
  while (pt >= minPt) {
    const cpl = Math.floor(maxWidthTwips / (pt * 11));
    lines = wrapWords(title, Math.max(cpl, 2));
    const last = lines[lines.length - 1] || "";
    if (lines.length <= 3 && last.length > 2) break;
    pt -= 2;
  }
  return { titlePt: pt, titleLines: lines };
}
function calcCoverSpacing(params) {
  const {
    titleLineCount = 1, titlePt = 36, hasSubtitle = false,
    hasEnglishLabel = false, metaLineCount = 0,
    fixedHeight = 800, pageHeight = 16838, marginTop = 0, marginBottom = 0,
  } = params;
  const SAFETY = 1200;
  const usableHeight = pageHeight - marginTop - marginBottom - SAFETY;
  const titleHeight = titleLineCount * (titlePt * 23 + 200);
  const subtitleHeight = hasSubtitle ? (12 * 23 + 600) + 400 : 0; // +400: subtitle wraps to 2 lines
  const englishLabelHeight = hasEnglishLabel ? (9 * 23 + 600) : 0;
  const metaHeight = metaLineCount * (10 * 23 + 100);
  const implicitParaHeight = 3 * 300;
  const contentHeight = titleHeight + subtitleHeight + englishLabelHeight + metaHeight + fixedHeight + implicitParaHeight;
  const remainingSpace = usableHeight - contentHeight;
  const safeRemaining = Math.max(remainingSpace, 400);
  const FOOTER_MIN = 800;
  const rawTop = Math.floor(safeRemaining * 0.45);
  const rawBottom = Math.floor(safeRemaining * 0.45);
  const bottomSpacing = Math.max(rawBottom, FOOTER_MIN);
  const topSpacing = Math.max(rawTop - Math.max(0, FOOTER_MIN - rawBottom), 400);
  const midSpacing = Math.max(safeRemaining - topSpacing - bottomSpacing, 0);
  return { topSpacing, midSpacing, bottomSpacing };
}

function buildCoverR1(config) {
  const P = config.palette;
  const padL = 1200, padR = 800;
  const availableWidth = 11906 - padL - padR - 300;
  const { titlePt, titleLines } = calcTitleLayoutEN(config.title, availableWidth, 40, 24);
  const titleSize = titlePt * 2;
  const spacing = calcCoverSpacing({
    titleLineCount: titleLines.length, titlePt,
    hasSubtitle: !!config.subtitle, hasEnglishLabel: !!config.englishLabel,
    metaLineCount: (config.metaLines || []).length, fixedHeight: 400,
  });
  const accentLeft = { style: BorderStyle.SINGLE, size: 8, color: P.accent, space: 12 };
  const children = [];
  children.push(new Paragraph({ spacing: { before: spacing.topSpacing } }));
  if (config.englishLabel) {
    children.push(new Paragraph({
      indent: { left: padL, right: padR }, spacing: { after: 500 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: P.accent, space: 8 } },
      children: [new TextRun({
        text: config.englishLabel.split("").join("  "), size: 18, color: P.accent,
        font: { ascii: "Arial", eastAsia: "SimHei" }, characterSpacing: 40,
      })],
    }));
  }
  for (let i = 0; i < titleLines.length; i++) {
    children.push(new Paragraph({
      indent: { left: padL },
      spacing: { after: i < titleLines.length - 1 ? 100 : 300, line: Math.ceil(titlePt * 23), lineRule: "atLeast" },
      children: [new TextRun({
        text: titleLines[i], size: titleSize, bold: true, color: P.titleColor,
        font: { ascii: "Arial", eastAsia: "SimHei" },
      })],
    }));
  }
  if (config.subtitle) {
    children.push(new Paragraph({
      indent: { left: padL, right: padR }, spacing: { after: 800 },
      children: [new TextRun({
        text: config.subtitle, size: 24, color: P.subtitleColor,
        font: { ascii: "Arial", eastAsia: "Microsoft YaHei" },
      })],
    }));
  }
  for (const line of (config.metaLines || [])) {
    children.push(new Paragraph({
      indent: { left: padL + 200, right: padR }, spacing: { after: 80 },
      border: { left: accentLeft },
      children: [new TextRun({
        text: line, size: 24, color: P.metaColor,
        font: { ascii: "Arial", eastAsia: "Microsoft YaHei" },
      })],
    }));
  }
  children.push(new Paragraph({ spacing: { before: spacing.bottomSpacing } }));
  children.push(new Paragraph({
    indent: { left: padL, right: padR },
    border: { top: { style: BorderStyle.SINGLE, size: 2, color: P.accent, space: 8 } },
    spacing: { before: 200 },
    children: [
      new TextRun({ text: config.footerLeft || "", size: 16, color: P.footerColor, font: { ascii: "Arial" } }),
      new TextRun({ text: "                                        ", size: 16, color: P.footerColor, font: { ascii: "Arial" } }),
      new TextRun({ text: config.footerRight || "", size: 16, color: P.footerColor, font: { ascii: "Arial" } }),
    ],
  }));
  return [new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    layout: TableLayoutType.FIXED,
    borders: allNoBorders,
    rows: [new TableRow({
      height: { value: 16838, rule: "exact" },
      children: [new TableCell({
        shading: { type: ShadingType.CLEAR, fill: P.bg }, borders: noBorders, children,
      })],
    })],
  })];
}

// ---------------------------------------------------------------- body builders
function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 160, line: 312 },
    children: [new TextRun({ text, bold: true, size: 32, color: T.primary, font: HEAD_FONT })],
  });
}
function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 240, after: 120, line: 312 },
    children: [new TextRun({ text, bold: true, size: 28, color: T.h2, font: HEAD_FONT })],
  });
}
function body(text, opts = {}) {
  const runs = [];
  // supports [["normal ", false], ["bold part", true]] or plain string
  if (Array.isArray(text)) {
    for (const [seg, bold] of text) runs.push(new TextRun({ text: seg, bold: !!bold, size: 24, color: T.body, font: EN_FONT }));
  } else {
    runs.push(new TextRun({ text, size: 24, color: T.body, font: EN_FONT }));
  }
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { after: 120, line: 312 },
    children: runs, ...opts,
  });
}
function numItem(reference, text) {
  return new Paragraph({
    numbering: { reference, level: 0 },
    alignment: AlignmentType.JUSTIFIED,
    spacing: { after: 80, line: 312 },
    children: [new TextRun({ text, size: 24, color: T.body, font: EN_FONT })],
  });
}
function caption(text) {
  return new Paragraph({
    keepNext: true, spacing: { before: 160, after: 80, line: 312 },
    children: [new TextRun({ text, bold: true, size: 21, color: T.primary, font: EN_FONT })],
  });
}
// three-line style table with filled header
function tbl(headers, rows, widths) {
  const mk = (text, isHeader, w) => new TableCell({
    width: { size: w, type: WidthType.PERCENTAGE },
    margins: { top: 60, bottom: 60, left: 120, right: 120 },
    shading: isHeader ? { type: ShadingType.CLEAR, fill: T.headerBg } : undefined,
    children: [new Paragraph({
      spacing: { line: 276 },
      children: [new TextRun({
        text, bold: isHeader, size: 20,
        color: isHeader ? T.headerText : T.body, font: EN_FONT,
      })],
    })],
  });
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 6, color: T.accentLine },
      bottom: { style: BorderStyle.SINGLE, size: 6, color: T.accentLine },
      left: NB, right: NB,
      insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: T.innerLine },
      insideVertical: NB,
    },
    rows: [
      new TableRow({
        tableHeader: true, cantSplit: true,
        children: headers.map((hh, i) => mk(hh, true, widths[i])),
      }),
      ...rows.map(r => new TableRow({
        cantSplit: true,
        children: r.map((cell, i) => mk(cell, false, widths[i])),
      })),
    ],
  });
}

// ---------------------------------------------------------------- page math (verified)
const EXISTING = [
  ["Home", 1], ["Services", 63], ["Industries", 397], ["Solutions", 25],
  ["Platforms", 25], ["Case Studies", 37], ["Company", 8], ["Approach", 4],
  ["Insights", 33], ["Contact & Legal", 9],
];
const NEW_PAGES = [
  ["Leadership & Governance — 12 executive and board profiles", 12],
  ["Partnerships & Alliances — hub plus 12 technology alliance pages", 13],
  ["Careers — hub, culture, open positions, benefits and development", 4],
  ["Newsroom — hub plus 8 launch press releases", 9],
];
const sum = (arr) => arr.reduce((a, b) => a + b, 0);
const existingTotal = sum(EXISTING.map(r => r[1]));
const newTotal = sum(NEW_PAGES.map(r => r[1]));
const grandTotal = existingTotal + newTotal;
console.log("Page math check: existing =", existingTotal, "| new =", newTotal, "| grand total =", grandTotal);
if (existingTotal !== 602 || grandTotal !== 640) throw new Error("Page math mismatch");

// ---------------------------------------------------------------- chapters
const execSummary = [
  h1("Executive Summary"),
  body([["This proposal defines how the approved Achala IT Solutions content platform — ", false], ["602 pages and 223,751 words", true], [" of industry- and service-aligned deep-technology copy — becomes a fully working public website at www.achalasolutions.com. It specifies the technology stack, the design system, the final page architecture, the SEO and conversion layers, the hosting approach and the delivery sequence, so that one approval produces one deployable result with no open questions left for the development team.", false]]),
  body([["The recommended build is a ", false], ["static-first Next.js production", true], [": every one of the ", false], ["640 final pages", true], [" ships as pre-built HTML carrying per-page metadata, JSON-LD structured data, four-level mega-menu navigation and complete cross-linking. The exported site is a single folder of files that runs on any hosting platform — from Vercel to the existing cPanel account — with no server code, database or plugin stack to maintain. Contact forms operate through a managed form endpoint, so the static architecture never compromises lead capture.", false]]),
  body([["Delivery is organised into ", false], ["seven phases with checkable artefacts", true], [": a clickable design preview after Phase 2, the complete 640-page staging site after Phase 3, and a deployable export with handover documentation at Phase 6. Ten kickoff inputs are required from Achala IT Solutions — logo source files, office addresses, executive profiles, legal sign-off on metrics and six further items listed in Chapter 10. Comparable 600-plus-page agency builds are typically quoted in the USD 1.5 to 2.5 million band (indicative enterprise market range); the automated content pipeline specified in this proposal is what makes the same scope deliverable now, and maintainable afterwards at a fraction of the ongoing cost.", false]]),
  body([["Decision requested: ", true], ["approval of this architecture and supply of the Phase 0 inputs listed in the kickoff checklist.", false]]),
];

const ch1 = [
  h1("1. Where the Project Stands Today"),
  body([["The writing phase is complete. Eleven content volumes cover the entire planned information architecture: home, eight deep service towers with 54 services, twelve industries with 48 sub-industries and 336 capability pages, 24 solutions, 8 platforms with architecture and use-case pages, 36 anonymised case studies, company and approach pages, the insights library, and contact and legal pages. Every page was drafted against the page inventory — the build contract that fixes URL paths, menu levels, page templates, SEO titles, meta descriptions and word targets for the whole site.", false]]),
  caption("Table 1 — Content volumes delivered and verified"),
  tbl(
    ["Volume", "Pages", "Words"],
    [
      ["V01 — Home & Services", "64", "27,425"],
      ["V02 — Industries A (Hubs & Sub-Industries)", "31", "14,254"],
      ["V03 — Industries B (Hubs & Sub-Industries)", "30", "11,859"],
      ["V04 — Industry Capability Pages A", "48", "22,986"],
      ["V05 — Industry Capability Pages B", "48", "21,312"],
      ["V06 — Sub-Industry Capability Pages A", "120", "41,833"],
      ["V07 — Sub-Industry Capability Pages B", "120", "38,318"],
      ["V08 — Solutions & Platforms", "50", "18,473"],
      ["V09 — Case Studies", "37", "12,507"],
      ["V10 — Company, Approach & Contact", "21", "4,780"],
      ["V11 — Insights Library", "33", "10,004"],
      ["Total", "602", "223,751"],
    ],
    [64, 18, 18],
  ),
  body([["Two supporting documents complete the package: the ", false], ["Website Blueprint", true], [" (navigation specification, URL conventions, 23 page-template recipes, SEO framework and governance checklist) and the ", false], ["Page Inventory workbook", true], [" (602 rows: ID, section, menu levels 1 to 4, title, URL path, template, SEO fields, word targets and volume references). Together they form the contract the website is built against; the build does not re-decide structure, it renders it.", false]]),
  body([["One repositioning point needs explicit confirmation. The current live site at www.achalasolutions.com presents the earlier web-development-agency identity — front-end and back-end stacks, mobile development, digital marketing and similar commodity services. The new content deliberately excludes basic web and app development and positions Achala IT Solutions around eight deep technology towers aligned to twelve industries. At launch the new architecture replaces the old positioning entirely, and a 301 redirect map carries any accumulated search equity from the old URLs to their closest new equivalents.", false]]),
];

const ch2 = [
  h1("2. Recommended Technology Stack"),
  body([["The governing requirement is that the finished site can be ", false], ["hosted by simply uploading files", true], [". That points to a static-first architecture: all 640 pages are pre-rendered at build time into plain HTML, CSS and JavaScript. The benefits compound across the life of the site — near-zero hosting cost, no database or plugin vulnerabilities, page loads in the low hundreds of milliseconds, and an attack surface that excludes the entire category of CMS exploits.", false]]),
  caption("Table 2 — Technology stack by layer"),
  tbl(
    ["Layer", "Selection", "Why this choice"],
    [
      ["Framework", "Next.js 16 (App Router, TypeScript, static export)", "Industry-standard React framework; first-class Metadata API for per-page SEO; static export deploys anywhere"],
      ["Styling", "Tailwind CSS 4 with design tokens", "A single token file drives colour, type and spacing across 640 pages, keeping the design consistent"],
      ["Components", "shadcn/ui accessible primitives", "Keyboard-complete menus, dialogs and forms out of the box; required for WCAG 2.2 AA"],
      ["Content", "Typed JSON content layer + MDX for long-form", "Pages are generated from the same structured data that produced the volumes — one source of truth"],
      ["Search", "Pagefind static index", "Sub-millisecond client-side search across all pages with no backend service"],
      ["Forms", "Managed endpoint (Web3Forms / Formspree)", "Working contact forms on purely static hosting; spam filtering included"],
      ["Analytics", "GA4 (optional Plausible) behind cookie consent", "Measures conversions while respecting the GDPR-aligned positioning"],
      ["SEO", "Metadata API + JSON-LD + sitemap.xml + robots.txt", "Every page ships title, description, canonical, Open Graph and structured data"],
      ["Hosting", "Vercel / Netlify, or any static host via export folder", "Same build artefact serves all three deployment options in Chapter 7"],
      ["QA", "Link-graph crawler + Lighthouse CI", "Zero broken links and performance budgets enforced before every release"],
    ],
    [16, 34, 50],
  ),
  body([["Alternatives were assessed and set aside for concrete reasons rather than preference.", false]]),
  caption("Table 3 — Options considered and rejected"),
  tbl(
    ["Option", "Why it is not recommended for this build"],
    [
      ["WordPress", "At 640 pages it requires heavy plugin chains for SEO, forms and performance; plugin and core updates become a permanent security and maintenance burden"],
      ["Astro", "A capable static generator, but the component ecosystem and future server upgrade path are weaker than Next.js for a site that may later grow a client portal"],
      ["Hand-coded HTML", "Unmaintainable at this scale; every content edit becomes a deployment-risk event"],
      ["Site builders (Wix, Squarespace)", "Cannot express the four-level navigation, custom design system or per-page structured data a Fortune-100-grade site requires"],
    ],
    [24, 76],
  ),
  body([["The stack also preserves an upgrade path: if Achala IT Solutions later wants authenticated client portals, personalisation or server-side integrations, the same codebase moves from static export to hosted Next.js without a rewrite. Nothing in the recommended build is throwaway.", false]]),
];

const ch3 = [
  h1("3. Site Architecture and Final Page Count"),
  body([["The site ships with 640 content pages: the 602 pages already drafted, plus 38 company-depth pages that the brief calls for and the volumes do not yet include — leadership profiles, a partnerships and alliances section, careers and a newsroom. These 38 pages are authored during the build to the same editorial standard and inventory format as the existing 602.", false]]),
  caption("Table 4 — Final page mathematics"),
  tbl(
    ["Section", "Existing", "Added in build", "Total"],
    [
      ["Home", "1", "0", "1"],
      ["Services (hub, 8 towers, 54 services)", "63", "0", "63"],
      ["Industries (12 hubs, 48 sub-industries, 336 capability pages)", "397", "0", "397"],
      ["Solutions (hub, 4 categories, 24 solutions)", "25", "0", "25"],
      ["Platforms (8 platforms x 3 pages, hub)", "25", "0", "25"],
      ["Case Studies (hub, 36 engagements)", "37", "0", "37"],
      ["Company (about, values, trust, offices and more)", "8", "38", "46"],
      ["Approach (4 methodology pages)", "4", "0", "4"],
      ["Insights (hub, 8 categories, 24 articles)", "33", "0", "33"],
      ["Contact & Legal", "9", "0", "9"],
      ["Total", "602", "38", "640"],
    ],
    [46, 16, 20, 18],
  ),
  body([["The 38 added pages break down as follows: ", false], ["Leadership & Governance", true], [" — twelve executive and board profiles joining the existing company pages; ", false], ["Partnerships & Alliances", true], [" — one hub plus twelve technology alliance pages (cloud, data, silicon and platform partners); ", false], ["Careers", true], [" — hub, culture, open positions and benefits; ", false], ["Newsroom", true], [" — hub plus eight launch press releases. Where any of these overlaps an existing company page, the inventory dedupes the structure — for example, the leadership overview page becomes the parent of the twelve profiles. Utility templates (404, search results, form thank-you, status) exist outside this count.", false]]),
  h2("3.1 Navigation: four levels, two mega menus"),
  body([["Primary navigation carries eight first-level items — Services, Industries, Solutions, Platforms, Case Studies, Insights, About Us — plus a Contact call-to-action button. The Services mega menu renders eight tower columns, each listing its services; the Industries mega menu renders twelve industries whose flyouts expose four sub-industries and capability links; Solutions groups into four categories of six; Platforms renders eight platforms with overview, architecture and use-case flyouts. The deepest tier, level four, is formed by the 336 industry and sub-industry capability pages, reached through breadcrumbs and in-page grids as well as menus.", false]]),
  h2("3.2 Interlinking: the site is a graph, not a pile"),
  body([["Four linking systems make every page discoverable from every other. First, ", false], ["breadcrumbs", true], [" on all pages expose the full level-1 to level-4 path. Second, ", false], ["related-page blocks", true], [" are computed from the taxonomy: each industry capability page links to its tower service equivalents, matching case studies and the relevant platform; each case study links back to its industry and towers. Third, ", false], ["contextual links", true], [" are written into the copy itself, following the alignment rules already fixed in the content. Fourth, the ", false], ["footer", true], [" carries a compact sitemap of all eight sections plus legal links. Phase 5 enforces the guarantee mechanically: an automated crawl of all 640 pages must report zero broken links, zero orphan pages, and every page reachable within four clicks of the home page.", false]]),
];

const ch4 = [
  h1("4. Design System: The Fortune-100 Standard"),
  body([["The visual benchmark is the set of sites that define enterprise gravitas today — accenture.com, ibm.com, palantir.com and mckinsey.com. The shared grammar is editorial confidence: a restrained palette, large and calm typography, generous whitespace, data-forward hero sections, and motion used only to direct attention. The design will read as a peer of those sites, not as a template.", false]]),
  h2("4.1 Tokens, type and motion"),
  body([["Palette: deep ink navy anchors the brand, an electric cyan accent carries interaction and data highlights, and white editorial sections hold long-form reading; the palette is continuous with this proposal so corporate documents and website share one identity. Typography: Sora for display headings and Inter for body text, self-hosted through next/font so there is zero external font request and zero layout shift; type scales on a 1.25 ratio over an 8-point spacing grid. Motion: scroll-triggered reveals capped at 300 milliseconds, animated counters on the proof bar, and smooth mega-menu transitions — all suppressed automatically for users who prefer reduced motion. Imagery: AI-generated abstract technology visuals and custom SVG architecture diagrams rather than stock photography, delivered in AVIF/WebP with alt text on every image.", false]]),
  h2("4.2 Twelve master templates render 640 pages"),
  caption("Table 5 — Template families and the pages they serve"),
  tbl(
    ["Template family", "Serves", "Defining blocks"],
    [
      ["Home", "1 page", "Hero, proof bar, tower grid, industries strip, featured cases, insights, CTA band"],
      ["Section hub", "7 hubs", "Intro, filterable card grid, featured items, linking rails"],
      ["Tower hub", "8 pages", "Tower narrative, 54-service grid, platform link, proof metrics"],
      ["Service page", "54 pages", "Problem frame, method, first-90-days plan, outcomes, related industries"],
      ["Industry / sub-industry", "60 pages", "Market pressures, alignment matrix to towers, regulatory notes, CTA"],
      ["Capability page", "336 pages", "Industry-specific challenge, tower capability, outcomes, case and platform links"],
      ["Solution page", "24 pages", "Outcome promise, architecture sketch, metrics, service dependencies"],
      ["Platform pages", "24 pages", "Overview, architecture and trust, industry use cases"],
      ["Case study", "36 pages", "Client context, intervention, quantified outcomes, delivery model, migration note"],
      ["Insight article", "24 pages", "Thesis, argument, vendor questions, related services"],
      ["Company pages", "46 pages", "About, 12 leadership profiles, 13 partnership pages, careers, newsroom"],
      ["Contact, legal & utility", "9 + 4 pages", "Contact, book-a-briefing, legal set, 404, search, thank-you, status"],
    ],
    [24, 16, 60],
  ),
  h2("4.3 Logo and brand assets"),
  body([["The brief requires the site to use the Achala IT Solutions logo. The current website is protected by a JavaScript bot challenge, so the logo cannot be extracted automatically; two routes resolve this in Phase 0: Achala IT Solutions supplies the source files (preferably SVG, or transparent PNG at 512 pixels and above), or approves a clean vector redraw traced from the existing mark. The logo package then generated includes favicon, apple-touch icon, Open Graph share image, and monochrome variants for the dark footer and light header contexts.", false]]),
];

const ch5 = [
  h1("5. SEO, Metadata and Discoverability"),
  body([["Every one of the 602 drafted pages already carries an SEO title of at most 60 characters and a meta description of at most 155 characters, fixed in the page inventory. The build wires these directly into the Next.js Metadata API — no page ships without its title, description, canonical URL, Open Graph and Twitter card. The 38 pages authored during the build are written to the same specification before they enter the pipeline.", false]]),
  caption("Table 6 — Structured data (JSON-LD) by page type"),
  tbl(
    ["Schema type", "Applied to"],
    [
      ["Organization + WebSite + SearchAction", "Site-wide; enables knowledge-panel signals and sitewide search box"],
      ["BreadcrumbList", "All 640 pages; mirrors the visible breadcrumb trail"],
      ["Service", "8 tower hubs and 54 service pages"],
      ["Article", "36 case studies and 24 insight articles"],
      ["NewsArticle", "8 newsroom releases"],
      ["ProfilePage", "12 leadership profiles"],
      ["JobPosting", "Careers open-positions page"],
      ["FAQPage", "Pages carrying FAQ blocks"],
      ["ItemList", "Hub pages listing their children"],
    ],
    [42, 58],
  ),
  body([["A sitemap of all 640 URLs is generated from the inventory at build time, with robots.txt excluding staging and utility paths. Site search uses a Pagefind static index: it indexes all pages at build, ships as static files, and returns results in milliseconds with no backend. The performance budget is part of the definition of done, not an aspiration.", false]]),
  caption("Table 7 — Performance and accessibility budgets"),
  tbl(
    ["Budget", "Target"],
    [
      ["Largest Contentful Paint (LCP)", "2.0 seconds or less on 4G mobile"],
      ["Interaction to Next Paint (INP)", "200 milliseconds or less"],
      ["Cumulative Layout Shift (CLS)", "0.05 or less"],
      ["Lighthouse (Performance, Accessibility, Best Practices, SEO)", "95 or higher in every category"],
      ["Initial JavaScript", "150 KB gzipped or less on content pages"],
      ["Accessibility", "WCAG 2.2 AA; full keyboard navigation; contrast verified"],
      ["Images", "AVIF/WebP, responsive sizes, lazy loading, alt text throughout"],
    ],
    [52, 48],
  ),
  body([["Migration safety: the legacy URLs receive 301 redirects to their closest new equivalents; staging runs behind a noindex header until cutover; at launch the sitemap is submitted to Google Search Console and Bing Webmaster Tools, and indexing is monitored for the first month.", false]]),
];

const ch6 = [
  h1("6. Conversion Layer: Forms, Contact and Careers"),
  body([["Lead capture works from every page. A compact four-field contact form lives in the footer sitewide — name, work email, company and area of interest chosen from the eight towers — while the contact page and the book-a-briefing page carry the full form with a message field and a consent checkbox. Submissions are delivered by a managed form endpoint (Web3Forms or Formspree) to the Achala IT Solutions inbox; spam protection combines a honeypot field, a time-trap and provider-side filtering, and an optional webhook can mirror each submission into a CRM or a Slack channel. A dedicated thank-you page fires the conversion event and offers the next best content.", false]]),
  body([["Analytics are wired to the business questions: GA4 events for form start, form submit, call-to-action clicks and mega-menu engagement, with an optional Plausible overlay for simple traffic reporting. Because the positioning is GDPR-aligned, a consent banner gates all analytics cookies by default — the site is compliant out of the box rather than by later patch. Careers and newsroom-subscribe forms reuse the same endpoint and tracking so every conversion path is measurable from day one.", false]]),
];

const ch7 = [
  h1("7. Hosting and Deployment Options"),
  body([["The build exports one self-contained folder — pure HTML, CSS, JavaScript and assets — so hosting is a choice rather than a constraint. All three options below run the identical artefact; the difference is operational convenience.", false]]),
  caption("Table 8 — Hosting options"),
  tbl(
    ["Option", "Fit", "Notes"],
    [
      ["A. Vercel or Netlify (recommended)", "Zero-effort operation", "Git-connected builds, preview URLs for review, automatic TLS and CDN; free tier comfortably covers a brochure site"],
      ["B. Existing hosting / cPanel", "Use what Achala IT Solutions already pays for", "Upload the export folder by FTP or file manager; works on Hostinger-type shared plans because the site is pure static files"],
      ["C. AWS S3 + CloudFront", "AWS-aligned organisations", "Infrastructure-as-code setup; effectively zero cost at brochure-site traffic"],
    ],
    [30, 22, 48],
  ),
  body([["Cutover follows a fixed sequence with no discretionary steps.", false]]),
  body([["1. Staging preview approved on the chosen host, with the noindex header active.", false]]),
  body([["2. DNS for www.achalasolutions.com pointed at the host; TLS issued automatically.", false]]),
  body([["3. The 301 redirect map from legacy URLs goes live together with the new site.", false]]),
  body([["4. The sitemap is submitted to Google Search Console and Bing Webmaster Tools.", false]]),
  body([["5. Analytics and form endpoints are verified end-to-end with live test submissions.", false]]),
  body([["6. The legacy site is archived, and the old positioning is retired from the index as redirects take effect.", false]]),
];

const ch8 = [
  h1("8. Build Plan: Phases, Deliverables and Effort"),
  body([["The build runs in seven phases, each ending in an artefact that can be checked before the next begins. Nothing depends on invisible progress: at every gate there is something to click, crawl or read.", false]]),
  caption("Table 9 — Delivery phases and their gates"),
  tbl(
    ["Phase", "Output", "Gate"],
    [
      ["0. Kickoff & assets", "Logo package, addresses, executive profiles, legal sign-off, hosting choice", "Ten kickoff inputs received (Chapter 10)"],
      ["1. Foundation & shell", "Next.js project, design tokens, four-level mega menu, footer with forms", "Navigable shell on staging"],
      ["2. Design system & templates", "12 master templates; six key pages fully designed", "Clickable design preview approved"],
      ["3. Content pipeline", "602 pages emitted from structured data; 38 new pages authored", "All 640 pages live on staging"],
      ["4. SEO & conversion layer", "Metadata, JSON-LD, sitemap, OG images, search, analytics, consent", "SEO audit passes on sampled pages"],
      ["5. QA & hardening", "Full link-graph crawl, Lighthouse runs, device matrix, content QA against inventory", "Zero broken links; budgets met"],
      ["6. Export & launch", "Static export deployed; DNS cut over; redirects verified; handover documentation", "Site live and indexed"],
    ],
    [24, 44, 32],
  ),
  body([["On effort: a 600-plus-page custom enterprise build with a bespoke design system and four-level navigation is the territory where agencies typically quote in the USD 1.5 to 2.5 million band (an indicative market range, not an offer). What makes this project tractable is that the writing — normally the largest single line item — is already complete, and the page pipeline generates every page from structured data rather than by hand. The remaining effort concentrates where humans add irreplaceable value: interaction design, the 38 authored company pages, and the QA regime.", false]]),
  body([["Maintenance after launch follows the same logic: a content change is an edit to structured data followed by a rebuild, which regenerates the affected pages, the sitemap and the search index in minutes — no page is ever edited by hand in the export folder.", false]]),
];

const ch9 = [
  h1("9. Risks and Mitigations"),
  body([["Every material risk to the build is paired with a concrete mitigation and, where relevant, a phase gate that stops the launch clock until the risk is retired.", false]]),
  caption("Table 10 — Risk register"),
  tbl(
    ["Risk", "Mitigation", "Gate"],
    [
      ["Logo source unavailable (legacy site bot-protected)", "Supply source files in Phase 0 or approve the vector redraw", "Phase 0"],
      ["Placeholders remain in content (addresses, executive data)", "Kickoff checklist item-by-item; export blocked while placeholders persist", "Phase 5"],
      ["Proof-bar and case metrics lack legal sign-off", "Metrics frozen at Phase 5; sign-off recorded before export", "Phase 5"],
      ["Contact form spam", "Managed endpoint filtering, honeypot, time-trap, mailbox rules", "Phase 4"],
      ["SEO equity lost in migration", "301 redirect map, staging noindex, Search Console monitoring for 30 days", "Phase 6"],
      ["Content drifts out of date", "Insights cadence; inventory-driven edits rebuild pages in minutes", "Ongoing"],
      ["Device or browser regressions", "Test matrix: Chrome, Safari, Firefox, Edge on desktop; iOS and Android at 320 to 1920 pixels", "Phase 5"],
    ],
    [34, 48, 18],
  ),
];

const ch10 = [
  h1("10. Kickoff Checklist: What We Need From Achala IT Solutions"),
  body([["Ten inputs unlock the build. Items 1 to 4 block final launch quality; the rest can arrive in parallel with Phase 1.", false]]),
  numItem("kickoff", "Logo source files — SVG preferred, or transparent PNG at 512 pixels and above; or written approval to redraw the mark as clean vector art."),
  numItem("kickoff", "Street addresses for the four offices (Tysons Corner, London, Hyderabad, Riyadh) — currently the only placeholders left in the content."),
  numItem("kickoff", "Leadership data — up to twelve names, titles, approximately 100-word biographies and headshots; or approval to draft structured profiles for later replacement."),
  numItem("kickoff", "Legal sign-off on the proof-bar claims (350+ engagements, 2,400+ specialists, 99.99% availability, zero-exposure record) and on case-study metrics."),
  numItem("kickoff", "Form destination — confirmation that info@achalasolutions.com receives submissions, plus any CRM webhook to mirror leads."),
  numItem("kickoff", "Hosting choice among Options A, B and C in Chapter 7, with DNS access arranged for cutover."),
  numItem("kickoff", "GA4 measurement identifier (or approval to create one) and consent-banner preferences."),
  numItem("kickoff", "Social profile URLs for the footer (LinkedIn and any others)."),
  numItem("kickoff", "Partner logos Achala IT Solutions has rights to display, for the twelve alliance pages; otherwise they launch text-first and gain logos later."),
  numItem("kickoff", "Written confirmation that the legacy web-development-agency positioning is retired at launch."),
  body([["On receipt of items 1 to 4, Phase 1 starts immediately; the design preview arrives at the end of Phase 2, and the full 640-page staging site at the end of Phase 3. Every later gate re-uses artefacts you have already approved, so the path from this document to a live, indexed, lead-generating website is short and fully visible.", false]]),
];

const appendix = [
  h1("Appendix A. Representative URL Map"),
  body([["The following rows are taken from the page inventory and illustrate the URL grammar for every template family. Six hundred and forty pages follow these patterns; the full map lives in the Page Inventory workbook.", false]]),
  caption("Table 11 — URL patterns by template"),
  tbl(
    ["URL path", "Page", "Template / depth"],
    [
      ["/", "Home", "home / L0"],
      ["/services/", "Services Overview", "hub / L1"],
      ["/services/applied-ai-generative-ai/", "Applied AI & Generative AI tower", "tower hub / L2"],
      ["/services/applied-ai-generative-ai/enterprise-ai-strategy/", "Enterprise AI Strategy & Roadmapping", "service / L3"],
      ["/industries/", "Industries Overview", "hub / L1"],
      ["/industries/banking-financial-services/", "Banking & Financial Services", "industry hub / L2"],
      ["/industries/banking-financial-services/retail-banking/", "Retail & Consumer Banking", "sub-industry / L3"],
      ["/industries/banking-financial-services/capabilities/applied-ai-generative-ai/", "Applied AI & GenAI for BFSI", "capability / L3"],
      ["/industries/banking-financial-services/retail-banking/capabilities/applied-ai-generative-ai/", "Applied AI & GenAI for Retail Banking", "capability / L4"],
      ["/solutions/customer-360/", "Customer 360 & Hyper-Personalization", "solution / L2"],
      ["/platforms/nexus/", "Achala Nexus — Overview", "platform / L2"],
      ["/platforms/nexus/architecture/", "Achala Nexus — Architecture & Trust", "platform / L3"],
      ["/case-studies/bank-01/", "A top-10 European retail bank", "case study / L2"],
      ["/about-us/", "About Achala IT Solutions", "company / L1"],
      ["/our-approach/the-achala-method/", "The Achala Method", "approach / L2"],
      ["/insights/insight-01/", "Insight article", "insight / L2"],
      ["/contact/", "Contact Achala IT Solutions", "contact / L1"],
      ["/privacy-policy/", "Privacy Policy", "legal / L1"],
    ],
    [52, 30, 18],
  ),
];

// ---------------------------------------------------------------- assembly
const pgSize = { width: 11906, height: 16838 };
const pgMargin = { top: 1440, bottom: 1440, left: 1701, right: 1417 };

function pageFooter() {
  return new Footer({
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "808080", font: EN_FONT })],
    })],
  });
}
function pageHeader() {
  return new Header({
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: T.innerLine, space: 4 } },
      children: [new TextRun({
        text: "Achala IT Solutions — Corporate Website Build & Technology Proposal",
        size: 18, color: "808080", font: EN_FONT,
      })],
    })],
  });
}

const frontMatter = [
  ...execSummary,
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { before: 480, after: 360 },
    children: [new TextRun({ text: "Table of Contents", bold: true, size: 32, color: T.primary, font: HEAD_FONT })],
  }),
  new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-2" }),
  new Paragraph({
    spacing: { before: 200 },
    children: [new TextRun({
      text: "Note: This Table of Contents is generated via field codes. To ensure page number accuracy after editing, please right-click the TOC and select Update Field.",
      italics: true, size: 18, color: "888888", font: EN_FONT,
    })],
  }),
];

const doc = new Document({
  creator: "Achala IT Solutions Corporation",
  title: "Achala IT Solutions — Corporate Website Build & Technology Proposal",
  description: "Technology stack, architecture, design system and delivery plan for the 640-page www.achalasolutions.com website.",
  styles: {
    default: {
      document: {
        run: { font: EN_FONT, size: 24, color: T.body },
        paragraph: { spacing: { line: 312 } },
      },
      heading1: {
        run: { font: HEAD_FONT, size: 32, bold: true, color: T.primary },
        paragraph: { spacing: { before: 360, after: 160, line: 312 }, outlineLevel: 0 },
      },
      heading2: {
        run: { font: HEAD_FONT, size: 28, bold: true, color: T.h2 },
        paragraph: { spacing: { before: 240, after: 120, line: 312 }, outlineLevel: 1 },
      },
    },
  },
  numbering: {
    config: [
      {
        reference: "kickoff",
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } },
        }],
      },
    ],
  },
  sections: [
    { // 1 — Cover
      properties: { page: { size: pgSize, margin: { top: 0, bottom: 0, left: 0, right: 0 } } },
      children: buildCoverR1({
        title: "Corporate Website Build Proposal",
        subtitle: "Technology stack, design system, SEO engineering and delivery plan for a 640-page, Fortune-100-grade website at www.achalasolutions.com",
        englishLabel: "ACHALA SOFT CORPORATION",
        metaLines: [
          "Prepared for: Achala IT Solutions Corporation — Board & Founders",
          "Scope: Design, build and launch of the full public website",
          "Basis: 602-page approved content platform (223,751 words)",
          "Date: November 20, 2026",
          "Version: 1.0 — For approval",
        ],
        footerLeft: "Achala IT Solutions Corporation — Confidential",
        footerRight: "www.achalasolutions.com",
        palette: COVER,
      }),
    },
    { // 2 — Front matter (Roman)
      properties: {
        type: SectionType.NEXT_PAGE,
        page: { size: pgSize, margin: pgMargin, pageNumbers: { start: 1, formatType: NumberFormat.UPPER_ROMAN } },
      },
      footers: { default: pageFooter() },
      children: frontMatter,
    },
    { // 3 — Body (Arabic, restart at 1)
      properties: {
        type: SectionType.NEXT_PAGE,
        page: { size: pgSize, margin: pgMargin, pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL } },
      },
      headers: { default: pageHeader() },
      footers: { default: pageFooter() },
      children: [...ch1, ...ch2, ...ch3, ...ch4, ...ch5, ...ch6, ...ch7, ...ch8, ...ch9, ...ch10, ...appendix],
    },
  ],
});

const OUT = "/home/z/my-project/download/achalasolutions-website-content/achala_Soft_Website_Build_Proposal.docx";
Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT, buf);
  console.log("Written:", OUT, "(", buf.length, "bytes )");
});
