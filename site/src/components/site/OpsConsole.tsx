"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { HelpCircle } from "lucide-react";

/* ── OpsConsole v2 — the leadership panel in the homepage hero ──────────────
   THE 3-GRAPH FIX: the hero previously rendered one static fraud chart no
   matter what was on screen. Now the console carries three program views,
   each derived from a different solution track we deliver —
     1. Fraud decisioning (Decision Intelligence, banking)
     2. Claims automation (Agentic AI, insurance)
     3. Asset performance (Digital Twin / IoT, manufacturing)
   — and each view has its OWN interactive graph: hover for a crosshair and
   the exact values at any point, animated draw-in on every switch, auto-
   rotation every 7s (pauses on hover / after manual interaction).
   E-04: labeled "Illustrative — reference program", never claiming liveness.
   A-06: every KPI tile carries a plain-language tooltip.
   Client component; reduced-motion aware. */

type LogRow = { t: string; tag: string; msg: string };

type Program = {
  key: string;
  tab: string;
  sector: string;
  chartTitle: string;
  chartUnit: string;
  /** the headline delta, bound to the hero proof line */
  delta: string;
  kpis: { label: string; value: string; delta: string; dir: "up" | "flat" | "down"; plain: string; aria: string }[];
  gates: { name: string; pct: number }[];
  log: LogRow[];
  nextLog: LogRow[];
  series: number[];
  compare: number[];
  labels: string[];
  note: string;
};

const mk = (seed: number, n = 24, drift: (i: number) => number, spread = 7): number[] => {
  let x = seed;
  const out: number[] = [];
  for (let i = 0; i < n; i++) {
    x = (x * 9301 + 49297) % 233280;
    const r = x / 233280;
    out.push(Math.max(4, Math.min(97, drift(i) + (r - 0.5) * spread)));
  }
  return out;
};

const PROGRAMS: Program[] = [
  {
    key: "fraud",
    tab: "Fraud decisioning",
    sector: "Banking · Decision Intelligence",
    chartTitle: "Fraud losses per 1,000 transactions",
    chartUnit: "",
    delta: "38% lower fraud losses",
    kpis: [
      { label: "Decisions today", value: "1.9M", delta: "streaming", dir: "flat", plain: "How many decisions the program runs per day, across every channel.", aria: "Decisions today: 1.9 million per day" },
      { label: "Decision p95", value: "148ms", delta: "within SLO", dir: "flat", plain: "95% of decisions finish faster than this — speed your customers actually feel.", aria: "Decision p95: 148 milliseconds" },
      { label: "Fraud losses", value: "−38%", delta: "vs baseline", dir: "down", plain: "Measured from the baseline your metric owner signed in week two.", aria: "Fraud losses down 38 percent against baseline" },
      { label: "Under replay", value: "100%", delta: "audit-ready", dir: "up", plain: "Every decision can be replayed later with the same inputs — that is what auditors test.", aria: "Under replay: 100 percent" },
    ],
    gates: [
      { name: "Baseline", pct: 100 },
      { name: "Channel slice live", pct: 82 },
      { name: "All rails live", pct: 64 },
      { name: "Industrialized", pct: 41 },
    ],
    log: [
      { t: "14:02:11", tag: "DECISION", msg: "credit limit review — approved, policy v2.4.1, replay id 8f3c" },
      { t: "14:01:41", tag: "INTERDICT", msg: "fraud interdiction — blocked, challenge issued, evidence attached" },
      { t: "14:01:22", tag: "GATE", msg: "wave 3 gate passed — reconciliation delta 0.00%, signed" },
    ],
    nextLog: [
      { t: "", tag: "DECISION", msg: "instant-rail payment scored — released, evidence pack attached" },
      { t: "", tag: "MODEL", msg: "challenger promoted — task quality +3.1pts, serving cost −12%" },
      { t: "", tag: "REPLAY", msg: "decision replay queried — 12ms p95, full trail" },
    ],
    series: mk(11, 24, (i) => 88 - (i / 23) * 52),
    compare: mk(29, 24, () => 74, 6),
    labels: ["Q1", "", "", "", "Q2", "", "", "", "Q3", "", "", "", "Q4", "", "", "", "Q1", "", "", "", "Q2", "", "", ""],
    note: "Fortnightly fraud-loss read against the signed baseline — the curve the CFO already owns.",
  },
  {
    key: "claims",
    tab: "Claims automation",
    sector: "Insurance · Agentic AI",
    chartTitle: "Claim turnaround time, hours",
    chartUnit: "h",
    delta: "55% faster claims",
    kpis: [
      { label: "Claims auto-decided", value: "63%", delta: "+8pts", dir: "up", plain: "How many claims run without a human touch — the rest deliberately keep one.", aria: "Autonomous share: 63 percent, up 8 points" },
      { label: "Turnaround p50", value: "21h", delta: "was 46h", dir: "down", plain: "The median claim now settles in under a day — measured, not promised.", aria: "Median turnaround 21 hours, down from 46" },
      { label: "Agent fleet", value: "216", delta: "governed", dir: "flat", plain: "Agents under policy envelopes — every action inside a signed guardrail.", aria: "216 automations governed" },
      { label: "Containment", value: "78%", delta: "portfolio", dir: "up", plain: "Share of claim volume that never escalates beyond the governed fleet.", aria: "78 percent portfolio containment" },
    ],
    gates: [
      { name: "Baseline", pct: 100 },
      { name: "Straight-through live", pct: 76 },
      { name: "Adjuster assist live", pct: 58 },
      { name: "Industrialized", pct: 37 },
    ],
    log: [
      { t: "14:02:09", tag: "AGENT", msg: "prior-auth package assembled — policy citations included" },
      { t: "14:01:47", tag: "DECISION", msg: "straight-through settlement — within guardrails, ledger posted" },
      { t: "14:01:15", tag: "GATE", msg: "human handoff rails verified — 0 unattended overrides" },
    ],
    nextLog: [
      { t: "", tag: "AGENT", msg: "KYC file assembled — 14 sources cited, routed to analyst" },
      { t: "", tag: "POLICY", msg: "guardrail update staged — envelope v14, approver signed" },
      { t: "", tag: "DECISION", msg: "complex claim routed to adjuster — confidence 0.81, context attached" },
    ],
    series: mk(47, 24, (i) => 86 - (i / 23) * 56),
    compare: mk(71, 24, () => 62, 5),
    labels: ["W1", "", "", "", "W4", "", "", "", "W7", "", "", "", "W10", "", "", "", "W13", "", "", "", "W16", "", "", ""],
    note: "Weekly turnaround read — every hour saved is a customer who got paid sooner.",
  },
  {
    key: "oee",
    tab: "Asset performance",
    sector: "Manufacturing · Digital Twin",
    chartTitle: "Overall equipment effectiveness, %",
    chartUnit: "%",
    delta: "OEE +7.2 pts",
    kpis: [
      { label: "OEE", value: "85.6%", delta: "+7.2 pts", dir: "up", plain: "Overall equipment effectiveness — availability × performance × quality, from your own plant systems.", aria: "OEE 85.6 percent, up 7.2 points" },
      { label: "Unplanned downtime", value: "−31%", delta: "vs baseline", dir: "down", plain: "Failures predicted before they stop the line — maintenance windows become planned ones.", aria: "Unplanned downtime down 31 percent" },
      { label: "Assets instrumented", value: "1,842", delta: "twinned", dir: "flat", plain: "Physical assets mirrored live in the twin — sensors, PLCs and historians fused.", aria: "1,842 assets instrumented" },
      { label: "Fleet OTA success", value: "99.7%", delta: "safe rollout", dir: "up", plain: "Over-the-air updates landing safely across the fleet, with rollback armed.", aria: "99.7 percent fleet OTA success" },
    ],
    gates: [
      { name: "Baseline", pct: 100 },
      { name: "Line 1–4 twinned", pct: 71 },
      { name: "Predictive live", pct: 55 },
      { name: "Fleet rollout", pct: 33 },
    ],
    log: [
      { t: "14:02:18", tag: "TWIN", msg: "line 3 state sync — 412 sensors, drift 0.4ms" },
      { t: "14:01:52", tag: "PREDICT", msg: "bearing wear flagged on press 7 — window proposed, planner notified" },
      { t: "14:01:20", tag: "GATE", msg: "twin fidelity gate passed — 99.2% state match, signed" },
    ],
    nextLog: [
      { t: "", tag: "TWIN", msg: "scenario replay queued — changeover simulation, line 2" },
      { t: "", tag: "PREDICT", msg: "RUL confidence 0.94 — maintenance window scheduled" },
      { t: "", tag: "GATE", msg: "OTA safety gate — canary 5%, rollback armed" },
    ],
    series: mk(83, 24, (i) => 55 + (i / 23) * 30),
    compare: mk(97, 24, () => 66, 4),
    labels: ["M1", "", "", "", "M3", "", "", "", "M6", "", "", "", "M9", "", "", "", "M12", "", "", "", "M15", "", "", ""],
    note: "Monthly OEE read from your plant systems — availability, performance and quality in one line.",
  },
];

/* deterministic series helper — SSR/CSR markup always matches */
function seriesOf(seed: number, n = 46): number[] {
  const out: number[] = [];
  let x = seed;
  for (let i = 0; i < n; i++) {
    x = (x * 9301 + 49297) % 233280;
    const r = x / 233280;
    const base = 46 + Math.sin(i / 6) * 14 + Math.sin(i / 2.2) * 6;
    out.push(Math.max(8, Math.min(96, base + (r - 0.5) * 18)));
  }
  return out;
}
const W = 320;
const H = 96;
const PAD = 6;
const pathFor = (vals: number[]): string => {
  const step = (W - PAD * 2) / Math.max(1, vals.length - 1);
  return vals
    .map((v, i) => `${i === 0 ? "M" : "L"} ${PAD + i * step},${H - PAD - (v / 100) * (H - PAD * 2)}`)
    .join(" ");
};

export default function OpsConsole() {
  const [prog, setProg] = useState(0);
  const [tick, setTick] = useState(0);
  const [hoverI, setHoverI] = useState<number | null>(null);
  const [log, setLog] = useState<LogRow[]>(PROGRAMS[0].log);
  const holdUntil = useRef(0);
  const P = PROGRAMS[prog];

  /* auto-rotate programs — pauses 18s after any manual choice or hover */
  useEffect(() => {
    const iv = setInterval(() => {
      if (Date.now() < holdUntil.current) return;
      if (document.hidden) return;
      if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
      setProg((p) => (p + 1) % PROGRAMS.length);
    }, 7000);
    return () => clearInterval(iv);
  }, []);

  /* streaming log rows for the active program */
  useEffect(() => {
    setLog(PROGRAMS[prog].log);
  }, [prog]);
  useEffect(() => {
    const iv = setInterval(() => setTick((t) => t + 1), 3400);
    return () => clearInterval(iv);
  }, []);
  useEffect(() => {
    if (tick === 0) return;
    const pool = P.nextLog;
    const nxt = pool[(tick - 1) % pool.length];
    setLog((cur) => {
      const stamped = { ...nxt, t: new Date().toLocaleTimeString("en-GB", { hour12: false }) };
      return [stamped, ...cur].slice(0, 3);
    });
  }, [tick]); // eslint-disable-line react-hooks/exhaustive-deps

  const pick = (i: number) => {
    holdUntil.current = Date.now() + 18000;
    setProg(i);
  };

  /* hover → nearest index on the chart */
  const svgHover = (e: React.PointerEvent<SVGSVGElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const vx = ((e.clientX - rect.left) / rect.width) * W;
    const n = P.series.length;
    const step = (W - PAD * 2) / (n - 1);
    const i = Math.max(0, Math.min(n - 1, Math.round((vx - PAD) / step)));
    setHoverI(i);
  };

  const labelFor = (i: number) => {
    const n = P.labels.length;
    for (let k = i; k >= 0; k--) if (P.labels[k]) return P.labels[k];
    for (let k = i; k < n; k++) if (P.labels[k]) return P.labels[k];
    return "";
  };
  const valAt = (arr: number[], i: number) => arr[Math.min(i, arr.length - 1)] ?? 0;
  const tipX = useMemo(() => {
    const n = P.series.length;
    const step = (W - PAD * 2) / (n - 1);
    return hoverI === null ? 0 : ((PAD + hoverI * step) / W) * 100;
  }, [hoverI, P]);

  return (
    <div
      className="rounded-2xl border border-white/12 bg-navy-950/70 shadow-3 backdrop-blur"
      onPointerEnter={() => (holdUntil.current = Date.now() + 3000)}
    >
      {/* window chrome */}
      <div className="flex items-center justify-between border-b border-white/10 px-4 py-2.5">
        <div className="flex items-center gap-2">
          <span className="h-2.5 w-2.5 rounded-full bg-white/15" />
          <span className="h-2.5 w-2.5 rounded-full bg-white/15" />
          <span className="h-2.5 w-2.5 rounded-full bg-brand/80" />
          <p className="ml-2 text-[12px] font-semibold text-white/85">Reference program view — {P.tab.toLowerCase()}</p>
        </div>
        <span
          id="prov"
          className="inline-flex items-center gap-1.5 rounded-full border border-white/20 bg-white/[0.06] px-2.5 py-0.5 text-[9.5px] font-bold uppercase tracking-[0.14em] text-white/60"
        >
          Illustrative — reference program
        </span>
      </div>

      <div className="px-4 py-3.5">
        {/* program switcher — three solution tracks, three graphs */}
        <div role="tablist" aria-label="Reference programs" className="flex gap-1 rounded-xl border border-white/10 bg-white/[0.04] p-1">
          {PROGRAMS.map((p, i) => (
            <button
              key={p.key}
              role="tab"
              aria-selected={i === prog}
              onClick={() => pick(i)}
              className={`relative flex-1 rounded-lg px-2 py-1.5 text-[10.5px] font-semibold transition-all duration-300 ${
                i === prog ? "bg-brand text-white shadow-2" : "text-white/55 hover:bg-white/[0.07] hover:text-white/85"
              }`}
            >
              {p.tab}
            </button>
          ))}
        </div>
        <p className="mb-2 mt-2 flex flex-wrap items-center gap-x-2 text-[11px] leading-relaxed text-white/45">
          <span className="rounded-md border border-white/15 bg-white/[0.06] px-1.5 py-0.5 font-semibold text-brand-300">{P.sector}</span>
          <span>
            Sample of the panel every Achala program ships — <span className="font-semibold text-white/70">{P.delta}</span>.
          </span>
        </p>

        {/* KPI tiles — A-06 tooltips */}
        <div key={`kpi-${P.key}`} className="grid grid-cols-2 gap-2 sm:grid-cols-4">
          {P.kpis.map((k, i) => (
            <div
              key={k.label}
              className="group/tile relative rounded-lg border border-white/10 bg-white/[0.05] px-3 py-2.5"
              style={{ animation: `dash-in .45s ${i * 0.07}s both` }}
            >
              <p className="text-[9.5px] font-bold uppercase leading-tight tracking-[0.12em] text-white/40">
                {k.label}
                <HelpCircle className="ml-1 inline h-2.5 w-2.5 text-white/30 group-hover/tile:text-brand-300" aria-hidden="true" />
              </p>
              <p className="mt-0.5 font-display text-[16px] font-bold tabular-nums text-white">
                {k.value}
                <span
                  className={`ml-1.5 align-middle text-[10px] font-semibold ${
                    k.dir === "up" ? "text-brand-300" : k.dir === "down" ? "text-emerald-300" : "text-white/45"
                  }`}
                >
                  {k.delta}
                </span>
              </p>
              <span
                role="tooltip"
                className="pointer-events-none absolute inset-x-1 bottom-full z-10 mb-1 hidden rounded-md border border-white/15 bg-navy-900 px-2 py-1.5 text-[10px] leading-snug text-white/80 shadow-3 group-hover/tile:block"
              >
                {k.plain}
              </span>
              <span className="sr-only">{k.aria}</span>
            </div>
          ))}
        </div>

        {/* THE INTERACTIVE PROGRAM GRAPH — hover for crosshair + values */}
        <div className="mt-3 rounded-lg border border-white/10 bg-white/[0.04] p-3">
          <div className="flex items-center justify-between">
            <p className="text-[9.5px] font-bold uppercase tracking-[0.14em] text-white/40">{P.chartTitle}</p>
            <p className="text-[9.5px] text-white/35">vs signed baseline</p>
          </div>
          <div className="relative">
            {hoverI !== null && (
              <div
                className="pointer-events-none absolute top-0 z-10 -translate-x-1/2 whitespace-nowrap rounded-md border border-brand/50 bg-navy-900 px-2 py-1 text-[10px] font-semibold text-white shadow-3"
                style={{ left: `${Math.max(10, Math.min(90, tipX))}%` }}
                role="status"
              >
                {labelFor(hoverI)} · {Math.round(valAt(P.series, hoverI))}
                {P.chartUnit}
                <span className="ml-1.5 font-normal text-white/55">(baseline {Math.round(valAt(P.compare, hoverI))}{P.chartUnit})</span>
              </div>
            )}
            <svg
              viewBox={`0 0 ${W} ${H}`}
              className="mt-1.5 h-[96px] w-full cursor-crosshair"
              aria-label={`${P.chartTitle} — illustrative reference program`}
              onPointerMove={svgHover}
              onPointerLeave={() => setHoverI(null)}
            >
              <defs>
                <linearGradient id={`oc-fill-${P.key}`} x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#d20000" stopOpacity="0.30" />
                  <stop offset="100%" stopColor="#d20000" stopOpacity="0" />
                </linearGradient>
              </defs>
              {[28, 56, 84].map((y) => (
                <line key={y} x1={PAD} y1={y} x2={W - PAD} y2={y} stroke="rgba(255,255,255,0.07)" />
              ))}
              {/* baseline comparison */}
              <path d={pathFor(P.compare)} fill="none" stroke="rgba(255,255,255,0.28)" strokeWidth="1.2" strokeDasharray="4 3" />
              <path
                key={`cmp-${P.key}`}
                d={`${pathFor(P.compare)} L ${W - PAD},${H - PAD} L ${PAD},${H - PAD} Z`}
                fill="rgba(255,255,255,0.04)"
              />
              {/* program series — redraws on every program switch */}
              <path
                key={`area-${P.key}`}
                d={`${pathFor(P.series)} L ${W - PAD},${H - PAD} L ${PAD},${H - PAD} Z`}
                fill={`url(#oc-fill-${P.key})`}
                style={{ animation: "oc-fade .9s ease .25s both" }}
              />
              <path
                key={`line-${P.key}`}
                d={pathFor(P.series)}
                fill="none"
                stroke="#d20000"
                strokeWidth="2"
                strokeLinecap="round"
                pathLength={1}
                strokeDasharray={1}
                style={{ animation: "oc-draw 1.1s cubic-bezier(.4,0,.2,1) both" }}
              />
              {hoverI !== null && (
                <g pointerEvents="none">
                  <line
                    x1={PAD + hoverI * ((W - PAD * 2) / (P.series.length - 1))}
                    x2={PAD + hoverI * ((W - PAD * 2) / (P.series.length - 1))}
                    y1={PAD}
                    y2={H - PAD}
                    stroke="rgba(255,255,255,.4)"
                    strokeDasharray="3 3"
                  />
                  <circle
                    cx={PAD + hoverI * ((W - PAD * 2) / (P.series.length - 1))}
                    cy={H - PAD - (valAt(P.series, hoverI) / 100) * (H - PAD * 2)}
                    r="4.5"
                    fill="#fff"
                    stroke="#d20000"
                    strokeWidth="2.4"
                  />
                </g>
              )}
            </svg>
          </div>
          <p className="mt-1 text-[10px] leading-snug text-white/40">{P.note}</p>
        </div>

        {/* gate bars */}
        <div key={`gates-${P.key}`} className="mt-3 space-y-2">
          {P.gates.map((b, i) => (
            <div key={b.name} className="flex items-center gap-2.5">
              <span className="w-28 shrink-0 text-[10px] font-medium text-white/55">{b.name}</span>
              <span className="h-1.5 flex-1 overflow-hidden rounded-full bg-white/10">
                <span
                  className="block h-full rounded-full"
                  style={{
                    width: `${b.pct}%`,
                    background: i === 0 ? "rgba(255,255,255,0.35)" : "rgba(210,0,0,0.6)",
                    animation: `dash-bar .8s ${0.15 + i * 0.12}s both`,
                  }}
                />
              </span>
              <span className="w-9 shrink-0 text-right text-[10px] font-semibold tabular-nums text-brand-300">{b.pct}%</span>
            </div>
          ))}
        </div>

        {/* decision log */}
        <div className="mt-3 rounded-lg border border-white/10 bg-black/30 p-2.5 font-mono">
          <p className="font-sans text-[9.5px] font-bold uppercase tracking-[0.14em] text-white/40">Decision log</p>
          <div className="mt-1.5 space-y-1">
            {log.map((r, i) => (
              <p
                key={`${r.t}-${i}-${r.msg.slice(0, 8)}`}
                className="flex flex-wrap items-baseline gap-x-1.5 truncate text-[9.5px] leading-relaxed text-white/65"
                style={{ animation: i === 0 && tick > 0 ? "dash-in .4s both" : undefined, opacity: 1 - i * 0.22 }}
              >
                <span className="text-white/30">{r.t}</span>
                <span className="rounded bg-brand/15 px-1 py-0.5 text-[8px] font-bold uppercase tracking-wider text-brand-300">{r.tag}</span>
                <span className="truncate">{r.msg}</span>
              </p>
            ))}
          </div>
        </div>

        {/* E-05: provenance caption */}
        <p className="mt-2 text-[9.5px] leading-relaxed text-white/40">
          The proof is not a slide — it is this panel, generated from your estate from week two. Values shown are the
          illustrative reference program.
        </p>
      </div>
    </div>
  );
}

/* keep the old helper referenced for potential reuse */
void seriesOf;
