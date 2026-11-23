import type { Metadata } from "next";
import Link from "next/link";
import { ArrowRight, ShieldCheck } from "lucide-react";
import Reveal from "@/components/site/Reveal";
import { PatentGrid } from "@/components/site/PageAugment";
import { CtaBand } from "@/components/site/PagePieces";
import { PATENTS } from "@/lib/patents";

export const metadata: Metadata = {
  title: "Patented Intelligence — the methods behind Achala IT Solutions delivery",
  description:
    "Eight patented method families — graph-native contextual intelligence, quantum-inspired optimization, federated trust, validated ethical decisions, generative workflow orchestration — power every Achala IT Solutions engagement.",
  alternates: { canonical: "/patented-intelligence/" },
};

export default function PatentedIntelligencePage() {
  return (
    <>
      <section className="relative overflow-hidden grad-navy-field text-white">
        <div className="bg-field-drift absolute inset-0 dot-grid" aria-hidden="true" />
        <div className="bg-glow-pulse absolute inset-0 grad-orange-glow" aria-hidden="true" />
        <div className="relative container-dq pb-14 pt-10 sm:pb-16 sm:pt-14">
          <nav aria-label="Breadcrumb" className="text-[12px] text-white/55">
            <ol className="flex items-center gap-1">
              <li>
                <Link href="/" className="hover:text-white/85">Home</Link>
              </li>
              <li aria-hidden="true">›</li>
              <li className="font-medium text-brand-300">Patented Intelligence</li>
            </ol>
          </nav>
          <div className="measure mt-6">
            <p className="kicker-bar-dark text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-300">
              Intellectual property foundation
            </p>
            <h1 className="text-display-2 mt-2 max-w-3xl text-white">
              Patented intelligence, hardened in production.
            </h1>
            <p className="mt-4 text-[15px] leading-relaxed text-white/70">
              {PATENTS.length} patent families filed by Strategemist Global Private Limited
              (Hyderabad) — the IP foundation of the Achala platform portfolio. Each method below is
              not slideware: it runs inside named platforms, under named controls, measured at every
              delivery gate.
            </p>
          </div>
          <div className="mt-7 flex flex-wrap gap-3">
            <Link
              href="/platforms/"
              className="btn-sheen inline-flex items-center gap-2 rounded-[10px] bg-brand px-5 py-2.5 text-[13px] font-semibold text-white transition hover:bg-brand-hover"
            >
              See the platforms <ArrowRight className="h-4 w-4" />
            </Link>
            <Link
              href="/book-a-briefing/"
              className="inline-flex items-center rounded-[10px] border border-white/25 px-5 py-2.5 text-[13px] font-medium text-white/85 transition hover:border-brand-300 hover:text-brand-300"
            >
              Book a technical briefing
            </Link>
          </div>
        </div>
      </section>

      <div className="py-12">
        <Reveal>
          <p className="mx-auto mb-10 max-w-3xl px-4 text-center text-[14px] leading-relaxed text-slate-body/75">
            Every family maps to platforms and service towers you can open directly — the chips under
            each card link to them. Capability summaries are engineering distillations of the patent
            specifications; claims language stays with the filings.
          </p>
        </Reveal>
        <PatentGrid />
        <div className="container-dq mt-10">
          <Reveal>
            <div className="flex items-start gap-2.5 rounded-xl border border-brand/30 bg-brand-tint px-4 py-3 text-[12.5px] leading-relaxed text-slate-body/90">
              <ShieldCheck className="mt-0.5 h-4 w-4 shrink-0 text-brand-deep" aria-hidden="true" />
              Patent families are filed in India under The Patents Act, 1970 by Strategemist
              Global Private Limited, Hyderabad (applicant of record), the IP foundation of the
              Achala IT Solutions delivery system. Full specifications are available to clients under NDA
              for technical due diligence.
            </div>
          </Reveal>
        </div>
        <div className="container-dq pb-6 pt-12">
          <CtaBand message="Bring your hardest decision problem — 45 minutes with the practice lead who owns the relevant patent-backed method." />
        </div>
      </div>
    </>
  );
}
