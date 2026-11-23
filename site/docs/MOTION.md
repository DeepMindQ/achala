# Achala IT Solutions — Motion Specification (Wave 2, CHG-101/171)

Motion tokens live in `globals.css` (`--dur-1`, `--dur-2`, `--ease-out`,
`--ease-spring`). Every animation on the site resolves through these rules:

1. **Duration budget** — micro-interactions ≤ 300 ms; entrances 500–900 ms;
   hero choreography ≤ 1.4 s total; marquee is ambient (42 s loop).
2. **Easing** — entrances use `cubic-bezier(.22,1,.36,1)` (decelerate);
   springy pops use `--ease-spring`; loops use `linear` or `ease-in-out`.
3. **Transforms only** — every animation drives `transform` / `opacity` /
   `stroke-dashoffset`. No layout properties (`top/left/width/height`) are
   animated, keeping the compositor at 60 fps (CHG-158/172).
4. **Reduced-motion kill switch** (CHG-157) — a single
   `@media (prefers-reduced-motion: reduce)` block zeroes every entrance,
   loop and marquee. Verified against: `.rise-item`, `.rise-word`,
   `.quote-mark`, `.footer-stagger`, `.bg-field-drift`, `.bg-glow-pulse`,
   `.animate-float`, `.marquee-inner`, `.text-shimmer`, `.skeleton-shimmer`,
   `.drawer-slide`, and the inline SVG draw transitions in DataVisuals
   (JS checks `matchMedia` before animating count-ups).
5. **Scroll trigger discipline** (CHG-155/156/159) — one IntersectionObserver
   per component, fires once, disconnects on reveal, `rootMargin -40px…-60px`
   so entrances start slightly before full visibility.
6. **Hydration safety** — CountUp and every chart render the final value /
   geometry server-side; animation is a post-mount enhancement only.

## Library map

| Utility | File | Covers |
| --- | --- | --- |
| `Reveal` (IO wrapper) | `Reveal.tsx` | CHG-121 staggered grid reveals |
| `CountUp`, `ScrollProgress`, `BackToTop`, `Marquee`, `useInView` | `Motion.tsx` | CHG-105/118/120/124/125/126 |
| `DataVisuals` (Bar/Line/Donut/Radar/Funnel/Network/Heatmap/Gauge/Sparkline/Flow/WorldPins) | `DataVisuals.tsx` | CHG-178/223 + output graphs |
| Hero choreography (`.rise-word`, `.rise-item`) | `globals.css` | CHG-102/103/104/149 |
| Background field (`.bg-field-drift`, `.bg-glow-pulse`) | `globals.css` | CHG-106/107 |
| Quote scale-in, footer stagger, drawer slide, tick draw, shimmer | `globals.css` | CHG-137/141/143/165/168 |
| Page-seeded telemetry + patent strips | `PageAugment.tsx` | output-graphs directive |

## Deterministic data contract

Chart data is generated server-side from `page.id` seeds
(`mulberry32(hashStr(id))` in `src/lib/seeded.ts`). Server and client always
agree, so there are no hydration mismatches, and every page shows stable,
page-unique illustrative telemetry.
