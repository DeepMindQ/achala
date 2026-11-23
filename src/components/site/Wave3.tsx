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
        <Sparkles className="h-3.5 w-3.5" aria-hidden="true" />
        <Link href={href} className="underline-offset-2 hover:underline">
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

/* ── In-page TOC + section dots (CHG-326/270/271/355) ─────────────────── */
export function TableOfContents({ items }: { items: { id: string; text: string }[] }) {
  const [active, setActive] = useState(items[0]?.id ?? "");
  useEffect(() => {
    if (!items.length) return;
    const heads = items
      .map((it) => document.getElementById(it.id))
      .filter(Boolean) as HTMLElement[];
    if (!heads.length) return;
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) setActive(e.target.id);
        });
      },
      { rootMargin: "-72px 0px -62% 0px", threshold: 0 },
    );
    heads.forEach((h) => io.observe(h));
    return () => io.disconnect();
  }, [items]);
  if (items.length < 3) return null;
  return (
    <nav aria-label="On this page" className="sticky top-32 hidden max-h-[70vh] overflow-y-auto xl:block">
      <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-slate-body/50">On this page</p>
      <ul className="mt-3 space-y-1 border-l border-line">
        {items.map((it) => (
          <li key={it.id}>
            <a
              href={`#${it.id}`}
              aria-current={active === it.id ? "true" : undefined}
              className={`-ml-px block border-l-2 py-1.5 pl-3 text-[12px] leading-snug transition-colors ${
                active === it.id
                  ? "border-brand font-semibold text-brand-deep"
                  : "border-transparent text-slate-body/65 hover:border-line hover:text-navy-800"
              }`}
            >
              {it.text}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}

export function SectionDots({ sections }: { sections: { id: string; label: string }[] }) {
  const [active, setActive] = useState("");
  useEffect(() => {
    const els = sections
      .map((s) => document.getElementById(s.id))
      .filter(Boolean) as HTMLElement[];
    if (!els.length) return;
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) setActive(e.target.id);
        });
      },
      { rootMargin: "-45% 0px -45% 0px" },
    );
    els.forEach((el) => io.observe(el));
    return () => io.disconnect();
  }, [sections]);
  if (sections.length < 3) return null;
  return (
    <div
      aria-hidden="true"
      className="fixed right-5 top-1/2 z-40 hidden -translate-y-1/2 flex-col items-center gap-2.5 2xl:flex"
    >
      {sections.map((s) => (
        <a
          key={s.id}
          href={`#${s.id}`}
          title={s.label}
          className={`rounded-full transition-all duration-300 ${
            active === s.id ? "h-2.5 w-2.5 bg-brand" : "h-1.5 w-1.5 bg-navy-800/25 hover:bg-brand/60"
          }`}
        />
      ))}
    </div>
  );
}

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
            placeholder="Search 639 pages — services, industries, insights…"
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

/* ── Testimonial band (CHG-248) — rotating pull-quotes ────────────────── */
export function TestimonialBand({
  quotes,
}: {
  quotes: { text: string; who: string; role: string }[];
}) {
  const [i, setI] = useState(0);
  useEffect(() => {
    const t = setInterval(() => setI((v) => (v + 1) % quotes.length), 6500);
    return () => clearInterval(t);
  }, [quotes.length]);
  const q = quotes[i];
  return (
    <div className="relative overflow-hidden rounded-2xl border border-line bg-white px-6 py-9 shadow-2 sm:px-12">
      <QuoteIcon className="h-8 w-8 text-brand/40" aria-hidden="true" />
      <div className="relative mt-3 min-h-[96px]">
        {quotes.map((qq, k) => (
          <blockquote
            key={k}
            className={`absolute inset-0 font-display text-[17.5px] font-medium leading-relaxed text-navy-800 transition-all duration-700 sm:text-[19.5px] ${
              k === i ? "translate-y-0 opacity-100" : "pointer-events-none translate-y-3 opacity-0"
            }`}
          >
            “{qq.text}”
          </blockquote>
        ))}
      </div>
      <figcaption className="mt-4 flex items-center justify-between gap-4">
        <span className="flex items-center gap-2.5">
          <span aria-hidden="true" className="h-7 w-[3px] rounded-full bg-brand" />
          <span className="text-[12.5px]">
            <span className="block font-semibold text-navy-800">{q.who}</span>
            <span className="block text-slate-body/65">{q.role}</span>
          </span>
        </span>
        <span className="flex gap-1.5" aria-label={`Testimonial ${i + 1} of ${quotes.length}`}>
          {quotes.map((_, k) => (
            <button
              key={k}
              aria-label={`Show testimonial ${k + 1}`}
              onClick={() => setI(k)}
              className={`h-1.5 rounded-full transition-all ${k === i ? "w-6 bg-brand" : "w-1.5 bg-line hover:bg-brand/50"}`}
            />
          ))}
        </span>
      </figcaption>
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
export function PlatformTabs({
  platforms,
}: {
  platforms: { name: string; url: string; desc: string }[];
  spark?: number[][];
}) {
  const [i, setI] = useState(0);
  const p = platforms[i];
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
            className={`rounded-lg px-3 py-1.5 text-[12px] font-semibold transition ${
              k === i ? "bg-navy-800 text-white" : "text-navy-800/70 hover:bg-white hover:text-brand-deep"
            }`}
          >
            {pl.name.replace("Achala ", "")}
          </button>
        ))}
      </div>
      <div className="grid gap-6 p-6 sm:p-8 md:grid-cols-[1fr_auto] md:items-center">
        <div>
          <p className="font-display text-[19px] font-semibold text-navy-800">{p.name}</p>
          <p className="mt-2 max-w-2xl text-[13.5px] leading-relaxed text-slate-body/80">{p.desc}</p>
          <div className="mt-5 flex flex-wrap gap-2.5">
            <Link
              href={p.url}
              className="btn-sheen inline-flex items-center gap-1.5 rounded-[10px] bg-brand px-4 py-2 text-[12.5px] font-semibold text-white hover:bg-brand-hover"
            >
              Enter {p.name.replace("Achala ", "")} <ArrowRight className="h-3.5 w-3.5" aria-hidden="true" />
            </Link>
            <Link
              href="/patented-intelligence/"
              className="inline-flex items-center rounded-[10px] border border-line px-4 py-2 text-[12.5px] font-semibold text-navy-800 transition hover:border-brand hover:text-brand-deep"
            >
              Patent underneath
            </Link>
          </div>
        </div>
        {/* mini capability bars per platform — deterministic from name */}
        <MiniBars seed={p.name} />
      </div>
    </div>
  );
}

function MiniBars({ seed }: { seed: string }) {
  let h = 2166136261;
  for (let i = 0; i < seed.length; i++) {
    h ^= seed.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  const rng = (n: number) => {
    let a = (h >>> 0) + n * 0x9e3779b9;
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  const bars = ["Throughput", "Precision", "Resilience", "Governance"].map((label, n) => ({
    label,
    v: Math.round(68 + rng(n) * 28),
  }));
  return (
    <div className="min-w-[190px] space-y-2.5" aria-hidden="true">
      {bars.map((b, n) => (
        <div key={b.label}>
          <div className="flex justify-between text-[10.5px] font-semibold text-slate-body/60">
            <span>{b.label}</span>
            <span className="tabular-nums">{b.v}</span>
          </div>
          <div className="mt-1 h-2 overflow-hidden rounded-full bg-mist">
            <div
              className="h-full rounded-full bg-gradient-to-r from-navy-800 to-brand transition-all duration-700"
              style={{ width: `${b.v}%`, transitionDelay: `${n * 90}ms` }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}

/* ── Scroll restoration on route change (CHG-383) ─────────────────────── */
export function ScrollRestoration() {
  const router = useRouter();
  useEffect(() => {
    const handler = () => window.scrollTo(0, 0);
    // Next App Router restores scroll by default on popstate; ensure pushes go to top
    window.history.scrollRestoration = "manual";
    const origPush = router.push;
    return () => {
      window.history.scrollRestoration = "auto";
    };
  }, [router]);
  return null;
}
