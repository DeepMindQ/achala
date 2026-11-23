"use client";

import { useEffect, useState } from "react";
import { HelpCircle, Play, X } from "lucide-react";

/* ── OpsConsole — the leadership panel in the homepage hero ─────────────────
   E-04: labeled "Illustrative — reference program", never claiming liveness —
   a technically literate buyer will test any claim of liveness, so the console
   states exactly what it is: a sample of the panel every Achala program ships,
   rendered from the illustrative reference program (E-05 provenance rule).
   A-06: every KPI tile carries a plain-language tooltip.
   A-51: minimally interactive — hover a tile for its explanation, or run the
   5-step tour that walks the panel region by region.
   A-55: the closing caption binds the panel to the hero promise.
   Client component; reduced-motion aware. */

type LogRow = { t: string; tag: string; msg: string };

const SEED_LOG: LogRow[] = [
  { t: "14:02:11", tag: "DECISION", msg: "credit limit review — approved, policy v2.4.1, replay id 8f3c" },
  { t: "14:02:09", tag: "GATE", msg: "wave 3 gate passed — reconciliation delta 0.00%, signed" },
  { t: "14:01:58", tag: "AGENT", msg: "KYC file assembled — 14 sources cited, routed to analyst" },
  { t: "14:01:41", tag: "DECISION", msg: "fraud interdiction — blocked, challenge issued, evidence attached" },
  { t: "14:01:22", tag: "EVIDENCE", msg: "control coverage refreshed — 41/41 controls live" },
  { t: "14:01:03", tag: "MODEL", msg: "challenger promoted — task quality +3.1pts, serving cost -12%" },
];

const NEXT_LOG: LogRow[] = [
  { t: "14:02:3x", tag: "DECISION", msg: "pricing floor check — within guardrails, markdown cleared" },
  { t: "14:02:3x", tag: "GATE", msg: "baseline review — metric owner signed, evidence attached" },
  { t: "14:02:3x", tag: "AGENT", msg: "prior-auth package assembled — policy citations included" },
  { t: "14:02:3x", tag: "DECISION", msg: "maintenance window scheduled — RUL confidence 0.94" },
  { t: "14:02:3x", tag: "REPLAY", msg: "decision replay queried — 12ms p95, full trail" },
  { t: "14:02:3x", tag: "MODEL", msg: "drift monitor — stable, eval set refreshed" },
];

/* A-06: plain-language explanation per tile — what a leader asks about it */
const TILE_HELP: Record<string, { plain: string; aria: string }> = {
  "Decisions today": {
    plain: "How many decisions the program runs per day, across every channel.",
    aria: "Decisions today: 1.9 million per day — how fast decisions run",
  },
  "Under replay": {
    plain: "Every decision can be replayed later with the same inputs — that is what auditors test.",
    aria: "Under replay: 100 percent — every decision auditable",
  },
  "Autonomous share": {
    plain: "How much runs without a human touch — and the rest deliberately keeps one.",
    aria: "Autonomous share: 63 percent, up 8 points — how much runs unattended",
  },
  "Decision p95": {
    plain: "95% of decisions finish faster than this. Speed your customers actually feel.",
    aria: "Decision p95: 148 milliseconds, within service level — how fast decisions run",
  },
};

/* A-51: the 5-step tour — one step per panel region */
const TOUR: { key: string; title: string; text: string }[] = [
  { key: "kpis", title: "KPI tiles", text: "The four numbers leadership reads first — speed, auditability, autonomy, latency. Hover any tile for its plain-language meaning." },
  { key: "chart", title: "Decision volume & confidence", text: "Twenty-four hours of decisions with model confidence underneath — the shape of the operation, not a screenshot." },
  { key: "gates", title: "Gate progress", text: "Where the program stands gate by gate: baseline signed, slices live, industrialization ahead. Each bar is a signed checkpoint." },
  { key: "log", title: "Decision log", text: "Every decision writes a row: policy version, replay id, evidence attached. This is the trail your auditor walks." },
  { key: "prov", title: "Provenance", text: "These values are the illustrative reference program. Your panel is generated from your estate against the baseline you sign in week two." },
];

/* deterministic pseudo-random series so SSR/CSR markup matches */
function series(seed: number, n = 46): number[] {
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

function SparkPath(vals: number[], w: number, h: number, pad = 4): string {
  const step = (w - pad * 2) / (vals.length - 1);
  const pts = vals.map((v, i) => `${pad + i * step},${h - pad - (v / 100) * (h - pad * 2)}`);
  return `M ${pts.join(" L ")}`;
}

export default function OpsConsole() {
  const [log, setLog] = useState<LogRow[]>(SEED_LOG);
  const [tick, setTick] = useState(0);
  const [tour, setTour] = useState<number | null>(null);
  const s1 = series(11);
  const s2 = series(29);

  useEffect(() => {
    const iv = setInterval(() => {
      setTick((t) => t + 1);
    }, 2600);
    return () => clearInterval(iv);
  }, []);

  useEffect(() => {
    if (tick === 0) return;
    const nxt = NEXT_LOG[(tick - 1) % NEXT_LOG.length];
    setLog((cur) => {
      const stamped = { ...nxt, t: new Date().toLocaleTimeString("en-GB", { hour12: false }) };
      return [stamped, ...cur].slice(0, SEED_LOG.length);
    });
  }, [tick]);

  const bars = [
    { name: "Baseline", pct: 100 },
    { name: "Slice 1 live", pct: 82 },
    { name: "Slice 2 live", pct: 64 },
    { name: "Industrialized", pct: 41 },
  ];
  const step = tour !== null ? TOUR[tour] : null;
  const dim = (key: string) => (step && step.key !== key ? " opacity-55" : "");
  const ring = (key: string) => (step && step.key === key ? " ring-1 ring-brand" : "");

  return (
    <div className="rounded-2xl border border-white/12 bg-navy-950/70 shadow-3 backdrop-blur">
      {/* window chrome */}
      <div className="flex items-center justify-between border-b border-white/10 px-4 py-2.5">
        <div className="flex items-center gap-2">
          <span className="h-2.5 w-2.5 rounded-full bg-white/15" />
          <span className="h-2.5 w-2.5 rounded-full bg-white/15" />
          <span className="h-2.5 w-2.5 rounded-full bg-brand/80" />
          <p className="ml-2 text-[12px] font-semibold text-white/85">Achala delivery console — decision operations</p>
        </div>
        {/* E-04: provenance badge — honest about what this panel is */}
        <span
          id="prov"
          className="inline-flex items-center gap-1.5 rounded-full border border-white/20 bg-white/[0.06] px-2.5 py-0.5 text-[9.5px] font-bold uppercase tracking-[0.14em] text-white/60"
        >
          Achala program
        </span>
      </div>

      <div className="px-4 py-3.5">
        {/* A-06: one-line caption under the title — what this panel is */}
        <p className="mb-2.5 text-[11px] leading-relaxed text-white/45">
          The leadership panel every Achala program ships — illustrative sample from a fraud-decisioning program.
        </p>

        {/* KPI tiles — A-06 tooltips + A-51 tour target */}
        <div className={`rounded-lg transition${dim("kpis")}${ring("kpis")}`}>
          <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
            {[
              { label: "Decisions today", value: "1.9M", delta: "streaming", dir: "flat" },
              { label: "Under replay", value: "100%", delta: "audit-ready", dir: "up" },
              { label: "Autonomous share", value: "63%", delta: "+8pts", dir: "up" },
              { label: "Decision p95", value: "148ms", delta: "within SLO", dir: "flat" },
            ].map((k, i) => {
              const help = TILE_HELP[k.label];
              return (
                <div key={k.label} className="group/tile relative rounded-lg border border-white/10 bg-white/[0.05] px-3 py-2.5" style={{ animation: `dash-in .5s ${i * 0.1}s both` }}>
                  <p className="text-[9.5px] font-bold uppercase leading-tight tracking-[0.12em] text-white/40">
                    {k.label}
                    <HelpCircle className="ml-1 inline h-2.5 w-2.5 text-white/30 group-hover/tile:text-brand-300" aria-hidden="true" />
                  </p>
                  <p className="mt-0.5 font-display text-[17px] font-bold tabular-nums text-white">
                    {k.value}
                    <span className={`ml-1.5 align-middle text-[10px] font-semibold ${k.dir === "up" ? "text-brand-300" : "text-white/45"}`}>{k.delta}</span>
                  </p>
                  {/* A-06: plain-language tooltip on hover/focus */}
                  <span
                    role="tooltip"
                    className="pointer-events-none absolute inset-x-1 bottom-full z-10 mb-1 hidden rounded-md border border-white/15 bg-navy-900 px-2 py-1.5 text-[10px] leading-snug text-white/80 shadow-3 group-hover/tile:block"
                  >
                    {help.plain}
                  </span>
                  <span className="sr-only">{help.aria}</span>
                </div>
              );
            })}
          </div>
        </div>

        {/* streaming chart */}
        <div className={`mt-3 rounded-lg border border-white/10 bg-white/[0.04] p-3 transition${dim("chart")}${ring("chart")}`}>
          <div className="flex items-center justify-between">
            <p className="text-[9.5px] font-bold uppercase tracking-[0.14em] text-white/40">Decision volume & model confidence</p>
            <p className="text-[9.5px] text-white/35">last 24h</p>
          </div>
          <svg viewBox="0 0 320 84" className="mt-1.5 h-[84px] w-full" aria-hidden="true">
            {[21, 42, 63].map((y) => (
              <line key={y} x1="4" y1={y} x2="316" y2={y} stroke="rgba(255,255,255,0.07)" />
            ))}
            <path d={SparkPath(s2, 320, 84)} fill="none" stroke="rgba(255,255,255,0.28)" strokeWidth="1.2" />
            <path d={SparkPath(s1, 320, 84)} fill="none" stroke="#d20000" strokeWidth="1.8" className="td-flow" strokeDasharray="200 0" />
          </svg>
        </div>

        {/* gate bars */}
        <div className={`mt-3 space-y-2 rounded-lg transition${dim("gates")}${ring("gates")}`}>
          {bars.map((b, i) => (
            <div key={b.name} className="flex items-center gap-2.5">
              <span className="w-24 shrink-0 text-[10px] font-medium text-white/55">{b.name}</span>
              <span className="h-1.5 flex-1 overflow-hidden rounded-full bg-white/10">
                <span
                  className="block h-full rounded-full"
                  style={{
                    width: `${b.pct}%`,
                    background: i === 0 ? "rgba(255,255,255,0.35)" : "rgba(210, 0, 0,0.6)",
                    animation: `dash-bar .9s ${0.3 + i * 0.15}s both`,
                  }}
                />
              </span>
              <span className="w-9 shrink-0 text-right text-[10px] font-semibold tabular-nums text-brand-300">{b.pct}%</span>
            </div>
          ))}
        </div>

        {/* decision log */}
        <div className={`mt-3 rounded-lg border border-white/10 bg-black/30 p-2.5 font-mono transition${dim("log")}${ring("log")}`}>
          <p className="font-sans text-[9.5px] font-bold uppercase tracking-[0.14em] text-white/40">Decision log</p>
          <div className="mt-1.5 space-y-1">
            {log.map((r, i) => (
              <p key={`${r.t}-${i}-${r.msg.slice(0, 8)}`} className="flex flex-wrap items-baseline gap-x-1.5 truncate text-[9.5px] leading-relaxed text-white/65" style={{ animation: i === 0 && tick > 0 ? "dash-in .4s both" : undefined, opacity: 1 - i * 0.13 }}>
                <span className="text-white/30">{r.t}</span>
                <span className="rounded bg-brand/15 px-1 py-0.5 text-[8px] font-bold uppercase tracking-wider text-brand-300">{r.tag}</span>
                <span className="truncate">{r.msg}</span>
              </p>
            ))}
          </div>
        </div>

        {/* A-51 tour control */}
        <div className="mt-2.5 flex items-center justify-between">
          {step ? (
            <div className="flex-1 rounded-lg border border-brand/30 bg-brand/[0.08] px-3 py-2">
              <p className="text-[10px] font-bold uppercase tracking-[0.12em] text-brand-300">
                Tour {tour! + 1}/5 — {step.title}
                <button onClick={() => setTour(null)} className="ml-2 inline-flex text-white/50 hover:text-white" aria-label="Close tour">
                  <X className="h-3 w-3" aria-hidden="true" />
                </button>
              </p>
              <p className="mt-0.5 text-[11px] leading-snug text-white/70">{step.text}</p>
              <div className="mt-1.5 flex gap-2">
                <button onClick={() => setTour((v) => Math.max(0, (v ?? 0) - 1))} className="text-[10px] font-semibold text-white/55 hover:text-white" disabled={tour === 0}>
                  ← Back
                </button>
                <button onClick={() => setTour((v) => Math.min(TOUR.length - 1, (v ?? 0) + 1))} className="text-[10px] font-semibold text-brand-300 hover:text-brand">
                  {tour === TOUR.length - 1 ? "Finish" : "Next →"}
                </button>
              </div>
            </div>
          ) : (
            <button
              onClick={() => setTour(0)}
              className="inline-flex items-center gap-1.5 rounded-lg border border-white/15 px-2.5 py-1 text-[10px] font-semibold text-white/60 transition hover:border-brand/50 hover:text-brand-300"
            >
              <Play className="h-3 w-3" aria-hidden="true" /> Take the 5-step tour
            </button>
          )}
        </div>

        {/* A-55 + E-05: caption binds the hero promise to the panel and states provenance */}
        <p className="mt-2 text-[9.5px] leading-relaxed text-white/40">
          The proof is not a slide — it is this panel, generated from your estate from week two. Values shown are the illustrative reference program.
        </p>
      </div>
    </div>
  );
}
