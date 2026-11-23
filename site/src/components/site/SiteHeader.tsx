"use client";

/* ── SiteHeader — Phase 1 navigation redesign ──────────────────────────────
   Mega-menu rebuilt as an "index rail + live preview" system:
   • LEFT: a compact index rail (one row per group, icon + label + depth hint).
     Hovering/focusing a row switches the preview — no more uniform link-dump
     columns, no truncated labels, a clear scan path top-to-bottom.
   • RIGHT: the selected group's destination links in a wide 2-column grid,
     with the group blurb, an "Explore …" hub link and (for platforms) the
     capability list so the menu itself teaches the product.
   • Interaction: 60ms hover-intent open, 220ms close grace, Esc closes,
     focus opens, first click opens (second navigates), full keyboard path.
   Laptop policy (hard rule): from 1024px up the full top navigation is
   ALWAYS visible — the old JS fit-guard that swapped laptops to a hamburger
   is gone. A deterministic CSS band compresses type/padding on 1024–1279px
   screens so the same top bar fits with headroom; the hamburger only exists
   below the lg breakpoint (phones / small tablets).                           */

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  ChevronDown, ChevronRight, Menu, X, ArrowRight, Search, Sparkles, Bot, Database, ShieldCheck,
  Cloud, Atom, Link2, Factory, Landmark, HeartPulse, Building2, TrendingUp,
  ShieldAlert, Gauge, Users, Boxes, Compass as CompassIcon, BookOpen, Newspaper,
  Handshake, Layers, BrainCircuit, CircleDot, Wrench,
} from "lucide-react";
import Logo from "./Logo";
import { SearchOverlay, SkipLink, AnnouncementBar, StickyMobileCTA, PLATFORM_EXTRAS } from "./Wave3";
import type { Brand, Nav } from "@/lib/content";

/* ── icon + blurb per mega group ─────────────────────────────────────────── */
const COL_META: Record<string, { icon: React.ComponentType<{ className?: string }>; blurb: string }> = {
  // consulting
  "Data & Analytics": { icon: Database, blurb: "Analytics products, migration factories and transformation programs — the decision substrate, engineered." },
  "Engineering & Quality": { icon: Wrench, blurb: "Software pods, quality engineering, application modernization and product design that ships." },
  "Cloud & Operations": { icon: Cloud, blurb: "Azure estates end to end, managed operations with named owners, and support measured on resolution." },
  "Advisory & Enterprise": { icon: Handshake, blurb: "Governed capacity, zero-trust security architecture and ERP programs that land process and controls." },
  // services
  "Applied AI & Generative AI": { icon: BrainCircuit, blurb: "Production AI measured on the P&L — strategy, platform build-out, retrieval and multimodal systems under one governance fabric." },
  "Agentic AI & Hyperautomation": { icon: Bot, blurb: "Governed digital workers at scale — process mining, decision intelligence and orchestration with human checkpoints by design." },
  "Data, Analytics & Lakehouse": { icon: Database, blurb: "Pipelines, models and governance — from ingestion engineering to monetizable data products on a lakehouse contract." },
  "Cybersecurity & Zero-Trust": { icon: ShieldCheck, blurb: "Identity-first security architecture — zero-trust estates, managed detection and AI-model protection that survives audit." },
  "Cloud, Edge & Platform Engineering": { icon: Cloud, blurb: "Reliable estates at lower unit cost — hybrid multicloud, edge fleets, SRE discipline and FinOps baked into the platform." },
  "Quantum & Advanced Compute": { icon: Atom, blurb: "Optimization and PQC migration — every quantum-inspired run benchmarked against the best classical solver." },
  "Blockchain & Digital Trust": { icon: Link2, blurb: "Permissioned networks and credentials — DLT engineering, tokenization and provenance regulators can inspect." },
  "IoT, Digital Twin & Robotics": { icon: Factory, blurb: "From sensor data to actuation — industrial IoT fabrics, twin platforms and vision systems that close the loop." },
  // industries
  "Financial Services & Insurance": { icon: Landmark, blurb: "Banking, payments and insurance — real-time decisioning under the strictest regulatory lens." },
  "Health, Public Sector & Education": { icon: HeartPulse, blurb: "Care, government and research — outcomes with privacy, equity and auditability engineered in." },
  "Industry, Retail & Commerce": { icon: Factory, blurb: "Plants, stores and supply chains — decision latency compressed from days to seconds." },
  "Energy, Infrastructure & Technology": { icon: Gauge, blurb: "Grids, networks and platforms — forecasting, reliability and optimization at infrastructure scale." },
  // solutions
  "Growth & Revenue": { icon: TrendingUp, blurb: "Pricing, commerce and CX — revenue mechanics recomposed around live decisions." },
  "Risk & Resilience": { icon: ShieldAlert, blurb: "Fraud, cyber and scenario risk — decisions explained well enough to defend in audit." },
  "Operational Excellence": { icon: Gauge, blurb: "Automation, assets and IT ops — throughput economics with autonomous runbooks." },
  "Workforce & Experience": { icon: Users, blurb: "Copilots and service orchestration — the frontline gets leverage, not another dashboard." },
  // platform suite (from our R&D programme)
  "Achala Nexus — Decision Intelligence Hub": { icon: CircleDot, blurb: "One decision API for credit, claims, triage and fraud, with versioned policies and full replay." },
  "Achala Forge — Data & Lakehouse Engineering Platform": { icon: Database, blurb: "A lakehouse built with data contracts, tested pipelines and a run cost you can steer." },
  "Achala Swarm — Agentic AI Orchestration Platform": { icon: Bot, blurb: "Large agent fleets run as one workforce — queues, budgets and human checkpoints included." },
  "Achala Sentinel — Zero-Trust & AI Security Platform": { icon: ShieldCheck, blurb: "Zero-trust controls for people, machines and models, with evidence your auditors accept." },
  "Achala Twinverse — Digital Twin & IoT Intelligence Platform": { icon: Boxes, blurb: "Sensor data to simulation to actuation — a twin you can trust for physical operations." },
  "Achala Quanta — Quantum & Advanced Compute Suite": { icon: Atom, blurb: "Emerging compute benchmarked against the best classical baseline before you invest." },
  "Achala Ledger — Distributed Trust & Tokenization Platform": { icon: Link2, blurb: "Permissioned networks for shared records and tokenized assets regulators can inspect." },
  "Achala Compass — Responsible AI & Governance Suite": { icon: CompassIcon, blurb: "Model risk, validation and monitoring with evidence your model-risk committee approves." },
  // production platforms
  "Platforms in production": { icon: Wrench, blurb: "Eight platforms running client operations today — emergency response, fleets, KYC, telemedicine and more." },
  // insights / about
  "AI & Data viewpoints": { icon: BrainCircuit, blurb: "Field notes on production AI — what ships, what scales, what stalls." },
  "Automation & operations viewpoints": { icon: Bot, blurb: "What actually scales — automation economics from the delivery floor." },
  "Security, cloud & trust viewpoints": { icon: ShieldCheck, blurb: "Controls that survive audit — security and platform theses with vendor questions." },
  "Emerging compute viewpoints": { icon: Atom, blurb: "Where the math pays back — quantum and advanced compute, benchmarked." },
  "Company": { icon: Building2, blurb: "Who we are and how we operate — offices, credentials and the delivery standard." },
  "Our Approach": { icon: Layers, blurb: "The method behind every program — gates that bind, evidence that travels." },
  "Join & Contact": { icon: Handshake, blurb: "Careers, news and offices — a human process on both sides." },
};
function colMeta(label: string) {
  return COL_META[label] ?? { icon: Sparkles, blurb: "" };
}
function platformKey(label: string): string {
  return label.replace(/^Achala /, "").split(" ")[0];
}
/* singular kicker word above the preview title */
const PREVIEW_KICKER: Record<string, string> = {
  Consulting: "Consulting practice",
  Services: "Service domain",
  Industries: "Industry group",
  Solutions: "Solution group",
  Platforms: "Platform",
  Insights: "Viewpoints",
  "About Us": "Company",
};

/* ── MegaPanel — index rail + live preview ───────────────────────────────── */
function MegaPanel({
  item,
  open,
  onCancelClose,
  onScheduleClose,
}: {
  item: Nav["primary"][number];
  open: boolean;
  onCancelClose: () => void;
  onScheduleClose: () => void;
}) {
  const [active, setActive] = useState(0);
  useEffect(() => {
    setActive(0);
  }, [item.label]);
  if (!item.mega) return null;
  const safeIdx = Math.min(active, item.mega.length - 1);
  const col = item.mega[safeIdx];
  const meta = colMeta(col.label);
  const Icon = meta.icon;
  const isPlatform = item.label === "Platforms";
  const extra = isPlatform ? PLATFORM_EXTRAS[platformKey(col.label)] : undefined;
  const shortName = col.label.replace(/^Achala /, "").split(" — ")[0];

  return (
    /* Anchored to the full-width header bar (inset-x-0), NOT the nav item. */
    <div
      className={`absolute inset-x-0 top-full hidden lg:block ${open ? "" : "pointer-events-none"}`}
      style={{ visibility: open ? "visible" : "hidden" }}
      onMouseEnter={onCancelClose}
      onMouseLeave={onScheduleClose}
    >
      <div
        className={`mega-panel border-t border-line bg-white shadow-3 ${open ? "" : "mega-hidden"}`}
        role="region"
        aria-label={`${item.label} menu`}
      >
        <div className="container-dq py-6">
          <div className="grid gap-7 lg:grid-cols-[288px_minmax(0,1fr)] xl:grid-cols-[368px_minmax(0,1fr)]">
            {/* ── index rail ─────────────────────────────────────────── */}
            <div
              className="flex flex-col gap-1 lg:border-r lg:border-line lg:pr-6"
              role="tablist"
              aria-label={`${item.label} groups`}
            >
              {item.mega.map((c, i) => {
                const rm = colMeta(c.label);
                const RIcon = rm.icon;
                const isActive = i === safeIdx;
                /* full menu names: platforms keep their complete
                   "Achala X — descriptor" label; nothing gets shortened. */
                const rowLabel = c.label;
                return (
                  <Link
                    key={c.label + c.url}
                    href={c.url}
                    role="tab"
                    aria-selected={isActive}
                    tabIndex={open ? 0 : -1}
                    onMouseEnter={() => setActive(i)}
                    onFocus={() => setActive(i)}
                    onKeyDown={(e) => {
                      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
                        e.preventDefault();
                        const next = (i + (e.key === "ArrowDown" ? 1 : item.mega!.length - 1)) % item.mega!.length;
                        setActive(next);
                        document.getElementById(`mega-rail-${item.label}-${next}`)?.focus();
                      }
                    }}
                    id={`mega-rail-${item.label}-${i}`}
                    className={`mega-rail-item group flex items-center gap-3 rounded-xl px-3 py-2.5 transition-colors duration-200 ${
                      isActive ? "bg-brand-tint" : "hover:bg-mist"
                    }`}
                  >
                    <span
                      className={`relative flex h-9 w-9 shrink-0 items-center justify-center rounded-[10px] transition-colors duration-200 ${
                        isActive ? "bg-brand text-white" : "bg-navy-800 text-white"
                      }`}
                    >
                      <RIcon className="h-4 w-4" aria-hidden="true" />
                      {isActive && (
                        <span aria-hidden="true" className="absolute -left-3 top-1/2 h-6 w-[3px] -translate-y-1/2 rounded-full bg-brand" />
                      )}
                    </span>
                    <span className="min-w-0">
                      <span
                        className={`block text-[13.5px] font-semibold leading-snug text-pretty transition-colors ${
                          isActive ? "text-brand-deep" : "text-navy-800"
                        }`}
                      >
                        {rowLabel}
                      </span>
                    </span>
                    <ChevronRight
                      aria-hidden="true"
                      className={`ml-auto h-4 shrink-0 transition-all duration-200 ${
                        isActive ? "w-4 translate-x-0 text-brand opacity-100" : "w-0 -translate-x-1 opacity-0"
                      }`}
                    />
                  </Link>
                );
              })}
            </div>

            {/* ── live preview (remounts on switch for the fade-up) ──── */}
            <div key={col.label} className="mega-preview-in min-w-0">
              <div className="flex flex-wrap items-start justify-between gap-x-6 gap-y-2">
                <div className="min-w-0">
                  <p className="text-[10.5px] font-bold uppercase tracking-[0.18em] text-slate-body/50">
                    {isPlatform ? "Platform" : PREVIEW_KICKER[item.label] ?? item.label}
                  </p>
                  <h3 className="mt-0.5 font-display text-[20px] font-semibold leading-snug text-navy-800">
                    {col.label}
                  </h3>
                  {meta.blurb && (
                    <p className="mt-1.5 max-w-xl text-[13px] leading-relaxed text-slate-body/75">{meta.blurb}</p>
                  )}
                </div>
                <Link
                  href={col.url}
                  tabIndex={open ? 0 : -1}
                  className="link-animated inline-flex shrink-0 items-center gap-1.5 py-1 text-[13px] font-semibold text-brand-deep"
                >
                  Explore {shortName} <ArrowRight className="h-4 w-4" aria-hidden="true" />
                </Link>
              </div>

              {isPlatform && extra ? (
                <div className="mt-4 grid gap-5 md:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]">
                  <div className="rounded-xl border border-line bg-mist/50 p-4">
                    <p className="text-[10.5px] font-bold uppercase tracking-[0.16em] text-brand-deep">
                      {extra.method}
                    </p>
                    <ul className="mt-2.5 space-y-1.5">
                      {extra.caps.slice(0, 5).map((c) => (
                        <li key={c} className="flex items-start gap-2 text-[12.5px] leading-snug text-navy-800/90">
                          <span aria-hidden="true" className="mt-[7px] h-1.5 w-1.5 shrink-0 rounded-full bg-brand" />
                          {c}
                        </li>
                      ))}
                    </ul>
                  </div>
                  <ul className="space-y-1 self-center">
                    {col.children.map((ch) => (
                      <li key={ch.label + ch.url}>
                        <Link
                          href={ch.url}
                          tabIndex={open ? 0 : -1}
                          className="group flex items-center justify-between gap-3 rounded-lg px-3 py-2.5 text-[13.5px] font-medium text-navy-800 transition-colors hover:bg-brand-tint hover:text-brand-deep"
                        >
                          {ch.label}
                          <ArrowRight className="h-3.5 w-3.5 shrink-0 text-brand-deep opacity-0 transition group-hover:translate-x-0.5 group-hover:opacity-100" aria-hidden="true" />
                        </Link>
                      </li>
                    ))}
                  </ul>
                </div>
              ) : (
                <ul className="mt-4 grid gap-x-6 sm:grid-cols-2">
                  {col.children.map((ch) => (
                    <li key={ch.label + ch.url}>
                      <Link
                        href={ch.url}
                        tabIndex={open ? 0 : -1}
                        className="group flex items-center justify-between gap-3 rounded-lg border-b border-line/70 px-3 py-2.5 text-[13.5px] font-medium text-navy-800 transition-colors last:border-0 hover:bg-brand-tint hover:text-brand-deep"
                      >
                        <span className="min-w-0">{ch.label}</span>
                        <ArrowRight className="h-3.5 w-3.5 shrink-0 text-brand-deep opacity-0 transition group-hover:translate-x-0.5 group-hover:opacity-100" aria-hidden="true" />
                      </Link>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>

          {/* featured strip — a next step on every panel */}
          <div className="mt-5 flex flex-wrap items-center justify-between gap-3 rounded-xl border border-brand/25 bg-brand-tint px-4 py-3">
            <p className="text-[12.5px] leading-snug text-slate-body/85">
              <span className="font-semibold text-navy-800">Not sure where to start?</span>{" "}
              A 45-minute briefing maps your metric to the right entry point.
            </p>
            <div className="flex flex-wrap gap-2">
              <Link
                href="/book-a-briefing/"
                tabIndex={open ? 0 : -1}
                className="inline-flex items-center gap-1 rounded-lg bg-brand px-3 py-1.5 text-[11.5px] font-semibold text-white transition hover:bg-brand-hover"
              >
                Book a briefing <ArrowRight className="h-3 w-3" aria-hidden="true" />
              </Link>
              <Link
                href="/value-assessment/"
                tabIndex={open ? 0 : -1}
                className="inline-flex items-center rounded-lg border border-line bg-white px-3 py-1.5 text-[11.5px] font-semibold text-navy-800 transition hover:border-brand"
              >
                Value assessment
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function SiteHeader({ nav, brand }: { nav: Nav; brand: Brand }) {
  const [openItem, setOpenItem] = useState<string | null>(null);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [mobileSection, setMobileSection] = useState<string | null>(null);
  const [scrolled, setScrolled] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const closeTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const openTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const rowRef = useRef<HTMLDivElement | null>(null);
  const pathname = usePathname();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    // close menus after navigation (deferred to avoid cascading render)
    const t = setTimeout(() => {
      setOpenItem(null);
      setMobileOpen(false);
      setMobileSection(null);
    }, 0);
    return () => clearTimeout(t);
  }, [pathname]);

  /* hover intent: short open delay kills fly-over flicker; generous close
     grace lets the pointer travel from the trigger to the panel. */
  const clearTimers = useCallback(() => {
    if (closeTimer.current) clearTimeout(closeTimer.current);
    if (openTimer.current) clearTimeout(openTimer.current);
  }, []);
  const scheduleOpen = useCallback(
    (label: string) => {
      clearTimers();
      openTimer.current = setTimeout(() => setOpenItem(label), 60);
    },
    [clearTimers],
  );
  const scheduleClose = useCallback(() => {
    clearTimers();
    closeTimer.current = setTimeout(() => setOpenItem(null), 220);
  }, [clearTimers]);
  const cancelClose = clearTimers;

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setOpenItem(null);
        setMobileOpen(false);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  return (
    <header className="sticky top-0 z-50">
      <SkipLink />
      {/* announcement bar (CHG-381) */}
      <AnnouncementBar message="8 patented accelerator families align Achala platforms and services. Explore the acceleration map" href="/patented-intelligence/" />
      {/* utility bar — brand navy (CHG-010) */}
      <div className="bg-navy-900 text-white/70 text-[11.5px]">
        <div className="container-dq flex h-8 items-center justify-between">
          <p className="tracking-wide">
            <span className="hidden sm:inline">ISO/IEC 27001 · TISAX · GDPR-aligned delivery</span>
            <span className="sm:hidden">ISO/IEC 27001 · TISAX · GDPR</span>
          </p>
          <div className="hidden md:flex items-center gap-4">
            <a href={`mailto:${brand.emails.general}`} className="hover:text-brand-300">
              {brand.emails.general}
            </a>
          </div>
        </div>
      </div>

      {/* main bar — `relative` anchors the full-width megamenu below */}
      <div
        className={`relative border-b border-line bg-white/95 backdrop-blur transition-shadow ${scrolled ? "shadow-2" : ""}`}
      >
        {/* scroll condense (CHG-357) + overflow-x-clip: nothing inside the bar can
            paint outside the viewport in any rendering condition. From 1024px up
            the top nav is always rendered (laptop policy); the compact band in
            globals.css keeps it inside the row on 1024–1279px screens. */}
        <div
          ref={rowRef}
          className={`container-dq flex flex-nowrap items-center justify-between gap-4 overflow-x-clip transition-[height] duration-300 ${scrolled ? "h-[56px]" : "h-[72px]"}`}
        >
          <Link href="/" aria-label="Achala IT Solutions home" className="hdr-logo shrink-0">
            <Logo height={40} />
          </Link>

          {/* desktop top navigation — visible from 1024px up, always (laptop
              policy). No JS fit-guard: a hamburger must never appear on a
              laptop-sized screen; compression is handled purely in CSS. */}
          <nav
            aria-label="Primary"
            className="hidden lg:flex items-center gap-0 xl:gap-0.5 min-w-0"
          >
            {nav.primary.map((item) => {
              const isOpen = openItem === item.label;
              return (
                <div
                  key={item.label}
                  className="relative"
                  onMouseEnter={() => {
                    if (item.mega) scheduleOpen(item.label);
                    else {
                      clearTimers();
                      setOpenItem(null);
                    }
                  }}
                  onMouseLeave={item.mega ? scheduleClose : undefined}
                >
                  <Link
                    href={item.url}
                    data-active={pathname.startsWith(item.url)}
                    aria-current={pathname === item.url ? "page" : undefined}
                    onClick={(e) => {
                      // first tap/click opens the panel; second click navigates.
                      if (item.mega && openItem !== item.label) {
                        e.preventDefault();
                        clearTimers();
                        setOpenItem(item.label);
                      }
                    }}
                    className={`nav-link flex items-center gap-1 px-2 py-2.5 text-[12px] xl:px-3.5 xl:text-[13.5px] font-medium whitespace-nowrap rounded-md transition-colors ${
                      pathname.startsWith(item.url)
                        ? "text-brand-deep"
                        : "text-navy-800 hover:text-brand-deep"
                    }`}
                    aria-expanded={item.mega ? isOpen : undefined}
                    onFocus={() => setOpenItem(item.mega ? item.label : null)}
                  >
                    {item.label}
                    {item.mega && (
                      <ChevronDown
                        className={`h-3.5 w-3.5 opacity-55 transition-transform duration-200 ${isOpen ? "rotate-180" : ""}`}
                        aria-hidden="true"
                      />
                    )}
                  </Link>
                </div>
              );
            })}
          </nav>

          <div className="flex shrink-0 items-center gap-2.5">
            {/* header search entry (CHG-358) */}
            <button
              type="button"
              onClick={() => setSearchOpen(true)}
              aria-label="Search the site"
              className="hdr-search inline-flex h-9 w-9 items-center justify-center rounded-[10px] border border-line text-navy-800 transition hover:border-brand hover:text-brand-deep"
            >
              <Search className="h-4 w-4" aria-hidden="true" />
            </button>
            {/* primary action: solid orange (CHG-012) with sheen (CHG-053) —
                slightly tighter on the 1024–1279px laptop band */}
            <Link
              href={nav.cta.url}
              className="hdr-cta btn-sheen hidden sm:inline-flex items-center rounded-[10px] bg-brand px-3.5 py-2.5 text-[12.5px] font-semibold text-white transition-colors hover:bg-brand-hover xl:px-4 xl:text-[13px]"
            >
              {nav.cta.label}
            </Link>
            {/* hamburger exists ONLY below the lg breakpoint — never on laptops */}
            <button
              className="lg:hidden inline-flex h-10 w-10 items-center justify-center rounded-[10px] border border-line"
              aria-label="Open menu"
              aria-expanded={mobileOpen}
              onClick={() => setMobileOpen((v) => !v)}
            >
              {mobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </button>
          </div>
        </div>

        {/* megamenu — one full-width rail+preview panel per mega item */}
        {nav.primary
          .filter((item) => item.mega)
          .map((item) => (
            <MegaPanel
              key={item.label}
              item={item}
              open={openItem === item.label}
              onCancelClose={cancelClose}
              onScheduleClose={scheduleClose}
            />
          ))}
      </div>

      {/* mobile drawer — drawer-scroll caps height at the dynamic viewport
          (see .drawer-scroll in globals.css) so the CTA never slides under
          mobile browser toolbars. Accordion groups with 2-col child grids.
          Strictly below lg: laptops always use the top navigation. */}
      {mobileOpen && (
        <div
          className="drawer-scroll lg:hidden border-b border-line bg-white shadow-3 overflow-y-auto"
        >
          <div className="container-dq space-y-1 pt-4 pb-[calc(1rem+env(safe-area-inset-bottom))]">
            {nav.primary.map((item) => (
              <div key={item.label} className="border-b border-line/70 last:border-0">
                <div className="flex items-center justify-between">
                  <Link href={item.url} className="py-3 text-[15px] font-semibold text-navy-800">
                    {item.label}
                  </Link>
                  {item.mega && (
                    <button
                      aria-label={`Expand ${item.label}`}
                      aria-expanded={mobileSection === item.label}
                      className="h-9 w-9 inline-flex items-center justify-center rounded-[10px] hover:bg-mist"
                      onClick={() => setMobileSection(mobileSection === item.label ? null : item.label)}
                    >
                      <ChevronDown
                        className={`h-4 w-4 transition-transform ${mobileSection === item.label ? "rotate-180" : ""}`}
                      />
                    </button>
                  )}
                </div>
                {item.mega && mobileSection === item.label && (
                  <div className="pb-4 space-y-4">
                    {item.mega.map((col) => {
                      const meta = colMeta(col.label);
                      const Icon = meta.icon;
                      return (
                        <div key={col.label + col.url}>
                          <Link href={col.url} className="flex items-center gap-2 text-[13px] font-semibold text-brand-deep">
                            <Icon className="h-3.5 w-3.5" aria-hidden="true" /> {col.label}
                          </Link>
                          {col.children.length > 0 && (
                            <ul className="mt-1.5 grid grid-cols-2 gap-x-3 gap-y-1 pl-3">
                              {col.children.map((ch) => (
                                <li key={ch.label + ch.url}>
                                  <Link href={ch.url} className="text-[12.5px] leading-snug text-slate-body/80">
                                    {ch.label}
                                  </Link>
                                </li>
                              ))}
                            </ul>
                          )}
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            ))}
            <Link
              href={nav.cta.url}
              className="mt-3 flex items-center justify-center rounded-[10px] bg-brand px-4 py-3 text-[14px] font-semibold text-white hover:bg-brand-hover"
            >
              {nav.cta.label}
            </Link>
          </div>
        </div>
      )}
      {/* sticky mobile CTA bar (CHG-362) */}
      <StickyMobileCTA cta={nav.cta} />

      {/* instant search overlay (CHG-359) */}
      {searchOpen && <SearchOverlay close={() => setSearchOpen(false)} />}
    </header>
  );
}
