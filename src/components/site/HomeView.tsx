import Link from "next/link";
import { ArrowRight, BrainCircuit, Bot, Database, ShieldCheck, CloudCog, Atom, Blocks, Radar, Crosshair, UserCheck, Gauge as GaugeIcon } from "lucide-react";
import Reveal from "@/components/site/Reveal";
import { Marquee } from "@/components/site/Motion";
import { Sparkline, NetworkGraph } from "@/components/site/DataVisuals";
import { mulberry32, hashStr } from "@/lib/seeded";
import { PATENTS } from "@/lib/patents";
import { SpotlightSlider, TestimonialBand, IndustryFinder, PlatformTabs, SectionDots } from "@/components/site/Wave3";
import NewsletterForm from "./NewsletterForm";
import { CtaBand, Quote, StatsStrip } from "@/components/site/PagePieces";
import { readPage, fileForUrl, type PageData } from "@/lib/content";

const HOME_SECTIONS = [
  { id: "top", label: "Hero" },
  { id: "output", label: "See the output" },
  { id: "value", label: "Operating discipline" },
  { id: "services", label: "Eight towers" },
  { id: "patents", label: "Patented intelligence" },
  { id: "industries", label: "Industries" },
  { id: "platforms", label: "Platforms" },
  { id: "evidence", label: "Evidence" },
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

const TESTIMONIALS = [
  {
    text: "The engagement charter is what sold us — a metric, an owner and a risk envelope signed before work began. Six months in, the steering pack reads itself.",
    who: "Group COO",
    role: "Top-5 private bank, EMEA",
  },
  {
    text: "We had seen a dozen agentic demos. Achala was the first team that showed us the control trail behind every autonomous action.",
    who: "VP Intelligent Automation",
    role: "Global insurer, APAC",
  },
  {
    text: "Baseline locked in week two, delta audited every gate. When the board asked what changed, the answer was a chart, not a narrative.",
    who: "Chief Supply Chain Officer",
    role: "Discrete manufacturer, AMER",
  },
];

function words(s: string): { w: string; accent: boolean }[] {
  return s.split(" ").map((w) => ({ w, accent: /engineered|outcomes\./.test(w) }));
}

const TOWER_ICONS = [BrainCircuit, Bot, Database, ShieldCheck, CloudCog, Atom, Blocks, Radar];

export default function HomeView() {
  const page: PageData | null = fileForUrl("/") ? readPage(fileForUrl("/")!) : null;
  const brand = page?.extras;
  if (!page || !brand) {
    return <div className="container-dq py-20 text-navy-800">Content not generated yet.</div>;
  }
  return (
    <>
      <SectionDots sections={HOME_SECTIONS} />
      {/* split hero — choreographed text + live intelligence-mesh visual (CHG-234/235) */}
      <section id="top" className="relative overflow-hidden grad-navy-field text-white">
        <div className="bg-field-drift absolute inset-0 dot-grid" aria-hidden="true" />
        <div className="bg-glow-pulse absolute inset-0 grad-orange-glow" aria-hidden="true" />
        <div className="absolute inset-0 pattern-noise" aria-hidden="true" />
        <div className="relative container-dq grid gap-10 pb-14 pt-16 sm:pt-24 lg:grid-cols-[minmax(0,7fr)_minmax(0,5fr)] lg:items-center">
          <div>
            <Reveal className="hero-choreo">
              <p className="rise-item text-[12px] font-semibold uppercase tracking-[0.22em] text-brand-300" style={{ ["--rise-delay" as string]: "40ms" }}>
                Global IT services &amp; consulting
              </p>
              <h1 className="text-display-1 mt-4 max-w-3xl text-white">
                {words("Intelligence, engineered for outcomes.").map((x, i) => (
                  <span key={i}>
                    <span className="rise-word" style={{ ["--rise-delay" as string]: `${120 + i * 90}ms` }}>
                      {x.accent ? <em>{x.w}</em> : x.w}
                    </span>{" "}
                  </span>
                ))}
              </h1>
              <p className="rise-item measure mt-5 text-body-lg leading-relaxed text-white/70" style={{ ["--rise-delay" as string]: "560ms" }}>
                Achala IT Solutions engineers the intelligence layer of the enterprise: applied AI, agentic
                automation, data platforms, cybersecurity and emerging compute — delivered through eight
                proprietary platforms and engagements anchored to named business metrics, named control
                owners and named risk budgets.
              </p>
              <div className="rise-item mt-8 flex flex-wrap gap-3" style={{ ["--rise-delay" as string]: "680ms" }}>
                <Link
                  href="/book-a-briefing/"
                  className="btn-sheen inline-flex items-center gap-2 rounded-[10px] bg-brand px-6 py-3 text-[14px] font-semibold text-white transition hover:bg-brand-hover"
                >
                  Book an Executive Briefing <ArrowRight className="h-4 w-4" />
                </Link>
                <Link
                  href="/services/"
                  className="inline-flex items-center rounded-[10px] border border-white/25 px-6 py-3 text-[14px] font-medium text-white/85 transition hover:border-brand-300 hover:text-brand-300"
                >
                  Explore the eight towers
                </Link>
              </div>
              {/* trust line + rating proof microcopy (CHG-236/257) */}
              <p className="rise-item mt-7 flex flex-wrap items-center gap-x-5 gap-y-2 text-[12px] text-white/55" style={{ ["--rise-delay" as string]: "780ms" }}>
                <span className="inline-flex items-center gap-1.5">
                  <ShieldCheck className="h-3.5 w-3.5 text-brand-300" aria-hidden="true" /> SOC 2 Type II · ISO 27001 · ISO 9001
                </span>
                <span className="inline-flex items-center gap-1.5">
                  <span className="font-bold tabular-nums text-brand-300">4.9/5</span> average client engagement rating
                </span>
                <span>Zero critical data-exposure incidents since inception</span>
              </p>
            </Reveal>
            <div className="mt-10 lg:hidden">
              <StatsStrip stats={brand.stats} />
            </div>
          </div>
          {/* animated hero visual — live decision mesh (client island) */}
          <div className="hidden lg:block">
            <Reveal delay={500}>
              <div className="overflow-hidden rounded-2xl border border-white/10 bg-white/[0.05] backdrop-blur">
                <p className="border-b border-white/10 px-5 py-3 text-[11px] font-bold uppercase tracking-[0.16em] text-brand-300">
                  Live decision mesh — illustrative
                </p>
                <div className="p-3">
                  <NetworkGraph
                    title="Live decision mesh"
                    dark
                    height={252}
                    nodes={[
                      { id: "Core", x: 0.5, y: 0.5, hub: true },
                      { id: "Signals", x: 0.12, y: 0.2 },
                      { id: "Graph", x: 0.2, y: 0.78 },
                      { id: "Agents", x: 0.48, y: 0.92 },
                      { id: "Twin", x: 0.78, y: 0.8 },
                      { id: "Sentinel", x: 0.88, y: 0.42 },
                      { id: "Risk", x: 0.78, y: 0.12 },
                      { id: "Metrics", x: 0.46, y: 0.1 },
                    ]}
                    links={[
                      [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7],
                      [1, 2], [2, 3], [4, 5], [5, 6], [6, 7],
                    ]}
                  />
                </div>
              </div>
            </Reveal>
          </div>
        </div>
        <div className="relative container-dq hidden pb-12 lg:block">
          <StatsStrip stats={brand.stats} />
        </div>
      </section>

      {/* credentials + platform marquee (CHG-124/125) */}
      <div className="border-b border-line bg-navy-900/95">
        <Marquee
          dark
          className="marquee-dark container-dq"
          items={[
            "SOC 2 Type II", "ISO 27001", "ISO 9001", "GDPR & CCPA aligned", "Zero-exposure delivery",
            "Achala Nexus", "Achala Forge", "Achala Swarm", "Achala Sentinel", "Achala Twinverse", "Achala Quanta", "Achala Ledger", "Achala Compass",
            "8 patented method families", "4 global delivery centers",
          ]}
        />
      </div>

      {/* output band — feel what the delivery produces (Wave 2 output graphs) */}
      <section id="output" className="container-dq scroll-mt-24 section-y-sm">
        <Reveal>
          <p className="text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">See the output, not the pitch</p>
          <h2 className="text-display-3 mt-1 max-w-3xl text-navy-800 sm:text-[28px]">
            Every engagement reports the same three curves — baseline locked, delta measured, gates audited.
          </h2>
          <p className="mt-2 max-w-2xl text-[14.5px] text-slate-body/75">
            Illustrative telemetry from comparable programs. Your baseline is set in the value assessment;
            the same panels go to your steering committee every fortnight.
          </p>
        </Reveal>
        <div className="mt-8 grid gap-4 lg:grid-cols-3">
          <Reveal delay={60}>
            <div className="[&>div]:h-full">
              {/* import at top of file */}
              <HomeBar />
            </div>
          </Reveal>
          <Reveal delay={140}>
            <div className="[&>div]:h-full">
              <HomeLine />
            </div>
          </Reveal>
          <Reveal delay={220}>
            <div className="[&>div]:h-full">
              <HomeDonut />
            </div>
          </Reveal>
        </div>
      </section>

      {/* towers */}
      <section id="services" className="scroll-mt-24 border-y border-line bg-mist/60 dot-grid-light">
        <div className="container-dq section-y-sm">
          <Reveal>
            <div className="flex flex-wrap items-end justify-between gap-4">
              <div>
                <p className="kicker-bar text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">
                  Services
                </p>
                <h2 className="text-display-3 mt-1 text-navy-800 sm:text-[30px]">
                  Eight deep technology towers
                </h2>
                <p className="mt-2 max-w-2xl text-[14.5px] text-slate-body/75">
                  We do not sell generic application development. We sell the capability layers that
                  decide whether an enterprise competes in the intelligence era — each tower aligned to
                  your industry from day one.
                </p>
              </div>
              <Link
                href="/services/"
                className="link-animated inline-flex items-center gap-1.5 text-[13.5px] font-semibold text-brand-deep"
              >
                All services <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </Reveal>
          <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {brand.towers.map((t, i) => {
              const Icon = TOWER_ICONS[i % TOWER_ICONS.length];
              return (
                <Reveal key={t.url} delay={i * 40}>
                  <Link
                    href={t.url}
                    className="group flex h-full flex-col rounded-2xl border border-line bg-white p-5 transition hover:-translate-y-0.5 hover:border-brand/60 shadow-1 hover:shadow-2"
                  >
                    <span className="flex items-center justify-between">
                      <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-navy-800 text-brand-300 transition group-hover:bg-brand group-hover:text-white">
                        <Icon className="h-5 w-5" aria-hidden="true" />
                      </span>
                      <span className="font-display text-[12px] font-bold text-brand-deep/70">
                        {String(i + 1).padStart(2, "0")}
                      </span>
                    </span>
                    <p className="mt-3 font-display text-[15.5px] font-semibold leading-snug text-navy-800 group-hover:text-brand-deep">
                      {t.name}
                    </p>
                    <p className="mt-2 flex-1 text-[12.5px] leading-relaxed text-slate-body/75">{t.desc}</p>
                    <span className="mt-4 inline-flex items-center gap-1 text-[12px] font-semibold text-brand-deep">
                      Enter tower <ArrowRight className="h-3.5 w-3.5 transition group-hover:translate-x-0.5" />
                    </span>
                  </Link>
                </Reveal>
              );
            })}
          </div>
        </div>
      </section>

      {/* patented intelligence band (Wave 2 + patent directive) */}
      <section id="patents" className="scroll-mt-24 container-dq section-y-sm">
        <Reveal>
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <p className="kicker-bar text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">
                Patented intelligence
              </p>
              <h2 className="text-display-3 mt-1 text-navy-800 sm:text-[28px]">
                Eight patented method families behind every delivery
              </h2>
              <p className="mt-2 max-w-2xl text-[14.5px] text-slate-body/75">
                Graph-native contextual intelligence, quantum-inspired optimization, federated trust,
                validated ethical decisions and self-evolving learning — filed by our IP foundation and
                hardened in production.
              </p>
            </div>
            <Link
              href="/patented-intelligence/"
              className="link-animated inline-flex items-center gap-1.5 text-[13.5px] font-semibold text-brand-deep"
            >
              The patent map <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </Reveal>
        <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {PATENTS.slice(0, 4).map((p, i) => (
            <Reveal key={p.ref} delay={i * 50}>
              <Link
                href="/patented-intelligence/"
                className="group flex h-full flex-col rounded-2xl border border-line bg-white p-5 transition hover:-translate-y-0.5 hover:border-brand/60 shadow-1 hover:shadow-2"
              >
                <span className="w-fit rounded-full bg-brand-tint px-2.5 py-0.5 text-[10.5px] font-bold uppercase tracking-wider text-brand-deep">
                  {p.ref}
                </span>
                <p className="mt-3 font-display text-[14.5px] font-semibold leading-snug text-navy-800 group-hover:text-brand-deep">
                  {p.title}
                </p>
                <p className="mt-2 flex-1 text-[12.5px] leading-relaxed text-slate-body/75">
                  {p.oneLiner.split(":")[0]}
                </p>
                <span className="mt-4 inline-flex items-center gap-1 text-[12px] font-semibold text-brand-deep">
                  Read the method <ArrowRight className="h-3.5 w-3.5 transition group-hover:translate-x-0.5" />
                </span>
              </Link>
            </Reveal>
          ))}
        </div>
      </section>

      {/* industries */}
      <section id="industries" className="scroll-mt-24 border-y border-line bg-mist/60 dot-grid-light">
        <div className="container-dq section-y-sm">
          <Reveal>
            <div className="flex flex-wrap items-end justify-between gap-4">
              <div>
                <p className="kicker-bar text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">
                  Industries
                </p>
                <h2 className="text-display-3 mt-1 text-navy-800 sm:text-[28px]">
                  Twelve industries, one operating discipline
                </h2>
                <p className="mt-2 max-w-2xl text-[14.5px] text-slate-body/75">
                  Every industry hub maps its regulatory reality, decision pressure and data estate
                  to the towers — 336 capability pages show exactly how each technology applies where
                  you live.
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
          <div className="mt-4 flex flex-wrap gap-2.5">
            {brand.industries.map((ind) => (
              <Link
                key={ind.url}
                href={ind.url}
                className="rounded-full border border-line bg-white px-4 py-2 text-[13px] font-medium text-navy-800 transition hover:border-brand hover:bg-brand-tint hover:text-brand-deep"
              >
                {ind.name}
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* three-pillar operating discipline (CHG-239) */}
      <section id="value" className="scroll-mt-24 border-y border-line bg-mist/60 dot-grid-light">
        <div className="container-dq section-y-sm">
          <Reveal>
            <p className="kicker-bar text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">The operating discipline</p>
            <h2 className="text-display-3 mt-1 max-w-3xl text-navy-800 sm:text-[28px]">
              Three names signed before delivery begins — the engagement charter
            </h2>
          </Reveal>
          <div className="mt-8 grid gap-4 md:grid-cols-3">
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
        </div>
      </section>

      {/* platforms — interactive showcase tabs (CHG-240/241) */}
      <section id="platforms" className="scroll-mt-24 container-dq section-y-sm">
        <Reveal>
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <p className="kicker-bar text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">
                Platforms
              </p>
              <h2 className="text-display-3 mt-1 text-navy-800 sm:text-[28px]">
                Eight proprietary platforms in production
              </h2>
              <p className="mt-2 max-w-2xl text-[14.5px] text-slate-body/75">
                Decision hubs, data contracts, agent fleets, zero-trust estates, digital twins,
                quantum readiness, digital trust and field intelligence — each with architecture and
                evidence trails a regulator can walk.
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

      {/* featured cases — spotlight slider (CHG-244/245/266) */}
      <section id="evidence" className="scroll-mt-24 relative border-y border-line grad-navy-field text-white">
        <div className="bg-field-drift absolute inset-0 dot-grid" aria-hidden="true" />
        <div className="container-dq section-y-sm">
          <Reveal>
            <div className="flex flex-wrap items-end justify-between gap-4">
              <div>
                <p className="kicker-bar-dark text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-300">
                  Evidence
                </p>
                <h2 className="text-display-3 mt-1 text-white sm:text-[28px]">
                  Evidence, not adjectives
                </h2>
                <p className="mt-2 max-w-2xl text-[14.5px] text-white/65">
                  Anonymized engagements with baselines locked in diagnosis and methods available
                  under NDA — because claims without measurement are just marketing.
                </p>
              </div>
              <Link
                href="/case-studies/"
                className="link-animated inline-flex items-center gap-1.5 text-[13.5px] font-semibold text-brand-300"
              >
                All case studies <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </Reveal>
          <div className="mt-8">
            <SpotlightSlider slides={brand.cases} />
          </div>
        </div>
      </section>

      {/* insights */}
      <section className="container-dq section-y-sm">
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
            <Link
              href="/insights/"
              className="link-animated inline-flex items-center gap-1.5 text-[13.5px] font-semibold text-brand-deep"
            >
              Insights library <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </Reveal>
        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {brand.insights.map((it, i) => (
            <Reveal key={it.url} delay={i * 60}>
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
              </Link>
            </Reveal>
          ))}
        </div>
      </section>

      {/* engagement charter pull-quote (CHG-070) + testimonial band (CHG-248) */}
      <section className="container-dq pt-12">
        <Quote
          text="Every engagement anchored to a named business metric, a named control owner and a named risk budget."
          attribution="The Achala engagement charter"
          role="Signed before delivery begins — measured at every gate"
        />
      </section>
      <section className="container-dq pt-8">
        <Reveal>
          <TestimonialBand quotes={TESTIMONIALS} />
        </Reveal>
      </section>

      {/* newsletter band (CHG-254) */}
      <section className="container-dq pt-12">
        <Reveal>
          <div className="grid gap-6 rounded-2xl border border-line bg-mist/60 px-6 py-8 shadow-1 sm:px-10 md:grid-cols-[1fr_320px] md:items-center">
            <div>
              <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-brand-deep">Intelligence briefing</p>
              <p className="mt-1.5 max-w-lg font-display text-[18px] font-semibold leading-snug text-navy-800">
                One briefing a month — the delivery-floor thesis, the vendor questions, no noise.
              </p>
            </div>
            <NewsletterForm />
          </div>
        </Reveal>
      </section>

      {/* closing CTA */}
      <section className="container-dq pb-16 pt-12">
        <CtaBand message="Book an executive briefing — 45 minutes with a practice lead, your metric, and three reference engagements." />
      </section>
    </>
  );
}

/* home output-band charts (client islands with fixed illustrative data) */
import { BarChart, LineArea, Donut } from "@/components/site/DataVisuals";

function HomeBar() {
  return (
    <BarChart
      title="Decision latency — baseline vs. day 90"
      caption="Sample engagement"
      labels={["Fraud triage", "Claims routing", "Demand plan", "Risk review"]}
      series={[
        { name: "Baseline", values: [42, 31, 64, 58] },
        { name: "With Achala", values: [11, 9, 22, 17], color: "#d20000" },
      ]}
      unit=" hrs"
    />
  );
}
function HomeLine() {
  return (
    <LineArea
      title="Autonomous resolution rate — 12-week ramp"
      caption="Live rollout"
      labels={Array.from({ length: 12 }, (_, i) => `W${i + 1}`)}
      series={[{ name: "Autonomous %", values: [8, 12, 19, 27, 34, 41, 48, 55, 61, 66, 71, 76] }]}
      unit="%"
    />
  );
}
function HomeDonut() {
  return (
    <Donut
      title="Where the value landed"
      caption="Impact mix"
      center="100% gated"
      segments={[
        { name: "Cost released", value: 38 },
        { name: "Revenue protected", value: 27 },
        { name: "Risk reduced", value: 21 },
        { name: "Cycle-time recovered", value: 14 },
      ]}
    />
  );
}
