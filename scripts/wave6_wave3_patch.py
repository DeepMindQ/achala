#!/usr/bin/env python3
"""Patch Wave3.tsx: autoplay SpotlightSlider w/ per-slide mini graphs,
animated tab panels, staggered evidence grid."""
import re, sys

P = "/home/z/my-project/site/src/components/site/Wave3.tsx"
src = open(P).read()

# ── 1. replace SpotlightSlider entirely (from its export to IndustryFinder comment)
start = src.index("export function SpotlightSlider({")
end = src.index("/* ── Industry finder typeahead")
new_slider = '''export function SpotlightSlider({
  slides,
}: {
  slides: { title: string; url: string; desc: string; tag: string }[];
}) {
  const [i, setI] = useState(0);
  const [hold, setHold] = useState(false);
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
  /* autoplay — pauses on hover / after manual nav / under reduced motion */
  useEffect(() => {
    if (hold) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const iv = setInterval(() => {
      if (!document.hidden) setI((v) => (v + 1) % n);
    }, 6000);
    return () => clearInterval(iv);
  }, [hold, n]);
  const s = slides[i];
  if (!s) return null;
  return (
    <div className="relative" onPointerEnter={() => setHold(true)} onPointerLeave={() => setHold(false)}>
      <div className="overflow-hidden rounded-2xl border border-white/10 bg-white/[0.06] backdrop-blur">
        <div className="flex transition-transform duration-500 ease-out" style={{ transform: `translateX(-${i * 100}%)` }}>
          {slides.map((sl, k) => {
            const mini = SLIDE_MINI[k % SLIDE_MINI.length];
            return (
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
                {/* each slide carries its own mini outcome graph — no two alike */}
                <MiniTrend
                  series={mini.series}
                  label={mini.label}
                  delta={mini.delta}
                  dir={mini.dir}
                  seed={k * 13 + 5}
                  active={k === i}
                />
              </Link>
            );
          })}
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
              onClick={() => {
                setI(k);
                setHold(true);
              }}
              className={`relative h-1.5 overflow-hidden rounded-full transition-all duration-300 ${
                k === i ? "w-9 bg-white/25" : "w-2.5 bg-white/25 hover:bg-white/45"
              }`}
            >
              {k === i && !hold && (
                <span
                  key={`bar-${i}-${n}`}
                  className="absolute inset-y-0 left-0 rounded-full bg-brand"
                  style={{ animation: "dq-slide-bar 6s linear both" }}
                />
              )}
              {k === i && hold && <span className="absolute inset-y-0 left-0 w-full rounded-full bg-brand" />}
            </button>
          ))}
        </div>
        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => {
              go(-1);
              setHold(true);
            }}
            aria-label="Previous case"
            className="inline-flex h-9 w-9 items-center justify-center rounded-full border border-white/20 text-white/75 transition hover:border-brand-300 hover:text-brand-300"
          >
            <ChevronLeft className="h-4 w-4" aria-hidden="true" />
          </button>
          <button
            type="button"
            onClick={() => {
              go(1);
              setHold(true);
            }}
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

/* ── per-slide outcome mini-graphs — three different shapes, derived from
   the three solution tracks the cases map to (fraud down / turnaround down / OEE up) */
const SLIDE_MINI: { series: number[]; label: string; delta: string; dir: "up" | "down" }[] = [
  {
    series: [92, 88, 84, 87, 78, 74, 70, 73, 65, 61, 64, 58, 55, 57, 52, 49, 51, 46, 44, 47, 42, 40, 38, 36],
    label: "Fraud losses per 1k txns",
    delta: "\\u221238%",
    dir: "down",
  },
  {
    series: [88, 85, 82, 84, 76, 72, 69, 71, 62, 58, 60, 54, 50, 52, 47, 43, 45, 40, 37, 39, 34, 31, 29, 27],
    label: "Claim turnaround, hours",
    delta: "\\u221255%",
    dir: "down",
  },
  {
    series: [38, 41, 40, 45, 48, 47, 52, 55, 54, 58, 61, 60, 64, 67, 66, 70, 72, 71, 75, 77, 76, 80, 82, 84],
    label: "OEE, %",
    delta: "+7.2 pts",
    dir: "up",
  },
];

/* animated, hover-interactive mini trend used inside the spotlight slides */
function MiniTrend({
  series,
  label,
  delta,
  dir,
  seed,
  active,
}: {
  series: number[];
  label: string;
  delta: string;
  dir: "up" | "down";
  seed: number;
  active: boolean;
}) {
  const [hi, setHi] = useState<number | null>(null);
  const W = 150;
  const H = 64;
  const PAD = 5;
  const pts = series.map(
    (v, k) => [PAD + (k * (W - PAD * 2)) / (series.length - 1), H - PAD - (v / 100) * (H - PAD * 2)] as const,
  );
  const line = pts.map(([px, py], k) => `${k === 0 ? "M" : "L"} ${px},${py}`).join(" ");
  const area = `${line} L ${W - PAD},${H - PAD} L ${PAD},${H - PAD} Z`;
  const good = dir === "up" ? "text-emerald-300" : "text-brand-300";
  return (
    <div className="hidden w-[170px] shrink-0 rounded-xl border border-white/10 bg-navy-950/60 p-3 sm:block">
      <p className="text-[9px] font-bold uppercase tracking-[0.13em] text-white/45">{label}</p>
      <div className="relative mt-1">
        {hi !== null && (
          <p
            role="status"
            className="pointer-events-none absolute -top-1 z-10 -translate-x-1/2 whitespace-nowrap rounded bg-navy-900 px-1.5 py-0.5 text-[9px] font-bold text-white shadow-2"
            style={{ left: `${Math.max(14, Math.min(86, (pts[hi][0] / W) * 100))}%` }}
          >
            {Math.round(series[hi])}
          </p>
        )}
        <svg
          viewBox={`0 0 ${W} ${H}`}
          className="h-[64px] w-full cursor-crosshair"
          aria-label={`${label}: ${delta} versus signed baseline`}
          onPointerMove={(e) => {
            const rect = e.currentTarget.getBoundingClientRect();
            const vx = ((e.clientX - rect.left) / rect.width) * W;
            let best = 0;
            let bd = Infinity;
            for (let j = 0; j < pts.length; j++) {
              const d = Math.abs(pts[j][0] - vx);
              if (d < bd) {
                bd = d;
                best = j;
              }
            }
            setHi(best);
          }}
          onPointerLeave={() => setHi(null)}
        >
          <path key={`a-${seed}`} d={area} fill="rgba(254,87,34,0.16)" style={{ animation: "oc-fade .9s ease .2s both" }} />
          <path
            key={`l-${seed}`}
            d={line}
            fill="none"
            stroke="#FE5722"
            strokeWidth="2"
            strokeLinecap="round"
            pathLength={1}
            strokeDasharray={1}
            style={{ animation: active ? "oc-draw 1.2s cubic-bezier(.4,0,.2,1) both" : undefined, strokeDashoffset: active ? undefined : 0 }}
          />
          {hi !== null && <circle cx={pts[hi][0]} cy={pts[hi][1]} r="3.4" fill="#fff" stroke="#FE5722" strokeWidth="2" />}
        </svg>
      </div>
      <p className={`mt-1 text-[11px] font-bold ${good}`}>{delta}</p>
      <p className="text-[8.5px] text-white/35">vs signed baseline \\u00b7 illustrative</p>
    </div>
  );
}

'''
src = src[:start] + new_slider + src[end:]

# ── 2. PlatformTabs panel: key + entrance animation
old = '''      <div className="grid gap-6 p-6 sm:p-7 lg:grid-cols-[minmax(0,5fr)_minmax(0,4fr)] lg:gap-7">
        {/* identity + promise + CTAs */}'''
new = '''      <div
        key={p.url}
        className="grid gap-6 p-6 sm:p-7 lg:grid-cols-[minmax(0,5fr)_minmax(0,4fr)] lg:gap-7"
        style={{ animation: "dq-panel-in .45s cubic-bezier(.22,1,.36,1) both" }}
      >
        {/* identity + promise + CTAs */}'''
assert src.count(old) == 1, f"platformtabs anchor: {src.count(old)}"
src = src.replace(old, new)

# ── 3. HomeIndustryExplorer panel: key + entrance animation
old = '''      <div className="grid gap-5 px-5 py-4 sm:px-6 lg:grid-cols-[minmax(0,3fr)_minmax(0,2fr)]">
        <div>
          <p className="flex flex-wrap items-center gap-2 font-display text-[15.5px] font-semibold text-navy-800">'''
new = '''      <div
        key={sel.url}
        className="grid gap-5 px-5 py-4 sm:px-6 lg:grid-cols-[minmax(0,3fr)_minmax(0,2fr)]"
        style={{ animation: "dq-panel-in .4s cubic-bezier(.22,1,.36,1) both" }}
      >
        <div>
          <p className="flex flex-wrap items-center gap-2 font-display text-[15.5px] font-semibold text-navy-800">'''
assert src.count(old) == 1, f"explorer anchor: {src.count(old)}"
src = src.replace(old, new)

# ── 4. EvidenceGrid: stagger + replay on filter change
old = '''      {/* A-40: grid of engagement notes */}
      <div className="mt-5 grid gap-3 md:grid-cols-2 xl:grid-cols-3">'''
new = '''      {/* A-40: grid of engagement notes — staggered entrance, replays on filter change */}
      <div key={filter} data-stagger className="mt-5 grid gap-3 md:grid-cols-2 xl:grid-cols-3">'''
assert src.count(old) == 1, f"evidence anchor: {src.count(old)}"
src = src.replace(old, new)

open(P, "w").write(src)
print("Wave3.tsx patched OK")
