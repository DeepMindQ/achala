# -*- coding: utf-8 -*-
"""Achala IT Solutions — Industries data layer, part B (6 industries)."""

INDUSTRIES_B = {
    "energy": {
        "name": "Energy & Utilities",
        "slug": "energy-utilities",
        "tagline": "Grid intelligence, trading optimization and safe operations for the energy transition.",
        "intro": [
            "The energy transition rewires the operating model: distributed renewables make supply stochastic, demand flexibility becomes an asset class, and the grid's control philosophy shifts from dispatchable certainty to probabilistic orchestration. Every actor in the value chain — generation, TSO/DSO, retail, trading, oil & gas — now competes on how fast it can turn telemetry into decisions and decisions into money.",
            "The complexity is physics plus markets plus regulation: NERC CIP and IEC 61850/62443 govern the operational estate, REMIT/MiFID shape trading conduct, DORA reaches grid operators, and sustainability reporting (CSRD) makes emissions data auditable. Meanwhile post-quantum timelines loom over infrastructure whose secrets must outlive careers. Getting this stack wrong is not a P&L event; it is a blackout or a sanction.",
            "Achala IT Solutions delivers across the chain: grid and asset intelligence from SCADA-class telemetry, forecasting and trading optimization with solver tournaments, O&M prediction for turbines and substations, OT segmentation and recovery engineering, customer analytics for retailers, and PQC programs for long-lived infrastructure. We speak both kilowatts and capital committees.",
        ],
        "pressures": [
            (["data"], "Forecasting under intermittency",
             "Renewable supply and flexible demand make legacy forecasting blind; imbalance costs and curtailment climb while forecasts run on yesterday's methods."),
            (["cyber"], "OT estate exposed by convergence",
             "IT/OT convergence, remote access growth and legacy SCADA estates create attack paths with physical consequences; CIP/NIS2 duties expand faster than programs mature."),
            (["iot"], "Asset fleets uninstrumented",
             "Turbines, transformers and pipelines hold decades of life left — and zero telemetry. Condition-based maintenance is impossible without sensing, and failures cost the most when they are unscheduled."),
            (["agentic"], "Trading and scheduling decisions at market speed",
             "Intraday markets reprice in minutes; scheduling, bidding and imbalance decisions run on spreadsheets and experience, not decision hubs."),
            (["cloud"], "Customer and market platforms creak",
             "Retailer platforms bend under market volatility events (price shocks, supplier failures); switching journeys and billing accuracy suffer at the worst moments."),
            (["blockchain"], "GO/REC certificate integrity",
             "Guarantees-of-origin and renewable certificates reconcile across registries with fraud exposure; buyers demand verifiable provenance."),
            (["quantum"], "PQC over infrastructure lifetimes",
             "Substations and pipelines outlive cryptographic eras; long-lived keys and protocols face PQ exposure with no inventory or clock."),
            (["data"], "ESG data assembled by spreadsheet",
             "Scope 1/2/3 reporting pulls from meter readings, invoices and estimates with no lineage; auditors begin to ask what accountants always ask: prove it."),
        ],
        "regs": [
            ("NERC CIP (North America)", "critical-infrastructure protection standards for bulk power systems"),
            ("IEC 62443 / 61850", "industrial cybersecurity and substation automation standards"),
            ("REMIT / MiFID II", "energy market conduct and reporting obligations"),
            ("DORA / NIS2", "operational resilience and cyber duties for essential entities"),
            ("CSRD / ISSB", "sustainability reporting with assurance expectations"),
            ("Data-privacy regimes", "smart-meter and consumer-energy data duties"),
        ],
        "kpis": [
            ("Forecast error (wind/solar/demand)", "down 20-35% on instrumented methods"),
            ("Unplanned outage hours on critical assets", "down 30-50%"),
            ("Imbalance and curtailment cost", "down measurably with decision hubs"),
            ("OT segmentation coverage", "complete zones-and-conduits with evidence"),
            ("ESG data production", "audit-ready on schedule, lineage complete"),
        ],
        "priorities": [
            ("Instrument the physics, monetize the forecast", "sensor fabric plus forecasting and trading decision hubs that pay for themselves in imbalance and O&M"),
            ("Segment and rehearse the OT estate", "IEC 62443 zoning, monitoring and restoration drills treating cyber events as operational events"),
            ("Build the audit-grade ESG spine", "energy/emissions telemetry with lineage feeding CSRD-grade reporting automatically"),
        ],
        "usecases": {
            "applied-ai": [
                ("Renewable and demand forecasting", "weather-coupled ML ensembles at asset and portfolio level feeding trading", "imbalance cost down via better forecasts"),
                ("Trading copilot", "market context summarized with citations to exchange data and risk policy", "trader coverage widened per desk"),
            ],
            "agentic": [
                ("Dispatch/scheduling decision hub", "unit-commitment and flexibility bidding with policy and replay", "scheduling decisions at market speed"),
                ("O&M decision agent", "condition signals to cost-optimal maintenance windows with parts and crews", "unplanned outage hours down 30-50%"),
            ],
            "data": [
                ("Grid telemetry backbone", "SCADA/AMI/weather streams into one governed estate with lineage", "forecasting and ops on the same truth"),
                ("ESG data spine", "metered energy/emissions with lineage to disclosure reports", "audit-ready reporting on schedule"),
            ],
            "cyber": [
                ("OT segmentation program", "IEC 62443 zones-and-conduits with monitoring and access control", "flat OT networks eliminated with evidence"),
                ("Grid recovery engineering", "restoration-tested backups and manual-fallback procedures", "cyber events rehearsed as outages"),
            ],
            "cloud": [
                ("Market platform resilience", "active-active customer/market platforms with chaos-verified failover", "volatility events absorbed without outages"),
                ("Edge at substations", "industrial edge fleets for local analytics", "grid-edge analytics without round trips"),
            ],
            "quantum": [
                ("Unit commitment tournaments", "classical vs. quantum-inspired solvers on scheduling formulations", "solve time and quality gains where hybrids win"),
                ("PQC for infrastructure", "CBOM across substations and control systems", "migration sequenced over asset lifetimes"),
            ],
            "blockchain": [
                ("GO/REC provenance network", "certificate issuance/transfer anchored with registry integration", "fraud and double-counting exposure down"),
                ("PPA settlement evidence", "shared settlement records between generators and offtakers", "reconciliation disputes collapse"),
            ],
            "iot": [
                ("Asset condition sensing", "turbine/transformer/pipeline telemetry with retrofit engineering", "condition-based maintenance enabled"),
                ("Grid-edge flexibility", "behind-the-meter device orchestration with customer consent", "flexibility revenue unlocked"),
            ],
        },
    },

    "logistics": {
        "name": "Logistics & Supply Chain",
        "slug": "logistics-supply-chain",
        "tagline": "The self-correcting supply chain — visibility, orchestration and autonomous flows.",
        "intro": [
            "Logistics is where operations research was born, and it is where agentic AI pays fastest: routes, loads, docks, yards and exceptions are decision fields with measurable physics. The winners run control towers that see events as they happen, re-plan autonomously within policy, and treat every exception as data — compounding an execution advantage that price discounting cannot buy.",
            "The environment keeps raising stakes: e-commerce compresses promise windows, capacity markets swing, EUDR/CSRD-style provenance and emissions reporting reach freight, and labor scarcity meets aging infrastructure. Ports, 3PLs, parcel networks and shippers all face the same core gap — operational telemetry exists but decisions still run on spreadsheets and veterans' instinct.",
            "Achala IT Solutions builds the flow stack: event-driven visibility across TMS/WMS/telematics, agentic dispatch and exception resolution, yard and dock orchestration, computer vision for damage and load verification, network twins for scenario planning, and provenance networks for compliance-grade chain-of-custody.",
        ],
        "pressures": [
            (["data"], "Visibility stitched from portals",
             "Carrier portals, EDI and telematics produce a patchwork; the control tower reads yesterday. Exceptions surface as customer complaints."),
            (["agentic"], "Dispatch and exception work manual",
             "Planners re-plan routes and loads by hand when trucks break down or orders change; exception queues eat capacity that should improve the network."),
            (["iot"], "Fleet and yard telemetry gaps",
             "Trailer/container/yard assets lack sensing; detention, dwell and theft are discovered in invoices. Cold-chain excursions surface at claim time."),
            (["applied-ai"], "Demand and capacity planning stale",
             "Volume forecasts lag promotion cycles and market shifts; capacity buys and network design inherit the error."),
            (["cyber"], "Freight fraud and cyber exposure",
             "Double-brokering fraud and carrier-identity theft rise alongside ransomware targeting 3PLs; the estate mixes corporate IT with driver-facing OT."),
            (["blockchain"], "Compliance-grade provenance missing",
             "EUDR-grade due diligence and custody evidence for high-value goods remain paper-based; customs and buyers escalate."),
            (["cloud"], "Peak surges break planning",
             "Q4 surges and disruptions (Suez-class) exceed static planning; network re-optimization takes weeks."),
            (["quantum"], "Routing at combinatorial scale",
             "Dynamic routing across thousands of stops hits classical solver ceilings in the time available."),
        ],
        "regs": [
            ("EUDR", "deforestation due diligence for in-scope commodities with evidence duties"),
            ("CSRD/ISSB logistics emissions", "scope 3 transport emissions with auditability"),
            ("CMR/ADR/IMDG transport rules", "dangerous-goods and carriage documentation duties"),
            ("Customs/security regimes (AEO, C-TPAT)", "chain-security compliance evidence"),
            ("GDPR", "driver and customer data duties across telematics"),
            ("Food safety (where cold chain)", "temperature evidence and recall duties"),
        ],
        "kpis": [
            ("On-time-in-full", "up 5-10 points on orchestrated lanes"),
            ("Empty miles", "down 10-20% with dynamic matching"),
            ("Detention and dwell time", "down 25-40% with yard/dock orchestration"),
            ("Exception resolution time", "hours instead of days via agentic remediation"),
            ("Cold-chain excursions", "intercepted in transit, not at claims"),
        ],
        "priorities": [
            ("One event spine, many decisions", "streaming visibility into dispatch, ETA, detention and claims decision hubs"),
            ("Automate the exception, not just the plan", "agentic remediation for the recoverable 80% of disruptions with human policy gates"),
            ("Provenance as a product", "compliance-grade chain-of-custody networks that customs and customers accept"),
        ],
        "usecases": {
            "applied-ai": [
                ("ETA prediction", "traffic, weather and history-driven ETA models per lane and mode", "promise accuracy up; penalties down"),
                ("Damage detection", "vision models at docks for load/damage verification with dispute evidence", "claims cycle time down"),
            ],
            "agentic": [
                ("Dispatch orchestration", "dynamic route/load re-planning within policy when events hit", "re-plan in minutes at network scale"),
                ("Exception resolution agent", "delay, detention and document exceptions remediated automatically with escalation", "exception queues cleared autonomously"),
            ],
            "data": [
                ("Control-tower event spine", "TMS/WMS/telematics/carrier events streamed into one governed estate", "network truth in seconds"),
                ("Emissions intelligence", "lane-level scope 3 transport emissions with methodology lineage", "CSRD-grade reporting automated"),
            ],
            "cyber": [
                ("Freight-fraud defense", "carrier identity verification and double-brokering detection analytics", "fraud losses down measurably"),
                ("3PL ransomware resilience", "segmentation between corporate IT and operational systems with recovery drills", "operations continue through IT events"),
            ],
            "cloud": [
                ("Peak surge engineering", "elastic capacity with load modeling for trading peaks", "peak absorbed at controlled unit cost"),
                ("Network re-optimization platform", "scenario engines for disruption events (port closures, lane breaks)", "re-optimization in days, not weeks"),
            ],
            "quantum": [
                ("Dynamic routing tournaments", "quantum-inspired vs. classical on daily dispatch formulations", "route cost down where solvers win"),
                ("Network design optimization", "hub/location formulations benchmarked honestly", "capital decisions better evidenced"),
            ],
            "blockchain": [
                ("EUDR chain-of-custody", "anchored custody events for in-scope commodities with regulator interfaces", "due-diligence evidence in hours"),
                ("High-value custody network", "shared evidence between shipper, carrier and insurer", "claims and disputes collapse"),
            ],
            "iot": [
                ("Fleet and trailer sensing", "telematics, door and temperature telemetry with governance", "cold-chain and detention visible live"),
                ("Yard and dock orchestration", "gate, yard and dock telemetry into appointment systems", "dwell time down 25-40%"),
            ],
        },
    },

    "public-sector": {
        "name": "Public Sector & Government",
        "slug": "public-sector",
        "tagline": "Citizen services that work — digital government, secure estates and accountable AI.",
        "intro": [
            "Governments face a delivery paradox: citizen expectations are set by the best private digital experiences, while estates run on legacy systems, procurement cycles and risk cultures that penalize innovation. The administrations breaking the paradox do three things well — they build shared digital infrastructure (identity, payments, notification), they industrialize service delivery on data, and they deploy AI under frameworks citizens can actually inspect.",
            "The accountability bar is total: procurement law, records management, accessibility mandates, privacy regimes, security accreditation and now AI transparency obligations all bind simultaneously. This is why Achala IT Solutions leads with evidence-grade engineering: every deliverable arrives with its documentation, its control mapping and its audit trail already in order.",
            "We serve national and local government, defense-adjacent agencies, public safety and justice: citizen-service platforms, document intelligence for casework, fraud and error detection in benefits and tax, zero-trust and PQC programs for critical data estates, emergency-management intelligence, and smart-city platforms with privacy-by-design governance.",
        ],
        "pressures": [
            (["data"], "Agency data islands",
             "Benefits, tax, health and licensing systems never joined; citizens re-submit the same facts to every agency. Fraud and error hide in the seams."),
            (["applied-ai"], "Casework drowning in documents",
             "Permits, claims and case files are paper-shaped; processing times measured in months erode trust and increase cost per case."),
            (["cyber"], "Legacy estates and accreditation drag",
             "Aging systems with hardening debt meet rising state-grade threats; accreditation cycles slow every change."),
            (["cloud"], "Legacy mainframes as single points of failure",
             "Tax, benefits and licensing cores run on platforms with shrinking talent pools; failure risk compounds annually."),
            (["agentic"], "Service delivery inconsistent across channels",
             "Web, phone and counter experiences diverge; back-office handoffs lose context and create rework loops."),
            (["blockchain"], "Records integrity under dispute",
             "Land registries, licenses and procurement records face integrity challenges; evidence chains are procedural, not cryptographic."),
            (["quantum"], "State-grade adversaries harvesting",
             "Citizen records and diplomatic traffic face HNDL exposure at scale; crypto inventory is unknown."),
            (["iot"], "Urban assets unmanaged",
             "Lighting, traffic, water and building estates lack telemetry; maintenance is reactive and energy waste invisible."),
        ],
        "regs": [
            ("Accessibility (Section 508 / EN 301 549 / WCAG)", "digital services must meet accessibility mandates"),
            ("GDPR / national privacy law", "citizen data duties including automated-decision transparency"),
            ("EU AI Act", "public-sector AI uses largely high-risk with conformity duties"),
            ("Records/archives law", "retention, integrity and evidence requirements"),
            ("Security accreditation (FedRAMP-class / national schemes)", "cloud and system authorization duties"),
            ("Procurement law", "competition, transparency and audit obligations"),
        ],
        "kpis": [
            ("Case processing time", "down 40-60% on document-intensive services"),
            ("Citizen contact resolution", "first-contact resolution up sharply with grounded assistants"),
            ("Fraud and error detection", "+20-30% capture at stable investigator load"),
            ("Service standardization", "one citizen record across channels"),
            ("Accreditation evidence", "produced continuously, not assembled annually"),
        ],
        "priorities": [
            ("Shared infrastructure before new services", "identity, notification, payments and data exchange as reusable rails every agency builds on"),
            ("Accountable AI by design", "transparency notices, human-oversight gates and conformity documentation built into every deployment"),
            ("Modernize cores without betting the estate", "strangler programs with parallel-run evidence on tax/benefits/licensing systems"),
        ],
        "usecases": {
            "applied-ai": [
                ("Citizen service assistant", "grounded answers on entitlements and procedures across web and voice with citations", "first-contact resolution up sharply"),
                ("Casework document intelligence", "permits/claims classified, extracted and summarized for officers", "processing time down 40-60%"),
            ],
            "agentic": [
                ("Eligibility assembly agent", "evidence gathered across registries for benefit/licensing decisions with officer approval", "backlog reduction at stable staff"),
                ("Fraud and error detection hub", "cross-agency analytics scoring anomalies with investigator case packs", "capture up at stable load"),
            ],
            "data": [
                ("Interagency data exchange", "event-driven, consent-aware data sharing between agencies with lineage", "tell-us-once services enabled"),
                ("Performance management platform", "service metrics aligned to delivery cadence with certified definitions", "delivery decisions on real numbers"),
            ],
            "cyber": [
                ("Zero-trust government estate", "identity-centric access across agencies and third parties", "state-grade threat surface reduced with evidence"),
                ("PQC for citizen records", "CBOM and migration for decade-retention data", "harvest exposure closed early"),
            ],
            "cloud": [
                ("Accredited cloud platform", "landing zones meeting accreditation with continuous evidence", "agencies onboard in weeks"),
                ("Legacy core modernization", "strangler decomposition with parallel-run equivalence", "mainframe risk reduced on schedule"),
            ],
            "quantum": [
                ("PQC program for state estates", "discovery through hybrid transition with agency playbooks", "migration sequenced before pressure"),
                ("Scheduling optimization pilots", "courts/inspection route formulations benchmarked", "resource allocation improved where solvers win"),
            ],
            "blockchain": [
                ("Records integrity anchoring", "registries and procurement records anchored for integrity", "disputes resolved on cryptographic evidence"),
                ("Verifiable credentials for licenses", "portable credentials across agencies and borders", "verification friction down"),
            ],
            "iot": [
                ("Smart-city platform", "lighting/traffic/water telemetry with privacy-by-design governance", "energy and service costs down measurably"),
                ("Public-building optimization", "occupancy-aware facility management across portfolios", "facility energy down 10-20%"),
            ],
        },
    },

    "education": {
        "name": "Education & Research",
        "slug": "education-research",
        "tagline": "Learning that adapts, research that accelerates — with academic integrity intact.",
        "intro": [
            "Education institutions run two businesses on one budget: teaching and knowledge production. Both are being reshaped by AI — adaptive learning and assessment automation on one side, research acceleration from literature synthesis to simulation on the other — while both face an integrity crisis that generic tooling makes worse. The institutions that thrive will industrialize the boring (operations, admissions, estate management) to fund the essential (teaching quality, research depth).",
            "The constraints are real: student-privacy regimes (FERPA/GDPR-K class), accessibility mandates, academic-integrity governance, research-data ethics, and budget cycles that punish stranded investments. Technology must respect pedagogy and governance, not bulldoze them — which is why Achala IT Solutions co-designs every deployment with faculty governance and student bodies.",
            "We deliver across higher education, K-12 systems, EdTech platforms and corporate learning: student-success analytics with early-warning discipline, admissions and enrollment intelligence, research computing (HPC, data platforms, quantum pilots), integrity-preserving assessment tools, and campus operations from energy to space utilization.",
        ],
        "pressures": [
            (["data"], "Student signals scattered",
             "LMS, SIS, attendance and support-service data never meet; at-risk students surface at failure, not at drift."),
            (["applied-ai"], "Integrity vs. AI confusion",
             "Generative tools flood campuses with no policy infrastructure; detection arms races erode trust while legitimate assistive use goes ungoverned."),
            (["agentic"], "Administrative burden on faculty",
             "Advising, scheduling, accreditation evidence and grant reporting consume academic hours; support staff swim in document flows."),
            (["cyber"], "Open estates under real threats",
             "Research IP attracts nation-grade interest while campus culture resists control; ransomware closes institutions for weeks."),
            (["cloud"], "Research computing fragmented",
             "Labs buy cloud haphazardly; HPC queues and cloud spend lack governance, and research data governance varies by department."),
            (["applied-ai"], "Enrollment economics tightening",
             "Demographic cliffs and competition demand precise recruitment and retention economics; marketing spend is unmeasured."),
            (["iot"], "Estates flying blind",
             "Space utilization, energy and lab-environment telemetry missing; facilities cost per student rises."),
            (["quantum"], "Research frontier advantage",
             "Quantum programs concentrate at wealthy institutions; mid-tier universities lack structured on-ramps."),
        ],
        "regs": [
            ("FERPA / student-privacy regimes", "educational-record duties incl. vendor contracts"),
            ("GDPR-K / minors' data rules", " heightened consent and profiling limits for K-12"),
            ("Accessibility mandates (ADA/EN 301 549)", "digital learning materials must comply"),
            ("Research ethics (IRB/ethics boards)", "human-subject and data governance for research"),
            ("Export controls on research", "dual-use technology data governance"),
            ("Accreditation evidence standards", "learning-outcome documentation duties"),
        ],
        "kpis": [
            ("Early-warning precision", "at-risk flags actionable 4-8 weeks earlier"),
            ("Retention in targeted cohorts", "up 3-6 points on intervened programs"),
            ("Faculty administrative hours", "down 25-40% on automated flows"),
            ("Research computing throughput", "up 2-5x on governed platforms"),
            ("Campus energy cost", "down 10-20% with instrumented estates"),
        ],
        "priorities": [
            ("Student success as a data discipline", "early-warning analytics wired to advising workflows with outcome measurement"),
            ("Governed AI for teaching and research", "integrity-preserving policy infrastructure, assistive tooling and faculty governance boards"),
            ("Shared research computing platform", "HPC/data/quantum access under governance that mid-size budgets sustain"),
        ],
        "usecases": {
            "applied-ai": [
                ("Learning assistants with integrity rails", "course-grounded tutoring within instructor-set boundaries and logging", "support access up; integrity disputes down"),
                ("Research literature synthesis", "domain corpora synthesized with citations for review acceleration", "review phase time down sharply"),
            ],
            "agentic": [
                ("Advising orchestration", "early-warning signals trigger advising interventions with case management", "retention lift in targeted cohorts"),
                ("Accreditation evidence agent", "learning-outcome evidence assembled for program reviews", "faculty reporting hours down"),
            ],
            "data": [
                ("Student success platform", "SIS/LMS/support data unified with outcome lineage", "intervention targeting measurable"),
                ("Research data commons", "governed research datasets with ethics-aware access control", "collaboration without governance loss"),
            ],
            "cyber": [
                ("Research IP protection", "classification-aware controls for sensitive research programs", "export-control posture evidenced"),
                ("Campus ransomware resilience", "segmentation and recovery drills for academic continuity", "restart time proven in exercises"),
            ],
            "cloud": [
                ("Research computing platform", "HPC/cloud burst with queue governance and cost telemetry", "throughput up 2-5x per funding unit"),
                ("Campus FinOps", "departmental cloud showback with commitment strategy", "waste visible and reduced"),
            ],
            "quantum": [
                ("Quantum curriculum on-ramp", "cloud-accessible quantum labs with classical baselines", "research-grade pilots at mid-budget"),
                ("Research simulation acceleration", "HPC+quantum benchmarked pilots for physics/chemistry groups", "honest verdicts with revisit triggers"),
            ],
            "blockchain": [
                ("Credential wallets for graduates", "verifiable diplomas/certificates with employer verification", "verification friction eliminated"),
                ("Research provenance", "dataset and publication provenance anchoring", "integrity evidence automated"),
            ],
            "iot": [
                ("Campus estate intelligence", "space, energy and lab-environment telemetry", "energy cost down 10-20%"),
                ("Lab environment safety", "freezer/ventilation monitoring with alerting", "research asset loss prevented"),
            ],
        },
    },

    "technology": {
        "name": "Technology & SaaS",
        "slug": "technology-saas",
        "tagline": "Ship faster, scale smarter, monetize data — engineering leverage for software companies.",
        "intro": [
            "Software companies eat their own cooking or get eaten: platform engineering, SRE discipline and FinOps are not nice-to-haves but the operating system of companies whose product is infrastructure. The AI era adds a new economics layer — inference cost per customer, model quality per feature, data moats per vertical — that decides which SaaS companies compound margin and which dilute it.",
            "The competitive math is unforgiving: NRR (net revenue retention) is decided by product velocity and reliability; enterprise procurement gates on SOC 2/ISO 27001 evidence; AI features must launch in weeks against well-funded rivals while keeping unit economics sane. Meanwhile data products — benchmarks, telemetry insights, vertical datasets — have become a second revenue line for companies that can build the privacy and entitlement plumbing.",
            "Achala IT Solutions works with SaaS and platform companies, fintech-adjacent teams, semiconductor and hardware firms, and gaming studios: platform engineering and DevEx programs, AI feature factories with evaluation harnesses, data monetization stacks, security and compliance automation, and scaling engineering for the moments when growth tests architecture.",
        ],
        "pressures": [
            (["cloud"], "Velocity vs. reliability tension",
             "Deploy frequency rises while incident load eats roadmap; error budgets exist in slide decks, not in release policy."),
            (["applied-ai"], "AI features ship without economics",
             "Teams bolt on LLM features with no cost telemetry, no eval harness and no guardrails; margins erode silently per customer."),
            (["data"], "Data moat unrealized",
             "Usage telemetry accumulates but never becomes product; data products stall on privacy questions and entitlement plumbing."),
            (["cyber"], "Compliance gates enterprise deals",
             "SOC 2/ISO 27001 evidence assembled manually per audit; security questionnaires consume engineering weeks per quarter."),
            (["cloud"], "Cloud unit economics opaque",
             "Cost per customer, per tenant, per feature unknown; gross margin surprises surface in board decks."),
            (["agentic"], "Support and success scale linearly",
             "Customer support and CS operations grow headcount with ARR; ticket deflection without resolution raises churn risk."),
            (["quantum"], "Post-quantum product pressure",
             "B2B customers begin demanding PQC roadmaps for products holding long-lived secrets; roadmaps don't exist."),
            (["blockchain"], "Marketplace trust mechanics weak",
             "Multi-sided marketplaces lack portable reputation/credential layers; verification friction suppresses liquidity."),
        ],
        "regs": [
            ("SOC 2 / ISO 27001", "procurement-gating certification with evidence duties"),
            ("GDPR/CCPA", "customer-data processing, DPAs and subprocessor duties"),
            ("EU AI Act (as AI providers)", "transparency, documentation and GPAI-adjacent duties"),
            ("EU Cyber Resilience Act", "product security duties for connected software/hardware"),
            ("Sector overlays (PCI, HIPAA B2B)", "compliance duties inherited from enterprise customers"),
            ("Export controls", "technology transfer restrictions where relevant"),
        ],
        "kpis": [
            ("DORA lead time", "down 50%+ on paved-road services"),
            ("Gross margin on AI features", "protected via routing, caching and eval gates"),
            ("Enterprise deal cycle", "security evidence produced continuously"),
            ("Data product revenue", "first line live within two quarters"),
            ("Support cost per customer", "down 30%+ with resolution-first agents"),
        ],
        "priorities": [
            ("Platform leverage before headcount", "golden paths, SLO discipline and FinOps unit economics as the growth foundation"),
            ("AI features as products, not demos", "evaluation harnesses, guardrails and cost telemetry from the first release"),
            ("Compliance as code", "continuous evidence turning procurement gates into a formality"),
        ],
        "usecases": {
            "applied-ai": [
                ("AI feature factory", "eval harness, guardrails and cost telemetry wired into the product release train", "AI features ship weekly with protected margin"),
                ("Support resolution agent", "product-knowledge-grounded agents resolving tickets with escalation context", "support cost per customer down 30%+"),
            ],
            "agentic": [
                ("Customer-success orchestration", "usage signals trigger health plays and renewal actions", "NRR protected at scale"),
                ("Internal DevEx agents", "runbooks, incident summaries and PR reviews automated with policy", "engineering hours reallocated to product"),
            ],
            "data": [
                ("Usage telemetry platform", "product events into governed analytics with feature-level cost attribution", "product decisions on real unit economics"),
                ("Data product stack", "clean rooms, entitlements and metering for customer-facing insights", "second revenue line launched"),
            ],
            "cyber": [
                ("Compliance automation", "continuous SOC 2/ISO evidence with framework-unified register", "audit prep down 60-80%"),
                ("Product security program", "CRA-aligned secure development and vulnerability SLAs", "enterprise security reviews passed faster"),
            ],
            "cloud": [
                ("Platform engineering program", "golden paths, catalog and DORA instrumentation", "lead time down 50%+"),
                ("Tenant economics engineering", "cost attribution per tenant/feature with showback", "margin surprises eliminated"),
            ],
            "quantum": [
                ("PQC product roadmap", "crypto-agility design for products holding customer secrets", "enterprise PQC demands answered"),
                ("Pricing/_matching optimization pilots", "marketplace matching benchmarked vs. classical solvers", "liquidity mechanics improved where solvers win"),
            ],
            "blockchain": [
                ("Marketplace credential layer", "portable reputation/credentials for participants", "verification friction down; liquidity up"),
                ("Usage-metered settlement", "on-chain metered settlement where multi-party value flows", "disputes reduced on shared evidence"),
            ],
            "iot": [
                ("Hardware fleet platform", "connected-device provisioning, OTA and telemetry for hardware-adjacent products", "device-to-revenue loop closed"),
                ("Office/lab estate intelligence", "energy and utilization telemetry for sites", "operating cost down measurably"),
            ],
        },
    },

    "agriculture": {
        "name": "Agriculture & Food Systems",
        "slug": "agriculture-food",
        "tagline": "From precision agronomy to verified provenance — technology across the food chain.",
        "intro": [
            "Food systems sit under simultaneous pressure: feed more with less input, prove sustainability claims to regulators and buyers, absorb climate volatility, and keep margins across a chain famous for thinning them. The technology response spans the chain — sensing and agronomy models in the field, traceability and EUDR-grade provenance through the chain, yield and quality intelligence in processing, and provenance premium capture at retail.",
            "The regulatory wave is arriving: EU Deforestation Regulation due diligence, Digital Product Passports, residue and food-safety regimes, and subsidy programs demanding measured practice. Farms and co-ops that instrument now convert compliance into competitive advantage; those that wait will buy evidence later at retail prices.",
            "Achala IT Solutions builds for agribusiness, co-ops, food processors and agri-finance: precision-agronomy platforms on sensor and satellite feeds, yield and quality prediction, chain-of-custody networks with verifiable credentials, agri-finance risk models, and food-safety traceability that answers a recall query in minutes.",
        ],
        "pressures": [
            (["iot"], "Field data gap",
             "Agronomic decisions run on tradition because soil, weather and crop telemetry are patchy; input spend is uniform where it should be variable."),
            (["blockchain"], "Provenance claims unverifiable",
             "Origin, organic and deforestation-free claims face EUDR-grade scrutiny; evidence is paper and trust."),
            (["applied-ai"], "Yield and quality surprises",
             "Harvest forecasting is regional guesswork; quality attributes (protein, moisture, defects) are discovered at intake, not predicted."),
            (["data"], "Chain data broken at every handoff",
             "Farm, co-op, processor and retail data never join; traceability requires weeks of document archaeology."),
            (["agentic"], "Input and logistics planning manual",
             "Input ordering, harvest logistics and storage decisions run on experience; weather windows missed cost yield and quality."),
            (["data"], "Agri-finance blind to practice",
             "Lenders and insurers price farms on history, not practice; sustainable practice earns no capital advantage."),
            (["cloud"], "Season peaks break systems",
             "Harvest intake, subsidy deadlines and trading windows spike; systems built for average load fail at the moments that matter."),
            (["quantum"], "Logistics at combinatorial scale",
             "Harvest logistics, storage allocation and export routing hit solver ceilings exactly when timing matters most."),
        ],
        "regs": [
            ("EUDR", "deforestation-free due diligence with geolocation evidence for in-scope commodities"),
            ("Digital Product Passport (EU)", "product-level data duties approaching for food-adjacent goods"),
            ("Food-safety regimes (HACCP/EU 178/FSMA)", "traceability and recall duties"),
            ("Residue/MRL standards", "input-compliance evidence duties"),
            ("CAP/subsidy measurement", "practice-verification requirements"),
            ("GDPR", "farmer and worker data duties"),
        ],
        "kpis": [
            ("Input cost per hectare", "down 10-20% with variable-rate practice"),
            ("Yield forecast error", "down 20-35% at field level"),
            ("Recall scoping time", "minutes with chain-of-custody, vs. weeks"),
            ("Provenance premium capture", "verified claims opening premium channels"),
            ("Harvest logistics losses", "down measurably with orchestrated windows"),
        ],
        "priorities": [
            ("Instrument the field that pays", "sensor/satellite fabric where input savings and yield prediction clear the investment hurdle fastest"),
            ("Turn EUDR into advantage", "chain-of-custody networks that convert compliance evidence into premium market access"),
            ("Predict quality before intake", "yield/quality models feeding harvest, storage and trading decisions"),
        ],
        "usecases": {
            "applied-ai": [
                ("Yield and quality prediction", "satellite+sensor+agronomy models per field with uncertainty bands", "harvest and trading decisions informed early"),
                ("Agronomy advisory assistant", "field-grounded recommendations with treatment citations for advisors", "advisory coverage extended per agronomist"),
            ],
            "agentic": [
                ("Harvest logistics orchestration", "weather-window aware scheduling of machines, crews and storage", "logistics losses down measurably"),
                ("Input ordering agents", "variable-rate input plans converted to orders within agronomy policy", "input cost per hectare down 10-20%"),
            ],
            "data": [
                ("Farm data platform", "field, machine, weather and lab data unified with plot-level lineage", "agronomy and finance on the same truth"),
                ("Chain traceability spine", "custody events from plot to pallet with master-data discipline", "recall queries answered in minutes"),
            ],
            "cyber": [
                ("Agri-finance fraud controls", "subsidy/loan application verification with cross-source analytics", "fraud and error capture up"),
                ("Rural estate security", "segmentation for farm/processing OT and office estates", "ransomware exposure reduced"),
            ],
            "cloud": [
                ("Season surge engineering", "elastic intake/trading capacity with load modeling", "season peaks absorbed"),
                ("Agri-fin platform modernization", "trading and settlement platforms modernized in waves", "deadline failures eliminated"),
            ],
            "quantum": [
                ("Harvest logistics optimization", "routing/storage tournaments at season peak", "windows met where solvers win"),
                ("Feed/formulation optimization", "ration and blend formulations benchmarked vs. classical", "cost per tonne down where hybrids win"),
            ],
            "blockchain": [
                ("EUDR chain-of-custody network", "geolocation-anchored plots, custody events and regulator interfaces", "due-diligence evidence produced continuously"),
                ("Producer credential network", "certifications (organic, fair-trade) as verifiable credentials", "premium channels unlocked with proof"),
            ],
            "iot": [
                ("Field sensor fabric", "soil, weather and crop sensing with governance", "variable-rate practice enabled"),
                ("Cold-chain and storage telemetry", "silo/supply-chain environment monitoring", "quality preserved; losses down"),
            ],
        },
    },
}
