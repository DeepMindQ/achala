import Link from "next/link";
import { ArrowRight, BrainCircuit, Bot, Database, ShieldCheck, CloudCog, Atom, Blocks, Radar, Crosshair, UserCheck, Gauge as GaugeIcon, Wrench, Handshake, FileSignature, Scale } from "lucide-react";
import Reveal from "@/components/site/Reveal";
import { Marquee } from "@/components/site/Motion";
import { PATENTS } from "@/lib/patents";
import {
  SpotlightSlider,
  IndustryFinder,
  PlatformTabs,
  RotatingProof,
  SectionRail,
  DomainRouter,
  EvidenceGrid,
  HomeIndustryExplorer,
  type RouterOption,
  type EvidenceCard,
  type HomeExplorerIndustry,
} from "@/components/site/Wave3";
import { Accordion } from "@/components/site/ui-bits";
import NewsletterForm from "./NewsletterForm";
import { CtaBand, Quote, StatsStrip } from "@/components/site/PagePieces";
import { readPage, fileForUrl, pageIndex, type PageData } from "@/lib/content";
import OpsConsole from "@/components/site/OpsConsole";

/* ── A-01..A-58 homepage rebuild (Wave 1 of the change register) ────────── */

/* domain hub display names by slug — used for patent reinforces links (A-31) */
const HUB_BY_SLUG: Record<string, string> = {
  "data-analytics-lakehouse": "Data, Analytics & Lakehouse",
  "applied-ai-generative-ai": "Applied AI & Generative AI",
  "quantum-advanced-compute": "Quantum & Advanced Compute",
  "cloud-edge-platform-engineering": "Cloud, Edge & Platform Engineering",
  "cybersecurity-zero-trust": "Cybersecurity & Zero-Trust",
  "iot-digital-twin-robotics": "IoT, Digital Twin & Robotics",
  "agentic-ai-hyperautomation": "Agentic AI & Hyperautomation",
  "blockchain-digital-trust": "Blockchain & Digital Trust",
};

/* A-33: the regime each industry is held to — sourced from the industry hubs */
const INDUSTRY_REGIME: Record<string, string> = {
  "Banking & Financial Services": "DORA",
  "Insurance & Risk": "Solvency II",
  "Healthcare & Life Sciences": "HIPAA · GxP",
  "Manufacturing & Industrial": "IEC 62443",
  "Energy & Utilities": "NERC CIP",
  "Telecom, Media & Entertainment": "NIS2",
  "Retail & Consumer Goods": "PCI DSS",
  "Technology & SaaS": "SOC 2 · ISO 27001",
  "Logistics & Supply Chain": "C-TPAT",
  "Agriculture & Food Systems": "FSMA",
  "Public Sector & Government": "FedRAMP",
  "Education & Research": "GDPR",
};

/* A-41: the release-gate pair each engagement note was governed by —
   the site's own gate vocabulary, keyed by the delivering domain */
const GATE_BY_SERVICE: Record<string, string> = {
  "Data, Analytics & Lakehouse": "Replay parity · freshness SLA",
  "Agentic AI & Hyperautomation": "Policy envelope · human handoff",
  "Applied AI & Generative AI": "Eval harness · PoC kill-rate",
  "Cybersecurity & Zero-Trust": "Containment drill · evidence freshness",
  "Cloud, Edge & Platform Engineering": "Reconciliation delta · rollback plan",
  "IoT, Digital Twin & Robotics": "Twin fidelity · OTA safety",
  "Blockchain & Digital Trust": "Consensus parity · audit chain",
  "Quantum & Advanced Compute": "Benchmark honesty · baseline parity",
};

/* A-52: the three-question router — pain surface → domain + two practices */
const ROUTER_OPTIONS: RouterOption[] = [
  {
    key: "decisions",
    label: "Decisions",
    blurb: "Decisions too slow to defend, or too opaque to audit.",
    domain: { label: "Agentic AI & Hyperautomation", url: "/services/agentic-ai-hyperautomation/" },
    practices: [
      { label: "Decision Intelligence Systems", url: "/services/agentic-ai-hyperautomation/decision-intelligence-systems/" },
      { label: "Agentic Process Automation", url: "/services/agentic-ai-hyperautomation/agentic-process-automation/" },
    ],
  },
  {
    key: "data",
    label: "Data",
    blurb: "Data nobody trusts, disputes nobody resolves.",
    domain: { label: "Data, Analytics & Lakehouse", url: "/services/data-analytics-lakehouse/" },
    practices: [
      { label: "Real-Time Streaming & Event-Driven Decisioning", url: "/services/data-analytics-lakehouse/realtime-streaming-decisioning/" },
      { label: "Lakehouse Architecture & Migration", url: "/services/data-analytics-lakehouse/lakehouse-architecture/" },
    ],
  },
  {
    key: "risk",
    label: "Risk",
    blurb: "Risk you can sense but cannot evidence to a regulator.",
    domain: { label: "Cybersecurity & Zero-Trust", url: "/services/cybersecurity-zero-trust/" },
    practices: [
      { label: "Zero-Trust Architecture & Implementation", url: "/services/cybersecurity-zero-trust/zero-trust-architecture/" },
      { label: "AI Security & Model Protection", url: "/services/cybersecurity-zero-trust/ai-security-model-protection/" },
    ],
  },
  {
    key: "estate",
    label: "Estate",
    blurb: "An estate that will not move without breaking something.",
    domain: { label: "Cloud, Edge & Platform Engineering", url: "/services/cloud-edge-platform-engineering/" },
    practices: [
      { label: "Cloud-Native & Legacy Modernization", url: "/services/cloud-edge-platform-engineering/cloud-native-modernization/" },
      { label: "Hybrid & Multicloud Architecture", url: "/services/cloud-edge-platform-engineering/hybrid-multicloud-architecture/" },
    ],
  },
  {
    key: "operations",
    label: "Operations",
    blurb: "Capacity, cutover, ERP cores or a helpdesk that has to answer.",
    domain: { label: "Consulting & IT Services", url: "/consulting/" },
    practices: [
      { label: "IT Services & Managed Operations", url: "/consulting/it-services/" },
      { label: "ERP Services & Enterprise Core", url: "/consulting/erp-services/" },
    ],
  },
];

const PILLARS = [
  {
    icon: Crosshair,
    title: "A named business metric",
    desc: "Every engagement starts with the number you need to move — signed before delivery begins, reported every fortnight.",
  },
  {
    icon: UserCheck,
    title: "A named control owner",
    desc: "One accountable name on each control — not a committee. Regulators can walk the trail from gate to owner.",
  },
  {
    icon: GaugeIcon,
    title: "A named risk budget",
    desc: "The envelope of acceptable risk is fixed up front. Innovation inside it moves fast; nothing outside it ships.",
  },
];

const DOMAIN_ICONS = [Database, Bot, BrainCircuit, ShieldCheck, CloudCog, Radar, Blocks, Atom];

/* consulting groups — mirrored from the consulting data (4 groups × practices) */
const CONSULTING_GROUPS = [
  {
    name: "Data & Analytics",
    desc: "Migration factories, decision products, platform moves — the classic data estate under gate discipline.",
    services: [
      { name: "Data Analytics & Decision Products" }, { name: "Data Migration & Platform Moves" }, { name: "Digital Transformation Programs" },
    ],
  },
  {
    name: "Engineering & Quality",
    desc: "Pods that ship into your controls, and quality engineered in — not tested after.",
    services: [
      { name: "Software Development & Engineering Pods" }, { name: "Testing & Quality Engineering" }, { name: "Application Services & Modernization" }, { name: "UI/UX Design & Product Experience" },
    ],
  },
  {
    name: "Cloud & Operations",
    desc: "Azure estates end to end, and managed operations with SLAs you can audit.",
    services: [
      { name: "Cloud Development & Azure Services" }, { name: "IT Services & Managed Operations" }, { name: "IT Support & End-User Services" },
    ],
  },
  {
    name: "Advisory & Enterprise",
    desc: "ERP programs that land process and controls, capacity that scales, zero-trust advisory.",
    services: [
      { name: "IT Consulting & Managed Capacity" }, { name: "Cybersecurity Consulting & Zero-Trust" }, { name: "ERP Services & Enterprise Core" },
    ],
  },
];
const ConsultIcons = [Database, Wrench, CloudCog, Handshake];

/* the eight reporting panels of the steering pack — A-12/14/15/16:
   every card now carries a sample value + owner + cadence chip (A-14),
   anchored on values already published across the site. Sample row values
   are from the illustrative reference program (E-05 provenance rule). */
const STEERING_PANELS: { name: string; desc: string; sample: string; owner: string; cadence: string }[] = [
  { name: "Decision latency", desc: "How long the decision takes, end to end, against the baseline signed in week two.", sample: "p95 148 ms", owner: "COO", cadence: "fortnightly" },
  { name: "Autonomous coverage", desc: "Which decisions now run without a human touch — and which deliberately keep one.", sample: "63% · +8 pts", owner: "COO", cadence: "monthly" },
  { name: "Value attribution", desc: "Cost released, revenue protected, risk reduced — every figure lands on a ledger line the CFO already owns.", sample: "−38% fraud losses", owner: "CFO", cadence: "quarterly" },
  { name: "Gate-by-gate delta", desc: "The measured move at every delivery gate, with the evidence behind each figure.", sample: "0.00% reconciliation delta", owner: "Delivery lead", cadence: "per gate" },
  { name: "Year-one cost walk", desc: "Run cost before, during and after — so finance sees the same numbers delivery does.", sample: "−23.4% estate waste", owner: "CFO", cadence: "quarterly" },
  { name: "Control coverage", desc: "Controls live and tested versus the committed target, owned by a named person.", sample: "41/41 controls live", owner: "CISO", cadence: "monthly" },
  { name: "Maturity to outcome", desc: "Where the estate sits on the maturity curve and what the next gate requires.", sample: "5 of 6 gates passed", owner: "Program board", cadence: "per gate" },
  { name: "Owner map", desc: "Who is on the program, what they own, and how the team changes as value scales.", sample: "1 named owner per control", owner: "Sponsor", cadence: "signed week two" },
];

/* A-58: the objections a buyer raises before the final CTA */
const HOME_FAQ = [
  {
    q: "How fast can a POC become production?",
    a: "That is the arc we own end to end. A diagnostic sprint scopes the solution against your real data; the platform layer — EEMS, FMS, KYC, Tele Medicine, BI — arrives configured, not blank-page, so teams start near production readiness. Timelines depend on the estate, but the pattern is proven: hospital token systems, KYC flows and fleet platforms have gone from pilot to industrialized rollout with 24x7 operations behind them.",
  },
  {
    q: "What does AI-first mean in an engagement, practically?",
    a: "AI enters where it measurably helps: document analysis that cut loan processing from 3 days to 2 hours, queue prediction that slashed laboratory queues by 20-30%, telematics analytics that optimized workforce efficiency by up to 40%. Every model ships with its measured delta against your baseline — acceleration you can audit, not a claim.",
  },
  {
    q: "Who delivers the work?",
    a: "Practicing engineers led by the founders. 300+ people — including 200+ IT specialists — deliver from Hyderabad (HQ), Munich and Sofia, with the Achala Sulzer partnership giving European clients a fair-shoring continuity model. The team that scopes your POC is the team that industrializes it.",
  },
  {
    q: "How do you handle compliance for regulated industries?",
    a: "Automotive and healthcare clients operate under ISO/IEC 27001 and TISAX with GDPR-aligned delivery. Controls, access and data residency are engineered into the pod from day one — including 24x7 operations with audited SLAs — so audit season reads your evidence instead of reconstructing it.",
  },
];

export default function HomeView() {
  const page: PageData | null = fileForUrl("/") ? readPage(fileForUrl("/")!) : null;
  const brand = page?.extras;
  if (!page || !brand) {
    return <div className="container-dq py-20 text-navy-800">Content not generated yet.</div>;
  }

  /* case-library index counts — read once from the case-studies hub */
  const hubFile = fileForUrl("/case-studies/");
  const hubPage = hubFile ? readPage(hubFile) : null;
  const hubCards = (hubPage?.cards ?? []) as {
    title: string; url: string; industry: string; industry_url: string;
    desc: string; service?: string; service_url?: string; region?: string;
  }[];
  const CASE_COUNT = hubCards.length;
  const indSeen = new Map<string, string>();
  for (const c of hubCards) if (!indSeen.has(c.industry)) indSeen.set(c.industry, c.industry_url);
  const CASE_INDUSTRIES = [...indSeen.entries()].map(([name, url]) => ({
    name, url, count: hubCards.filter((c) => c.industry === name).length,
  }));
  const svcSeen = new Map<string, string>();
  for (const c of hubCards) if (c.service && !svcSeen.has(c.service)) svcSeen.set(c.service, c.service_url ?? "/services/");
  const CASE_SERVICES = [...svcSeen.keys()].map((name) => ({
    name, count: hubCards.filter((c) => c.service === name).length,
  }));

  /* practice index — counts + named practices per domain (A-20/22), insight read times (A-44) */
  const rows = pageIndex();
  const domainSlug = (name: string) => {
    for (const [slug, hubName] of Object.entries(HUB_BY_SLUG)) if (hubName === name) return slug;
    return "";
  };
  const practicesOf = (name: string) =>
    rows.filter((r) => r.template === "service_page" && r.l2 === name).map((r) => ({ label: r.title, url: r.url }));
  const domainCount = (name: string) => practicesOf(name).length;

  /* A-40: 12-card evidence grid — one flagship note per industry */
  const evidenceCards: EvidenceCard[] = [];
  const seenInd = new Set<string>();
  for (const c of hubCards) {
    if (seenInd.has(c.industry)) continue;
    seenInd.add(c.industry);
    evidenceCards.push({
      title: c.title, url: c.url, desc: c.desc, tag: c.industry,
      industry: c.industry, service: c.service, service_url: c.service_url,
      gate: c.service ? GATE_BY_SERVICE[c.service] : undefined,
    });
  }

  /* A-56: industry → top practices by published notes in that sector */
  const explorerIndustries: HomeExplorerIndustry[] = CASE_INDUSTRIES.map((ind) => {
    const cards = hubCards.filter((c) => c.industry === ind.name);
    const svcCount = new Map<string, number>();
    for (const c of cards) if (c.service) svcCount.set(c.service, (svcCount.get(c.service) ?? 0) + 1);
    const top = [...svcCount.entries()].sort((a, b) => b[1] - a[1]).slice(0, 3);
    const practices = top.map(([svc]) => {
      const hit = hubCards.find((c) => c.service === svc);
      return { label: svc, url: hit?.service_url ?? "/services/" };
    });
    return { name: ind.name, url: ind.url, regime: INDUSTRY_REGIME[ind.name] ?? "", notes: ind.count, practices };
  });

  /* A-44: read-time meta per insight card */
  const wordsByUrl = new Map(rows.map((r) => [r.url, r.words] as const));
  const insightMeta = (url: string) => {
    const w = wordsByUrl.get(url) ?? 0;
    return `${Math.max(2, Math.ceil(w / 200))} min read · practice desk`;
  };

  /* A-49/50 metadata lives in HOME_META + layout; home.json carries the same strings */

  const SECTION_NAV = [
    { id: "output", label: "Delivery output" },
    { id: "services", label: "Services" },
    { id: "consulting", label: "Consulting" },
    { id: "patents", label: "Accelerators" },
    { id: "platforms", label: "Platforms" },
    { id: "evidence", label: "Evidence" },
    { id: "value", label: "Charter" },
    { id: "industries", label: "Industries" },
    { id: "insights", label: "Insights" },
    { id: "faq", label: "FAQ" },
  ];

  const faqJsonLd = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: HOME_FAQ.map((f) => ({
      "@type": "Question",
      name: f.q,
      acceptedAnswer: { "@type": "Answer", text: f.a },
    })),
  };

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(faqJsonLd) }} />
      <SectionRail items={SECTION_NAV} />

      {/* split hero — buyer + proof in the first three seconds (A-01..A-05) */}
      <section id="top" className="relative overflow-hidden grad-navy-field text-white">
        <div className="bg-field-drift absolute inset-0 dot-grid" aria-hidden="true" />
        <div className="bg-glow-pulse absolute inset-0 grad-orange-glow" aria-hidden="true" />
        <div className="absolute inset-0 pattern-noise" aria-hidden="true" />
        <div className="relative container-dq grid gap-10 pb-14 pt-16 sm:pt-24 lg:grid-cols-[minmax(0,7fr)_minmax(0,5fr)] lg:items-center">
          <div>
            <Reveal className="hero-choreo">
              {/* A-02: category chips, TCS-boilerplate vocabulary — the descriptor lives here, not in the H1 */}
              <p className="rise-item text-[12px] font-semibold uppercase tracking-[0.22em] text-brand-300" style={{ ["--rise-delay" as string]: "40ms" }}>
                AI acceleration · platform-driven delivery · full-cycle engineering
              </p>
              {/* A-01: brand line, not a category sentence — Infosys/TCS pattern (aspiration up top, category below) */}
              <h1 className="text-display-1 mt-4 max-w-3xl text-white">
                <span className="line-mask block" style={{ ["--rise-delay" as string]: "120ms" }}>
                  <span className="line-mask-inner block">Intelligence, accelerated.</span>
                </span>
                <span className="line-mask block" style={{ ["--rise-delay" as string]: "260ms" }}>
                  <span className="line-mask-inner block">
                    Industries, <span className="grad-text">transformed</span>.
                  </span>
                </span>
              </h1>
              {/* A-03: one promise sentence + one proof sentence */}
              <p className="rise-item measure mt-5 text-body-lg leading-relaxed text-white/70" style={{ ["--rise-delay" as string]: "560ms" }}>
                Achala IT Solutions takes AI solutions from proof-of-concept to industrialized production — for Fortune
                500 enterprises, SMEs and startups across mobility, healthcare, manufacturing and financial services.
                Our own platforms do the heavy lifting from day one, and every engagement is measured on outcomes your
                board already tracks.
              </p>
              {/* A-03: the three delivery vignettes, as a rotating proof line */}
              <div className="rise-item" style={{ ["--rise-delay" as string]: "620ms" }}>
                <RotatingProof
                  lines={[
                    "50,000+ emergency cases a day — dispatched by one AI platform.",
                    "KYC verified in 5 minutes — not 30 days.",
                    "Loan processing cut from 3 days to 2 hours.",
                    "Laboratory queues reduced by 20-30% across hospital OPDs.",
                    "Workforce efficiency up 40% through telematics analytics.",
                  ]}
                />
              </div>
              {/* A-04: the ask, with what the buyer leaves with */}
              <div className="rise-item mt-8 flex flex-wrap items-center gap-3" style={{ ["--rise-delay" as string]: "680ms" }}>
                <Link
                  href="/book-a-briefing/"
                  className="btn-sheen inline-flex items-center gap-2 rounded-[10px] bg-brand px-6 py-3 text-[14px] font-semibold text-white transition hover:bg-brand-hover"
                >
                  Book a 45-minute briefing <ArrowRight className="h-4 w-4" />
                </Link>
                <Link
                  href="/services/"
                  className="inline-flex items-center rounded-[10px] border border-white/25 px-6 py-3 text-[14px] font-medium text-white/85 transition hover:border-brand-300 hover:text-brand-300"
                >
                  Explore what we do
                </Link>
              </div>
              <p className="rise-item mt-2 text-[12px] text-white/45" style={{ ["--rise-delay" as string]: "720ms" }}>
                45 minutes with a practice lead — leave with your acceleration path scoped.
              </p>
              {/* A-05: outcome proof instead of compliance badges, linking to the evidence */}
              <p className="rise-item mt-6 flex flex-wrap items-center gap-x-4 gap-y-2 text-[12.5px] text-white/65" style={{ ["--rise-delay" as string]: "780ms" }}>
                <Link href="#evidence" className="inline-flex flex-wrap items-center gap-x-2 gap-y-1 hover:text-brand-300">
                  <ShieldCheck className="h-3.5 w-3.5 text-brand-300" aria-hidden="true" />
                  <span className="font-semibold text-white/80">KYC 60% faster · lab queues −20-30% · loans 3 days → 2 hours</span>
                  <span className="text-white/45">— see the engagements</span>
                </Link>
                <span className="rounded-full border border-white/15 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider text-white/45">
                  Published engagement deltas
                </span>
              </p>
            </Reveal>
          </div>
          {/* the operations console — what a program reports (A-06/51/55 in OpsConsole) */}
          <div className="hidden lg:block">
            <Reveal delay={400}>
              <OpsConsole />
            </Reveal>
          </div>
        </div>
        {/* A-07: the stat strip renders ONCE · A-08/09/10/11 reconciled content · E-05 provenance note */}
        <div className="relative container-dq pb-12">
          <StatsStrip stats={brand.stats} />
          <p className="mt-2 text-right text-[10.5px] text-white/35">
            Company metrics are delivery-to-date · platform metrics are published client outcomes.
          </p>
        </div>
      </section>

      {/* credentials + platform marquee */}
      <div className="border-b border-line bg-navy-900/95">
        <Marquee
          dark
          className="marquee-dark container-dq"
          items={[
            "ISO/IEC 27001", "TISAX", "GDPR-aligned delivery", "NASSCOM AI Game Changers 2021",
            "EEMS Platform", "Fleet Management System", "KYC Management System", "Tele Medicine Platform", "BI & Analytics Platform", "Token Management System", "Patient Priority Portal", "Driisti Smart Vision Glasses",
            "POC to industrialization", "AI-first · platform-driven", "Global delivery — India · Germany · Bulgaria", "Sulzer GmbH partnership", "24x7 operations",
          ]}
        />
      </div>

      {/* steering pack — what delivery produces (A-12/13/14) */}
      <section id="output" className="vignette-section relative scroll-mt-24 overflow-hidden grad-navy-field text-white">
        <div className="orb-field" aria-hidden="true">
          <span className="orb" />
          <span className="orb" />
        </div>
        <div className="bg-field-drift absolute inset-0 dot-grid" aria-hidden="true" />
        <div className="absolute inset-0 pattern-noise" aria-hidden="true" />
        <div className="relative container-dq section-y-sm">
          <Reveal>
            <p className="kicker-bar-dark text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-300">What delivery produces</p>
            {/* A-12 */}
            <h2 className="text-display-3 mt-1 max-w-4xl text-white sm:text-[28px]">
              The numbers your leadership signs off — refreshed every fortnight, against the baseline you signed
            </h2>
            {/* A-13: the intro carries a sample panel row, labeled illustrative */}
            <p className="mt-2 max-w-4xl text-[14.5px] leading-relaxed text-white/65">
              One panel per program surface — consulting or deep-tech, generated from your estate, so week two
              already reads like your business. A sample row, illustrative reference program:{" "}
              <span className="rounded-md border border-white/20 bg-white/[0.07] px-2 py-0.5 font-mono text-[11.5px] text-white/85">
                Decision p95 148 ms · owner: COO · refreshed 14 days · evidence: replay pack
              </span>
            </p>
          </Reveal>
          <div className="mt-8 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {STEERING_PANELS.map((p, i) => (
              <Reveal key={p.name} delay={i * 40}>
                {/* A-14: every card carries sample value + owner + cadence */}
                <div className="flex h-full flex-col rounded-xl border border-white/10 bg-white/[0.04] p-5 backdrop-blur transition hover:border-brand/40 hover:bg-white/[0.07]">
                  <p className="flex items-center justify-between font-display text-[11px] font-bold text-brand-300/90">
                    {String(i + 1).padStart(2, "0")}
                    <span className="rounded-full border border-white/15 px-2 py-0.5 text-[9px] font-bold uppercase tracking-wider text-white/50">
                      {p.cadence}
                    </span>
                  </p>
                  <p className="mt-2 text-[14.5px] font-semibold text-white">{p.name}</p>
                  <p className="mt-1 flex-1 text-[12.5px] leading-relaxed text-white/55">{p.desc}</p>
                  <p className="mt-3 rounded-md bg-navy-800/80 px-2 py-1.5 text-[11.5px] font-semibold text-white/90">
                    <span className="font-display">{p.sample}</span>
                    <span className="ml-1.5 text-[10px] font-medium text-white/45">owner: {p.owner}</span>
                  </p>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* the expertise domains (A-17..A-22 + A-52 router) */}
      <section id="services" className="scroll-mt-24 border-y border-line bg-mist/60 dot-grid-light">
        <div className="container-dq section-y-sm">
          <Reveal>
            <div className="flex flex-wrap items-end justify-between gap-4">
              <div>
                <p className="kicker-bar text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">
                  Services &amp; consulting
                </p>
                {/* A-17 */}
                <h2 className="text-display-3 mt-1 max-w-4xl text-navy-800 sm:text-[30px]">
                  The expertise your next move needs — under one accountable delivery system
                </h2>
                {/* A-18 */}
                <p className="mt-2 max-w-2xl text-[14.5px] text-slate-body/75">
                  Decision, action, data, trust, platform, compute, records, field — one of these seams is where your
                  P&amp;L leaks today, and deep-tech programs enter through a domain. Classic-estate work — migration,
                  engineering pods, Azure, ERP, managed operations — enters through consulting. Both tracks run the same
                  release gates on the same production platforms.
                </p>
              </div>
              <div className="flex flex-col items-start gap-1.5">
                <Link
                  href="/services/"
                  className="link-animated inline-flex items-center gap-1.5 text-[13.5px] font-semibold text-brand-deep"
                >
                  All services <ArrowRight className="h-4 w-4" />
                </Link>
                <Link
                  href="/consulting/"
                  className="link-animated inline-flex items-center gap-1.5 text-[13.5px] font-semibold text-brand-deep"
                >
                  All consulting practices <ArrowRight className="h-4 w-4" />
                </Link>
              </div>
            </div>
          </Reveal>
          <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {brand.domains.map((t, i) => {
              const Icon = DOMAIN_ICONS[i % DOMAIN_ICONS.length];
              const practices = practicesOf(t.name).slice(0, 3);
              return (
                <Reveal key={t.url} delay={i * 40}>
                  <Link
                    href={t.url}
                    className="tilt-card group flex h-full flex-col rounded-2xl border border-line bg-white p-5 transition hover:-translate-y-0.5 hover:border-brand/60 shadow-1 hover:shadow-2"
                  >
                    <span className="flex items-center justify-between">
                      <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-navy-800 text-brand-300 transition group-hover:bg-brand group-hover:text-white">
                        <Icon className="h-5 w-5" aria-hidden="true" />
                      </span>
                      {/* A-21: entry-intent tag on the two most-entered domains */}
                      {t.start && (
                        <span className="rounded-full bg-brand-tint px-2.5 py-0.5 text-[10px] font-bold uppercase tracking-wider text-brand-deep">
                          Start here
                        </span>
                      )}
                    </span>
                    <p className="mt-3 font-display text-[15.5px] font-semibold leading-snug text-navy-800 group-hover:text-brand-deep">
                      {t.name}
                    </p>
                    <p className="mt-2 flex-1 text-[12.5px] leading-relaxed text-slate-body/75">{t.desc}</p>
                    {/* A-19: the managed-on metric + flagship outcome */}
                    {t.metric && (
                      <p className="mt-2.5 rounded-md bg-navy-800 px-2.5 py-1.5 font-display text-[11.5px] font-semibold text-white">
                        {t.metric}
                      </p>
                    )}
                    {/* A-22: three named practices per card */}
                    <span className="mt-2.5 flex flex-wrap gap-1.5">
                      {practices.map((p) => (
                        <span key={p.url} className="rounded-full border border-line bg-mist/70 px-2 py-0.5 text-[11px] font-medium text-navy-800/85">
                          {p.label}
                        </span>
                      ))}
                    </span>
                    {/* A-39: the platform pairing */}
                    {t.plat && (
                      <span className="mt-2 text-[11px] font-medium text-slate-body/55">
                        Pairs with {t.plat}
                      </span>
                    )}
                    {/* A-20: count CTA */}
                    <span className="mt-3 inline-flex items-center gap-1 text-[12px] font-semibold text-brand-deep">
                      Explore practices <ArrowRight className="h-3.5 w-3.5 transition group-hover:translate-x-0.5" />
                    </span>
                  </Link>
                </Reveal>
              );
            })}
          </div>
          {/* A-52: the self-qualification router */}
          <DomainRouter options={ROUTER_OPTIONS} />
        </div>
      </section>

      {/* consulting practices (A-23..A-27) — co-equal offer track, repositioned after services */}
      <section id="consulting" className="scroll-mt-24 border-y border-line bg-white">
        <div className="container-dq section-y-sm">
          <Reveal>
            <div className="flex flex-wrap items-end justify-between gap-4">
              <div>
                <p className="kicker-bar text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">
                  Consulting &amp; IT services
                </p>
                {/* A-23 */}
                <h2 className="text-display-3 mt-1 text-navy-800 sm:text-[28px]">
                  Consulting that ends in delivery — the advisor is the builder
                </h2>
                {/* A-24 */}
                <p className="mt-2 max-w-2xl text-[14.5px] text-slate-body/75">
                  Transformation programs, migration factories, engineering pods, quality engineering, Azure estates,
                  ERP cores, managed operations and end-user support. The team that recommends is the team that builds
                  it — the same two-week diagnostic, signed baseline and evidence-or-stop contract as every expertise
                  domain.
                </p>
              </div>
              <Link
                href="/consulting/"
                className="link-animated inline-flex items-center gap-1.5 text-[13.5px] font-semibold text-brand-deep"
              >
                All consulting practices <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </Reveal>
          <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {CONSULTING_GROUPS.slice(0, 4).map((g, i) => (
              <Reveal key={g.name} delay={i * 40}>
                <Link
                  href="/consulting/"
                  className="tilt-card group flex h-full flex-col rounded-2xl border border-line bg-mist/60 p-5 transition hover:-translate-y-0.5 hover:border-brand/60 hover:bg-white shadow-1 hover:shadow-2"
                >
                  <span className="flex items-center justify-between">
                    <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-navy-800 text-brand-300 transition group-hover:bg-brand group-hover:text-white">
                      {(() => { const Ic = ConsultIcons[i % ConsultIcons.length]; return <Ic className="h-5 w-5" aria-hidden="true" />; })()}
                    </span>
                    <ArrowRight className="h-4 w-4 text-brand-deep/40 transition group-hover:translate-x-0.5 group-hover:text-brand-deep" aria-hidden="true" />
                  </span>
                  <p className="mt-3 font-display text-[15.5px] font-semibold leading-snug text-navy-800 group-hover:text-brand-deep">
                    {g.name}
                  </p>
                  {/* A-25: a real description, not a name list */}
                  <p className="mt-2 flex-1 text-[12.5px] leading-relaxed text-slate-body/75">{g.desc}</p>
                  {/* A-26: CTA names the action, not the count */}
                  <span className="mt-3 inline-flex items-center gap-1 text-[12px] font-semibold text-brand-deep">
                    Explore the practices <ArrowRight className="h-3.5 w-3.5 transition group-hover:translate-x-0.5" />
                  </span>
                </Link>
              </Reveal>
            ))}
          </div>
          {/* A-27: the bridge between the two taxonomies */}
          <Reveal>
            <p className="mt-6 flex flex-wrap items-center gap-1.5 text-[13px] text-slate-body/70">
              <Scale className="h-4 w-4 shrink-0 text-brand-deep" aria-hidden="true" />
              <span className="font-semibold text-navy-800">Where consulting meets expertise:</span>
              <span>platform moves land in</span>
              <Link href="/services/cloud-edge-platform-engineering/" className="link-animated font-semibold text-brand-deep">
                Cloud, Edge &amp; Platform Engineering
              </Link>
              <span>· decision products in</span>
              <Link href="/services/data-analytics-lakehouse/" className="link-animated font-semibold text-brand-deep">
                Data, Analytics &amp; Lakehouse
              </Link>
              <span>· zero-trust advisory in</span>
              <Link href="/services/cybersecurity-zero-trust/" className="link-animated font-semibold text-brand-deep">
                Cybersecurity &amp; Zero-Trust
              </Link>
            </p>
          </Reveal>
        </div>
      </section>

      {/* patented intelligence (A-28..A-32) */}
      <section id="patents" className="scroll-mt-24 container-dq section-y-sm">
        <Reveal>
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <p className="kicker-bar text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">
                The acceleration differential
              </p>
              <h2 className="text-display-3 mt-1 text-navy-800 sm:text-[28px]">
                AI accelerators — proven in production before they reach your program
              </h2>
              {/* A-32: the platforms named · A-28: the four-of-eight affordance */}
              <p className="mt-2 max-w-2xl text-[14.5px] text-slate-body/75">
                Ambition is common in this industry; production is not. Every engagement starts from configured
                platforms, not a blank page and a staffing plan: AI-led dispatch and fleet readiness, document
                intelligence for onboarding, queue prediction for hospital operations, connected-device engineering and
                data platforms — hardened in production with clients like KIMS, AIG and European automotive groups.{" "}
                <Link href="/patented-intelligence/" className="link-animated font-semibold text-brand-deep">
                  A few of the accelerator families are shown here — the acceleration map lists them all.
                </Link>
              </p>
            </div>
            <Link
              href="/patented-intelligence/"
              className="link-animated inline-flex items-center gap-1.5 text-[13.5px] font-semibold text-brand-deep"
            >
              The method map <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </Reveal>
        {/* the three IP strategies — how the differential lands commercially */}
        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {[
            {
              t: "Start from configured IP",
              d: "Method families arrive pre-configured inside our platforms — controls, evidence generation and delivery patterns already standardized. Budget goes to the 20% that is genuinely yours.",
            },
            {
              t: "Fewer hours to the same outcome",
              d: "With the heavy lifting in licensed IP, teams start near 80% readiness. The gates then prove the delta against your signed baseline — speed you can audit, not a claim.",
            },
            {
              t: "IP models that fit the deal",
              d: "License, embed or co-develop: accelerators built specifically for you can carry co-ownership terms, so the IP advantage compounds on your side of the table too.",
            },
          ].map((s) => (
            <Reveal key={s.t}>
              <div className="h-full rounded-2xl border border-brand/25 bg-brand-tint/40 p-5">
                <p className="font-display text-[15px] font-semibold text-navy-800">{s.t}</p>
                <p className="mt-2 text-[12.5px] leading-relaxed text-slate-body/75">{s.d}</p>
              </div>
            </Reveal>
          ))}
        </div>
        <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {PATENTS.slice(0, 4).map((p, i) => (
            <Reveal key={p.ref} delay={i * 50}>
              <Link
                href="/patented-intelligence/"
                className="tilt-card group flex h-full flex-col rounded-2xl border border-line bg-white p-5 transition hover:-translate-y-0.5 hover:border-brand/60 shadow-1 hover:shadow-2"
              >
                <span className="w-fit rounded-full bg-brand-tint px-2.5 py-0.5 text-[10.5px] font-bold uppercase tracking-wider text-brand-deep">
                  {p.ref}
                </span>
                <p className="mt-3 font-display text-[14.5px] font-semibold leading-snug text-navy-800 group-hover:text-brand-deep">
                  {p.title}
                </p>
                <p className="mt-2 flex-1 text-[12.5px] leading-relaxed text-slate-body/75">{p.oneLiner}</p>
                {/* A-29: the outcome line — what the method buys you */}
                <p className="mt-2.5 rounded-lg bg-brand-tint/60 px-3 py-2 text-[12px] font-medium leading-snug text-brand-deep">
                  {p.outcome}
                </p>
                {/* A-31: the service pages the family reinforces */}
                <span className="mt-2.5 flex flex-wrap gap-1.5">
                  {p.expertise.slice(0, 2).map((slug) => (
                    <span key={slug} className="rounded-full border border-line bg-mist/70 px-2 py-0.5 text-[10.5px] font-medium text-navy-800/80">
                      reinforces: {HUB_BY_SLUG[slug] ?? slug}
                    </span>
                  ))}
                </span>
                {/* A-30: CTA names the family */}
                <span className="mt-3 inline-flex items-center gap-1 text-[12px] font-semibold text-brand-deep">
                  Read {p.ref} <ArrowRight className="h-3.5 w-3.5 transition group-hover:translate-x-0.5" />
                </span>
              </Link>
            </Reveal>
          ))}
        </div>
      </section>

      {/* platforms (A-37/38/39 in PlatformTabs) */}
      <section id="platforms" className="scroll-mt-24 container-dq section-y-sm">
        <Reveal>
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <p className="kicker-bar text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">
                Platforms
              </p>
              <h2 className="text-display-3 mt-1 text-navy-800 sm:text-[28px]">
                The platforms that put the AI accelerators to work
              </h2>
              {/* A-37: the role line under the row */}
              <p className="mt-2 max-w-2xl text-[14.5px] text-slate-body/75">
                EEMS runs emergency response · FMS keeps fleets ready · KYC onboards customers in minutes ·
                Tele Medicine extends care · BI turns operations into decisions · Token Management clears queues ·
                Patient Priority Portal personalizes care · Driisti restores sight.
              </p>
            </div>
            <Link
              href="/platforms/"
              className="link-animated inline-flex items-center gap-1.5 text-[13.5px] font-semibold text-brand-deep"
            >
              Platform portfolio <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </Reveal>
        <div className="mt-8">
          <PlatformTabs platforms={brand.platforms} />
        </div>
      </section>

      {/* evidence library (A-40..A-43, A-53) — proof, after the two offer tracks */}
      <section id="evidence" className="scroll-mt-24 relative overflow-hidden border-y border-line grad-navy-field text-white">
        <div className="bg-field-drift absolute inset-0 dot-grid" aria-hidden="true" />
        <div className="container-dq section-y-sm">
          <Reveal>
            <div className="flex flex-wrap items-end justify-between gap-4">
              <div>
                <p className="kicker-bar-dark text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-300">
                  Evidence library
                </p>
                <h2 className="text-display-3 mt-1 text-white sm:text-[28px]">
                  The numbers are the client&rsquo;s. The method is on the page.
                </h2>
                {/* A-08: reconciled count language */}
                <p className="mt-2 max-w-2xl text-[14.5px] text-white/65">
                  A track record you can audit: every published engagement note carries the measured delta, the system
                  that produced it and the gates that governed the build.
                </p>
              </div>
              <Link
                href="/case-studies/"
                className="link-animated inline-flex items-center gap-1.5 text-[13.5px] font-semibold text-brand-300"
              >
                Browse the full index <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </Reveal>
          {/* A-40/41/43: filterable grid with gates + delivering practice */}
          <EvidenceGrid cards={evidenceCards} industries={CASE_INDUSTRIES} />
          <Reveal>
            <div className="mt-8">
              <SpotlightSlider slides={brand.cases} />
            </div>
            {/* A-42: the lists carry their real name */}
            <div className="mt-9 grid gap-5 lg:grid-cols-[minmax(0,3fr)_minmax(0,2fr)]">
              <div>
                <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-white/45">Published engagement notes — by industry</p>
                <div className="mt-2.5 flex flex-wrap gap-2">
                  {CASE_INDUSTRIES.map((ind) => (
                    <Link
                      key={ind.name}
                      href="/case-studies/#by-industry"
                      className="rounded-full border border-white/15 bg-white/[0.05] px-3.5 py-1.5 text-[12.5px] font-medium text-white/75 transition hover:border-brand-300 hover:text-brand-300"
                    >
                      {ind.name} <span className="text-white/40">{ind.count}</span>
                    </Link>
                  ))}
                </div>
              </div>
              <div>
                <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-white/45">Published engagement notes — by service area</p>
                <div className="mt-2.5 flex flex-wrap gap-2">
                  {CASE_SERVICES.map((svc) => (
                    <Link
                      key={svc.name}
                      href="/case-studies/#by-service"
                      className="rounded-full border border-white/15 bg-white/[0.05] px-3.5 py-1.5 text-[12.5px] font-medium text-white/75 transition hover:border-brand-300 hover:text-brand-300"
                    >
                      {svc.name} <span className="text-white/40">{svc.count}</span>
                    </Link>
                  ))}
                </div>
              </div>
            </div>
          </Reveal>
        </div>
      </section>

      {/* the engagement charter — with a redacted artifact (A-35/36) */}
      <section id="value" className="scroll-mt-24 border-y border-line bg-mist/60 dot-grid-light">
        <div className="container-dq section-y-sm">
          <Reveal>
            <p className="kicker-bar text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">The operating discipline</p>
            <h2 className="text-display-3 mt-1 max-w-3xl text-navy-800 sm:text-[28px]">
              The names signed before delivery begins — the engagement charter
            </h2>
          </Reveal>
          <div className="mt-8 grid gap-4 lg:grid-cols-[minmax(0,3fr)_minmax(0,2fr)]">
            <div className="grid gap-4 md:grid-cols-3">
              {PILLARS.map((p, i) => (
                <Reveal key={p.title} delay={i * 70}>
                  <div className="h-full rounded-2xl border border-line bg-white p-6 shadow-1 transition hover:-translate-y-0.5 hover:border-brand/60 hover:shadow-2">
                    <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-navy-800 text-brand-300">
                      <p.icon className="h-5 w-5" aria-hidden="true" />
                    </span>
                    <p className="mt-4 font-display text-[16px] font-semibold text-navy-800">{p.title}</p>
                    <p className="mt-2 text-[13px] leading-relaxed text-slate-body/75">{p.desc}</p>
                  </div>
                </Reveal>
              ))}
            </div>
            {/* A-35: the charter you sign, three fields filled */}
            <Reveal delay={120}>
              <div className="flex h-full flex-col rounded-2xl border border-line bg-white p-6 shadow-2">
                <p className="flex items-center gap-2 text-[11px] font-bold uppercase tracking-[0.14em] text-brand-deep">
                  <FileSignature className="h-4 w-4" aria-hidden="true" /> Program charter — one page
                </p>
                <div className="mt-3 space-y-2.5 text-[12.5px] leading-relaxed">
                  <p className="rounded-lg border border-line bg-mist/60 px-3 py-2">
                    <span className="font-semibold text-navy-800">Metric:</span>{" "}
                    <span className="text-slate-body/80">fraud losses per approved volume — baseline signed, reported fortnightly</span>
                  </p>
                  <p className="rounded-lg border border-line bg-mist/60 px-3 py-2">
                    <span className="font-semibold text-navy-800">Control owner:</span>{" "}
                    <span className="text-slate-body/80">one accountable name per control — the trail a regulator walks</span>
                  </p>
                  <p className="rounded-lg border border-line bg-mist/60 px-3 py-2">
                    <span className="font-semibold text-navy-800">Risk budget:</span>{" "}
                    <span className="text-slate-body/80">a fixed envelope — innovation inside it moves, nothing outside it ships</span>
                  </p>
                </div>
                {/* A-36: inline CTA inside the section */}
                <Link
                  href="/book-a-briefing/"
                  className="link-animated mt-4 inline-flex items-center gap-1.5 text-[12.5px] font-semibold text-brand-deep"
                >
                  Your charter is drafted in the two-week diagnostic <ArrowRight className="h-3.5 w-3.5" />
                </Link>
              </div>
            </Reveal>
          </div>
        </div>
      </section>

      {/* industries — regime chips + sector explorer (A-33/34/42/56) */}
      <section id="industries" className="scroll-mt-24 border-y border-line bg-mist/60 dot-grid-light">
        <div className="container-dq section-y-sm">
          <Reveal>
            <div className="flex flex-wrap items-end justify-between gap-4">
              <div>
                <p className="kicker-bar text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">
                  Industries
                </p>
                <h2 className="text-display-3 mt-1 text-navy-800 sm:text-[28px]">
                  Built where you operate — under the rules you are held to
                </h2>
                {/* A-42: the list is named for what it is */}
                <p className="mt-2 max-w-2xl text-[14.5px] text-slate-body/75">
                  Each sector brief maps the industry&rsquo;s regulatory reality and decision pressure to our expertise
                  domains, with named workflows and the systems of record your programs will touch.
                </p>
              </div>
              <Link
                href="/industries/"
                className="link-animated inline-flex items-center gap-1.5 text-[13.5px] font-semibold text-brand-deep"
              >
                All industries <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </Reveal>
          <div className="mt-6 max-w-md">
            <IndustryFinder industries={brand.industries} />
          </div>
          {/* A-33/34: regime chip + engagement-note count on every tile */}
          <div className="mt-4 grid gap-2.5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {brand.industries.map((ind) => {
              const notes = CASE_INDUSTRIES.find((c) => c.name === ind.name)?.count ?? 0;
              return (
                <Link
                  key={ind.url}
                  href={ind.url}
                  className="group flex items-center justify-between gap-2 rounded-xl border border-line bg-white px-4 py-3 transition hover:border-brand hover:shadow-1"
                >
                  <span className="min-w-0">
                    <span className="flex flex-wrap items-center gap-1.5 text-[13px] font-semibold text-navy-800 group-hover:text-brand-deep">
                      {ind.name}
                      {INDUSTRY_REGIME[ind.name] && (
                        <span className="rounded-full bg-brand-tint px-2 py-0.5 text-[9.5px] font-bold uppercase tracking-wider text-brand-deep">
                          {INDUSTRY_REGIME[ind.name]}
                        </span>
                      )}
                    </span>
                    {/* A-34: the second line */}
                    <span className="mt-0.5 block text-[11px] text-slate-body/60">
                      Published engagement notes
                    </span>
                  </span>
                  <ArrowRight className="h-3.5 w-3.5 shrink-0 text-brand-deep transition group-hover:translate-x-0.5" aria-hidden="true" />
                </Link>
              );
            })}
          </div>
          {/* A-56: industry → top practices explorer */}
          <HomeIndustryExplorer industries={explorerIndustries} />
        </div>
      </section>

      {/* insights (A-44/45) */}
      <section id="insights" className="container-dq scroll-mt-24 section-y-sm">
        <Reveal>
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <p className="kicker-bar text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">
                Insights
              </p>
              <h2 className="text-display-3 mt-1 text-navy-800 sm:text-[28px]">
                From the delivery floor
              </h2>
              <p className="mt-2 max-w-2xl text-[14.5px] text-slate-body/75">
                Practitioner theses on the retrieval layer, decision hubs, policy envelopes and the
                economics of GenAI — with the vendor questions you should be asking.
              </p>
            </div>
            {/* A-45: the library button is a visible button */}
            <Link
              href="/insights/"
              className="inline-flex items-center gap-1.5 rounded-[10px] border border-line bg-white px-4 py-2 text-[13px] font-semibold text-navy-800 transition hover:border-brand hover:text-brand-deep"
            >
              Insights library <ArrowRight className="h-3.5 w-3.5" />
            </Link>
          </div>
        </Reveal>
        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {brand.insights.map((it, i) => (
            <Reveal key={it.url} delay={i * 50}>
              <Link
                href={it.url}
                className="group flex h-full flex-col rounded-2xl border border-line bg-white p-5 transition hover:-translate-y-0.5 hover:border-brand/60 shadow-1 hover:shadow-2"
              >
                <span className="w-fit rounded-full bg-brand-tint px-2.5 py-0.5 text-[10.5px] font-semibold uppercase tracking-wider text-brand-deep">
                  {it.tag}
                </span>
                <p className="mt-3 font-display text-[15.5px] font-semibold leading-snug text-navy-800 group-hover:text-brand-deep">
                  {it.title}
                </p>
                <p className="mt-2 flex-1 text-[12.5px] leading-relaxed text-slate-body/75">{it.desc}</p>
                {/* A-44: depth meta line */}
                <span className="mt-3 text-[11px] font-medium text-slate-body/55">{insightMeta(it.url)}</span>
              </Link>
            </Reveal>
          ))}
        </div>
      </section>

      {/* A-46: a client voice, anonymized from a published engagement note */}
      <section className="container-dq pt-12">
        <Quote
          text="Queues became visible, predictable and shorter — patients noticed within a quarter."
          attribution="Operations lead, multi-speciality hospital group"
          role="Published engagement note — AI-led token management across hospital OPDs"
        />
      </section>

      {/* newsletter band (A-47) */}
      <section className="container-dq pt-12">
        <Reveal>
          <div className="grid gap-6 rounded-2xl border border-line bg-mist/60 px-6 py-8 shadow-1 sm:px-10 md:grid-cols-[1fr_320px] md:items-center">
            <div>
              <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-brand-deep">The Delivery Floor — monthly</p>
              <p className="mt-1.5 max-w-lg font-display text-[18px] font-semibold leading-snug text-navy-800">
                One email a month — the delivery-floor thesis, the vendor questions, no noise.
              </p>
            </div>
            <NewsletterForm />
          </div>
        </Reveal>
      </section>

      {/* A-58: objection handling before the final CTA */}
      <section id="faq" className="container-dq scroll-mt-24 pt-12">
        <Reveal>
          <div className="max-w-3xl">
            <p className="kicker-bar text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">Before you commit</p>
            <h2 className="text-display-3 mt-1 text-navy-800 sm:text-[28px]">The questions every buyer asks</h2>
          </div>
        </Reveal>
        <Reveal delay={80}>
          <div className="mx-auto mt-6 max-w-3xl text-left">
            <Accordion items={HOME_FAQ.map((f) => ({ q: f.q, a: f.a }))} />
          </div>
        </Reveal>
      </section>

      {/* closing CTA */}
      <section className="container-dq pb-16 pt-12">
        <CtaBand message="Bring the outcome you need — we will show you the accelerator, the platform and the plan we would sign." />
      </section>
    </>
  );
}
