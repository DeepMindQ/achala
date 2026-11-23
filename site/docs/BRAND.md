# Achala IT Solutions Brand Rules

Sampled directly from the supplied `achala_logo.png` (Wave 1, CHG-023/041).

## Palette

| Token | Hex | Use |
|---|---|---|
| `brand` | `#d20000` | Primary accent: primary buttons, kickers, active states, key metrics, stat values. Keep to ~10% of any view. |
| `brand-hover` | `#a80000` | Button hover state. |
| `brand-deep` | `#8f0000` | Small orange text and inline links on white (≈4.6:1, AA). |
| `brand-300` | `#ff9d96` | Orange text on navy surfaces (AA-safe at small sizes). |
| `brand-tint` | `#fdecec` | Soft backgrounds, hover washes, callout fills. |
| `navy-950/900/800/700/600/500` | `#0e2230` → `#568aa6` | All dark surfaces: hero bands, CTA bands, footer, table headers, glass cards. |
| `mist` / `line` | `#F6F7FB` / `#E5E7F0` | Alternating light sections; hairlines and card borders. |
| `slate-body` | `#46425A` | Body text on white. |

**Prohibited legacy tokens:** cyan `#22D3EE`, deep cyan `#1B6B7A`, teal `#0E7490`, gray-ink `#0A1424` family. Zero tolerance (CHG-038).

## Logo

- Authentic lockup, vectorized 1:1 from the PNG: orange block with white lowercase
  `achala` + navy lowercase `software` whose `o` is the red dot. Lowercase always.
- Variants: **full** on light, **reversed** (white wordmark, orange block intact) on navy,
  **mono navy** for print/legal. Component: `src/components/site/Logo.tsx`.
- Assets: `/logo.svg`, `/logo-white.svg`, `/logo-mono.svg`, `logo-512.png`,
  `logo-white-512.png`, favicon `/icon.svg` + `/favicon.ico` + `apple-touch-icon.png`.
- Clearspace: equal to the orange block height on all sides. Minimum width 120px.

## Logo misuse — do-not list

1. Never recolor the orange block or wordmark.
2. Never stretch, squash or rotate the mark.
3. Never add drop shadows, outlines or gradients to the mark.
4. Never use cyan/teal variants.
5. Never redraw the letterforms — use the traced SVG paths only.
6. Never place the full-color lockup on navy (use the reversed variant).

## Pairing matrix (CHG-037)

| Pairing | Verdict |
|---|---|
| White label on orange button (semibold 13px+) | Approved |
| Navy text on orange tint background | Approved |
| Orange on navy — large text/UI only (values 22px+ bold) | Approved |
| Orange small text on white | Prohibited — use `brand-deep #8f0000` |
| Orange small text on navy | Use `brand-300 #ff9d96` |
