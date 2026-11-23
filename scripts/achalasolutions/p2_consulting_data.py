"""dqs_data_consulting — the new Consulting section: 13 IT consulting &
engineering services, each with deep technical content, toolchains, named
methods and its own architecture graph.
"""

C = []

C.append(dict(
    slug="data-migration", name="Data Migration & Platform Moves",
    promise="Move estates without losing a row, an audit trail or a night's sleep.",
    overview=[
        "Data migration fails in the planning, not the pipeline. Estates that look simple on a slide hold decades of undocumented logic: spreadsheets that became systems, triggers nobody owns, and reference data that three applications interpret three different ways. We start every migration with discovery that reads the estate the way the estate actually behaves — dependency mapping at column level, profile-driven data quality baselines, and a reconciliation contract agreed before anything moves.",
        "Execution runs in waves with reversible cutovers: each wave carries its own rehearsal, row-level reconciliation (counts, sums, spot business keys, hashed payloads), and a rollback plan your operations team has already rehearsed. Cutover decisions are made against pre-agreed evidence — reconciliation deltas, latency budgets, dual-run comparisons — never against a date on a program charter.",
    ],
    method=[
        ("Discovery & dependency mapping", "Column-level lineage across every source; undocumented logic surfaced and priced"),
        ("Target architecture & contracts", "Schema contracts, quality rules and reconciliation math agreed with owners"),
        ("Wave rehearsal", "Full-volume dry runs in isolated lanes with timed cutovers"),
        ("Execution & reconciliation", "Row-level checks at every boundary; deltas explained, not accepted"),
        ("Cutover & stabilization", "Reversible cutovers, hypercare war-room, decommission with archival"),
    ],
    tools=[
        ("Movement", ["Azure Data Factory / SSIS", "AWS DMS & Glue", "Kafka Connect", "Informatica / Talend", "Custom CDC frameworks"]),
        ("Assurance", ["Great Expectations / dbt tests", "Row-hash reconciliation harnesses", "Collibra / Purview lineage", "Dual-run comparators"]),
    ],
    deliverables=[
        "Dependency map & migration blueprint (column-level)",
        "Reconciliation contract with signed thresholds",
        "Wave plan with rehearsed cutovers and rollback drills",
        "Hypercare runbook with named owners",
        "Decommission & archival plan for the old estate",
    ],
    arch_lanes=["Source estate", "Discovery & contracts", "Migration lanes", "Reconciliation", "Target platform"],
    arch_nodes=[
        ("src", 0, "Legacy databases & files", True), ("src", 0, "SaaS & flat-file estates"),
        ("dc", 1, "Column-level lineage", True), ("dc", 1, "Quality baseline"),
        ("ml", 2, "Wave pipelines (CDC + batch)", True), ("ml", 2, "Transformation codegen"),
        ("rc", 3, "Row-hash reconciliation", True), ("rc", 3, "Dual-run comparator"),
        ("tp", 4, "Azure / Databricks / Snowflake target", True), ("tp", 4, "Archival & decommission"),
    ],
    arch_edges=[("src0","dc0"),("src1","dc1"),("dc0","ml0"),("dc1","ml1"),("ml0","rc0"),("ml1","rc1"),("rc0","tp0"),("rc1","tp1")],
    focus=["banking", "insurance", "healthcare", "manufacturing", "public-sector", "retail"],
))

C.append(dict(
    slug="software-development", name="Software Development & Engineering Pods",
    promise="Product-grade engineering pods that ship into your controls, not around them.",
    overview=[
        "Our engineering pods build the systems the business actually runs on: transactional platforms, customer portals, integration fabrics and the internal tools operations depends on. Pods arrive with a delivery system, not just developers — trunk-based development, contract-tested APIs, progressive delivery and evidence-producing pipelines are the default, because software that cannot be audited is a liability no matter how well it demos.",
        "Every pod embeds against your controls from sprint one: identity and secrets follow your standards, environments are provisioned as code, and the definition of done includes the evidence your auditors will later ask for. The same pod model scales from a six-person feature team to a fifty-person platform rebuild without changing the delivery mechanics.",
    ],
    method=[
        ("Discovery & architecture baseline", "Domain mapping, ADRs, and the non-negotiable controls written down"),
        ("Pod assembly", "Named engineers, named owner, delivery system provisioned in week one"),
        ("Trunk-based delivery", "Two-week increments behind flags; contract tests at every boundary"),
        ("Hardening & progressive release", "Load, chaos and security gates before exposure widens"),
        ("Handover & enablement", "Runbooks, walkthroughs, and a team that can run it without us"),
    ],
    tools=[
        ("Engineering", ["TypeScript / Java / Python / .NET", "React & Next.js front ends", "Kubernetes & serverless runtimes", "Event-driven architectures (Kafka)"]),
        ("Delivery", ["GitHub Actions / Azure DevOps", "Contract tests (Pact)", "Progressive delivery (Argo)", "Snyk & dependency governance"]),
    ],
    deliverables=[
        "Architecture baseline with ADRs",
        "Working software in production increments",
        "Pipeline with quality, security and evidence gates",
        "Runbooks, walkthroughs and enablement sessions",
        "Cost and observability telemetry wired from day one",
    ],
    arch_lanes=["Product & stakeholders", "Delivery system", "Service architecture", "Quality gates", "Production"],
    arch_nodes=[
        ("ps", 0, "Product backlog", ), ("ps", 0, "Architecture decisions (ADR)"),
        ("ds", 1, "Trunk-based CI/CD", True), ("ds", 1, "IaC environments"),
        ("sa", 2, "Domain services & APIs", True), ("sa", 2, "Event streams"),
        ("qg", 3, "Contract & load tests", True), ("qg", 3, "Security scans"),
        ("pr", 4, "Progressive rollout", True), ("pr", 4, "Observability & SLOs"),
    ],
    arch_edges=[("ps0","ds0"),("ps1","ds0"),("ds0","sa0"),("ds1","sa1"),("sa0","qg0"),("sa1","qg1"),("qg0","pr0"),("qg1","pr1")],
    focus=["technology", "banking", "retail", "healthcare", "manufacturing", "telecom"],
))

C.append(dict(
    slug="testing-qa", name="Testing & Quality Engineering",
    promise="Quality engineered in — measurable coverage, honest gate criteria, fewer escapes.",
    overview=[
        "Testing is not a phase; it is the evidence system for delivery. We build quality engineering functions that prove what works and find what does not: risk-based test strategies tied to real failure data, automation pyramids that run in minutes instead of nights, and performance models that simulate production load rather than guessing at it. Escapes are analyzed to the root, and every analysis changes a gate.",
        "For AI systems, testing extends beyond deterministic checks: evaluation sets with human-labeled ground truth, adversarial suites, drift monitors and bias probes become part of the same gate machinery. The output is a quality signal leadership can read — escape rate, coverage of risk, time-to-feedback — rather than a pass percentage nobody trusts.",
    ],
    method=[
        ("Quality baseline & risk map", "Escapes, hotspots and the cost of poor quality made visible"),
        ("Strategy & automation pyramid", "Unit / contract / E2E balance tuned to the estate"),
        ("Performance & resilience", "Load models from production traces; chaos scenarios authored"),
        ("AI evaluation harnesses", "Ground-truth sets, adversarial suites, drift and bias monitors"),
        ("Gate operation & improvement", "Quality signal reported weekly; escapes feed the gates"),
    ],
    tools=[
        ("Automation", ["Playwright / Cypress", "pytest / JUnit", "k6 & JMeter performance", "Contract tests (Pact)"]),
        ("AI quality", ["Custom eval harnesses", "Adversarial & bias suites", "Drift monitors", "Human-label pipelines"]),
    ],
    deliverables=[
        "Risk-based test strategy with escape analysis",
        "Automation suite running in minutes, in your CI",
        "Performance & resilience scenario library",
        "AI evaluation harness with signed ground truth",
        "Weekly quality signal for leadership",
    ],
    arch_lanes=["Delivery flow", "Test layers", "Environments", "AI evaluation", "Quality signal"],
    arch_nodes=[
        ("df", 0, "Build & deploy pipeline"),
        ("tl", 1, "Unit & contract layers", True), ("tl", 1, "E2E journeys"),
        ("ev", 2, "Production-like environments"),
        ("ai", 3, "Eval sets & adversarial suites", True), ("ai", 3, "Drift & bias monitors"),
        ("qs", 4, "Escape-rate & coverage signal", True),
    ],
    arch_edges=[("df0","tl0"),("df0","tl1"),("tl0","ev0"),("tl1","ai0"),("ai0","ai1"),("ai1","qs0"),("tl0","qs0")],
    focus=["technology", "banking", "healthcare", "retail", "telecom", "manufacturing"],
))

C.append(dict(
    slug="application-services", name="Application Services & Modernization",
    promise="Keep the applications that earn their keep; retire the ones that only cost.",
    overview=[
        "Every estate carries a portfolio, not an application: some systems earn their keep, some hold critical logic nobody understands, and some only cost. We start with a portfolio triage — business value against technical debt — and give each application a disposition: invest, modernize, encapsulate, or retire. Modernization then runs incrementally: strangler patterns around monoliths, contract-first extraction of services, and data uncoupled from application lifecycles so neither migration blocks the other.",
        "Run-state matters as much as build-state. Modernized applications land with observability, cost telemetry and support models defined — because an application that cannot be observed, costed and supported safely has not been modernized; it has been relocated.",
    ],
    method=[
        ("Portfolio triage", "Value-vs-debt scoring; disposition per application, signed with owners"),
        ("Encapsulation first", "APIs and anti-corruption layers around what must stay"),
        ("Incremental modernization", "Strangler patterns; data decoupled from code lifecycles"),
        ("Run-state engineering", "Observability, cost telemetry and support models as deliverables"),
        ("Retirement & simplification", "Decommission with archival; complexity removed, not moved"),
    ],
    tools=[
        ("Modernization", ["Strangler patterns & API facades", "Event interception", "Azure AppCAT assessments", "Containerization (AKS/EKS)"]),
        ("Run state", ["OpenTelemetry estates", "SLO frameworks", "FinOps tooling", "ITSM integration (ServiceNow)"]),
    ],
    deliverables=[
        "Portfolio disposition map with owners",
        "Encapsulation & modernization blueprint",
        "Modernized services in production increments",
        "Run-state pack: observability, cost, support",
        "Retirement schedule with archival",
    ],
    arch_lanes=["Legacy estate", "Encapsulation", "New services", "Shared data", "Run state"],
    arch_nodes=[
        ("le", 0, "Monoliths & legacy apps", True), ("le", 0, "Vendor packages"),
        ("en", 1, "API facades & ACLs", True),
        ("ns", 2, "Extracted domain services", True), ("ns", 2, "New build services"),
        ("sd", 3, "Decoupled data platform", True),
        ("rs", 4, "Observability & cost telemetry", True),
    ],
    arch_edges=[("le0","en0"),("le1","en0"),("en0","ns0"),("en0","ns1"),("ns0","sd0"),("ns1","sd0"),("ns0","rs0"),("le0","rs0")],
    focus=["banking", "insurance", "manufacturing", "retail", "public-sector", "healthcare"],
))

C.append(dict(
    slug="ui-ux-design", name="UI/UX Design & Product Experience",
    promise="Interfaces your customers finish — designed from evidence, built for accessibility.",
    overview=[
        "Experience work at Achala IT Solutions starts with evidence: session analytics, support tickets, task-completion data and field research, not opinions in a conference room. We design journeys around the jobs users are actually trying to finish, prototype in code where it matters, and test with real users before a single component is committed to the design system.",
        "Accessibility is an engineering requirement, not a compliance annex — WCAG 2.2 AA is the floor, verified in CI with automated checks and assistive-technology test passes. Design systems we deliver ship as versioned component libraries with usage guidance, so the hundredth screen is as considered as the first.",
    ],
    method=[
        ("Evidence base", "Analytics, ticket mining and task-completion studies"),
        ("Journey & service design", "Journeys mapped to jobs; service blueprints for cross-channel flows"),
        ("Design system engineering", "Versioned component library with tokens and documentation"),
        ("Prototype & validate", "Code prototypes tested with real users on real tasks"),
        ("Accessibility verification", "WCAG 2.2 AA in CI; AT test passes with real users"),
    ],
    tools=[
        ("Design", ["Figma systems & tokens", "Storybook component libraries", "Journey & service blueprints", "Maze / UserTesting research ops"]),
        ("Verification", ["axe-core in CI", "NVDA / VoiceOver test passes", "Core Web Vitals budgets", "Analytics-driven iteration"]),
    ],
    deliverables=[
        "Evidence base & journey blueprints",
        "Design system as versioned code",
        "Tested, accessible front-end components",
        "Research ops playbook for continuous discovery",
        "Accessibility conformance evidence",
    ],
    arch_lanes=["Evidence", "Design", "System", "Verification", "Users"],
    arch_nodes=[
        ("ev", 0, "Analytics & ticket mining", True), ("ev", 0, "Field research"),
        ("dj", 1, "Journeys & blueprints"),
        ("dsg", 2, "Design system in code", True), ("dsg", 2, "Tokens & patterns"),
        ("vr", 3, "WCAG 2.2 AA in CI", True), ("vr", 3, "AT & user test passes"),
        ("us", 4, "Web & mobile users"), ("usb", 4, "Support & training"),
    ],
    arch_edges=[("ev0","dj0"),("ev1","dj0"),("dj0","dsg0"),("dsg0","vr0"),("dsg1","vr1"),("vr0","us0"),("dsg0","us1")],
    focus=["retail", "banking", "telecom", "healthcare", "public-sector", "technology"],
))

C.append(dict(
    slug="it-services", name="IT Services & Managed Operations",
    promise="Operations with named owners, measured SLAs and a cost line you can read.",
    overview=[
        "Managed operations fail when nobody owns the outcome. Our IT services model assigns a named service owner per tower of your estate, publishes the SLA and the evidence behind it monthly, and instruments the cost per service so budget conversations happen with numbers instead of anecdotes. Runbooks are engineered artifacts — versioned, tested and rehearsed — not wiki pages.",
        "The operating rhythm is deliberately boring: change flows through managed windows with evidence, incidents carry blameless reviews that change the runbook, and capacity is planned against measured demand. The result is an estate that behaves the same on day 700 as it did on day one — at a unit cost that trends down, not up.",
    ],
    method=[
        ("Estate baseline & catalog", "Service catalog with owners, SLAs and cost per service"),
        ("Runbook engineering", "Versioned, tested runbooks; drills before live operations"),
        ("Managed operations", "Named owner per service tower; monthly evidence packs"),
        ("Continual improvement", "Blameless incident reviews that change the runbook"),
        ("Capacity & cost discipline", "Demand-measured capacity; unit-cost trends reported"),
    ],
    tools=[
        ("Operations", ["ServiceNow / Jira SM", "Observability stacks (OTel, Grafana)", "AIOps alert correlation", "Capacity models"]),
        ("Assurance", ["SLA evidence automation", "Change advisory integration", "Backup & DR drills", "Cost-per-service telemetry"]),
    ],
    deliverables=[
        "Service catalog with named owners and SLAs",
        "Engineered runbook library with drills",
        "Monthly SLA & cost evidence packs",
        "Incident review program with runbook updates",
        "Capacity & unit-cost trend reporting",
    ],
    arch_lanes=["Estate", "Intake", "Operations core", "Evidence", "Business"],
    arch_nodes=[
        ("es", 0, "Applications & infrastructure", True),
        ("in", 1, "Service desk & requests"), ("in", 1, "Monitoring & alerts"),
        ("oc", 2, "Runbook-driven operations", True), ("oc", 2, "Change management"),
        ("evd", 3, "SLA evidence automation", True), ("evd", 3, "Cost per service"),
        ("bs", 4, "Business service reviews"), ("bsb", 4, "Budget owners"),
    ],
    arch_edges=[("es0","in0"),("es0","in1"),("in0","oc0"),("in1","oc1"),("oc0","evd0"),("oc1","evd1"),("evd0","bs0"),("evd1","bsb")],
    focus=["banking", "insurance", "healthcare", "public-sector", "manufacturing", "retail"],
))

C.append(dict(
    slug="data-analytics", name="Data Analytics & Decision Products",
    promise="From dashboards people tolerate to decisions people trust.",
    overview=[
        "Most analytics estates produce dashboards and call it insight. We build the layer beneath: certified metric definitions with owners, semantic models that answer questions the same way every time, and decision products that push the answer into the workflow where the decision happens. Analysis is engineered for reuse — one governed definition per metric, tested like code, served wherever it is needed.",
        "The analytics stack we deliver spans executive reporting, embedded analytics in product surfaces, and the feature stores that feed real-time models — all on one governance fabric, so the number in the board deck, the number in the app, and the number in the model agree.",
    ],
    method=[
        ("Metric & decision inventory", "The decisions that matter and the metrics they consume, named"),
        ("Semantic layer engineering", "Certified definitions, tested in CI, versioned like code"),
        ("Product build", "Executive BI, embedded analytics and alerting as products"),
        ("Real-time serving", "Feature stores and streaming metrics for live decisions"),
        ("Adoption & measurement", "Usage instrumentation; decisions traced to outcomes"),
    ],
    tools=[
        ("Analytics", ["Databricks / Snowflake", "dbt semantic layer", "Power BI / Tableau / Looker", "Feature stores (Feast/Databricks)"]),
        ("Governance", ["Column-level lineage", "Data contracts", "Metric certification workflows", "Catalogs (Purview/Collibra)"]),
    ],
    deliverables=[
        "Certified metric layer with owners",
        "Executive & embedded analytics products",
        "Real-time feature & metric serving",
        "Decision-outcome tracing for key metrics",
        "Governance fabric: lineage, contracts, catalog",
    ],
    arch_lanes=["Sources", "Modeling", "Certified layer", "Serving", "Decisions"],
    arch_nodes=[
        ("so", 0, "Operational estates", True),
        ("mo", 1, "dbt transformation graph", True), ("mo", 1, "Streaming aggregations"),
        ("cl", 2, "Certified metric layer", True), ("cl", 2, "Semantic models"),
        ("sv", 3, "Executive BI"), ("sv", 3, "Embedded & API serving", True),
        ("dc", 4, "Workflow decisions", True), ("dcb", 4, "Executive review"),
    ],
    arch_edges=[("so0","mo0"),("so0","mo1"),("mo0","cl0"),("mo1","cl1"),("cl0","sv0"),("cl1","sv1"),("sv0","dc0"),("sv1","dcb")],
    focus=["banking", "retail", "insurance", "healthcare", "telecom", "manufacturing"],
))

C.append(dict(
    slug="digital-transformation", name="Digital Transformation Programs",
    promise="Transformation that changes the operating model, not just the org chart font.",
    overview=[
        "Transformation programs fail at the seam between strategy and operations. We run them from both ends: the strategy end sequences a portfolio against the P&L with funding gates that can stop a program, and the operations end engineers the delivery system — platforms, pods, evidence cadence — that turns decisions into production systems. Between the two sits an operating model that names who decides what, at which gate, with which evidence.",
        "The program instrument panel is the difference: a value ledger signed with finance, gate-by-gate deltas against baselines, and a capability maturity view that shows what the organization can absorb next. Transformation that cannot show its ledger is a reorg with better branding.",
    ],
    method=[
        ("Value-mapping sprint", "Portfolio scored on value density, readiness and absorption"),
        ("Operating model design", "Decision rights, platform teams, control ownership mapped"),
        ("Delivery system build", "Platforms, pods and evidence cadence stood up"),
        ("Sequenced execution", "Waves with funding gates and falsifiable criteria"),
        ("Capability compounding", "Enablement and maturity tracks that outlive the program"),
    ],
    tools=[
        ("Program", ["Value ledger frameworks", "Gate & baseline tooling", "OKR-to-gate traceability", "Portfolio dashboards"]),
        ("Change", ["Capability academies", "Champion networks", "Communication cadences", "Adoption analytics"]),
    ],
    deliverables=[
        "Sequenced transformation roadmap with funding gates",
        "Target operating model with named decision rights",
        "Working delivery system on your first wave",
        "Value ledger signed with finance",
        "Capability academy for your teams",
    ],
    arch_lanes=["Strategy", "Portfolio", "Delivery system", "Evidence", "Organization"],
    arch_nodes=[
        ("st", 0, "Strategy & P&L anchors", True),
        ("pf", 1, "Sequenced portfolio", True), ("pf", 1, "Funding gates"),
        ("dl", 2, "Platforms & pods", True), ("dl", 2, "Evidence cadence"),
        ("vl", 3, "Value ledger", True), ("vlb", 3, "Gate deltas"),
        ("og", 4, "Capability academy"), ("ogb", 4, "Operating model"),
    ],
    arch_edges=[("st0","pf0"),("st0","pf1"),("pf0","dl0"),("pf1","dl1"),("dl0","vl0"),("dl1","vlb"),("vl0","og0"),("dl1","ogb")],
    focus=["banking", "insurance", "manufacturing", "retail", "public-sector", "telecom"],
))

C.append(dict(
    slug="it-consulting-outsourcing", name="IT Consulting & Managed Capacity",
    promise="Senior capacity with accountability — scoped, governed and measurable.",
    overview=[
        "Staff augmentation fails when the client carries all the management overhead. Our consulting and capacity model delivers senior engineers, architects and program leads inside a governed structure: named engagements with outcomes, a delivery lead accountable for the whole team, and knowledge transfer engineered into the rhythm rather than promised at the end. You buy outcomes and accountability; we carry the management load.",
        "Capacity flexes by quarter against measured demand — scaling pods up and down without renegotiating quality, because the delivery system (methods, runbooks, evidence) stays constant regardless of team size. Every engagement carries the same gate discipline as a full build.",
    ],
    method=[
        ("Scoped engagement design", "Outcomes, gates and team shape agreed in writing"),
        ("Senior team assembly", "Named people, verified delivery records, one accountable lead"),
        ("Governed delivery", "Gates, baselines and evidence from week one"),
        ("Knowledge transfer loop", "Pairing, walkthroughs and documentation as standing practice"),
        ("Quarterly flex", "Capacity moved against measured demand"),
    ],
    tools=[
        ("Capacity", ["Senior architect & lead bench", "Engineering pods", "Program office", "Specialist practices (AI, data, security)"]),
        ("Governance", ["Outcome-gated SOWs", "Evidence dashboards", "Knowledge-transfer playbooks", "Quarterly flex reviews"]),
    ],
    deliverables=[
        "Scoped statement of work with outcome gates",
        "Named senior team with accountable lead",
        "Delivery evidence from week one",
        "Knowledge-transfer artifacts and sessions",
        "Quarterly capacity plan tied to demand",
    ],
    arch_lanes=["Your estate", "Engagement frame", "Senior capacity", "Evidence", "Your teams"],
    arch_nodes=[
        ("ye", 0, "Programs & platforms", True),
        ("ef", 1, "Outcome-gated scope", True), ("ef", 1, "Governance frame"),
        ("sc", 2, "Senior architects & pods", True), ("sc", 2, "Specialist practices"),
        ("evd", 3, "Gate evidence", True),
        ("kt", 4, "Pairing & walkthroughs"), ("ktb", 4, "Enabled owners"),
    ],
    arch_edges=[("ye0","ef0"),("ef0","sc0"),("ef1","sc1"),("sc0","evd0"),("sc1","evd0"),("sc0","kt0"),("evd0","ktb"),("kt0","ktb")],
    focus=["banking", "insurance", "technology", "healthcare", "public-sector", "retail"],
))

C.append(dict(
    slug="it-support", name="IT Support & End-User Services",
    promise="Support that measures resolution, not tickets closed.",
    overview=[
        "Support metrics that count tickets hide the truth. We run end-user services against outcomes: time-to-resolution by business impact, first-contact quality, and the avoidance curve — how many tickets never happen because the underlying cause was engineered out. Knowledge is managed as a product, with articles tested against real incidents and retired when they stop earning their place.",
        "The support estate we deliver blends human tiers with governed automation: agents work with grounded assistants that cite the runbook, password and access flows run self-service with full audit, and field services dispatch against measured demand. Escalation paths are designed, and the feedback loop into engineering closes the causes, not just the tickets.",
    ],
    method=[
        ("Outcome baseline", "TTR by impact, avoidance rate, first-contact quality"),
        ("Knowledge as product", "Tested article library wired into the assistant"),
        ("Tiered operation", "Human tiers with grounded AI assist; self-service flows"),
        ("Proactive avoidance", "Cause analytics fed to engineering; drills for major incidents"),
        ("Executive signal", "Monthly outcome pack for business owners"),
    ],
    tools=[
        ("Service", ["ServiceNow / Jira SM", "Grounded AI assistant", "Self-service password & access", "Field dispatch"]),
        ("Quality", ["CSAT & resolution analytics", "Knowledge testing", "Major-incident drills", "Cause-to-engineering loop"]),
    ],
    deliverables=[
        "Outcome-based support model with named owner",
        "Tested knowledge library + grounded assistant",
        "Self-service flows with full audit",
        "Avoidance program with engineering loop",
        "Monthly outcome pack for business owners",
    ],
    arch_lanes=["Users", "Intake", "Resolution", "Knowledge", "Prevention"],
    arch_nodes=[
        ("us", 0, "Employees & field staff", True),
        ("in", 1, "Omnichannel intake"), ("in", 1, "Self-service flows", True),
        ("re", 2, "Tiered resolution", True), ("re", 2, "AI assist with citations", True),
        ("kn", 3, "Tested knowledge library", True),
        ("pv", 4, "Cause analytics → engineering", True),
    ],
    arch_edges=[("us0","in0"),("us0","in1"),("in0","re0"),("in1","re1"),("re0","kn0"),("kn0","re1"),("re0","pv0"),("pv0","in1")],
    focus=["banking", "healthcare", "manufacturing", "retail", "public-sector", "technology"],
))

C.append(dict(
    slug="cybersecurity", name="Cybersecurity Consulting & Zero-Trust",
    promise="Security architecture that survives audit and attack — in that order, on the same day.",
    overview=[
        "Security consulting that ends in a binder is a liability with better fonts. We deliver controls in production: identity-first architecture with phishing-resistant MFA and workload identity, network segmentation priced against blast radius, and detection tuned to the attacks your sector actually faces. Every control ships with its evidence path — who tested it, when, against what scenario — so the audit reads the system, not the paperwork.",
        "The consulting layer covers what architecture alone cannot: board-level risk framing, incident playbooks rehearsed with your teams, third-party and supply-chain risk registers that survive DORA-grade scrutiny, and PQC migration planning that treats cryptographic agility as an estate-wide engineering problem.",
    ],
    method=[
        ("Estate risk baseline", "Attack surface mapped; controls priced against blast radius"),
        ("Zero-trust architecture", "Identity, device, network and data planes designed together"),
        ("Detection & response", "Telemetry, analytics and rehearsed playbooks"),
        ("Evidence engineering", "Control testing automated; audit packs generated in-flight"),
        ("Program & governance", "Board framing, third-party registers, PQC roadmap"),
    ],
    tools=[
        ("Architecture", ["Zero-trust brokers (ZTNA)", "SPIFFE/SPIRE workload identity", "Micro-segmentation", "CNAPP posture"]),
        ("Assurance", ["Attack-path modeling", "Purple-team rehearsals", "Control-evidence automation", "PQC inventory (CBOM)"]),
    ],
    deliverables=[
        "Zero-trust blueprint with phased rollout",
        "Detection & response stack tuned to your sector",
        "Rehearsed incident playbooks",
        "Automated control-evidence packs",
        "Board risk framing and PQC roadmap",
    ],
    arch_lanes=["Identities", "Devices & network", "Data plane", "Detection", "Evidence"],
    arch_nodes=[
        ("id", 0, "Workforce & workload identity", True),
        ("dn", 1, "Posture-checked devices"), ("dn", 1, "Segmented network"),
        ("dp", 2, "Classification & encryption", True),
        ("de", 3, "Detection & automated response", True),
        ("evd", 4, "Continuous control evidence", True),
    ],
    arch_edges=[("id0","dn0"),("id0","dn1"),("dn0","dp0"),("dn1","dp0"),("dp0","de0"),("de0","evd0"),("dn1","evd0")],
    focus=["banking", "insurance", "healthcare", "public-sector", "energy", "technology"],
))

C.append(dict(
    slug="cloud-azure", name="Cloud Development & Azure Services",
    promise="Azure estates engineered end to end — landing zones to AI workloads.",
    overview=[
        "Cloud programs stall between the landing zone and the workload that proves the model. As a Microsoft-aligned partner we deliver both ends: enterprise landing zones with policy-as-code and cost guardrails, and the workloads that earn the cloud its keep — data platforms on Fabric and Databricks, GenAI systems on Azure OpenAI with private networking, and modernized applications on AKS with progressive delivery.",
        "The engineering discipline stays constant across workloads: environments as code, contract-tested integrations, observability and FinOps telemetry from the first resource, and identity boundaries that follow your zero-trust standard. Azure OpenAI deployments ship with the guardrails model risk teams expect — private endpoints, content safety configured to policy, and evaluation harnesses before exposure.",
    ],
    method=[
        ("Landing zone & guardrails", "Policy-as-code, identity boundaries, cost guardrails from day one"),
        ("Data & AI platform", "Fabric/Databricks estate with contracts and lineage"),
        ("Azure OpenAI engineering", "Private endpoints, safety configuration, evaluation gates"),
        ("Application modernization", "AKS runtimes, progressive delivery, AppCAT-led moves"),
        ("Operate & optimize", "FinOps telemetry, SLO operations, well-architected reviews"),
    ],
    tools=[
        ("Platform", ["Azure landing zones (CAF)", "Azure Fabric / Databricks", "AKS & App Service", "Azure OpenAI + AI Search"]),
        ("Engineering", ["Bicep / Terraform", "GitHub Actions / Azure DevOps", "Azure Policy & Cost Management", "Defender for Cloud"]),
    ],
    deliverables=[
        "CAF landing zone with policy-as-code",
        "Data & AI platform with contracts and lineage",
        "Azure OpenAI workload with evaluation gates",
        "Modernized applications on AKS",
        "FinOps & well-architected review program",
    ],
    arch_lanes=["Governance", "Landing zone", "Data & AI", "Applications", "Operations"],
    arch_nodes=[
        ("mg", 0, "Management groups & policy", True),
        ("lz", 1, "CAF landing zones", True), ("lz", 1, "Identity boundaries"),
        ("da", 2, "Fabric / Databricks estate", True), ("da", 2, "Azure OpenAI (private)", True),
        ("ap", 3, "AKS workloads"), ("ap", 3, "Progressive delivery"),
        ("op", 4, "FinOps & SLO telemetry", True),
    ],
    arch_edges=[("mg0","lz0"),("mg0","lz1"),("lz0","da0"),("lz1","da1"),("lz0","ap0"),("da0","ap1"),("ap0","op0"),("da1","op0")],
    focus=["banking", "insurance", "healthcare", "retail", "public-sector", "manufacturing"],
))

C.append(dict(
    slug="erp-services", name="ERP Services & Enterprise Core",
    promise="ERP programs that land process, data and controls — not just software.",
    overview=[
        "ERP programs fail at the seams: the customizations nobody documented, the master data nobody owns, and the controls the auditors test that the implementers never saw. We run ERP programs as enterprise engineering — S/4HANA and Dynamics 365 implementations, finance and supply-chain transformations, and the integration fabric that keeps the core synchronized with everything around it.",
        "The method is process-first and data-governed: to-be processes designed against measurable cycle times, master data governed with owners and quality gates before the first load, controls mapped into the configuration, and cutover rehearsals that time everything — including the reconciliation your finance team will demand.",
    ],
    method=[
        ("Process & controls design", "To-be processes with cycle-time targets; controls mapped into config"),
        ("Master data governance", "Owners, quality gates and loads sequenced before cutover"),
        ("Implementation & extensions", "Clean-core discipline; extensions contract-tested"),
        ("Integration fabric", "Event-driven sync with the estate; reconciliation by design"),
        ("Cutover & hypercare", "Rehearsed cutovers with finance reconciliation; hypercare runbook"),
    ],
    tools=[
        ("Platforms", ["SAP S/4HANA", "Microsoft Dynamics 365", " Fiori / Power Platform extensions", "Event-driven integrations"]),
        ("Delivery", ["Process mining baselines", "MDG governance workflows", "Automated test suites", "Reconciliation harnesses"]),
    ],
    deliverables=[
        "To-be process & controls design",
        "Master data governance with quality gates",
        "Implemented core with clean-core extensions",
        "Integration fabric with reconciliation",
        "Rehearsed cutover & hypercare pack",
    ],
    arch_lanes=["Enterprise processes", "ERP core", "Extensions", "Integration", "Controls"],
    arch_nodes=[
        ("ep", 0, "Finance & supply-chain processes", True),
        ("co", 1, "S/4HANA / Dynamics 365 core", True), ("co", 1, "Master data governance"),
        ("ex", 2, "Clean-core extensions", True), ("ex", 2, "Fiori / Power Platform"),
        ("in", 3, "Event-driven integration", True),
        ("ct", 4, "Controls & audit evidence", True),
    ],
    arch_edges=[("ep0","co0"),("ep0","co1"),("co0","ex0"),("co1","ex1"),("ex0","in0"),("co0","in0"),("in0","ct0"),("co1","ct0")],
    focus=["manufacturing", "retail", "banking", "energy", "healthcare", "public-sector"],
))

CONSULTING = C

CONSULTING_GROUPS = [
    ("Data & Analytics", ["data-analytics", "data-migration", "digital-transformation"]),
    ("Engineering & Quality", ["software-development", "testing-qa", "application-services", "ui-ux-design"]),
    ("Cloud & Operations", ["cloud-azure", "it-services", "it-support"]),
    ("Advisory & Enterprise", ["it-consulting-outsourcing", "cybersecurity", "erp-services"]),
]
