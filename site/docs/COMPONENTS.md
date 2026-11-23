# Component Usage

Wave 1 design-system reference (CHG-098). Site components live in `src/components/site/`.

## Utilities (globals.css)

| Class | Purpose |
|---|---|
| `.container-dq` | 1280px container with fluid gutters 20–40px — replaces `max-w-7xl px-6`. |
| `.section-y` / `.section-y-sm` | Responsive section rhythm (80–144px / 56–96px). |
| `.text-display-1/2/3`, `.text-body-lg` | Fluid type scale (clamp). |
| `.grad-navy-field`, `.grad-orange-glow`, `.grad-sweep` | Sanctioned gradients — no ad-hoc gradients. |
| `.dot-grid`, `.dot-grid-light`, `.pattern-hatch`, `.pattern-mesh`, `.pattern-noise` | Dark/light band textures. |
| `.kicker-bar` / `.kicker-bar-dark` | 24×3px orange rule above kickers — the brand motif. |
| `.nav-link` | Header items: sliding orange underline on hover, persistent when `data-active="true"`. |
| `.link-animated` | Inline links: animated underline on hover. |
| `.btn-sheen` | Light sweep across primary buttons on hover (disabled under reduced motion). |
| `.shadow-1/2/3` | Navy-tinted elevation tokens. |
| `.measure` | 68ch prose measure. |

## Components

- **`Logo`** — `variant`: `full` (light) | `reversed` (navy) | `mono` (print/legal). `height` prop, default 38. Hover: red dot bounce (reduced-motion safe).
- **`Reveal`** — scroll-triggered fade-up; `delay` prop staggers grids.
- **`SiteHeader`** — navy-900 utility bar, orange CTA with sheen, mega panel with navy-tinted elevation.
- **`SiteFooter`** — navy gradient, contact band + form, newsletter slot, reversed lockup in legal bar, social icon row.
- **`NewsletterForm`** — email capture with success state; posts to web3forms when `NEXT_PUBLIC_FORM_ACCESS_KEY` is set.
- **`ContactForm`** — input system: labels, orange focus ring, custom select arrow, orange checkbox accent, honeypot, error/success states.
- **`CookieConsent`** — navy card with orange accept / ghost secondary.
- **`PagePieces`** — `Breadcrumbs` (chevrons, deep-path truncation), `PageHero` (navy field + orange glow + fluid h1), `Blocks` (prose/bullets/tables/notes/CTA), `CtaBand` v2, `CardGrid`, `RelatedRail`, `StatsStrip` (tabular-nums), `ContentPage` (universal template).
- **`/style-guide`** — hidden route rendering all tokens and components (not indexed).
