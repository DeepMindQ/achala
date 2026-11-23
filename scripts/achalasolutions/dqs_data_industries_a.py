# -*- coding: utf-8 -*-
"""Achala IT Solutions — Industries data layer, part A (6 industries)."""

# Each industry: intro (3 paras), pressures [(tower_ids, title, desc)], regs, kpis,
# priorities [(theme, response)], usecases {tower_id: [(title, what, kpi), ...]}

INDUSTRIES_A = {
    "banking": {
        "name": "Banking & Financial Services",
        "slug": "banking-financial-services",
        "tagline": "Real-time risk, resilient operations and auditable AI for institutions that cannot fail quietly.",
        "intro": [
            "Banking runs on decisions made under regulatory scrutiny at transaction speed. Credit limits, fraud interdiction, liquidity buffers, KYC refreshes — each is a decision that must be explainable months later, yet taken in milliseconds. The institutions pulling ahead have rebuilt the machinery beneath those decisions: governed data estates, decision hubs with replay, and AI programs whose controls were designed for the audit, not bolted on after it.",
            "The pressure is structural, not cyclical. Operational resilience regimes such as DORA make third-party ICT risk and incident reporting board-level obligations. Basel-style capital discipline prices risk model quality directly. Real-time payment rails compress the fraud window from hours to seconds. And digital challengers reset customer expectations every quarter — your app is compared against the best experience your customer has seen anywhere, not against your peer banks.",
            "Achala IT Solutions works with retail banks, corporate and investment banks, payment institutions and capital-markets firms as an engineering partner, not a slide deck. We build the lakehouse underneath risk and finance, the decision hubs that score and route, the agentic workforce that clears the KYC and exception backlog, and the evidence layer that turns every audit into a formality. Outcome-linked engagements put our fees next to the metric we move — loss rate, straight-through rate, cycle time.",
        ],
        "pressures": [
            (["agentic"], "KYC and periodic-review backlog",
             "Customer due diligence refresh cycles lag behind actual risk changes; files queue for weeks in review pools while remediation backlogs grow. Manual file assembly across registries, screening tools and core systems consumes analyst hours that produce no judgment."),
            (["applied-ai", "cyber"], "GenAI stuck between pilot and policy",
             "Generative assistants for credit memos, research summaries and client drafts stall in model-risk review because guardrails, provenance and audit trails were not designed in. Shadow AI fills the gap, creating exactly the exposure the review was meant to prevent."),
            (["data"], "Fragmented risk and finance data",
             "Credit, market, liquidity and operational risk live in separate estates with divergent reference data. Regulatory reporting leans on manual workarounds, and lineage questions that regulators now ask take expeditions instead of queries."),
            (["cyber"], "Resilience and third-party evidence burden",
             "DORA-class regimes demand registers of ICT third parties, tested incident playbooks and exit strategies. Evidence lives in spreadsheets and mailboxes; every assessment becomes a quarter-long archaeology project."),
            (["agentic", "data"], "Fraud and AML decisions too slow",
             "Batch scoring misses the real-time payment window; rules engines generate alert volumes that investigation teams cannot clear. The result is both rising fraud leakage and rising false-positive cost in the same program."),
            (["cloud"], "Core estate inertia",
             "Mainframe-adjacent cores and change freezes make every product launch a negotiation. Meanwhile cloud spend grows without unit economics — nobody can state cost per payment processed or per account opened."),
            (["quantum"], "Harvest-now-decrypt-later exposure",
             "Long-lived client records, interbank traffic and archived communications face retrospective decryption risk as quantum timelines shorten. Cryptographic inventory is incomplete; migration has no owner and no clock."),
            (["blockchain"], "Settlement and reconciliation friction",
             "T+2/T+1 cycles, multi-party reconciliation and dispute evidence spread across counterparties consume operations capacity. Interbank workflows still reconcile by exchanging files and hoping."),
            (["applied-ai"], "Service deflection without resolution",
             "Chatbots deflect contact volume but not intent; repeat contact within seven days rises while CSAT falls. Front-line teams inherit escalations stripped of context."),
        ],
        "regs": [
            ("DORA (EU)", "ICT risk, incident reporting, resilience testing and third-party oversight obligations with supervisory scrutiny"),
            ("Basel III endgame / capital regimes", "model quality and data lineage directly affect RWA and capital"),
            ("PSD2 / PSD3 and instant payments", "real-time rails with fraud and SCA obligations"),
            ("EU AI Act", "credit scoring and risk assessment classify as high-risk AI with documentation duties"),
            ("GDPR / privacy regimes", "automated decision-making transparency and DSAR timelines"),
            ("MiCA", "digital-asset exposure and service obligations where crypto-adjacent"),
        ],
        "kpis": [
            ("Fraud losses", "down 30-45% within three quarters on instrumented rails"),
            ("KYC refresh cycle time", "from weeks to days with agentic assembly and review"),
            ("Straight-through processing on payments/claims-adjacent flows", "up 25-40 points"),
            ("Regulatory report production effort", "down 50%+ with lineage-driven automation"),
            ("Alert false-positive rate", "down 40-60% with tuned models and policy layers"),
        ],
        "priorities": [
            ("Decision infrastructure before more models", "one governed decision hub with replay serving fraud, credit and service routing — models become swappable challengers"),
            ("Evidence-first resilience posture", "DORA-aligned third-party register, tested playbooks and automated evidence collection replacing spreadsheet archaeology"),
            ("Industrialized GenAI under model risk", "platform guardrails, provenance and evaluation harnesses agreed with the model risk function before the first prompt ships"),
        ],
        "usecases": {
            "applied-ai": [
                ("Credit memo drafting copilot", "analysts draft credit memos with retrieval over mandates, financials and policy, every paragraph citing its source", "memo preparation time down 50-60%"),
                ("Client research assistant", "relationship teams query the research corpus in policy-bounded language with compliance-approved phrasing", "research turnaround from days to minutes"),
            ],
            "agentic": [
                ("KYC refresh agent", "assembles registry extracts, screening results and account history per file; analysts judge instead of gathering", "refresh cycle time down 60-80%"),
                ("Real-time fraud decision hub", "streaming features and policy layers score instant payments with decision replay for disputes", "fraud losses down 35%+ at constant alert volume"),
            ],
            "data": [
                ("Enterprise risk lakehouse", "credit, market, liquidity and ops risk on one governed estate with BCBS 239-style lineage", "report lineage questions answered in hours"),
                ("Payments telemetry backbone", "event-streamed payment flows feeding monitoring, pricing and client analytics", "issue detection moved to event time"),
            ],
            "cyber": [
                ("Zero-trust for the branch and core estate", "identity-centric access, microsegmentation and workload identity across branch, office and datacenter zones", "lateral-movement paths eliminated in purple-team validation"),
                ("DORA evidence automation", "third-party register, incident playbooks and control tests continuously evidenced", "assessment preparation down from quarters to weeks"),
            ],
            "cloud": [
                ("Core-adjacent modernization", "strangler-pattern decomposition of monolith wrappers around core with parallel-run equivalence", "product launch lead time cut in half on migrated domains"),
                ("Payments processing FinOps", "unit cost per payment instrumented; commitment and workload isolation applied", "processing unit cost down 25-40%"),
            ],
            "quantum": [
                ("Portfolio optimization tournament", "classical MIP vs. quantum-inspired solvers on identical rebalancing benchmarks", "solve time down and quality up where hybrid wins"),
                ("PQC for long-lived client records", "CBOM inventory, exposure ranking and hybrid key-establishment transition", "migration sequenced years ahead of supervisory pressure"),
            ],
            "blockchain": [
                ("Interbank reconciliation network", "permissioned DLT with shared custody-event evidence replacing file exchange", "reconciliation effort down 70%"),
                ("Collateral tokenization pilot", "permissioned issuance with transfer controls and custody integration under securities discipline", "collateral mobilization cycle compressed"),
            ],
            "iot": [
                ("Branch and office estate telemetry", "environment, occupancy and ATM telemetry into facilities and service analytics", "facilities energy cost down 10-15%"),
                ("ATM predictive maintenance", "device telemetry driving field-service dispatch and parts staging", "ATM downtime down 30%+"),
            ],
        },
    },

    "insurance": {
        "name": "Insurance & Risk",
        "slug": "insurance",
        "tagline": "Underwriting precision, claims velocity and reserving discipline — engineered on governed data.",
        "intro": [
            "Insurance is a decision business wrapped in a promise: price the risk correctly, honor the claim quickly, hold the reserves honestly. All three now depend on machinery most carriers have underinvested in — pricing models that see the portfolio's drift, claims pipelines that read documents instead of waiting for humans, and reserving analytics that reconcile actuarial judgment with live experience data.",
            "The industry's structural pressures compound: catastrophe volatility reprices property books annually, combined-ratio pressure meets softening cycles, and fraud has industrialized on both sides of the ledger. Meanwhile distribution shifts — embedded insurance, ecosystems, digital MGAs — reward carriers whose underwriting and claims engines can plug into partners' platforms through APIs rather than PDFs.",
            "Achala IT Solutions builds the machinery: underwriting workbenches with speed-to-quote discipline, agentic claims triage that reads FNOL packets and medical reports, fraud decision hubs with network analytics, and reserving workbenches that keep actuaries in command while automating the data wrangling. Our delivery includes the model governance carriers' regulators expect — documentation as you build, not reconstruction under exam.",
        ],
        "pressures": [
            (["agentic"], "Claims intake drowning in documents",
             "FNOL packets, medical reports, repair estimates and police files arrive as unstructured documents; manual triage queues claims for days before an adjuster sees them. Leakage and customer patience both bleed in the queue."),
            (["applied-ai"], "Pricing sophistication outrunning governance",
             "GLM-based pricing, telematics factors and external data enrichment multiply model complexity faster than validation capacity. Filings get challenged; model risk documentation is reconstructed under exam pressure."),
            (["data"], "Claims, policy and exposure data fragmented",
             "Underwriting, claims and finance each hold their own truth; loss triangles reconcile by spreadsheet. Portfolio analytics that should steer the cycle take months of manual assembly."),
            (["cyber"], "Sensitive data estate under pressure",
             "Health and financial records concentrate breach value; carrier cyber programs face both attacker interest and regulatory scrutiny on safeguarding. Third-party ecosystems (TPAs, brokers) extend the attack surface."),
            (["agentic"], "Fraud industrialized against manual detection",
             "Organized fraud rings exploit application and claims patterns across carriers faster than rule updates. SIU teams work leads generated by thresholds tuned for last year's fraud."),
            (["cloud"], "Legacy policy admin drag",
             "Core policy systems from another era make product changes quarterly affairs. Expense ratios carry the weight of manual operations that competitors have automated."),
            (["applied-ai"], "Distribution partners need embedded rails",
             "Embedded and ecosystem distribution demand real-time quoting, API-first underwriting and event-driven policy servicing. PDF-and-portal partners lose the shelf space."),
            (["quantum"], "Long-tail data under PQ risk",
             "Decade-long claim files and reinsurance treaties create deep harvest-now-decrypt-later exposure; cryptographic estates are undocumented."),
        ],
        "regs": [
            ("Solvency II / NAIC RBC regimes", "reserving, capital and model governance under supervisory review"),
            ("EIOPA / state DOIs AI guidance", "pricing models and automated decisions under fairness and explainability expectations"),
            ("GDPR / HIPAA-adjacent health data", "sensitive-category handling, retention and DSAR duties"),
            ("DORA (for EU insurers)", "ICT third-party and resilience obligations like banking peers"),
            ("AML/CTF obligations", "premium and payout channels under financial-crime monitoring"),
            ("IFRS 17 / LDTI accounting", "data and actuarial pipeline discipline for new reporting bases"),
        ],
        "kpis": [
            ("Claims cycle time (FNOL to decision)", "down 40-60% on triaged flows"),
            ("Underwriting submission turnaround", "hours for SME classes with agentic workbenches"),
            ("Fraud detection uplift", "+20-30% capture with network analytics at stable SIU capacity"),
            ("Combined-ratio contribution from loss adjustment expense", "measurable reduction on automated flows"),
            ("Model filing preparation effort", "down 50% with documentation-as-you-build"),
        ],
        "priorities": [
            ("Claims as a decision pipeline", "document intelligence and decision hubs moving FNOL-to-decision from days to hours with audit replay"),
            ("Pricing governance that scales", "model inventory, validation tooling and filing-grade documentation produced during build"),
            ("Distribution-ready underwriting rails", "API-first quoting and policy servicing for embedded and ecosystem partners"),
        ],
        "usecases": {
            "applied-ai": [
                ("Underwriting workbench assistant", "submissions summarized with citations to loss runs, exposure data and appetite rules", "quote turnaround down 50% for SME lines"),
                ("Claims adjuster copilot", "policy, coverage and prior-claims context assembled per file with grounding", "adjuster handling time down 30%"),
            ],
            "agentic": [
                ("FNOL triage agent", "documents classified, extracted and routed with confidence thresholds; straight-through for clean claims", "triage queue clearance in minutes"),
                ("Fraud network decision hub", "entity-link analytics scoring claims and applications against ring patterns", "organized-fraud capture up 25%+"),
            ],
            "data": [
                ("Portfolio pricing lakehouse", "exposure, claims and external data unified with lineage for actuarial and filing use", "loss triangle assembly from months to days"),
                ("Reserving analytics workbench", "triangle pipelines, chain-ladder and ML hybrids with actuarial-in-command controls", "reserve review cycles shortened materially"),
            ],
            "cyber": [
                ("Sensitive-data protection program", "classification-aware DLP, encryption policy and access analytics across health/financial stores", "breach-surface measurable and shrinking"),
                ("TPA and broker security gating", "third-party risk tiers, access reviews and evidence automation", "vendor assessments automated"),
            ],
            "cloud": [
                ("Policy admin modernization", "strangler decomposition of core wrappers with parallel-run equivalence testing", "product change lead time cut in half"),
                ("Claims platform FinOps", "unit cost per claim instrumented across document, scoring and adjuster stages", "processing unit cost down 25%+"),
            ],
            "quantum": [
                ("Catastrophe portfolio optimization", "reinsurance structure benchmarked across classical and quantum-inspired solvers", "structure search time compressed"),
                ("PQC for long-tail claim archives", "CBOM and exposure ranking for decade-retention records", "archives prioritized before regulatory pressure"),
            ],
            "blockchain": [
                ("Reinsurance settlement network", "permissioned DLT for treaty settlement evidence between cedants and reinsurers", "settlement reconciliation effort down 60%"),
                ("Parametric trigger products", "oracle-verified triggers with audited contracts for weather/catastrophe covers", "payout cycles from weeks to days"),
            ],
            "iot": [
                ("Commercial property risk telemetry", "water, temperature and vibration sensors pricing and preventing perils", "water-damage frequency down on instrumented sites"),
                ("Fleet telematics underwriting feed", "event-based driving data into pricing and claims verification", "pricing factors enriched at event time"),
            ],
        },
    },

    "healthcare": {
        "name": "Healthcare & Life Sciences",
        "slug": "healthcare-life-sciences",
        "tagline": "Clinical-grade AI, interoperable data and secure estates — outcomes with governance attached.",
        "intro": [
            "Healthcare generates the most consequential data in the economy and spends most of it unread. Radiology backlogs, prior-authorization ping-pong, coding leakage, clinical trial recruitment shortfalls — each is an information problem wearing an operational costume. The organizations improving outcomes are the ones treating data interoperability (FHIR, TEFCA-style exchange) and clinical-grade AI governance as infrastructure, not innovation theater.",
            "The regulatory bar is the highest in any industry: HIPAA and GDPR privacy regimes, FDA oversight where software informs clinical decisions, EU AI Act classification for medical AI, and GxP validation for pharma-adjacent systems. That bar is passable — but only when controls, documentation and validation are designed into delivery from the first sprint, which is precisely how Achala IT Solutions builds.",
            "We work with hospital systems, payers, pharma and biotech, and device makers: ambient clinical documentation that returns hours to clinicians, imaging and multimodal triage inside radiology workflows, prior-authorization agents that read policies and clinical notes, real-world-evidence pipelines on governed data, and zero-trust estates that assume breach because PHI concentrates breach value.",
        ],
        "pressures": [
            (["applied-ai"], "Clinician burden and documentation debt",
             "Physicians spend hours daily on notes, orders and inbox; burnout drives attrition. Documentation AI exists but stalls on integration with the EHR and on compliance sign-off."),
            (["agentic"], "Prior authorization and RCM friction",
             "Prior auth, coding and denial management consume staff across payer-provider boundaries. Denials arrive for documentation that existed but was never surfaced."),
            (["data"], "Interoperability gaps despite FHIR mandates",
             "Imaging, genomics, claims and social determinants live in separate estates; exchange compliance is achieved technically but decision support still reads silos."),
            (["cyber"], "PHI concentration and ransomware exposure",
             "Health records carry the highest breach value; ransomware has shuttered hospitals. Legacy devices and third-party vendors widen the surface beyond the IT team's control."),
            (["applied-ai"], "Imaging and diagnostic backlogs",
             "Radiology and pathology queues grow while reporting stays manual; AI triage exists but sits outside the clinical workflow, so nobody acts on it."),
            (["data"], "Trial recruitment and RWE pipelines manual",
             "Protocol eligibility matching against EHR data remains chart-review work; real-world evidence assemblies take months per study."),
            (["cloud"], "Validated-environment rigidity",
             "GxP validation and change control make cloud adoption feel impossible, so analytics run on desktop extracts with no lineage."),
            (["quantum"], "Genomic and longitudinal data exposure",
             "Genomes and decade-long clinical histories are the definition of long-lived secrets; cryptographic posture is undocumented."),
        ],
        "regs": [
            ("HIPAA / HITECH", "PHI safeguards, BAAs, breach notification and audit trails"),
            ("GDPR / EU health-data regimes", "special-category data, DPIAs and cross-border transfer controls"),
            ("FDA SaMD / CDS guidance", "clinical decision support under enforcement discretion boundaries and validation duties"),
            ("EU AI Act", "medical AI classified high-risk: documentation, human oversight, post-market monitoring"),
            ("GxP / GCP validation", "computerized-system validation for pharma and trial systems"),
            ("HL7 FHIR / TEFCA-style exchange", "interoperability obligations for access and exchange"),
        ],
        "kpis": [
            ("Clinician documentation time", "down 20-35% with ambient documentation inside the EHR"),
            ("Radiology reporting turnaround", "down 30-50% with workflow-integrated triage"),
            ("Prior-authorization cycle time", "down 50-70% with agentic assembly and submission"),
            ("Claim denial overturn rate", "up sharply when documentation is auto-surfaced"),
            ("Trial pre-screening throughput", "10x chart-review equivalent on governed cohorts"),
        ],
        "priorities": [
            ("Clinical AI inside the workflow, not beside it", "EHR-integrated documentation, triage and coding with clinical governance boards and autonomy ladders"),
            ("Interoperable data as infrastructure", "FHIR-native pipelines, terminologies (SNOMED, LOINC, ICD) and lineage for every analytic"),
            ("Assume-breach security for PHI", "zero-trust estates, medical-device segmentation and rehearsed clinical-continuity playbooks"),
        ],
        "usecases": {
            "applied-ai": [
                ("Ambient clinical documentation", "visit audio to structured draft notes in EHR templates with clinician sign-off", "documentation time down 25%+"),
                ("Radiology triage and report drafting", "study prioritization and structured draft findings inside PACS workflow", "report turnaround down 35%"),
            ],
            "agentic": [
                ("Prior-auth assembly agent", "policy criteria mapped to chart evidence; submissions and appeals assembled automatically", "prior-auth cycle time down 60%"),
                ("Denial management agent", "payer denial letters parsed, evidence assembled, appeal packets drafted", "overturn rate up 20-30%"),
            ],
            "data": [
                ("Clinical data platform", "EHR, imaging, genomics and claims on FHIR-native governed foundations with terminology services", "cohort queries in minutes with lineage"),
                ("RWE pipeline", "protocol-driven evidence assembly with provenance for regulatory-grade studies", "evidence assembly from months to weeks"),
            ],
            "cyber": [
                ("Zero-trust clinical estate", "identity-centric access, device posture and segmentation across hospitals and clinics", "ransomware blast radius contained in tabletop evidence"),
                ("Medical-device segmentation", "IEC 80001-informed zoning for legacy devices with monitoring", "unmanaged device surface made visible and controlled"),
            ],
            "cloud": [
                ("Validated cloud analytics", "GxP-aligned validation pipelines on cloud with documented equivalence", "analytics modernization without losing validation status"),
                ("Imaging storage economics", "tiered DICOM archives with cost telemetry", "storage unit cost down 30-40%"),
            ],
            "quantum": [
                ("Protein/materials simulation pilots", "quantum vs. classical benchmarking on chemistry-adjacent workloads", "honest verdicts with revisit triggers"),
                ("PQC for genomic archives", "CBOM and migration sequencing for decade-retention sequences", "genomic data protected ahead of the clock"),
            ],
            "blockchain": [
                ("Credentialing network", "verifiable credentials for clinician licenses and privileges across institutions", "onboarding verification from weeks to days"),
                ("Trial consent integrity", "anchored consent records with versioned protocols", "audit-ready consent evidence"),
            ],
            "iot": [
                ("Clinical asset intelligence", "infusion pumps, imaging and mobile assets tracked with telemetry and maintenance prediction", "asset uptime and utilization up"),
                ("Remote monitoring programs", "device telemetry into care pathways with alert governance", "readmission risk flagged earlier"),
            ],
        },
    },

    "manufacturing": {
        "name": "Manufacturing & Industrial",
        "slug": "manufacturing",
        "tagline": "Self-correcting plants — sensor fabric, twins and agentic operations on the shop floor.",
        "intro": [
            "Manufacturing's competitive frontier has moved from automation of motion to automation of judgment: inspection decisions, scheduling trade-offs, maintenance windows, quality escapes. The plants compounding advantage run governed telemetry into physics-informed models into closed loops — and their workers trust the system because it predicts, explains and hands off cleanly when it is wrong.",
            "Structural pressure is permanent: skilled-labor scarcity deepens, energy costs reshape process economics, supply chains re-fragment geopolitically, and customers demand lot-level traceability. Meanwhile IT/OT convergence (IEC 62443) turns the plant network from an afterthought into a regulated, segmented, monitored estate — a program, not a project.",
            "Achala IT Solutions delivers the operations stack: retrofit sensor fabric on brownfield lines, computer vision inspection and safety analytics at the edge, digital twins for capacity decisions, predictive maintenance wired into CMMS work orders, agentic scheduling assistants for planners, and quality analytics that trace escapes to root cause across process telemetry.",
        ],
        "pressures": [
            (["iot"], "Brownfield instrumentation gap",
             "Critical assets run uninstrumented because gut-and-replace is unthinkable; the data that twins and models need does not exist, and downtime for retrofit is unaffordable."),
            (["iot", "applied-ai"], "Quality escapes and manual inspection",
             "Defect detection depends on sampling and eyes; escapes reach customers, and scrap/rework costs hide in the P&L. Vision systems stall in pilot because lighting, thresholds and line integration were never engineered."),
            (["agentic"], "Planning by spreadsheet under volatility",
             "Planners fight demand volatility, material shortages and changeovers in spreadsheets; scheduling knowledge lives in two veterans' heads. OEE losses from changeover and waiting are structurally accepted."),
            (["cyber"], "IT/OT convergence exposure",
             "Plant networks flatten as sensors and remote access multiply; legacy HMIs and flat topologies make ransomware and sabotage credible threats with physical consequences."),
            (["data"], "MES/ERP/quality data silos",
             "Process telemetry, quality records and ERP lots never meet; root-cause analysis takes weeks of manual correlation when a customer complaint arrives."),
            (["cloud"], "Energy and OEE economics unmeasured",
             "Energy per unit and OEE components lack trustworthy telemetry, so improvement programs guess. Corporate ESG reporting for plants is a spreadsheet festival."),
            (["agentic"], "Maintenance planning reactive",
             "PM schedules fire by calendar while failures happen by physics; planners cannot see which assets are trending toward failure this week."),
            (["quantum"], "Scheduling at combinatorial scale",
             "Job-shop scheduling and changeover optimization hit classical solver ceilings at plant complexity; better sequences are left on the table."),
        ],
        "regs": [
            ("IEC 62443", "industrial cybersecurity zones-and-conduits for OT estates"),
            ("ISO 9001/IATF 16949 quality systems", "traceability and process control evidence for audits"),
            ("EU Machinery / Product regulations & Digital Product Passport", "product-level data obligations approaching"),
            ("NIS2 (EU operators)", "essential-entity cyber duties touching industrial operations"),
            ("ESG reporting (CSRD/ISSB)", "plant-level energy and emissions data with auditability"),
            ("Sector export-control and dual-use rules", "engineering data governance where applicable"),
        ],
        "kpis": [
            ("Unplanned downtime on critical assets", "down 30-50% within a year of instrumented prediction"),
            ("Defect escape rate on instrumented stations", "down sharply with vision closed loops"),
            ("OEE uplift", "+5-10 points from scheduling, changeover and waiting-loss recovery"),
            ("Energy cost per unit", "down 10-20% with metered optimization"),
            ("Root-cause investigation time", "from weeks to hours with correlated telemetry"),
        ],
        "priorities": [
            ("Instrument the physics that pays", "retrofit sensor fabric starting with failure modes and energy sinks that move OEE and cost per unit"),
            ("Close the loop from prediction to work order", "RUL models and vision alerts wired into CMMS/MES so intelligence becomes scheduled work"),
            ("Segment the plant like a bank", "IEC 62443 zones, monitoring and recovery drills with physical-consequence playbooks"),
        ],
        "usecases": {
            "applied-ai": [
                ("Visual quality inspection", "defect detection and completeness checks closing loops into andon and MES holds", "escape rate down sharply on instrumented stations"),
                ("Process anomaly detection", "multivariate telemetry models flagging drift before scrap is produced", "scrap and rework cost down 15-25%"),
            ],
            "agentic": [
                ("Planning assistant agents", "demand/supply scenarios and changeover-aware sequences proposed to planners", "planner throughput up; OEE waiting losses down"),
                ("Maintenance decision agent", "RUL signals converted into cost-optimal maintenance windows with parts staging", "unplanned downtime down 30-50%"),
            ],
            "data": [
                ("Plant data backbone", "OPC UA/Sparkplug telemetry, MES and quality records unified with lineage", "root cause in hours, not weeks"),
                ("Energy intelligence platform", "meter-level energy analytics with per-unit cost and ESG feeds", "energy cost per unit down 10-20%"),
            ],
            "cyber": [
                ("OT segmentation program", "IEC 62443 zones-and-conduits with monitoring and remote-access control", "flat plant networks eliminated"),
                ("OT recovery playbooks", "restoration-tested backups and manual-fallback procedures for production lines", "recovery time proven in drills"),
            ],
            "cloud": [
                ("Plant edge fabric", "KubeEdge/K3s fleets with offline-first patterns and OTA model updates", "site decisions at millisecond latency"),
                ("Global plant telemetry consolidation", "multi-site streaming into one governed lakehouse", "cross-plant benchmarking becomes real"),
            ],
            "quantum": [
                ("Changeover sequence optimization", "solver tournament on job-shop/changeover formulations", "makespan improvements where hybrid solvers win"),
                ("Materials simulation pilots", "alloy/process formulations benchmarked honestly vs. HPC", "formulation search compressed where advantage shows"),
            ],
            "blockchain": [
                ("Lot traceability network", "custody-anchored traceability across suppliers to satisfy IATF/DPP demands", "recall scoping in minutes"),
                ("Supplier provenance verification", "verifiable credentials for material certifications", "audit evidence automated"),
            ],
            "iot": [
                ("Retrofit sensor fabric", "Ex-rated/industrial sensing on live lines with governed telemetry", "critical assets instrumented without stoppage"),
                ("Digital twin for capacity", "physics+data twin for line reconfiguration and bottleneck decisions", "capital validated before spend"),
            ],
        },
    },

    "retail": {
        "name": "Retail & Consumer Goods",
        "slug": "retail-consumer-goods",
        "tagline": "Margin recovered in milliseconds — pricing, availability, personalization and shelf truth.",
        "intro": [
            "Retail margin is decided in thousands of small decisions a day: the price on the tag, the fill rate on the shelf, the offer in the app, the allocation behind the promotion. Winners industrialize those decisions on live data — demand sensing, price elasticity, availability telemetry — and losers discover the loss later in the margin bridge, unwritten.",
            "The operating environment keeps tightening: marketplace giants set fulfillment expectations, private label squeezes brand premium, retail media becomes a P&L line of its own, and sustainability regulation (packaging, provenance, CSRD-adjacent reporting) turns supply-chain data into a compliance asset. Store estates themselves become sensor networks — computer vision for shelf truth, footfall analytics, energy optimization.",
            "Achala IT Solutions builds the retail decision stack: demand and pricing intelligence on streaming data, agentic replenishment and allocation, personalization platforms with privacy architecture, store-edge vision for shelf and safety, supply-chain twins from supplier to shelf, and retail-media analytics that prove incrementality rather than correlation.",
        ],
        "pressures": [
            (["data"], "Demand signals too slow",
             "Batch demand models react to last week; promotions, weather and local events shift baskets daily. Markdown decisions and replenishment both inherit the lag."),
            (["applied-ai"], "Personalization without privacy architecture",
             "Personalization programs stall between marketing ambition and privacy office veto; consent, preference and profiling rules are retrofitted after launch."),
            (["agentic"], "Replenishment and allocation by rules of thumb",
             "Store allocation, DC replenishment and size-curve decisions run on legacy heuristics; phantom availability and overstock coexist across the network."),
            (["iot"], "Shelf truth unknown",
             "Out-of-stocks, planogram compliance and shrink are discovered at audit; store camera estates sit unanalyzed while OOS costs margin silently."),
            (["data"], "Retail media measurement contested",
             "Vendors claim incrementality with last-touch logic; the retailer cannot arbitrate because clean-room measurement does not exist."),
            (["cloud"], "Peak-season elasticity unmanaged",
             "Black Friday peaks break cost models; nobody can state cost per order at P95, and cloud spend spikes are discovered on invoices."),
            (["blockchain"], "Provenance claims unverifiable",
             "Organic, recycled-content and origin claims face greenwashing scrutiny; evidence lives in supplier PDFs."),
            (["agentic"], "Supplier collaboration by email",
             "PO changes, OTIF exceptions and forecast sharing run on email chains; supplier risk surfaces as missed deliveries."),
        ],
        "regs": [
            ("GDPR/CCPA and consent regimes", "profiling, consent and preference management duties"),
            ("EU AI Act transparency", "personalization and pricing automation disclosure expectations"),
            ("CSRD/ISSB-adjacent reporting", "scope 3 and packaging data with auditability"),
            ("EUDR (where applicable)", "deforestation due diligence for relevant commodities"),
            ("PCI DSS 4.0", "payment estate compliance across store and e-commerce"),
            ("Price-transparency/consumer-protection rules", "dynamic pricing constraints by jurisdiction"),
        ],
        "kpis": [
            ("Out-of-stock rate on instrumented categories", "down 20-35%"),
            ("Markdown spend as % of revenue", "down 10-20% with elasticity-driven pricing"),
            ("Personalization conversion lift", "measured incrementality in clean rooms, not last-touch"),
            ("Store energy cost", "down 10-25% on occupancy-aware control"),
            ("Retail media proven incrementality", "clean-room verified for every major campaign"),
        ],
        "priorities": [
            ("Decide at event speed", "streaming demand sensing and decision hubs for pricing, replenishment and allocation"),
            ("Privacy-architected personalization", "consent, clean rooms and profiling governance designed before the first campaign"),
            ("Instrument the store", "shelf-truth vision, energy optimization and safety analytics on the existing camera estate"),
        ],
        "usecases": {
            "applied-ai": [
                ("Demand sensing", "streaming signals (sales, weather, local events, search) into daily SKU-location forecasts", "forecast error down 20-35%"),
                ("Content and offer generation", "product copy and campaign variants generated under brand guardrails with approval flows", "campaign production time down 50%"),
            ],
            "agentic": [
                ("Replenishment and allocation agents", "store/DC replenishment with size-curve logic proposed for planner approval", "OOS down, overstock down simultaneously"),
                ("Supplier exception agent", "PO changes, OTIF misses and forecast revisions orchestrated with supplier portals", "email chains replaced by governed events"),
            ],
            "data": [
                ("Retail decision lakehouse", "POS, loyalty, supply and cost data unified for merchandising and finance", "margin bridge decomposes automatically"),
                ("Clean-room retail media measurement", "retailer-brand joint measurement without data leakage", "incrementality verified per campaign"),
            ],
            "cyber": [
                ("PCI DSS 4.0 program", "tokenization, segmentation and continuous compliance across store estates", "audit evidence continuous, not annual"),
                ("Loyalty and identity protection", "account-takeover detection with step-up authentication", "ATO losses down sharply"),
            ],
            "cloud": [
                ("Peak-readiness engineering", "load modeling, chaos drills and capacity policy for trading peaks", "P95 cost per order known and controlled"),
                ("Store edge compute", "in-store inference for vision and personalization screens", "latency local; WAN costs down"),
            ],
            "quantum": [
                ("Assortment optimization", "solver tournaments on assortment/bin-packing formulations", "assortment refresh cadence up"),
                ("Delivery route optimization", "quantum-inspired routing benchmarked vs. classical for last-mile", "route cost down where solvers win"),
            ],
            "blockchain": [
                ("Provenance verification", "EUDR/DPP-grade chain-of-custody for claim-bearing products", "claims verified, greenwashing risk down"),
                ("Supplier credentials", "verifiable certifications (organic, fair-trade) exchanged cryptographically", "audit evidence automated"),
            ],
            "iot": [
                ("Shelf-truth vision", "OOS, planogram and shrink detection on existing cameras with edge inference", "OOS discovered in minutes"),
                ("Smart building optimization", "occupancy-aware HVAC/lighting across the store portfolio", "energy cost down 10-25%"),
            ],
        },
    },

    "telecom": {
        "name": "Telecom, Media & Entertainment",
        "slug": "telecom-media",
        "tagline": "Network intelligence, churn precision and platform economics — engineered at carrier scale.",
        "intro": [
            "Telcos run the most demanding real-time estate in the private sector — and monetize a fraction of its intelligence. Network telemetry predicts failures before customers notice; usage and experience data predict churn quarters ahead; edge infrastructure positions operators as compute providers, not bit pipes. The gap between what the network knows and what the business acts on is the strategic opportunity.",
            "The pressures are margin-structural: ARPU stagnation against capex cycles, OTT substitution in core services, spectrum and energy costs, and now the AI era's twist — inference demand makes operator edge assets newly valuable while AI-native competitors attack customer ownership. Media arms fight attention economics with content economics and need measurement that investors trust.",
            "Achala IT Solutions builds at carrier scale: network telemetry platforms and AIOps, churn and CLV decision hubs, fraud management for interconnect and subsides, edge compute fabric, monetization data products (insights partnerships under privacy architecture), and for media groups — streaming personalization, ad targeting under consent, and content-performance analytics.",
        ],
        "pressures": [
            (["data"], "Network telemetry underused",
             "Element managers, probes and tickets feed separate systems; NOC decisions remain reactive. The estate generates petabytes that never reach a decision model."),
            (["agentic"], "Churn saves run on campaign calendars",
             "Retention offers fire in monthly batches; in-quarter intent signals (support tickets, usage drops, billing disputes) do not trigger saves in the moment."),
            (["cloud"], "Energy cost compounds",
             "RAN and datacenter energy is the second cost line and rising with traffic; per-site energy lacks telemetry discipline for optimization or ESG reporting."),
            (["cyber"], "Signaling and core exposure",
             "SS7/Diameter weaknesses, API exposure and core-estate sprawl create nation-grade threat surfaces; regulator attention is rising."),
            (["applied-ai"], "Care experiences fail at IVR",
             "Voice self-service deflects without resolving; call volumes migrate to humans with context stripped. Care cost per contact rises while CSAT falls."),
            (["blockchain"], "Interconnect and roaming reconciliation",
             "Wholesale settlement between operators reconciles by file exchange and dispute cycles; evidence is bilateral and contested."),
            (["data"], "Data partnerships stall on privacy",
             "Operator data monetization freezes between opportunity and privacy risk; clean-room and consent architecture do not exist, so everything is declined."),
            (["quantum"], "PQC across a distributed estate",
             "Millions of endpoints, long-lived keys in SIM/eSIM and core signaling face PQ exposure with no inventory."),
        ],
        "regs": [
            ("GDPR and privacy regimes", "subscriber profiling and data-sharing consent duties"),
            ("NIS2 / sector cyber regulation", "essential-entity obligations across network estates"),
            ("EU AI Act", "biometric and profiling constraints shaping AI deployment"),
            ("NERC/sector-specific grid-adjacent rules (where utility-adjacent)", "operational compliance for infrastructure roles"),
            ("Consumer protection on pricing/billing", "dynamic offer disclosure duties"),
            ("Numbering/interconnection regulation", "wholesale obligations with evidence duties"),
        ],
        "kpis": [
            ("Unplanned network outage minutes", "down 30-50% via predictive ops"),
            ("Churn in targeted segments", "down 15-25% with event-triggered saves"),
            ("Care cost per contact", "down 30%+ with resolution-first voice AI"),
            ("Energy per site", "down 10-20% with telemetry-driven optimization"),
            ("Data partnership revenue", "first clean-room products live within two quarters"),
        ],
        "priorities": [
            ("Monetize the network's intelligence", "telemetry backbone into AIOps, experience analytics and sellable insight products under privacy architecture"),
            ("Save churn in the moment", "event-triggered decision hub for retention across care, billing and usage signals"),
            ("Edge as a product", "multi-tenant edge compute fabric with developer platform and SLA discipline"),
        ],
        "usecases": {
            "applied-ai": [
                ("Resolution-first voice care", "grounded voice agents resolving top intents with telephony integration and escalation context", "care cost per contact down 30%"),
                ("Network anomaly narrative models", "telemetry anomalies translated into operator-actionable explanations", "MTTR down on NOC queues"),
            ],
            "agentic": [
                ("Churn-save decision hub", "intent signals trigger personalized save offers within policy in the moment", "segment churn down 15-25%"),
                ("Field-workforce orchestration", "install/repair tasking with skills, parts and SLA routing", "first-time-fix rate up"),
            ],
            "data": [
                ("Network telemetry backbone", "probes, elements and tickets streamed into one governed estate", "NOC decisions on event time"),
                ("Insight data products", "mobility/footfall insights via clean rooms with consent architecture", "first monetized partnership live"),
            ],
            "cyber": [
                ("Signaling security program", "SS7/Diameter hardening and API exposure management", "attack paths closed with evidence"),
                ("Core zero-trust", "identity-centric access and segmentation across core functions", "lateral movement eliminated in validation"),
            ],
            "cloud": [
                ("Edge compute fabric", "KubeEdge-class fleets at POPs with developer platform", "edge workloads live with SLAs"),
                ("Energy telemetry and optimization", "per-site energy instrumentation with load-shaping", "energy cost per site down 10-20%"),
            ],
            "quantum": [
                ("PQC for SIM/eSIM and signaling", "CBOM across distributed endpoints with migration waves", "estate sequenced ahead of PQ pressure"),
                ("Network planning optimization", "solver tournaments for capacity/coverage trade-offs", "planning cycles compressed"),
            ],
            "blockchain": [
                ("Wholesale settlement network", "permissioned DLT for interconnect/roaming evidence", "dispute cycles collapsed"),
                ("Number/asset registry", "anchored registries for spectrum-backed assets where applicable", "audit evidence simplified"),
            ],
            "iot": [
                ("Site intelligence", "tower/site environment and security telemetry", "site incidents anticipated"),
                ("Fleet operations", "technician vehicles and assets tracked with maintenance prediction", "fleet availability up"),
            ],
        },
    },
}
