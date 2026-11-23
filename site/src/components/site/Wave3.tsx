"use client";

/* ── Wave 3 — Page Experience & Navigation client systems ───────────────
   CHG-258 floating pill · CHG-266/244/245 sliders · CHG-270/271 section
   anchors+dots · CHG-278 CTA dedupe · CHG-326 in-page TOC · CHG-327 reading
   progress (in Motion) · CHG-343/349/350 callouts · CHG-358/359/360 header
   search + instant results · CHG-361/362 drawer + sticky mobile CTA ·
   CHG-381 announcement bar · CHG-383 scroll restoration.                    */

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { ArrowRight, ArrowUpRight, CalendarDays, ChevronDown, ChevronLeft, ChevronRight, Quote as QuoteIcon, Search, Sparkles, X } from "lucide-react";
import { useInView } from "./Motion";

/* ── Skip-to-content (CHG-370) ────────────────────────────────────────── */
export function SkipLink() {
  return (
    <a
      href="#main-content"
      className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-[70] focus:rounded-lg focus:bg-brand focus:px-4 focus:py-2 focus:text-[13px] focus:font-semibold focus:text-white focus:shadow-3"
    >
      Skip to content
    </a>
  );
}

/* ── Announcement bar (CHG-381/264): dismissible, session-persisted ───── */
export function AnnouncementBar({ message, href }: { message: string; href: string }) {
  const [hidden, setHidden] = useState(true);
  useEffect(() => {
    try {
      setHidden(sessionStorage.getItem("dq-ann-closed") === "1");
    } catch {}
  }, []);
  if (hidden) return null;
  return (
    <div className="relative bg-brand text-white">
      <div className="container-dq flex h-9 items-center justify-center gap-2 text-[12.5px] font-medium">
        <Sparkles className="h-3.5 w-3.5 shrink-0" aria-hidden="true" />
        <Link href={href} className="min-w-0 truncate underline-offset-2 hover:underline">
          {message}
        </Link>
        <button
          type="button"
          aria-label="Dismiss announcement"
          className="absolute right-3 rounded-md p-1 hover:bg-white/15"
          onClick={() => {
            setHidden(true);
            try {
              sessionStorage.setItem("dq-ann-closed", "1");
            } catch {}
          }}
        >
          <X className="h-3.5 w-3.5" aria-hidden="true" />
        </button>
      </div>
    </div>
  );
}

/* ── Floating briefing pill — mobile CTA ergonomics (CHG-258/277/362) ─── */
export function StickyMobileCTA({ cta }: { cta: { label: string; url: string } }) {
  const [show, setShow] = useState(false);
  useEffect(() => {
    const onScroll = () => setShow(window.scrollY > 480);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);
  return (
    <div
      className={`fixed inset-x-3 bottom-3 z-50 transition-all duration-300 xl:hidden ${
        show ? "translate-y-0 opacity-100" : "pointer-events-none translate-y-4 opacity-0"
      }`}
    >
      <Link
        href={cta.url}
        className="btn-sheen flex items-center justify-center gap-2 rounded-xl bg-brand px-5 py-3 text-[13.5px] font-semibold text-white shadow-3"
        style={{ marginBottom: "env(safe-area-inset-bottom)" }}
      >
        {cta.label} <ArrowUpRight className="h-4 w-4" aria-hidden="true" />
      </Link>
    </div>
  );
}

/* (Phase 1 redesign) The in-page "On this page" TOC rail and the right-edge
   section dots were removed from the page template — they duplicated the
   hover anchor links and gave long pages a term-paper structure. Section
   navigation now lives in the breadcrumbs + hover anchors + related rails. */

/* ── Header instant search overlay (CHG-358/359/360) ──────────────────── */
type PfdResult = { url: string; meta: { title: string }; excerpt: string };
export function SearchOverlay({ close }: { close: () => void }) {
  const router = useRouter();
  const [q, setQ] = useState("");
  const [results, setResults] = useState<PfdResult[] | null>(null);
  const [status, setStatus] = useState<"idle" | "loading" | "none" | "ready" | "fallback">("idle");
  const inputRef = useRef<HTMLInputElement>(null);
  useEffect(() => {
    inputRef.current?.focus();
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && close();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [close]);
  const run = useCallback(async (query: string) => {
    if (query.trim().length < 2) {
      setResults(null);
      setStatus("idle");
      return;
    }
    setStatus("loading");
    try {
      const pf = await import(/* webpackIgnore: true */ "/pagefind/pagefind.js" as string).catch(() => null);
      if (!pf) throw new Error("no pagefind");
      await pf.options({ ranking: { pageLength: 12 } });
      const search = await pf.search(query);
      const out: PfdResult[] = [];
      for (const r of search.results.slice(0, 8)) {
        const d = await r.data();
        out.push({ url: d.url, meta: { title: d.meta?.title || d.url }, excerpt: d.excerpt?.replace(/<[^>]+>/g, "") || "" });
      }
      setResults(out);
      setStatus(out.length ? "ready" : "none");
    } catch {
      setStatus("fallback");
      router.push(`/search?q=${encodeURIComponent(query)}`);
      close();
    }
  }, [router, close]);
  return (
    <div className="fixed inset-0 z-[70]" role="dialog" aria-modal="true" aria-label="Search the site">
      <div className="absolute inset-0 bg-navy-950/60 backdrop-blur-sm" onClick={close} />
      <div className="absolute inset-x-4 top-16 mx-auto max-w-xl overflow-hidden rounded-2xl border border-line bg-white shadow-3 sm:inset-x-8">
        <div className="flex items-center gap-3 border-b border-line px-4 py-3">
          <Search className="h-4.5 w-4.5 shrink-0 text-brand-deep" aria-hidden="true" />
          <input
            ref={inputRef}
            value={q}
            onChange={(e) => {
              setQ(e.target.value);
              run(e.target.value);
            }}
            placeholder="Search services, industries, insights, case studies…"
            className="w-full bg-transparent text-[14px] text-navy-800 outline-none placeholder:text-slate-body/45"
            aria-label="Search query"
          />
          <button type="button" onClick={close} aria-label="Close search" className="rounded-md p-1 hover:bg-mist">
            <X className="h-4 w-4 text-slate-body/60" aria-hidden="true" />
          </button>
        </div>
        <div className="max-h-[52vh] overflow-y-auto">
          {status === "loading" && <p className="px-4 py-6 text-center text-[12.5px] text-slate-body/60">Searching…</p>}
          {status === "none" && (
            <p className="px-4 py-6 text-center text-[12.5px] text-slate-body/60">
              No matches. Try “fraud”, “lakehouse”, “zero trust”…
            </p>
          )}
          {results?.map((r) => (
            <Link
              key={r.url}
              href={r.url}
              onClick={close}
              className="block border-b border-line/60 px-4 py-3 transition hover:bg-brand-tint/60"
            >
              <span className="flex items-center justify-between gap-3">
                <span className="text-[13.5px] font-semibold text-navy-800">{r.meta.title}</span>
                <ArrowRight className="h-3.5 w-3.5 shrink-0 text-brand-deep" aria-hidden="true" />
              </span>
              <span className="mt-0.5 line-clamp-2 block text-[12px] leading-snug text-slate-body/70">{r.excerpt}</span>
            </Link>
          ))}
        </div>
        <p className="bg-mist/60 px-4 py-2 text-[10.5px] text-slate-body/55">
          Enter navigates to full results · Esc closes
        </p>
      </div>
    </div>
  );
}

/* ── Case spotlight slider (CHG-244/245/266) ──────────────────────────── */
export function SpotlightSlider({
  slides,
}: {
  slides: { title: string; url: string; desc: string; tag: string }[];
}) {
  const [i, setI] = useState(0);
  const n = slides.length;
  const go = useCallback((d: number) => setI((v) => (v + d + n) % n), [n]);
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "ArrowRight") go(1);
      if (e.key === "ArrowLeft") go(-1);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [go]);
  const s = slides[i];
  if (!s) return null;
  return (
    <div className="relative">
      <div className="overflow-hidden rounded-2xl border border-white/10 bg-white/[0.06] backdrop-blur">
        <div className="flex transition-transform duration-500 ease-out" style={{ transform: `translateX(-${i * 100}%)` }}>
          {slides.map((sl) => (
            <Link
              key={sl.url}
              href={sl.url}
              className="grid min-w-full gap-6 p-7 sm:grid-cols-[1fr_auto] sm:items-end sm:p-9"
            >
              <div>
                <span className="w-fit rounded-full bg-brand/15 px-2.5 py-0.5 text-[10.5px] font-semibold uppercase tracking-wider text-brand-300">
                  {sl.tag}
                </span>
                <p className="mt-3 max-w-2xl font-display text-[19px] font-semibold leading-snug text-white sm:text-[22px]">
                  {sl.title}
                </p>
                <p className="mt-2 max-w-2xl text-[13px] leading-relaxed text-white/65">{sl.desc}</p>
                <span className="mt-5 inline-flex items-center gap-1.5 text-[12.5px] font-semibold text-brand-300">
                  Read the engagement <ArrowRight className="h-4 w-4" aria-hidden="true" />
                </span>
              </div>
            </Link>
          ))}
        </div>
      </div>
      <div className="mt-4 flex items-center justify-between">
        <div className="flex gap-1.5" role="tablist" aria-label="Case slides">
          {slides.map((_, k) => (
            <button
              key={k}
              role="tab"
              aria-selected={k === i}
              aria-label={`Slide ${k + 1}`}
              onClick={() => setI(k)}
              className={`h-1.5 rounded-full transition-all duration-300 ${k === i ? "w-7 bg-brand" : "w-2.5 bg-white/25 hover:bg-white/45"}`}
            />
          ))}
        </div>
        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => go(-1)}
            aria-label="Previous case"
            className="inline-flex h-9 w-9 items-center justify-center rounded-full border border-white/20 text-white/75 transition hover:border-brand-300 hover:text-brand-300"
          >
            <ChevronLeft className="h-4 w-4" aria-hidden="true" />
          </button>
          <button
            type="button"
            onClick={() => go(1)}
            aria-label="Next case"
            className="inline-flex h-9 w-9 items-center justify-center rounded-full border border-white/20 text-white/75 transition hover:border-brand-300 hover:text-brand-300"
          >
            <ChevronRight className="h-4 w-4" aria-hidden="true" />
          </button>
        </div>
      </div>
    </div>
  );
}

/* ── Industry finder typeahead (CHG-243) ──────────────────────────────── */
export function IndustryFinder({
  industries,
}: {
  industries: { name: string; url: string }[];
}) {
  const [q, setQ] = useState("");
  const [open, setOpen] = useState(false);
  const hits = useMemo(
    () =>
      q.trim().length < 1
        ? industries.slice(0, 6)
        : industries.filter((x) => x.name.toLowerCase().includes(q.toLowerCase())).slice(0, 6),
    [q, industries],
  );
  return (
    <div className="relative">
      <div className="flex items-center gap-2 rounded-xl border border-line bg-white px-3.5 py-2.5 shadow-1 focus-within:border-brand">
        <Search className="h-4 w-4 text-slate-body/50" aria-hidden="true" />
        <input
          value={q}
          onChange={(e) => {
            setQ(e.target.value);
            setOpen(true);
          }}
          onFocus={() => setOpen(true)}
          onBlur={() => setTimeout(() => setOpen(false), 150)}
          placeholder="Find your industry — try “banking”, “health”…"
          aria-label="Find your industry"
          className="w-full bg-transparent text-[13.5px] text-navy-800 outline-none placeholder:text-slate-body/45"
        />
      </div>
      {open && (
        <ul className="absolute inset-x-0 top-full z-20 mt-1.5 overflow-hidden rounded-xl border border-line bg-white py-1 shadow-3">
          {hits.length === 0 && (
            <li className="px-4 py-2.5 text-[12.5px] text-slate-body/60">No industry matches — try the full grid below.</li>
          )}
          {hits.map((h) => (
            <li key={h.url}>
              <Link
                href={h.url}
                className="flex items-center justify-between px-4 py-2.5 text-[13px] font-medium text-navy-800 transition hover:bg-brand-tint hover:text-brand-deep"
              >
                {h.name}
                <ArrowRight className="h-3.5 w-3.5 text-brand-deep" aria-hidden="true" />
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

/* ── Interactive platform showcase tabs (CHG-240/241) ─────────────────── */
/* ── Interactive platform showcase tabs (CHG-240/241 + BG-046 dense rebuild) ──
   PLATFORM_EXTRAS is also consumed by the header mega-menu (platform preview).
   A-37 role (what the platform runs) · A-38 facts (measured, reference estate)
   · A-39 serves (the expertise domain the platform pairs with).           */
export const PLATFORM_EXTRAS: Record<
  string,
  { caps: string[]; method: string; role: string; facts: string; serves: { label: string; url: string }[] }
> = {
  Nexus: {
    caps: ["Streaming graph ingestion", "Replayable decision trail", "Contextual scoring at read time", "Policy-gated actions", "Board-ready evidence packs"],
    method: "Graph-native contextual core",
    role: "Runs decisions — in milliseconds, with the evidence attached",
    facts: "p95 148 ms · 100% of decisions replayable",
    serves: [{ label: "Applied AI & Generative AI", url: "/services/applied-ai-generative-ai/" }, { label: "Agentic AI & Hyperautomation", url: "/services/agentic-ai-hyperautomation/" }],
  },
  Forge: {
    caps: ["Tensor-manifold scheduling", "Log-complexity workload routing", "Energy-aware orchestration", "Fault-tolerant checkpointing", "Cost-per-decision economics"],
    method: "Quantum-inspired optimization core",
    role: "Runs the governed data estate every program depends on",
    facts: "0 lost rows across migration gates · 99.4% freshness SLA",
    serves: [{ label: "Data, Analytics & Lakehouse", url: "/services/data-analytics-lakehouse/" }, { label: "Cloud, Edge & Platform Engineering", url: "/services/cloud-edge-platform-engineering/" }],
  },
  Swarm: {
    caps: ["Multi-agent fleet control", "Shared-reward credit assignment", "Policy envelopes per agent", "Human handoff rails", "Validated decentralized execution"],
    method: "Generative knowledge-workflow blueprints",
    role: "Runs the agent workforce — hundreds of agents, one governed fleet",
    facts: "216 automations governed · 78% portfolio containment",
    serves: [{ label: "Agentic AI & Hyperautomation", url: "/services/agentic-ai-hyperautomation/" }],
  },
  Sentinel: {
    caps: ["Encrypted collaborative intelligence", "Byzantine-consensus trust fabric", "Zero-exposure defaults", "Continuous control validation", "Cross-party workflows"],
    method: "Privacy-preserving federated learning",
    role: "Guards access — for humans, machines and models",
    facts: "97.4% evidence freshness · 41/41 controls live",
    serves: [{ label: "Cybersecurity & Zero-Trust", url: "/services/cybersecurity-zero-trust/" }],
  },
  Twinverse: {
    caps: ["Multimodal sensor fusion", "Recalibration without retraining", "Edge-cloud latency routing", "Scenario replay", "Anomaly recognition at scale"],
    method: "Multimodal perception layer",
    role: "Mirrors physical operations — sense, simulate, act",
    facts: "1,842 assets instrumented · 99.7% fleet OTA success",
    serves: [{ label: "IoT, Digital Twin & Robotics", url: "/services/iot-digital-twin-robotics/" }],
  },
  Quanta: {
    caps: ["Quantum-walk state-space exploration", "Tensor processing units", "Riemannian clustering", "Temporal-logic verification", "Hybrid quantum-classical routing"],
    method: "Quantum-inspired optimization core",
    role: "Readies emerging compute with investor discipline",
    facts: "82% parallel efficiency · 100% benchmark honesty",
    serves: [{ label: "Quantum & Advanced Compute", url: "/services/quantum-advanced-compute/" }],
  },
  Ledger: {
    caps: ["Immutable audit chains", "Blockchain-integrated recovery", "Self-healing clusters", "zk-validated execution", "Consensus-gated releases"],
    method: "Byzantine-consensus trust fabric",
    role: "Anchors shared truth with regulatory teeth",
    facts: "0 reconciliation deltas · 412k credentials issued",
    serves: [{ label: "Blockchain & Digital Trust", url: "/services/blockchain-digital-trust/" }],
  },
  Compass: {
    caps: ["Self-evolving decision loops", "Reinforcement-optimized orchestration", "Knowledge-graph decision support", "Explainable stakeholder outputs", "Coherent distributed state"],
    method: "Multi-layer decision validation",
    role: "Keeps AI inspectable — approved by the model-risk committee",
    facts: "87% eval coverage · 68% PoC kill rate enforced",
    serves: [{ label: "Applied AI & Generative AI", url: "/services/applied-ai-generative-ai/" }],
  },
};

export function PlatformTabs({
  platforms,
}: {
  platforms: { name: string; url: string; desc: string }[];
  spark?: number[][];
}) {
  const [i, setI] = useState(0);
  const p = platforms[i];
  const key = p?.name.replace("Achala ", "") ?? "";
  const extra = PLATFORM_EXTRAS[key];
  if (!p) return null;
  return (
    <div className="overflow-hidden rounded-2xl border border-line bg-white shadow-2">
      <div className="flex flex-wrap gap-1 border-b border-line bg-mist/60 px-3 py-2.5" role="tablist" aria-label="Platform showcase">
        {platforms.map((pl, k) => (
          <button
            key={pl.url}
            role="tab"
            aria-selected={k === i}
            onClick={() => setI(k)}
            title={pl.desc /* A-37: role line per chip on hover/focus */}
            className={`rounded-lg px-3 py-1.5 text-[12px] font-semibold transition ${
              k === i ? "bg-navy-800 text-white" : "text-navy-800/70 hover:bg-white hover:text-brand-deep"
            }`}
          >
            {pl.name.replace("Achala ", "")}
          </button>
        ))}
      </div>
      <div className="grid gap-6 p-6 sm:p-7 lg:grid-cols-[minmax(0,5fr)_minmax(0,4fr)] lg:gap-7">
        {/* identity + promise + CTAs */}
        <div className="min-w-0">
          <p className="font-display text-[19px] font-semibold text-navy-800">{p.name}</p>
          <p className="mt-1 text-[11px] font-bold uppercase tracking-[0.14em] text-brand-deep">
            {extra?.method ?? "Patented method underneath"}
          </p>
          {/* A-37: role line — what this platform runs, in plain language */}
          <p className="mt-2 text-[12.5px] font-medium leading-snug text-slate-body/70">{extra?.role ?? p.desc}</p>
          <p className="mt-3 text-[13.5px] leading-relaxed text-slate-body/80">{p.desc}</p>
          {/* A-38: measured facts + provenance (E-05) */}
          {extra?.facts && (
            <p className="mt-3 flex flex-wrap items-center gap-2 text-[12.5px] font-semibold text-navy-800">
              <span className="rounded-md bg-navy-800 px-2 py-1 font-display text-[11.5px] text-white">{extra.facts}</span>
              <span className="rounded-full border border-line bg-mist/70 px-2 py-0.5 text-[9.5px] font-bold uppercase tracking-[0.12em] text-slate-body/60">
                Illustrative · reference program
              </span>
            </p>
          )}
          {/* A-39: reverse link — the expertise domain this platform serves */}
          {extra?.serves && (
            <p className="mt-2.5 flex flex-wrap items-center gap-1.5 text-[12px] text-slate-body/70">
              <span className="font-semibold text-navy-800">Serves:</span>
              {extra.serves.map((s, si) => (
                <span key={s.url} className="inline-flex items-center gap-1.5">
                  {si > 0 && <span className="text-slate-body/40">·</span>}
                  <Link href={s.url} className="link-animated font-medium text-brand-deep hover:underline">
                    {s.label}
                  </Link>
                </span>
              ))}
            </p>
          )}
          <div className="mt-5 flex flex-wrap gap-2.5">
            <Link
              href={p.url}
              className="btn-sheen inline-flex items-center gap-1.5 rounded-[10px] bg-brand px-4 py-2 text-[12.5px] font-semibold text-white hover:bg-brand-hover"
            >
              Enter {key} <ArrowRight className="h-3.5 w-3.5" aria-hidden="true" />
            </Link>
            <Link
              href="/patented-intelligence/"
              className="inline-flex items-center rounded-[10px] border border-line px-4 py-2 text-[12.5px] font-semibold text-navy-800 transition hover:border-brand hover:text-brand-deep"
            >
              The method underneath
            </Link>
          </div>
        </div>
        {/* capability list */}
        <div className="min-w-0 border-line lg:border-l lg:pl-6">
          <p className="text-[11px] font-bold uppercase tracking-[0.14em] text-slate-body/60">What it runs on your estate</p>
          <ul className="mt-3 space-y-2">
            {(extra?.caps ?? []).map((c) => (
              <li key={c} className="flex items-start gap-2 text-[12.5px] leading-snug text-navy-800/90">
                <span aria-hidden="true" className="mt-0.5 flex h-4 w-4 shrink-0 items-center justify-center rounded-full bg-brand-tint text-brand-deep">
                  <svg viewBox="0 0 10 10" className="h-2.5 w-2.5" fill="none" stroke="currentColor" strokeWidth="1.8"><path d="M1.5 5.5l2.2 2.2L8.5 2.8" /></svg>
                </span>
                {c}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

/* ═══════════════════════════════════════════════════════════════════════════
   Wave 1 homepage systems (A-03/40/41/43/52/54/56)
   ═══════════════════════════════════════════════════════════════════════════ */

/* ── RotatingProof (A-03): the three delivery vignettes, rotated ────────── */
export function RotatingProof({ lines }: { lines: string[] }) {
  const [i, setI] = useState(0);
  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const iv = setInterval(() => setI((v) => (v + 1) % lines.length), 3800);
    return () => clearInterval(iv);
  }, [lines.length]);
  return (
    <p className="mt-4 flex min-h-[20px] items-center gap-2 text-[12.5px] text-white/50" aria-live="polite">
      <style>{`@keyframes dq-rot-in { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: none; } }`}</style>
      <span className="inline-block h-1.5 w-1.5 shrink-0 rounded-full bg-brand" aria-hidden="true" />
      <span key={i} style={{ animation: "dq-rot-in .5s both" }} className="inline-block">{lines[i]}</span>
    </p>
  );
}

/* ── SectionRail (A-54): sticky right-edge section nav for the long page ── */
export function SectionRail({ items }: { items: { id: string; label: string }[] }) {
  const [active, setActive] = useState(items[0]?.id ?? "");
  const [hover, setHover] = useState<string | null>(null);
  useEffect(() => {
    const els = items.map((s) => document.getElementById(s.id)).filter(Boolean) as HTMLElement[];
    if (!els.length) return;
    const io = new IntersectionObserver(
      (entries) => {
        for (const e of entries) if (e.isIntersecting) setActive(e.target.id);
      },
      { rootMargin: "-30% 0px -55% 0px" },
    );
    els.forEach((el) => io.observe(el));
    return () => io.disconnect();
  }, [items]);
  return (
    <nav
      aria-label="Page sections"
      className="fixed right-4 top-1/2 z-40 hidden -translate-y-1/2 flex-col items-end gap-2.5 xl:flex"
    >
      {items.map((s) => {
        const on = active === s.id;
        const show = on || hover === s.id;
        return (
          <a
            key={s.id}
            href={`#${s.id}`}
            onMouseEnter={() => setHover(s.id)}
            onMouseLeave={() => setHover(null)}
            className="group flex items-center gap-2"
            aria-label={s.label}
            aria-current={on ? "true" : undefined}
          >
            <span
              className={`rounded-full bg-navy-800 px-2.5 py-1 text-[10.5px] font-semibold text-white shadow-2 transition-all duration-200 ${
                show ? "block opacity-100" : "hidden opacity-0"
              }`}
            >
              {s.label}
            </span>
            <span
              aria-hidden="true"
              className={`block rounded-full transition-all duration-200 ${
                on ? "h-2.5 w-2.5 bg-brand" : "h-1.5 w-1.5 bg-navy-800/25 group-hover:bg-brand/60"
              }`}
            />
          </a>
        );
      })}
    </nav>
  );
}

/* ── DomainRouter (A-52): three-question self-qualification path ───────── */
export type RouterOption = {
  key: string;
  label: string;
  blurb: string;
  domain: { label: string; url: string };
  practices: { label: string; url: string }[];
};

export function DomainRouter({ options }: { options: RouterOption[] }) {
  const [pick, setPick] = useState<string | null>(null);
  const sel = options.find((o) => o.key === pick) ?? null;
  return (
    <div className="mt-8 rounded-2xl border border-line bg-white p-5 shadow-1 sm:p-6">
      <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-brand-deep">Where does it hurt today?</p>
      <div className="mt-3 flex flex-wrap gap-2">
        {options.map((o) => (
          <button
            key={o.key}
            onClick={() => setPick(pick === o.key ? null : o.key)}
            aria-pressed={pick === o.key}
            className={`rounded-full px-4 py-2 text-[13px] font-semibold transition ${
              pick === o.key
                ? "bg-brand text-white"
                : "border border-line bg-mist/60 text-navy-800 hover:border-brand hover:text-brand-deep"
            }`}
          >
            {o.label}
          </button>
        ))}
      </div>
      {sel && (
        <div className="mt-4 rounded-xl border border-brand/30 bg-brand-tint/40 px-4 py-3.5">
          <p className="text-[13px] text-navy-800">
            <span className="font-semibold">{sel.blurb}</span> Start in{" "}
            <Link href={sel.domain.url} className="link-animated font-semibold text-brand-deep hover:underline">
              {sel.domain.label}
            </Link>
            :
          </p>
          <div className="mt-2 flex flex-wrap gap-2">
            {sel.practices.map((p) => (
              <Link
                key={p.url}
                href={p.url}
                className="inline-flex items-center gap-1 rounded-full border border-line bg-white px-3 py-1.5 text-[12.5px] font-medium text-navy-800 transition hover:border-brand hover:text-brand-deep"
              >
                {p.label} <ArrowRight className="h-3 w-3 text-brand-deep" aria-hidden="true" />
              </Link>
            ))}
          </div>
        </div>
      )}
      {!sel && (
        <p className="mt-3 text-[12px] leading-relaxed text-slate-body/60">
          Pick the surface that bleeds — the router links the matching domain and the two practices that fix it first.
        </p>
      )}
    </div>
  );
}

/* ── EvidenceGrid (A-40/41/43): filterable engagement-note grid ────────── */
export type EvidenceCard = {
  title: string;
  url: string;
  desc: string;
  tag: string;
  industry: string;
  service?: string;
  service_url?: string;
  gate?: string;
};

export function EvidenceGrid({
  cards,
  industries,
}: {
  cards: EvidenceCard[];
  industries: { name: string; count: number }[];
}) {
  const [filter, setFilter] = useState<string>("All");
  const shown = filter === "All" ? cards : cards.filter((c) => c.industry === filter);
  return (
    <div>
      {/* A-40: industry filter chips */}
      <div className="mt-2 flex flex-wrap gap-2" role="group" aria-label="Filter engagements by industry">
        <button
          onClick={() => setFilter("All")}
          aria-pressed={filter === "All"}
          className={`rounded-full px-3.5 py-1.5 text-[12.5px] font-semibold transition ${
            filter === "All" ? "bg-brand text-white" : "border border-white/20 bg-white/[0.06] text-white/75 hover:border-brand-300 hover:text-brand-300"
          }`}
        >
          All
        </button>
        {industries.map((ind) => (
          <button
            key={ind.name}
            onClick={() => setFilter(ind.name)}
            aria-pressed={filter === ind.name}
            className={`rounded-full px-3.5 py-1.5 text-[12.5px] font-semibold transition ${
              filter === ind.name ? "bg-brand text-white" : "border border-white/20 bg-white/[0.06] text-white/75 hover:border-brand-300 hover:text-brand-300"
            }`}
          >
            {ind.name} 
          </button>
        ))}
      </div>
      {/* A-40: grid of engagement notes */}
      <div className="mt-5 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
        {shown.map((c) => (
          <Link
            key={c.url}
            href={c.url}
            className="group flex flex-col rounded-xl border border-white/12 bg-white/[0.05] p-4 transition hover:border-brand-300/60 hover:bg-white/[0.09]"
          >
            <span className="w-fit rounded-full bg-brand/15 px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-wider text-brand-300">
              {c.tag}
            </span>
            <p className="mt-2.5 font-display text-[14.5px] font-semibold leading-snug text-white group-hover:text-brand-300">
              {c.title}
            </p>
            <p className="mt-1.5 flex-1 text-[12px] leading-relaxed text-white/60">{c.desc}</p>
            {/* A-41: the gates that governed the build */}
            {c.gate && (
              <span className="mt-3 w-fit rounded-md border border-white/15 px-2 py-1 text-[10.5px] font-semibold text-white/70">
                Gates: {c.gate}
              </span>
            )}
            {/* A-43: the delivering practice, named and linked */}
            {c.service && c.service_url && (
              <span className="mt-2 inline-flex items-center gap-1 text-[11.5px] font-medium text-white/50 group-hover:text-brand-300">
                Delivered by {c.service} <ArrowRight className="h-3 w-3" aria-hidden="true" />
              </span>
            )}
          </Link>
        ))}
      </div>
    </div>
  );
}

/* ── HomeIndustryExplorer (A-56): industry → top practices, compact ────── */
export type HomeExplorerIndustry = {
  name: string;
  url: string;
  regime: string;
  notes: number;
  practices: { label: string; url: string }[];
};

export function HomeIndustryExplorer({ industries }: { industries: HomeExplorerIndustry[] }) {
  const [i, setI] = useState(0);
  const sel = industries[i];
  if (!sel) return null;
  return (
    <div className="mt-8 overflow-hidden rounded-2xl border border-line bg-white shadow-2">
      <div className="flex flex-wrap gap-1.5 border-b border-line bg-mist/60 px-3 py-2.5" role="tablist" aria-label="Choose your industry">
        {industries.map((ind, k) => (
          <button
            key={ind.url}
            role="tab"
            aria-selected={k === i}
            onClick={() => setI(k)}
            className={`rounded-lg px-3 py-1.5 text-[12px] font-semibold transition ${
              k === i ? "bg-navy-800 text-white" : "text-navy-800/70 hover:bg-white hover:text-brand-deep"
            }`}
          >
            {ind.name.replace(" & ", " & ")}
          </button>
        ))}
      </div>
      <div className="grid gap-5 px-5 py-4 sm:px-6 lg:grid-cols-[minmax(0,3fr)_minmax(0,2fr)]">
        <div>
          <p className="flex flex-wrap items-center gap-2 font-display text-[15.5px] font-semibold text-navy-800">
            {sel.name}
            {sel.regime && (
              <span className="rounded-full bg-brand-tint px-2.5 py-0.5 text-[10.5px] font-bold uppercase tracking-wider text-brand-deep">
                {sel.regime}
              </span>
            )}
          </p>
          <p className="mt-1.5 text-[12.5px] leading-relaxed text-slate-body/70">
            Published engagement notes in this sector — these are the practices the notes credit.
          </p>
          <div className="mt-3 flex flex-col gap-2">
            {sel.practices.map((p) => (
              <Link
                key={p.url}
                href={p.url}
                className="group flex items-center justify-between gap-3 rounded-lg border border-line bg-mist/50 px-3.5 py-2.5 transition hover:border-brand/60 hover:bg-white"
              >
                <span className="text-[12.5px] font-medium text-navy-800 group-hover:text-brand-deep">{p.label}</span>
                <ArrowRight className="h-3.5 w-3.5 shrink-0 text-brand-deep transition group-hover:translate-x-0.5" aria-hidden="true" />
              </Link>
            ))}
          </div>
        </div>
        <div className="flex flex-col justify-between gap-3 border-line lg:border-l lg:pl-6">
          <div>
            <p className="text-[11px] font-bold uppercase tracking-[0.14em] text-slate-body/60">The sector brief</p>
            <p className="mt-2 text-[12.5px] leading-relaxed text-slate-body/75">
              Regulatory reality, decision pressure and the systems of record — mapped to the expertise domains on the industry hub.
            </p>
          </div>
          <Link
            href={sel.url}
            className="btn-sheen w-fit inline-flex items-center gap-1.5 rounded-[10px] bg-brand px-4 py-2 text-[12.5px] font-semibold text-white hover:bg-brand-hover"
          >
            Open the {sel.name.split(" ")[0].replace(",", "")} hub <ArrowRight className="h-3.5 w-3.5" aria-hidden="true" />
          </Link>
        </div>
      </div>
    </div>
  );
}
