# Achala IT Solutions — Corporate Website

The full public website for **www.achalasolutions.com** — a 633-page, Fortune-100-grade
static-first platform built from the approved content package (223,751 words of
industry- and service-aligned deep-technology copy).

**Stack**: Next.js 16 (App Router, TypeScript, static export) · Tailwind CSS 4 ·
shadcn/ui primitives · Pagefind static search · self-hosted Sora/Inter fonts.

---

## What is inside

| | |
|---|---|
| Pages | 633 content pages (home, 8 service towers, 54 services, 12 industries, 48 sub-industries, 336 capability pages, 24 solutions, 8 platforms ×3, 36 case studies, insights, company, leadership, partners, careers, newsroom, contact, legal) |
| Navigation | 4-level mega menu (Services / Industries / Solutions / Platforms / Insights / About) + mobile drawer |
| SEO | Per-page SEO title + meta description, canonical URLs, Open Graph/Twitter cards, JSON-LD (Organization, WebSite, BreadcrumbList, Service, Article, NewsArticle, ProfilePage), auto sitemap.xml + robots.txt |
| Search | Pagefind static index generated on every export (`/search`) |
| Conversion | Sitewide footer contact form + full contact/briefing/value-assessment pages, honeypot spam protection, GDPR-aligned cookie consent |
| Link graph | 0 broken internal links, 0 orphan pages — verified at build time by the content exporter |

## Quick start

```bash
bun install
bun run dev        # develop at localhost:3000
bun run lint       # eslint
bun run export     # static export -> ./out (run "npx serve out" to preview)
```

## Configuration (`.env`)

Copy `.env.example` to `.env`:

- `NEXT_PUBLIC_SITE_URL` — canonical site URL (default https://www.achalasolutions.com)
- `NEXT_PUBLIC_FORM_ACCESS_KEY` — Web3Forms access key; without it the contact
  form runs in demo mode (success state, no delivery). Get a free key at
  web3forms.com; submissions are delivered to your inbox (info@achalasolutions.com).
- `NEXT_PUBLIC_GA_ID` — GA4 measurement id, loaded only after cookie consent.

## Deploy

**GitHub Pages (included)** — the repository ships with
`.github/workflows/deploy-pages.yml`. Push to `main`, enable
*Settings → Pages → Source: GitHub Actions*. The workflow runs the static
export (639 files incl. sitemap/robots/search index) and deploys `out/`.

**Vercel / Netlify** — import the repo; build command `bun run export`,
output directory `out`.

**cPanel / any static host** — run `bun run export` locally, upload the
contents of `out/` to `public_html/`. The site is pure static files; forms
keep working through the Web3Forms endpoint.

## Editing content

Content lives in `src/content/` as structured JSON (one file per page plus
`index.json`, `nav.json`, `brand.json`). Edit a page JSON, and the page,
its metadata, sitemap entry and search index all update on the next build.

To regenerate the whole content set from the source data modules:

```bash
cd scripts/achalasolutions
python3 dqs_site_export.py     # emits src/content/* (633 pages) and verifies the link graph
```

## Placeholders to replace before launch

These are marked in the content and must be swapped for real data:

1. **Leadership names** (8 profiles under `/leadership/…`) — the names shown
   are placeholders (`placeholder: true` in JSON); replace name + biography.
2. **Contact emails** — `info@ / press@ / careers@achalasolutions.com` are set as
   the documented inboxes; confirm they exist.
3. **Partner alliance pages** (`/partner-ecosystem/…`) — written as
   *alliance status: in validation*; upgrade copy + logos after legal
   verification of each partnership.
4. **Legal pages** — verified text note included; final review by counsel.
5. **Form endpoint + GA4 id** — set in `.env`.
6. **Logo** — the site ships with a clean vector logomark
   (`src/components/site/Logo.tsx` + `src/app/icon.svg`); swap with the
   official brand asset when available.

## Site architecture

```
src/app/[[...slug]]/page.tsx   — renders all 633 routes from content JSON
src/app/page.tsx               — (removed; home handled by catch-all, slug=[])
src/components/site/           — header/mega-menu, footer+form, templates, SEO pieces
src/lib/content.ts             — server-side content layer
src/content/                   — index.json + 633 page JSONs + nav.json + brand.json
scripts/achalasolutions/             — content source modules + exporter (Python)
.github/workflows/             — GitHub Pages deploy
```
