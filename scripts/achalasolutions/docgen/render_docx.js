/* Achala IT Solutions — docx renderer (volumes + blueprint).
   Follows docx skill: cover recipes R1/R2 (DM-1 palette), calcTitleLayout/calcCoverSpacing,
   3-section page numbering, TOC rules, table cross-page control, WPS-safe patterns. */

const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, PageNumber, NumberFormat, AlignmentType, HeadingLevel,
  WidthType, BorderStyle, ShadingType, TableOfContents, PageBreak,
  SectionType, TableLayoutType,
} = require("docx");
const fs = require("fs");

// ---------- palette (DM-1 Deep Cyan — AI/tech) ----------
const PAL = {
  bg: "162235", accent: "37DCF2",
  cover: { titleColor: "FFFFFF", subtitleColor: "B0B8C0", metaColor: "90989F", footerColor: "687078" },
  table: { headerBg: "1B6B7A", headerText: "FFFFFF", accentLine: "1B6B7A", innerLine: "C8DDE2", surface: "EDF3F5" },
  h1: "162235", h2: "1B6B7A", h3: "1B6B7A", body: "000000",
};
const FONT = { ascii: "Times New Roman", eastAsia: "SimSun" };
const allNoBorders = {
  top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE },
  left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE },
  insideHorizontal: { style: BorderStyle.NONE }, insideVertical: { style: BorderStyle.NONE },
};
const noBorders = {
  top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE },
  left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE },
};

// ---------- title layout helpers (skill-mandated) ----------
function textWidthUnits(title) {
  // CJK chars count double vs ASCII
  let u = 0;
  for (const ch of title) u += /[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]/.test(ch) ? 2 : 1;
  return u;
}
function splitTitleLines(title, charsPerLine) {
  if (textWidthUnits(title) <= charsPerLine) return [title];
  const breakAfter = new Set([..."\uFF0C\u3002\u3001\uFF1B\uFF1A\uFF01\uFF1F", ..."-_\u2014\u2013\u00B7/", ..." \t"]);
  const lines = [];
  let remaining = title;
  const widthTo = (s, n) => {
    let u = 0, i = 0;
    for (const ch of s) { u += /[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]/.test(ch) ? 2 : 1; if (u >= n) return i + 1; i++; }
    return s.length;
  };
  while (textWidthUnits(remaining) > charsPerLine) {
    let breakAt = -1;
    const limitIdx = widthTo(remaining, charsPerLine);
    for (let i = limitIdx; i >= Math.floor(limitIdx * 0.6); i--) {
      if (i > 0 && i <= remaining.length && breakAfter.has(remaining[i - 1])) { breakAt = i; break; }
    }
    if (breakAt === -1) {
      const fwd = Math.min(remaining.length, Math.ceil(limitIdx * 1.3));
      for (let i = limitIdx + 1; i < fwd; i++) {
        if (breakAfter.has(remaining[i - 1])) { breakAt = i; break; }
      }
    }
    if (breakAt === -1) breakAt = Math.max(1, limitIdx);
    lines.push(remaining.slice(0, breakAt).trim());
    remaining = remaining.slice(breakAt).trim();
  }
  if (remaining) lines.push(remaining);
  if (lines.length > 1 && lines[lines.length - 1].length <= 2) {
    const last = lines.pop();
    lines[lines.length - 1] += last;
  }
  return lines;
}
function calcTitleLayout(title, maxWidthTwips, preferredPt = 40, minPt = 24) {
  const unitW = (pt) => pt * 10; // ASCII-dominant width per unit (CJK counts 2 units)
  let titlePt = preferredPt, lines;
  while (titlePt >= minPt) {
    const cpl = Math.floor(maxWidthTwips / unitW(titlePt));
    if (cpl < 4) { titlePt -= 2; continue; }
    lines = splitTitleLines(title, cpl);
    if (lines.length <= 3) break;
    titlePt -= 2;
  }
  if (!lines || lines.length > 3) {
    lines = splitTitleLines(title, Math.floor(maxWidthTwips / unitW(minPt)));
    titlePt = minPt;
  }
  return { titlePt, titleLines: lines };
}
function calcCoverSpacing(params) {
  const { titleLineCount = 1, titlePt = 36, hasSubtitle = false, hasEnglishLabel = false,
          metaLineCount = 0, fixedHeight = 800, pageHeight = 16838, marginTop = 0, marginBottom = 0 } = params;
  const SAFETY = 1200;
  const usableHeight = pageHeight - marginTop - marginBottom - SAFETY;
  const titleHeight = titleLineCount * (titlePt * 23 + 200);
  const subtitleHeight = hasSubtitle ? (12 * 23 + 600) : 0;
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
  return { topSpacing, midSpacing: Math.max(safeRemaining - topSpacing - bottomSpacing, 0), bottomSpacing };
}

// ---------- cover recipe R1 (volumes) ----------
function buildCoverR1(config) {
  const P = { bg: PAL.bg, ...PAL.cover, accent: PAL.accent };
  const padL = 1200, padR = 800;
  const availableWidth = 11906 - padL - padR - 300;
  const { titlePt, titleLines } = calcTitleLayout(config.title, availableWidth, 40, 24);
  const titleSize = titlePt * 2;
  const spacing = calcCoverSpacing({
    titleLineCount: titleLines.length, titlePt,
    hasSubtitle: !!config.subtitle, hasEnglishLabel: !!config.label,
    metaLineCount: (config.metaLines || []).length, fixedHeight: 400,
  });
  const accentLeft = { style: BorderStyle.SINGLE, size: 8, color: P.accent, space: 12 };
  const children = [];
  children.push(new Paragraph({ spacing: { before: spacing.topSpacing } }));
  if (config.label) {
    children.push(new Paragraph({
      indent: { left: padL, right: padR }, spacing: { after: 500 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: P.accent, space: 8 } },
      children: [new TextRun({ text: config.label.split("").join("  "), size: 18, color: P.accent,
        font: { ascii: "Arial", eastAsia: "SimHei" }, characterSpacing: 40 })],
    }));
  }
  for (let i = 0; i < titleLines.length; i++) {
    children.push(new Paragraph({
      indent: { left: padL },
      spacing: { after: i < titleLines.length - 1 ? 100 : 300, line: Math.ceil(titlePt * 23), lineRule: "atLeast" },
      children: [new TextRun({ text: titleLines[i], size: titleSize, bold: true,
        color: P.titleColor, font: { eastAsia: "SimHei", ascii: "Arial" } })],
    }));
  }
  if (config.subtitle) {
    children.push(new Paragraph({
      indent: { left: padL, right: padR }, spacing: { after: 800, line: 320, lineRule: "atLeast" },
      children: [new TextRun({ text: config.subtitle, size: 24, color: P.subtitleColor,
        font: { eastAsia: "Microsoft YaHei", ascii: "Arial" } })],
    }));
  }
  for (const line of (config.metaLines || [])) {
    children.push(new Paragraph({
      indent: { left: padL + 200 }, spacing: { after: 80 },
      border: { left: accentLeft },
      children: [new TextRun({ text: line, size: 22, color: P.metaColor,
        font: { eastAsia: "Microsoft YaHei", ascii: "Arial" } })],
    }));
  }
  children.push(new Paragraph({ spacing: { before: spacing.bottomSpacing } }));
  children.push(new Paragraph({
    indent: { left: padL, right: padR },
    border: { top: { style: BorderStyle.SINGLE, size: 2, color: P.accent, space: 8 } },
    spacing: { before: 200 },
    children: [
      new TextRun({ text: config.footerLeft || "", size: 16, color: P.footerColor, font: { ascii: "Arial" } }),
      new TextRun({ text: "                                        ", size: 16, color: P.footerColor }),
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
        shading: { type: ShadingType.CLEAR, fill: P.bg }, borders: noBorders,
        children,
      })],
    })],
  })];
}

// ---------- cover recipe R2 (blueprint) ----------
function buildCoverR2(config) {
  const P = { bg: PAL.bg, ...PAL.cover, accent: PAL.accent };
  const padL = 1400, padR = 1400;
  const { titlePt, titleLines } = calcTitleLayout(config.title, 11906 - padL - padR, 40, 24);
  const titleSize = titlePt * 2;
  const thickBorder = { style: BorderStyle.SINGLE, size: 18, color: P.accent, space: 20 };
  const children = [];
  children.push(new Paragraph({
    indent: { left: padL - 400, right: padR - 400 }, spacing: { before: 1200, after: 200 },
    border: { top: thickBorder }, children: [],
  }));
  children.push(new Paragraph({ spacing: { before: 1400 } }));
  if (config.label) {
    children.push(new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { after: 500 },
      children: [new TextRun({ text: config.label.split("").join("  "), size: 18, color: P.accent,
        font: { ascii: "Calibri" }, characterSpacing: 40 })],
    }));
  }
  for (let i = 0; i < titleLines.length; i++) {
    children.push(new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: i < titleLines.length - 1 ? 80 : 300, line: Math.ceil(titlePt * 23), lineRule: "atLeast" },
      children: [new TextRun({ text: titleLines[i], size: titleSize, bold: true,
        color: P.titleColor, font: { eastAsia: "SimHei", ascii: "Arial" } })],
    }));
  }
  if (config.subtitle) {
    children.push(new Paragraph({
      alignment: AlignmentType.CENTER, indent: { left: padL - 600, right: padR - 600 },
      spacing: { after: 400, line: 320, lineRule: "atLeast" },
      children: [new TextRun({ text: config.subtitle, size: 24, color: P.subtitleColor,
        font: { eastAsia: "Microsoft YaHei", ascii: "Arial" } })],
    }));
  }
  children.push(new Paragraph({ spacing: { before: 1000 } }));
  for (const line of (config.metaLines || [])) {
    children.push(new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 100, line: Math.ceil(14 * 23), lineRule: "atLeast" },
      children: [new TextRun({ text: line, size: 28, color: P.metaColor,
        font: { eastAsia: "Microsoft YaHei", ascii: "Arial" } })],
    }));
  }
  children.push(new Paragraph({ spacing: { before: 1600 } }));
  children.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    indent: { left: padL - 400, right: padR - 400 }, spacing: { before: 200 },
    border: { bottom: thickBorder },
    children: [new TextRun({ text: config.footerRight || "", size: 18, color: P.footerColor, font: { ascii: "Arial" } })],
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

// ---------- body block builders ----------
function h1(text, pageBreakBefore) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1, pageBreakBefore: !!pageBreakBefore,
    spacing: { before: 240, after: 160, line: 340, lineRule: "atLeast" },
    children: [new TextRun({ text, bold: true, size: 30, color: PAL.h1, font: { ascii: "Arial", eastAsia: "SimHei" } })],
  });
}
function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 280, after: 120, line: 320, lineRule: "atLeast" },
    children: [new TextRun({ text, bold: true, size: 26, color: PAL.h2, font: { ascii: "Arial", eastAsia: "SimHei" } })],
  });
}
function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 200, after: 100 },
    children: [new TextRun({ text, bold: true, size: 24, color: PAL.h3, font: { ascii: "Arial", eastAsia: "SimHei" } })],
  });
}
function bodyP(text) {
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { line: 312, after: 140 },
    children: [new TextRun({ text, size: 22, color: PAL.body, font: FONT })],
  });
}
function heroP(text) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    indent: { left: 240 },
    border: { left: { style: BorderStyle.SINGLE, size: 12, color: PAL.table.accentLine, space: 10 } },
    spacing: { line: 330, after: 200, before: 60 },
    children: [new TextRun({ text, italics: true, size: 24, color: PAL.h2, font: FONT })],
  });
}
function ctaP(text) {
  return new Paragraph({
    indent: { left: 240 },
    shading: { type: ShadingType.CLEAR, fill: PAL.table.surface },
    border: { left: { style: BorderStyle.SINGLE, size: 12, color: PAL.table.accentLine, space: 10 } },
    spacing: { line: 312, before: 220, after: 160 },
    children: [new TextRun({ text: "CTA — " + text, bold: true, size: 22, color: PAL.h1, font: FONT })],
  });
}
function noteP(text) {
  return new Paragraph({
    spacing: { line: 280, before: 120, after: 120 },
    children: [new TextRun({ text: "Note: " + text, italics: true, size: 18, color: "888888", font: FONT })],
  });
}
function bulletP(label, text) {
  const runs = [];
  if (label && text) {
    runs.push(new TextRun({ text: label + " — ", bold: true, size: 22, color: PAL.h1, font: FONT }));
    runs.push(new TextRun({ text, size: 22, color: PAL.body, font: FONT }));
  } else {
    runs.push(new TextRun({ text: String(label || text || ""), size: 22, color: PAL.body, font: FONT }));
  }
  return new Paragraph({
    bullet: { level: 0 },
    alignment: AlignmentType.JUSTIFIED,
    spacing: { line: 312, after: 80 },
    children: runs,
  });
}
function caption(text) {
  return new Paragraph({
    keepNext: true,
    spacing: { before: 200, after: 80 },
    children: [new TextRun({ text, bold: true, size: 20, color: PAL.h2, font: FONT })],
  });
}
function mkCell(text, opts) {
  const o = opts || {};
  return new TableCell({
    width: { size: o.w || 50, type: WidthType.PERCENTAGE },
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    shading: o.fill ? { type: ShadingType.CLEAR, fill: o.fill } : undefined,
    children: [new Paragraph({
      alignment: AlignmentType.LEFT,
      spacing: { line: 264 },
      children: [new TextRun({ text: String(text), bold: !!o.bold, size: o.size || 18,
        color: o.color || PAL.body, font: FONT })],
    })],
  });
}
function mkTable(headers, rows) {
  const n = headers.length;
  const w = Math.floor(100 / n);
  const widths = headers.map((_, i) => (i === 0 ? Math.max(w, 18) : Math.floor((100 - Math.max(w, 18)) / (n - 1))));
  const headerRow = new TableRow({
    tableHeader: true, cantSplit: true,
    children: headers.map((htext, i) => mkCell(htext, { w: widths[i], fill: PAL.table.headerBg, color: PAL.table.headerText, bold: true })),
  });
  const dataRows = rows.map((r, ri) => new TableRow({
    cantSplit: true,
    children: r.map((cell, ci) => mkCell(cell, { w: widths[ci], fill: ri % 2 === 0 ? undefined : PAL.table.surface })),
  }));
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 4, color: PAL.table.accentLine },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: PAL.table.accentLine },
      left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 1, color: PAL.table.innerLine },
      insideVertical: { style: BorderStyle.NONE },
    },
    rows: [headerRow, ...dataRows],
  });
}
function metaBox(page) {
  const rows = [
    ["URL path", page.url || "—"],
    ["Breadcrumb", page.breadcrumb || "—"],
    ["Template", page.template || "—"],
    ["SEO title", page.seo_title || "—"],
    ["Meta description", page.meta_description || "—"],
    ["Draft words", String(page.words || 0)],
  ];
  const headerRow = new TableRow({
    tableHeader: true, cantSplit: true,
    children: [mkCell("Page metadata", { w: 22, fill: PAL.table.headerBg, color: PAL.table.headerText, bold: true }),
               mkCell("Value", { w: 78, fill: PAL.table.headerBg, color: PAL.table.headerText, bold: true })],
  });
  const dataRows = rows.map(([k, v]) => new TableRow({
    cantSplit: true,
    children: [mkCell(k, { w: 22, bold: true, color: PAL.h2, size: 16 }), mkCell(v, { w: 78, size: 16 })],
  }));
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 2, color: PAL.table.innerLine },
      bottom: { style: BorderStyle.SINGLE, size: 2, color: PAL.table.innerLine },
      left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 1, color: PAL.table.innerLine },
      insideVertical: { style: BorderStyle.NONE },
    },
    rows: [headerRow, ...dataRows],
  });
}

function renderBlocks(blocks) {
  const out = [];
  for (const b of blocks) {
    if (b.t === "h2") out.push(h2(b.x));
    else if (b.t === "h3") out.push(h3(b.x));
    else if (b.t === "p") out.push(bodyP(b.x));
    else if (b.t === "hero") out.push(heroP(b.x));
    else if (b.t === "cta") out.push(ctaP(b.x));
    else if (b.t === "note") out.push(noteP(b.x));
    else if (b.t === "bullets") for (const it of b.items) out.push(bulletP(it[0], it[1]));
    else if (b.t === "table") {
      out.push(caption(b.caption));
      out.push(mkTable(b.headers, b.rows));
      out.push(new Paragraph({ spacing: { after: 120 }, children: [] }));
    }
  }
  return out;
}

// ---------- document assembly ----------
function pageNumFooter() {
  return new Footer({
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "888888", font: FONT })],
    })],
  });
}
function docHeader(text) {
  return new Header({
    children: [new Paragraph({
      alignment: AlignmentType.RIGHT,
      border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: PAL.table.innerLine, space: 4 } },
      children: [new TextRun({ text, size: 14, color: "999999", font: FONT })],
    })],
  });
}

async function main() {
  const [jsonPath, outPath] = process.argv.slice(2);
  const doc = JSON.parse(fs.readFileSync(jsonPath, "utf-8"));
  const isBlueprint = doc.volume === "BLUEPRINT";
  const coverCfg = isBlueprint ? doc.cover : {
    label: "ACHALA SOFT — WEBSITE CONTENT PACKAGE",
    title: doc.volume_title.split("—").slice(1).join("—").trim() || doc.volume_title,
    subtitle: "Full page copy for www.achalasolutions.com — prepared for the web design & development team",
    metaLines: [
      doc.volume_title,
      doc.pages.length + " web pages of content in this volume",
      "Blocks render in order; each page opens with its metadata box",
      "November 2026",
    ],
    footerLeft: "Achala IT Solutions Corporation",
    footerRight: doc.volume,
  };

  // body children
  const bodyChildren = [];
  doc.pages.forEach((page, idx) => {
    bodyChildren.push(h1(page.title, idx > 0));
    if (!isBlueprint && page.url) {
      bodyChildren.push(metaBox(page));
      bodyChildren.push(new Paragraph({ spacing: { after: 120 }, children: [] }));
    }
    bodyChildren.push(...renderBlocks(page.blocks));
  });

  const tocTitle = new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 480, after: 360 },
    children: [new TextRun({ text: "Table of Contents", bold: true, size: 32, color: PAL.h1, font: { ascii: "Arial", eastAsia: "SimHei" } })],
  });
  const tocRange = doc.toc_range || (doc.pages.length > 40 ? "1-1" : "1-2");
  const tocEl = new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: tocRange });
  const tocHint = new Paragraph({
    spacing: { before: 200 },
    children: [new TextRun({
      text: "Note: This Table of Contents is generated via field codes. To ensure page number accuracy after editing, please right-click the TOC and select \u201CUpdate Field.\u201D",
      italics: true, size: 18, color: "888888", font: FONT })],
  });
  // NOTE: no PageBreak after TOC — body starts in its own NEXT_PAGE section
  // (a trailing PageBreak + section break would produce a blank page)

  const pgSize = { width: 11906, height: 16838 };
  const pgMargin = { top: 1440, bottom: 1440, left: 1701, right: 1417 };

  const d = new Document({
    creator: "Z.ai",
    styles: {
      default: {
        document: {
          run: { font: FONT, size: 22, color: PAL.body },
          paragraph: { spacing: { line: 312 } },
        },
        heading1: {
          run: { font: { ascii: "Arial", eastAsia: "SimHei" }, size: 30, bold: true, color: PAL.h1 },
          paragraph: { spacing: { before: 240, after: 160, line: 340 }, outlineLevel: 0 },
        },
        heading2: {
          run: { font: { ascii: "Arial", eastAsia: "SimHei" }, size: 26, bold: true, color: PAL.h2 },
          paragraph: { spacing: { before: 280, after: 120, line: 320 }, outlineLevel: 1 },
        },
        heading3: {
          run: { font: { ascii: "Arial", eastAsia: "SimHei" }, size: 24, bold: true, color: PAL.h3 },
          paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 2 },
        },
      },
    },
    sections: [
      { // Section 1: cover — margin 0, no page numbers
        properties: { page: { size: pgSize, margin: { top: 0, bottom: 0, left: 0, right: 0 } } },
        children: isBlueprint ? buildCoverR2(coverCfg) : buildCoverR1(coverCfg),
      },
      { // Section 2: front matter — Roman numerals
        properties: {
          type: SectionType.NEXT_PAGE,
          page: { size: pgSize, margin: pgMargin, pageNumbers: { start: 1, formatType: NumberFormat.UPPER_ROMAN } },
        },
        footers: { default: pageNumFooter() },
        children: [tocTitle, tocEl, tocHint],
      },
      { // Section 3: body — Arabic from 1
        properties: {
          type: SectionType.NEXT_PAGE,
          page: { size: pgSize, margin: pgMargin, pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL } },
        },
        headers: { default: docHeader("Achala IT Solutions — " + (isBlueprint ? "Website Blueprint" : doc.volume_title)) },
        footers: { default: pageNumFooter() },
        children: bodyChildren,
      },
    ],
  });

  const buf = await Packer.toBuffer(d);
  fs.writeFileSync(outPath, buf);
  console.log("WROTE", outPath, (buf.length / 1024 / 1024).toFixed(2) + " MB");
}
main().catch(e => { console.error(e); process.exit(1); });
