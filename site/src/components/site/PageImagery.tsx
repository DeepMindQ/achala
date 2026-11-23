import Image from "next/image";
import Reveal from "./Reveal";

/* ── PageImagery (Wave 2 → v3: premium art direction) ─────────────────────
   Every page gets a real brand-graded visual. Priority order:
   1. AI-generated brand photography (site/public/images/gen/*) for service
      expertise domains, industries, platforms and company pages.
   2. Animated SMIL SVG art for the long tail (solutions, insights, cases).
   NOTE: next/image does NOT prefix src under unoptimized+basePath, so every
   raw asset path must go through withBasePath(). */

const BP = process.env.NEXT_PUBLIC_BASE_PATH || "";

type Img = { src: string; alt: string };

const gen = (file: string, alt: string): Img => ({
  src: `${BP}/images/gen/${file}.png`,
  alt,
});

const DOMAIN_IMG: Record<string, Img> = {
  "applied-ai-generative-ai": gen("svc-applied-ai", "Neural intelligence mesh over a city skyline — applied and generative AI in production"),
  "agentic-ai-hyperautomation": gen("svc-agentic", "Agent fleet moving in coordinated formation — hyperautomation at work"),
  "data-analytics-lakehouse": gen("svc-data", "Layered lakehouse strata with live data streams — analytics foundation"),
  "cybersecurity-zero-trust": gen("svc-cyber", "Hexagonal shield lattice guarding a luminous core — zero trust defense"),
  "cloud-edge-platform-engineering": gen("svc-cloud", "Edge constellation uplinking to a bright compute core — platform engineering"),
  "quantum-advanced-compute": gen("svc-quantum", "Golden orbit rings around a radiant compute core — quantum-inspired optimization"),
  "blockchain-digital-trust": gen("svc-blockchain", "Crystalline ledger chain passing signed pulses — digital trust"),
  "iot-digital-twin-robotics": gen("svc-iot", "Industrial twin mirrored above the physical floor — IoT and robotics"),
};

const PLATFORM_IMG: Record<string, Img> = {
  nexus: gen("plat-nexus", "EEMS Platform — decision intelligence sphere with ranked data columns"),
  forge: gen("plat-forge", "Fleet Management System — platform strata assembled by construction light"),
  swarm: gen("plat-swarm", "KYC Management System — agent fleet in coordinated formation"),
  sentinel: gen("plat-sentinel", "Tele Medicine Platform — monitored control wall in the security operations room"),
  twinverse: gen("plat-twinverse", "BI & Analytics Platform — the mirrored operations city"),
  quanta: gen("plat-quanta", "Token Management System — optimizer vortex converging on the best schedule"),
  ledger: gen("plat-ledger", "Patient Priority Portal — distributed trust constellation"),
  compass: gen("plat-compass", "Driisti Smart Vision Glasses — governance needle steering regulated delivery"),
};

/* Industry motifs, matched by keyword anywhere in the page path. */
const INDUSTRY_RULES: [RegExp, Img][] = [
  [/banking|financial|insurance|fintech|capital-markets|payments/, gen("ind-banking", "Value streams compounding across a financial estate")],
  [/healthcare|pharma|life-science|medical/, gen("ind-health", "Live clinical signal drawn through a monitored network")],
  [/retail|consumer|e-?commerce|cpg/, gen("ind-retail", "Demand curve rising across retail channels")],
  [/manufacturing|energy|utilit|industrial|automotive|logistics|supply/, gen("ind-manufacturing", "Industrial grid with power flowing between plants")],
  [/government|public-sector|education|defense/, gen("ind-gov", "Public-service dome with governed service arcs")],
  [/telecom|media|travel|hospitality|sports/, gen("ind-telecom", "Global mesh linking markets across continents")],
];

const INDUSTRY_IMG = gen("ind-telecom", "Global delivery mesh in the Achala brand");

const SOLUTION_RULES: [RegExp, Img][] = [
  [/workflow|orchestr|agent|swarm|hyperautomat|automation/, gen("svc-agentic", "Orchestrated agents moving work through lanes")],
  [/decision|intelligen|insight|nexus|forecast/, gen("plat-nexus", "Decision sphere surfacing ranked, governed decisions")],
  [/data|lakehouse|estate|govern|migrat|quality|master/, gen("svc-data", "Lakehouse layers receiving governed data streams")],
  [/securit|zero-trust|threat|sentinel|soc|compliance/, gen("svc-cyber", "Shield lattice sweeping the threat surface")],
  [/quantum|optimi|schedul|route/, gen("svc-quantum", "Optimization orbit rings converging on the best plan")],
  [/blockchain|ledger|trust|chain/, gen("svc-blockchain", "Ledger chain passing signed pulses")],
  [/twin|iot|robot|sensor|simulat/, gen("svc-iot", "Digital twin mirroring physical operations")],
  [/cloud|edge|infrastruc|platform-engineer|sre|devops/, gen("svc-cloud", "Edge lattice uplinking to the core")],
  [/compass|risk|regulat|audit|ethical/, gen("plat-compass", "Governance compass steering delivery")],
  [/generative|gen-?ai|copilot|knowledge|document/, gen("svc-applied-ai", "Neural mesh composing knowledge")],
];

const HUB_IMG: Record<string, Img> = {
  "/services": gen("co-approach", "Service platform strata in the Achala brand"),
  "/solutions": gen("co-home", "Solution field composing intelligence"),
  "/industries": gen("ind-telecom", "Global industry mesh"),
  "/platforms": gen("plat-forge", "Eight platforms, one governed stack"),
  "/case-studies": gen("plat-nexus", "Outcomes surfaced as ranked decisions"),
  "/insights": gen("svc-data", "Insight streams from the knowledge estate"),
  "/newsroom": gen("ind-telecom", "Achala newsroom, worldwide"),
  "/careers": gen("co-careers", "Rising steps — growth at Achala IT Solutions"),
  "/about-us": gen("co-about", "Achala delivery campus at dusk"),
  "/why-achala": gen("plat-compass", "The Achala edge — governed, outcome-linked delivery"),
  "/our-approach": gen("co-approach", "The Achala method, step by step"),
  "/patented-intelligence": gen("svc-quantum", "Patent-pending capability families converging into delivery"),
  "/partner-ecosystem": gen("plat-ledger", "Partner trust constellation"),
  "/global-offices": gen("ind-telecom", "Four global delivery centers"),
  "/contact": gen("co-contact", "Talk to Achala IT Solutions"),
  "/values-culture": gen("plat-compass", "Values that steer every engagement"),
  "/book-a-briefing": gen("co-contact", "Bring your baseline — leave with a plan"),
};

/* Company-section roots that inherit the hub image on sub-URLs too. */
const COMPANY_ROOTS = ["/about-us", "/why-achala", "/our-approach", "/careers", "/newsroom", "/insights", "/case-studies", "/patented-intelligence", "/partner-ecosystem", "/global-offices", "/contact", "/values-culture", "/book-a-briefing"];

const DEFAULT_IMG = gen("co-home", "Achala IT Solutions — intelligence, engineered for outcomes");

function firstRule(rules: [RegExp, Img][], haystack: string): Img | null {
  for (const [re, im] of rules) if (re.test(haystack)) return im;
  return null;
}

export function pick(page: { url: string; template: string; l1?: string | null; l2?: string | null }): Img {
  const url = page.url || "/";
  const hay = `${url} ${page.l1 ?? ""} ${page.l2 ?? ""}`.toLowerCase();

  // hub + company pages first (exact-ish prefixes)
  for (const prefix of Object.keys(HUB_IMG).sort((a, b) => b.length - a.length)) {
    if (url === prefix || url.startsWith(prefix + "/") || url.startsWith(prefix)) {
      if (url === prefix) return HUB_IMG[prefix];
      if (COMPANY_ROOTS.some((c) => url.startsWith(c))) return HUB_IMG[prefix];
    }
  }

  const segs = url.split("/").filter(Boolean);
  if (segs[0] === "services") {
    for (const s of segs) if (DOMAIN_IMG[s]) return DOMAIN_IMG[s];
    const r = firstRule(SOLUTION_RULES, hay);
    if (r) return r;
    return DOMAIN_IMG["applied-ai-generative-ai"];
  }
  if (segs[0] === "platforms") {
    return PLATFORM_IMG[segs[segs.length - 1]] ?? PLATFORM_IMG.nexus;
  }
  if (segs[0] === "solutions") {
    return firstRule(SOLUTION_RULES, hay) ?? gen("co-home", "Solution field composing intelligence");
  }
  if (segs[0] === "industries") {
    return firstRule(INDUSTRY_RULES, hay) ?? INDUSTRY_IMG;
  }
  const r = firstRule(SOLUTION_RULES, hay) ?? firstRule(INDUSTRY_RULES, hay);
  return r ?? DEFAULT_IMG;
}

export function PageImagery({
  page,
}: {
  page: { url: string; template: string; l1?: string | null; l2?: string | null };
}) {
  if (page.url === "/search" || page.url === "/style-guide") return null;
  const im = pick(page);
  const priority = page.template === "expertise_hub" || page.template === "industry_hub";
  return (
    <Reveal className="container-dq pt-2" delay={60}>
      <figure className="pi-figure overflow-hidden rounded-2xl border border-line bg-white shadow-1">
        <div className="relative aspect-[21/9] w-full overflow-hidden bg-navy-900">
          <Image
            src={im.src}
            alt={im.alt}
            fill
            sizes="(max-width: 768px) 100vw, 1200px"
            className="object-cover pi-img"
            priority={priority}
          />
          <div aria-hidden="true" className="pointer-events-none absolute inset-0 bg-gradient-to-t from-navy-950/75 via-navy-950/10 to-transparent" />
          <div aria-hidden="true" className="pointer-events-none absolute inset-0 rounded-2xl ring-1 ring-inset ring-white/10" />
        </div>
      </figure>
    </Reveal>
  );
}
