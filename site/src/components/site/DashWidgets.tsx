"use client";

import { useMemo, useState } from "react";

/* ═══════════════════════════════════════════════════════════════════════════
   DashWidgets — interactive, PhD-grade widgets for service delivery consoles.
   Every widget takes its data from the page JSON (static-export safe,
   hydration-safe: no Date/Math.random in render). Interactivity: hover
   crosshairs, legend toggles, clickable nodes/stages, sliders driving
   derived physics-style formulas, sortable tables.

   Widget kinds (see DashSuite for the console frame):
     line    hover crosshair + tooltip + legend toggle
     bar     grouped bars, hover tooltip, click-to-isolate series
     radar   profile polygons with series toggles
     heat    intensity matrix with hover cell readout panel
     donut   composition with hover center readout + pin
     gauge   threshold-band gauge cluster
     slo     error-budget burn simulator (sliders → burn rate → ETA)
     sim     what-if simulator (sliders → formula outputs + response curve)
     flow    pipeline stepper: click stage → detail panel
     arch    interactive topology: click node → detail panel
     table   sortable + filterable evidence table
     scatter decision map with group legend + hover
   ═══════════════════════════════════════════════════════════════════════════ */

const ORANGE = "#d20000";
const PALETTE = [
  "#d20000",
  "rgba(255,255,255,0.92)",
  "rgba(254,140,80,0.85)",
  "rgba(255,255,255,0.55)",
  "rgba(210, 0, 0,0.45)",
  "rgba(160,190,255,0.75)",
];

export type Series = { name: string; points: number[] };

export type DashWidget =
  | { kind: "line"; title: string; cats: string[]; series: Series[]; unit?: string; yMax?: number; note?: string }
  | { kind: "bar"; title: string; cats: string[]; series: Series[]; unit?: string; yMax?: number; note?: string }
  | { kind: "radar"; title: string; cats: string[]; series: Series[]; yMax?: number; note?: string }
  | { kind: "heat"; title: string; rows: string[]; cats: string[]; matrix: number[][]; unit?: string; note?: string }
  | { kind: "donut"; title: string; cats: string[]; points: number[]; unit?: string; note?: string }
  | {
      kind: "gauge";
      title: string;
      items: { name: string; value: number; max: number; unit: string; warn?: number; crit?: number }[];
      note?: string;
    }
  | {
      kind: "slo";
      title: string;
      target: number; // e.g. 99.95
      windowDays: number;
      traffic: number; // default req/s
      errPct: number; // default error %
      note?: string;
    }
  | {
      kind: "sim";
      title: string;
      params: { name: string; min: number; max: number; step: number; value: number; unit: string }[];
      outputs: { name: string; unit: string; formula: string; good?: string; bad?: string }[];
      curve?: { param: number; output: number; label: string };
      note?: string;
    }
  | {
      kind: "flow";
      title: string;
      stages: { name: string; role: string; detail: string; metrics: { label: string; value: string }[] }[];
      note?: string;
    }
  | {
      kind: "arch";
      title: string;
      lanes: string[];
      nodes: { id: string; lane: number; label: string; detail: string; hot?: boolean }[];
      edges: { a: string; b: string; label?: string }[];
      note?: string;
    }
  | { kind: "table"; title: string; headers: string[]; rows: string[][]; note?: string }
  | {
      kind: "scatter";
      title: string;
      points: { x: number; y: number; label: string; group: string }[];
      groups: string[];
      xLabel: string;
      yLabel: string;
      xMax?: number;
      yMax?: number;
      note?: string;
    };

export type DashKpiSpec = {
  label: string;
  value: string;
  delta?: string;
  dir?: "up" | "down" | "flat";
  spark?: number[];
};

/* ── shared frame pieces ─────────────────────────────────────────────────── */

export function WidgetHead({ title, badge }: { title: string; badge?: string }) {
  return (
    <div className="mb-3 flex items-center justify-between gap-3">
      <p className="text-[12.5px] font-semibold leading-snug text-white">{title}</p>
      {badge && (
        <span className="shrink-0 rounded-full border border-white/15 bg-white/[0.06] px-2.5 py-0.5 text-[9.5px] font-bold uppercase tracking-[0.14em] text-white/55">
          {badge}
        </span>
      )}
    </div>
  );
}

export function WidgetNote({ children }: { children?: React.ReactNode }) {
  if (!children) return null;
  return <p className="mt-2.5 text-[11px] leading-relaxed text-white/45">{children}</p>;
}

const fmtNum = (v: number) =>
  Math.abs(v) >= 1000 ? v.toLocaleString("en-US", { maximumFractionDigits: 0 }) : String(Math.round(v * 100) / 100);

/* ── line — hover crosshair + tooltip + legend toggle ────────────────────── */

function LineWidget({ w }: { w: Extract<DashWidget, { kind: "line" }> }) {
  const [off, setOff] = useState<Set<string>>(new Set());
  const [hi, setHi] = useState<number | null>(null);
  const show = (name: string) => !off.has(name);
  const vis = w.series.filter((s) => show(s.name));
  const maxV = w.yMax ?? (Math.max(...w.series.flatMap((s) => s.points)) * 1.12 || 1);

  const W = 620;
  const H = 216;
  const PL = 42;
  const PR = 12;
  const PT = 12;
  const PB = 30;
  const iw = W - PL - PR;
  const ih = H - PT - PB;
  const n = Math.max(w.cats.length - 1, 1);
  const x = (i: number) => PL + (i * iw) / n;
  const y = (v: number) => PT + ih - (Math.min(v, maxV) / maxV) * ih;

  const path = (pts: number[]) =>
    pts.map((v, i) => `${i === 0 ? "M" : "L"} ${x(i).toFixed(1)} ${y(v).toFixed(1)}`).join(" ");

  return (
    <div>
      <WidgetHead title={w.title} badge="Interactive trend" />
      <div className="relative rounded-xl border border-white/10 bg-navy-950/50 p-1">
        <svg
          viewBox={`0 0 ${W} ${H}`}
          className="h-auto w-full"
          onMouseMove={(e) => {
            const r = e.currentTarget.getBoundingClientRect();
            const px = ((e.clientX - r.left) / r.width) * W;
            const i = Math.round(((px - PL) / iw) * n);
            setHi(Math.max(0, Math.min(w.cats.length - 1, i)));
          }}
          onMouseLeave={() => setHi(null)}
        >
          {[0, 0.25, 0.5, 0.75, 1].map((f) => (
            <g key={f}>
              <line x1={PL} x2={W - PR} y1={PT + f * ih} y2={PT + f * ih} stroke="rgba(255,255,255,0.07)" strokeWidth={1} />
              <text x={PL - 6} y={PT + f * ih + 3.5} fontSize={9} fill="rgba(255,255,255,0.4)" textAnchor="end">
                {fmtNum(maxV * (1 - f))}
              </text>
            </g>
          ))}
          {w.cats.map((c, i) => (
            <text key={c + i} x={x(i)} y={H - 10} fontSize={9} fill="rgba(255,255,255,0.45)" textAnchor="middle">
              {c}
            </text>
          ))}
          {hi !== null && (
            <line x1={x(hi)} x2={x(hi)} y1={PT} y2={PT + ih} stroke="rgba(210, 0, 0,0.55)" strokeDasharray="3 4" strokeWidth={1.2} />
          )}
          {vis.map((s, si) => (
            <g key={s.name}>
              <path d={path(s.points)} fill="none" stroke={PALETTE[(w.series.indexOf(s)) % PALETTE.length]} strokeWidth={2} strokeLinejoin="round" />
              {hi !== null && (
                <circle cx={x(hi)} cy={y(s.points[Math.min(hi, s.points.length - 1)])} r={3.5} fill={PALETTE[(w.series.indexOf(s)) % PALETTE.length]} stroke="#1a1533" strokeWidth={1.5} />
              )}
              {si === vis.length - 1 && (
                <path
                  d={`M ${PL} ${PT + ih} ${path(vis[0].points)} L ${W - PR} ${PT + ih} Z`}
                  fill={PALETTE[0]}
                  opacity={0.07}
                />
              )}
            </g>
          ))}
        </svg>
        {hi !== null && (
          <div
            className="pointer-events-none absolute top-2 rounded-lg border border-white/15 bg-navy-950/95 px-3 py-2 shadow-2"
            style={{ left: `${Math.min(72, (x(hi) / W) * 100)}%` }}
          >
            <p className="text-[10px] font-bold uppercase tracking-wider text-white/55">{w.cats[hi]}</p>
            {vis.map((s, i) => (
              <p key={s.name} className="mt-0.5 flex items-center gap-1.5 text-[11px] text-white/85">
                <span className="inline-block h-1.5 w-1.5 rounded-full" style={{ background: PALETTE[(w.series.indexOf(s)) % PALETTE.length] }} />
                {s.name}: <b className="tabular-nums">{fmtNum(s.points[Math.min(hi, s.points.length - 1)])}</b>
                {w.unit && <span className="text-white/45">{w.unit}</span>}
                {i === 99 && null}
              </p>
            ))}
          </div>
        )}
      </div>
      <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1">
        {w.series.map((s, i) => (
          <button
            key={s.name}
            onClick={() => {
              const nx = new Set(off);
              if (nx.has(s.name)) nx.delete(s.name);
              else if (vis.length > 1) nx.add(s.name);
              setOff(nx);
            }}
            className={`inline-flex items-center gap-1.5 rounded px-1.5 py-0.5 text-[10.5px] font-medium transition ${
              show(s.name) ? "text-white/80 hover:text-white" : "text-white/30 line-through"
            }`}
          >
            <span className="inline-block h-[3px] w-4 rounded-full" style={{ background: show(s.name) ? PALETTE[i % PALETTE.length] : "rgba(255,255,255,0.25)" }} />
            {s.name}
            {w.unit && <span className="text-white/40">{w.unit}</span>}
          </button>
        ))}
      </div>
      <WidgetNote>{w.note}</WidgetNote>
    </div>
  );
}

/* ── bar — grouped bars, hover tooltip, click-to-isolate ─────────────────── */

function BarWidget({ w }: { w: Extract<DashWidget, { kind: "bar" }> }) {
  const [sel, setSel] = useState<number | null>(null);
  const [hi, setHi] = useState<{ s: number; c: number } | null>(null);
  const maxV = w.yMax ?? (Math.max(...w.series.flatMap((s) => s.points)) * 1.12 || 1);
  const W = 620;
  const H = 216;
  const PL = 42;
  const PR = 12;
  const PT = 12;
  const PB = 30;
  const iw = W - PL - PR;
  const ih = H - PT - PB;
  const groupW = iw / Math.max(w.cats.length, 1);
  const bw = Math.min(30, (groupW - 14) / Math.max(w.series.length, 1));
  const y = (v: number) => PT + ih - (Math.min(v, maxV) / maxV) * ih;

  return (
    <div>
      <WidgetHead title={w.title} badge={sel === null ? "Hover · click legend" : "Isolated: " + w.series[sel].name} />
      <div className="relative rounded-xl border border-white/10 bg-navy-950/50 p-1">
        <svg viewBox={`0 0 ${W} ${H}`} className="h-auto w-full">
          {[0, 0.5, 1].map((f) => (
            <g key={f}>
              <line x1={PL} x2={W - PR} y1={PT + f * ih} y2={PT + f * ih} stroke="rgba(255,255,255,0.07)" />
              <text x={PL - 6} y={PT + f * ih + 3.5} fontSize={9} fill="rgba(255,255,255,0.4)" textAnchor="end">
                {fmtNum(maxV * (1 - f))}
              </text>
            </g>
          ))}
          {w.cats.map((c, ci) => (
            <g key={c + ci}>
              <text x={PL + groupW * ci + groupW / 2} y={H - 10} fontSize={9} fill="rgba(255,255,255,0.45)" textAnchor="middle">
                {c}
              </text>
              {w.series.map((s, si) => {
                if (sel !== null && sel !== si) return null;
                const v = s.points[Math.min(ci, s.points.length - 1)];
                const bx = PL + groupW * ci + groupW / 2 - (bw * w.series.length) / 2 + si * bw + 1;
                const by = y(v);
                const active = hi && hi.s === si && hi.c === ci;
                return (
                  <rect
                    key={si}
                    x={bx}
                    y={by}
                    width={bw - 2}
                    height={PT + ih - by}
                    rx={3}
                    fill={PALETTE[si % PALETTE.length]}
                    opacity={active ? 1 : 0.82}
                    stroke={active ? "rgba(255,255,255,0.85)" : "none"}
                    strokeWidth={1}
                    onMouseEnter={() => setHi({ s: si, c: ci })}
                    onMouseLeave={() => setHi(null)}
                    style={{ transition: "opacity .15s" }}
                  />
                );
              })}
            </g>
          ))}
        </svg>
        {hi && (
          <div className="pointer-events-none absolute right-2 top-2 rounded-lg border border-white/15 bg-navy-950/95 px-3 py-1.5 shadow-2">
            <p className="text-[10px] text-white/55">{w.cats[hi.c]} · {w.series[hi.s].name}</p>
            <p className="text-[13px] font-bold tabular-nums text-white">
              {fmtNum(w.series[hi.s].points[Math.min(hi.c, w.series[hi.s].points.length - 1)])}
              <span className="ml-1 text-[10px] font-medium text-white/45">{w.unit}</span>
            </p>
          </div>
        )}
      </div>
      <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1">
        {w.series.map((s, i) => (
          <button
            key={s.name}
            onClick={() => setSel(sel === i ? null : i)}
            className={`inline-flex items-center gap-1.5 rounded px-1.5 py-0.5 text-[10.5px] font-medium transition ${
              sel === null || sel === i ? "text-white/80 hover:text-white" : "text-white/30"
            }`}
          >
            <span className="inline-block h-[3px] w-4 rounded-full" style={{ background: PALETTE[i % PALETTE.length] }} />
            {s.name}
          </button>
        ))}
      </div>
      <WidgetNote>{w.note}</WidgetNote>
    </div>
  );
}

/* ── radar — profile polygons + series toggles ───────────────────────────── */

function RadarWidget({ w }: { w: Extract<DashWidget, { kind: "radar" }> }) {
  const [off, setOff] = useState<Set<string>>(new Set());
  const vis = w.series.filter((s) => !off.has(s.name));
  const maxV = w.yMax ?? 100;
  const cx = 150;
  const cy = 108;
  const R = 82;
  const nC = w.cats.length;
  const pt = (i: number, f: number) => {
    const a = (Math.PI * 2 * i) / nC - Math.PI / 2;
    return { x: cx + Math.cos(a) * R * f, y: cy + Math.sin(a) * R * f };
  };
  const poly = (pts: number[]) =>
    pts.map((v, i) => { const p = pt(i, Math.min(v, maxV) / maxV); return `${p.x.toFixed(1)},${p.y.toFixed(1)}`; }).join(" ");

  return (
    <div>
      <WidgetHead title={w.title} badge="Toggle series" />
      <div className="flex flex-col items-center gap-2 rounded-xl border border-white/10 bg-navy-950/50 p-2 sm:flex-row">
        <svg viewBox="0 0 300 216" className="h-auto w-full max-w-[300px]">
          {[0.25, 0.5, 0.75, 1].map((f) => (
            <polygon
              key={f}
              points={w.cats.map((_, i) => { const p = pt(i, f); return `${p.x},${p.y}`; }).join(" ")}
              fill="none"
              stroke="rgba(255,255,255,0.09)"
            />
          ))}
          {w.cats.map((c, i) => {
            const p = pt(i, 1.16);
            return (
              <g key={c + i}>
                <line x1={cx} y1={cy} x2={pt(i, 1).x} y2={pt(i, 1).y} stroke="rgba(255,255,255,0.07)" />
                <text x={p.x} y={p.y + 3} fontSize={8.5} fill="rgba(255,255,255,0.55)" textAnchor="middle">
                  {c}
                </text>
              </g>
            );
          })}
          {vis.map((s) => {
            const idx = w.series.indexOf(s);
            return (
              <g key={s.name}>
                <polygon points={poly(s.points)} fill={PALETTE[idx % PALETTE.length]} opacity={0.16} stroke={PALETTE[idx % PALETTE.length]} strokeWidth={1.8} />
                {s.points.map((v, i) => {
                  const p = pt(i, Math.min(v, maxV) / maxV);
                  return <circle key={i} cx={p.x} cy={p.y} r={2.4} fill={PALETTE[idx % PALETTE.length]} />;
                })}
              </g>
            );
          })}
        </svg>
        <div className="flex flex-col gap-1">
          {w.series.map((s, i) => {
            const on = !off.has(s.name);
            const avg = s.points.reduce((a, b) => a + b, 0) / s.points.length;
            return (
              <button
                key={s.name}
                onClick={() => {
                  const nx = new Set(off);
                  if (nx.has(s.name)) nx.delete(s.name);
                  else if (vis.length > 1) nx.add(s.name);
                  setOff(nx);
                }}
                className={`flex items-center justify-between gap-3 rounded-lg border px-2.5 py-1.5 text-left transition ${
                  on ? "border-white/15 bg-white/[0.06]" : "border-white/5 bg-transparent opacity-40"
                }`}
              >
                <span className="flex items-center gap-1.5 text-[11px] font-medium text-white/80">
                  <span className="inline-block h-[3px] w-4 rounded-full" style={{ background: on ? PALETTE[i % PALETTE.length] : "rgba(255,255,255,0.25)" }} />
                  {s.name}
                </span>
                <span className="text-[11px] font-bold tabular-nums text-brand-300">{avg.toFixed(0)}</span>
              </button>
            );
          })}
        </div>
      </div>
      <WidgetNote>{w.note}</WidgetNote>
    </div>
  );
}

/* ── heat — intensity matrix + hover cell readout ────────────────────────── */

function HeatWidget({ w }: { w: Extract<DashWidget, { kind: "heat" }> }) {
  const [cell, setCell] = useState<{ r: number; c: number } | null>(null);
  const max = Math.max(...w.matrix.flat()) || 1;
  const sel = cell ? w.matrix[cell.r]?.[Math.min(cell.c, w.matrix[cell.r].length - 1)] : null;
  return (
    <div>
      <WidgetHead title={w.title} badge="Hover cells" />
      <div className="flex gap-3 rounded-xl border border-white/10 bg-navy-950/50 p-3">
        <div className="min-w-0 flex-1 overflow-x-auto">
          <table className="w-full border-separate" style={{ borderSpacing: "3px" }}>
            <tbody>
              {w.rows.map((r, ri) => (
                <tr key={r}>
                  <td className="whitespace-nowrap pr-1.5 text-right text-[10px] font-medium text-white/60">{r}</td>
                  {w.cats.map((c, ci) => {
                    const v = w.matrix[ri]?.[ci] ?? 0;
                    const f = v / max;
                    const active = cell && cell.r === ri && cell.c === ci;
                    return (
                      <td key={c + ci}>
                        <div
                          onMouseEnter={() => setCell({ r: ri, c: ci })}
                          onMouseLeave={() => setCell(null)}
                          className="flex h-8 cursor-crosshair items-center justify-center rounded text-[10.5px] font-bold tabular-nums transition"
                          style={{
                            background: `rgba(210, 0, 0,${0.08 + f * 0.8})`,
                            color: f > 0.45 ? "#fff" : "rgba(255,255,255,0.75)",
                            outline: active ? "1.5px solid rgba(255,255,255,0.9)" : "none",
                          }}
                        >
                          {v}
                        </div>
                      </td>
                    );
                  })}
                </tr>
              ))}
              <tr>
                <td />
                {w.cats.map((c) => (
                  <td key={c} className="pt-1 text-center text-[9px] font-medium leading-tight text-white/50">{c}</td>
                ))}
              </tr>
            </tbody>
          </table>
        </div>
        <div className="w-44 shrink-0 rounded-lg border border-white/10 bg-white/[0.04] p-3">
          {cell && sel !== null ? (
            <>
              <p className="text-[10px] font-bold uppercase tracking-wider text-brand-300">{w.rows[cell.r]}</p>
              <p className="text-[10px] text-white/50">{w.cats[Math.min(cell.c, w.cats.length - 1)]}</p>
              <p className="mt-1.5 font-display text-[22px] font-bold tabular-nums text-white">
                {sel}
                <span className="ml-1 text-[11px] font-medium text-white/45">{w.unit}</span>
              </p>
              <div className="mt-1.5 h-1.5 overflow-hidden rounded-full bg-white/10">
                <div className="h-full rounded-full bg-brand" style={{ width: `${(sel / max) * 100}%` }} />
              </div>
              <p className="mt-1.5 text-[9.5px] leading-snug text-white/40">
                {(sel / max * 100).toFixed(0)}% of {fmtNum(max)} {w.unit} max across the matrix
              </p>
            </>
          ) : (
            <p className="text-[11px] leading-relaxed text-white/45">
              Hover a cell to read the exact intensity. Darker cells carry the heaviest load or risk — sequencing follows the color.
            </p>
          )}
        </div>
      </div>
      <WidgetNote>{w.note}</WidgetNote>
    </div>
  );
}

/* ── donut — composition with hover center readout + pin ─────────────────── */

function DonutWidget({ w }: { w: Extract<DashWidget, { kind: "donut" }> }) {
  const [pin, setPin] = useState<number | null>(null);
  const [hov, setHov] = useState<number | null>(null);
  const total = w.points.reduce((a, b) => a + b, 0) || 1;
  const active = hov ?? pin;
  const R = 74;
  const C = 2 * Math.PI * R;
  let acc = 0;
  const arcs = w.points.map((v, i) => {
    const frac = v / total;
    const seg = { i, v, frac, dash: `${(frac * C).toFixed(1)} ${(C - frac * C).toFixed(1)}`, off: C * (1 - acc) + C * 0.25 };
    acc += frac;
    return seg;
  });
  return (
    <div>
      <WidgetHead title={w.title} badge="Composition" />
      <div className="flex flex-col items-center gap-3 rounded-xl border border-white/10 bg-navy-950/50 p-3 sm:flex-row sm:gap-4">
        <svg viewBox="0 0 200 200" className="h-auto w-full max-w-[200px] shrink-0">
          <g transform="translate(100,100) rotate(-90)">
            <circle r={R} fill="none" stroke="rgba(255,255,255,0.07)" strokeWidth={22} />
            {arcs.map((a) => (
              <circle
                key={a.i}
                r={R}
                fill="none"
                stroke={PALETTE[a.i % PALETTE.length]}
                strokeWidth={active === a.i ? 26 : 22}
                strokeDasharray={a.dash}
                strokeDashoffset={a.off}
                strokeLinecap="butt"
                opacity={active === null || active === a.i ? 0.92 : 0.3}
                onMouseEnter={() => setHov(a.i)}
                onMouseLeave={() => setHov(null)}
                onClick={() => setPin(pin === a.i ? null : a.i)}
                className="cursor-pointer"
                style={{ transition: "stroke-width .15s, opacity .15s" }}
              />
            ))}
          </g>
          <text x={100} y={95} textAnchor="middle" fontSize={22} fontWeight={700} fill="#fff" className="tabular-nums">
            {active !== null ? `${((w.points[active] / total) * 100).toFixed(1)}%` : fmtNum(total)}
          </text>
          <text x={100} y={114} textAnchor="middle" fontSize={9.5} fill="rgba(255,255,255,0.5)">
            {active !== null ? w.cats[active] : w.unit || "total"}
          </text>
        </svg>
        <div className="grid w-full grid-cols-1 gap-1 sm:grid-cols-1">
          {w.cats.map((c, i) => (
            <button
              key={c}
              onMouseEnter={() => setHov(i)}
              onMouseLeave={() => setHov(null)}
              onClick={() => setPin(pin === i ? null : i)}
              className={`flex items-center justify-between gap-2 rounded-lg px-2.5 py-1.5 text-left transition ${
                active === i ? "bg-white/[0.08]" : "hover:bg-white/[0.04]"
              }`}
            >
              <span className="flex min-w-0 items-center gap-2 text-[11px] font-medium text-white/75">
                <span className="h-2.5 w-2.5 shrink-0 rounded-sm" style={{ background: PALETTE[i % PALETTE.length] }} />
                <span className="truncate">{c}</span>
              </span>
              <span className="shrink-0 text-[11px] font-bold tabular-nums text-white/85">
                {((w.points[i] / total) * 100).toFixed(1)}%
              </span>
            </button>
          ))}
        </div>
      </div>
      <WidgetNote>{w.note}</WidgetNote>
    </div>
  );
}

/* ── gauge — threshold-band cluster ──────────────────────────────────────── */

function GaugeWidget({ w }: { w: Extract<DashWidget, { kind: "gauge" }> }) {
  const arc = (v: number, max: number, warn?: number, crit?: number) => {
    const f = Math.max(0.02, Math.min(1, v / max));
    const a = Math.PI * (1 - f);
    const r1 = 44;
    const x1 = 50 + Math.cos(a) * r1;
    const y1 = 50 - Math.sin(a) * r1;
    const large = f > 0.5 ? 1 : 0;
    const col = crit !== undefined && v >= crit ? "#f87171" : warn !== undefined && v >= warn ? "#facc15" : "#d20000";
    return { d: `M 6 50 A ${r1} ${r1} 0 ${large} 1 ${x1.toFixed(1)} ${y1.toFixed(1)}`, col, f };
  };
  return (
    <div>
      <WidgetHead title={w.title} badge="Live bands" />
      <div className="grid grid-cols-2 gap-2 rounded-xl border border-white/10 bg-navy-950/50 p-3 sm:grid-cols-4">
        {w.items.map((it, i) => {
          const a = arc(it.value, it.max, it.warn, it.crit);
          return (
            <div key={it.name} className="rounded-lg border border-white/10 bg-white/[0.04] px-2 py-2.5 text-center">
              <svg viewBox="0 0 100 54" className="mx-auto h-auto w-full max-w-[120px]">
                <path d="M 6 50 A 44 44 0 0 1 94 50" fill="none" stroke="rgba(255,255,255,0.09)" strokeWidth={9} strokeLinecap="round" />
                {it.crit !== undefined && (
                  <path
                    d={`M ${50 + Math.cos(Math.PI * (1 - it.crit / it.max)) * 44} ${50 - Math.sin(Math.PI * (1 - it.crit / it.max)) * 44} A 44 44 0 ${it.crit / it.max > 0.5 ? 1 : 0} 1 94 50`}
                    fill="none"
                    stroke="rgba(248,113,113,0.35)"
                    strokeWidth={9}
                  />
                )}
                <path d={a.d} fill="none" stroke={a.col} strokeWidth={9} strokeLinecap="round" style={{ transition: "d .4s" }} />
                <text x={50} y={47} textAnchor="middle" fontSize={13} fontWeight={700} fill="#fff" className="tabular-nums">
                  {it.value.toLocaleString("en-US", { maximumFractionDigits: 1 })}
                </text>
              </svg>
              <p className="mt-0.5 text-[10px] font-semibold leading-tight text-white/70">{it.name}</p>
              <p className="text-[9px] text-white/40">
                {it.unit} · cap {fmtNum(it.max)}
              </p>
              <p className="text-[9px] font-bold" style={{ color: a.col }}>
                {(a.f * 100).toFixed(0)}% of cap
              </p>
              <span className="hidden">{i}</span>
            </div>
          );
        })}
      </div>
      <WidgetNote>{w.note}</WidgetNote>
    </div>
  );
}

/* ── tiny formula engine for the sim widget (no eval) ────────────────────── */

function evalFormula(src: string, env: Record<string, number>): number {
  const s = src.replace(/\s+/g, "");
  let i = 0;
  const peek = () => s[i];
  const eat = (c: string) => {
    if (s[i] === c) { i++; return true; }
    return false;
  };
  const num = (): number => {
    let st = i;
    while (i < s.length && /[0-9.]/.test(s[i])) i++;
    return parseFloat(s.slice(st, i));
  };
  const ident = (): string => {
    let st = i;
    while (i < s.length && /[a-zA-Z0-9_]/.test(s[i])) i++;
    return s.slice(st, i);
  };
  const primary = (): number => {
    if (eat("-")) return -primary();
    if (eat("(")) { const v = expr(); eat(")"); return v; }
    if (/[0-9.]/.test(peek() ?? "")) return num();
    const id = ident();
    if (id in env) return env[id];
    // function call: collect comma-separated args properly
    const args: number[] = [];
    if (eat("(")) {
      args.push(expr());
      while (eat(",")) args.push(expr());
      eat(")");
    }
    let r = args[0] ?? 0;
    switch (id) {
      case "min": r = Math.min(...args); break;
      case "max": r = Math.max(...args); break;
      case "sqrt": r = Math.sqrt(r); break;
      case "abs": r = Math.abs(r); break;
      case "log": r = Math.log(r); break;
      case "exp": r = Math.exp(r); break;
      case "pow": r = Math.pow(args[0] ?? 0, args[1] ?? 1); break;
      default: break;
    }
    return r;
  };
  const power = (): number => {
    const b = primary();
    if (eat("^")) return Math.pow(b, power());
    return b;
  };
  const term = (): number => {
    let v = power();
    for (;;) {
      if (eat("*")) v *= power();
      else if (eat("/")) v /= power() || 1;
      else return v;
    }
  };
  const expr = (): number => {
    let v = term();
    for (;;) {
      if (eat("+")) v += term();
      else if (eat("-")) v -= term();
      else return v;
    }
  };
  const out = expr();
  return isFinite(out) ? out : 0;
}

/* ── sim — what-if simulator: sliders → formula outputs + response curve ─── */

function SimWidget({ w }: { w: Extract<DashWidget, { kind: "sim" }> }) {
  const [vals, setVals] = useState<number[]>(() => w.params.map((p) => p.value));
  const env = useMemo(() => {
    const e: Record<string, number> = {};
    w.params.forEach((p, i) => (e[`p${i}`] = vals[i]));
    return e;
  }, [vals, w.params]);
  const outs = w.outputs.map((o) => ({ spec: o, v: evalFormula(o.formula, env) }));

  const curve = useMemo(() => {
    if (!w.curve) return null;
    const p = w.params[w.curve.param];
    const steps = 40;
    const pts: { x: number; y: number }[] = [];
    for (let k = 0; k <= steps; k++) {
      const xv = p.min + ((p.max - p.min) * k) / steps;
      const e = { ...env, [`p${w.curve.param}`]: xv };
      pts.push({ x: xv, y: evalFormula(w.outputs[w.curve.output].formula, e) });
    }
    return pts;
  }, [env, w]);

  const W = 560;
  const H = 170;
  const PL = 46;
  const PR = 14;
  const PT = 12;
  const PB = 28;
  const iw = W - PL - PR;
  const ih = H - PT - PB;
  let cPath = "";
  let curPt = "";
  if (curve && curve.length) {
    const ys = curve.map((q) => q.y);
    const ymin = Math.min(...ys);
    const ymax = Math.max(...ys);
    const span = ymax - ymin || 1;
    const px = (xv: number) => {
      const p = w.params[w.curve!.param];
      return PL + ((xv - p.min) / (p.max - p.min)) * iw;
    };
    const py = (yv: number) => PT + ih - ((yv - ymin) / span) * ih;
    cPath = curve.map((q, k) => `${k === 0 ? "M" : "L"} ${px(q.x).toFixed(1)} ${py(q.y).toFixed(1)}`).join(" ");
    const cx = px(vals[w.curve.param]);
    const cyv = py(evalFormula(w.outputs[w.curve.output].formula, env));
    curPt = `M ${cx} ${PT + ih} L ${cx} ${cyv}`;
    cPath += `||${curPt}||${cx.toFixed(1)},${cyv.toFixed(1)},${vals[w.curve.param].toFixed(1)}`;
  }

  return (
    <div>
      <WidgetHead title={w.title} badge="What-if model" />
      <div className="grid gap-3 rounded-xl border border-white/10 bg-navy-950/50 p-3 lg:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]">
        {/* sliders + outputs */}
        <div>
          {w.params.map((p, i) => (
            <div key={p.name} className="mb-3 last:mb-1">
              <div className="flex items-center justify-between gap-2">
                <label className="text-[11px] font-medium text-white/70">{p.name}</label>
                <span className="rounded bg-white/[0.07] px-1.5 py-0.5 text-[11px] font-bold tabular-nums text-brand-300">
                  {vals[i].toLocaleString("en-US", { maximumFractionDigits: p.step < 1 ? 1 : 0 })} <span className="text-white/45">{p.unit}</span>
                </span>
              </div>
              <input
                type="range"
                min={p.min}
                max={p.max}
                step={p.step}
                value={vals[i]}
                onChange={(e) => {
                  const nv = [...vals];
                  nv[i] = parseFloat(e.target.value);
                  setVals(nv);
                }}
                className="mt-1 w-full accent-[#d20000]"
                aria-label={p.name}
              />
              <div className="flex justify-between text-[9px] text-white/35">
                <span>{p.min.toLocaleString("en-US")}{p.unit}</span>
                <span>{p.max.toLocaleString("en-US")}{p.unit}</span>
              </div>
            </div>
          ))}
          <div className="mt-3 space-y-1.5">
            {outs.map((o) => {
              const good = o.spec.good !== undefined && o.v <= parseFloat(o.spec.good);
              const bad = o.spec.bad !== undefined && o.v > parseFloat(o.spec.bad);
              return (
                <div key={o.spec.name} className="flex items-center justify-between rounded-lg border border-white/10 bg-white/[0.05] px-3 py-2">
                  <span className="text-[11.5px] font-medium text-white/75">{o.spec.name}</span>
                  <span className="text-[14px] font-bold tabular-nums" style={{ color: bad ? "#f87171" : good ? "#34d399" : "#d20000" }}>
                    {o.v.toLocaleString("en-US", { maximumFractionDigits: 1 })}
                    <span className="ml-1 text-[10px] font-medium text-white/45">{o.spec.unit}</span>
                  </span>
                </div>
              );
            })}
          </div>
        </div>
        {/* response curve */}
        {curve && (
          <div>
            <svg viewBox={`0 0 ${W} ${H}`} className="h-auto w-full">
              {[0, 0.5, 1].map((f) => (
                <g key={f}>
                  <line x1={PL} x2={W - PR} y1={PT + f * ih} y2={PT + f * ih} stroke="rgba(255,255,255,0.07)" />
                  <text x={PL - 5} y={PT + f * ih + 3} fontSize={9} fill="rgba(255,255,255,0.4)" textAnchor="end">
                    {fmtNum(Math.max(...curve.map((q) => q.y)) * (1 - f))}
                  </text>
                </g>
              ))}
              <path d={cPath.split("||")[0]} fill="none" stroke={ORANGE} strokeWidth={2.2} />
              <path d={cPath.split("||")[1]} fill="none" stroke="rgba(255,255,255,0.4)" strokeDasharray="3 4" />
              {(() => {
                const [cx, cy, label] = cPath.split("||")[2].split(",");
                return (
                  <g>
                    <circle cx={parseFloat(cx)} cy={parseFloat(cy)} r={4.5} fill="#fff" stroke={ORANGE} strokeWidth={2} />
                    <text x={Math.min(parseFloat(cx) + 8, W - 80)} y={parseFloat(cy) - 8} fontSize={10} fontWeight={700} fill="#fff">
                      now
                    </text>
                    <text x={Math.min(parseFloat(cx) + 8, W - 80)} y={parseFloat(cy) + 4} fontSize={9} fill="rgba(255,255,255,0.55)">
                      {label}
                    </text>
                  </g>
                );
              })()}
              <text x={PL} y={H - 8} fontSize={9} fill="rgba(255,255,255,0.4)">
                {w.curve!.label} →
              </text>
            </svg>
          </div>
        )}
      </div>
      <WidgetNote>{w.note}</WidgetNote>
    </div>
  );
}

/* ── slo — error-budget burn simulator ───────────────────────────────────── */

function SloWidget({ w }: { w: Extract<DashWidget, { kind: "slo" }> }) {
  const [traffic, setTraffic] = useState(w.traffic);
  const [errPct, setErrPct] = useState(w.errPct);
  const budgetPct = 100 - w.target;
  const burn = errPct / budgetPct;
  const etaDays = burn > 0 ? w.windowDays / burn : Infinity;
  const badMinDay = (errPct / 100) * 1440;
  const verdict =
    burn > 14.4
      ? { t: "Critical burn — page now", c: "#f87171" }
      : burn > 6
        ? { t: "Fast burn — investigate today", c: "#facc15" }
        : burn > 1
          ? { t: "Slow burn — watch the trend", c: "#fb923c" }
          : { t: "Within budget — ship features", c: "#34d399" };
  const eta = etaDays === Infinity ? "∞" : etaDays >= 1 ? `${etaDays.toFixed(1)} days` : `${(etaDays * 24).toFixed(1)} hours`;
  const burnClamp = Math.min(burn, 15);
  return (
    <div>
      <WidgetHead title={w.title} badge="Burn-rate model" />
      <div className="grid gap-3 rounded-xl border border-white/10 bg-navy-950/50 p-3 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.05fr)]">
        <div>
          <div className="mb-3">
            <div className="flex items-center justify-between">
              <label className="text-[11px] font-medium text-white/70">Request rate</label>
              <span className="rounded bg-white/[0.07] px-1.5 py-0.5 text-[11px] font-bold tabular-nums text-brand-300">
                {traffic.toLocaleString("en-US")} <span className="text-white/45">req/s</span>
              </span>
            </div>
            <input type="range" min={100} max={50000} step={100} value={traffic} onChange={(e) => setTraffic(parseInt(e.target.value))} className="mt-1 w-full accent-[#d20000]" aria-label="Request rate" />
          </div>
          <div className="mb-2">
            <div className="flex items-center justify-between">
              <label className="text-[11px] font-medium text-white/70">Observed error rate</label>
              <span className="rounded bg-white/[0.07] px-1.5 py-0.5 text-[11px] font-bold tabular-nums text-brand-300">
                {errPct.toFixed(2)} <span className="text-white/45">%</span>
              </span>
            </div>
            <input type="range" min={0} max={2} step={0.01} value={errPct} onChange={(e) => setErrPct(parseFloat(e.target.value))} className="mt-1 w-full accent-[#d20000]" aria-label="Error rate" />
            <div className="flex justify-between text-[9px] text-white/35">
              <span>0%</span>
              <span>budget floor {budgetPct.toFixed(2)}%</span>
              <span>2%</span>
            </div>
          </div>
          <div className="mt-2 rounded-lg border border-white/10 bg-white/[0.05] px-3 py-2 text-[10.5px] leading-relaxed text-white/55">
            SLO <b className="text-white">{w.target}%</b> over <b className="text-white">{w.windowDays} days</b> allows{" "}
            <b className="text-white">{(w.windowDays * 1440 * (budgetPct / 100)).toFixed(0)} bad minutes</b> for the window.
          </div>
        </div>
        <div>
          <div className="rounded-lg border border-white/10 bg-white/[0.04] p-3">
            <div className="flex items-baseline justify-between">
              <p className="text-[10.5px] font-bold uppercase tracking-wider text-white/45">Burn rate</p>
              <p className="font-display text-[26px] font-bold tabular-nums" style={{ color: verdict.c }}>
                {burn.toFixed(1)}×
              </p>
            </div>
            <svg viewBox="0 0 300 46" className="mt-1 h-auto w-full">
              <rect x={0} y={10} width={300} height={16} rx={8} fill="rgba(255,255,255,0.08)" />
              <rect x={0} y={10} width={(6 / 15) * 300} height={16} rx={8} fill="rgba(52,211,153,0.25)" />
              <rect x={(6 / 15) * 300} y={10} width={(8.4 / 15) * 300} height={16} fill="rgba(250,204,21,0.22)" />
              <rect x={(14.4 / 15) * 300} y={10} width={(0.6 / 15) * 300} height={16} rx={8} fill="rgba(248,113,113,0.3)" />
              <line x1={(1 / 15) * 300} y1={4} y2={32} x2={(1 / 15) * 300} stroke="rgba(255,255,255,0.5)" strokeDasharray="2 3" />
              <text x={(1 / 15) * 300} y={42} fontSize={8} fill="rgba(255,255,255,0.45)" textAnchor="middle">1×</text>
              <line x1={(6 / 15) * 300} y1={4} y2={32} x2={(6 / 15) * 300} stroke="rgba(255,255,255,0.5)" strokeDasharray="2 3" />
              <text x={(6 / 15) * 300} y={42} fontSize={8} fill="rgba(255,255,255,0.45)" textAnchor="middle">6×</text>
              <line x1={(14.4 / 15) * 300} y1={4} y2={32} x2={(14.4 / 15) * 300} stroke="rgba(255,255,255,0.5)" strokeDasharray="2 3" />
              <text x={(14.4 / 15) * 300} y={42} fontSize={8} fill="rgba(255,255,255,0.45)" textAnchor="middle">14.4×</text>
              <line x1={(burnClamp / 15) * 300} y1={6} y2={30} x2={(burnClamp / 15) * 300} stroke={verdict.c} strokeWidth={2.5} />
            </svg>
            <p className="text-[11.5px] font-bold" style={{ color: verdict.c }}>{verdict.t}</p>
            <div className="mt-2 grid grid-cols-2 gap-2">
              <div className="rounded border border-white/10 bg-navy-950/60 px-2.5 py-1.5">
                <p className="text-[9px] uppercase tracking-wider text-white/40">Budget exhausts in</p>
                <p className="text-[13px] font-bold tabular-nums text-white">{eta}</p>
              </div>
              <div className="rounded border border-white/10 bg-navy-950/60 px-2.5 py-1.5">
                <p className="text-[9px] uppercase tracking-wider text-white/40">Burned / day</p>
                <p className="text-[13px] font-bold tabular-nums text-white">{badMinDay.toFixed(0)} min</p>
              </div>
            </div>
          </div>
          <WidgetNote>{w.note}</WidgetNote>
        </div>
      </div>
    </div>
  );
}

/* ── flow — pipeline stepper with click-through detail ───────────────────── */

function FlowWidget({ w }: { w: Extract<DashWidget, { kind: "flow" }> }) {
  const [sel, setSel] = useState(0);
  const st = w.stages[Math.min(sel, w.stages.length - 1)];
  return (
    <div>
      <WidgetHead title={w.title} badge="Click stages" />
      <div className="rounded-xl border border-white/10 bg-navy-950/50 p-3">
        <div className="flex flex-wrap items-stretch gap-1.5">
          {w.stages.map((s, i) => (
            <button
              key={s.name}
              onClick={() => setSel(i)}
              className={`group relative min-w-[118px] flex-1 rounded-lg border px-2.5 py-2 text-left transition ${
                i === sel
                  ? "border-brand bg-brand/15 shadow-2"
                  : "border-white/10 bg-white/[0.04] hover:border-brand/50"
              }`}
            >
              <p className="text-[9px] font-bold uppercase tracking-wider text-brand-300">Stage {i + 1}</p>
              <p className={`mt-0.5 text-[11.5px] font-semibold leading-tight ${i === sel ? "text-white" : "text-white/75"}`}>{s.name}</p>
              <p className="mt-0.5 hidden text-[9.5px] leading-snug text-white/40 group-hover:block">{s.role}</p>
              {i < w.stages.length - 1 && (
                <span className="absolute -right-[7px] top-1/2 z-10 hidden -translate-y-1/2 text-white/25 sm:block">▸</span>
              )}
            </button>
          ))}
        </div>
        <div className="mt-3 grid gap-3 lg:grid-cols-[minmax(0,1.3fr)_minmax(0,1fr)]">
          <div className="rounded-lg border border-white/10 bg-white/[0.04] p-3">
            <p className="text-[10.5px] font-bold uppercase tracking-wider text-brand-300">
              Stage {sel + 1} — {st.name}
            </p>
            <p className="mt-1.5 text-[12px] leading-relaxed text-white/75">{st.detail}</p>
          </div>
          <div className="grid grid-cols-2 content-start gap-1.5">
            {st.metrics.map((m) => (
              <div key={m.label} className="rounded-lg border border-white/10 bg-navy-950/60 px-2.5 py-2">
                <p className="text-[9px] uppercase tracking-wider text-white/40">{m.label}</p>
                <p className="text-[13px] font-bold tabular-nums text-brand-300">{m.value}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
      <WidgetNote>{w.note}</WidgetNote>
    </div>
  );
}

/* ── arch — interactive topology: click node → detail ────────────────────── */

function ArchWidget({ w }: { w: Extract<DashWidget, { kind: "arch" }> }) {
  const [sel, setSel] = useState<string | null>(null);
  const COL_W = 172;
  const GAP = 58;
  const NODE_W = 152;
  const NODE_H = 40;
  const TOP = 56;
  const ROW_GAP = 50;
  const W = w.lanes.length * COL_W + (w.lanes.length - 1) * GAP + 24;
  const maxRows = Math.max(2, ...w.lanes.map((_, li) => w.nodes.filter((n) => n.lane === li).length));
  const H = TOP + maxRows * (NODE_H + ROW_GAP) + 18;
  const laneX = (li: number) => 12 + li * (COL_W + GAP);
  const pos: Record<string, { x: number; y: number }> = {};
  const perLane: number[] = w.lanes.map(() => 0);
  for (const n of w.nodes) {
    const row = perLane[n.lane]++;
    const cnt = w.nodes.filter((m) => m.lane === n.lane).length;
    const totalH = cnt * NODE_H + (cnt - 1) * ROW_GAP;
    const startY = TOP + (maxRows * (NODE_H + ROW_GAP) - ROW_GAP - totalH) / 2;
    pos[n.id] = { x: laneX(n.lane) + (COL_W - NODE_W) / 2, y: startY + row * (NODE_H + ROW_GAP) };
  }
  const node = sel ? w.nodes.find((n) => n.id === sel) : null;
  const touch = new Set<string>();
  if (sel) for (const e of w.edges) { if (e.a === sel) touch.add(e.b); if (e.b === sel) touch.add(e.a); }

  return (
    <div>
      <WidgetHead title={w.title} badge={sel ? "Node detail below" : "Click any node"} />
      <div className="rounded-xl border border-white/10 bg-navy-950/50 p-1">
        <div className="overflow-x-auto">
          <svg viewBox={`0 0 ${W} ${H}`} className="h-auto w-full min-w-[680px]">
            {w.lanes.map((lane, li) => (
              <g key={lane}>
                <rect x={laneX(li)} y={10} width={COL_W} height={H - 24} rx={10} fill={li % 2 ? "rgba(255,255,255,0.035)" : "rgba(255,255,255,0.015)"} stroke="rgba(255,255,255,0.06)" />
                <text x={laneX(li) + COL_W / 2} y={28} fontSize={9.5} fontWeight={800} fill="rgba(210, 0, 0,0.9)" textAnchor="middle" letterSpacing="0.14em">
                  {lane.toUpperCase()}
                </text>
              </g>
            ))}
            {w.edges.map((e, i) => {
              const a = pos[e.a];
              const b = pos[e.b];
              if (!a || !b) return null;
              const ax = a.x + NODE_W;
              const bx = b.x;
              const ay = a.y + NODE_H / 2;
              const by = b.y + NODE_H / 2;
              const mx = (ax + bx) / 2;
              const d = `M ${ax} ${ay} C ${mx} ${ay}, ${mx} ${by}, ${bx} ${by}`;
              const lit = sel && (e.a === sel || e.b === sel);
              return (
                <g key={`e${i}`}>
                  <path d={d} fill="none" stroke={lit ? "rgba(210, 0, 0,0.85)" : "rgba(255,255,255,0.18)"} strokeWidth={lit ? 1.8 : 1.2} />
                  {lit && e.label && (
                    <text x={mx} y={(ay + by) / 2 - 4} fontSize={8.5} fill="rgba(210, 0, 0,0.9)" textAnchor="middle">{e.label}</text>
                  )}
                </g>
              );
            })}
            {w.nodes.map((n) => {
              const p = pos[n.id];
              if (!p) return null;
              const active = sel === n.id;
              const linked = touch.has(n.id);
              const words = n.label.split(" ");
              const lines: string[] = [];
              let cur = "";
              for (const wd of words) {
                if ((cur + " " + wd).trim().length > 19 && cur) { lines.push(cur); cur = wd; }
                else cur = (cur + " " + wd).trim();
              }
              if (cur) lines.push(cur);
              return (
                <g
                  key={n.id}
                  onClick={() => setSel(active ? null : n.id)}
                  className="cursor-pointer"
                  style={{ transition: "opacity .15s" }}
                  opacity={sel && !active && !linked ? 0.45 : 1}
                >
                  <rect
                    x={p.x} y={p.y} width={NODE_W} height={NODE_H} rx={8}
                    fill={active ? "rgba(210, 0, 0,0.3)" : n.hot ? "rgba(210, 0, 0,0.14)" : "rgba(255,255,255,0.05)"}
                    stroke={active ? "#d20000" : linked ? "rgba(210, 0, 0,0.6)" : n.hot ? "rgba(210, 0, 0,0.55)" : "rgba(255,255,255,0.24)"}
                    strokeWidth={active ? 2 : 1.1}
                  />
                  {lines.slice(0, 2).map((ln, k) => (
                    <text key={k} x={p.x + NODE_W / 2} y={p.y + NODE_H / 2 + 3.5 + (k - (lines.slice(0, 2).length - 1) / 2) * 12} fontSize={9.5} fontWeight={600} fill="#fff" textAnchor="middle">
                      {ln}
                    </text>
                  ))}
                </g>
              );
            })}
          </svg>
        </div>
        {node && (
          <div className="mx-2 mb-2 rounded-lg border border-brand/40 bg-brand/10 p-3" style={{ animation: "dash-in .3s both" }}>
            <p className="text-[10px] font-bold uppercase tracking-wider text-brand-300">{w.lanes[node.lane]} · {node.label}</p>
            <p className="mt-1 text-[12px] leading-relaxed text-white/80">{node.detail}</p>
          </div>
        )}
      </div>
      <WidgetNote>{w.note}</WidgetNote>
    </div>
  );
}

/* ── table — sortable + filterable ───────────────────────────────────────── */

function TableWidget({ w }: { w: Extract<DashWidget, { kind: "table" }> }) {
  const [sort, setSort] = useState<{ col: number; dir: 1 | -1 } | null>(null);
  const [q, setQ] = useState("");
  const rows = useMemo(() => {
    let rs = w.rows;
    if (q.trim()) {
      const s = q.trim().toLowerCase();
      rs = rs.filter((r) => r.some((c) => c.toLowerCase().includes(s)));
    }
    if (sort) {
      rs = [...rs].sort((a, b) => {
        const av = a[sort.col] ?? "";
        const bv = b[sort.col] ?? "";
        const an = parseFloat(av.replace(/[^0-9.\-]/g, ""));
        const bn = parseFloat(bv.replace(/[^0-9.\-]/g, ""));
        if (!isNaN(an) && !isNaN(bn) && av.match(/[0-9]/) && bv.match(/[0-9]/)) return (an - bn) * sort.dir;
        return av.localeCompare(bv) * sort.dir;
      });
    }
    return rs;
  }, [w.rows, q, sort]);
  return (
    <div>
      <WidgetHead title={w.title} badge="Sort · filter" />
      <div className="rounded-xl border border-white/10 bg-navy-950/50 p-3">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Filter rows…"
          className="mb-2 w-full rounded-lg border border-white/15 bg-white/[0.05] px-3 py-1.5 text-[12px] text-white placeholder:text-white/30 focus:border-brand focus:outline-none"
          aria-label="Filter table"
        />
        <div className="overflow-x-auto">
          <table className="w-full text-left text-[11.5px]">
            <thead>
              <tr>
                {w.headers.map((h, i) => (
                  <th key={h} className="whitespace-nowrap px-2.5 py-2">
                    <button
                      onClick={() => setSort(sort && sort.col === i ? { col: i, dir: sort.dir === 1 ? -1 : 1 } : { col: i, dir: 1 })}
                      className="inline-flex items-center gap-1 font-bold uppercase tracking-wider text-white/50 transition hover:text-brand-300"
                    >
                      {h}
                      <span className="text-[9px]">{sort && sort.col === i ? (sort.dir === 1 ? "▲" : "▼") : "⇅"}</span>
                    </button>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((r, ri) => (
                <tr key={ri} className={ri % 2 ? "bg-white/[0.03]" : ""}>
                  {r.map((c, ci) => (
                    <td key={ci} className={`px-2.5 py-2 align-top ${ci === 0 ? "font-semibold text-white/85" : "text-white/60"}`}>
                      {c}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
          {rows.length === 0 && <p className="px-2 py-3 text-[11.5px] text-white/40">No rows match the filter.</p>}
        </div>
        <p className="mt-1.5 text-[9.5px] text-white/35">{rows.length} of {w.rows.length} rows</p>
      </div>
      <WidgetNote>{w.note}</WidgetNote>
    </div>
  );
}

/* ── scatter — decision map with groups + hover ──────────────────────────── */

function ScatterWidget({ w }: { w: Extract<DashWidget, { kind: "scatter" }> }) {
  const [off, setOff] = useState<Set<string>>(new Set());
  const [hi, setHi] = useState<number | null>(null);
  const xmax = w.xMax ?? Math.max(...w.points.map((p) => p.x)) * 1.1;
  const ymax = w.yMax ?? Math.max(...w.points.map((p) => p.y)) * 1.1;
  const W = 560;
  const H = 220;
  const PL = 44;
  const PR = 14;
  const PT = 14;
  const PB = 32;
  const iw = W - PL - PR;
  const ih = H - PT - PB;
  const px = (x: number) => PL + (Math.min(x, xmax) / xmax) * iw;
  const py = (y: number) => PT + ih - (Math.min(y, ymax) / ymax) * ih;
  const show = (g: string) => !off.has(g);
  return (
    <div>
      <WidgetHead title={w.title} badge="Position map" />
      <div className="relative rounded-xl border border-white/10 bg-navy-950/50 p-1">
        <svg viewBox={`0 0 ${W} ${H}`} className="h-auto w-full">
          {[0, 0.5, 1].map((f) => (
            <g key={f}>
              <line x1={PL} x2={W - PR} y1={PT + f * ih} y2={PT + f * ih} stroke="rgba(255,255,255,0.07)" />
              <text x={PL - 5} y={PT + f * ih + 3} fontSize={9} fill="rgba(255,255,255,0.4)" textAnchor="end">{fmtNum(ymax * (1 - f))}</text>
            </g>
          ))}
          <text x={PL + iw / 2} y={H - 10} fontSize={9.5} fill="rgba(255,255,255,0.5)" textAnchor="middle">{w.xLabel} →</text>
          <text x={10} y={PT + ih / 2} fontSize={9.5} fill="rgba(255,255,255,0.5)" textAnchor="middle" transform={`rotate(-90 10 ${PT + ih / 2})`}>
            {w.yLabel} →
          </text>
          {w.points.map((p, i) => {
            if (!show(p.group)) return null;
            const gi = w.groups.indexOf(p.group);
            const active = hi === i;
            return (
              <g key={i} onMouseEnter={() => setHi(i)} onMouseLeave={() => setHi(null)} className="cursor-pointer">
                <circle cx={px(p.x)} cy={py(p.y)} r={active ? 7 : 5} fill={PALETTE[gi % PALETTE.length]} opacity={active ? 1 : 0.75} stroke={active ? "#fff" : "none"} strokeWidth={1.5} style={{ transition: "r .12s" }} />
                {active && (
                  <text x={px(p.x) + 9} y={py(p.y) + 3.5} fontSize={10} fontWeight={700} fill="#fff">{p.label}</text>
                )}
              </g>
            );
          })}
        </svg>
        {hi !== null && (
          <div className="pointer-events-none absolute right-2 top-2 rounded-lg border border-white/15 bg-navy-950/95 px-3 py-1.5 shadow-2">
            <p className="text-[11px] font-bold text-white">{w.points[hi].label}</p>
            <p className="text-[10px] text-white/55">
              {w.xLabel} {fmtNum(w.points[hi].x)} · {w.yLabel} {fmtNum(w.points[hi].y)} · {w.points[hi].group}
            </p>
          </div>
        )}
      </div>
      <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1">
        {w.groups.map((g, i) => (
          <button
            key={g}
            onClick={() => {
              const nx = new Set(off);
              if (nx.has(g)) nx.delete(g);
              else if (w.groups.filter((x) => show(x)).length > 1) nx.add(g);
              setOff(nx);
            }}
            className={`inline-flex items-center gap-1.5 rounded px-1.5 py-0.5 text-[10.5px] font-medium transition ${show(g) ? "text-white/80" : "text-white/30 line-through"}`}
          >
            <span className="inline-block h-2 w-2 rounded-full" style={{ background: show(g) ? PALETTE[i % PALETTE.length] : "rgba(255,255,255,0.25)" }} />
            {g}
          </button>
        ))}
      </div>
      <WidgetNote>{w.note}</WidgetNote>
    </div>
  );
}

/* ── dispatcher ──────────────────────────────────────────────────────────── */

export function DashWidgetView({ w }: { w: DashWidget }) {
  switch (w.kind) {
    case "line": return <LineWidget w={w} />;
    case "bar": return <BarWidget w={w} />;
    case "radar": return <RadarWidget w={w} />;
    case "heat": return <HeatWidget w={w} />;
    case "donut": return <DonutWidget w={w} />;
    case "gauge": return <GaugeWidget w={w} />;
    case "sim": return <SimWidget w={w} />;
    case "slo": return <SloWidget w={w} />;
    case "flow": return <FlowWidget w={w} />;
    case "arch": return <ArchWidget w={w} />;
    case "table": return <TableWidget w={w} />;
    case "scatter": return <ScatterWidget w={w} />;
    default: return null;
  }
}

/* KPI strip with sparkline */
export function KpiStrip({ kpis }: { kpis: DashKpiSpec[] }) {
  const spark = (pts: number[], key: string) => {
    if (!pts?.length) return null;
    const mx = Math.max(...pts) || 1;
    const mn = Math.min(...pts);
    const span = mx - mn || 1;
    const W = 64;
    const H = 18;
    const d = pts.map((v, i) => `${i === 0 ? "M" : "L"} ${(i / Math.max(pts.length - 1, 1)) * W} ${H - ((v - mn) / span) * H}`).join(" ");
    return (
      <svg viewBox={`0 0 ${W} ${H}`} className="h-[18px] w-[64px]" aria-hidden="true" key={key}>
        <path d={d} fill="none" stroke="rgba(210, 0, 0,0.85)" strokeWidth={1.6} />
      </svg>
    );
  };
  return (
    <div className="grid grid-cols-2 gap-2 sm:grid-cols-3 lg:grid-cols-5">
      {kpis.map((k, i) => (
        <div
          key={k.label}
          className="group rounded-xl border border-white/10 bg-white/[0.05] px-3 py-2.5 transition hover:border-brand/40 hover:bg-white/[0.08]"
          style={{ animation: `dash-in .5s ${0.1 * i}s both` }}
        >
          <p className="text-[9.5px] font-bold uppercase leading-tight tracking-[0.12em] text-white/45">{k.label}</p>
          <div className="mt-1 flex items-end justify-between gap-1">
            <p className="font-display text-[18px] font-bold leading-none tabular-nums text-white">{k.value}</p>
            {k.spark && <span className="opacity-70 transition group-hover:opacity-100">{spark(k.spark, k.label)}</span>}
          </div>
          {k.delta && (
            <p className={`mt-1 text-[10px] font-semibold ${k.dir === "down" ? "text-emerald-400" : k.dir === "flat" ? "text-white/45" : "text-brand-300"}`}>
              {k.dir === "up" ? "▲" : k.dir === "down" ? "▼" : "■"} {k.delta}
            </p>
          )}
        </div>
      ))}
    </div>
  );
}
