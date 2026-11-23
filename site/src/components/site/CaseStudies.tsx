"use client";

/* ── Case Studies views (Phase 2 redesign) ────────────────────────────────
   CaseHubView   — the /case-studies/ hub: dual index (by industry / by
                   service area), static browse sections that render without
                   JS for crawlers, plus an interactive filter grid.
   CaseStudyView — redesigned case-study page: hero with metric + context
                   chips, sticky facts rail, narrative blocks, and "more in
                   this industry / same service area" rails.                    */

import { useMemo, useState } from "react";
import Link from "next/link";
import {
  ArrowRight, ArrowUpRight, Building2, ChevronRight, Layers, MapPin,
  ShieldCheck,
} from "lucide-react";
import Reveal from "./Reveal";
import { Breadcrumbs, Blocks, CtaBand } from "./PageBlocks";
import { DashStyles } from "./ArchDash";
import type { PageData } from "@/lib/content";

export type CaseCard = {
  title: string;
  url: string;
  industry: string;
  industry_url: string;
  desc: string;
  service?: string;
  service_url?: string;
  region?: string;
};

function useCaseIndex(cards: CaseCard[]) {
  return useMemo(() => {
    const byInd = new Map<string, { url: string; cases: CaseCard[] }>();
    const bySvc = new Map<string, string>();
    for (const c of cards) {
      if (!byInd.has(c.industry)) byInd.set(c.industry, { url: c.industry_url, cases: [] });
      byInd.get(c.industry)!.cases.push(c);
      if (c.service && !bySvc.has(c.service)) bySvc.set(c.service, c.service_url ?? "/services/");
    }
    const industries = [...byInd.entries()].map(([name, e]) => ({
      name, url: e.url, count: e.cases.length, cases: e.cases,
    }));
    const services = [...bySvc.entries()].map(([name, url]) => ({
      name, url, count: cards.filter((c) => c.service === name).length,
    }));
    return { industries, services };
  }, [cards]);
}

/* ══════════════════════════ CASE HUB VIEW ═══════════════════════════════ */
export function CaseHubView({ page }: { page: PageData }) {
  const cards = (page.cards ?? []) as unknown as CaseCard[];
  const { industries, services } = useCaseIndex(cards);
  const [fInd, setFInd] = useState<string | null>(null);
  const [fSvc, setFSvc] = useState<string | null>(null);

  const heroX = page.blocks.find((b) => b.t === "hero")?.x ?? "";
  const ctaX = page.blocks.find((b) => b.t === "cta")?.x;

  const filtered = cards.filter(
    (c) => (!fInd || c.industry === fInd) && (!fSvc || c.service === fSvc),
  );

  const scrollToIndex = (ind?: string, svc?: string) => {
    if (ind !== undefined) setFInd(ind);
    if (svc !== undefined) setFSvc(svc);
    requestAnimationFrame(() =>
      document.getElementById("case-index")?.scrollIntoView({ behavior: "smooth", block: "start" }),
    );
  };

  return (
    <>
      <DashStyles />
      {/* hero */}
      <section className="relative overflow-hidden grad-navy-field text-white">
        <div className="absolute inset-0 dot-grid" aria-hidden="true" />
        <div className="absolute inset-0 grad-orange-glow" aria-hidden="true" />
        <div className="relative container-dq pb-12 pt-10 sm:pb-14 sm:pt-14">
          <Breadcrumbs crumbs={page.crumbs} dark />
          <div className="measure mt-6 max-w-4xl">
            <p className="kicker-bar-dark text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-300">
              Client results
            </p>
            <h1 className="text-display-2 mt-2 text-white">Case studies</h1>
            {heroX && <p className="mt-4 text-[15px] leading-relaxed text-white/70">{heroX}</p>}
          </div>
          <div className="mt-6 flex flex-wrap items-center gap-2.5">
            <span className="rounded-full border border-brand/40 bg-brand/15 px-3.5 py-1.5 text-[12px] font-semibold text-brand-300">
              {cards.length} engagements published
            </span>
            <span className="rounded-full border border-white/15 bg-white/[0.06] px-3.5 py-1.5 text-[12px] text-white/70">
              {industries.length} industries
            </span>
            <span className="rounded-full border border-white/15 bg-white/[0.06] px-3.5 py-1.5 text-[12px] text-white/70">
              {services.length} service areas
            </span>
            <span className="inline-flex items-center gap-1.5 rounded-full border border-white/15 bg-white/[0.06] px-3.5 py-1.5 text-[12px] text-white/70">
              <ShieldCheck className="h-3.5 w-3.5 text-brand-300" aria-hidden="true" /> Measured against signed baselines
            </span>
          </div>
          <div className="mt-7 flex flex-wrap gap-3">
            <button
              type="button"
              onClick={() => scrollToIndex(null, null)}
              className="btn-sheen inline-flex items-center gap-2 rounded-[10px] bg-brand px-5 py-2.5 text-[13px] font-semibold text-white transition hover:bg-brand-hover"
            >
              Explore the results <ArrowDownIcon />
            </button>
            <Link
              href="/book-a-briefing/"
              className="inline-flex items-center rounded-[10px] border border-white/25 px-5 py-2.5 text-[13px] font-medium text-white/85 transition hover:border-brand-300 hover:text-brand-300"
            >
              Book a 45-minute briefing
            </Link>
          </div>
        </div>
      </section>

      {/* ── browse by industry ─────────────────────────────────────────── */}
      <section id="by-industry" className="scroll-mt-28 border-b border-line bg-mist/60 dot-grid-light">
        <div className="container-dq section-y-sm">
          <Reveal>
            <div className="flex flex-wrap items-end justify-between gap-4">
              <div>
                <p className="kicker-bar text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">
                  By industry
                </p>
                <h2 className="text-display-3 mt-1 text-navy-800 sm:text-[26px]">
                  Start with the sector you run
                </h2>
              </div>
              <p className="max-w-md text-[13px] text-slate-body/70">
                Engagement notes from every sector we serve — each written for the rules, pressures and systems of
                record of that industry.
              </p>
            </div>
          </Reveal>
          <div className="mt-8 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            {industries.map((ind, i) => (
              <Reveal key={ind.name} delay={Math.min(i * 30, 180)}>
                <div className="flex h-full flex-col rounded-2xl border border-line bg-white p-5 shadow-1 transition hover:-translate-y-0.5 hover:border-brand/60 hover:shadow-2">
                  <div className="flex items-start justify-between gap-3">
                    <div className="min-w-0">
                      <p className="font-display text-[15.5px] font-semibold leading-snug text-navy-800">
                        {ind.name}
                      </p>
                      <p className="mt-0.5 text-[12px] font-medium text-brand-deep">
                        {ind.count} case{ind.count === 1 ? "" : "s"}
                      </p>
                    </div>
                    <span className="font-display text-[12px] font-bold text-slate-body/30">
                      {String(i + 1).padStart(2, "0")}
                    </span>
                  </div>
                  <ul className="mt-3 flex-1 space-y-2">
                    {ind.cases.slice(0, 3).map((c) => (
                      <li key={c.url}>
                        <Link
                          href={c.url}
                          className="group flex items-start justify-between gap-2 rounded-lg px-2 py-1.5 text-[12.5px] leading-snug text-slate-body/85 transition hover:bg-brand-tint hover:text-brand-deep"
                        >
                          <span className="min-w-0">{c.desc}</span>
                          <ChevronRight className="mt-0.5 h-3.5 w-3.5 shrink-0 text-brand-deep opacity-0 transition group-hover:translate-x-0.5 group-hover:opacity-100" aria-hidden="true" />
                        </Link>
                      </li>
                    ))}
                  </ul>
                  <button
                    type="button"
                    onClick={() => scrollToIndex(ind.name, null)}
                    className="mt-4 inline-flex items-center gap-1.5 self-start text-[12.5px] font-semibold text-brand-deep hover:text-brand"
                  >
                    View all {ind.count} <ArrowRight className="h-3.5 w-3.5" aria-hidden="true" />
                  </button>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* ── browse by service area ─────────────────────────────────────── */}
      <section id="by-service" className="scroll-mt-28 border-b border-line bg-white">
        <div className="container-dq section-y-sm">
          <Reveal>
            <p className="kicker-bar text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">
              By service area
            </p>
            <h2 className="text-display-3 mt-1 text-navy-800 sm:text-[26px]">
              Or start with the capability
            </h2>
          </Reveal>
          <div className="mt-8 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {services.map((svc, i) => (
              <Reveal key={svc.name} delay={Math.min(i * 30, 180)}>
                <button
                  type="button"
                  onClick={() => scrollToIndex(null, svc.name)}
                  className="group flex h-full w-full flex-col items-start rounded-xl border border-line bg-mist/50 p-4 text-left transition hover:-translate-y-0.5 hover:border-brand/60 hover:bg-white hover:shadow-2"
                >
                  <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-navy-800 text-brand-300 transition group-hover:bg-brand group-hover:text-white">
                    <Layers className="h-4 w-4" aria-hidden="true" />
                  </span>
                  <span className="mt-3 text-[13.5px] font-semibold leading-snug text-navy-800 group-hover:text-brand-deep">
                    {svc.name}
                  </span>
                  <span className="mt-1 inline-flex items-center gap-1 text-[12px] font-medium text-brand-deep">
                    {svc.count} case{svc.count === 1 ? "" : "s"} <ArrowRight className="h-3 w-3 transition group-hover:translate-x-0.5" aria-hidden="true" />
                  </span>
                </button>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* ── interactive index ──────────────────────────────────────────── */}
      <section id="case-index" className="scroll-mt-24 bg-mist/60 dot-grid-light">
        <div className="container-dq section-y-sm">
          <Reveal>
            <p className="kicker-bar text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">
              All client builds
            </p>
            <h2 className="text-display-3 mt-1 text-navy-800 sm:text-[26px]">
              Every engagement, one filter away
            </h2>
          </Reveal>

          {/* filter bar */}
          <div className="mt-6 rounded-2xl border border-line bg-white p-4 shadow-1">
            <div className="flex flex-wrap items-center gap-2">
              <span className="inline-flex items-center gap-1.5 text-[11px] font-bold uppercase tracking-[0.14em] text-slate-body/50">
                <Building2 className="h-3.5 w-3.5" aria-hidden="true" /> Industry
              </span>
              {industries.map((ind) => (
                <button
                  key={ind.name}
                  type="button"
                  onClick={() => setFInd(fInd === ind.name ? null : ind.name)}
                  className={`rounded-full border px-3 py-1.5 text-[12px] font-medium transition ${
                    fInd === ind.name
                      ? "border-brand bg-brand text-white"
                      : "border-line bg-mist/60 text-navy-800 hover:border-brand/60 hover:text-brand-deep"
                  }`}
                >
                  {ind.name} <span className="opacity-60">{ind.count}</span>
                </button>
              ))}
            </div>
            <div className="mt-3 flex flex-wrap items-center gap-2 border-t border-line/70 pt-3">
              <span className="inline-flex items-center gap-1.5 text-[11px] font-bold uppercase tracking-[0.14em] text-slate-body/50">
                <Layers className="h-3.5 w-3.5" aria-hidden="true" /> Service area
              </span>
              {services.map((svc) => (
                <button
                  key={svc.name}
                  type="button"
                  onClick={() => setFSvc(fSvc === svc.name ? null : svc.name)}
                  className={`rounded-full border px-3 py-1.5 text-[12px] font-medium transition ${
                    fSvc === svc.name
                      ? "border-brand bg-brand text-white"
                      : "border-line bg-mist/60 text-navy-800 hover:border-brand/60 hover:text-brand-deep"
                  }`}
                >
                  {svc.name} <span className="opacity-60">{svc.count}</span>
                </button>
              ))}
              {(fInd || fSvc) && (
                <button
                  type="button"
                  onClick={() => {
                    setFInd(null);
                    setFSvc(null);
                  }}
                  className="ml-auto inline-flex items-center gap-1 rounded-full border border-brand/40 bg-brand-tint px-3 py-1.5 text-[12px] font-semibold text-brand-deep transition hover:bg-brand hover:text-white"
                >
                  Clear filters
                </button>
              )}
            </div>
          </div>

          {/* active-filter heading + grid */}
          <div className="mt-8">
            {(fInd || fSvc) && (
              <p className="mb-4 text-[13.5px] text-slate-body/75">
                Showing <span className="font-semibold text-brand-deep">{filtered.length}</span> case
                {filtered.length === 1 ? "" : "s"}
                {fInd ? (
                  <>
                    {" "}in <span className="font-semibold text-navy-800">{fInd}</span>
                    {fInd && fInd !== fSvc && (
                      <Link href={industries.find((i) => i.name === fInd)?.url ?? "#"} className="ml-1.5 inline-flex items-center text-[12px] font-medium text-brand-deep hover:underline">
                        industry hub <ArrowUpRight className="h-3 w-3" aria-hidden="true" />
                      </Link>
                    )}
                  </>
                ) : null}
                {fSvc ? (
                  <>
                    {" "}via <span className="font-semibold text-navy-800">{fSvc}</span>
                    <Link href={services.find((s) => s.name === fSvc)?.url ?? "#"} className="ml-1.5 inline-flex items-center text-[12px] font-medium text-brand-deep hover:underline">
                      service page <ArrowUpRight className="h-3 w-3" aria-hidden="true" />
                    </Link>
                  </>
                ) : null}
              </p>
            )}
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {filtered.map((c) => (
                <Link
                  key={c.url}
                  href={c.url}
                  className="group flex flex-col rounded-2xl border border-line bg-white p-5 shadow-1 transition hover:-translate-y-0.5 hover:border-brand/60 hover:shadow-2"
                >
                  <div className="flex flex-wrap gap-1.5">
                    <span className="rounded-full bg-brand-tint px-2.5 py-0.5 text-[10.5px] font-semibold uppercase tracking-wider text-brand-deep">
                      {c.industry}
                    </span>
                    {c.service && (
                      <span className="rounded-full border border-line px-2.5 py-0.5 text-[10.5px] font-medium text-slate-body/70">
                        {c.service}
                      </span>
                    )}
                  </div>
                  <p className="mt-3 flex-1 text-[13.5px] font-medium leading-relaxed text-navy-800 group-hover:text-brand-deep">
                    {c.desc}
                  </p>
                  <div className="mt-4 flex items-center justify-between gap-2 border-t border-line/70 pt-3">
                    <span className="text-[11.5px] leading-snug text-slate-body/60">
                      {c.title}
                      {c.region ? ` · ${c.region}` : ""}
                    </span>
                    <ArrowRight className="h-3.5 w-3.5 shrink-0 text-brand-deep transition group-hover:translate-x-0.5" aria-hidden="true" />
                  </div>
                </Link>
              ))}
            </div>
            {filtered.length === 0 && (
              <p className="rounded-xl border border-line bg-white px-4 py-6 text-center text-[13px] text-slate-body/70">
                No case matches that combination yet — clear a filter, or bring the metric to a briefing.
              </p>
            )}
          </div>
        </div>
      </section>

      {/* closing CTA */}
      <section className="container-dq pb-16 pt-12">
        <CtaBand message={ctaX ?? "Book a briefing — bring the metric you need to move, and we will walk the closest engagement end to end."} />
      </section>
    </>
  );
}

function ArrowDownIcon() {
  return <ArrowRight className="h-4 w-4 rotate-90" aria-hidden="true" />;
}

/* ══════════════════════════ CASE STUDY VIEW ═════════════════════════════ */
export function CaseStudyView({
  page,
  hub,
}: {
  page: PageData;
  hub: PageData | null;
}) {
  const cards = ((hub?.cards ?? []) as unknown as CaseCard[]).filter((c) => c.url !== page.url);
  const sameIndustry = cards.filter((c) => c.industry === page.l2).slice(0, 3);
  const svcName = page.related?.find((r) => r.title.startsWith("Service area — ") || r.title.startsWith("Tower — "))?.title.replace(/^(Service area|Tower) — /, "");
  const sameService = svcName ? cards.filter((c) => c.service === svcName).slice(0, 3) : [];
  const heroX = page.blocks.find((b) => b.t === "hero")?.x ?? page.meta_description;
  const noteX = page.blocks.find((b) => b.t === "note")?.x;
  const ctaIdx = page.blocks.findIndex((b) => b.t === "cta");
  const ctaX = ctaIdx >= 0 ? (page.blocks[ctaIdx] as { x: string }).x : undefined;

  /* engagement facts live in the table block; the rail renders them so the
     article no longer needs the raw table */
  const factsTable = page.blocks.find(
    (b) => b.t === "table" && b.caption === "Engagement facts",
  ) as { rows: string[][] } | undefined;
  const facts = factsTable?.rows?.[0] ?? [];
  const factRows: [string, string][] = facts.length === 4
    ? [["Duration", facts[0]], ["Team", facts[1]], ["Region", facts[2]], ["Engagement model", facts[3]]]
    : [];

  const articleBlocks = page.blocks.filter((b) => !(b.t === "table" && b.caption === "Engagement facts"));
  const svcRelated = page.related?.find((r) => r.title.startsWith("Service area — ") || r.title.startsWith("Tower — "));
  const svcLabel = svcRelated?.title.replace(/^(Service area|Tower) — /, "");
  const indRelated = page.related?.find((r) => r.title.endsWith("— industry hub"));

  return (
    <>
      <DashStyles />
      {/* hero */}
      <section className="relative overflow-hidden grad-navy-field text-white">
        <div className="absolute inset-0 dot-grid" aria-hidden="true" />
        <div className="absolute inset-0 grad-orange-glow" aria-hidden="true" />
        <div className="relative container-dq pb-12 pt-10 sm:pb-14 sm:pt-14">
          <Breadcrumbs crumbs={page.crumbs} dark />
          <div className="mt-6 max-w-4xl">
            <p className="kicker-bar-dark text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-300">
              Case study
            </p>
            <h1 className="text-display-2 mt-2 text-white">{page.title}</h1>
            {heroX && <p className="mt-4 max-w-3xl text-[16px] leading-relaxed text-white/80">{heroX}</p>}
          </div>
          <div className="mt-6 flex flex-wrap items-center gap-2">
            <Link
              href={page.crumbs[1]?.url ?? "/industries/"}
              className="inline-flex items-center gap-1.5 rounded-full border border-white/15 bg-white/[0.06] px-3.5 py-1.5 text-[12px] font-medium text-white/75 transition hover:border-brand-300 hover:text-brand-300"
            >
              <Building2 className="h-3.5 w-3.5 text-brand-300" aria-hidden="true" />
              {page.l2}
            </Link>
            {svcRelated && (
              <Link
                href={svcRelated.url}
                className="inline-flex items-center gap-1.5 rounded-full border border-white/15 bg-white/[0.06] px-3.5 py-1.5 text-[12px] font-medium text-white/75 transition hover:border-brand-300 hover:text-brand-300"
              >
                <Layers className="h-3.5 w-3.5 text-brand-300" aria-hidden="true" />
                {svcLabel}
              </Link>
            )}
            {factRows.find(([k]) => k === "Region") && (
              <span className="inline-flex items-center gap-1.5 rounded-full border border-white/15 bg-white/[0.06] px-3.5 py-1.5 text-[12px] text-white/70">
                <MapPin className="h-3.5 w-3.5 text-brand-300" aria-hidden="true" />
                {factRows.find(([k]) => k === "Region")![1]}
              </span>
            )}
          </div>
        </div>
      </section>

      {/* body */}
      <div className="container-dq py-12">
        <div className="grid gap-10 lg:grid-cols-[minmax(0,1fr)_300px]">
          {/* article */}
          <article className="dq-article min-w-0">
            <Blocks blocks={articleBlocks} skip={["hero"]} />
          </article>

          {/* facts rail */}
          <aside className="min-w-0">
            <div className="lg:sticky lg:top-24 space-y-4">
              <div className="rounded-2xl border border-line bg-white p-5 shadow-1">
                <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-brand-deep">
                  Engagement facts
                </p>
                <dl className="mt-3 space-y-2.5">
                  {factRows.map(([k, v]) => (
                    <div key={k} className="flex items-start justify-between gap-3 text-[12.5px]">
                      <dt className="shrink-0 text-slate-body/60">{k}</dt>
                      <dd className="text-right font-medium text-navy-800">{v}</dd>
                    </div>
                  ))}
                  <div className="flex items-start justify-between gap-3 border-t border-line/70 pt-2.5 text-[12.5px]">
                    <dt className="shrink-0 text-slate-body/60">Industry</dt>
                    <dd className="text-right font-medium text-navy-800">{page.l2}</dd>
                  </div>
                  {svcRelated && (
                    <div className="flex items-start justify-between gap-3 text-[12.5px]">
                      <dt className="shrink-0 text-slate-body/60">Service area</dt>
                      <dd className="text-right">
                        <Link href={svcRelated.url} className="font-medium text-brand-deep hover:underline">
                          {svcLabel}
                        </Link>
                      </dd>
                    </div>
                  )}
                </dl>
                {noteX && (
                  <p className="mt-4 border-t border-line/70 pt-3 text-[11px] leading-relaxed text-slate-body/60">
                    {noteX}
                  </p>
                )}
              </div>

              {indRelated && (
                <Link
                  href={indRelated.url}
                  className="group flex items-start justify-between gap-3 rounded-2xl border border-line bg-mist/50 p-4 transition hover:border-brand/60 hover:bg-white"
                >
                  <span>
                    <span className="block text-[12px] font-semibold text-brand-deep">Industry hub</span>
                    <span className="mt-0.5 block text-[13px] font-medium text-navy-800 group-hover:text-brand-deep">
                      {page.l2}
                    </span>
                  </span>
                  <ArrowUpRight className="mt-1 h-4 w-4 shrink-0 text-brand-deep transition group-hover:translate-x-0.5" aria-hidden="true" />
                </Link>
              )}
              <Link
                href="/case-studies/"
                className="group flex items-start justify-between gap-3 rounded-2xl border border-line bg-mist/50 p-4 transition hover:border-brand/60 hover:bg-white"
              >
                <span>
                  <span className="block text-[12px] font-semibold text-brand-deep">All case studies</span>
                  <span className="mt-0.5 block text-[13px] font-medium text-navy-800 group-hover:text-brand-deep">
                    The full results library, filterable by industry and capability
                  </span>
                </span>
                <ArrowUpRight className="mt-1 h-4 w-4 shrink-0 text-brand-deep transition group-hover:translate-x-0.5" aria-hidden="true" />
              </Link>
            </div>
          </aside>
        </div>

        {/* more in this industry */}
        {sameIndustry.length > 0 && (
          <section className="mt-14 border-t border-line pt-10">
            <div className="flex flex-wrap items-end justify-between gap-3">
              <div>
                <p className="kicker-bar text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">
                  Same industry
                </p>
                <h2 className="mt-1 font-display text-[20px] font-semibold text-navy-800">
                  More in {page.l2}
                </h2>
              </div>
              <button
                type="button"
                onClick={() => document.getElementById("case-index")?.scrollIntoView({ behavior: "smooth" })}
                className="hidden text-[12.5px] font-semibold text-brand-deep hover:underline lg:inline-flex lg:items-center lg:gap-1.5"
              >
                All {cards.length + 1} engagements <ArrowRight className="h-3.5 w-3.5" aria-hidden="true" />
              </button>
            </div>
            <div className="mt-5 grid gap-3 md:grid-cols-3">
              {sameIndustry.map((c) => (
                <Link
                  key={c.url}
                  href={c.url}
                  className="group rounded-xl border border-line bg-mist/50 px-4 py-3.5 transition hover:border-brand/60 hover:bg-white"
                >
                  <span className="block text-[13px] font-semibold leading-snug text-navy-800 group-hover:text-brand-deep">
                    {c.desc}
                  </span>
                  {c.service && (
                    <span className="mt-1 block text-[11.5px] text-slate-body/60">{c.service}</span>
                  )}
                </Link>
              ))}
            </div>
          </section>
        )}

        {/* same service area */}
        {sameService.length > 0 && (
          <section className="mt-10 border-t border-line pt-10">
            <p className="kicker-bar text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">
              Same service area
            </p>
            <h2 className="mt-1 font-display text-[20px] font-semibold text-navy-800">
              Other estates this capability moved
            </h2>
            <div className="mt-5 grid gap-3 md:grid-cols-3">
              {sameService.map((c) => (
                <Link
                  key={c.url}
                  href={c.url}
                  className="group rounded-xl border border-line bg-mist/50 px-4 py-3.5 transition hover:border-brand/60 hover:bg-white"
                >
                  <span className="block text-[13px] font-semibold leading-snug text-navy-800 group-hover:text-brand-deep">
                    {c.desc}
                  </span>
                  <span className="mt-1 block text-[11.5px] text-slate-body/60">{c.industry}</span>
                </Link>
              ))}
            </div>
          </section>
        )}

        {/* next step */}
        {ctaX && (
          <div className="mt-12">
            <CtaBand message={ctaX} />
          </div>
        )}
      </div>
    </>
  );
}
