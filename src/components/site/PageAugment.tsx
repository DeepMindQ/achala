import { PageData } from "@/lib/content";
import { PATENTS, patentsForPage, Patent } from "@/lib/patents";
import { mulberry32, hashStr } from "@/lib/seeded";
import Link from "next/link";
import { ShieldCheck } from "lucide-react";
import {
  ArchitectureFlow,
  BarChart,
  Donut,
  Funnel,
  Gauge,
  Heatmap,
  LineArea,
  Radar,
  WorldPins,
} from "./DataVisuals";

/* ── PageAugment (Wave 2 + output-graphs directive) ─────────────────────
   Server-side, template-aware augmentation: every internal page receives a
   deterministic, page-seeded "output telemetry" panel (illustrative sample
   engagement data) plus the patents that power it. No per-page JSON edits. */

type Rng = () => number;

const TOWER_KPI: Record<string, { names: string[]; unit: string; trend: string; trendUnit: string }> = {
  "applied-ai-generative-ai": {
    names: ["Decision accuracy", "Time-to-answer", "Content ops cost", "Manual review hrs"],
    unit: "%",
    trend: "Assisted decisions per day",
    trendUnit: "",
  },
  "agentic-ai-hyperautomation": {
    names: ["Straight-through rate", "Cycle time", "Touches per case", "Backlog age"],
    unit: "%",
    trend: "Cases resolved autonomously / week",
    trendUnit: "",
  },
  "data-analytics-lakehouse": {
    names: ["Query latency p95", "Pipeline failures", "Freshness lag", "Cost per TB"],
    unit: "%",
    trend: "Governed queries served / day",
    trendUnit: "",
  },
  "cybersecurity-zero-trust": {
    names: ["MTTD", "MTTR", "Policy violations", "Open audit findings"],
    unit: "%",
    trend: "Threat signals correlated / hour",
    trendUnit: "",
  },
  "cloud-edge-platform-engineering": {
    names: ["Deploy frequency", "Change failure rate", "Cost per workload", "Incidents / mo"],
    unit: "%",
    trend: "Workloads orchestrated / day",
    trendUnit: "",
  },
  "quantum-advanced-compute": {
    names: ["Optimality gap", "Solve time", "Scenario coverage", "Energy per solve"],
    unit: "%",
    trend: "Scenarios explored / run",
    trendUnit: "",
  },
  "blockchain-digital-trust": {
    names: ["Reconciliation time", "Verification cost", "Dispute rate", "Provenance coverage"],
    unit: "%",
    trend: "Assets verified on-ledger / day",
    trendUnit: "",
  },
  "iot-digital-twin-robotics": {
    names: ["Unplanned downtime", "OEE uplift", "Defect escape rate", "Sensor coverage"],
    unit: "%",
    trend: "Twin sync events / minute",
    trendUnit: "",
  },
};

function towerOf(page: PageData): string {
  const seg = page.url.split("/").filter(Boolean);
  const towers = Object.keys(TOWER_KPI);
  for (const s of seg) if (towers.includes(s)) return s;
  return "applied-ai-generative-ai";
}

function baselineVsAfter(rng: Rng, names: string[]): { base: number[]; after: number[] } {
  // Improvement magnitudes per KPI: 22–58% better than baseline
  const base = names.map(() => Math.round(38 + rng() * 50));
  const after = base.map((b) => Math.max(6, Math.round(b * (1 - (0.22 + rng() * 0.36)))));
  return { base, after };
}

/* ── Output telemetry panel — per-template deterministic charts ───────── */
export function OutputTelemetry({ page }: { page: PageData }) {
  const rng = mulberry32(hashStr(page.id || page.url));
  const tower = towerOf(page);
  const kpi = TOWER_KPI[tower];
  const t = page.template;
  const dark = t === "case_study";
  const wrap = (children: React.ReactNode) => (
    <section className="container-dq pt-2">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <p className={`text-[12px] font-semibold uppercase tracking-[0.2em] ${dark ? "text-brand-300" : "text-brand-deep"}`}>
            What the output looks like
          </p>
          <h2 className={`mt-1 font-display text-[21px] font-semibold sm:text-[23px] ${dark ? "text-white" : "text-navy-800"}`}>
            Illustrative engagement telemetry
          </h2>
          <p className={`mt-1.5 max-w-2xl text-[13px] ${dark ? "text-white/60" : "text-slate-body/70"}`}>
            Sample delivery telemetry from comparable engagements — the baseline is locked in diagnosis,
            the delta is measured at every gate. Your numbers are set in the value assessment.
          </p>
        </div>
      </div>
      {children}
    </section>
  );

  if (t === "service_page" || t === "sub_capability" || t === "industry_capability") {
    const { base, after } = baselineVsAfter(rng, kpi.names);
    const weeks = Array.from({ length: 12 }, (_, i) => `W${i + 1}`);
    const trendStart = 300 + Math.round(rng() * 500);
    const trend = weeks.map((_, i) => Math.round(trendStart + i * (6 + rng() * 14)));
    return wrap(
      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        <BarChart
          title="Baseline vs. Achala delivery — 90-day gate review"
          caption="Measured delta"
          labels={kpi.names}
          series={[
            { name: "Baseline (diagnosis)", values: base },
            { name: "With Achala (day 90)", values: after, color: "#d20000" },
          ]}
          dark={dark}
        />
        <LineArea
          title={kpi.trend}
          caption="12-week ramp"
          labels={weeks}
          series={[{ name: kpi.trend, values: trend }]}
          dark={dark}
        />
      </div>,
    );
  }

  if (t === "tower_hub") {
    const { base, after } = baselineVsAfter(rng, kpi.names);
    return wrap(
      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        <BarChart
          title="Capability-level outcome range — tower engagements"
          caption="Median delta"
          labels={kpi.names}
          series={[
            { name: "Baseline", values: base },
            { name: "Post-delivery", values: after, color: "#d20000" },
          ]}
        />
        <Radar
          title="Operating maturity scorecard"
          caption="5-point scale ×20"
          axes={["Speed", "Precision", "Resilience", "Governance", "Scale"]}
          series={[
            { name: "Typical starting position", values: [38, 42, 35, 30, 45], color: "#568aa6" },
            { name: "After Achala engagement", values: [82, 78, 86, 90, 76], color: "#d20000" },
          ]}
        />
      </div>,
    );
  }

  if (t === "platform_overview") {
    return wrap(
      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        <Radar
          title="Platform capability scorecard"
          caption="Reference deployment"
          axes={["Throughput", "Precision", "Resilience", "Governance", "Time-to-value"]}
          series={[{ name: "Platform benchmark", values: [84, 80, 88, 92, 74], color: "#d20000" }]}
        />
        <LineArea
          title="Decision volume supported — first 12 weeks"
          caption="Ramp curve"
          labels={Array.from({ length: 12 }, (_, i) => `W${i + 1}`)}
          series={[{ name: "Decisions", values: weeksRamp(rng) }]}
        />
      </div>,
    );
  }

  if (t === "platform_architecture") {
    const layers = PLATFORM_LAYERS[keyOf(page.url)] ?? PLATFORM_LAYERS.nexus;
    return wrap(
      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        <ArchitectureFlow title="Reference architecture — trust layers" caption="Patent-aligned" layers={layers} />
        <Gauge title="Deterministic verification coverage" caption="Runtime assurance" value={92 + Math.round(rng() * 6)} unit="%" />
      </div>,
    );
  }

  if (t === "platform_usecases") {
    const inds = ["Banking", "Insurance", "Healthcare", "Manufacturing", "Retail", "Telecom", "Energy", "Logistics"];
    return wrap(
      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        <BarChart
          title="Median outcome delta by industry"
          caption="Sampled engagements"
          labels={inds}
          series={[{ name: "Improvement %", values: inds.map(() => 24 + Math.round(rng() * 34)) }]}
        />
        <Funnel
          title="Program adoption funnel"
          caption="Enterprise rollout"
          stages={[
            { name: "Value assessment", value: 120 },
            { name: "Pilot scoped", value: 64 },
            { name: "Production pilot", value: 38 },
            { name: "Scaled rollout", value: 26 },
            { name: "Enterprise standard", value: 18 },
          ]}
        />
      </div>,
    );
  }

  if (t === "case_study") {
    const { base, after } = baselineVsAfter(rng, kpi.names);
    return wrap(
      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        <BarChart
          title="Locked baseline vs. audited outcome"
          caption="Method under NDA"
          labels={kpi.names}
          dark
          series={[
            { name: "Baseline", values: base },
            { name: "Delivered", values: after, color: "#d20000" },
          ]}
        />
        <Donut
          title="Where the value landed"
          caption="Impact mix"
          dark
          center="100% verified"
          segments={[
            { name: "Cost released", value: 38 },
            { name: "Revenue protected", value: 27 },
            { name: "Risk reduced", value: 21 },
            { name: "Cycle-time recovered", value: 14 },
          ]}
        />
      </div>,
    );
  }

  if (t === "industry_hub" || t === "subindustry_page") {
    const regions = ["AMER", "EMEA", "APAC", "MEASA"];
    const quarters = ["Q1", "Q2", "Q3", "Q4"];
    const matrix = regions.map(() => quarters.map(() => 24 + Math.round(rng() * 52)));
    return wrap(
      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        <Heatmap
          title="Program impact index by region and quarter"
          caption="Illustrative"
          rows={regions}
          cols={quarters}
          matrix={matrix}
        />
        <LineArea
          title={`${page.l1 || "Industry"} decision velocity — 12 weeks`}
          caption="Ramp"
          labels={Array.from({ length: 12 }, (_, i) => `W${i + 1}`)}
          series={[{ name: "Decisions", values: weeksRamp(rng) }]}
        />
      </div>,
    );
  }

  if (t === "solution_page") {
    return wrap(
      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        <Funnel
          title="Decision pipeline — from signal to action"
          caption="Reference flow"
          stages={[
            { name: "Signals ingested", value: 4800 },
            { name: "Contextualized", value: 2400 },
            { name: "Decisions proposed", value: 960 },
            { name: "Human-approved", value: 640 },
            { name: "Automated execution", value: 520 },
          ]}
        />
        <BarChart
          title="Operational effect — before / after"
          caption="Measured delta"
          labels={kpi.names}
          series={[
            { name: "Baseline", values: baselineVsAfter(rng, kpi.names).base },
            { name: "With solution", values: baselineVsAfter(rng, kpi.names).after, color: "#d20000" },
          ]}
        />
      </div>,
    );
  }

  if (t === "insight_article") {
    return wrap(
      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        <LineArea
          title="Adoption curve the thesis tracks"
          caption="Composite signal"
          labels={Array.from({ length: 12 }, (_, i) => `W${i + 1}`)}
          series={[{ name: "Index", values: weeksRamp(rng) }]}
        />
        <Donut
          title="Where programs stall"
          caption="Field pattern"
          segments={[
            { name: "Data contracts", value: 34 },
            { name: "Decision ownership", value: 26 },
            { name: "Model operations", value: 22 },
            { name: "Change management", value: 18 },
          ]}
        />
      </div>,
    );
  }

  if (t === "approach_page" || t === "company_page") {
    return wrap(
      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        <ArchitectureFlow
          title="The Achala Method — gate structure"
          caption="Outcome-linked"
          layers={[
            { name: "Diagnose — metric lock", nodes: ["Named metric", "Baseline audit", "Control owner"] },
            { name: "Design — risk budget", nodes: ["Risk envelope", "Control mapping", "Gate criteria"] },
            { name: "Deliver — measured build", nodes: ["Sprint gates", "Evidence trail", "Deterministic checks"] },
            { name: "Scale — enterprise standard", nodes: ["Runbooks", "Enablement", "Quarterly re-audit"] },
          ]}
        />
        <Gauge title="Engagements passing every gate" caption="Program quality" value={94} unit="%" />
      </div>,
    );
  }

  return null;
}
function weeksRamp(rng: Rng): number[] {
  const start = 180 + Math.round(rng() * 400);
  return Array.from({ length: 12 }, (_, i) => Math.round(start + i * i * (1.4 + rng() * 1.8) + i * (4 + rng() * 10)));
}
function keyOf(url: string): string {
  const m = url.match(/platforms\/([a-z-]+)\//);
  return m ? m[1] : "nexus";
}

/* Patent-aligned reference architectures per platform (from the specs) */
export const PLATFORM_LAYERS: Record<string, { name: string; nodes: string[] }[]> = {
  nexus: [
    { name: "Ingestion & fusion", nodes: ["Multi-modal intake", "Normalization", "Context tensors"] },
    { name: "Graph intelligence core", nodes: ["Dynamic graphs", "Hypergraph tensors", "Spectral analysis"] },
    { name: "Decision hub", nodes: ["Contextual scoring", "Anomaly detection", "Deterministic streaming"] },
    { name: "Delivery & audit", nodes: ["APIs", "Dashboards", "Evidence trail"] },
  ],
  forge: [
    { name: "Workload intake", nodes: ["Task graphs", "Constraint capture", "Cost envelopes"] },
    { name: "Tensor decomposition", nodes: ["SVD / low-rank", "Manifold encoding", "Energy profiling"] },
    { name: "Quantum-walk optimizer", nodes: ["State exploration", "Amplitude amplification", "Route synthesis"] },
    { name: "Execution fabric", nodes: ["TPU / FPGA dispatch", "Grid-aware sync", "Verification"] },
  ],
  swarm: [
    { name: "Task graph synthesis", nodes: ["Dependency mapper", "Blueprint generator", "Temporal logic"] },
    { name: "Agent fleet", nodes: ["MARL policies", "Swarm clusters", "Shared rewards"] },
    { name: "Orchestration", nodes: ["Scheduler", "Conflict resolver", "Resource arbiter"] },
    { name: "Validated execution", nodes: ["zk-SNARK checks", "Blockchain log", "Rollback"] },
  ],
  sentinel: [
    { name: "Telemetry estate", nodes: ["Identity signals", "Network fabric", "Data posture"] },
    { name: "Encrypted computation", nodes: ["ZHNE homomorphic ops", "Secure aggregation", "Key governance"] },
    { name: "Consensus & trust", nodes: ["MABC protocol", "Byzantine isolation", "Compliance monitors"] },
    { name: "Resilient response", nodes: ["Self-healing ledger", "Workload redistribution", "Forensics"] },
  ],
  twinverse: [
    { name: "Sensor fabric", nodes: ["IoT streams", "Vision feeds", "Edge gateways"] },
    { name: "Multimodal perception", nodes: ["Quantum-enhanced NN", "Ensemble scoring", "Noise suppression"] },
    { name: "Twin synchronization", nodes: ["State estimator", "Curvature transforms", "What-if simulation"] },
    { name: "Actuation", nodes: ["Maintenance plans", "Autonomous control", "Operator HMI"] },
  ],
  quanta: [
    { name: "Problem encoding", nodes: ["Objective capture", "Constraint tensors", "Hilbert-space map"] },
    { name: "Spectral decomposition", nodes: ["Laplacian eigensets", "Band isolation", "Phase estimation"] },
    { name: "Quantum-inspired solver", nodes: ["Quantum walks", "Amplitude amplification", "Annealing"] },
    { name: "Verified result", nodes: ["Optimality bound", "Reproducibility check", "Explain report"] },
  ],
  ledger: [
    { name: "Event capture", nodes: ["Signed events", "Stream validation", "Schema contracts"] },
    { name: "Consensus ledger", nodes: ["DAG ordering", "Byzantine tolerance", "Immutable log"] },
    { name: "Provenance graph", nodes: ["Lineage links", "Attribution", "Retention policy"] },
    { name: "Trust delivery", nodes: ["Audit API", "Regulator views", "Disclosures"] },
  ],
  compass: [
    { name: "Signal lake", nodes: ["Temporal streams", "Spatial context", "Semantic layer"] },
    { name: "Adaptive learning loop", nodes: ["DRLF policies", "NAS refinement", "POMDP policies"] },
    { name: "Decision intelligence", nodes: ["Knowledge-graph DSS", "Explainability", "Fairness checks"] },
    { name: "Outcome tracking", nodes: ["Metric ledger", "Raft coherence", "Board reporting"] },
  ],
};

/* ── Patent strip — powers-this-page band ─────────────────────────────── */
export function PatentStrip({ page, dark }: { page: PageData; dark?: boolean }) {
  const patents = patentsForPage(page.url, page.title);
  if (!patents.length) return null;
  return (
    <section className="container-dq pt-6">
      <div className={`rounded-2xl border px-5 py-4 ${dark ? "border-white/10 bg-white/[0.05]" : "border-line bg-mist/60"}`}>
        <p className={`text-[11px] font-bold uppercase tracking-[0.18em] ${dark ? "text-brand-300" : "text-brand-deep"}`}>
          Patented method underneath
        </p>
        <div className="mt-3 grid gap-3 md:grid-cols-3">
          {patents.map((p) => (
            <div key={p.ref} className="flex items-start gap-2.5">
              <ShieldCheck className="mt-0.5 h-4 w-4 shrink-0 text-brand" aria-hidden="true" />
              <div>
                <p className={`text-[12.5px] font-semibold leading-snug ${dark ? "text-white" : "text-navy-800"}`}>{p.title}</p>
                <Link
                  href="/patented-intelligence/"
                  className={`text-[11px] font-medium hover:underline ${dark ? "text-brand-300" : "text-brand-deep"}`}
                >
                  {p.ref} — see the patent map
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ── Patented-intelligence full grid (used by /patented-intelligence/) ── */
export function PatentGrid() {
  return (
    <div className="container-dq pb-4">
      <div className="grid gap-4 md:grid-cols-2">
        {PATENTS.map((p: Patent, i) => (
          <article
            key={p.ref}
            className="group flex flex-col rounded-2xl border border-line bg-white p-6 shadow-1 transition hover:-translate-y-0.5 hover:border-brand/60 hover:shadow-2"
          >
            <div className="flex items-center justify-between gap-3">
              <span className="inline-flex items-center gap-1.5 rounded-full bg-brand-tint px-2.5 py-1 text-[10.5px] font-bold uppercase tracking-[0.12em] text-brand-deep">
                <ShieldCheck className="h-3.5 w-3.5" aria-hidden="true" /> Patented method
              </span>
              <span className="font-display text-[12px] font-bold text-brand-deep/60">{String(i + 1).padStart(2, "0")}</span>
            </div>
            <h2 className="mt-3 font-display text-[17px] font-semibold leading-snug text-navy-800 group-hover:text-brand-deep">
              {p.title}
            </h2>
            <p className="mt-2 text-[13px] leading-relaxed text-slate-body/80">{p.oneLiner}</p>
            <ul className="mt-3 space-y-1.5">
              {p.capabilities.slice(0, 4).map((c) => (
                <li key={c} className="flex items-start gap-2 text-[12.5px] leading-snug text-slate-body/85">
                  <span aria-hidden="true" className="mt-[7px] h-1.5 w-1.5 shrink-0 rounded-full bg-brand" />
                  {c}
                </li>
              ))}
            </ul>
            <div className="mt-4 flex flex-wrap gap-1.5 border-t border-line pt-3">
              <span className="text-[10.5px] font-semibold uppercase tracking-wider text-slate-body/50">Powers</span>
              {[...p.platforms.map((x) => `/platforms/${x}/`), ...p.towers.map((x) => `/services/${x}/`)].map((u) => (
                <Link
                  key={u}
                  href={u}
                  className="rounded-md border border-line bg-mist px-2 py-0.5 text-[11px] font-medium text-navy-800 transition hover:border-brand hover:text-brand-deep"
                >
                  {u.replace(/\//g, " ").trim()}
                </Link>
              ))}
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}

/* ── Offices world map (CHG-186) — consumed by global-offices via template */
export function OfficesMap({ offices }: { offices: { city: string }[] }) {
  const coords: Record<string, { x: number; y: number }> = {
    Hyderabad: { x: 0.69, y: 0.56 },
    Bengaluru: { x: 0.685, y: 0.575 },
    Dubai: { x: 0.585, y: 0.47 },
    Riyadh: { x: 0.575, y: 0.455 },
    "Tysons Corner": { x: 0.268, y: 0.375 },
    London: { x: 0.46, y: 0.3 },
    "New York": { x: 0.26, y: 0.36 },
    Singapore: { x: 0.755, y: 0.6 },
  };
  const pins = offices
    .map((o) => {
      const city = o.city.split(",")[0].split("(")[0].trim();
      const c = coords[city];
      return c ? { id: city, ...c } : null;
    })
    .filter(Boolean) as { id: string; x: number; y: number }[];
  if (!pins.length) return null;
  return <WorldPins title="Four global delivery centers, one delivery standard" caption="Global delivery" pins={pins} />;
}
