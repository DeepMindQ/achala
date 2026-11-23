import Link from "next/link";
import Image from "next/image";
import { ArrowRight, ArrowUpRight, ChevronRight, CircleCheck, Info, Layers, Cog, Factory, FileBarChart2, BookOpen, Boxes, Building2, Compass, UserRound, Mail, Scale, Briefcase, Newspaper, Wrench, MapPin, Handshake, ShieldCheck, TriangleAlert } from "lucide-react";
import Reveal from "./Reveal";
import { CountUp } from "./Motion";
import { pick as pickImagery } from "./PageImagery";
import { TechDiagram, DIAGRAM_KINDS, type DiagramKind } from "./TechDiagrams";
import { ArchGraph, MetricsDash, ChartPanel } from "./ArchDash";
import { DashSuite } from "./DashSuite";
import { ServiceIndustryExplorer } from "./ServiceIndustryExplorer";
import type { Block, Card, Crumb, PageData } from "@/lib/content";

/* ── PageBlocks — browser-safe presentational pieces.
   Split out of PagePieces so client components (CaseStudies) can import
   them without dragging the server-side content layer into the bundle.
   PagePieces re-exports everything below, so existing imports keep working. */
/* ── Breadcrumbs (CHG-062): chevrons, deep-path truncation, orange current ── */
export function Breadcrumbs({ crumbs, dark = false }: { crumbs: Crumb[]; dark?: boolean }) {
  // deep capability paths (4+ levels): keep first + last two, collapse the middle
  const truncated = crumbs.length > 4;
  const shown = truncated
    ? [crumbs[0], { name: "…", url: undefined } as Crumb, ...crumbs.slice(-2)]
    : crumbs;
  return (
    <nav aria-label="Breadcrumb" className={`text-[12px] ${dark ? "text-white/55" : "text-slate-body/60"}`}>
      <ol className="flex flex-wrap items-center gap-x-1 gap-y-1">
        {shown.map((c, i) => {
          const last = i === shown.length - 1;
          const collapsed = c.name === "…" && truncated;
          const label = (
            <span
              className={
                last
                  ? dark
                    ? "text-brand-300 font-medium"
                    : "text-brand-deep font-medium"
                  : undefined
              }
            >
              {c.name}
            </span>
          );
          return (
            <li key={`${c.name}-${i}`} className="flex items-center gap-1">
              {c.url && !last ? (
                <Link href={c.url} className={`hover:underline ${dark ? "hover:text-white/85" : "hover:text-navy-800"}`}>
                  {label}
                </Link>
              ) : (
                label
              )}
              {!last && <ChevronRight aria-hidden="true" className="h-3 w-3 opacity-40" />}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}

/* ── Template kicker icon + v2 hero chrome (CHG-288/289/290/344) ─────── */
const KICKER_ICON: Record<string, React.ComponentType<{ className?: string }>> = {
  expertise_hub: Layers,
  service_page: Cog,
  industry_hub: Factory,
  subindustry_page: Factory,
  industry_capability: Wrench,
  sub_capability: Wrench,
  solution_page: Handshake,
  platform_overview: Boxes,
  platform_architecture: ShieldCheck,
  platform_usecases: MapPin,
  case_study: FileBarChart2,
  insight_article: BookOpen,
  insights_category: BookOpen,
  company_page: Building2,
  approach_page: Compass,
  legal_page: Scale,
  contact_page: Mail,
  leadership_profile: UserRound,
  partner_page: Handshake,
  careers_page: Briefcase,
  newsroom_article: Newspaper,
};

/* Template-specific secondary hero CTA (CHG-290); empty = hide CTAs */
function heroSecondaryCta(page: PageData): { label: string; url: string } | null {
  switch (page.template) {
    case "case_study":
      return { label: "Run the same diagnostic", url: "/value-assessment/" };
    case "insight_article":
    case "newsroom_article":
      return { label: "Discuss with the practice lead", url: "/contact/" };
    case "careers_page":
      return { label: "See open positions", url: "/careers/open-positions/" };
    case "platform_architecture":
      return { label: "Talk to the platform team", url: "/contact/" };
    default:
      return { label: "Request a Value Assessment", url: "/value-assessment/" };
  }
}
const NO_HERO_CTA = new Set(["contact_page", "legal_page", "leadership_profile", "search_page"]);

/* Per-template micro-chips shown ON the hero image (wave-2 hero redesign).
   Two short, factual lines — never repeated copy, just template semantics. */
const HERO_CHIP: Record<string, { head: string; sub: string }> = {
  expertise_hub: { head: "8 services · 2 platforms", sub: "Expertise evidence pack" },
  service_page: { head: "Baseline → audited delta", sub: "Weekly evidence cadence" },
  sub_capability: { head: "Composable delivery", sub: "Signed baseline metric" },
  industry_capability: { head: "Sector-calibrated", sub: "Regime-aware controls" },
  subindustry_page: { head: "Workflow-level scope", sub: "Five priority capabilities" },
  industry_hub: { head: "8 capability lanes", sub: "Regulatory posture mapped" },
  solution_page: { head: "Composed architecture", sub: "Named prerequisites" },
  platform_overview: { head: "Production rails", sub: "Deployment under NDA" },
  platform_architecture: { head: "Three-plane design", sub: "Audit evidence ready" },
  platform_usecases: { head: "Proven scenarios", sub: "Reference flows" },
  case_study: { head: "Baseline audited", sub: "Method under NDA" },
  insight_article: { head: "Field-tested practice", sub: "No vendor theater" },
  newsroom_article: { head: "Company release", sub: "Press contact inside" },
  company_page: { head: "Operating detail", sub: "Named owners" },
  approach_page: { head: "Method, not slideware", sub: "Gates that bind" },
  partner_page: { head: "Certified delivery", sub: "Joint reference stack" },
  leadership_profile: { head: "Practice leader", sub: "Direct line to team" },
  careers_page: { head: "Hiring now", sub: "Human process" },
  legal_page: { head: "Plain-language terms", sub: "Effective date inside" },
  contact_page: { head: "Named inboxes", sub: "Response within 1 business day" },
};

/* ── Split hero v3 (wave-2): copy left, live visual INSIDE the title block ──
   The image is no longer a detached figure under the band — it is a framed
   panel of the hero grid itself, with beam sweep, telemetry chip and ring. */
export function PageHero({
  page,
  kicker,
  lede,
  children,
}: {
  page: PageData;
  kicker?: string;
  lede?: string;
  children?: React.ReactNode;
}) {
  const intro =
    lede ??
    (page.blocks.find((b) => b.t === "hero") as { x: string } | undefined)?.x ??
    page.blocks.find((b) => b.t === "p")?.x ??
    "";
  const Icon = KICKER_ICON[page.template];
  const secondary = heroSecondaryCta(page);
  const chips = [page.l1, page.l2, page.l3].filter(Boolean) as string[];
  const showVisual = page.url !== "/search" && page.url !== "/style-guide";
  const im = showVisual ? pickImagery(page) : null;
  const chip = page.hero_chip ?? HERO_CHIP[page.template];
  const priority = page.template === "expertise_hub" || page.template === "industry_hub";
  return (
    <section className="dq-hero relative overflow-hidden grad-navy-field text-white">
      <div className="absolute inset-0 dot-grid" aria-hidden="true" />
      <div className="absolute inset-0 grad-orange-glow" aria-hidden="true" />
      <div className="relative container-dq pb-12 pt-10 sm:pb-16 sm:pt-14">
        <div className="hero-stagger grid gap-8 lg:grid-cols-[minmax(0,1fr)_minmax(0,30rem)] lg:items-center lg:gap-12">
          {/* left column — the copy */}
          <div className="min-w-0">
            <Breadcrumbs crumbs={page.crumbs} dark />
            <div className="measure mt-6">
              {kicker && (
                <p className="kicker-bar-dark flex items-center gap-2 text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-300">
                  {Icon && <Icon className="h-4 w-4" aria-hidden="true" />}
                  {kicker}
                </p>
              )}
              <h1 data-split className="text-display-2 mt-2 max-w-3xl text-white">{page.title}</h1>
              {intro && <p className="mt-4 text-[15px] leading-relaxed text-white/70">{intro}</p>}
            </div>
            {chips.length > 0 && (
              <div className="mt-5 flex flex-wrap items-center gap-2">
                {chips.map((c, i) => (
                  <span
                    key={c + i}
                    className="rounded-full border border-white/15 bg-white/[0.06] px-3 py-1 text-[11px] font-medium text-white/70"
                  >
                    {c}
                  </span>
                ))}
                {page.template === "case_study" && (
                  <span className="rounded-full border border-brand/40 bg-brand/15 px-3 py-1 text-[11px] font-semibold text-brand-300">
                    Identity withheld · Baseline audited · Method under NDA
                  </span>
                )}
              </div>
            )}
            {children}
            {!NO_HERO_CTA.has(page.template) && (
              <div className="mt-7 flex flex-wrap gap-3">
                <Link
                  href="/book-a-briefing/"
                  className="btn-sheen inline-flex items-center gap-2 rounded-[10px] bg-brand px-5 py-2.5 text-[13px] font-semibold text-white transition hover:bg-brand-hover"
                >
                  Book a 45-minute briefing <ArrowRight className="h-4 w-4" />
                </Link>
                {secondary && (
                  <Link
                    href={secondary.url}
                    className="inline-flex items-center rounded-[10px] border border-white/25 px-5 py-2.5 text-[13px] font-medium text-white/85 transition hover:border-brand-300 hover:text-brand-300"
                  >
                    {secondary.label}
                  </Link>
                )}
              </div>
            )}
          </div>

          {/* right column — the visual, INSIDE the title block */}
          {im && (
            <figure className="hv-figure group relative m-0 aspect-[16/11] w-full overflow-hidden rounded-2xl border border-white/15 bg-navy-900 shadow-3 lg:aspect-[4/3]">
              <Image
                src={im.src}
                alt={im.alt}
                fill
                sizes="(max-width: 1024px) 100vw, 480px"
                className="object-cover hv-img"
                priority={priority}
              />
              {/* legibility + brand grading */}
              <div aria-hidden="true" className="pointer-events-none absolute inset-0 bg-gradient-to-t from-navy-950/85 via-navy-950/15 to-transparent" />
              <div aria-hidden="true" className="pointer-events-none absolute inset-0 grad-orange-glow-soft opacity-60 mix-blend-screen" />
              {/* animated beam sweep */}
              <div aria-hidden="true" className="hv-beam pointer-events-none absolute inset-0 overflow-hidden">
                <span />
              </div>
              {/* corner brackets */}
              <svg aria-hidden="true" className="pointer-events-none absolute inset-0 h-full w-full text-brand-300/70" viewBox="0 0 100 100" preserveAspectRatio="none">
                <path d="M3 12 V3 H12" fill="none" stroke="currentColor" strokeWidth="0.8" vectorEffect="non-scaling-stroke" />
                <path d="M88 3 H97 V12" fill="none" stroke="currentColor" strokeWidth="0.8" vectorEffect="non-scaling-stroke" />
                <path d="M97 88 V97 H88" fill="none" stroke="currentColor" strokeWidth="0.8" vectorEffect="non-scaling-stroke" />
                <path d="M12 97 H3 V88" fill="none" stroke="currentColor" strokeWidth="0.8" vectorEffect="non-scaling-stroke" />
              </svg>
              {/* template badge — top right */}
              {kicker && (
                <figcaption className="absolute right-3 top-3 rounded-full border border-white/20 bg-navy-950/55 px-3 py-1 text-[10px] font-semibold uppercase tracking-[0.16em] text-white/80 backdrop-blur-sm">
                  {kicker}
                </figcaption>
              )}
              {/* telemetry chip — bottom left, rises on hover */}
              {chip && (
                <div className="hv-chip absolute bottom-3 left-3 rounded-xl border border-white/15 bg-navy-950/65 px-3.5 py-2.5 backdrop-blur-md">
                  <p className="text-[12.5px] font-semibold leading-none text-white">{chip.head}</p>
                  <p className="mt-1 flex items-center gap-1.5 text-[10.5px] leading-none text-brand-300">
                    <span className="hv-pulse inline-block h-1.5 w-1.5 rounded-full bg-brand" aria-hidden="true" />
                    {chip.sub}
                  </p>
                </div>
              )}
              <div aria-hidden="true" className="pointer-events-none absolute inset-0 rounded-2xl ring-1 ring-inset ring-white/10" />
            </figure>
          )}
        </div>
      </div>
    </section>
  );
}

/* ── Block renderer ───────────────────────────────────────────────────── */
export function Blocks({ blocks, skip = [] }: { blocks: Block[]; skip?: string[] }) {
  const out: React.ReactNode[] = [];
  let h2Index = 0;
  for (const b of blocks) {
    if (skip.includes(b.t)) continue;
    if (b.t === "p") {
      out.push(
        <Reveal key={`p-${out.length}`}>
          <p className="measure text-[15px] leading-[1.8] text-slate-body">{b.x}</p>
        </Reveal>,
      );
    } else if (b.t === "diagram") {
      out.push(
        <TechDiagram
          key={`d-${out.length}`}
          kind={(DIAGRAM_KINDS as string[]).includes(b.kind) ? (b.kind as DiagramKind) : "pipeline"}
          labels={b.labels}
          note={b.note}
          title={b.title}
        />,
      );
    } else if (b.t === "arch") {
      out.push(
        <ArchGraph
          key={`a-${out.length}`}
          title={b.title}
          lanes={b.lanes}
          nodes={b.nodes}
          edges={b.edges}
          badges={b.badges}
          note={b.note}
        />,
      );
    } else if (b.t === "chart") {
      out.push(
        <ChartPanel
          key={`ch-${out.length}`}
          title={b.title}
          variant={(b.variant as "line" | "bar" | "radar") || "line"}
          cats={b.cats}
          series={b.series}
          unit={b.unit}
          yMax={b.yMax}
          note={b.note}
          caption={b.caption}
        />,
      );
    } else if (b.t === "dash") {
      out.push(
        <MetricsDash
          key={`m-${out.length}`}
          title={b.title}
          kpis={b.kpis}
          gates={b.gates}
          log={b.log}
          caption={b.note}
        />,
      );
    } else if (b.t === "explorer") {
      out.push(
        <ServiceIndustryExplorer
          key={`x-${out.length}`}
          title={b.title}
          intro={b.intro}
          service={b.service}
          practiceNote={b.practiceNote}
          industries={b.industries}
        />,
      );
    } else if (b.t === "idash") {
      out.push(
        <DashSuite
          key={`i-${out.length}`}
          title={b.title}
          badge={b.badge}
          kpis={b.kpis}
          tabs={b.tabs}
          note={b.note}
        />,
      );
    } else if (b.t === "h2") {
      h2Index += 1;
      const anchorId = `sec-${h2Index}`;
      const h2b = b as { t: "h2"; x: string; sub?: string };
      out.push(
        <Reveal key={`h2-${h2Index}`}>
          <h2
            id={anchorId}
            className="dq-h2 group measure mt-12 flex scroll-mt-28 items-baseline gap-3 font-display text-[22px] font-semibold text-navy-800 sm:text-[24px]"
          >
            {h2b.x}
          </h2>
          {h2b.sub && (
            <p className="measure mt-2 border-l-2 border-brand/40 pl-3 text-[13.5px] leading-relaxed text-slate-body/70">
              {h2b.sub}
            </p>
          )}
        </Reveal>,
      );
    } else if (b.t === "h3") {
      out.push(
        <Reveal key={`h3-${out.length}`}>
          <h3 className="measure mt-7 font-display text-[16.5px] font-semibold text-navy-800">{b.x}</h3>
        </Reveal>,
      );
    } else if (b.t === "bullets") {
      if (!b.items || b.items.length === 0) continue; // never render empty card grids
      out.push(
        <Reveal key={`b-${out.length}`}>
          <ul data-stagger className="mt-5 grid gap-3 sm:grid-cols-2">
            {b.items.map(([title, desc], i) => (
              <li
                key={i}
                className="card-sheen tilt-card group rounded-xl border border-line bg-white p-4 transition hover:-translate-y-0.5 hover:border-brand/50 shadow-1 hover:shadow-2"
              >
                <p className="text-[13.5px] font-semibold text-navy-800">{title}</p>
                <p className="mt-1 text-[12.5px] leading-relaxed text-slate-body/80">{desc}</p>
              </li>
            ))}
          </ul>
        </Reveal>,
      );
    } else if (b.t === "table") {
      // CHG-063: numeric columns right-aligned with tabular figures; two-column
      // tables collapse to stacked cards on mobile instead of horizontal scroll.
      const numericCol = b.headers.map((_, ci) =>
        ci > 0 &&
        b.rows.length > 0 &&
        b.rows.every((r) => r[ci] === undefined || r[ci] === "" || /^[\s]*[+\-−−]?[$€₹£]?[\d.,]+[\s%°]?\S*\s*$/.test(r[ci] ?? "")),
      );
      const twoCol = b.headers.length === 2;
      const cellAlign = (ci: number) => (numericCol[ci] ? "text-right tabular-nums" : "text-left");
      out.push(
        <Reveal key={`t-${out.length}`}>
          <figure className="mt-8 overflow-hidden rounded-xl border border-line shadow-1">
            {b.caption && (
              <figcaption className="border-b border-line bg-mist px-4 py-3 text-[13px] font-semibold text-navy-800">
                {b.caption}
              </figcaption>
            )}
            <div className={twoCol ? "hidden md:block" : "overflow-x-auto"}>
              <table className={`w-full ${twoCol ? "" : "min-w-[480px]"} text-left text-[13px]`}>
                <thead>
                  <tr className="bg-navy-800 text-white">
                    {b.headers.map((h, ci) => (
                      <th key={h} className={`px-4 py-2.5 font-semibold ${cellAlign(ci)}`}>
                        {h}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {b.rows.map((row, ri) => (
                    <tr key={ri} className={ri % 2 ? "bg-mist/60" : "bg-white hover:bg-brand-tint/60"}>
                      {row.map((cell, ci) => (
                        <td
                          key={ci}
                          className={`px-4 py-2.5 align-top ${cellAlign(ci)} ${
                            ci === 0
                              ? "sticky left-0 bg-inherit font-semibold text-navy-800 min-w-[132px]"
                              : "text-slate-body/85"
                          }`}
                        >
                          {cell}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {twoCol && (
              <div className="md:hidden">
                {b.rows.map((row, ri) => (
                  <div
                    key={ri}
                    className={`flex items-baseline justify-between gap-4 px-4 py-3 ${ri % 2 ? "bg-mist/60" : "bg-white"}`}
                  >
                    <span className="text-[13px] font-semibold text-navy-800">{row[0]}</span>
                    <span className={`text-[13px] ${numericCol[1] ? "text-right tabular-nums" : "text-right"} ${
                      numericCol[1] ? "text-navy-800" : "text-slate-body/85"
                    }`}>
                      {row[1]}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </figure>
        </Reveal>,
      );
    } else if (b.t === "note") {
      // CHG-082: four callout variants replace the single note style —
      // insight (orange, default) · compliance (navy) · warning (amber) · success (green)
      const v = b.variant ?? "insight";
      const skin = {
        insight: "border border-brand/30 bg-brand-tint text-slate-body/90",
        compliance: "border border-navy-800/25 bg-[#EEF0F7] text-slate-body/90",
        warning: "border border-amber-600/35 bg-amber-50 text-slate-body/90",
        success: "border border-emerald-700/35 bg-emerald-50 text-slate-body/90",
      }[v];
      const Icon =
        v === "compliance" ? ShieldCheck : v === "warning" ? TriangleAlert : v === "success" ? CircleCheck : Info;
      const iconColor =
        v === "compliance" ? "text-navy-800" : v === "warning" ? "text-amber-700" : v === "success" ? "text-emerald-700" : "text-brand-deep";
      const role = v === "warning" ? "status" : undefined;
      out.push(
        <Reveal key={`n-${out.length}`}>
          <p role={role} className={`mt-6 flex items-start gap-2.5 rounded-xl px-4 py-3 text-[12.5px] leading-relaxed ${skin}`}>
            <Icon className={`mt-0.5 h-4 w-4 shrink-0 ${iconColor}`} aria-hidden="true" />
            {b.x}
          </p>
        </Reveal>,
      );
    } else if (b.t === "cta") {
      out.push(<CtaBand key={`c-${out.length}`} message={b.x} />);
    } else if (b.t === "hero") {
      // rendered inside PageHero
      continue;
    }
  }
  return <div className="space-y-4">{out}</div>;
}

/* ── CTA band v2 — navy gradient + texture + orange actions (CHG-071) ──── */
export function CtaBand({ message }: { message: string }) {
  return (
    <Reveal className="mt-12">
      <div className="cta-glow-band relative overflow-hidden rounded-2xl grad-navy-field px-6 py-10 text-white shadow-3 sm:px-10">
        <div className="orb-field" aria-hidden="true">
          <span className="orb" />
          <span className="orb" />
          <span className="orb" />
        </div>
        <div className="absolute inset-0 dot-grid" aria-hidden="true" />
        <div className="absolute inset-0 grad-orange-glow" aria-hidden="true" />
        <div className="absolute inset-0 pattern-noise" aria-hidden="true" />
        <div className="relative flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
          <p className="max-w-2xl font-display text-[19px] font-medium leading-snug sm:text-[21px]">{message}</p>
          <div className="flex flex-wrap gap-3">
            <Link
              href="/book-a-briefing/"
              className="btn-sheen inline-flex items-center gap-2 rounded-[10px] bg-brand px-5 py-2.5 text-[13px] font-semibold text-white hover:bg-brand-hover"
            >
              Book a briefing <ArrowUpRight className="h-4 w-4" />
            </Link>
            <Link
              href="/contact/"
              className="inline-flex items-center rounded-[10px] border border-white/25 px-5 py-2.5 text-[13px] font-medium text-white/85 hover:border-brand-300 hover:text-brand-300"
            >
              Contact us
            </Link>
          </div>
        </div>
      </div>
    </Reveal>
  );
}

/* ── Card grid (CHG-058 base card contract) ───────────────────────────── */
export function CardGrid({ cards, heading, sub }: { cards: Card[]; heading?: string; sub?: string }) {
  if (!cards.length) return null;
  return (
    <Reveal className="mt-14">
      <div className="flex items-end justify-between gap-4">
        <div>
          {heading && <h2 className="font-display text-[22px] font-semibold text-navy-800 sm:text-[24px]">{heading}</h2>}
          {sub && <p className="mt-1 text-[13.5px] text-slate-body/70">{sub}</p>}
        </div>
      </div>
      <div data-stagger className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {cards.map((c) => (
          <Link
            key={c.url + c.title}
            href={c.url}
            className="tilt-card group flex flex-col rounded-2xl border border-line bg-white p-5 transition hover:-translate-y-0.5 hover:border-brand/60 shadow-1 hover:shadow-2"
          >
            <span className="inline-flex w-fit rounded-full bg-brand-tint px-2.5 py-0.5 text-[10.5px] font-semibold uppercase tracking-wider text-brand-deep">
              {c.tag}
            </span>
            <p className="mt-3 font-display text-[15.5px] font-semibold leading-snug text-navy-800 group-hover:text-brand-deep">
              {c.title}
            </p>
            <p className="mt-1.5 flex-1 text-[12.5px] leading-relaxed text-slate-body/75">{c.desc}</p>
            <span className="mt-4 inline-flex items-center gap-1 text-[12px] font-semibold text-brand-deep">
              Explore <ArrowRight className="h-3.5 w-3.5 transition group-hover:translate-x-0.5" />
            </span>
          </Link>
        ))}
      </div>
    </Reveal>
  );
}

/* ── Pull-quote slab (CHG-070): navy field, oversized orange quote glyph ── */
export function Quote({
  text,
  attribution,
  role,
}: {
  text: string;
  attribution: string;
  role?: string;
}) {
  return (
    <Reveal>
      <figure className="quote-fade relative overflow-hidden rounded-2xl grad-navy-field px-6 py-10 text-white shadow-3 sm:px-12 sm:py-12">
        <div className="absolute inset-0 dot-grid" aria-hidden="true" />
        <div className="absolute inset-0 grad-orange-glow-soft" aria-hidden="true" />
        <span
          aria-hidden="true"
          className="quote-mark relative block select-none font-display text-[88px] leading-[0.7] text-brand sm:text-[112px]"
        >
          &ldquo;
        </span>
        <blockquote className="relative mt-4 max-w-3xl font-display text-[19px] font-medium leading-snug sm:text-[23px]">
          {text}
        </blockquote>
        <figcaption className="relative mt-6 flex items-center gap-3">
          <span aria-hidden="true" className="h-8 w-[3px] rounded-full bg-brand" />
          <span className="text-[13px]">
            <span className="block font-semibold text-white">{attribution}</span>
            {role && <span className="mt-0.5 block text-white/60">{role}</span>}
          </span>
        </figcaption>
      </figure>
    </Reveal>
  );
}

/* ── Related rail ─────────────────────────────────────────────────────── */
export function RelatedRail({ links }: { links: Card[] }) {
  if (!links.length) return null;
  return (
    <Reveal className="mt-14">
      <h2 className="font-display text-[20px] font-semibold text-navy-800">Related pages</h2>
      <div className="mt-5 grid gap-3 md:grid-cols-2">
        {links.map((l) => (
          <Link
            key={l.url + l.title}
            href={l.url}
            className="group flex items-start justify-between gap-4 rounded-xl border border-line bg-mist/50 px-4 py-3.5 transition hover:border-brand/60 hover:bg-white"
          >
            <span>
              <span className="block text-[13.5px] font-semibold text-navy-800 group-hover:text-brand-deep">
                {l.title}
              </span>
              {l.desc && <span className="mt-0.5 block text-[12px] text-slate-body/70">{l.desc}</span>}
            </span>
            <ArrowRight className="mt-1 h-4 w-4 shrink-0 text-brand-deep transition group-hover:translate-x-0.5" />
          </Link>
        ))}
      </div>
    </Reveal>
  );
}

/* ── Stats strip (CHG-069: tabular numerals, brand values) ────────────── */
export function StatsStrip({ stats }: { stats: { value: string; label: string }[] }) {
  return (
    <div data-stagger className="stat-flip grid grid-cols-2 gap-px overflow-hidden rounded-xl border border-white/10 bg-white/10 sm:grid-cols-4">
      {stats.map((s) => (
        <div key={s.label} className="bg-navy-800/70 px-4 py-5 text-center backdrop-blur">
          <p className="font-display text-[22px] font-bold tabular-nums text-brand sm:text-[26px]">
            <CountUp value={s.value} />
          </p>
          <p className="mt-1 text-[11px] leading-snug text-white/60">{s.label}</p>
        </div>
      ))}
    </div>
  );
}

