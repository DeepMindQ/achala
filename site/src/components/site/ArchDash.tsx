"use client";

import { useRef, useState, type PointerEvent as RPointerEvent, type ReactNode } from "react";
import Reveal from "./Reveal";
import { CountUp } from "./Motion";

/* ── ArchDash — data-driven deep-tech visuals ───────────────────────────────
   Two components, both fed from the page JSON so every page renders its OWN
   architecture / dashboard (no shared template imagery):

   1. ArchGraph   — a real architecture graph: lanes + nodes + edges passed
                    from content. Each (domain × industry × variant) renders a
                    different topology with that sector's actual systems.
   2. MetricsDash — an operations-console mock: KPI tiles, gate-by-gate bar
                    chart, decision-log ticker. Values are the page's own
                    measured outcomes (case studies) or named program
                    metrics — never invented figures.

   Pure SVG + CSS animation, static-export safe, reduced-motion aware. */

const CL = {
  bg: "#1a1630",
  bg2: "rgba(255,255,255,0.09)",
  stroke: "rgba(255,255,255,0.26)",
  edge: "rgba(255,255,255,0.20)",
  hot: "#2c1e2d",
  hotStroke: "rgba(210, 0, 0,0.75)",
  orange: "#d20000",
  txt: "rgba(255,255,255,0.95)",
  dim: "rgba(255,255,255,0.60)",
  lane: "rgba(255,255,255,0.05)",
};

/* ── PanelTip — shared hover readout for ChartPanel charts ──────────────────
   Absolutely positioned inside a relative wrapper, follows the hovered index.
   Pure CSS positioning — no layout shift, static-export safe. */
function PanelTip({ left, children }: { left: number; children: ReactNode }) {
  return (
    <div
      className="pointer-events-none absolute top-1 z-10 -translate-x-1/2 whitespace-nowrap rounded-lg px-2.5 py-1.5 text-[11px] leading-snug text-white shadow-3"
      style={{
        left: `${Math.max(8, Math.min(92, left))}%`,
        background: "rgba(24,20,45,0.94)",
        border: "1px solid rgba(210,0,0,0.45)",
      }}
      role="status"
    >
      {children}
    </div>
  );
}

export type ArchNode = { id: string; lane: number; label: string; sub?: string; hot?: boolean };
export type ArchEdge = { a: string; b: string; label?: string };

function wrapLabel(label: string, max = 20): string[] {
  const words = label.split(/\s+/);
  const lines: string[] = [];
  let cur = "";
  for (const w of words) {
    if ((cur + " " + w).trim().length > max && cur) {
      lines.push(cur);
      cur = w;
    } else {
      cur = (cur + " " + w).trim();
    }
  }
  if (cur) lines.push(cur);
  return lines.slice(0, 2).length ? lines.slice(0, 2) : [label];
}

export function ArchGraph({
  title,
  note,
  lanes,
  nodes,
  edges,
  badges,
}: {
  title: string;
  note?: string;
  lanes: string[];
  nodes: ArchNode[];
  edges?: ArchEdge[];
  badges?: { label: string; value: string }[];
}) {
  const edgeList = edges ?? [];
  const [hiNode, setHiNode] = useState<string | null>(null);
  const COL_W = 178;
  const GAP = 64;
  const NODE_W = 164;
  const NODE_H = 46;
  const SUB_H = 64;
  const TOP = 66;
  const ROW_GAP = 26;

  const boxH = (n: ArchNode) => (n.sub ? SUB_H : NODE_H);
  const wrapSub = (sub: string): string[] => {
    if (sub.length <= 26) return [sub];
    const words = sub.split(" ");
    const l1: string[] = [];
    let i = 0;
    while (i < words.length && [...l1, words[i]].join(" ").length <= 26) {
      l1.push(words[i]);
      i += 1;
    }
    const rest = words.slice(i).join(" ");
    return rest ? [l1.join(" "), rest.slice(0, 30)] : [l1.join(" ")];
  };

  // lane x origins
  const laneX = (li: number) => 16 + li * (COL_W + GAP);
  // node positions per lane, stacked with sub-aware heights
  const pos: Record<string, { x: number; y: number; h: number }> = {};
  const perLaneCount: number[] = lanes.map(() => 0);
  const laneHeights = lanes.map((_, li) => {
    const ln = nodes.filter((m) => m.lane === li);
    return ln.reduce((s, m) => s + boxH(m), 0) + Math.max(0, ln.length - 1) * ROW_GAP;
  });
  const maxLaneH = Math.max(1, ...laneHeights);
  for (const n of nodes) {
    const row = perLaneCount[n.lane]++;
    const laneNodes = nodes.filter((m) => m.lane === n.lane);
    const startY = TOP + 24 + (maxLaneH - laneHeights[n.lane]) / 2;
    const y = startY + laneNodes.slice(0, row).reduce((s, m) => s + boxH(m) + ROW_GAP, 0);
    pos[n.id] = { x: laneX(n.lane) + (COL_W - NODE_W) / 2, y, h: boxH(n) };
  }
  const W = lanes.length * COL_W + (lanes.length - 1) * GAP + 32;
  const H = TOP + 24 + maxLaneH + 30;

  const anchor = (id: string, side: "l" | "r") => {
    const p = pos[id];
    if (!p) return null;
    return { x: side === "l" ? p.x : p.x + NODE_W, y: p.y + p.h / 2 };
  };

  // node rect for label collision tests
  const rects = Object.entries(pos).map(([id, p]) => ({ id, x: p.x, y: p.y, w: NODE_W, h: p.h }));
  const insideAnyRect = (x: number, y: number, pad = 4) =>
    rects.some((r) => x > r.x - pad && x < r.x + r.w + pad && y > r.y - pad && y < r.y + r.h + pad);

  return (
    <Reveal className="mt-6">
      <figure className="overflow-hidden rounded-2xl border border-white/10 grad-navy-field shadow-3">
        <div className="flex flex-wrap items-center justify-between gap-2 border-b border-white/10 px-5 py-3">
          <p className="text-[12.5px] font-semibold text-white">{title}</p>
          {badges && badges.length > 0 ? (
            <div className="flex flex-wrap items-center gap-1.5">
              {badges.map((bd) => (
                <span
                  key={bd.label}
                  className="inline-flex items-baseline gap-1.5 rounded-lg border border-brand/35 bg-brand/10 px-2.5 py-1"
                  title={bd.label}
                >
                  <span className="font-display text-[13px] font-bold leading-none tabular-nums text-brand-300">
                    {bd.value}
                  </span>
                  <span className="text-[9.5px] font-semibold uppercase tracking-[0.1em] text-white/60">
                    {bd.label}
                  </span>
                </span>
              ))}
            </div>
          ) : (
            <span className="rounded-full border border-brand/40 bg-brand/15 px-2.5 py-0.5 text-[10px] font-bold uppercase tracking-[0.14em] text-brand-300">
              Architecture
            </span>
          )}
        </div>
        <div className="overflow-x-auto px-2 py-3">
          <svg viewBox={`0 0 ${W} ${H}`} className="h-auto w-full min-w-[720px]" role="img" aria-label={title}>
            {/* lane bands + headers */}
            {lanes.map((lane, li) => (
              <g key={lane}>
                <rect
                  x={laneX(li)}
                  y={14}
                  width={COL_W}
                  height={H - 30}
                  rx={12}
                  fill={li % 2 ? CL.lane : "rgba(255,255,255,0.02)"}
                  stroke="rgba(255,255,255,0.07)"
                />
                <text
                  x={laneX(li) + COL_W / 2}
                  y={36}
                  fontSize={10.5}
                  fontWeight={800}
                  fill="rgba(210, 0, 0,0.9)"
                  textAnchor="middle"
                  letterSpacing="0.14em"
                >
                  {lane.toUpperCase()}
                </text>
              </g>
            ))}
            {/* edges */}
            {edgeList.map((e, i) => {
              const a = anchor(e.a, "r");
              const b = anchor(e.b, "l");
              if (!a || !b) return null;
              const mx = (a.x + b.x) / 2;
              const d = `M ${a.x} ${a.y} C ${mx} ${a.y}, ${mx} ${b.y}, ${b.x} ${b.y}`;
              const hot = hiNode !== null && (e.a === hiNode || e.b === hiNode);
              const dim = hiNode !== null && !hot;
              return (
                <g key={`e${i}`} opacity={dim ? 0.25 : 1} style={{ transition: "opacity .18s" }}>
                  <path d={d} fill="none" stroke={hot ? CL.hotStroke : CL.edge} strokeWidth={hot ? 2 : 1.4} />
                  <path
                    className="td-flow"
                    d={d}
                    fill="none"
                    stroke={CL.orange}
                    strokeWidth={hot ? 2.4 : 1.8}
                    strokeDasharray="4 12"
                    strokeLinecap="round"
                    style={{ animationDelay: `${(i % 6) * 0.35}s`, animationDuration: `${2 + (i % 4) * 0.4}s`, opacity: dim ? 0.2 : 0.85 }}
                  />
                </g>
              );
            })}
            {/* edge labels — only where they do not collide with nodes */}
            {edgeList.map((e, i) => {
              const a = anchor(e.a, "r");
              const b = anchor(e.b, "l");
              if (!a || !b || !e.label) return null;
              const mx = (a.x + b.x) / 2;
              let my = (a.y + b.y) / 2 - 5;
              let ok = !insideAnyRect(mx, my, 6);
              if (!ok) {
                my = my - 26;
                ok = !insideAnyRect(mx, my, 4);
              }
              if (!ok) return null;
              return (
                <text key={`el${i}`} x={mx} y={my} fontSize={9} fill={CL.dim} textAnchor="middle">
                  {e.label}
                </text>
              );
            })}
            {/* nodes */}
            {nodes.map((n) => {
              const p = pos[n.id];
              if (!p) return null;
              const lines = wrapLabel(n.label);
              const subLines = n.sub ? wrapSub(n.sub) : [];
              const hasSub = subLines.length > 0;
              const labelBase = hasSub ? p.y + 19 : p.y + p.h / 2 + 4;
              const linked = hiNode === n.id;
              return (
                <g
                  key={n.id}
                  onPointerEnter={() => setHiNode(n.id)}
                  onPointerLeave={() => setHiNode((v) => (v === n.id ? null : v))}
                  className="cursor-pointer"
                >
                  <rect
                    x={p.x}
                    y={p.y}
                    width={NODE_W}
                    height={p.h}
                    rx={9}
                    fill={linked || n.hot ? CL.hot : CL.bg}
                    stroke={linked || n.hot ? CL.hotStroke : CL.stroke}
                    strokeWidth={linked ? 2 : n.hot ? 1.5 : 1.1}
                  />
                  {lines.map((ln, k) => (
                    <text
                      key={k}
                      x={p.x + NODE_W / 2}
                      y={labelBase + (k - (lines.length - 1) / 2) * 13}
                      fontSize={10.5}
                      fontWeight={600}
                      fill={n.hot ? "rgba(255,255,255,0.97)" : CL.txt}
                      textAnchor="middle"
                    >
                      {ln}
                    </text>
                  ))}
                  {subLines.map((sl, k) => (
                    <text
                      key={`s${k}`}
                      x={p.x + NODE_W / 2}
                      y={p.y + 36 + k * 10.5}
                      fontSize={8}
                      fill="rgba(210, 0, 0,0.9)"
                      textAnchor="middle"
                    >
                      {sl}
                    </text>
                  ))}
                </g>
              );
            })}
          </svg>
        </div>
        {note && (
          <figcaption className="border-t border-white/10 px-5 py-2.5 text-[11.5px] leading-relaxed text-white/55">
            {note}
          </figcaption>
        )}
      </figure>
    </Reveal>
  );
}

/* ── MetricsDash — the operations console ─────────────────────────────────── */

export type DashKpi = { label: string; value: string; delta?: string; dir?: "up" | "down" | "flat" };
export type DashGate = { name: string; pct: number };
export type DashLog = { t: string; msg: string; tag: string };

export function MetricsDash({
  title,
  kpis,
  gates,
  log,
  caption,
}: {
  title: string;
  kpis: DashKpi[];
  gates?: DashGate[];
  log?: DashLog[];
  caption?: string;
}) {
  return (
    <Reveal className="mt-6">
      <figure className="overflow-hidden rounded-2xl border border-white/10 grad-navy-field shadow-3">
        {/* console header */}
        <div className="flex items-center justify-between border-b border-white/10 px-5 py-3">
          <div className="flex items-center gap-2">
            <span className="h-2.5 w-2.5 rounded-full bg-white/20" />
            <span className="h-2.5 w-2.5 rounded-full bg-white/20" />
            <span className="h-2.5 w-2.5 rounded-full bg-brand/70" />
            <p className="ml-2 text-[12.5px] font-semibold text-white">{title}</p>
          </div>
          <span className="inline-flex items-center gap-1.5 rounded-full border border-white/20 bg-white/[0.06] px-2.5 py-0.5 text-[10px] font-bold uppercase tracking-[0.14em] text-white/60">
            Achala program — illustrative
          </span>
        </div>
        <div className="px-5 py-4">
          {/* KPI tiles */}
          <div className="grid grid-cols-2 gap-2.5 sm:grid-cols-4">
            {kpis.map((k, i) => (
              <div
                key={k.label}
                className="rounded-xl border border-white/10 bg-white/[0.05] px-3.5 py-3 backdrop-blur"
                style={{ animation: `dash-in 0.5s ${0.12 * i}s both` }}
              >
                <p className="text-[10.5px] font-bold uppercase leading-tight tracking-[0.12em] text-white/45">{k.label}</p>
                <p className="mt-1 font-display text-[20px] font-bold tabular-nums text-white">
                  {k.value}
                  {k.delta && (
                    <span
                      className={`ml-2 align-middle text-[11.5px] font-semibold ${
                        k.dir === "down" ? "text-emerald-400" : k.dir === "flat" ? "text-white/50" : "text-brand-300"
                      }`}
                    >
                      {k.delta}
                    </span>
                  )}
                </p>
              </div>
            ))}
          </div>
          {/* gate bars */}
          {gates && gates.length > 0 && (
            <div className="mt-4 rounded-xl border border-white/10 bg-white/[0.04] px-4 py-3.5">
              <p className="text-[10.5px] font-bold uppercase tracking-[0.14em] text-white/45">Gate-by-gate position</p>
              <div className="mt-3 space-y-2.5">
                {gates.map((g, i) => (
                  <div key={g.name} className="flex items-center gap-3">
                    <span className="w-36 shrink-0 text-[11px] font-medium leading-tight text-white/70">{g.name}</span>
                    <span className="h-2 flex-1 overflow-hidden rounded-full bg-white/10">
                      <span
                        className="block h-full rounded-full"
                        style={{
                          width: `${Math.max(4, Math.min(100, g.pct))}%`,
                          background: i === gates.length - 1 ? CL.orange : "rgba(210, 0, 0,0.55)",
                          animation: `dash-bar 0.9s ${0.25 + 0.15 * i}s both`,
                        }}
                      />
                    </span>
                    <span className="w-10 shrink-0 text-right text-[11px] font-semibold tabular-nums text-brand-300">
                      {g.pct}%
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
          {/* decision log */}
          {log && log.length > 0 && (
            <div className="mt-4 rounded-xl border border-white/10 bg-navy-950/60 px-4 py-3 font-mono">
              <p className="font-sans text-[10.5px] font-bold uppercase tracking-[0.14em] text-white/45">Decision log</p>
              <div className="mt-2.5 space-y-1.5">
                {log.map((r, i) => (
                  <p
                    key={i}
                    className="flex flex-wrap items-baseline gap-x-2 text-[11px] leading-relaxed text-white/70"
                    style={{ animation: `dash-in 0.5s ${0.5 + 0.18 * i}s both` }}
                  >
                    <span className="text-white/35">{r.t}</span>
                    <span className="rounded bg-brand/15 px-1.5 py-0.5 text-[9.5px] font-bold uppercase tracking-wider text-brand-300">
                      {r.tag}
                    </span>
                    <span>{r.msg}</span>
                  </p>
                ))}
              </div>
            </div>
          )}
        </div>
        {caption && (
          <figcaption className="border-t border-white/10 px-5 py-2.5 text-[11.5px] leading-relaxed text-white/55">
            {caption}
          </figcaption>
        )}
      </figure>
    </Reveal>
  );
}

/* ── ChartPanel — data charts (line / bar / radar) fed from page JSON ───────
   Every series comes from the page's own content spec, so two pages never
   render the same chart. Pure SVG + CSS, static-export safe, reduced-motion
   aware. Values are engineering targets / reference bands, clearly captioned
   as such — never client-owned figures. */

export type ChartSeries = { name: string; points: number[] };

export function ChartPanel({
  title,
  variant = "line",
  cats,
  series,
  unit,
  yMax,
  nodes,
  links,
  note,
  caption,
}: {
  title: string;
  variant?:
    | "line"
    | "bar"
    | "radar"
    | "area"
    | "donut"
    | "funnel"
    | "heatmap"
    | "gauge"
    | "network";
  cats: string[];
  series: ChartSeries[];
  unit?: string;
  yMax?: number;
  nodes?: { id: string; x: number; y: number; hub?: boolean; label: string }[];
  links?: [number, number][];
  note?: string;
  caption?: string;
}) {
  const maxV = yMax ?? Math.max(...series.flatMap((s) => s.points)) * 1.12;
  const colors = ["#d20000", "rgba(255,255,255,0.85)", "rgba(210, 0, 0,0.55)", "rgba(255,255,255,0.45)"];
  const legend = (
    <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1">
      {series.map((s, i) => (
        <span key={s.name} className="inline-flex items-center gap-1.5 text-[10.5px] font-medium text-white/65">
          <span className="inline-block h-[3px] w-4 rounded-full" style={{ background: colors[i % colors.length] }} />
          {s.name}
          {unit && !s.name.includes(unit) ? ` (${unit})` : ""}
        </span>
      ))}
    </div>
  );

  return (
    <Reveal className="mt-6">
      <figure className="overflow-hidden rounded-2xl border border-white/10 grad-navy-field shadow-3">
        {/* header */}
        <div className="flex items-center justify-between border-b border-white/10 px-5 py-3">
          <div className="flex items-center gap-2">
            <span className="h-2.5 w-2.5 rounded-full bg-white/20" />
            <span className="h-2.5 w-2.5 rounded-full bg-white/20" />
            <span className="h-2.5 w-2.5 rounded-full bg-brand/70" />
            <p className="ml-2 text-[12.5px] font-semibold text-white">{title}</p>
          </div>
          <span className="rounded-full border border-white/15 bg-white/[0.06] px-2.5 py-0.5 text-[9.5px] font-bold uppercase tracking-[0.14em] text-white/60">
            {{
              line: "Trend view",
              area: "Trajectory",
              bar: "Breakdown",
              radar: "Profile",
              donut: "Composition",
              funnel: "Stage conversion",
              heatmap: "Intensity matrix",
              gauge: "Gauge read",
              network: "Topology",
            }[variant]}
          </span>
          {/* E-05: provenance chip on every chart panel */}
          <span className="rounded-full border border-white/15 bg-white/[0.06] px-2.5 py-0.5 text-[9.5px] font-bold uppercase tracking-[0.14em] text-white/60">
            Achala program — illustrative
          </span>
        </div>

        <div className="px-5 py-4">
          {variant === "line" && <LineChart cats={cats} series={series} maxV={maxV} colors={colors} />}
          {variant === "bar" && <BarChart cats={cats} series={series} maxV={maxV} colors={colors} />}
          {variant === "radar" && <RadarChart cats={cats} series={series} maxV={maxV} colors={colors} />}
          {variant === "area" && <AreaChart cats={cats} series={series} maxV={maxV} colors={colors} unit={unit} />}
          {variant === "donut" && <DonutChart cats={cats} series={series} unit={unit} center={note} />}
          {variant === "funnel" && <FunnelChart cats={cats} series={series} unit={unit} />}
          {variant === "heatmap" && <HeatmapChart cats={cats} series={series} unit={unit} />}
          {variant === "gauge" && <GaugeChart series={series} maxV={maxV} unit={unit} label={cats[0] ?? series[0]?.name ?? ""} />}
          {variant === "network" && <NetworkChart nodes={nodes} links={links} />}
          {variant !== "donut" && variant !== "gauge" && variant !== "network" && legend}
          {note && variant !== "gauge" && variant !== "network" && (
            <p className="mt-2 text-[11px] leading-relaxed text-white/45">{note}</p>
          )}
        </div>
        {caption && (
          <figcaption className="border-t border-white/10 px-5 py-2.5 text-[11.5px] leading-relaxed text-white/55">
            {caption}
          </figcaption>
        )}
      </figure>
    </Reveal>
  );
}

function LineChart({
  cats,
  series,
  maxV,
  colors,
}: {
  cats: string[];
  series: ChartSeries[];
  maxV: number;
  colors: string[];
}) {
  const W = 640;
  const H = 210;
  const PL = 44;
  const PR = 14;
  const PT = 14;
  const PB = 34;
  const iw = W - PL - PR;
  const ih = H - PT - PB;
  const n = Math.max(cats.length - 1, 1);
  const x = (i: number) => PL + (i * iw) / n;
  const y = (v: number) => PT + ih - (Math.min(v, maxV) / maxV) * ih;
  const ticks = [0, 0.25, 0.5, 0.75, 1];
  const [hover, setHover] = useState<number | null>(null);
  const svgRef = useRef<SVGSVGElement | null>(null);
  const onMove = (e: RPointerEvent<SVGSVGElement>) => {
    const r = svgRef.current?.getBoundingClientRect();
    if (!r || r.width === 0) return;
    const vx = ((e.clientX - r.left) / r.width) * W;
    setHover(Math.max(0, Math.min(cats.length - 1, Math.round(((vx - PL) / iw) * n))));
  };
  return (
    <div className="relative">
      {hover !== null && (
        <PanelTip left={(x(hover) / W) * 100}>
          <span className="font-semibold">{cats[hover]}</span>
          {series.map((s, si) => (
            <span key={s.name} className="ml-2 inline-flex items-center gap-1">
              <span aria-hidden="true" className="h-1.5 w-1.5 rounded-full" style={{ background: colors[si % colors.length] }} />
              {(s.points[hover] ?? 0).toLocaleString("en-US")}
            </span>
          ))}
        </PanelTip>
      )}
      <svg
        ref={svgRef}
        viewBox={`0 0 ${W} ${H}`}
        className="w-full cursor-crosshair"
        role="img"
        aria-label={series.map((s) => s.name).join(", ")}
        onPointerMove={onMove}
        onPointerDown={onMove}
        onPointerLeave={() => setHover(null)}
      >
        {/* horizontal grid + y labels */}
        {ticks.map((tv, i) => {
          const yy = PT + (i * ih) / (ticks.length - 1);
          const val = Math.round(maxV * (1 - tv));
          return (
            <g key={i}>
              <line x1={PL} y1={yy} x2={W - PR} y2={yy} stroke="rgba(255,255,255,0.08)" />
              <text x={PL - 6} y={yy + 3} textAnchor="end" fontSize="9" fill="rgba(255,255,255,0.4)">
                {val.toLocaleString()}
              </text>
            </g>
          );
        })}
        {/* x labels (spread) */}
        {cats.map((c, i) => {
          const show = cats.length <= 8 || i % Math.ceil(cats.length / 8) === 0 || i === cats.length - 1;
          return show ? (
            <text key={i} x={x(i)} y={H - 12} textAnchor="middle" fontSize="9" fill="rgba(255,255,255,0.5)">
              {c}
            </text>
          ) : null;
        })}
        {/* hover crosshair */}
        {hover !== null && (
          <g pointerEvents="none">
            <line x1={x(hover)} y1={PT} x2={x(hover)} y2={PT + ih} stroke="rgba(255,255,255,0.38)" strokeDasharray="3 3" />
            {series.map((s, si) => (
              <circle
                key={s.name}
                cx={x(hover)}
                cy={y(s.points[hover] ?? 0)}
                r={si === 0 ? 4.6 : 3.6}
                fill={colors[si % colors.length]}
                stroke="rgba(255,255,255,0.9)"
                strokeWidth={1.2}
              />
            ))}
          </g>
        )}
        {/* series */}
        {series.map((s, si) => {
          const d = s.points.map((v, i) => `${i === 0 ? "M" : "L"} ${x(i).toFixed(1)},${y(v).toFixed(1)}`).join(" ");
          const area = `${d} L ${x(s.points.length - 1).toFixed(1)},${(PT + ih).toFixed(1)} L ${PL},${PT + ih} Z`;
          return (
            <g key={s.name}>
              {si === 0 && <path d={area} fill="rgba(210, 0, 0,0.10)" stroke="none" />}
              <path
                d={d}
                fill="none"
                stroke={colors[si % colors.length]}
                strokeWidth={si === 0 ? 2.2 : 1.6}
                strokeLinejoin="round"
                strokeLinecap="round"
                pathLength={1}
                strokeDasharray={si === 0 ? "1" : undefined}
                style={si === 0 ? { animation: "dash-draw 1.4s 0.2s var(--ease-out, ease-out) both" } : undefined}
              />
              {s.points.map((v, i) => (
                <circle key={i} cx={x(i)} cy={y(v)} r={si === 0 ? 2.6 : 1.8} fill={colors[si % colors.length]}
                  style={{ animation: `dash-in 0.4s ${0.3 + i * 0.05}s both` }} />
              ))}
            </g>
          );
        })}
      </svg>
    </div>
  );
}

function BarChart({
  cats,
  series,
  maxV,
  colors,
}: {
  cats: string[];
  series: ChartSeries[];
  maxV: number;
  colors: string[];
}) {
  const W = 640;
  const H = 210;
  const PL = 44;
  const PR = 14;
  const PT = 14;
  const PB = 36;
  const iw = W - PL - PR;
  const ih = H - PT - PB;
  const groups = cats.length;
  const gw = iw / Math.max(groups, 1);
  const bw = Math.min(26, (gw - 10) / Math.max(series.length, 1));
  const ticks = [0, 0.5, 1];
  const [hover, setHover] = useState<number | null>(null);
  return (
    <div className="relative">
      {hover !== null && (
        <PanelTip left={((PL + hover * gw + gw / 2) / W) * 100}>
          <span className="font-semibold">{cats[hover]}</span>
          {series.map((s, si) => (
            <span key={s.name} className="ml-2 inline-flex items-center gap-1">
              <span aria-hidden="true" className="h-1.5 w-1.5 rounded-full" style={{ background: colors[si % colors.length] }} />
              {(s.points[hover] ?? 0).toLocaleString("en-US")}
            </span>
          ))}
        </PanelTip>
      )}
      <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img" aria-label={series.map((s) => s.name).join(", ")} onPointerLeave={() => setHover(null)}>
        {ticks.map((tv, i) => {
          const yy = PT + (i * ih) / (ticks.length - 1);
          return (
            <g key={i}>
              <line x1={PL} y1={yy} x2={W - PR} y2={yy} stroke="rgba(255,255,255,0.08)" />
              <text x={PL - 6} y={yy + 3} textAnchor="end" fontSize="9" fill="rgba(255,255,255,0.4)">
                {Math.round(maxV * (1 - tv)).toLocaleString()}
              </text>
            </g>
          );
        })}
        {cats.map((c, gi) => {
          const cx = PL + gi * gw + gw / 2;
          const total = series.length * (bw + 4);
          const active = hover === gi;
          const dim = hover !== null && !active;
          return (
            <g
              key={gi}
              onPointerEnter={() => setHover(gi)}
              onPointerLeave={() => setHover((v) => (v === gi ? null : v))}
              className="cursor-pointer"
            >
              <rect x={PL + gi * gw} y={PT} width={gw} height={ih} rx={6} fill="rgba(255,255,255,0.05)" opacity={active ? 1 : 0} style={{ transition: "opacity .15s" }} />
              {series.map((s, si) => {
                const v = s.points[gi] ?? 0;
                const bh = Math.max(2, (Math.min(v, maxV) / maxV) * ih);
                const bx = cx - total / 2 + si * (bw + 4);
                return (
                  <g key={si}>
                    <rect
                      x={bx}
                      y={PT + ih - bh}
                      width={bw}
                      height={bh}
                      rx={3}
                      fill={colors[si % colors.length]}
                      opacity={active ? 1 : dim ? 0.35 : si === 0 ? 0.95 : 0.75}
                      style={{ animation: `dash-col 0.7s ${0.15 + (gi * series.length + si) * 0.05}s both`, transformBox: "fill-box", transformOrigin: "bottom" }}
                    />
                    <text x={bx + bw / 2} y={PT + ih - bh - 4} textAnchor="middle" fontSize="8.5" fill="rgba(255,255,255,0.6)">
                      {v >= 1000 ? `${Math.round(v / 100) / 10}k` : v}
                    </text>
                  </g>
                );
              })}
              <text x={cx} y={H - 14} textAnchor="middle" fontSize="9.5" fill="rgba(255,255,255,0.65)">
                {c}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}

function RadarChart({
  cats,
  series,
  maxV,
  colors,
}: {
  cats: string[];
  series: ChartSeries[];
  maxV: number;
  colors: string[];
}) {
  const CX = 320;
  const CY = 112;
  const R = 86;
  const N = Math.max(cats.length, 3);
  const ang = (i: number) => (2 * Math.PI * i) / N - Math.PI / 2;
  const pt = (i: number, v: number) => {
    const r = (Math.min(v, maxV) / maxV) * R;
    return `${(CX + r * Math.cos(ang(i))).toFixed(1)},${(CY + r * Math.sin(ang(i))).toFixed(1)}`;
  };
  const rings = [0.33, 0.66, 1];
  const [hover, setHover] = useState<number | null>(null);
  return (
    <div className="relative flex flex-col items-center">
      {hover !== null && (
        <PanelTip left={((CX + (R + 10) * Math.cos(ang(hover))) / 640) * 100}>
          <span className="font-semibold">{cats[hover]}</span>
          {series.map((s, si) => (
            <span key={s.name} className="ml-2 inline-flex items-center gap-1">
              <span aria-hidden="true" className="h-1.5 w-1.5 rounded-full" style={{ background: colors[si % colors.length] }} />
              {(s.points[hover] ?? 0).toLocaleString("en-US")}
            </span>
          ))}
        </PanelTip>
      )}
      <svg viewBox="0 0 640 224" className="w-full max-w-[560px]" role="img" aria-label={series.map((s) => s.name).join(", ")} onPointerLeave={() => setHover(null)}>
        {rings.map((rv, i) => (
          <polygon
            key={i}
            points={cats.map((_, j) => pt(j, maxV * rv)).join(" ")}
            fill="none"
            stroke={i === rings.length - 1 ? "rgba(255,255,255,0.22)" : "rgba(255,255,255,0.09)"}
          />
        ))}
        {cats.map((c, i) => (
          <circle
            key={`hx${i}`}
            cx={CX + R * Math.cos(ang(i))}
            cy={CY + R * Math.sin(ang(i))}
            r={11}
            fill="rgba(0,0,0,0)"
            className="cursor-pointer"
            onPointerEnter={() => setHover(i)}
            onPointerLeave={() => setHover((v) => (v === i ? null : v))}
          />
        ))}
        {cats.map((c, i) => {
          const lx = CX + (R + 16) * Math.cos(ang(i));
          const ly = CY + (R + 14) * Math.sin(ang(i));
          const anchor = Math.abs(Math.cos(ang(i))) < 0.3 ? "middle" : Math.cos(ang(i)) > 0 ? "start" : "end";
          return (
            <g key={i}>
              <line x1={CX} y1={CY} x2={CX + R * Math.cos(ang(i))} y2={CY + R * Math.sin(ang(i))} stroke="rgba(255,255,255,0.10)" />
              <text x={lx} y={ly} textAnchor={anchor} fontSize="9.5" fill="rgba(255,255,255,0.6)">
                {c.length > 26 ? `${c.slice(0, 24)}…` : c}
              </text>
            </g>
          );
        })}
        {series.map((s, si) => (
          <g key={s.name}>
            <polygon
              points={s.points.map((v, i) => pt(i, v)).join(" ")}
              fill={si === 0 ? "rgba(210, 0, 0,0.16)" : "rgba(255,255,255,0.07)"}
              stroke={colors[si % colors.length]}
              strokeWidth={si === 0 ? 2 : 1.4}
              style={{ animation: `dash-in 0.8s ${0.2 + si * 0.2}s both`, transformBox: "fill-box", transformOrigin: "center" }}
            />
            {s.points.map((v, i) => {
              const [px, py] = pt(i, v).split(",").map(Number);
              const hov = hover === i;
              return (
                <circle
                  key={i}
                  cx={px}
                  cy={py}
                  r={hov ? 4.4 : 2.2}
                  fill={colors[si % colors.length]}
                  stroke={hov ? "rgba(255,255,255,0.92)" : "none"}
                  strokeWidth={1.2}
                />
              );
            })}
          </g>
        ))}
      </svg>
    </div>
  );
}

/* ── Area chart — smooth cumulative/trajectory band ─────────────────────── */
function AreaChart({
  cats,
  series,
  maxV,
  colors,
  unit,
}: {
  cats: string[];
  series: ChartSeries[];
  maxV: number;
  colors: string[];
  unit?: string;
}) {
  const W = 640;
  const H = 220;
  const PL = 46;
  const PR = 16;
  const PT = 16;
  const PB = 36;
  const iw = W - PL - PR;
  const ih = H - PT - PB;
  const n = Math.max(cats.length - 1, 1);
  const x = (i: number) => PL + (i * iw) / n;
  const y = (v: number) => PT + ih - (Math.min(v, maxV) / maxV) * ih;
  const ticks = [0, 0.25, 0.5, 0.75, 1];
  const [hover, setHover] = useState<number | null>(null);
  const svgRef = useRef<SVGSVGElement | null>(null);
  const onMove = (e: RPointerEvent<SVGSVGElement>) => {
    const r = svgRef.current?.getBoundingClientRect();
    if (!r || r.width === 0) return;
    const vx = ((e.clientX - r.left) / r.width) * W;
    setHover(Math.max(0, Math.min(cats.length - 1, Math.round(((vx - PL) / iw) * n))));
  };
  return (
    <div className="relative">
      {hover !== null && (
        <PanelTip left={(x(hover) / W) * 100}>
          <span className="font-semibold">{cats[hover]}</span>
          {series.map((s, si) => (
            <span key={s.name} className="ml-2 inline-flex items-center gap-1">
              <span aria-hidden="true" className="h-1.5 w-1.5 rounded-full" style={{ background: colors[si % colors.length] }} />
              {(s.points[hover] ?? 0).toLocaleString("en-US")}
              {unit ? ` ${unit}` : ""}
            </span>
          ))}
        </PanelTip>
      )}
      <svg
        ref={svgRef}
        viewBox={`0 0 ${W} ${H}`}
        className="w-full cursor-crosshair"
        role="img"
        aria-label={series.map((s) => s.name).join(", ")}
        onPointerMove={onMove}
        onPointerDown={onMove}
        onPointerLeave={() => setHover(null)}
      >
      <defs>
        <linearGradient id="dv-area-fill" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="rgba(210, 0, 0,0.38)" />
          <stop offset="100%" stopColor="rgba(210, 0, 0,0.04)" />
        </linearGradient>
      </defs>
      {ticks.map((tv, i) => {
        const yy = PT + (i * ih) / (ticks.length - 1);
        return (
          <g key={i}>
            <line x1={PL} y1={yy} x2={W - PR} y2={yy} stroke="rgba(255,255,255,0.08)" />
            <text x={PL - 6} y={yy + 3} textAnchor="end" fontSize="9" fill="rgba(255,255,255,0.4)">
              {Math.round(maxV * (1 - tv)).toLocaleString()}
              {i === ticks.length - 1 && unit ? ` ${unit}` : ""}
            </text>
          </g>
        );
      })}
      {hover !== null && (
        <g pointerEvents="none">
          <line x1={x(hover)} y1={PT} x2={x(hover)} y2={PT + ih} stroke="rgba(255,255,255,0.38)" strokeDasharray="3 3" />
          {series.map((s, si) => (
            <circle
              key={s.name}
              cx={x(hover)}
              cy={y(s.points[hover] ?? 0)}
              r={si === 0 ? 4.8 : 3.4}
              fill={colors[si % colors.length]}
              stroke="rgba(255,255,255,0.9)"
              strokeWidth={1.2}
            />
          ))}
        </g>
      )}
      {series.map((s, si) => {
        // smooth curve through points
        const pts = s.points.map((v, i) => [x(i), y(v)] as const);
        let d = `M ${pts[0][0]},${pts[0][1]}`;
        for (let i = 1; i < pts.length; i++) {
          const [x0, y0] = pts[i - 1];
          const [x1, y1] = pts[i];
          const mx = (x0 + x1) / 2;
          d += ` C ${mx},${y0} ${mx},${y1} ${x1},${y1}`;
        }
        const area = `${d} L ${pts[pts.length - 1][0]},${PT + ih} L ${pts[0][0]},${PT + ih} Z`;
        return (
          <g key={s.name}>
            {si === 0 && <path d={area} fill="url(#dv-area-fill)" stroke="none" />}
            <path
              d={d}
              fill="none"
              stroke={colors[si % colors.length]}
              strokeWidth={si === 0 ? 2.4 : 1.6}
              strokeLinecap="round"
              pathLength={1}
              strokeDasharray={si === 0 ? "1" : undefined}
              style={si === 0 ? { animation: "dash-draw 1.6s 0.2s var(--ease-out, ease-out) both" } : undefined}
            />
            {s.points.map((v, i) => (
              <circle key={i} cx={x(i)} cy={y(v)} r={si === 0 ? 3 : 2} fill={colors[si % colors.length]}
                style={{ animation: `dash-in 0.4s ${0.3 + i * 0.06}s both` }} />
            ))}
          </g>
        );
      })}
      {cats.map((c, i) => {
        const show = cats.length <= 10 || i % Math.ceil(cats.length / 10) === 0 || i === cats.length - 1;
        return show ? (
          <text key={i} x={x(i)} y={H - 12} textAnchor="middle" fontSize="9" fill="rgba(255,255,255,0.5)">
            {c}
          </text>
        ) : null;
      })}
      </svg>
    </div>
  );
}

/* ── Donut — composition share ──────────────────────────────────────────── */
function DonutChart({
  cats,
  series,
  unit,
  center,
}: {
  cats: string[];
  series: ChartSeries[];
  unit?: string;
  center?: string;
}) {
  const vals = series[0]?.points ?? [];
  const total = vals.reduce((a, b) => a + b, 0) || 1;
  const centerText =
    center && center.length <= 16 ? center : unit ? `${total} ${unit}` : String(total);
  const PALETTE = ["#d20000", "rgba(254,135,80,0.92)", "#7C6FF0", "rgba(255,255,255,0.75)", "rgba(210, 0, 0,0.5)", "#3ECFB2", "rgba(255,255,255,0.4)", "#F0B429"];
  const CX = 150;
  const CY = 110;
  const R = 72;
  const SW = 26;
  const [hover, setHover] = useState<number | null>(null);
  let acc = -Math.PI / 2;
  const segs = vals.map((v, i) => {
    const a0 = acc;
    const a1 = acc + (v / total) * Math.PI * 2;
    acc = a1;
    const large = a1 - a0 > Math.PI ? 1 : 0;
    const p0 = [CX + R * Math.cos(a0), CY + R * Math.sin(a0)];
    const p1 = [CX + R * Math.cos(a1), CY + R * Math.sin(a1)];
    return {
      d: `M ${p0[0].toFixed(1)},${p0[1].toFixed(1)} A ${R},${R} 0 ${large} 1 ${p1[0].toFixed(1)},${p1[1].toFixed(1)}`,
      color: PALETTE[i % PALETTE.length],
      pct: Math.round((v / total) * 100),
      name: cats[i] ?? `#${i}`,
      v,
      delay: i * 0.12,
    };
  });
  return (
    <div className="flex flex-col items-center gap-4 sm:flex-row sm:items-center sm:justify-center sm:gap-8">
      <svg viewBox="0 0 300 220" className="w-full max-w-[300px]" role="img" aria-label={cats.join(", ")}>
        {segs.map((s, k) => (
          <path
            key={s.name}
            d={s.d}
            fill="none"
            stroke={s.color}
            strokeWidth={hover === k ? SW + 7 : SW}
            strokeLinecap="butt"
            pathLength={1}
            className="cursor-pointer"
            onPointerEnter={() => setHover(k)}
            onPointerLeave={() => setHover((v) => (v === k ? null : v))}
            style={{ animation: "dash-draw 0.9s both", animationDelay: `${s.delay}s`, opacity: hover === null ? 0.92 : hover === k ? 1 : 0.45, transition: "opacity .15s, stroke-width .15s" }}
          />
        ))}
        <text x={CX} y={CY - 4} textAnchor="middle" fontSize={hover !== null ? "14" : "22"} fontWeight="800" fill="rgba(255,255,255,0.95)">
          {hover !== null ? segs[hover].name.slice(0, 14) : centerText}
        </text>
        <text x={CX} y={CY + 16} textAnchor="middle" fontSize="9" fill="rgba(255,255,255,0.5)" letterSpacing="0.12em">
          {hover !== null
            ? `${segs[hover].pct}% · ${segs[hover].v.toLocaleString("en-US")}${unit ? ` ${unit}` : ""}`
            : "TOTAL"}
        </text>
      </svg>
      <ul className="grid w-full max-w-[320px] gap-1.5">
        {segs.map((s, k) => (
          <li
            key={s.name}
            className={`flex cursor-pointer items-center gap-2 rounded-md px-1.5 py-0.5 text-[11.5px] ${hover === k ? "bg-white/10" : ""}`}
            style={{ animation: `dash-in 0.5s ${s.delay}s both`, transition: "background .15s" }}
            onPointerEnter={() => setHover(k)}
            onPointerLeave={() => setHover((v) => (v === k ? null : v))}
          >
            <span className="h-2.5 w-2.5 shrink-0 rounded-sm" style={{ background: s.color }} />
            <span className="flex-1 truncate text-white/75">{s.name}</span>
            <span className="font-semibold tabular-nums text-white/90">
              {s.pct}%
              {hover === k ? (
                <span className="ml-1.5 font-normal text-white/55">
                  · {s.v.toLocaleString("en-US")}
                  {unit ? ` ${unit}` : ""}
                </span>
              ) : null}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}

/* ── Funnel — stage conversion ──────────────────────────────────────────── */
function FunnelChart({
  cats,
  series,
  unit,
}: {
  cats: string[];
  series: ChartSeries[];
  unit?: string;
}) {
  const vals = series[0]?.points ?? [];
  const top = Math.max(...vals, 1);
  const W = 640;
  const ROW = Math.min(44, 200 / Math.max(vals.length, 1));
  const H = vals.length * (ROW + 8) + 16;
  const CXm = W / 2;
  const halfTop = 250;
  const [hover, setHover] = useState<number | null>(null);
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img" aria-label={cats.join(", ")} onPointerLeave={() => setHover(null)}>
      {vals.map((v, i) => {
        const half = halfTop * Math.max(0.16, Math.sqrt(v / top));
        const yTop = 10 + i * (ROW + 8);
        const nextHalf = i < vals.length - 1 ? halfTop * Math.max(0.16, Math.sqrt(vals[i + 1] / top)) : half;
        const yBot = yTop + ROW;
        const poly = `${CXm - half},${yTop} ${CXm + half},${yTop} ${CXm + nextHalf},${yBot} ${CXm - nextHalf},${yBot}`;
        const fill = i === 0 ? "rgba(210, 0, 0,0.85)" : `rgba(210, 0, 0,${Math.max(0.28, 0.7 - i * 0.09)})`;
        const active = hover === i;
        const dim = hover !== null && !active;
        return (
          <g key={cats[i] ?? i} onPointerEnter={() => setHover(i)} onPointerLeave={() => setHover((v) => (v === i ? null : v))} className="cursor-pointer">
            <polygon
              points={poly}
              fill={fill}
              opacity={dim ? 0.35 : 1}
              stroke={active ? "rgba(255,255,255,0.9)" : "none"}
              strokeWidth={1.3}
              style={{ animation: `dash-in 0.5s ${0.15 + i * 0.12}s both`, transition: "opacity .15s" }}
            />
            <text x={CXm - half - 12} y={yTop + ROW / 2 + 3.5} textAnchor="end" fontSize="10.5" fill="rgba(255,255,255,0.72)" fontWeight="600">
              {cats[i]}
            </text>
            <text x={CXm} y={yTop + ROW / 2 + 4} textAnchor="middle" fontSize="12" fontWeight="800" fill="white">
              {v.toLocaleString()}
              {unit ? ` ${unit}` : ""}
            </text>
            {i < vals.length - 1 && vals[i] > 0 && (
              <text x={CXm + half + 10} y={yBot + 2} fontSize="9.5" fill="rgba(255,255,255,0.45)">
                {Math.round((vals[i + 1] / vals[i]) * 100)}% carry
              </text>
            )}
          </g>
        );
      })}
    </svg>
  );
}

/* ── Heatmap — intensity matrix (rows = cats, cols = series) ────────────── */
function HeatmapChart({
  cats,
  series,
  unit,
}: {
  cats: string[];
  series: ChartSeries[];
  unit?: string;
}) {
  const all = series.flatMap((s) => s.points);
  const lo = Math.min(...all);
  const hi = Math.max(...all);
  const CW = 92;
  const RH = 30;
  const LBW = 148;
  const W = LBW + series.length * CW + 60;
  const H = 34 + cats.length * RH + 16;
  const [hov, setHov] = useState<string | null>(null);
  const shade = (v: number) => {
    if (hi === lo) return 0.55;
    return 0.1 + 0.8 * ((v - lo) / (hi - lo));
  };
  return (
    <div className="relative">
      {hov && (
        <PanelTip left={((LBW + Number(hov.split("-")[1]) * CW + CW / 2) / W) * 100}>
          <span className="font-semibold">{cats[Number(hov.split("-")[0])]}</span>
          <span className="ml-1.5 text-white/70">{series[Number(hov.split("-")[1])]?.name}</span>
          <span className="ml-1.5 font-semibold">
            {(series[Number(hov.split("-")[1])]?.points[Number(hov.split("-")[0])] ?? 0).toLocaleString("en-US")}
            {unit ? ` ${unit}` : ""}
          </span>
        </PanelTip>
      )}
      <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img" aria-label={cats.join(", ")} onPointerLeave={() => setHov(null)}>
      {series.map((s, ci) => (
        <text
          key={s.name}
          x={LBW + ci * CW + CW / 2}
          y={20}
          textAnchor="middle"
          fontSize="9.5"
          fontWeight="700"
          fill="rgba(254,135,80,0.95)"
        >
          {s.name.length > 14 ? `${s.name.slice(0, 12)}…` : s.name}
        </text>
      ))}
      {cats.map((r, ri) => {
        const y = 34 + ri * RH;
        return (
          <g key={r}>
            <text x={LBW - 10} y={y + RH / 2 + 3.5} textAnchor="end" fontSize="10" fill="rgba(255,255,255,0.7)">
              {r.length > 24 ? `${r.slice(0, 22)}…` : r}
            </text>
            {series.map((s, ci) => {
              const v = s.points[ri] ?? 0;
              const cell = `${ri}-${ci}`;
              return (
                <g
                  key={ci}
                  className="cursor-pointer"
                  onPointerEnter={() => setHov(cell)}
                  onPointerLeave={() => setHov((v) => (v === cell ? null : v))}
                >
                  <rect
                    x={LBW + ci * CW + 3}
                    y={y + 3}
                    width={CW - 6}
                    height={RH - 6}
                    rx={5}
                    fill={`rgba(210, 0, 0,${shade(v)})`}
                    stroke={hov === cell ? "rgba(255,255,255,0.9)" : "rgba(255,255,255,0.10)"}
                    strokeWidth={hov === cell ? 1.6 : 1}
                    style={{ animation: `dash-in 0.4s ${(ri * series.length + ci) * 0.02}s both` }}
                  />
                  <text
                    x={LBW + ci * CW + CW / 2}
                    y={y + RH / 2 + 3.5}
                    textAnchor="middle"
                    fontSize="9.5"
                    fontWeight="700"
                    fill={shade(v) > 0.55 ? "rgba(255,255,255,0.96)" : "rgba(255,255,255,0.62)"}
                  >
                    {v}
                    {unit && !Number.isNaN(Number(v)) ? "" : ""}
                  </text>
                </g>
              );
            })}
          </g>
        );
      })}
      </svg>
    </div>
  );
}

/* ── Gauge — single live indicator with threshold band ──────────────────── */
function GaugeChart({
  series,
  maxV,
  unit,
  label,
}: {
  series: ChartSeries[];
  maxV: number;
  unit?: string;
  label: string;
}) {
  const v = series[0]?.points[0] ?? 0;
  const frac = Math.max(0, Math.min(1, v / maxV));
  const CX = 160;
  const CY = 120;
  const R = 88;
  const a0 = Math.PI * 0.75;
  const a1 = Math.PI * 2.25;
  const arc = (from: number, to: number) => {
    const p0 = [CX + R * Math.cos(from), CY + R * Math.sin(from)];
    const p1 = [CX + R * Math.cos(to), CY + R * Math.sin(to)];
    return `M ${p0[0].toFixed(1)},${p0[1].toFixed(1)} A ${R},${R} 0 ${to - from > Math.PI ? 1 : 0} 1 ${p1[0].toFixed(1)},${p1[1].toFixed(1)}`;
  };
  const av = a0 + (a1 - a0) * frac;
  const needle = [CX + (R - 14) * Math.cos(av), CY + (R - 14) * Math.sin(av)];
  const [hov, setHov] = useState(false);
  return (
    <div className="flex flex-col items-center sm:flex-row sm:justify-center sm:gap-10">
      <div className="relative">
        {hov && (
          <PanelTip left={50}>
            <span className="font-semibold">{label}</span>
            <span className="ml-1.5">
              {v.toLocaleString("en-US")}
              {unit ? ` ${unit}` : ""} · {Math.round(frac * 100)}% of scale
            </span>
          </PanelTip>
        )}
        <svg
          viewBox="0 0 320 190"
          className="w-full max-w-[320px] cursor-pointer"
          role="img"
          aria-label={label}
          onPointerEnter={() => setHov(true)}
          onPointerLeave={() => setHov(false)}
        >
        <path d={arc(a0, a1)} fill="none" stroke="rgba(255,255,255,0.10)" strokeWidth={20} strokeLinecap="round" />
        <path
          d={arc(a0, av)}
          fill="none"
          stroke={hov ? "#ff4040" : "#d20000"}
          strokeWidth={hov ? 22 : 20}
          strokeLinecap="round"
          pathLength={1}
          style={{ animation: "dash-draw 1.3s 0.2s var(--ease-out, ease-out) both", transition: "stroke .15s, stroke-width .15s" }}
        />
        <line x1={CX} y1={CY} x2={needle[0]} y2={needle[1]} stroke="rgba(255,255,255,0.9)" strokeWidth={2.5} strokeLinecap="round"
          style={{ animation: "dash-in 0.6s 1.3s both", transformOrigin: `${CX}px ${CY}px` }} />
        <circle cx={CX} cy={CY} r={5.5} fill="#d20000" />
        <text x={CX} y={CY - 26} textAnchor="middle" fontSize="26" fontWeight="800" fill="white">
          {v.toLocaleString()}
          <tspan fontSize="12" fill="rgba(255,255,255,0.55)">{unit ? ` ${unit}` : ""}</tspan>
        </text>
        <text x={CX} y={CY + 34} textAnchor="middle" fontSize="10" fill="rgba(255,255,255,0.55)">
          scale 0 – {maxV.toLocaleString()}
        </text>
        </svg>
      </div>
      <div className="max-w-[300px] text-center sm:text-left">
        <p className="text-[12.5px] font-semibold text-white/90">{label}</p>
        <p className="mt-1 text-[11.5px] leading-relaxed text-white/55">
          Reference indicator for this practice — pinned against the signed baseline and re-scored at every gate review.
        </p>
      </div>
    </div>
  );
}

/* ── Network — topology graph from JSON node coordinates ────────────────── */
function NetworkChart({
  nodes,
  links,
}: {
  nodes?: { id: string; x: number; y: number; hub?: boolean; label: string }[];
  links?: [number, number][];
}) {
  const ns = (nodes ?? []).slice(0, 22);
  const ls = (links ?? []).filter(([a, b]) => a < ns.length && b < ns.length);
  const W = 640;
  const H = 240;
  const px = (f: number) => 40 + f * (W - 80);
  const py = (f: number) => 22 + f * (H - 44);
  const [hov, setHov] = useState<number | null>(null);
  return (
    <div className="relative">
      {hov !== null && ns[hov] && (
        <PanelTip left={(px(ns[hov].x) / W) * 100}>
          <span className="font-semibold">{ns[hov].label}</span>
          {ns[hov].hub ? <span className="ml-1.5 text-brand-300">hub</span> : null}
        </PanelTip>
      )}
      <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img" aria-label={ns.map((n) => n.label).join(", ")} onPointerLeave={() => setHov(null)}>
        {ls.map(([a, b], i) => {
          const A = ns[a];
          const B = ns[b];
          if (!A || !B) return null;
          const mx = (px(A.x) + px(B.x)) / 2;
          const my = (py(A.y) + py(B.y)) / 2;
          const hot = hov !== null && (a === hov || b === hov);
          const dim = hov !== null && !hot;
          return (
            <path
              key={i}
              d={`M ${px(A.x)},${py(A.y)} Q ${mx},${my} ${px(B.x)},${py(B.y)}`}
              fill="none"
              stroke={hot ? "rgba(210,0,0,0.9)" : dim ? "rgba(255,255,255,0.07)" : "rgba(255,255,255,0.18)"}
              strokeWidth={hot ? 2 : 1.2}
              style={{ transition: "stroke .15s" }}
            />
          );
        })}
        {ns.map((n, i) => {
          const r = (n.hub ? 22 : 14) + (hov === i ? 4 : 0);
          return (
            <g
              key={n.id}
              className="cursor-pointer"
              onPointerEnter={() => setHov(i)}
              onPointerLeave={() => setHov((v) => (v === i ? null : v))}
              style={{ animation: `dash-in 0.5s ${0.1 + i * 0.04}s both` }}
            >
              <circle
                cx={px(n.x)}
                cy={py(n.y)}
                r={r}
                fill={hov === i ? "rgba(210, 0, 0,0.38)" : n.hub ? "rgba(210, 0, 0,0.22)" : "rgba(255,255,255,0.06)"}
                stroke={hov === i ? "rgba(255,255,255,0.95)" : n.hub ? "rgba(210, 0, 0,0.85)" : "rgba(255,255,255,0.4)"}
                strokeWidth={n.hub ? 1.8 : 1.1}
                style={{ transition: "fill .15s, stroke .15s" }}
              />
              <text x={px(n.x)} y={py(n.y) + 3} textAnchor="middle" fontSize={n.hub ? 10 : 8.5} fontWeight="700" fill="rgba(255,255,255,0.9)">
                {n.label.length > 12 ? `${n.label.slice(0, 10)}…` : n.label}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}

/* keyframes injected once (used by tiles/bars/log rows) */
export function DashStyles() {
  return (
    <style>{`
      @keyframes dash-in { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
      @keyframes dash-bar { from { width: 4% !important; } }
      @keyframes dash-col { from { transform: scaleY(0.04); } to { transform: scaleY(1); } }
      @keyframes dash-draw { from { stroke-dashoffset: 1; } to { stroke-dashoffset: 0; } }
      @media (prefers-reduced-motion: reduce) {
        [style*="dash-in"], [style*="dash-bar"], [style*="dash-col"], [style*="dash-draw"] { animation: none !important; }
      }
    `}</style>
  );
}
