"use client";

import { useEffect, useRef, useState } from "react";

/* Hero slider — three rotating Achala stories (services / platforms / delivery).
 * SSR renders slide 0 (crawlers and no-JS see a complete hero). Each slide change
 * remounts the block so the existing rise/line-mask choreography replays; the
 * wrapper carries .is-visible the same way Reveal does. Pause on hover;
 * prefers-reduced-motion renders slide 1 statically. */

export type HeroSlide = {
  kicker: string;
  l1: string;
  l2a: string;
  l2grad: string;
  sub: string;
  proof: string;
  aria: string;
};

export default function HeroSlider({ slides }: { slides: HeroSlide[] }) {
  const [idx, setIdx] = useState(0);
  const [live, setLive] = useState(false);
  const hover = useRef(false);

  /* replay choreography on every slide change */
  useEffect(() => {
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced) {
      setLive(true);
      return;
    }
    setLive(false);
    const r = requestAnimationFrame(() => requestAnimationFrame(() => setLive(true)));
    return () => cancelAnimationFrame(r);
  }, [idx]);

  /* auto-advance unless hovered or reduced motion */
  useEffect(() => {
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced) return;
    const t = setInterval(() => {
      if (!hover.current) setIdx((i) => (i + 1) % slides.length);
    }, 7000);
    return () => clearInterval(t);
  }, [slides.length]);

  const s = slides[idx];

  return (
    <div onMouseEnter={() => (hover.current = true)} onMouseLeave={() => (hover.current = false)}>
      <div key={idx} className={`hero-slide${live ? " is-visible" : ""}`} aria-live="polite">
        <p
          className="rise-item text-[12px] font-semibold uppercase tracking-[0.22em] text-brand-300"
          style={{ ["--rise-delay" as string]: "40ms" }}
        >
          {s.kicker}
        </p>
        <h1 className="text-display-1 mt-4 max-w-none text-white">
          <span className="line-mask block" style={{ ["--rise-delay" as string]: "120ms" }}>
            <span className="line-mask-inner block">{s.l1}</span>
          </span>
          <span className="line-mask block" style={{ ["--rise-delay" as string]: "260ms" }}>
            <span className="line-mask-inner block">
              {s.l2a} <span className="grad-text">{s.l2grad}</span>.
            </span>
          </span>
        </h1>
        <p
          className="rise-item mt-5 text-body-lg leading-relaxed text-white/70"
          style={{ ["--rise-delay" as string]: "560ms" }}
        >
          {s.sub}
        </p>
        <p
          className="rise-item mt-5 inline-flex max-w-full items-center gap-2 rounded-full border border-white/15 bg-white/[0.06] px-4 py-1.5 text-[12.5px] font-medium text-white/80"
          style={{ ["--rise-delay" as string]: "660ms" }}
        >
          <span className="h-1.5 w-1.5 shrink-0 rounded-full bg-brand" aria-hidden="true" />
          {s.proof}
        </p>
      </div>

      {/* slide controls */}
      <div className="mt-7 flex items-center gap-3" role="tablist" aria-label="Hero stories">
        {slides.map((sl, i) => (
          <button
            key={sl.kicker}
            role="tab"
            aria-selected={i === idx}
            aria-label={sl.aria}
            onClick={() => setIdx(i)}
            className={`group relative h-1.5 rounded-full transition-all duration-500 ${
              i === idx ? "w-10 bg-brand" : "w-4 bg-white/25 hover:bg-white/50"
            }`}
          />
        ))}
        <span className="ml-1 text-[11px] tabular-nums text-white/40">
          {String(idx + 1).padStart(2, "0")} / {String(slides.length).padStart(2, "0")}
        </span>
      </div>
    </div>
  );
}
