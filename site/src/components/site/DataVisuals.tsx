"use client";

/* ── Achala IT Solutions data-visualization library (Wave 2, CHG-178/223 + output graphs)
   Pure SVG, brand-token colored, scroll-triggered draw animations, deterministic
   props (all data computed server-side → hydration-safe). Reduced motion: the
   globals.css kill switch drops every transition to instant.                 */

import { useRef, useState } from "react";
import { useInView } from "./Motion";
import { hashStr, mulberry32 } from "@/lib/seeded";

export const BRAND = "#d20000";
export const BRAND_SOFT = "#ff9d96";
export const NAVY = "#2b5672";
const NAVY_SOFT = "#568aa6";

type Dark = { dark?: boolean };

/* deterministic RNG lives in lib/seeded (server-safe); re-exported for compat */
export { hashStr, mulberry32 };

/* ── shared frame ─────────────────────────────────────────────────────── */
function Frame({
  title,
  caption,
  dark,
  children,
}: { title: string; caption?: string; dark?: boolean } & Dark & { children: React.ReactNode }) {
  return (
    <figure
      className={`dv-card overflow-hidden rounded-2xl border shadow-2 ${
        dark ? "border-white/10 bg-white/[0.05] backdrop-blur" : "border-line bg-white"
      }`}
    >
      <figcaption
        className={`flex flex-wrap items-center justify-between gap-2 border-b px-5 py-3.5 ${
          dark ? "border-white/10" : "border-line bg-mist/70"
        }`}
      >
        <span className={`text-[13px] font-semibold ${dark ? "text-white" : "text-navy-800"}`}>{title}</span>
        {caption && (
          <span className={`text-[10.5px] font-medium uppercase tracking-[0.14em] ${dark ? "text-brand-300" : "text-brand-deep"}`}>
            {caption}
          </span>
        )}
      </figcaption>
      <div className="px-5 py-5">{children}</div>
    </figure>
  );
}

/* ── shared hover tooltip (interactive charts) ─────────────────────────
   Absolutely-positioned readout that follows the hovered data index.
   Pure CSS transform positioning inside a relative wrapper — no layout shift. */
function ChartTip({
  left,
  dark,
  children,
}: {
  left: number; // 0..100 percentage inside the plot wrapper
  dark?: boolean;
  children: React.ReactNode;
}) {
  return (
    <div
      className="pointer-events-none absolute top-1 z-10 -translate-x-1/2 whitespace-nowrap rounded-lg px-2.5 py-1.5 text-[11px] leading-snug shadow-2"
      style={{
        left: `${Math.max(9, Math.min(91, left))}%`,
        background: dark ? "rgba(24,20,45,0.94)" : "rgba(24,20,45,0.94)",
        color: "#fff",
        border: "1px solid rgba(210,0,0,0.45)",
      }}
      role="status"
    >
      {children}
    </div>
  );
}

/* ── grouped bar chart (before/after or multi-metric) ─────────────────── */
export function BarChart({
  title,
  labels,
  series,
  unit = "",
  caption,
  dark,
  height = 210,
}: {
  title: string;
  labels: string[];
  series: { name: string; values: number[]; color?: string }[];
  unit?: string;
  caption?: string;
  height?: number;
} & Dark) {
  const { ref, inView } = useInView<HTMLDivElement>(0.3);
  const [hi, setHi] = useState<number | null>(null);
  const max = Math.max(...series.flatMap((s) => values1(s.values))) * 1.15 || 1;
  return (
    <div ref={ref}>
      <Frame title={title} caption={caption} dark={dark}>
        <div style={{ height }} className="flex items-end">
          <div className="relative flex h-full flex-1 flex-col">
            {hi !== null && (
              <ChartTip left={((hi + 0.5) / labels.length) * 100} dark={dark}>
                <span className="font-semibold">{labels[hi]}</span>
                {series.map((s, si) => (
                  <span key={s.name} className="ml-2 inline-flex items-center gap-1">
                    <span aria-hidden="true" className="h-1.5 w-1.5 rounded-full" style={{ background: s.color ?? (si === 0 ? NAVY_SOFT : BRAND) }} />
                    {s.values[hi]?.toLocaleString("en-US")}
                    {unit}
                  </span>
                ))}
              </ChartTip>
            )}
            <div className="flex h-full items-end gap-1">
              {labels.map((lb, gi) => (
                <div
                  key={lb}
                  className="flex h-full flex-1 cursor-pointer items-end justify-center gap-1.5"
                  onPointerEnter={() => setHi(gi)}
                  onPointerLeave={() => setHi((v) => (v === gi ? null : v))}
                  onFocus={() => setHi(gi)}
                  tabIndex={-1}
                >
                  {series.map((s, si) => {
                    const v = s.values[gi] ?? 0;
                    const h = Math.max(2, (v / max) * 100);
                    const active = hi === gi;
                    return (
                      <div key={si} className="relative flex h-full flex-1 max-w-[46px] flex-col justify-end">
                        <span
                          className={`absolute -top-5 w-full text-center text-[10.5px] font-semibold tabular-nums ${dark ? "text-white/80" : "text-navy-800"}`}
                          style={{
                            opacity: inView && (hi === null || active) ? 1 : 0.35,
                            transition: "opacity 500ms ease " + (si * 90 + gi * 90 + 350) + "ms",
                          }}
                        >
                          {v.toLocaleString("en-US")}
                          {unit}
                        </span>
                        <div
                          className="w-full rounded-t-[5px]"
                          style={{
                            height: `${h}%`,
                            background: s.color ?? (si === 0 ? NAVY : BRAND),
                            opacity: si === 0 && series.length > 1 ? (active ? 0.8 : 0.55) : 1,
                            filter: active ? "brightness(1.18)" : "none",
                            boxShadow: active ? "0 0 0 1.5px rgba(210,0,0,.5)" : "none",
                            transform: inView ? "scaleY(1)" : "scaleY(0)",
                            transformOrigin: "bottom",
                            transition: `transform 800ms cubic-bezier(.22,1,.36,1) ${si * 90 + gi * 90}ms, filter 200ms ease, box-shadow 200ms ease`,
                          }}
                        />
                      </div>
                    );
                  })}
                </div>
              ))}
            </div>
            <div className={`mt-2.5 flex gap-1 border-t pt-2 ${dark ? "border-white/10" : "border-line"}`}>
              {labels.map((lb) => (
                <span
                  key={lb}
                  className={`flex-1 text-center text-[10px] font-medium leading-tight ${dark ? "text-white/55" : "text-slate-body/70"}`}
                >
                  {lb}
                </span>
              ))}
            </div>
          </div>
        </div>
        {series.length > 1 && (
          <div className="mt-3 flex flex-wrap gap-4">
            {series.map((s, si) => (
              <span key={s.name} className={`flex items-center gap-1.5 text-[11px] ${dark ? "text-white/65" : "text-slate-body/75"}`}>
                <span aria-hidden="true" className="h-2 w-2 rounded-[3px]" style={{ background: s.color ?? (si === 0 ? NAVY : BRAND) }} />
                {s.name}
              </span>
            ))}
          </div>
        )}
      </Frame>
    </div>
  );
}
const values1 = (a: number[]) => (a.length ? a : [0]);

/* ── line + area chart (trend) ────────────────────────────────────────── */
export function LineArea({
  title,
  labels,
  series,
  unit = "",
  caption,
  dark,
  height = 210,
}: {
  title: string;
  labels: string[];
  series: { name: string; values: number[]; color?: string }[];
  unit?: string;
  caption?: string;
  height?: number;
} & Dark) {
  const { ref, inView } = useInView<HTMLDivElement>(0.3);
  const [hi, setHi] = useState<number | null>(null);
  const W = 560;
  const H = height;
  const pad = { l: 34, r: 12, t: 14, b: 26 };
  const all = series.flatMap((s) => s.values);
  const min = Math.min(0, ...all);
  const max = Math.max(...all) * 1.1 || 1;
  const x = (i: number, n: number) => pad.l + (i * (W - pad.l - pad.r)) / Math.max(1, n - 1);
  const y = (v: number) => pad.t + (1 - (v - min) / (max - min || 1)) * (H - pad.t - pad.b);
  const nPts = series[0]?.values.length ?? 0;
  const svgRef = useRef<SVGSVGElement | null>(null);
  const onMove = (e: React.PointerEvent<SVGSVGElement>) => {
    if (nPts < 2) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const vx = ((e.clientX - rect.left) / rect.width) * W;
    let best = 0;
    let bd = Infinity;
    for (let i = 0; i < nPts; i++) {
      const d = Math.abs(x(i, nPts) - vx);
      if (d < bd) {
        bd = d;
        best = i;
      }
    }
    setHi(best);
  };
  return (
    <div ref={ref}>
      <Frame title={title} caption={caption} dark={dark}>
        <div className="relative">
          {hi !== null && labels[hi] !== undefined && (
            <ChartTip left={((x(hi, nPts) - pad.l) / (W - pad.l - pad.r)) * 100} dark={dark}>
              <span className="font-semibold">{labels[hi]}</span>
              {series.map((s, si) => (
                <span key={s.name} className="ml-2 inline-flex items-center gap-1">
                  <span aria-hidden="true" className="h-1.5 w-1.5 rounded-full" style={{ background: s.color ?? (si === 0 ? BRAND : NAVY_SOFT) }} />
                  {s.values[hi]?.toLocaleString("en-US")}
                  {unit}
                </span>
              ))}
            </ChartTip>
          )}
          <svg
            ref={svgRef}
            viewBox={`0 0 ${W} ${H}`}
            className="w-full cursor-crosshair"
            role="img"
            aria-label={title}
            onPointerMove={onMove}
            onPointerLeave={() => setHi(null)}
          >
          {[0, 0.5, 1].map((g) => (
            <line
              key={g}
              x1={pad.l}
              x2={W - pad.r}
              y1={pad.t + g * (H - pad.t - pad.b)}
              y2={pad.t + g * (H - pad.t - pad.b)}
              stroke={dark ? "rgba(255,255,255,.12)" : "#E7E3F0"}
              strokeWidth="1"
            />
          ))}
          {series.map((s, si) => {
            const pts = s.values.map((v, i) => `${x(i, s.values.length)},${y(v)}`).join(" ");
            const line = `M${pts}`;
            const area = `${line} L${x(s.values.length - 1, s.values.length)},${H - pad.b} L${x(0, s.values.length)},${H - pad.b} Z`;
            const color = s.color ?? (si === 0 ? BRAND : NAVY_SOFT);
            return (
              <g key={si}>
                <path d={area} fill={color} opacity={inView ? 0.14 : 0} style={{ transition: "opacity 900ms ease 500ms" }} />
                <path
                  d={line}
                  fill="none"
                  stroke={color}
                  strokeWidth="2.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  pathLength={1}
                  strokeDasharray={1}
                  strokeDashoffset={inView ? 0 : 1}
                  style={{ transition: `stroke-dashoffset 1300ms cubic-bezier(.4,0,.2,1) ${si * 180}ms` }}
                />
                {s.values.map((v, i) => (
                  <circle
                    key={i}
                    cx={x(i, s.values.length)}
                    cy={y(v)}
                    r={hi === i ? 4.6 : 2.6}
                    fill={dark ? "#fff" : "#fff"}
                    stroke={color}
                    strokeWidth={hi === i ? "2.4" : "1.6"}
                    opacity={inView ? 1 : 0}
                    style={{ transition: `opacity 300ms ease ${700 + i * 60 + si * 180}ms, r 150ms ease, stroke-width 150ms ease` }}
                  />
                ))}
              </g>
            );
          })}
          {hi !== null && nPts > 0 && (
            <line
              x1={x(hi, nPts)}
              x2={x(hi, nPts)}
              y1={pad.t}
              y2={H - pad.b}
              stroke={dark ? "rgba(255,255,255,.35)" : "rgba(24,20,45,.3)"}
              strokeWidth="1"
              strokeDasharray="3 3"
              pointerEvents="none"
            />
          )}
          {labels.map((lb, i) =>
            i % Math.ceil(labels.length / 7) === 0 || i === labels.length - 1 ? (
              <text key={i} x={x(i, labels.length)} y={H - 8} textAnchor="middle" fontSize="9.5" fill={dark ? "rgba(255,255,255,.5)" : "#6B6580"}>
                {lb}
              </text>
            ) : null,
          )}
          <text x={pad.l - 6} y={pad.t + 4} textAnchor="end" fontSize="9" fill={dark ? "rgba(255,255,255,.5)" : "#6B6580"}>
            {Math.round(max).toLocaleString("en-US")}
            {unit}
          </text>
        </svg>
        </div>
        {series.length > 1 && (
          <div className="mt-1 flex flex-wrap gap-4">
            {series.map((s, si) => (
              <span key={s.name} className={`flex items-center gap-1.5 text-[11px] ${dark ? "text-white/65" : "text-slate-body/75"}`}>
                <span aria-hidden="true" className="h-[3px] w-4 rounded-full" style={{ background: s.color ?? (si === 0 ? BRAND : NAVY_SOFT) }} />
                {s.name}
              </span>
            ))}
          </div>
        )}
      </Frame>
    </div>
  );
}

/* ── donut (composition) ──────────────────────────────────────────────── */
export function Donut({
  title,
  segments,
  caption,
  dark,
  center,
}: {
  title: string;
  segments: { name: string; value: number; color?: string }[];
  caption?: string;
  center?: string;
} & Dark) {
  const { ref, inView } = useInView<HTMLDivElement>(0.35);
  const [hi, setHi] = useState<number | null>(null);
  const total = segments.reduce((a, s) => a + s.value, 0) || 1;
  const C = 2 * Math.PI * 40;
  let acc = 0;
  const palette = [BRAND, NAVY, BRAND_SOFT, NAVY_SOFT, "#8A82A6"];
  return (
    <div ref={ref}>
      <Frame title={title} caption={caption} dark={dark}>
        <div className="flex flex-col items-center gap-5 sm:flex-row">
          <svg viewBox="0 0 110 110" className="h-[132px] w-[132px] shrink-0 -rotate-90" role="img" aria-label={title}>
            <circle cx="55" cy="55" r="40" fill="none" stroke={dark ? "rgba(255,255,255,.1)" : "#EEEAF5"} strokeWidth="13" />
            {segments.map((s, i) => {
              const frac = s.value / total;
              const dash = `${inView ? frac * C : 0} ${C}`;
              const off = -acc * C;
              acc += frac;
              const dimmed = hi !== null && hi !== i;
              return (
                <circle
                  key={i}
                  cx="55"
                  cy="55"
                  r="40"
                  fill="none"
                  stroke={s.color ?? palette[i % palette.length]}
                  strokeWidth={hi === i ? 16 : 13}
                  strokeDasharray={dash}
                  strokeDashoffset={off}
                  opacity={dimmed ? 0.35 : 1}
                  className="cursor-pointer"
                  onPointerEnter={() => setHi(i)}
                  onPointerLeave={() => setHi((v) => (v === i ? null : v))}
                  style={{ transition: `stroke-dasharray 1000ms cubic-bezier(.22,1,.36,1) ${i * 160}ms, stroke-width 200ms ease, opacity 200ms ease` }}
                />
              );
            })}
          </svg>
          <div className="w-full space-y-2">
            {center && (
              <p className={`text-[20px] font-bold tabular-nums ${dark ? "text-white" : "text-navy-800"}`}>{center}</p>
            )}
            {segments.map((s, i) => (
              <div
                key={s.name}
                className={`flex items-center justify-between gap-3 rounded-md px-1.5 py-0.5 text-[12px] transition ${hi === i ? (dark ? "bg-white/10" : "bg-brand-tint") : ""}`}
                onPointerEnter={() => setHi(i)}
                onPointerLeave={() => setHi((v) => (v === i ? null : v))}
              >
                <span className={`flex items-center gap-2 ${hi === i ? (dark ? "text-white" : "text-navy-800 font-semibold") : dark ? "text-white/75" : "text-slate-body/85"}`}>
                  <span aria-hidden="true" className="h-2.5 w-2.5 rounded-full" style={{ background: s.color ?? palette[i % palette.length] }} />
                  {s.name}
                </span>
                <span className={`font-semibold tabular-nums ${dark ? "text-white/90" : "text-navy-800"}`}>
                  {Math.round((s.value / total) * 100)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      </Frame>
    </div>
  );
}

/* ── radar (capability scorecard) ─────────────────────────────────────── */
export function Radar({
  title,
  axes,
  series,
  caption,
  dark,
}: {
  title: string;
  axes: string[];
  series: { name: string; values: number[]; color?: string }[]; // values 0..100
  caption?: string;
} & Dark) {
  const { ref, inView } = useInView<HTMLDivElement>(0.3);
  const N = axes.length;
  const R = 78;
  const c = 110;
  const pt = (i: number, v: number) => {
    const a = (Math.PI * 2 * i) / N - Math.PI / 2;
    return [c + Math.cos(a) * R * (v / 100), c + Math.sin(a) * R * (v / 100)] as const;
  };
  return (
    <div ref={ref}>
      <Frame title={title} caption={caption} dark={dark}>
        <div className="flex flex-col items-center gap-4 sm:flex-row sm:items-start">
          <svg viewBox="0 0 220 220" className="h-[200px] w-[200px] shrink-0" role="img" aria-label={title}>
            {[25, 50, 75, 100].map((g) => (
              <polygon
                key={g}
                points={axes.map((_, i) => pt(i, g).join(",")).join(" ")}
                fill="none"
                stroke={dark ? "rgba(255,255,255,.1)" : "#E7E3F0"}
                strokeWidth="1"
              />
            ))}
            {axes.map((_, i) => (
              <line key={i} x1={c} y1={c} x2={pt(i, 100)[0]} y2={pt(i, 100)[1]} stroke={dark ? "rgba(255,255,255,.1)" : "#E7E3F0"} />
            ))}
            {series.map((s, si) => {
              const pts = s.values.map((v, i) => pt(i, v).join(",")).join(" ");
              return (
                <polygon
                  key={si}
                  points={pts}
                  fill={(s.color ?? (si === 0 ? BRAND : NAVY)) + "33"}
                  stroke={s.color ?? (si === 0 ? BRAND : NAVY)}
                  strokeWidth="2"
                  style={{
                    transformOrigin: "110px 110px",
                    transform: inView ? "scale(1)" : "scale(0.05)",
                    opacity: inView ? 1 : 0,
                    transition: `transform 900ms cubic-bezier(.22,1,.36,1) ${si * 150}ms, opacity 500ms ease ${si * 150}ms`,
                  }}
                />
              );
            })}
            {axes.map((a, i) => {
              const [px, py] = pt(i, 118);
              return (
                <text key={a} x={px} y={py} textAnchor="middle" dominantBaseline="middle" fontSize="8.5" fill={dark ? "rgba(255,255,255,.6)" : "#6B6580"}>
                  {a}
                </text>
              );
            })}
          </svg>
          <div className="space-y-2.5">
            {series.map((s, si) => (
              <div key={s.name}>
                <span className={`flex items-center gap-2 text-[12px] font-semibold ${dark ? "text-white" : "text-navy-800"}`}>
                  <span aria-hidden="true" className="h-2.5 w-2.5 rounded-full" style={{ background: s.color ?? (si === 0 ? BRAND : NAVY) }} />
                  {s.name}
                </span>
                <p className={`mt-0.5 text-[11px] tabular-nums ${dark ? "text-white/60" : "text-slate-body/70"}`}>
                  {axes.map((a, i) => `${a.split(" ")[0]} ${Math.round(s.values[i])}`).join(" · ")}
                </p>
              </div>
            ))}
          </div>
        </div>
      </Frame>
    </div>
  );
}

/* ── funnel (conversion / pipeline stages) ────────────────────────────── */
export function Funnel({
  title,
  stages,
  caption,
  dark,
}: {
  title: string;
  stages: { name: string; value: number }[];
  caption?: string;
} & Dark) {
  const { ref, inView } = useInView<HTMLDivElement>(0.3);
  const max = Math.max(...stages.map((s) => s.value)) || 1;
  return (
    <div ref={ref}>
      <Frame title={title} caption={caption} dark={dark}>
        <div className="space-y-2.5">
          {stages.map((s, i) => (
            <div key={s.name} className="flex items-center gap-3">
              <span className={`w-28 shrink-0 text-right text-[11.5px] font-medium leading-tight ${dark ? "text-white/70" : "text-slate-body/80"}`}>
                {s.name}
              </span>
              <div className={`relative h-7 flex-1 overflow-hidden rounded-md ${dark ? "bg-white/5" : "bg-mist"}`}>
                <div
                  className="flex h-full items-center justify-end rounded-md pr-2.5"
                  style={{
                    width: inView ? `${Math.max(14, (s.value / max) * 100)}%` : "4%",
                    background: `linear-gradient(90deg, ${BRAND}, ${BRAND_SOFT})`,
                    opacity: 1 - i * 0.14,
                    transition: `width 900ms cubic-bezier(.22,1,.36,1) ${i * 120}ms`,
                  }}
                >
                  <span className="text-[11px] font-bold tabular-nums text-white">{s.value.toLocaleString("en-US")}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </Frame>
    </div>
  );
}

/* ── network graph (agent / knowledge-graph mesh) ─────────────────────── */
export function NetworkGraph({
  title,
  nodes,
  links,
  caption,
  dark,
  height = 230,
}: {
  title: string;
  nodes: { id: string; x: number; y: number; hub?: boolean }[]; // 0..1 coordinates
  links: [number, number][];
  caption?: string;
  height?: number;
} & Dark) {
  const { ref, inView } = useInView<HTMLDivElement>(0.3);
  const W = 560;
  const H = height;
  const px = (n: { x: number }) => 24 + n.x * (W - 48);
  const py = (n: { y: number }) => 20 + n.y * (H - 40);
  return (
    <div ref={ref}>
      <Frame title={title} caption={caption} dark={dark}>
        <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img" aria-label={title}>
          {links.map(([a, b], i) => (
            <line
              key={i}
              x1={px(nodes[a])}
              y1={py(nodes[a])}
              x2={px(nodes[b])}
              y2={py(nodes[b])}
              stroke={dark ? "rgba(210, 0, 0,.5)" : "rgba(210, 0, 0,.45)"}
              strokeWidth="1.4"
              pathLength={1}
              strokeDasharray={1}
              strokeDashoffset={inView ? 0 : 1}
              style={{ transition: `stroke-dashoffset 800ms ease ${i * 70 + 200}ms` }}
            />
          ))}
          {nodes.map((n, i) => (
            <g key={n.id} style={{ opacity: inView ? 1 : 0, transition: `opacity 400ms ease ${i * 45}ms` }}>
              {n.hub && (
                <circle
                  cx={px(n)}
                  cy={py(n)}
                  r={13}
                  fill="none"
                  stroke={BRAND}
                  strokeWidth="1.4"
                  opacity={inView ? 0.5 : 0}
                  style={{ transition: "opacity 800ms ease 900ms" }}
                />
              )}
              <circle cx={px(n)} cy={py(n)} r={n.hub ? 8 : 4.5} fill={n.hub ? BRAND : NAVY} stroke={dark ? "#fff" : "#fff"} strokeWidth={n.hub ? 2 : 1} />
              <text x={px(n)} y={py(n) - 11} textAnchor="middle" fontSize="9" fontWeight="600" fill={dark ? "rgba(255,255,255,.85)" : NAVY}>
                {n.id}
              </text>
            </g>
          ))}
        </svg>
      </Frame>
    </div>
  );
}

/* ── heatmap (latency / utilization matrix) ───────────────────────────── */
export function Heatmap({
  title,
  rows,
  cols,
  matrix,
  caption,
  dark,
  unit = "",
}: {
  title: string;
  rows: string[];
  cols: string[];
  matrix: number[][];
  caption?: string;
  unit?: string;
} & Dark) {
  const { ref, inView } = useInView<HTMLDivElement>(0.3);
  const [hi, setHi] = useState<string | null>(null);
  const max = Math.max(...matrix.flat()) || 1;
  return (
    <div ref={ref}>
      <Frame title={title} caption={caption} dark={dark}>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[420px] border-separate border-spacing-[3px] text-[10.5px]">
            <thead>
              <tr>
                <th aria-hidden="true" />
                {cols.map((c) => (
                  <th key={c} className={`px-1 pb-1 font-semibold ${dark ? "text-white/60" : "text-slate-body/70"}`}>
                    {c}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((r, ri) => (
                <tr key={r}>
                  <td className={`pr-2 text-right font-medium ${dark ? "text-white/70" : "text-slate-body/80"}`}>{r}</td>
                  {matrix[ri].map((v, ci) => (
                    <td
                      key={ci}
                      className="cursor-pointer rounded-[4px] text-center font-semibold tabular-nums text-white"
                      title={`${r} · ${cols[ci]}: ${v.toLocaleString("en-US")}${unit}`}
                      onPointerEnter={() => setHi(`${ri}-${ci}`)}
                      onPointerLeave={() => setHi((cur) => (cur === `${ri}-${ci}` ? null : cur))}
                      style={{
                        background: `rgba(210, 0, 0, ${0.12 + 0.78 * (v / max)})`,
                        color: v / max > 0.55 || v / max < 0.2 ? (dark ? "#fff" : NAVY) : "#fff",
                        opacity: inView ? 1 : 0,
                        transform: inView ? (hi === `${ri}-${ci}` ? "scale(1.14)" : "scale(1)") : "scale(.6)",
                        boxShadow: hi === `${ri}-${ci}` ? "0 0 0 2px rgba(24,20,45,.55)" : "none",
                        transition: `opacity 500ms ease ${(ri * cols.length + ci) * 35}ms, transform 400ms ease ${(ri * cols.length + ci) * 35}ms, box-shadow 150ms ease`,
                      }}
                    >
                      {v.toLocaleString("en-US")}
                      {unit}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Frame>
    </div>
  );
}

/* ── gauge (SLA / utilization) ────────────────────────────────────────── */
export function Gauge({
  title,
  value,
  max = 100,
  unit = "%",
  caption,
  dark,
}: { title: string; value: number; max?: number; unit?: string; caption?: string } & Dark) {
  const { ref, inView } = useInView<HTMLDivElement>(0.4);
  const frac = Math.min(1, value / max);
  const C = Math.PI * 42;
  return (
    <div ref={ref}>
      <Frame title={title} caption={caption} dark={dark}>
        <div className="flex flex-col items-center">
          <svg viewBox="0 0 110 66" className="w-[190px]" role="img" aria-label={title}>
            <path d="M 13 58 A 42 42 0 0 1 97 58" fill="none" stroke={dark ? "rgba(255,255,255,.12)" : "#EEEAF5"} strokeWidth="11" strokeLinecap="round" />
            <path
              d="M 13 58 A 42 42 0 0 1 97 58"
              fill="none"
              stroke={BRAND}
              strokeWidth="11"
              strokeLinecap="round"
              pathLength={1}
              strokeDasharray={1}
              strokeDashoffset={inView ? 1 - frac : 1}
              style={{ transition: "stroke-dashoffset 1200ms cubic-bezier(.22,1,.36,1)" }}
            />
            <text x="55" y="52" textAnchor="middle" fontSize="15" fontWeight="700" fill={dark ? "#fff" : NAVY} className="tabular-nums">
              {value.toLocaleString("en-US")}
              {unit}
            </text>
          </svg>
        </div>
      </Frame>
    </div>
  );
}

/* ── sparkline (CHG-223) — inline card decoration ─────────────────────── */
export function Sparkline({ data, dark, className = "" }: { data: number[]; className?: string } & Dark) {
  const W = 120;
  const H = 34;
  const min = Math.min(...data);
  const max = Math.max(...data);
  const pts = data
    .map((v, i) => `${(i * W) / (data.length - 1)},${H - 4 - ((v - min) / (max - min || 1)) * (H - 8)}`)
    .join(" ");
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className={`w-[110px] ${className}`} aria-hidden="true">
      <polyline
        points={pts}
        fill="none"
        stroke={BRAND}
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        pathLength={1}
        strokeDasharray={1}
        strokeDashoffset={0}
      />
    </svg>
  );
}

/* ── architecture flow (CHG-152/132) — stacked layers with drawn connectors */
export function ArchitectureFlow({
  title,
  layers,
  caption,
  dark,
}: {
  title: string;
  layers: { name: string; nodes: string[] }[];
  caption?: string;
} & Dark) {
  const { ref, inView } = useInView<HTMLDivElement>(0.22);
  return (
    <div ref={ref}>
      <Frame title={title} caption={caption} dark={dark}>
        <div className="relative">
          {layers.map((l, i) => (
            <div key={l.name} className="relative">
              {i > 0 && (
                <div aria-hidden="true" className="flex justify-center py-1">
                  <svg width="26" height="18" viewBox="0 0 26 18">
                    <line
                      x1="13"
                      y1="0"
                      x2="13"
                      y2="14"
                      stroke={BRAND}
                      strokeWidth="2"
                      pathLength={1}
                      strokeDasharray={1}
                      strokeDashoffset={inView ? 0 : 1}
                      style={{ transition: `stroke-dashoffset 350ms ease ${i * 220 - 110}ms` }}
                    />
                    <path d="M 8 12 L 13 17 L 18 12" fill="none" stroke={BRAND} strokeWidth="2" style={{ opacity: inView ? 1 : 0, transition: `opacity 300ms ease ${i * 220}ms` }} />
                  </svg>
                </div>
              )}
              <div
                className={`rounded-xl border px-4 py-3 ${
                  dark ? "border-white/12 bg-white/[0.06]" : "border-line bg-mist/60"
                }`}
                style={{
                  opacity: inView ? 1 : 0,
                  transform: inView ? "translateY(0)" : "translateY(14px)",
                  transition: `opacity 600ms ease ${i * 220}ms, transform 600ms cubic-bezier(.22,1,.36,1) ${i * 220}ms`,
                }}
              >
                <p className={`text-[11px] font-bold uppercase tracking-[0.14em] ${dark ? "text-brand-300" : "text-brand-deep"}`}>{l.name}</p>
                <div className="mt-2 flex flex-wrap gap-1.5">
                  {l.nodes.map((n) => (
                    <span
                      key={n}
                      className={`rounded-md px-2 py-1 text-[11px] font-medium ${dark ? "bg-white/10 text-white/85" : "bg-white text-navy-800 border border-line"}`}
                    >
                      {n}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </Frame>
    </div>
  );
}

/* ── world map with office pins (CHG-186) ─────────────────────────────── */
export function WorldPins({
  title,
  pins,
  caption,
  dark,
}: {
  title: string;
  pins: { id: string; x: number; y: number }[]; // 0..1 normalized on the map box
  caption?: string;
} & Dark) {
  const { ref, inView } = useInView<HTMLDivElement>(0.3);
  const dots: { x: number; y: number }[] = [];
  const rng = mulberry32(7);
  for (let i = 0; i < 420; i++) dots.push({ x: rng(), y: 0.12 + rng() * 0.72 });
  return (
    <div ref={ref}>
      <Frame title={title} caption={caption} dark={dark}>
        <div className="relative overflow-hidden rounded-xl" style={{ aspectRatio: "2.1 / 1" }}>
          <svg viewBox="0 0 100 48" className="absolute inset-0 h-full w-full" aria-hidden="true">
            {dots.map((d, i) => (
              <circle key={i} cx={d.x * 100} cy={d.y * 48} r="0.45" fill={dark ? "rgba(255,255,255,.28)" : "rgba(43, 86, 114,.22)"} />
            ))}
            {pins.map((p, i) => (
              <g key={p.id} style={{ opacity: inView ? 1 : 0, transition: `opacity 500ms ease ${400 + i * 220}ms` }}>
                <circle cx={p.x * 100} cy={p.y * 48} r="1.9" fill={BRAND} />
                <circle cx={p.x * 100} cy={p.y * 48} r="3.4" fill="none" stroke={BRAND} strokeWidth="0.5" opacity="0.6">
                  <animate attributeName="r" values="2.4;4.4;2.4" dur="2.6s" begin={`${i * 0.5}s`} repeatCount="indefinite" />
                </circle>
              </g>
            ))}
          </svg>
          {pins.map((p) => (
            <span
              key={p.id}
              className="absolute -translate-x-1/2 whitespace-nowrap rounded-md px-1.5 py-0.5 text-[10px] font-semibold"
              style={{
                left: `${p.x * 100}%`,
                top: `calc(${p.y * 100}% - 24px)`,
                background: dark ? "rgba(43, 86, 114,.85)" : "rgba(43, 86, 114,.85)",
                color: "#fff",
              }}
            >
              {p.id}
            </span>
          ))}
        </div>
      </Frame>
    </div>
  );
}
