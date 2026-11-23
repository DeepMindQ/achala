"use client";

/* ── Achala IT Solutions motion primitives (Wave 2, CHG-101/105/118/120/124/125/157/169/170)
   Shared in-view hook + scroll chrome + marquee. All animations respect the
   prefers-reduced-motion kill switch declared in globals.css.               */

import { useEffect, useRef, useState, useCallback } from "react";
import { ArrowUp } from "lucide-react";

/* ── shared IntersectionObserver hook (fires once) ────────────────────── */
export function useInView<T extends HTMLElement>(threshold = 0.25, margin = "0px 0px -60px 0px") {
  const ref = useRef<T | null>(null);
  const [inView, setInView] = useState(false);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const io = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          setInView(true);
          io.disconnect();
        }
      },
      { threshold, rootMargin: margin },
    );
    io.observe(el);
    return () => io.disconnect();
  }, [threshold, margin]);
  return { ref, inView };
}

/* ── Count-up on scroll (CHG-105/126) — renders the final value server-side
   (SEO + no-JS safe), animates from the start value only after mount.      */
function parseStat(value: string): { prefix: string; num: number; suffix: string; decimals: number } {
  const m = value.match(/^([^\d.,]*)([\d.,]+)(.*)$/);
  if (!m) return { prefix: "", num: 0, suffix: value, decimals: 0 };
  const raw = m[2].replace(/,/g, "");
  const decimals = raw.includes(".") ? raw.split(".")[1].length : 0;
  return { prefix: m[1], num: parseFloat(raw) || 0, suffix: m[3], decimals };
}

function fmt(n: number, decimals: number): string {
  return n.toLocaleString("en-US", { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
}

export function CountUp({
  value,
  className = "",
  duration = 1400,
}: {
  value: string;
  className?: string;
  duration?: number;
}) {
  const { ref, inView } = useInView<HTMLSpanElement>(0.4);
  const { prefix, num, suffix, decimals } = parseStat(value);
  // initial render: number part only (prefix/suffix are added by the wrapper)
  const [shown, setShown] = useState(() => fmt(num, decimals));
  const started = useRef(false);
  useEffect(() => {
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!inView || reduced || started.current) return;
    started.current = true;
    const t0 = performance.now();
    let raf = 0;
    const tick = (t: number) => {
      const p = Math.min(1, (t - t0) / duration);
      const eased = 1 - Math.pow(1 - p, 3);
      setShown(fmt(num * eased, decimals));
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [inView, num, decimals, duration]);
  return (
    <span ref={ref} className={`tabular-nums ${className}`}>
      {prefix}
      {shown}
      {suffix}
    </span>
  );
}

/* ── scroll progress bar (CHG-118) ────────────────────────────────────── */
export function ScrollProgress() {
  const [p, setP] = useState(0);
  useEffect(() => {
    const onScroll = () => {
      const h = document.documentElement;
      const max = h.scrollHeight - h.clientHeight;
      setP(max > 0 ? h.scrollTop / max : 0);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);
  return (
    <div aria-hidden="true" className="pointer-events-none fixed inset-x-0 top-0 z-[60] h-[3px]">
      <div
        className="h-full origin-left bg-gradient-to-r from-brand via-brand to-brand-300 transition-transform duration-150 ease-out"
        style={{ transform: `scaleX(${p})`, width: "100%" }}
      />
    </div>
  );
}

/* ── back-to-top control (CHG-120) ────────────────────────────────────── */
export function BackToTop() {
  const [show, setShow] = useState(false);
  useEffect(() => {
    const onScroll = () => setShow(window.scrollY > 720);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);
  const toTop = useCallback(() => window.scrollTo({ top: 0, behavior: "smooth" }), []);
  return (
    <button
      type="button"
      onClick={toTop}
      aria-label="Back to top"
      className={`fixed bottom-5 right-5 z-50 inline-flex h-11 w-11 items-center justify-center rounded-full border border-white/15 bg-navy-800 text-white shadow-3 transition-all duration-300 hover:bg-brand ${
        show ? "translate-y-0 opacity-100" : "pointer-events-none translate-y-3 opacity-0"
      }`}
    >
      <ArrowUp className="h-4.5 w-4.5" aria-hidden="true" />
    </button>
  );
}

/* ── marquee band (CHG-124/125/170): duplicated track, ARIA-safe, pauses on
   hover, collapses to a static wrapped row under reduced motion.           */
export function Marquee({
  items,
  dark = false,
  speed = 42,
  className = "",
}: {
  items: string[];
  dark?: boolean;
  speed?: number;
  className?: string;
}) {
  const row = (hidden: boolean) => (
    <ul
      aria-hidden={hidden || undefined}
      className="marquee-track flex shrink-0 items-center gap-10 pr-10"
    >
      {items.map((it, i) => (
        <li
          key={i}
          className={`flex shrink-0 items-center gap-3 whitespace-nowrap text-[12.5px] font-semibold uppercase tracking-[0.14em] ${
            dark ? "text-white/55" : "text-navy-800/60"
          }`}
        >
          <span aria-hidden="true" className={`h-1.5 w-1.5 rounded-full ${dark ? "bg-brand" : "bg-brand-deep/70"}`} />
          {it}
          {/* E-01: linear-text separator so reader mode / no-CSS reads
              "SOC 2 Type II · ISO 27001 · …" instead of run-on concatenation */}
          <span className="sr-only"> · </span>
        </li>
      ))}
    </ul>
  );
  return (
    <div
      className={`marquee group relative overflow-hidden py-3.5 ${className}`}
      style={{ ["--marquee-speed" as string]: `${speed}s` }}
    >
      <div className="marquee-inner flex w-max">
        {row(false)}
        {row(true)}
      </div>
    </div>
  );
}
