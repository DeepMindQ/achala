import { PageData } from "@/lib/content";
import { PATENTS, patentsForPage, Patent } from "@/lib/patents";
import Link from "next/link";
import { ShieldCheck } from "lucide-react";
/* Diagrams only: ArchitectureFlow + WorldPins live in DataVisuals. */
import { ArchitectureFlow, WorldPins } from "./DataVisuals";

/* ── PageAugment — factual augmentation only ────────────────────────────
   The old "output telemetry / program economics" panels were removed on
   purpose: they published invented planning figures with disclaimers, and
   invented numbers are not evidence. What stays is factual and useful —
   the reference-architecture diagrams (patent-aligned) and the patent
   strip. Baselines and outcomes belong to client estates, not brochures. */

export function OutputTelemetry({ page }: { page: PageData }) {
  const t = page.template;
  if (t === "platform_architecture") {
    const layers = PLATFORM_LAYERS[keyOf(page.url)] ?? PLATFORM_LAYERS.nexus;
    return (
      <section className="container-dq pt-2">
        <p className="text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">
          Reference architecture
        </p>
        <h2 className="mt-1 font-display text-[21px] font-semibold text-navy-800 sm:text-[23px]">
          How the platform is engineered, layer by layer
        </h2>
        <p className="mt-1.5 max-w-2xl text-[13px] text-slate-body/70">
          Each layer maps to a proprietary accelerator family — the same map your auditors
          can walk from control to owner.
        </p>
        <div className="mt-5">
          <ArchitectureFlow title="Trust layers" caption="Accelerator-aligned design" layers={layers} />
        </div>
      </section>
    );
  }
  if (t === "approach_page" || t === "company_page") {
    return (
      <section className="container-dq pt-2">
        <p className="text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">
          The Achala Method
        </p>
        <h2 className="mt-1 font-display text-[21px] font-semibold text-navy-800 sm:text-[23px]">
          Four gates, each with evidence that stops the program if it is missing
        </h2>
        <div className="mt-5">
          <ArchitectureFlow
            title="Gate structure"
            caption="Outcome-anchored"
            layers={[
              { name: "Diagnose — metric lock", nodes: ["Named metric", "Baseline audit", "Control owner"] },
              { name: "Design — risk budget", nodes: ["Risk envelope", "Control mapping", "Gate criteria"] },
              { name: "Prove — measured pilot", nodes: ["Bounded scope", "Evidence trail", "Gate review"] },
              { name: "Industrialize — scale", nodes: ["Runbooks", "Enablement", "Quarterly re-audit"] },
            ]}
          />
        </div>
      </section>
    );
  }
  return null;
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
          Accelerator underneath
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
                  {p.ref} — see the acceleration map
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
                <ShieldCheck className="h-3.5 w-3.5" aria-hidden="true" /> Accelerator family
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
              {[...p.platforms.map((x) => `/platforms/${x}/`), ...p.expertise.map((x) => `/services/${x}/`)].map((u) => (
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
    "United States": { x: 0.268, y: 0.375 },
    "Tysons Corner": { x: 0.268, y: 0.375 },
    "New York": { x: 0.26, y: 0.36 },
    "United Kingdom": { x: 0.46, y: 0.3 },
    London: { x: 0.46, y: 0.3 },
    India: { x: 0.69, y: 0.56 },
    Bengaluru: { x: 0.685, y: 0.575 },
    "Kingdom of Saudi Arabia": { x: 0.575, y: 0.455 },
    "Saudi Arabia": { x: 0.575, y: 0.455 },
    Riyadh: { x: 0.575, y: 0.455 },
    Dubai: { x: 0.585, y: 0.47 },
    Singapore: { x: 0.755, y: 0.6 },
  };
  const pins = offices
    .map((o) => {
      const city = o.city.split(",")[0].split("(")[0].split("—")[0].split(" — ")[0].trim();
      const c = coords[city];
      return c ? { id: city, ...c } : null;
    })
    .filter(Boolean) as { id: string; x: number; y: number }[];
  if (!pins.length) return null;
  return <WorldPins title="Four global delivery centers, one delivery standard" caption="Global delivery" pins={pins} />;
}
