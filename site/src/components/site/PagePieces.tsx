import Link from "next/link";
import { ArrowUpRight, ArrowRight, ChevronRight, GitBranch, Scale, FileSearch, Network } from "lucide-react";
import { PageHero, Blocks, CardGrid, RelatedRail } from "./PageBlocks";
import { DashStyles } from "./ArchDash";
import { PatentStrip, OfficesMap } from "./PageAugment";
import { brandData, pageIndex } from "@/lib/content";
import type { Block, PageData } from "@/lib/content";

export { Breadcrumbs, PageHero, Blocks, CtaBand, CardGrid, Quote, RelatedRail, StatsStrip } from "./PageBlocks";

/* ── Sibling paging + hub (CHG-329/330) + next-step map (CHG-337) ─────── */
function siblingPages(page: PageData) {
  const rows = pageIndex();
  const key = page.l2 || page.l1;
  const group = rows.filter((r) => (r.l2 || r.l1) === key && r.template === page.template);
  const idx = group.findIndex((r) => r.url === page.url);
  if (group.length < 2 || idx === -1) return null;
  const at = (i: number) => group[(i + group.length) % group.length];
  return { prev: at(idx - 1), next: at(idx + 1), position: idx + 1, total: group.length };
}
const NEXT_STEP: Record<string, { label: string; blurb: string; url: string }> = {
  consulting_service: { label: "Book a practice briefing", blurb: "45 minutes with the practice lead — your estate, the method, a straight feasibility read.", url: "/book-a-briefing/" },
  service_page: { label: "Value assessment", blurb: "Price the delta in your estate before anything is signed.", url: "/value-assessment/" },
  expertise_hub: { label: "Book a briefing", blurb: "45 minutes with the domain lead — your metric, our method.", url: "/book-a-briefing/" },
  solution_page: { label: "Book a briefing", blurb: "Map this solution to the metric you own.", url: "/book-a-briefing/" },
  case_study: { label: "Run the same diagnostic", blurb: "The diagnostic that locked this baseline takes two weeks.", url: "/value-assessment/" },
  insight_article: { label: "Talk to the practice lead", blurb: "Bring your context — the thesis meets your data.", url: "/contact/" },
  platform_overview: { label: "See the platform live", blurb: "A working session on your use case, not a demo script.", url: "/book-a-briefing/" },
};

function faqJsonLd(page: PageData): object | null {
  const eligible =
    page.template === "service_page" ||
    page.template === "expertise_hub" ||
    page.template === "services_hub";
  if (!eligible) return null;
  // FAQ = the last bullets block whose items are question-shaped (>= 3).
  // Non-question bullets (rungs, clauses, principles) must never leak into FAQ markup.
  const faqBlock = [...page.blocks]
    .reverse()
    .find(
      (b) =>
        b.t === "bullets" &&
        (b as { items: [string, string][] }).items.length >= 3 &&
        (b as { items: [string, string][] }).items.filter(([q]) => q.trimEnd().endsWith("?")).length >= 3,
    ) as { items: [string, string][] } | undefined;
  if (!faqBlock) return null;
  return {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: faqBlock.items.slice(0, 6).map(([q, a]) => ({
      "@type": "Question",
      name: q,
      acceptedAnswer: { "@type": "Answer", text: a },
    })),
  };
}

/* ── ServiceNetwork — the interlinking web across the Services estate ────
   Every service page sits in a navigable network: siblings inside the same
   expertise domain, curated cross-domain pairings, anonymized field evidence
   and the sector briefs behind it. Server-rendered from the page index, so
   the links are always live and consistent with the URL contract. */
const DOMAIN_PAIRS: Record<string, { label: string; url: string }[]> = {
  "Agentic AI & Hyperautomation": [
    { label: "Conversational AI & Digital Humans", url: "/services/applied-ai-generative-ai/conversational-ai-digital-humans/" },
    { label: "Real-Time Streaming & Event-Driven Decisioning", url: "/services/data-analytics-lakehouse/realtime-streaming-decisioning/" },
    { label: "Zero-Trust Architecture & Implementation", url: "/services/cybersecurity-zero-trust/zero-trust-architecture/" },
  ],
  "Applied AI & Generative AI": [
    { label: "Agentic Process Automation", url: "/services/agentic-ai-hyperautomation/agentic-process-automation/" },
    { label: "Enterprise BI & Executive Analytics", url: "/services/data-analytics-lakehouse/enterprise-bi-executive-analytics/" },
    { label: "AI Security & Model Protection", url: "/services/cybersecurity-zero-trust/ai-security-model-protection/" },
  ],
  "Blockchain & Digital Trust": [
    { label: "Identity & Access Modernization", url: "/services/cybersecurity-zero-trust/identity-access-modernization/" },
    { label: "Industrial IoT & Sensor Fabric", url: "/services/iot-digital-twin-robotics/industrial-iot-sensor-fabric/" },
    { label: "Compliance, Audit & Digital Trust", url: "/services/cybersecurity-zero-trust/compliance-audit-digital-trust/" },
  ],
  "Cloud, Edge & Platform Engineering": [
    { label: "Zero-Trust Architecture & Implementation", url: "/services/cybersecurity-zero-trust/zero-trust-architecture/" },
    { label: "Industrial IoT & Sensor Fabric", url: "/services/iot-digital-twin-robotics/industrial-iot-sensor-fabric/" },
    { label: "Lakehouse Architecture & Migration", url: "/services/data-analytics-lakehouse/lakehouse-architecture/" },
  ],
  "Cybersecurity & Zero-Trust": [
    { label: "Decentralized Identity & Verifiable Credentials", url: "/services/blockchain-digital-trust/decentralized-identity/" },
    { label: "Hybrid & Multicloud Architecture", url: "/services/cloud-edge-platform-engineering/hybrid-multicloud-architecture/" },
    { label: "Post-Quantum Cryptography Migration", url: "/services/quantum-advanced-compute/post-quantum-cryptography/" },
  ],
  "Data, Analytics & Lakehouse": [
    { label: "Generative AI Platform Engineering", url: "/services/applied-ai-generative-ai/genai-platform-engineering/" },
    { label: "Decision Intelligence Systems", url: "/services/agentic-ai-hyperautomation/decision-intelligence-systems/" },
    { label: "Cloud-Native & Legacy Modernization", url: "/services/cloud-edge-platform-engineering/cloud-native-modernization/" },
  ],
  "IoT, Digital Twin & Robotics": [
    { label: "High-Performance & Mission-Critical Systems", url: "/services/cloud-edge-platform-engineering/high-performance-mission-critical/" },
    { label: "Advanced Risk & Predictive Analytics", url: "/services/data-analytics-lakehouse/advanced-risk-predictive-analytics/" },
    { label: "Zero-Trust Architecture & Implementation", url: "/services/cybersecurity-zero-trust/zero-trust-architecture/" },
  ],
  "Quantum & Advanced Compute": [
    { label: "Cyber Resilience & Incident Recovery", url: "/services/cybersecurity-zero-trust/cyber-resilience-incident-recovery/" },
    { label: "Advanced Risk & Predictive Analytics", url: "/services/data-analytics-lakehouse/advanced-risk-predictive-analytics/" },
    { label: "SRE & Reliability Engineering", url: "/services/cloud-edge-platform-engineering/sre-reliability-engineering/" },
  ],
};

function ServiceNetwork({ page }: { page: PageData }) {
  const isService = page.template === "service_page";
  const isDomainHub = page.template === "expertise_hub";
  const isRoot = page.template === "services_hub";
  if (!isService && !isDomainHub && !isRoot) return null;

  const rows = pageIndex();
  const siblings = isService
    ? rows.filter((r) => r.template === "service_page" && r.l2 === page.l2 && r.url !== page.url)
    : isRoot
      ? rows.filter((r) => r.template === "expertise_hub" && r.l1 === "Services")
      : isDomainHub
        ? rows.filter((r) => r.template === "expertise_hub" && r.l1 === "Services" && r.url !== page.url)
        : [];
  const pairs = isRoot || isDomainHub ? [] : DOMAIN_PAIRS[page.l2] ?? [];
  const evidence = page.evidence ?? [];
  if (!siblings.length && !pairs.length && !evidence.length) return null;

  const groupHead = "text-[10.5px] font-bold uppercase tracking-[0.14em] text-slate-body/55";
  const chip =
    "inline-flex items-center rounded-lg border border-line bg-mist/60 px-3 py-1.5 text-[12px] font-medium text-navy-800 transition hover:border-brand hover:text-brand-deep hover:bg-white";

  return (
    <section className="mt-14" aria-label="Where this capability connects">
      <div className="flex items-center gap-2.5">
        <Network className="h-4.5 w-4.5 text-brand-deep" aria-hidden="true" />
        <h2 className="font-display text-[20px] font-semibold text-navy-800 sm:text-[22px]">
          Where this capability connects
        </h2>
      </div>
      <p className="mt-1 max-w-3xl text-[13px] text-slate-body/70">
        The service network around this page — continue across the expertise, pair with the adjacent domain,
        or read the anonymized field evidence behind the method.
      </p>
      <div className="mt-6 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
        {siblings.length > 0 && (
          <div className="rounded-2xl border border-line bg-white p-5 shadow-1">
            <p className={`flex items-center gap-1.5 ${groupHead}`}>
              <GitBranch className="h-3.5 w-3.5 text-brand-deep" aria-hidden="true" />
              {isRoot
                ? "The eight expertise domains"
                : isDomainHub
                  ? "The other seven expertise domains"
                  : "Continue across this expertise"}
            </p>
            <div className="mt-3 flex flex-wrap gap-2">
              {siblings.map((s) => (
                <Link key={s.url} href={s.url} className={chip}>
                  {s.title}
                </Link>
              ))}
            </div>
            {!isRoot && !isDomainHub && page.l2 && (
              <Link
                href={`/services/${page.l2.toLowerCase().replace(/[^a-z]+/g, "-").replace(/^-|-$/g, "")}/`}
                className="mt-4 inline-flex items-center gap-1 text-[12px] font-semibold text-brand-deep hover:underline"
              >
                {page.l2} domain overview <ArrowRight className="h-3 w-3" aria-hidden="true" />
              </Link>
            )}
            {isDomainHub && (
              <Link
                href="/services/"
                className="mt-4 inline-flex items-center gap-1 text-[12px] font-semibold text-brand-deep hover:underline"
              >
                All services and practices <ArrowRight className="h-3 w-3" aria-hidden="true" />
              </Link>
            )}
          </div>
        )}
        {pairs.length > 0 && (
          <div className="rounded-2xl border border-line bg-white p-5 shadow-1">
            <p className={`flex items-center gap-1.5 ${groupHead}`}>
              <Scale className="h-3.5 w-3.5 text-brand-deep" aria-hidden="true" />
              Pairs with — adjacent domains
            </p>
            <div className="mt-3 flex flex-col gap-2">
              {pairs.map((p) => (
                <Link
                  key={p.url}
                  href={p.url}
                  className="group flex items-center justify-between gap-3 rounded-lg border border-line bg-mist/50 px-3.5 py-2.5 transition hover:border-brand/60 hover:bg-white"
                >
                  <span className="text-[12.5px] font-medium text-navy-800 group-hover:text-brand-deep">{p.label}</span>
                  <ArrowRight className="h-3.5 w-3.5 shrink-0 text-brand-deep transition group-hover:translate-x-0.5" aria-hidden="true" />
                </Link>
              ))}
            </div>
          </div>
        )}
        {evidence.length > 0 && (
          <div className="rounded-2xl border border-line bg-white p-5 shadow-1">
            <p className={`flex items-center gap-1.5 ${groupHead}`}>
              <FileSearch className="h-3.5 w-3.5 text-brand-deep" aria-hidden="true" />
              Field evidence — anonymized builds
            </p>
            <div className="mt-3 flex flex-col gap-2">
              {evidence.map((e) => (
                <Link
                  key={e.url}
                  href={e.url}
                  className="group flex items-center justify-between gap-3 rounded-lg border border-line bg-mist/50 px-3.5 py-2.5 transition hover:border-brand/60 hover:bg-white"
                >
                  <span>
                    <span className="block text-[12.5px] font-medium text-navy-800 group-hover:text-brand-deep">{e.title}</span>
                    <span className="mt-0.5 block text-[11px] text-slate-body/60">{e.ind}</span>
                  </span>
                  <ArrowUpRight className="h-3.5 w-3.5 shrink-0 text-brand-deep transition group-hover:translate-x-0.5 group-hover:-translate-y-0.5" aria-hidden="true" />
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}

/* ── Universal content page (all templates except home) ───────────────── */
export function ContentPage({ page }: { page: PageData }) {
  const kicker = sectionKicker(page);
  const siblings = siblingPages(page);
  const nextStep = NEXT_STEP[page.template];
  const faq = faqJsonLd(page);
  return (
    <>
      {faq && <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(faq) }} />}
      <DashStyles />
      <PageHero page={page} kicker={kicker}>
        {page.published && (
          <p className="mt-3 inline-flex rounded-full border border-white/20 px-3 py-1 text-[11.5px] text-white/70">
            Published {page.published}
          </p>
        )}
        {page.profile && (
          <div className="mt-5 flex flex-wrap items-center gap-3">
            {/* navy-orange monogram (CHG-066) until photos exist */}
            <span className="flex h-12 w-12 items-center justify-center rounded-full bg-gradient-to-br from-navy-700 to-brand font-display text-[15px] font-bold text-white shadow-2">
              {page.profile.name
                .split(" ")
                .map((w) => w[0])
                .slice(0, 3)
                .join("")}
            </span>
            <div>
              <p className="text-[14.5px] font-semibold text-white">{page.profile.name}</p>
              <p className="text-[12px] text-white/55">{page.profile.role}</p>
            </div>
            <span className="ml-2 rounded-full border border-white/20 px-2.5 py-0.5 text-[10.5px] uppercase tracking-wider text-white/50">
              Profile
            </span>
          </div>
        )}
      </PageHero>
      <div className="container-dq py-12">
        {/* Phase 1 editorial layout: ONE centered article column. The old
            232px "On this page" rail and the duplicate back-to-hub link were
            removed — they produced the term-paper structure the redesign bans.
            Section wayfinding = breadcrumbs (hero) + hover anchors (headings)
            + the related/next-step rails at the end. */}
        <article className="dq-article mx-auto w-full max-w-[1080px]">
          <Blocks blocks={page.blocks} skip={["hero"]} />

          {/* in-narrative exploration cards ("Services in this expertise", hubs…) */}
          <CardGrid
            cards={page.cards}
            heading={cardsHeading(page.template)}
            sub={cardsSub(page.template)}
          />

          {/* the interlinking web — siblings, paired domains, field evidence */}
          <ServiceNetwork page={page} />

          {/* the patented methods underneath — factual, patent-mapped */}
          <PatentStrip page={page} />

          {page.profile && page.profile.focus.length > 0 && (
            <div className="mt-6 flex flex-wrap gap-2">
              {page.profile.focus.map((f) => (
                <span key={f} className="rounded-full border border-line bg-mist px-3 py-1 text-[12px] font-medium text-navy-800">
                  {f}
                </span>
              ))}
            </div>
          )}
          <RelatedRail links={page.related} />
          {/* prev / next sibling paging (CHG-330) */}
          {siblings && (
            <nav aria-label="Sibling pages" className="mt-12 grid gap-3 border-t border-line pt-6 sm:grid-cols-2">
              <Link
                href={siblings.prev.url}
                className="group rounded-xl border border-line bg-mist/50 px-4 py-3.5 transition hover:border-brand/60 hover:bg-white"
              >
                <span className="text-[10.5px] font-bold uppercase tracking-[0.14em] text-slate-body/50">
                  Previous · {siblings.position - 1 < 1 ? siblings.total : siblings.position - 1} of {siblings.total}
                </span>
                <span className="mt-0.5 flex items-center gap-1.5 text-[13.5px] font-semibold text-navy-800 group-hover:text-brand-deep">
                  <ChevronRight className="h-3.5 w-3.5 rotate-180" aria-hidden="true" /> {siblings.prev.title}
                </span>
              </Link>
              <Link
                href={siblings.next.url}
                className="group rounded-xl border border-line bg-mist/50 px-4 py-3.5 text-right transition hover:border-brand/60 hover:bg-white"
              >
                <span className="text-[10.5px] font-bold uppercase tracking-[0.14em] text-slate-body/50">
                  Next · {siblings.position + 1 > siblings.total ? 1 : siblings.position + 1} of {siblings.total}
                </span>
                <span className="mt-0.5 flex items-center justify-end gap-1.5 text-[13.5px] font-semibold text-navy-800 group-hover:text-brand-deep">
                  {siblings.next.title} <ChevronRight className="h-3.5 w-3.5" aria-hidden="true" />
                </span>
              </Link>
            </nav>
          )}
          {/* contextual next-step (CHG-337) */}
          {nextStep && (
            <Link
              href={nextStep.url}
              className="group mt-10 flex flex-col gap-3 rounded-2xl grad-navy-field px-6 py-6 text-white shadow-3 transition hover:shadow-2 sm:flex-row sm:items-center sm:justify-between"
            >
              <span>
                <span className="text-[11px] font-bold uppercase tracking-[0.16em] text-brand-300">Next step</span>
                <span className="mt-1 block font-display text-[17px] font-semibold text-white">{nextStep.label}</span>
                <span className="mt-0.5 block text-[12.5px] text-white/65">{nextStep.blurb}</span>
              </span>
              <span className="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-brand text-white transition group-hover:scale-105">
                <ArrowUpRight className="h-4.5 w-4.5" aria-hidden="true" />
              </span>
            </Link>
          )}
          <p className="mt-8 border-t border-line pt-4 text-[11px] text-slate-body/55">
            Maintained by the Achala IT Solutions practice council · Last reviewed 2026-11 ·
            {" "}
            <Link href="/html-sitemap/" className="hover:text-brand-deep">
              Sitemap
            </Link>
          </p>
        </article>
        {page.url === "/global-offices/" && (
          <div className="mt-10">
            <OfficesMap offices={brandData().offices} />
          </div>
        )}
      </div>
    </>
  );
}

function sectionKicker(page: PageData): string | undefined {
  const map: Record<string, string> = {
    expertise_hub: "Expertise Domain",
    service_page: "Service",
    industry_hub: "Industry",
    subindustry_page: "Sub-industry",
    industry_capability: "Industry Capability",
    sub_capability: "Sub-Industry Capability",
    solution_page: "Solution",
    platform_overview: "Platform",
    platform_architecture: "Platform — Architecture & Trust",
    platform_usecases: "Platform — Industry Use Cases",
    case_study: "Case study — anonymized",
    insight_article: "Insight",
    insights_category: "Insights Library",
    company_page: "Company",
    approach_page: "Our Approach",
    consulting_hub: "Consulting Services",
    consulting_service: "Consulting Practice",
    legal_page: "Legal & Compliance",
    contact_page: "Contact",
    leadership_profile: "Leadership",
    partner_page: "Partner Ecosystem — Alliance in validation",
    careers_page: "Careers",
    newsroom_article: "Newsroom",
    cases_hub: "Evidence library",
    services_hub: "Services & Expertise",
    industries_hub: "Industries",
    solutions_hub: "Solutions",
    platforms_hub: "Proprietary Platforms",
    insights_hub: "Insights Library",
  };
  return map[page.template];
}

function cardsHeading(template: string): string {
  const map: Record<string, string> = {
    services_hub: "The eight expertise domains",
    industries_hub: "Twelve industries, one operating discipline",
    solutions_hub: "24 outcome-linked solutions",
    platforms_hub: "The Achala platform portfolio",
    cases_hub: "The case index",
    insights_hub: "Insight categories",
    expertise_hub: "Services in this expertise domain",
    industry_hub: "Sub-industries",
    subindustry_page: "Capabilities for this sub-industry",
    industry_capability: "Sub-industry depth",
    solution_page: "Related solutions",
    platforms_hub_alt: "",
  };
  return map[template] ?? "Explore further";
}

function cardsSub(template: string): string {
  const map: Record<string, string> = {
    services_hub: "Each domain card opens its hub — the practices, the reference architectures, the sector briefs and the metric the domain is managed on.",
    cases_hub: "Indexed by industry and service area — every case carries its measured delta and the gates that governed the build.",
    insights_hub: "Practitioner theses from the delivery floor — published with vendor questions included.",
  };
  return map[template] ?? "";
}
