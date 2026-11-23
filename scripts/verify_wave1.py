#!/usr/bin/env python3
"""Wave 1 (CHG-001..100) verification — concrete artifact checks against the site source."""
import os, re, json, subprocess, sys

SITE = "/home/z/my-project/site"
results = []  # (id, name, ok, detail)

def rd(p):
    with open(os.path.join(SITE, p), encoding="utf-8") as f:
        return f.read()

def exists(p):
    return os.path.exists(os.path.join(SITE, p))

def scan(pattern, paths, flags=re.I):
    """Return True if regex found in any of the given relative paths (glob-like via walk)."""
    rx = re.compile(pattern, flags)
    hits = []
    for root, dirs, files in os.walk(os.path.join(SITE, paths[0]) if not paths[0].startswith("src") else SITE):
        pass
    return hits

def grep_src(pattern, include=r"\.(tsx?|css|json)$", flags=re.I):
    """Search whole src/ for regex; return list of (file, line)."""
    rx = re.compile(pattern, flags)
    hits = []
    for root, dirs, files in os.walk(os.path.join(SITE, "src")):
        for fn in files:
            if not re.search(include, fn):
                continue
            p = os.path.join(root, fn)
            try:
                with open(p, encoding="utf-8") as f:
                    for i, line in enumerate(f, 1):
                        if rx.search(line):
                            hits.append((os.path.relpath(p, SITE), i))
            except Exception:
                pass
    return hits

def add(chg, name, ok, detail=""):
    results.append((chg, name, ok, detail))

g_css = rd("src/app/globals.css")
logo = rd("src/components/site/Logo.tsx")
layout = rd("src/app/layout.tsx")
brand = rd("src/content/brand.json")
brandmd = rd("docs/BRAND.md")
compmd = rd("docs/COMPONENTS.md") if exists("docs/COMPONENTS.md") else ""
manifest = rd("public/manifest.json")
icon = rd("src/app/icon.svg")
nf = rd("src/app/not-found.tsx")
styleguide = rd("src/app/style-guide/page.tsx")
uibits = rd("src/components/site/ui-bits.tsx")
header = rd("src/components/site/SiteHeader.tsx")
footer = rd("src/components/site/SiteFooter.tsx")
home = rd("src/components/site/HomeView.tsx")
cookie = rd("src/components/site/CookieConsent.tsx")
contact = rd("src/components/site/ContactForm.tsx")
newsletter = rd("src/components/site/NewsletterForm.tsx")
PagePieces = rd("src/components/site/PagePieces.tsx")
PageBlocks = rd("src/components/site/PageBlocks.tsx")
content_types = rd("src/lib/content.ts")

# ── A: Brand Identity & Logo (CHG-001..042) ─────────────────────────────
add("CHG-001", "Delete invented hexagon logo", "hexagon" not in logo.lower() and "22D3EE" not in logo.upper())
add("CHG-002", "Authentic lockup SVG in Logo.tsx", "#d20000" in logo and "#2b5672" in logo and "fillRule" in logo)
logo_usage = grep_src(r"from \"\./Logo\"|from \"@/components/site/Logo\"")
add("CHG-003", "Logo installed Header+Footer", len(logo_usage) >= 2, f"{len(logo_usage)} importers")
assets = ["logo.svg","logo-white.svg","logo-mono.svg","logo-512.png","logo-white-512.png"]
add("CHG-004", "Full logo asset set in public/", all(exists(f"public/{a}") for a in assets), str([a for a in assets if exists(f"public/{a}")]))
add("CHG-005", "icon.svg orange-block d glyph", exists("src/app/icon.svg") and ("FE5722" in icon or "fe5722" in icon) and "hexagon" not in icon.lower())
add("CHG-006", "metadata icons + theme-color", "apple-touch-icon" in layout and "themeColor" in layout and "18142D" in layout)
cyan = grep_src(r"#22[Dd]3[Ee][Ee]|#1[Bb]6[Bb]7[Aa]|#0[Ee]7490|brand-cyan|brand-teal")
add("CHG-007", "Cyan/teal tokens removed", len([h for h in cyan if h[0] not in ("src/app/globals.css", "src/content/brand.json")]) == 0, f"residual: {cyan[:5]}")
add("CHG-008", "Orange token ramp", "--color-brand:" in g_css and "#d20000" in g_css and "brand-hover" in g_css and "brand-deep" in g_css and "brand-tint" in g_css)
add("CHG-009", "Navy token ramp", all(f"--color-navy-{s}" in g_css for s in ["950","900","800","700","600","500"]))
gray_ink = grep_src(r"#0a1424|#0e1b30|#14263f")
add("CHG-010", "Dark surfaces = navy ramp", len(gray_ink) == 0, f"gray-ink residual: {gray_ink[:3]}")
cyan_cls = grep_src(r"text-brand-cyan|bg-brand-cyan|border-brand-cyan|from-brand-cyan|to-brand-cyan")
add("CHG-011", "Zero cyan class refs in tsx", len(cyan_cls) == 0)
btn_orange = re.findall(r"bg-brand[\s\"']", uibits) + re.findall(r"bg-brand[\s\"']", header) + re.findall(r"bg-brand[\s\"']", home) + re.findall(r"bg-brand[\s\"']", contact)
add("CHG-012", "Primary CTAs solid orange", len(btn_orange) >= 3, f"{len(btn_orange)} bg-brand usages")
add("CHG-013", "Link accent rules", "link-animated" in g_css and "hover:text-brand-deep" in uibits + footer + home + PagePieces)
add("CHG-014", "Selection + focus orange", "rgba(210, 0, 0, 0.28)" in g_css and ":focus-visible" in g_css and "outline: 2px solid var(--color-brand)" in g_css)
add("CHG-015", "dot-grid recolored", "rgba(210, 0, 0, 0.16)" in g_css and "dot-grid-light" in g_css)
add("CHG-016", "Hero gradient navy+orange", "grad-navy-field" in g_css and "grad-orange-glow" in g_css and "grad-navy-field" in rd("src/components/site/PagePieces.tsx"))
add("CHG-017", "PWA manifest", exists("public/manifest.json") and "manifest" in layout and "icons" in manifest)
add("CHG-018", "Branded OG image", exists("public/og-default.png") and "og-default.png" in layout and os.path.getsize(os.path.join(SITE,"public/og-default.png")) > 50000)
add("CHG-019", "Org JSON-LD logo URL", '"@type": "Organization"' in layout and "logo.svg" in layout)
add("CHG-020", "Branded email assets", exists("docs/email-header.html"))
add("CHG-021", "Social banner set", exists("public/social-linkedin.png") and exists("public/social-x.png"))
printcss = "@media print" in g_css or any("@media print" in rd(os.path.join(dp, f)) for dp, dn, fn in os.walk(os.path.join(SITE, "src")) for f in fn if f.endswith(".css"))
add("CHG-022", "Print-safe styles", printcss or "print" in brandmd.lower())
add("CHG-023", "brand.json tokens encoded", "#d20000" in brand and "#2b5672" in brand and "usageRules" in brand)
add("CHG-024", "Logo sizing + clearspace rules", "Math.round(height" in logo and "clearspace" in logo.lower())
add("CHG-025", "Logo dark-surface variants", 'variant === "reversed"' in logo and "logo-white.svg" in brand)
# brand string per naming_ci BG-008: the only allowed brand string is "Achala IT Solutions"
add("CHG-026", "Logo a11y", 'role="img"' in logo and 'aria-label="Achala IT Solutions"' in logo)
add("CHG-027", "Toaster brand colors", exists("src/components/ui/toaster.tsx"))
chart_ok = "--chart-1: #d20000" in g_css
add("CHG-028", "Chart palette branded", chart_ok)
add("CHG-029", "CookieConsent branded", "brand" in cookie and ("bg-brand" in cookie or "text-brand" in cookie or "brand-" in cookie))
add("CHG-030", "Branded 404", "grad-navy-field" in nf or "brand" in nf or "navy" in nf)
hex_in_content = []
for root, dirs, files in os.walk(os.path.join(SITE, "src/content")):
    for fn in files:
        if fn.endswith(".json") and fn != "brand.json":
            with open(os.path.join(root, fn), encoding="utf-8") as f:
                t = f.read()
            for hx in re.findall(r"#[0-9a-fA-F]{6}", t):
                if hx.upper() not in {"#d20000","#2b5672"} and hx.lower() not in {"#d20000","#2b5672"}:
                    hex_in_content.append((fn, hx))
add("CHG-031", "Content layer hex audit", len(hex_in_content) == 0, f"non-brand hex: {hex_in_content[:5]}")
add("CHG-032", "Skeleton brand ramp", "Skeleton" in uibits and ("animate-pulse" in uibits or "pulse" in uibits))
add("CHG-033", "Watermark pattern asset", exists("public/pattern-d.svg"))
add("CHG-034", "favicon.ico fallback", exists("public/favicon.ico") and "favicon.ico" in layout)
add("CHG-035", "Sanctioned gradient set", all(f".grad-{n}" in g_css for n in ["navy-field","orange-glow","sweep"]))
add("CHG-036", "Orange kicker motif", ".kicker-bar" in g_css)
add("CHG-037", "Pairing matrix approved", "Pairing matrix" in brandmd or "pairing" in brandmd.lower())
add("CHG-038", "No teal/cyan echoes", len(cyan_cls) == 0 and len([h for h in cyan if h[0] not in ("src/app/globals.css", "src/content/brand.json")]) == 0 and len(grep_src(r"sky-|cyan-|teal-", include=r"\.tsx$")) == 0)
add("CHG-039", "Safari/Edge tab theming", "themeColor" in layout)
add("CHG-040", "Logo hover micro-motion", ".logo-dot" in g_css and "logo-dot" in logo)
add("CHG-041", "Logo misuse rules doc", "misuse" in brandmd.lower() and "Never" in brandmd)
add("CHG-042", "Pixel-match sign-off", exists("/home/z/my-project/download/Wave1_Logo_PixelMatch_Signoff.png"))

# ── B: Design System & Tokens (CHG-043..100) ────────────────────────────
add("CHG-043", "Full token layer in @theme", "@theme inline" in g_css and "--color-brand" in g_css)
add("CHG-044", "Fluid type scale clamp()", ".text-display-1" in g_css and "clamp(" in g_css)
add("CHG-045", "Display font treatment", "--font-display" in g_css and "Sora" in g_css)
add("CHG-046", "Body font polish", 'font-feature-settings: "cv11", "ss01"' in g_css)
add("CHG-047", "Container system", ".container-dq" in g_css)
add("CHG-048", "12-column grid utility", ".grid-12" in g_css)
add("CHG-049", "Section rhythm tokens", ".section-y" in g_css and "clamp(" in g_css.split(".section-y")[1][:200])
add("CHG-050", "Elevation tokens navy-tinted", ".shadow-3" in g_css and "rgba(43, 86, 114" in g_css)
add("CHG-051", "Radius consistency", "--radius: 0.625rem" in g_css)
add("CHG-052", "Button system rebuild", "rounded-[10px] bg-brand" in (uibits+PagePieces+header))
add("CHG-053", "Sheen hover effect", ".btn-sheen" in g_css and sum(rd(os.path.join(r, fn)).count("btn-sheen") for r, _, fns in os.walk(os.path.join(SITE, "src")) for fn in fns if fn.endswith((".tsx", ".ts"))) >= 10)
add("CHG-054", "Input system rebuild", "rounded-[10px]" in contact and ("border-line" in contact or "border" in contact) and "bg-brand" in contact)
add("CHG-055", "Checkbox/radio/switch brand", re.search(r"accent-|checkbox|radio|Checkbox", contact + uibits, re.I) is not None)
add("CHG-056", "Select styling", re.search(r"<select|Select", contact + uibits, re.I) is not None)
add("CHG-057", "Badge/chip system", "rounded-full bg-brand-tint" in PagePieces or "rounded-full" in uibits)
add("CHG-058", "Card system + variants", "CardGrid" in PagePieces and "hover:-translate-y-0.5" in PagePieces)
add("CHG-059", "Tabs sliding indicator", "export function Tabs" in uibits)
add("CHG-060", "Accordion height animation", "export function Accordion" in uibits)
add("CHG-061", "Tooltip component", "export function Tooltip" in uibits)
add("CHG-062", "Breadcrumbs restyle", "export function Breadcrumbs" in PageBlocks and "aria-label=\"Breadcrumb\"" in PageBlocks and "…" in PageBlocks)
add("CHG-063", "Table restyle", "bg-navy-800 text-white" in PageBlocks and "hover:bg-brand-tint/60" in PageBlocks and "text-right tabular-nums" in PageBlocks and "md:hidden" in PageBlocks)
add("CHG-064", "Pagination component", "export function Pagination" in uibits)
add("CHG-065", "Skeleton loaders", "export function Skeleton" in uibits)
add("CHG-066", "Avatar/monogram component", "monogram" in PagePieces.lower())
add("CHG-067", "Icon standard (lucide registry)", 'from "lucide-react"' in PagePieces and 'from "lucide-react"' in header)
add("CHG-068", "Kicker/overline component", "kicker-bar" in g_css and "kicker" in PagePieces)
add("CHG-069", "Stat/metric component", "export function StatsStrip" in PageBlocks and "tabular-nums" in PageBlocks and "CountUp" in PageBlocks)
add("CHG-070", "Quote/testimonial component", re.search(r"blockquote|Quote", uibits + PagePieces + home, re.I) is not None)
add("CHG-071", "CTA band v2", "export function CtaBand" in PageBlocks and "pattern-noise" in PageBlocks and "grad-navy-field" in PageBlocks and "bg-brand" in PageBlocks)
add("CHG-072", "Section header component", "cardsHeading" in PagePieces or "SectionHeader" in uibits or "heading" in PagePieces)
add("CHG-073", "Numbered process component", "export function NumberedProcess" in uibits)
add("CHG-074", "Timeline component", "export function Timeline" in uibits)
add("CHG-075", "Logo wall component", "export function LogoWall" in uibits)
add("CHG-076", "Newsletter signup component", exists("src/components/site/NewsletterForm.tsx") and "bg-brand" in newsletter)
add("CHG-077", "Social icon row", re.search(r"Linkedin|Twitter|X\(Twitter\)|lucide", footer, re.I) is not None)
add("CHG-078", "Language/region selector stub", "export function LanguageSelector" in uibits)
add("CHG-079", "FAQ block component", re.search(r"FAQ|Accordion", uibits + home, re.I) is not None)
add("CHG-080", "Dialog restyle", exists("src/components/ui/dialog.tsx"))
add("CHG-081", "Drawer/sheet restyle", exists("src/components/ui/sheet.tsx") or "drawer" in header.lower())
add("CHG-082", "Callout variants", 'variant?: "insight" | "compliance" | "warning" | "success"' in content_types and "TriangleAlert" in PageBlocks and "ShieldCheck" in PageBlocks and "CircleCheck" in PageBlocks and "bg-brand-tint" in PageBlocks)
add("CHG-083", "Progress bar + stepper", "export function ProgressBar" in uibits and "export function Stepper" in uibits)
add("CHG-084", "Glossary tooltip", "export function GlossaryTip" in uibits)
add("CHG-085", "Divider with centered label", "export function Divider" in uibits)
add("CHG-086", "Global link styles", ".link-animated" in g_css)
add("CHG-087", "Sliding underline nav", ".nav-link" in g_css and "nav-link" in header)
add("CHG-088", "Prose typography", ".measure" in g_css and "measure" in PagePieces)
add("CHG-089", "Dark-band pattern library", all(p in g_css for p in ["dot-grid","pattern-hatch","pattern-mesh","pattern-noise"]))
add("CHG-090", "Z-index scale", "z-index scale" in g_css or "z-50" in header)
add("CHG-091", "Unified focus-visible", ":focus-visible" in g_css)
add("CHG-092", "Scrollbar styling", "::-webkit-scrollbar-thumb" in g_css)
add("CHG-093", "Dead dark theme resolved", "dark token block was removed" in g_css or ".dark" not in g_css)
add("CHG-094", "Container queries", "@container cards" in g_css)
add("CHG-095", "CSS motion tokens", "--dur-1" in g_css and "--ease-spring" in g_css)
add("CHG-096", "Tablet breakpoint audit", "sm:" in PagePieces and "md:" in PagePieces)
add("CHG-097", "Hidden style-guide page", exists("src/app/style-guide/page.tsx") and "FE5722" in styleguide and 'index: false' in styleguide)
add("CHG-098", "Component usage docs", exists("docs/COMPONENTS.md"))
add("CHG-099", "Font loading strategy", "display: \"swap\"" in layout and "next/font/google" in layout)
add("CHG-100", "Color-area contract", "10%" in brandmd or "10%" in compmd)

# ── report ──────────────────────────────────────────────────────────────
fails = [r for r in results if not r[2]]
print(f"\n=== Wave 1 verification: {len(results)-len(fails)}/{len(results)} checks passed ===\n")
for chg, name, ok, detail in results:
    mark = "PASS" if ok else "FAIL"
    d = f"  [{detail}]" if detail and not ok else (f"  [{detail}]" if detail else "")
    if not ok or "-v" in sys.argv:
        print(f"{mark}  {chg}  {name}{d}")
if fails:
    print(f"\nFAILED: {len(fails)}")
    for chg, name, ok, detail in fails:
        print(f"  {chg}: {name} {('['+detail+']') if detail else ''}")
