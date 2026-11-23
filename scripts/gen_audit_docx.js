// Generate: Achala Website Content Audit & Change Register (.docx)
// Cover recipe R2 (Double-Rule Frame) per docx skill design-system.
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, PageNumber, NumberFormat, AlignmentType, HeadingLevel,
  WidthType, BorderStyle, ShadingType, TableLayoutType, SectionType,
  TableOfContents, PageBreak,
} = require("docx");
const fs = require("fs");

const { A, B } = require("./audit_data_1.js");
const { C } = require("./audit_data_2.js");
const { DS, E } = require("./audit_data_3.js");
const { DP } = require("./audit_data_4.js");

// ── Brand palette (Achala: orange FE5722 + deep navy 18142D + white) ──
const P = {
  bg: "18142D", accent: "FE5722",
  primary: "18142D", body: "1A1A1A", secondary: "5A5F6B",
  cover: { titleColor: "FFFFFF", subtitleColor: "C9CDD6", metaColor: "A7ACB8", footerColor: "8A8F9C" },
  table: { headerBg: "18142D", headerText: "FFFFFF", accentLine: "FE5722", innerLine: "D9DBE0", surface: "F5F6F8" },
};
const NB = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: NB, bottom: NB, left: NB, right: NB };
const allNoBorders = { top: NB, bottom: NB, left: NB, right: NB, insideHorizontal: NB, insideVertical: NB };
const EN = { ascii: "Times New Roman", eastAsia: "Times New Roman", hAnsi: "Times New Roman" };

function safeText(v, ph) {
  if (v === undefined || v === null || v === "" || String(v) === "NaN" || String(v) === "undefined") return ph || "[n/a]";
  return String(v);
}

// ── Title layout helpers (from design-system.md, width-aware for Latin text) ──
function estimateTextWidth(text, pt) {
  let w = 0;
  for (const ch of text) {
    const code = ch.codePointAt(0);
    const isCJK = (code >= 0x4e00 && code <= 0x9fff) || (code >= 0x3000 && code <= 0x303f);
    w += isCJK ? pt * 20 : pt * 11;
  }
  return w;
}
function splitTitleLines(title, maxWidthTwips, pt) {
  const words = title.split(" ");
  const lines = [];
  let cur = "";
  for (const wd of words) {
    const trial = cur ? cur + " " + wd : wd;
    if (estimateTextWidth(trial, pt) <= maxWidthTwips || !cur) cur = trial;
    else { lines.push(cur); cur = wd; }
  }
  if (cur) lines.push(cur);
  if (lines.length > 1 && lines[lines.length - 1].length <= 2) {
    const last = lines.pop();
    lines[lines.length - 1] += " " + last;
  }
  return lines;
}
function calcTitleLayout(title, maxWidthTwips, preferredPt = 40, minPt = 24) {
  let titlePt = preferredPt, lines;
  while (titlePt >= minPt) {
    lines = splitTitleLines(title, maxWidthTwips, titlePt);
    if (lines.length <= 3) break;
    titlePt -= 2;
  }
  if (!lines || lines.length > 3) { lines = splitTitleLines(title, maxWidthTwips, minPt); titlePt = minPt; }
  return { titlePt, titleLines: lines };
}

// ── Cover: Recipe R2 Double-Rule Frame ──
function buildCoverR2(config) {
  const padL = 1400, padR = 1400;
  const { titlePt, titleLines } = calcTitleLayout(config.title, 11906 - padL - padR, 40, 24);
  const titleSize = titlePt * 2;
  const thickBorder = { style: BorderStyle.SINGLE, size: 18, color: P.accent, space: 20 };
  const children = [];

  children.push(new Paragraph({
    indent: { left: padL - 400, right: padR - 400 }, spacing: { before: 1200, after: 200 },
    border: { top: thickBorder }, children: [],
  }));
  children.push(new Paragraph({ spacing: { before: 1500 } }));
  if (config.englishLabel) {
    children.push(new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { after: 500 },
      children: [new TextRun({ text: config.englishLabel.split("").join("  "), size: 18, color: P.accent, font: EN, characterSpacing: 40 })],
    }));
  }
  for (let i = 0; i < titleLines.length; i++) {
    children.push(new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: i < titleLines.length - 1 ? 80 : 300, line: Math.ceil(titlePt * 23), lineRule: "atLeast" },
      children: [new TextRun({ text: titleLines[i], size: titleSize, bold: true, color: P.cover.titleColor, font: { ascii: "Arial", eastAsia: "Arial", hAnsi: "Arial" } })],
    }));
  }
  if (config.subtitle) {
    children.push(new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { after: 400, line: 320, lineRule: "atLeast" },
      children: [new TextRun({ text: config.subtitle, size: 24, color: P.cover.subtitleColor, font: { ascii: "Arial", eastAsia: "Arial", hAnsi: "Arial" } })],
    }));
  }
  children.push(new Paragraph({ spacing: { before: 1000 } }));
  for (const line of (config.metaLines || [])) {
    children.push(new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { after: 100, line: Math.ceil(18 * 23), lineRule: "atLeast" },
      children: [new TextRun({ text: line, size: 36, color: P.cover.metaColor, font: { ascii: "Arial", eastAsia: "Arial", hAnsi: "Arial" } })],
    }));
  }
  children.push(new Paragraph({ spacing: { before: 1700 } }));
  children.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    indent: { left: padL - 400, right: padR - 400 }, spacing: { before: 200 },
    border: { bottom: thickBorder },
    children: [new TextRun({ text: config.footerRight || "", size: 18, color: P.cover.footerColor, font: { ascii: "Arial", eastAsia: "Arial", hAnsi: "Arial" } })],
  }));

  return [new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    layout: TableLayoutType.FIXED,
    borders: allNoBorders,
    rows: [new TableRow({
      height: { value: 16838, rule: "exact" },
      children: [new TableCell({
        shading: { type: ShadingType.CLEAR, fill: P.bg }, borders: noBorders,
        children,
      })],
    })],
  })];
}

// ── Body builders ──
function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1, spacing: { before: 400, after: 160, line: 312 },
    children: [new TextRun({ text, bold: true, size: 32, color: P.primary, font: EN })],
  });
}
function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2, spacing: { before: 300, after: 120, line: 312 },
    children: [new TextRun({ text, bold: true, size: 26, color: P.primary, font: EN })],
  });
}
function body(text, opts = {}) {
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED, spacing: { after: opts.after ?? 120, line: 312 },
    children: [new TextRun({ text: safeText(text), size: 22, color: P.body, font: EN })],
  });
}
function bodyRuns(runs, opts = {}) {
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED, spacing: { after: opts.after ?? 120, line: 312 },
    children: runs,
  });
}
const PRI_LABEL = { 1: "P1 \u00b7 must-fix", 2: "P2 \u00b7 should-fix", 3: "P3 \u00b7 polish" };
function changeItem(it) {
  const out = [];
  out.push(new Paragraph({
    spacing: { before: 180, after: 40, line: 312 },
    border: { left: { style: BorderStyle.SINGLE, size: 18, color: P.accent, space: 8 } },
    indent: { left: 200 },
    children: [
      new TextRun({ text: it.id, bold: true, size: 22, color: P.accent, font: EN }),
      new TextRun({ text: "  \u00b7  " + safeText(it.loc), bold: true, size: 22, color: P.primary, font: EN }),
      new TextRun({ text: "   [" + PRI_LABEL[it.pri] + "]", size: 18, color: P.secondary, font: EN }),
    ],
  }));
  if (it.now) {
    out.push(new Paragraph({
      alignment: AlignmentType.JUSTIFIED, spacing: { after: 30, line: 312 }, indent: { left: 340 },
      children: [
        new TextRun({ text: "Now: ", bold: true, size: 20, color: P.secondary, font: EN }),
        new TextRun({ text: it.now, italics: true, size: 20, color: "3A3F4A", font: EN }),
      ],
    }));
  }
  out.push(new Paragraph({
    alignment: AlignmentType.JUSTIFIED, spacing: { after: 30, line: 312 }, indent: { left: 340 },
    children: [
      new TextRun({ text: "Problem: ", bold: true, size: 20, color: P.secondary, font: EN }),
      new TextRun({ text: safeText(it.why), size: 20, color: P.body, font: EN }),
    ],
  }));
  out.push(new Paragraph({
    alignment: AlignmentType.JUSTIFIED, spacing: { after: 60, line: 312 }, indent: { left: 340 },
    children: [
      new TextRun({ text: "Change: ", bold: true, size: 20, color: P.primary, font: EN }),
      new TextRun({ text: safeText(it.chg), size: 20, color: P.body, font: EN }),
    ],
  }));
  return out;
}
function renderItems(items) {
  const out = [];
  for (const it of items) out.push(...changeItem(it));
  return out;
}
function cell(text, opts = {}) {
  return new TableCell({
    width: { size: opts.w, type: WidthType.PERCENTAGE },
    shading: opts.header ? { type: ShadingType.CLEAR, fill: P.table.headerBg } : undefined,
    margins: { top: 70, bottom: 70, left: 120, right: 120 },
    children: [new Paragraph({
      spacing: { line: 276 },
      children: [new TextRun({
        text: safeText(text), size: opts.header ? 20 : 20, bold: !!opts.header || !!opts.bold,
        color: opts.header ? P.table.headerText : P.body, font: EN,
      })],
    })],
  });
}
function makeTable(headers, rows, widths) {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 6, color: P.table.accentLine },
      bottom: { style: BorderStyle.SINGLE, size: 6, color: P.table.accentLine },
      left: NB, right: NB,
      insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: P.table.innerLine },
      insideVertical: NB,
    },
    rows: [
      new TableRow({
        tableHeader: true, cantSplit: true,
        children: headers.map((t, i) => cell(t, { header: true, w: widths[i] })),
      }),
      ...rows.map((r) => new TableRow({
        cantSplit: true,
        children: r.map((t, i) => cell(t, { w: widths[i] })),
      })),
    ],
  });
}
function tableTitle(text) {
  return new Paragraph({
    keepNext: true, spacing: { before: 200, after: 100, line: 312 },
    children: [new TextRun({ text, bold: true, size: 21, color: P.primary, font: EN })],
  });
}

// ── Item population: group D-P items by domain for H2 groupings ──
const DP_DOMAINS = [
  ["Agentic AI & Hyperautomation (14 items)", "agentic"],
  ["Applied AI & Generative AI (14 items)", ["D-P15","D-P16","D-P17","D-P18","D-P19","D-P20","D-P21","D-P22","D-P23","D-P24","D-P25","D-P26","D-P27","D-P28"]],
  ["Blockchain & Digital Trust (12 items)", "blockchain"],
];

function groupByPrefix(items, prefixes) {
  const groups = [];
  let rest = items.slice();
  for (const [label, pref] of prefixes) {
    const plist = Array.isArray(pref) ? pref : null;
    const grp = rest.filter((it) => plist ? plist.includes(it.id) : it.id.startsWith(pref));
    rest = rest.filter((it) => !(plist ? plist.includes(it.id) : it.id.startsWith(pref)));
    groups.push([label, grp]);
  }
  if (rest.length) groups.push(["Remaining pages", rest]);
  return groups;
}
const dpGroups = groupByPrefix(DP, [
  ["Agentic AI & Hyperautomation \u2014 7 pages (14 items)", ["D-P0", "D-P1"]],
  ["Applied AI & Generative AI \u2014 7 pages (14 items)", ["D-P2", "D-P3", "D-P4"]],
  ["Blockchain & Digital Trust \u2014 6 pages (12 items)", ["D-P29", "D-P3", "D-P40"]],
]);

// careful: prefix overlaps; do explicit slicing instead
function sliceIds(list) {
  const byId = Object.fromEntries(DP.map((it) => [it.id, it]));
  return list.map((id) => byId[id]).filter(Boolean);
}
const dpGroupsExact = [
  ["Agentic AI & Hyperautomation \u2014 7 pages (14 items)", sliceIds(["D-P01","D-P02","D-P03","D-P04","D-P05","D-P06","D-P07","D-P08","D-P09","D-P10","D-P11","D-P12","D-P13","D-P14"])],
  ["Applied AI & Generative AI \u2014 7 pages (14 items)", sliceIds(["D-P15","D-P16","D-P17","D-P18","D-P19","D-P20","D-P21","D-P22","D-P23","D-P24","D-P25","D-P26","D-P27","D-P28"])],
  ["Blockchain & Digital Trust \u2014 6 pages (12 items)", sliceIds(["D-P29","D-P30","D-P31","D-P32","D-P33","D-P34","D-P35","D-P36","D-P37","D-P38","D-P39","D-P40"])],
  ["Cloud, Edge & Platform Engineering \u2014 7 pages (14 items)", sliceIds(["D-P41","D-P42","D-P43","D-P44","D-P45","D-P46","D-P47","D-P48","D-P49","D-P50","D-P51","D-P52","D-P53","D-P54"])],
  ["Cybersecurity & Zero-Trust \u2014 7 pages (14 items)", sliceIds(["D-P55","D-P56","D-P57","D-P58","D-P59","D-P60","D-P61","D-P62","D-P63","D-P64","D-P65","D-P66","D-P67","D-P68"])],
  ["Data, Analytics & Lakehouse \u2014 7 pages (14 items)", sliceIds(["D-P69","D-P70","D-P71","D-P72","D-P73","D-P74","D-P75","D-P76","D-P77","D-P78","D-P79","D-P80","D-P81","D-P82"])],
  ["IoT, Digital Twin & Robotics \u2014 7 pages (14 items)", sliceIds(["D-P83","D-P84","D-P85","D-P86","D-P87","D-P88","D-P89","D-P90","D-P91","D-P92","D-P93","D-P94","D-P95","D-P96"])],
  ["Quantum & Advanced Compute \u2014 6 pages (12 items)", sliceIds(["D-P97","D-P98","D-P99","D-P100","D-P101","D-P102","D-P103","D-P104","D-P105","D-P106","D-P107","D-P108"])],
];

// ── Assemble body ──
const bodyChildren = [];

// 1. Executive summary
bodyChildren.push(h1("1. Executive summary"));
bodyChildren.push(body(
  "This register answers a direct instruction: walk the site like a user, judge the homepage and the Services section as a buyer would, and list the required changes before any code or copy is touched. The walkthrough covered the homepage, the Services hub, all eight expertise hubs and all 54 practice pages of the deployed-equivalent build, at desktop viewport, reading every hero, every section heading and every dashboard element. The verdict is recorded here as 290 numbered change items, each with the current state, the specific failure, and the required change. Nothing in this document is a suggestion of style; every item traces to a communication failure a first-time visitor would hit."
));
bodyChildren.push(body(
  "The single most important finding is structural, not editorial. Measured mechanically, 45 of the 54 practice pages share the exact same block-type sequence \u2014 the same rhythm of headings, tables, diagrams and dashboards at the same positions \u2014 and the interactive widgets sit at identical slots on nearly every page. Layered on top of that skeleton are repeated sentence devices: the same \u201cBelow: the failure modes that make\u2026\u201d opener on 46 pages, the same interlink introduction on all 54, the same closing CTA block on all 54. This is why the section reads as system-generated even after the round of content enrichment: the words were changed; the machine rhythm was not."
));
bodyChildren.push(body(
  "The second finding is a trust problem in the site\u2019s core visual device. Numbers are everywhere \u2014 KPI tiles, consoles, charts \u2014 and many of the strongest ones are invented for illustration, yet they are presented without provenance. The homepage hero panel is labeled \u201cLIVE VIEW\u201d while being static; no dashboard anywhere states \u201cillustrative reference program\u201d; the homepage simultaneously claims 350+ engagements delivered and 116 published engagements without reconciling the two; and the footer carries an unverifiable absolute (\u201czero critical data-exposure incidents since inception\u201d). A diligent CFO or CISO will test one number, fail to trace it, and discount everything else on the page."
));
bodyChildren.push(body(
  "The third finding is that the pages never orient the buyer. Not one of the 54 practice pages says who owns the problem, when the practice is the wrong answer, or what effort it typically takes. Heroes average over 45 words of comma-spliced mechanism before any buyer moment appears. The architecture diagrams \u2014 the site\u2019s best asset \u2014 still carry empty annotations where it matters most: on the flagship streaming page, 13 of 19 nodes have no explanatory sub-label and roughly half the edges are unlabeled. The register\u2019s 290 items break down as follows."
));
bodyChildren.push(tableTitle("Table 1 \u2014 Register contents"));
bodyChildren.push(makeTable(
  ["Part", "Scope", "Items", "P1"],
  [
    ["A", "Homepage", "58", "12"],
    ["B", "Services hub", "16", "3"],
    ["C", "Eight expertise hubs (2 shared + 6 per hub)", "50", "1"],
    ["D-S", "Inner pages \u2014 systemic patterns", "38", "10"],
    ["D-P", "Inner pages \u2014 54 pages \u00d7 2 bespoke items", "108", "9"],
    ["E", "Global, cross-cutting and guards", "20", "7"],
    ["\u2014", "Total", "290", "42"],
  ],
  [14, 56, 14, 16]
));
bodyChildren.push(body(
  "Priorities: P1 items are must-fix \u2014 they block credible buyer communication or carry trust/legal risk (42 items). P2 items materially improve comprehension and conversion. P3 items are polish. The eight root causes below generate most of the register; fixing them once fixes hundreds of symptoms.", { after: 160 }
));
bodyChildren.push(tableTitle("Table 2 \u2014 Root causes and their evidence"));
bodyChildren.push(makeTable(
  ["#", "Root cause", "Hard evidence from the walkthrough", "Drives"],
  [
    ["1", "One page skeleton stamped 54 times", "45/54 pages share the exact block-type sequence; widgets at identical positions", "D-S01, D-S02, D-S32"],
    ["2", "Repeated sentence devices", "\u201cBelow: the failure modes\u2026\u201d on 46/54; interlink intro and CTA block on 54/54", "D-S03, D-S08, D-S09, E-10"],
    ["3", "Diagrams with empty annotations", "Streaming page: 13/19 node subs empty; ~half of edges unlabeled", "D-S11, D-S12"],
    ["4", "Numbers without provenance", "\u201cLIVE VIEW\u201d on a static mock; no illustrative labels; 350+ vs 116 conflict; absolute incident claim", "E-04, E-05, A-08, E-06"],
    ["5", "Heroes that never orient", "45+ word comma-spliced subtitles; no persona line, fit/no-fit or effort anchor on any page", "D-S15, D-S16, D-S17, D-S18"],
    ["6", "Homepage hides its proof", "3 of 116 evidence cards shown; evidence section is section 8 of 12; stats duplicated in DOM", "A-40, A-53, A-07"],
    ["7", "Component-level fingerprints", "HERO_CHIP identical on all 54 service pages; same CTA pair site-wide; marquee duplication", "E-07, E-01, E-10"],
    ["8", "Hub-level template feel", "All 8 hubs share the same 8-section order; \u201cServices Overview\u201d as hub H1", "C-01, C-02, B-01"],
  ],
  [6, 26, 44, 24]
));

// 2. Method
bodyChildren.push(h1("2. Method and evidence base"));
bodyChildren.push(body(
  "Scope. The walkthrough covered the homepage, the Services hub, all eight expertise hubs and all 54 practice pages \u2014 65 URLs in total \u2014 exactly the pages named in the instruction. The build inspected is the current gh-pages export, which contains every fix from the previous round, so the findings below are not already-known issues resurfacing; they are what remains after that round."
));
bodyChildren.push(body(
  "Procedure. Each page was read as a visitor reads it: hero, first sections, every heading, every dashboard, chart and diagram, and the closing CTA. In parallel, three extraction scripts harvested the full text and content-JSON of all 65 pages, and two metrics scripts measured structural sameness objectively: block-type sequence fingerprints, block-position histograms, shared heading and shared-string counts, and paragraph-opener repetition across the 54 pages. Screenshots captured what a user actually sees, including the cookie banner overlay and the unstyled-first-paint defects."
));
bodyChildren.push(body(
  "How to read the register. Items are grouped in six parts (A homepage, B hub, C expertise hubs, D inner pages, E global) and carry stable IDs (A-01\u2026E-20). Each item states the current text or state, the specific problem it causes a reader, and the change required \u2014 written so an implementer can execute without re-deriving intent. Where a rewrite is proposed, the quoted copy is illustrative of direction, not final approved wording; final wording is produced in the implementation pass. Cross-cutting behaviors (e.g., the CTA pair on all 63 pages) are stated once in the systemic or global part and are not repeated page by page.", { after: 200 }
));

// 3. Part A
bodyChildren.push(h1("3. Part A \u2014 Homepage (58 items)"));
bodyChildren.push(body(
  "The homepage\u2019s strongest assets \u2014 the operating console, the charter, the evidence library \u2014 are undermined by ordering, repetition and unproven numbers. The 58 items below are grouped by section; A-07, A-08, E-04 and E-06 are the trust-critical ones."
));
const A_GROUPS = [
  ["Hero and above-fold (A-01\u2013A-06)", 0, 6],
  ["Stats and proof strip (A-07\u2013A-11)", 6, 11],
  ["What delivery produces (A-12\u2013A-16)", 11, 16],
  ["Services grid (A-17\u2013A-22)", 16, 22],
  ["Consulting practices (A-23\u2013A-27)", 22, 27],
  ["Patented intelligence (A-28\u2013A-32)", 27, 32],
  ["Industries (A-33\u2013A-34)", 32, 34],
  ["Engagement charter (A-35\u2013A-36)", 34, 36],
  ["Platforms (A-37\u2013A-39)", 36, 39],
  ["Evidence library (A-40\u2013A-43)", 39, 43],
  ["Insights (A-44\u2013A-45)", 43, 45],
  ["Quote, newsletter, footer, SEO (A-46\u2013A-50)", 45, 50],
  ["Structure, navigation and conversion (A-51\u2013A-58)", 50, 58],
];
for (const [label, from, to] of A_GROUPS) {
  bodyChildren.push(h2(label));
  bodyChildren.push(...renderItems(A.slice(from, to)));
}

// 4. Part B
bodyChildren.push(h1("4. Part B \u2014 Services hub (16 items)"));
bodyChildren.push(body(
  "The hub carries the site\u2019s best written sections (the ladder, the operating contract) and its weakest first impression (a bureaucratic H1 over stock art, then a chart whose slices carry no information)."
));
bodyChildren.push(...renderItems(B));

// 5. Part C
bodyChildren.push(h1("5. Part C \u2014 Eight expertise hubs (50 items)"));
bodyChildren.push(body(
  "C-01 and C-02 apply to all eight hubs; the remaining 48 items are hub-specific, six per domain, quoting each hub\u2019s actual copy."
));
bodyChildren.push(h2("Shared across all eight hubs (C-01\u2013C-02)"));
bodyChildren.push(...renderItems(C.slice(0, 2)));
const C_HUBS = [
  ["Agentic AI & Hyperautomation hub (C-03\u2013C-08)", 2, 8],
  ["Applied AI & Generative AI hub (C-09\u2013C-14)", 8, 14],
  ["Blockchain & Digital Trust hub (C-15\u2013C-20)", 14, 20],
  ["Cloud, Edge & Platform Engineering hub (C-21\u2013C-26)", 20, 26],
  ["Cybersecurity & Zero-Trust hub (C-27\u2013C-32)", 26, 32],
  ["Data, Analytics & Lakehouse hub (C-33\u2013C-38)", 32, 38],
  ["IoT, Digital Twin & Robotics hub (C-39\u2013C-44)", 38, 44],
  ["Quantum & Advanced Compute hub (C-45\u2013C-50)", 44, 50],
];
for (const [label, from, to] of C_HUBS) {
  bodyChildren.push(h2(label));
  bodyChildren.push(...renderItems(C.slice(from, to)));
}

// 6. Part D
bodyChildren.push(h1("6. Part D \u2014 The 54 practice pages (146 items)"));
bodyChildren.push(h2("6.1 Systemic patterns (D-S01\u2013D-S38)"));
bodyChildren.push(body(
  "These 38 items apply across the inner-page population; the evidence counts state exactly how many pages each pattern touches. Fixing them is mostly generator and component work \u2014 one fix removes the symptom from dozens of pages."
));
bodyChildren.push(...renderItems(DS));
bodyChildren.push(h2("6.2 Page-specific items (D-P01\u2013D-P108, two per page)"));
bodyChildren.push(body(
  "Every practice page receives two bespoke items: one that rewrites or re-aims its hero, and one that adds the page-specific proof artifact it currently lacks (a worked case, a walkthrough, a redacted template). These are the items that make no two pages read alike."
));
for (const [label, items] of dpGroupsExact) {
  bodyChildren.push(h2(label));
  bodyChildren.push(...renderItems(items));
}

// 7. Part E
bodyChildren.push(h1("7. Part E \u2014 Global and cross-cutting (20 items)"));
bodyChildren.push(body(
  "These items span the whole site: trust fixes (provenance, the LIVE VIEW badge, the footer claim), accessibility and layout defects seen during the walkthrough (marquee duplication, cookie overlay), and the guardrail item that prevents every sameness pattern from returning."
));
bodyChildren.push(...renderItems(E));

// 8. Rollout
bodyChildren.push(h1("8. Rollout plan and acceptance criteria"));
bodyChildren.push(body(
  "The register is sequenced into five waves. Wave 0 installs the trust fixes and the automated content lint, because every later wave depends on being able to prove that sameness and unproven numbers cannot return. Waves 1\u20134 then execute the register top-down. No work outside this register starts until each wave\u2019s acceptance criteria pass."
));
bodyChildren.push(tableTitle("Table 3 \u2014 Waves, scope and acceptance"));
bodyChildren.push(makeTable(
  ["Wave", "Scope", "Items", "Acceptance criteria"],
  [
    ["0", "Guards and trust: E-20 lint; E-01, E-03, E-04, E-06 page fixes; provenance convention (E-05)", "6",
      "Build fails on empty arch subs/edges and duplicated openers; no LIVE VIEW badge; provenance chips on all numeric panels; cookie banner never overlays content"],
    ["1", "Homepage: all A items in priority order", "58",
      "Hero states buyer+proof in \u226430 words; evidence grid \u2265\u00d93 cards with filters; stats reconciled; sticky section nav live"],
    ["2", "Hub + eight expertise hubs: B and C items", "66",
      "New hub H1s live; hub narratives differ section-by-section; pairing cards present on all 8 hubs"],
    ["3", "Inner pages systemic: D-S items", "38",
      "4 page archetypes in rotation; every node sub and edge label filled; persona line, fit/no-fit and effort anchor on all 54 pages"],
    ["4", "Inner pages bespoke: D-P items, 8 domain batches", "108",
      "All 108 artifacts live (worked cases, redacted templates, timelines); no two sibling pages share hero structure"],
  ],
  [10, 38, 10, 42]
));
bodyChildren.push(body(
  "Estimation note: Waves 0\u20132 are primarily component and copy work on 9 distinct pages and can complete in one editing pass each. Wave 3 is generator-level work across 54 pages and should be executed archetype by archetype. Wave 4 is genuine editorial authorship \u2014 108 bespoke artifacts \u2014 and is the long pole; it is batched by domain so each domain\u2019s pages ship together and can be reviewed against their hub.", { after: 200 }
));

// ── Footers ──
function numFooter() {
  return new Footer({
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ children: [PageNumber.CURRENT], size: 18, color: P.secondary, font: EN })],
    })],
  });
}
function docHeader() {
  return new Header({
    children: [new Paragraph({
      alignment: AlignmentType.RIGHT,
      border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: P.table.innerLine, space: 4 } },
      children: [new TextRun({ text: "Achala IT Solutions \u2014 Homepage & Services Content Audit", size: 16, color: P.secondary, font: EN })],
    })],
  });
}

// ── Front matter (TOC) ──
const frontMatter = [
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { before: 480, after: 360 },
    children: [new TextRun({ text: "Table of Contents", bold: true, size: 32, font: EN, color: P.primary })],
  }),
  new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-2" }),
  new Paragraph({
    spacing: { before: 200 },
    children: [new TextRun({
      text: "Note: This Table of Contents is generated via field codes. To ensure page number accuracy after editing, please right-click the TOC and select \u201cUpdate Field.\u201d",
      italics: true, size: 18, color: "888888", font: EN,
    })],
  }),
  // no trailing PageBreak: the body starts in its own NEXT_PAGE section
];

// ── Document ──
const doc = new Document({
  creator: "Achala IT Solutions",
  title: "Homepage & Services Content Audit \u2014 Change Register",
  styles: {
    default: {
      document: {
        run: { font: EN, size: 22, color: P.body },
        paragraph: { spacing: { line: 312 } },
      },
      heading1: {
        run: { font: EN, size: 32, bold: true, color: P.primary },
        paragraph: { spacing: { before: 400, after: 160, line: 312 } },
      },
      heading2: {
        run: { font: EN, size: 26, bold: true, color: P.primary },
        paragraph: { spacing: { before: 300, after: 120, line: 312 } },
      },
    },
  },
  sections: [
    { // cover
      properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 0, bottom: 0, left: 0, right: 0 } } },
      children: buildCoverR2({
        title: "Homepage & Services Content Audit",
        subtitle: "A user-eye walkthrough of the homepage and all 63 Services pages \u2014 with 290 numbered changes",
        englishLabel: "CHANGE REGISTER",
        metaLines: [
          "290 change items \u00b7 42 P1 must-fix",
          "Homepage \u00b7 Services hub \u00b7 8 expertise hubs \u00b7 54 practice pages",
          "Phase 3 review gate \u2014 for approval before implementation",
        ],
        footerRight: "Achala IT Solutions \u00b7 November 2026",
      }),
    },
    { // front matter
      properties: {
        type: SectionType.NEXT_PAGE,
        page: {
          size: { width: 11906, height: 16838 },
          margin: { top: 1440, bottom: 1440, left: 1701, right: 1417 },
          pageNumbers: { start: 1, formatType: NumberFormat.UPPER_ROMAN },
        },
      },
      headers: { default: docHeader() },
      footers: { default: numFooter() },
      children: frontMatter,
    },
    { // body
      properties: {
        type: SectionType.NEXT_PAGE,
        page: {
          size: { width: 11906, height: 16838 },
          margin: { top: 1440, bottom: 1440, left: 1701, right: 1417 },
          pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL },
        },
      },
      headers: { default: docHeader() },
      footers: { default: numFooter() },
      children: bodyChildren,
    },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  const out = "/home/z/my-project/download/Achala_Content_Audit_Change_Register.docx";
  fs.writeFileSync(out, buf);
  console.log("written", out, (buf.length / 1024).toFixed(1) + " KB");
  const total = A.length + B.length + C.length + DS.length + DP.length + E.length;
  console.log("items:", { A: A.length, B: B.length, C: C.length, DS: DS.length, DP: DP.length, E: E.length, total });
});
