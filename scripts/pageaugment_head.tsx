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
          Each layer maps to a patented method family — the same map your auditors
          can walk from control to owner.
        </p>
        <div className="mt-5">
          <ArchitectureFlow title="Trust layers" caption="Patent-aligned design" layers={layers} />
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
