# -*- coding: utf-8 -*-
"""Wave-2 domain banks for the Achala IT Solutions content engine.

Pure data. The engine (dqs_content_wave2.py) combines these banks with each
page's identity (tower x industry x sub-industry x platform) and a seeded RNG
to synthesize technically deep, page-unique prose. Nothing here is copied to
more than one page verbatim: identity nouns are injected into every sentence.
"""

# ── 8 service towers ────────────────────────────────────────────────────────
# arch        : labels fed to the animated diagrams
# stack       : engineering stack items (4-5 picked per page, phrased uniquely)
# telemetry   : (name, direction, lo, hi, unit) — engine phrases the desc
# guards      : (name, seed clause) — failure modes & the guards we ship
# systems     : tower-level integration surface seeds
# diagram     : primary animated diagram archetype

TOWERS = {
    "applied-ai-generative-ai": {
        "name": "Applied AI & Generative AI",
        "short": "applied AI",
        "arch": ["Documents & policies", "Grounded retrieval core", "Eval & guard harness", "Decision plane", "Governed action", "Evidence telemetry"],
        "arch_title": "Grounded generation fabric",
        "diagram": "decision-fabric",
        "stack": [
            ("vLLM serving pool", "batched GPU inference with p95 latency ceilings"),
            ("hybrid retrieval", "BM25 + dense embeddings with reciprocal-rank fusion"),
            ("LangGraph state machines", "typed graph runs with checkpointed state"),
            ("Ragas eval harness", "groundedness and faithfulness scored per release"),
            ("PII redaction fence", "entity-level masking before any model call"),
            ("OpenTelemetry traces", "per-span token cost and latency attribution"),
            ("prompt registry", "versioned templates with signed change records"),
            ("canary eval gate", "release blocked when groundedness regresses"),
        ],
        "telemetry": [
            ("grounded-answer rate", "up", 88, 95, "% of responses citing retrieved evidence"),
            ("cost per resolved query", "down", 25, 45, "% after cache and routing tuning"),
            ("p95 response latency", "down", 30, 50, "% under load-matched conditions"),
            ("reviewer override rate", "down", 35, 55, "% on drafted knowledge work"),
            ("citation precision", "up", 90, 97, "% of citations pointing to the right passage"),
        ],
        "guards": [
            ("Ungrounded fluency", "answers that read well but cite nothing are blocked at the fence — every claim carries a retrieval pointer or the response declines"),
            ("Silent prompt drift", "prompt changes ship through a signed registry with eval baselines, so a tweak can never quietly move behavior"),
            ("PII escape", "entity-level redaction runs before inference and after generation, with sampling audits on live traffic"),
        ],
        "systems": ["SharePoint / Drive corpora", "Confluence & policy vaults", "CRM knowledge objects", "ITSM knowledge base", "DMS repositories", "Data lakehouse tables"],
    },
    "agentic-ai-hyperautomation": {
        "name": "Agentic AI & Hyperautomation",
        "short": "agentic automation",
        "arch": ["Work intake & queueing", "Role & policy engine", "Agent fleet execution", "Tool & system adapters", "Verification & eval", "Audit & cost ledger"],
        "arch_title": "Agent fleet orchestration loop",
        "diagram": "orchestration-loop",
        "stack": [
            ("Temporal durable execution", "idempotent runs that survive retries and deploys"),
            ("LangGraph agent runtimes", "typed tool calls with scoped credentials"),
            ("OPA policy engine", "high-risk actions routed to approval workflows"),
            ("Kafka event backbone", "task queues with priority lanes for SLA work"),
            ("Redis blackboard", "shared-memory contracts that stop duplicated work"),
            ("cost metering sidecar", "per-team, per-role token and action budgets"),
            ("canary cohorts", "agent releases staged shadow-first with auto rollback"),
        ],
        "telemetry": [
            ("straight-through processing", "up", 25, 45, "points on selected decision paths"),
            ("cost per completed task", "down", 30, 50, "% after metering and budget gates"),
            ("queue utilization", "up", 80, 90, "% task-slot efficiency at steady state"),
            ("rollback time", "down", 60, 80, "% — cohort rollout contains incidents in minutes"),
            ("approval cycle time", "down", 40, 60, "% on policy-routed actions"),
        ],
        "guards": [
            ("Agent sprawl", "every agent ships with a role spec, budget and owner — unregistered agents are quarantined at the queue"),
            ("Duplicated work", "blackboard contracts make task claims exclusive, so two agents can never own the same case"),
            ("Runaway loops", "durable execution caps retries, tool calls and spend per run; breach trips a kill switch that pages the owner"),
        ],
        "systems": ["ITSM platforms", "ERP order modules", "CRM workflows", "Core document systems", "RPA bridges", "Email & ticket intake"],
    },
    "data-analytics-lakehouse": {
        "name": "Data, Analytics & Lakehouse",
        "short": "lakehouse engineering",
        "arch": ["Source systems", "Ingest & contracts", "Lakehouse storage", "Feature & metric layer", "Serving & BI", "Decision feedback"],
        "arch_title": "Governed lakehouse pipeline",
        "diagram": "pipeline",
        "stack": [
            ("Delta / Iceberg tables", "ACID guarantees with time travel and schema enforcement"),
            ("data contracts", "producer-side schemas with breakage alerts, not silent nulls"),
            ("dbt transformation graph", "tested, documented models with lineage exposure"),
            ("Unity Catalog governance", "tag-based access control inherited end to end"),
            ("streaming ingest", "Kafka-backed CDC with exactly-once sinks"),
            ("cost-aware clustering", "partition and Z-order plans reviewed per load"),
            (" freshness SLOs", "per-table freshness and completeness SLAs wired to paging"),
        ],
        "telemetry": [
            ("batch window", "down", 50, 70, "% after re-architecture"),
            ("pipeline breakage MTTR", "down", 55, 75, "% with contracts and lineage paging"),
            ("query p95", "down", 40, 60, "% on the certified gold layer"),
            ("freshness SLO attainment", "up", 97, 99.5, "% of tables inside their declared window"),
            ("warehouse spend per query", "down", 20, 40, "% after clustering and pruning"),
        ],
        "guards": [
            ("Metric anarchy", "one certified semantic layer owns definitions — dashboards that shadow it lose endorsement and budget"),
            ("Silent schema drift", "producer contracts fail loudly at ingest; downstream models refuse to build on drifted sources"),
            ("Cost creep", "per-team chargeback with query tags; untagged compute is quarantined at the queue level"),
        ],
        "systems": ["Core ERP", "CRM & marketing clouds", "Event streams & CDC", "SaaS operational stores", "Legacy warehouses", "Partner file feeds"],
    },
    "cybersecurity-zero-trust": {
        "name": "Cybersecurity & Zero-Trust",
        "short": "zero trust",
        "arch": ["Identity & posture", "Policy decision point", "Segmented access fabric", "Workload enforcement", "Detection & response", "Audit evidence"],
        "arch_title": "Zero-trust verification mesh",
        "diagram": "zero-trust-mesh",
        "stack": [
            ("SPIFFE/SPIRE workload identity", "short-lived SVIDs instead of shared secrets"),
            ("OPA sidecar authorization", "deny-by-default decisions logged per call"),
            ("micro-segmentation", "identity-based east-west rules, not flat networks"),
            ("EPP/XDR fabric", "telemetry fused into one detection graph"),
            ("SOAR playbooks", "containment actions pre-approved with blast-radius caps"),
            ("CNAPP posture scans", "misconfiguration deltas opened as tickets, not PDFs"),
            ("purple-team cadence", "segmentation proven under live attack simulation"),
        ],
        "telemetry": [
            ("alert false-positive rate", "down", 40, 60, "% with tuned detections and policy context"),
            ("lateral-movement dwell time", "down", 55, 75, "% after segmentation"),
            ("privileged session coverage", "up", 95, 100, "% of admin paths brokered and recorded"),
            ("mean time to contain", "down", 45, 65, "% with pre-approved playbooks"),
            ("audit finding closure", "up", 20, 40, "% faster with evidence-as-code"),
        ],
        "guards": [
            ("Flat-network habits", "every east-west flow needs an identity reason; legacy allowances expire on a dated register"),
            ("Alert flood", "detections are deduplicated into incidents at the graph level, so analysts work one story, not four hundred rows"),
            ("Audit theater", "controls map to named evidence artifacts generated in-flight — screenshots of dashboards do not count"),
        ],
        "systems": ["IdP / IGA platforms", "SIEM & XDR", "Cloud CSPM/CNAPP", "Secrets managers", "Ticketing & SOC tooling", "Network policy controllers"],
    },
    "cloud-edge-platform-engineering": {
        "name": "Cloud, Edge & Platform Engineering",
        "short": "platform engineering",
        "arch": ["Golden-path templates", "Self-service portal", "GitOps control plane", "Runtime enforcement", "Observability plane", "FinOps telemetry"],
        "arch_title": "Golden-path platform topology",
        "diagram": "edge-topology",
        "stack": [
            ("Backstage-style portal", "scaffolding that ships a compliant service in minutes"),
            ("GitOps reconciliation", "Argo-style drift correction with signed commits"),
            ("Kubernetes landing zones", "namespaces, quotas and network policy pre-wired"),
            ("service mesh", "mTLS by default with traffic policy as code"),
            ("OpenTelemetry defaults", "traces, metrics and logs wired into templates"),
            ("FinOps unit economics", "cost per service surfaced in the portal, per team"),
            ("SLO tooling", "error budgets enforced in the release gate"),
        ],
        "telemetry": [
            ("environment lead time", "down", 70, 85, "% — from weeks to same-day"),
            ("change failure rate", "down", 35, 55, "% with progressive delivery"),
            ("toil hours per sprint", "down", 40, 60, "% absorbed by golden paths"),
            ("cost per deployed service", "down", 20, 35, "% after right-sizing"),
            ("SLO attainment", "up", 95, 99, "% across tier-one services"),
        ],
        "guards": [
            ("Snowflake infrastructure", "off-template builds need a signed exception with an expiry date — the platform team can see every drift"),
            ("Observability theater", "dashboards without alerts, or alerts without owners, fail the readiness review"),
            ("Cost invisibility", "untagged resources are quarantined within 24 hours; every team sees its own unit costs weekly"),
        ],
        "systems": ["Cloud landing zones", "CI/CD systems", "Artifact registries", "Secrets & PKI", "Observability stacks", "Ticketing & on-call"],
    },
    "quantum-advanced-compute": {
        "name": "Quantum & Advanced Compute",
        "short": "quantum-inspired optimization",
        "arch": ["Problem formulation", "Constraint encoding", "Hybrid solver pool", "Solution validation", "Plan commit", "Baseline tracking"],
        "arch_title": "Optimization convergence funnel",
        "diagram": "optimization-funnel",
        "stack": [
            ("QUBO/Ising formulation", "business constraints encoded as energy landscapes"),
            ("hybrid solvers", "quantum-inspired annealing + classical branch-and-bound"),
            ("simulation harness", "candidate plans replayed against historical demand"),
            ("constraint linter", "infeasible plans rejected before reaching planners"),
            ("solver benchmark registry", "every run compared against the best classical baseline"),
            ("explainability layer", "each committed plan ships with binding-constraint audit"),
        ],
        "telemetry": [
            ("plan quality gap", "down", 15, 30, "% versus the incumbent heuristic"),
            ("solve time", "down", 40, 65, "% on equivalent constraint sets"),
            ("constraint violations", "down", 80, 95, "% versus planner-manual plans"),
            ("planner override rate", "down", 30, 50, "% once trust is established"),
            ("margin captured", "up", 5, 12, "% on optimized decision slices"),
        ],
        "guards": [
            ("Solver worship", "a quantum-inspired result that cannot beat the classical baseline is rejected by default — benchmarks are published"),
            ("Constraint hiding", "planners can mark any output infeasible; every rejection trains the formulation, not the planner"),
            ("Black-box plans", "each committed plan carries a binding-constraint report; unexplainable schedules never reach execution"),
        ],
        "systems": ["APS / planning suites", "WMS & TMS", "ERP master data", "Demand forecasting stores", "Portfolio risk engines", "Grid & network models"],
    },
    "blockchain-digital-trust": {
        "name": "Blockchain & Digital Trust",
        "short": "digital trust",
        "arch": ["Event capture", "Canonical signing", "Distributed ledger", "Verification layer", "Settlement & action", "Provenance query"],
        "arch_title": "Signed provenance chain",
        "diagram": "ledger-chain",
        "stack": [
            ("permissioned DLT", "Hyperledger-class networks with known validators"),
            ("W3C Verifiable Credentials", "issuer-agnostic attestations with revocation"),
            ("hash-linked anchoring", "business events anchored without leaking payloads"),
            ("HSM key ceremonies", "root-of-trust operations under dual control"),
            ("on-chain/off-chain split", "personal data stays off-ledger by design"),
            ("notarized audit exports", "regulator-ready evidence with chain-of-custody"),
        ],
        "telemetry": [
            ("reconciliation breaks", "down", 60, 85, "% on anchored flows"),
            ("settlement cycle time", "down", 30, 50, "% for verified counterparties"),
            ("attestation verification", "up", 95, 100, "% automated at ingest"),
            ("audit evidence prep", "down", 50, 70, "% — exports are generated, not assembled"),
            ("dispute resolution time", "down", 40, 60, "% with shared provenance"),
        ],
        "guards": [
            ("Ledger worship", "a chain only helps where counterparties dispute truth; workflows that already trust one database stay on one database"),
            ("On-chain PII", "personal data never touches the ledger; only salted hashes and pointers are anchored"),
            ("Key fragility", "root keys live in HSMs under dual control with ceremony logs; rotation is rehearsed, not documented"),
        ],
        "systems": ["ERP & GL systems", "Trade & settlement rails", "Notary & registry services", "IoT attestation feeds", "Supplier portals", "Regulatory reporting"],
    },
    "iot-digital-twin-robotics": {
        "name": "IoT, Digital Twin & Robotics",
        "short": "digital twin",
        "arch": ["Sensors & PLCs", "Edge gateway", "Twin state store", "Simulation & prediction", "Control recommendations", "Plant feedback"],
        "arch_title": "Physical-digital twin loop",
        "diagram": "twin-loop",
        "stack": [
            ("OPC UA / MQTT spine", "unified namespace for every sensor and cell"),
            ("edge inference", "vision and anomaly models running at the gateway"),
            ("twin state store", "calibrated digital mirror with drift tracking"),
            ("physics + ML hybrid", "first-principles models regularized by plant data"),
            ("OT security zoning", "Purdue-ring segmentation with unidirectional gateways"),
            ("control guard-banding", "recommendations clamped to certified envelopes"),
        ],
        "telemetry": [
            ("unplanned downtime", "down", 25, 45, "% on instrumented lines"),
            ("scrap & rework", "down", 15, 30, "% with early-warning signatures"),
            ("OEE uplift", "up", 5, 12, "points on twin-covered assets"),
            ("energy per unit", "down", 8, 18, "% after orchestration tuning"),
            ("alarm noise", "down", 50, 70, "% after rationalization"),
        ],
        "guards": [
            ("Twin decay", "models are recalibrated against plant truth every shift; a drifting twin loses control authority automatically"),
            ("OT/IT blur", "control traffic never crosses zones without a broker; laptops do not talk to PLCs"),
            ("Override culture", "operators can reject any recommendation in one tap — rejections are mined weekly, not punished"),
        ],
        "systems": ["SCADA & historians", "MES layers", "CMMS maintenance", "WMS floor systems", "Vision & sensor fleets", "Energy meters"],
    },
}

# ── 12 industries ───────────────────────────────────────────────────────────
# systems : integration-surface items (name, seed clause)
# regimes : regulatory anchors cited in governance notes
# vocab   : sector phrases injected into prose
# kctx    : KPI contexts

INDUSTRIES = {
    "banking-financial-services": {
        "name": "Banking & Financial Services",
        "systems": [
            ("core banking rails", "ledger, payments and interest engines with CDC ingest"),
            ("card switch & fraud stores", "authorization streams scored at event time"),
            ("KYC/AML case managers", "periodic review queues with evidence hooks"),
            ("trade & treasury systems", "position and liquidity feeds under sub-second SLOs"),
            ("CRM & onboarding", "journey events joined to decision outcomes"),
            ("regulatory reporting hub", "lineage-backed submissions with replay"),
        ],
        "regimes": ["DORA operational resilience", "Basel III endgame capital", "GDPR / privacy regimes", "PSD2 / open banking", "AML/CTF directives", "EBA outsourcing guidelines"],
        "vocab": ["instant rails", "fraud velocity", "capital regimes", "credit decisioning", "KYC refresh", "liquidity stress", "resilience testing", "branch & core estate"],
        "kctx": ["per 1,000 transactions", "per decision path", "per product line", "per business day"],
    },
    "insurance": {
        "name": "Insurance & Risk",
        "systems": [
            ("policy admin platforms", "master policy state with event streams"),
            ("claims orchestration", "FNOL through settlement with stage telemetry"),
            ("underwriting workbench", "risk inputs, referrals and authority limits"),
            ("actuarial & pricing stores", "exposure bases and factor tables under versioning"),
            ("claims document intake", "indexed packets with redaction at rest"),
            ("reinsurance reporting", "treaty-level aggregation with audit lineage"),
        ],
        "regimes": ["Solvency II reporting", "GDPR / privacy regimes", "EIOPA conduct expectations", "IFRS 17 data chains", "DORA operational resilience", "model governance SR 11-7 style"],
        "vocab": ["loss ratios", "prior authorization", "claims leakage", "underwriting discipline", "reinsurance treaties", "subrogation", "actuarial bases", "claims triage"],
        "kctx": ["per 1,000 claims", "per policy cohort", "per underwriting referral", "per claims handler"],
    },
    "healthcare-life-sciences": {
        "name": "Healthcare & Life Sciences",
        "systems": [
            ("EHR integration", "FHIR-backed reads with consent-aware scopes"),
            ("claims & clearinghouse feeds", "remittance loops joined to clinical events"),
            ("pharmacovigilance intake", "adverse-event cases with duplicate detection"),
            ("LIMS & trial systems", "assay and visit data under GxP validation"),
            ("supply & pharmacy chains", "lot-level traceability end to end"),
            ("patient engagement stack", "consented outreach with journey telemetry"),
        ],
        "regimes": ["HIPAA / HITECH", "GxP / GCP validation", "GDPR / privacy regimes", "FDA 21 CFR Part 11", "EU AI Act high-risk duties", "MDR device oversight"],
        "vocab": ["clinical reality", "prior authorization", "care pathways", "pharmacovigilance", "trial pre-screening", "PHI estate", "care management", "medication adherence"],
        "kctx": ["per 1,000 patients", "per care pathway", "per trial site", "per clinical unit"],
    },
    "manufacturing": {
        "name": "Manufacturing & Industrial",
        "systems": [
            ("MES layers", "work orders and genealogy per unit"),
            ("SCADA & historians", "tag-level telemetry with unified namespace"),
            ("APS planning suites", "finite-capacity schedules under constraint feeds"),
            ("CMMS maintenance", "work orders joined to failure signatures"),
            ("quality labs (LIMS/QMS)", "SPC charts and lot dispositions"),
            ("supplier portals", "inbound quality and lead-time signals"),
        ],
        "regimes": ["ISO 9001 / IATF 16949 quality", "IEC 62443 OT security", "GDPR / privacy regimes", "CE machinery directives", "REACH & materials compliance", "CSRD value-chain reporting"],
        "vocab": ["OEE uplift", "scrap & rework", "finite-capacity schedules", "changeover discipline", "plant truth", "line downtime", "quality signatures", "maintenance windows"],
        "kctx": ["per production line", "per shift", "per asset class", "per plant"],
    },
    "energy-utilities": {
        "name": "Energy & Utilities",
        "systems": [
            ("SCADA / EMS cores", "grid state under hardened OT zoning"),
            ("meter data platforms", "interval data with quality codes"),
            ("asset health registries", "condition monitoring joined to work management"),
            ("market & settlement systems", "bid stacks and imbalance accounting"),
            ("work & asset management", "field crews synchronized to network state"),
            ("weather & generation feeds", "forecast ensembles for unit commitment"),
        ],
        "regimes": ["NERC CIP standards", "EU network codes", "GDPR / privacy regimes", "NIS2 directives", "IRECS / guarantees of origin", "CSRD sustainability reporting"],
        "vocab": ["grid state", "unit commitment", "imbalance costs", "outage restoration", "asset health", "renewables curtailment", "load forecasting", "field crews"],
        "kctx": ["per feeder", "per settlement period", "per asset class", "per balancing window"],
    },
    "retail-consumer-goods": {
        "name": "Retail & Consumer Goods",
        "systems": [
            ("commerce & POS estates", "transaction streams unified across channels"),
            ("inventory & order brokers", "ATP logic with promise-quality telemetry"),
            ("demand planning suites", "SKU-location histories with promotion context"),
            ("supply chain control towers", "milestone events under exception lanes"),
            ("loyalty & CDP platforms", "consent-scoped profiles with activation logs"),
            ("trade promotion systems", "spend and lift joined per event"),
        ],
        "regimes": ["GDPR / privacy regimes", "EU GPSR product safety", "CSRD value-chain reporting", "DSA marketplace duties", "PCI-DSS card handling", "EPR packaging rules"],
        "vocab": ["fresh waste", "on-shelf availability", "markdown depth", "day-part demand", "sell-through", "promotion lift", "fulfillment promise", "assortment depth"],
        "kctx": ["per SKU-store", "per day-part", "per category", "per channel"],
    },
    "logistics-supply-chain": {
        "name": "Logistics & Supply Chain",
        "systems": [
            ("TMS execution", "loads, rates and tender events under SLAs"),
            ("WMS floor systems", "pick-path and dock telemetry in near-real-time"),
            ("visibility networks", "carrier EDI/API milestones with quality scores"),
            ("yard & gate systems", "dwell and appointment orchestration"),
            ("customs & compliance hubs", "document packs with sanction screening"),
            ("fleet telematics", "position and driver-state streams"),
        ],
        "regimes": ["GDPR / privacy regimes", "ICS/CT-PAT security filings", "IMO decarbonization rules", "CMR & carriage liability", "EPR & packaging duties", "CBAM carbon reporting"],
        "vocab": ["dwell time", "tender acceptance", "on-time-in-full", "lane discipline", "empty miles", "customs holds", "slot utilization", "milestone integrity"],
        "kctx": ["per lane", "per shipment", "per node", "per carrier"],
    },
    "telecom-media": {
        "name": "Telecom, Media & Entertainment",
        "systems": [
            ("OSS/BSS stacks", "network inventory joined to customer state"),
            ("network telemetry lakes", "cell-level KPIs under streaming ingest"),
            ("ad & audience platforms", "consent-scoped identity resolution"),
            ("content supply chains", "asset pipelines with rights metadata"),
            ("field-force management", "dispatch queues with skill matching"),
            ("billing & mediation", "usage rating with revenue-assurance checks"),
        ],
        "regimes": ["GDPR / privacy regimes", "NIS2 directives", "DSA transparency duties", "AVMS content rules", "accessibility directives", "roaming regulations"],
        "vocab": ["churn propensity", "network KPIs", "ad yield", "content velocity", "field dispatch", "spectral efficiency", "audience identity", "troubleshooting loops"],
        "kctx": ["per cell site", "per subscriber cohort", "per campaign", "per market"],
    },
    "public-sector": {
        "name": "Public Sector & Government",
        "systems": [
            ("case & benefits platforms", "entitlement workflows with decision logs"),
            ("permitting & licensing", "staged reviews with published SLAs"),
            ("records & archives", "retention-grade storage with provenance"),
            ("justice & safety systems", "warrant-scoped data sharing with audit"),
            ("tax & revenue engines", "declaration pipelines with risk scoring"),
            ("citizen contact centers", "omnichannel intake with outcome tracking"),
        ],
        "regimes": ["GDPR / privacy regimes", "WPSHR accessibility duties", "NIS2 directives", "records retention statutes", "procurement transparency rules", "AI Act high-risk duties"],
        "vocab": ["service standards", "entitlement decisions", "case backlogs", "digital letters", "interoperability layers", "public value", "transparency duties", "once-only data"],
        "kctx": ["per case file", "per service line", "per agency", "per citizen journey"],
    },
    "education-research": {
        "name": "Education & Research",
        "systems": [
            ("SIS & registries", "enrollment state with academic standing"),
            ("LMS & learning stores", "activity streams joined to outcomes"),
            ("research data platforms", "project data under DMP governance"),
            ("grants & compliance", "spend tracking with funder rules"),
            ("credentialing services", "verifiable awards with issuer identity"),
            ("library & knowledge bases", "discovery layers with usage analytics"),
        ],
        "regimes": ["GDPR / privacy regimes", "FERPA-style student privacy", "research ethics codes", "export-control rules", "accessibility directives", "funder DMP mandates"],
        "vocab": ["learning analytics", "at-risk signals", "research data plans", "credential verifiability", "enrollment funnels", "grant compliance", "study progress", "assessment integrity"],
        "kctx": ["per cohort", "per program", "per research group", "per term"],
    },
    "technology-saas": {
        "name": "Technology & SaaS",
        "systems": [
            ("product analytics", "event taxonomies with property governance"),
            ("billing & metering", "usage-rated invoicing with entitlement checks"),
            ("feature flag platforms", "progressive delivery with kill switches"),
            ("customer data stores", "consent-scoped profiles per tenant"),
            ("support & success stacks", "ticket telemetry joined to product health"),
            ("CI/CD & observability", "release markers linked to SLO burn"),
        ],
        "regimes": ["GDPR / privacy regimes", "SOC 2 / ISO 27001 controls", "SOC 2 trust criteria", "data residency clauses", "DPA / SCC transfer rules", "AI Act transparency duties"],
        "vocab": ["activation loops", "product-led growth", "tenant isolation", "usage-based pricing", "SLO burn", "feature adoption", "churn signals", "expansion motions"],
        "kctx": ["per tenant", "per feature area", "per release train", "per pricing tier"],
    },
    "agriculture-food": {
        "name": "Agriculture & Food Systems",
        "systems": [
            ("farm management systems", "field operations joined to telemetry"),
            ("traceability ledgers", "lot-level provenance from field to shelf"),
            ("commodity & trade desks", "position and hedging data under controls"),
            ("food-safety labs", "test results with lot linkage"),
            ("cold-chain telemetry", "temperature excursions with alerting"),
            ("processing line historians", "yield and quality signatures"),
        ],
        "regimes": ["EU deforestation rules", "GDPR / privacy regimes", "HACCP / food-safety law", "organic certification chains", "CGMP feed standards", "CSRD land-use reporting"],
        "vocab": ["yield per hectare", "cold-chain integrity", "lot traceability", "food-safety holds", "agrifinance exposure", "harvest windows", "sustainability claims", "processor yields"],
        "kctx": ["per field", "per lot", "per season", "per facility"],
    },
}

# ── solution topics (l2 on solution pages) ──────────────────────────────────
TOPIC_BOWLS = {
    "workforce": ["scheduling fairness", "labor compliance", "skills coverage", "shift economics"],
    "revenue": ["price realization", "elasticity capture", "margin integrity", "promotion ROI"],
    "risk": ["exposure visibility", "control effectiveness", "loss containment", "resilience posture"],
    "experience": ["journey friction", "resolution quality", "trust signals", "effort scores"],
    "operations": ["cycle-time compression", "waste removal", "throughput stability", "exception lanes"],
}

# ── clause pools ────────────────────────────────────────────────────────────
# Each pool: list of strings with {slots}. The engine picks seeded variants;
# identity nouns ({subject},{ind},{sub},{tower},{plat}) guarantee uniqueness.

P_HERO = [
    "What {subject} means at Achala IT Solutions: the scope we sign, the architecture we ship, the evidence generated in-flight, and the {kctx} outcomes measured against your audited baseline.",
    "A working definition of {subject} for {ind}: engineered controls, named owners, weekly evidence, and a signed baseline so every claim of improvement can be replayed line by line.",
    "{subject} delivered as an operating capability for {ind}, not a slide deck — durable runtime, policy-checked actions, and telemetry your auditors can read without translation.",
    "The Achala IT Solutions build of {subject}: concrete interfaces at {sys1}, measured movement on {kpi0}, and a delivery rhythm your control owners can plan around from week one.",
    "How {subject} runs when it is engineered for {ind}: bounded scope per gate, platform evidence generated in-flight, and outcomes stated as deltas against the number we signed together.",
    "{subject} in production terms — the runtime that holds it, the policies that bound it, the dashboards that prove it, and the quarterly delta your finance team can bank.",
    "A no-theater description of {subject}: what ships first, what it touches at {sys2}, how it is verified, and the {kctx} metric we commit to moving against baseline.",
    "The contract behind {subject}: signed baseline in week two, working slice by week eight, industrialized controls by week twelve, and evidence flowing to your control owner throughout.",
]

P_OV1A = [
    "Most {subject} programs fail the same way: a pilot that impresses on a demo dataset and then dissolves when it meets {sys1}, exception handling and audit. We start from the production seams instead — the queues, the exception lanes, the reconciliation breaks — and engineer those first.",
    "The economics of {subject} flipped in the last two years: runtimes got durable, evaluation became routine, and orchestration frameworks matured into something you can run under change control. What separates winners now is integration discipline — how cleanly the capability plugs into {sys1} without inventing a shadow estate.",
    "Every serious {subject} effort hits the same wall: the distance between a promising model or agent and a system your control owners will sign. We close that distance with policy-checked actions, evidence generated in-flight, and gates that stop the program when a metric regresses — which is exactly why ours rarely do.",
    "{subject} earns its budget only when it changes a number on someone's scorecard. So we invert the usual sequence: lock the metric and its baseline first, then work backwards to the smallest architecture that moves it — usually composed from {sys1} and the tower platform rather than built from scratch.",
    "There is a reason {subject} pilots stall between demo and production: nobody owns the seam between the clever part and the operational estate. Our builds assign that seam a named owner from day one, wrap it in contracts and telemetry, and make the first quarter produce artifacts — not slideware.",
    "The hidden cost of {subject} is never the model; it is the scaffolding — data contracts, evaluation harnesses, rollback machinery, audit evidence. We price and build that scaffolding explicitly, on {sys1}, because that is where programs actually succeed or die.",
]

P_OV1B = [
    "In {ind} the constraints are structural, not cosmetic: {reg1} shapes what data may move, {vocab0} dominates the economics, and any capability that cannot explain its own decisions will be switched off by risk committees. The architecture reflects all three from the first commit.",
    "For {ind}, the design tension is specific — {vocab0} on one side, {reg1} on the other, and a control environment that must survive both internal audit and external inspection. We build for that tension explicitly rather than discovering it at gate review.",
    "The {ind} operating reality gives this work its shape: {vocab0} pressure at event speed, {reg1} obligations on every artifact, and practitioners who will not accept recommendations they cannot interrogate. The pattern below is calibrated to those three forces.",
    "{ind} punishes generic deployments. {vocab0} moves faster than batch cycles, {reg1} demands evidence chains most tools cannot produce, and the estate is heterogeneous — which is why every engagement starts with the seams named above rather than a platform-first rollout.",
    "What makes {ind} different is not the math; it is the operating context: {reg1} governs the data, {vocab0} governs the economics, and the people accountable for outcomes answer to regulators as well as customers. Every design choice below is downstream of that context.",
]

P_ARCH = [
    "The reference architecture separates concerns so each plane can evolve independently: signals land through contracts, the core reasons over governed state, and every outward action passes a policy check with a signed audit trail. Nothing crosses a boundary without an owner and a metric.",
    "Structurally, the build is three planes and a spine — workload, decision, evidence, with {plat} carrying the spine. The decision plane never touches raw sources directly; the evidence plane records what was known at decision time, which is what makes the whole thing defensible in audit.",
    "We keep the topology boring on purpose: explicit stages, typed interfaces, no hidden couplings. Each stage owns a latency budget and a failure policy, so when something degrades you know exactly where — and the {plat} control plane shows it in one view.",
    "The diagram is not decoration — it is the deployment map. Lanes correspond to Kubernetes namespaces and IAM boundaries; the flows correspond to streaming topics and API contracts; the gates correspond to release checks your change board will recognize.",
    "Every arrow in the schematic is a contract with an SLO, and every box is a service with a named owner. That is deliberate: the fastest way to lose a {subject} program is an architecture nobody can draw from memory.",
]

P_ARCH2 = [
    "Two properties do the heavy lifting. First, evidence is generated in-flight — approvals, evaluations and decision context are captured as the work happens, so audit prep is an export, not an archaeology project. Second, every state change is replayable: from the signed baseline you can re-derive any number the program reports.",
    "The pattern is engineered for change: models, agents and rules are versioned artifacts, environments are stamped, and rollback is a rehearsed operation rather than a hope. When a release regresses its eval gate, the canary cohort falls back in minutes — the incident blast radius is a cohort, not the estate.",
    "Resilience is structural. Durable execution means work resumes after crashes and deploys; idempotent semantics mean retries never double-commit; policy gates mean high-risk paths degrade to human review instead of failing open. Boring properties, deliberate choices, program-saving consequences.",
    "What makes the fabric auditable is that trust is computed, not asserted: identities are short-lived, decisions carry their policy inputs, and ledgers are hash-linked where counterparties share them. The result is a system that answers 'how do you know?' with a pointer instead of a paragraph.",
]

P_WHY = [
    "In {ind}, {subject} pays for itself where the seam is busiest: {vocab0}. That is where we instrument first, because a percentage point there compounds across every upstream process that feeds it.",
    "The attack surface for {subject} in {ind} is specific — {vocab0} pressure points that show up as queue depth, exception rates and reconciliation breaks. The bullets below are the ones we hear most from operators, phrased the way they say them.",
    "Operators in {ind} do not need convincing that {subject} matters; they need proof it will hold under {vocab0} pressure at quarter close. The sections below are organized around exactly that proof: what breaks today, what we deploy, and what number moves.",
    "For {ind} the priority is {vocab0}: the metric most exposed to regulatory scrutiny and most sensitive to operational drift. Everything in this pattern — scope, cadence, controls — is tuned to move that metric first and let the rest follow.",
]

P_DELIVER = [
    "Delivery composes proven services rather than bespoke heroics: the pattern below draws on {svc_count} services from the {tower} tower, each with its own runbook, so your team inherits something maintained — not a one-off.",
    "The build sequence is deliberate: contracts and identity first, the working decision slice second, the verification harness third — because a {subject} capability without its eval gate is just another unattended automation.",
    "We deliver in bounded slices with gates that bind. Each slice ends with evidence to your control owner: measured delta, updated runbooks, and a go/no-go decision recorded in the program ledger. The slice either earns the next one or it stops.",
    "Under the hood the pattern is a composition, not a monolith: {svc_count} tower services, the {plat} platform for rails, and your estate at {sys1} for truth. Every boundary is a contract; every contract has an SLO and an owner.",
    "Execution follows the Achala Method: two weeks to a signed baseline, six to the first working slice on live data at bounded scope, four more to industrialize — runbooks, monitoring, enablement — with the measured delta reviewed at each gate.",
]

P_CADENCE0 = [
    "The rhythm is engineered, not ritual:",
    "The operating cadence, concretely:",
    "What the delivery actually looks like week to week:",
    "The cadence, without the ceremony:",
    "Here is the working rhythm, stated so you can hold us to it:",
]

P_CADENCE1 = [
    "weeks {w1a}–{w1b} lock the baseline with your team: the metric, its measurement method and its owner, all signed before a line of build code ships",
    "the first {w1d} weeks are pure verification — we measure {kpi0} with your analysts, reconcile disagreements, and freeze the number both sides defend",
    "weeks {w1a}–{w1b} produce the signed baseline: current {kctx0} performance, method note, and a control owner who co-signs every later claim",
    "before any build work, we spend {w1d} weeks proving the measurement: if two analysts cannot reproduce {kpi0} the same way, nothing else starts",
]

P_CADENCE2 = [
    "weeks {w2a}–{w2b} deliver the pilot on bounded scope — one decision path, one workflow, one {scope_noun} — with evidence to your control owner weekly",
    "the middle block runs the pilot against live {sys2} data at deliberately small scope: one path, one team, one {scope_noun}, expanded only after its eval gate holds",
    "from week {w2a} the working slice goes live at {scope_noun} scope: shadow first, then canary, then promoted cohorts — each promotion justified by the eval gate, not enthusiasm",
    "the pilot block (weeks {w2a}–{w2b}) ships one complete path end to end, on real traffic, with rollback rehearsed — bounded scope is a feature, not a limitation",
]

P_CADENCE3 = [
    "weeks {w3a}–{w3b} industrialize: runbooks, monitoring, enablement and the measured delta against the signed baseline, reviewed at a gate your steering committee attends",
    "the closing block hardens the capability: runbooks handed to your operators, alerting wired to your channels, and the delta versus baseline reported with method notes attached",
    "the last {w3d} weeks convert pilot to product — monitoring, runbooks, enablement sessions, chargeback wiring — and the gate reviews the measured delta, not a demo",
    "industrialization (weeks {w3a}–{w3b}) is where most vendors stop; we treat it as the deliverable: your team runs it, our evidence pack survives your auditor, and the delta is signed",
]

P_CADENCE4 = [
    "Gates are binding: miss one and the program stops or redirects with a documented decision — that is the point of signing baselines.",
    "Gates bind in both directions: we stop on regression, you fund on evidence, and every gate decision lands in the program ledger with its reasoning.",
    "Miss a gate and the work pauses — with a written decision, not a quiet scope change. That discipline is why our deltas survive audit.",
    "Each gate can end the program, redirect it, or release the next slice — decided on the signed numbers, recorded in the ledger, no exceptions.",
]

P_RECEIVE_P = [
    "Artifacts, not anecdotes — at the first-quarter close your team holds:",
    "The first quarter ends with named artifacts in your estate, each walked through live with your control owners:",
    "What changes hands at quarter close, with a guided walkthrough per item:",
    "You receive the following at gate three — each artifact versioned, owned and stored in your repositories:",
    "The quarter-close package, built to be handed over rather than demonstrated:",
]

P_PORTFOLIO = [
    "No capability ships alone: the links below are the compositions this {tpl_noun} most often travels with, chosen by observed delivery patterns rather than menu logic.",
    "This {tpl_noun} is one move in a larger program — the adjacent pages below are where clients typically go next, ordered by how often they appear in the same delivery plan.",
    "In delivery this work composes with the capabilities listed below; each link is a pattern we have run alongside it, with the interface between them already designed.",
    "The strongest results come from composition: the {tpl_noun}s below share data contracts, identity fabric or control lanes with this one, which is why they co-occur in our delivery plans.",
    "Where this sits in the portfolio: the pages below are the compositions that most often share its contracts and cadence — a good next click if you are mapping a program.",
]

P_CTA = [
    "Put your {kpi0} in front of the practice lead — bring the baseline, leave with a scoped plan.",
    "Book a working session with the {tower} practice: your metric, our reference architecture, a scoped first slice.",
    "Bring the audited baseline; we will show the pattern on your numbers and scope the first slice in the same session.",
    "Take this pattern to a briefing with your baseline — the first meeting ends with a measurement plan, not a proposal document.",
    "Start with a value assessment: two weeks, your {kpi0} measured and signed, a delivery plan priced from evidence.",
    "Talk to the team that runs this pattern in {ind} — the briefing is technical by design, and the baseline is yours to keep either way.",
]

P_STACK_NOTE = [
    "The stack is boring by design — proven components, no experimental dependencies:",
    "Under the hood, chosen for operability rather than novelty:",
    "The engineering substrate, as deployed in current programs:",
    "Standards we hold the build to, component by component:",
]

P_TELEM_NOTE = [
    "The program dashboard tracks these by default, wired to your channels:",
    "Telemetry your control owner sees weekly — the same numbers at every gate:",
    "The measures that decide gate outcomes, generated in-flight:",
    "What we watch so you do not have to ask:",
]

P_FAIL_NOTE = [
    "Failure modes we design against, with the guard shipped for each:",
    "The ways programs like this die — and the guard we ship against each:",
    "Known failure modes, engineered out at the architecture level:",
    "What usually goes wrong, and the specific guard in this build:",
]

# section titles (stable TOC anchors)
H_ARCH = "Reference architecture"
H_STACK = "Engineering standards & stack"
H_INTG = "Integration surface"
H_TELEM = "Operational telemetry"
H_FAIL = "Failure modes & the guards we ship"
