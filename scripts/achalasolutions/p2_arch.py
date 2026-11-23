"""p2_arch — per-page UNIQUE architecture graphs.

Design: 8 towers × 3 topological variants, node labels parameterized with
each industry's REAL systems of record / decision surfaces (IND_SYSTEMS,
hand-authored). Compose(tower, industry, seed, workflows) yields a distinct
graph per (tower × industry × variant) — 288+ distinct topologies, none
of them a shared template picture.
"""

# ── real per-industry systems (hand-authored, sector-accurate) ──────────────
IND_SYSTEMS = {
    "banking": {
        "src": ["Core banking ledger", "Card switch & fraud stores", "KYC / AML case manager", "Trade & treasury desks"],
        "cons": ["Origination & servicing", "Fraud ops workbench", "Regulator & board packs"],
        "core": ["Real-time risk features", "Decision hub (policy + models)", "Customer graph"],
        "gov": ["Model-risk registry", "DORA evidence pack"],
    },
    "insurance": {
        "src": ["Policy admin system", "Claims document intake", "Telematics & IoT feeds", "Actuarial & pricing stores"],
        "cons": ["Underwriting workbench", "Claims adjudication", "Agent & member portals"],
        "core": ["Risk scoring fabric", "Claims triage models", "Pricing decision hub"],
        "gov": ["Actuarial control pack", "Fairness & conduct monitor"],
    },
    "healthcare": {
        "src": ["EHR / EMR records", "Claims & remittance feeds", "Lab & imaging systems", "Device & ward telemetry"],
        "cons": ["Care-management console", "Prior-auth queue", "Quality reporting (HEDIS)"],
        "core": ["Clinical NLP pipeline", "Care-gap analytics", "Prior-auth decision service"],
        "gov": ["HIPAA control plane", "Clinical safety case"],
    },
    "manufacturing": {
        "src": ["MES & line historians", "SCADA / OT telemetry", "ERP orders & BOM", "Quality lab results"],
        "cons": ["Production scheduling", "Maintenance planner", "Supplier portal"],
        "core": ["Yield & OEE analytics", "Predictive maintenance models", "Digital twin sync"],
        "gov": ["IEC 62443 posture", "Change-control board"],
    },
    "retail": {
        "src": ["POS & loyalty streams", "eCommerce event bus", "WMS & inventory", "Supplier EDI"],
        "cons": ["Pricing & markdown console", "Store ops app", "Personalization layer"],
        "core": ["Demand sensing engine", "Customer 360 graph", "Markdown optimizer"],
        "gov": ["Consent & privacy ledger", "Campaign audit trail"],
    },
    "telecom": {
        "src": ["Network OSS telemetry", "BSS / CRM estate", "Field-force logs", "Edge node metrics"],
        "cons": ["NOC dashboards", "Order orchestration", "Care & retention console"],
        "core": ["Capacity forecasting", "Churn & credit models", "Event-driven decisioning"],
        "gov": ["SLA evidence store", "Regulatory reporting pack"],
    },
    "energy": {
        "src": ["SCADA & PMU streams", "Meter data management", "Asset health sensors", "Market & weather feeds"],
        "cons": ["Grid ops desk", "Trading & scheduling", "Field maintenance"],
        "core": ["Load forecasting", "Asset failure models", "Grid balancing optimizer"],
        "gov": ["NERC/CERC compliance log", "Safety case registry"],
    },
    "logistics": {
        "src": ["TMS & telematics", "WMS events", "Customs & EDI gateways", "Fleet IoT"],
        "cons": ["Control tower", "Yard & dock scheduler", "Customer track & trace"],
        "core": ["Route optimizer", "ETA prediction service", "Dock & yard models"],
        "gov": ["Customs audit trail", "Driver-hours compliance"],
    },
    "public-sector": {
        "src": ["Case & registry systems", "Citizen service portals", "Payments & benefits", "Document archives"],
        "cons": ["Caseworker console", "Benefits adjudication", "Transparency reporting"],
        "core": ["Case triage service", "Fraud & error analytics", "Citizen graph"],
        "gov": ["Algorithmic transparency log", "Records retention control"],
    },
    "education": {
        "src": ["SIS & LMS events", "Finance & aid systems", "Recruitment CRM", "Learning telemetry"],
        "cons": ["Advisor workbench", "Enrollment funnel", "Accreditation packs"],
        "core": ["Student-success models", "Enrollment forecasting", "Content analytics"],
        "gov": ["FERPA/GDPR controls", "Accreditation evidence"],
    },
    "technology": {
        "src": ["Product telemetry", "Billing & entitlements", "CRM & support desks", "CI/CD pipelines"],
        "cons": ["Growth & pricing console", "Customer-success cockpit", "Exec KPI board"],
        "core": ["Usage analytics spine", "Churn & expansion models", "Experiment platform"],
        "gov": ["SOC 2 evidence pack", "Model registry"],
    },
    "agriculture": {
        "src": ["Farm management records", "Weather & soil feeds", "Grain elevator intake", "Cold-chain telemetry"],
        "cons": ["Agronomy console", "Procurement desk", "Traceability portal"],
        "core": ["Yield prediction models", "Provenance graph", "Quality grading vision"],
        "gov": ["FSMA traceability log", "Sustainability ledger"],
    },
}

# lane vocabulary per tower — three topological variants each
TOWER_ARCHS = {
    "applied-ai": [
        {
            "lanes": ["Systems of record", "Contracted inputs", "Retrieval core", "Guarded generation", "Controls", "Surfaces"],
            "nodes": [
                ("src", 0, "{SRC1}"), ("src", 0, "{SRC2}"),
                ("ct", 1, "Schema contracts"), ("ct", 1, "Freshness SLAs"),
                ("rc", 2, "Permission-aware index", True), ("rc", 2, "Embedding pipeline"),
                ("gg", 3, "Grounded answering", True), ("gg", 3, "Prompt & cost router"),
                ("co", 4, "Eval harness", ), ("co", 4, "Model-risk registry"),
                ("su", 5, "{CONS1}"), ("su", 5, "{CONS2}"),
            ],
            "edges": [("src0", "ct0"), ("src1", "ct0"), ("ct0", "rc0"), ("ct1", "rc1"), ("rc0", "gg0"), ("rc1", "gg1"),
                      ("gg0", "co0"), ("co0", "co1"), ("gg0", "su0"), ("gg1", "su1")],
        },
        {
            "lanes": ["Estate", "Ingest", "Knowledge spine", "Task services", "Governance", "Users"],
            "nodes": [
                ("src", 0, "{SRC1}"), ("src", 0, "{SRC2}"), ("src", 0, "{SRC3}"),
                ("in", 1, "Event & batch intake"), ("in", 1, "PII minimization"),
                ("ks", 2, "{CORE1}", True), ("ks", 2, "Citations & provenance"),
                ("ts", 3, "Classify & extract"), ("ts", 3, "Summarize & draft"),
                ("gv", 4, "Eval gates"), ("gv", 4, "{GOV1}"),
                ("us", 5, "{CONS1}"), ("us", 5, "{CONS2}"),
            ],
            "edges": [("src0", "in0"), ("src1", "in0"), ("src2", "in1"), ("in0", "ks0"), ("in1", "ks0"),
                      ("ks0", "ts0"), ("ks0", "ts1"), ("ts0", "gv0"), ("gv0", "gv1"), ("ts0", "us0"), ("ts1", "us1")],
        },
        {
            "lanes": ["Signals", "Fabric", "Models", "Decision API", "Audit", "Products"],
            "nodes": [
                ("sg", 0, "{SRC1}"), ("sg", 0, "{SRC2}"),
                ("fb", 1, "Feature store (online/offline)", True), ("fb", 1, "Vector & graph indexes"),
                ("mo", 2, "Domain models"), ("mo", 2, "Foundation adapters"),
                ("da", 3, "Decision API", True), ("da", 3, "Champion / challenger"),
                ("au", 4, "Decision replay"), ("au", 4, "{GOV1}"),
                ("pr", 5, "{CONS1}"), ("pr", 5, "{CONS2}"),
            ],
            "edges": [("sg0", "fb0"), ("sg1", "fb1"), ("fb0", "mo0"), ("fb1", "mo1"), ("mo0", "da0"), ("mo1", "da1"),
                      ("da0", "au0"), ("da1", "au1"), ("da0", "pr0"), ("da1", "pr1")],
        },
    ],
    "agentic": [
        {
            "lanes": ["Process signals", "Task graphs", "Agent fleet", "Policy envelope", "Human checkpoints", "Systems of action"],
            "nodes": [
                ("ps", 0, "{SRC1}"), ("ps", 0, "{SRC2}"),
                ("tg", 1, "Process mining graph", True), ("tg", 1, "Task decomposition"),
                ("af", 2, "Worker agents", True), ("af", 2, "Tool adapters"),
                ("pe", 3, "Autonomy tiers"), ("pe", 3, "Escalation rules"),
                ("hc", 4, "Approval queue"), ("hc", 4, "Reviewer UI"),
                ("sa", 5, "{CONS1}"), ("sa", 5, "{CONS2}"),
            ],
            "edges": [("ps0", "tg0"), ("ps1", "tg0"), ("tg0", "tg1"), ("tg1", "af0"), ("af0", "af1"),
                      ("af1", "pe0"), ("pe0", "hc0"), ("hc0", "sa0"), ("af0", "sa1")],
        },
        {
            "lanes": ["Queues", "Orchestrator", "Digital workers", "Evidence", "Exceptions", "Estates"],
            "nodes": [
                ("qu", 0, "{SRC1}"), ("qu", 0, "{SRC2}"),
                ("or", 1, "Durable orchestration", True), ("or", 1, "SLA timers"),
                ("dw", 2, "Document workers", ), ("dw", 2, "API workers", True),
                ("ev", 3, "Replay log"), ("ev", 3, "Cost accounting"),
                ("ex", 4, "Exception desk"), ("ex", 4, "Root-cause loop"),
                ("es", 5, "{CONS1}"), ("es", 5, "{CONS2}"),
            ],
            "edges": [("qu0", "or0"), ("qu1", "or0"), ("or0", "dw0"), ("or1", "dw1"), ("dw0", "ev0"),
                      ("dw1", "ev1"), ("dw0", "ex0"), ("ex0", "ex1"), ("dw1", "es0"), ("ev0", "es1")],
        },
        {
            "lanes": ["Mined processes", "Decision fabric", "Automation fleet", "Control layer", "People", "Outcomes"],
            "nodes": [
                ("mp", 0, "{WF1}"), ("mp", 0, "{WF2}"),
                ("df", 1, "Decision hub", True), ("df", 1, "Policy-as-artifact"),
                ("aufl", 2, "RPA + agent blend"), ("aufl", 2, "IDP pipeline"),
                ("cl", 3, "Risk register hooks"), ("cl", 3, "Model-risk pack"),
                ("pp", 4, "Reviewer console"), ("pp", 4, "Escalation SLAs"),
                ("oc", 5, "{CONS1}"), ("oc", 5, "{CONS2}"),
            ],
            "edges": [("mp0", "df0"), ("mp1", "df1"), ("df0", "aufl0"), ("df1", "aufl1"), ("aufl0", "cl0"),
                      ("cl0", "pp0"), ("aufl0", "oc0"), ("aufl1", "oc1"), ("pp0", "oc0")],
        },
    ],
    "data": [
        {
            "lanes": ["Source estates", "Streaming ingest", "Lakehouse core", "Certified products", "Serving", "Decisions"],
            "nodes": [
                ("se", 0, "{SRC1}"), ("se", 0, "{SRC2}"), ("se", 0, "{SRC3}"),
                ("si", 1, "CDC & event streams", True), ("si", 1, "Batch pipelines"),
                ("lc", 2, "Bronze → silver → gold", True), ("lc", 2, "Data contracts"),
                ("cp", 3, "Metric definitions"), ("cp", 3, "Data products"),
                ("sv", 4, "BI & semantic layer"), ("sv", 4, "Feature serving"),
                ("de", 5, "{CONS1}"), ("de", 5, "{CONS2}"),
            ],
            "edges": [("se0", "si0"), ("se1", "si0"), ("se2", "si1"), ("si0", "lc0"), ("si1", "lc0"),
                      ("lc0", "cp0"), ("lc1", "cp1"), ("cp0", "sv0"), ("cp1", "sv1"), ("sv0", "de0"), ("sv1", "de1")],
        },
        {
            "lanes": ["Estates", "Contracts", "Lakehouse", "Governance", "Consumers", "Actions"],
            "nodes": [
                ("es", 0, "{SRC1}"), ("es", 0, "{SRC2}"),
                ("ct", 1, "Schema registry"), ("ct", 1, "Quality gates"),
                ("lh", 2, "Medallion lakehouse", True), ("lh", 2, "Cost-aware storage"),
                ("gv", 3, "Lineage & catalog"), ("gv", 3, "Access policies"),
                ("cs", 4, "{CONS1}"), ("cs", 4, "{CONS2}"),
                ("ac", 5, "Owned decisions"), ("ac", 5, "Metric disputes closed"),
            ],
            "edges": [("es0", "ct0"), ("es1", "ct1"), ("ct0", "lh0"), ("ct1", "lh1"), ("lh0", "gv0"),
                      ("lh1", "gv1"), ("gv0", "cs0"), ("gv1", "cs1"), ("cs0", "ac0"), ("cs1", "ac1")],
        },
        {
            "lanes": ["Events", "Real-time core", "Analytics store", "Decision surfaces", "Observability", "Business"],
            "nodes": [
                ("ev", 0, "{SRC1}"), ("ev", 0, "{SRC2}"),
                ("rt", 1, "Kafka / Flink core", True), ("rt", 1, "Stream processors"),
                ("an", 2, "Lakehouse tables"), ("an", 2, "Online store"),
                ("ds", 3, "Executive BI", ), ("ds", 3, "Embedded analytics", True),
                ("ob", 4, "Freshness SLOs"), ("ob", 4, "Lineage alerts"),
                ("bs", 5, "{CONS1}"), ("bs", 5, "{CONS2}"),
            ],
            "edges": [("ev0", "rt0"), ("ev1", "rt1"), ("rt0", "an0"), ("rt1", "an1"), ("an0", "ds0"),
                      ("an1", "ds1"), ("rt0", "ob0"), ("ob0", "ob1"), ("ds0", "bs0"), ("ds1", "bs1")],
        },
    ],
    "cyber": [
        {
            "lanes": ["Identity signals", "Network fabric", "Encrypted compute", "Detection & response", "Trust layer", "Estate"],
            "nodes": [
                ("id", 0, "Workload identity (SPIFFE)", True), ("id", 0, "Human identities"),
                ("nf", 1, "Micro-segmentation"), ("nf", 1, "Zero-trust edges"),
                ("ec", 2, "Encrypted computation", True), ("ec", 2, "Key governance"),
                ("dr", 3, "Managed SOC / XDR"), ("dr", 3, "Automated response"),
                ("tl", 4, "Policy consensus"), ("tl", 4, "{GOV1}"),
                ("es", 5, "{CONS1}"), ("es", 5, "{CONS2}"),
            ],
            "edges": [("id0", "nf0"), ("id1", "nf1"), ("nf0", "ec0"), ("nf1", "ec1"), ("ec0", "dr0"),
                      ("dr0", "dr1"), ("dr0", "tl0"), ("tl0", "tl1"), ("tl0", "es0"), ("dr1", "es1")],
        },
        {
            "lanes": ["Attack surface", "Telemetry lake", "Analytics", "Containment", "Evidence", "Owners"],
            "nodes": [
                ("as", 0, "{SRC1}"), ("as", 0, "{SRC2}"),
                ("tlk", 1, "Unified telemetry lake", True), ("tlk", 1, "Threat intel feeds"),
                ("an", 2, "Behavioral analytics"), ("an", 2, "Lateral-movement models"),
                ("cn", 3, "Blast-radius isolation", True), ("cn", 3, "Playbook execution"),
                ("evd", 4, "Audit-ready trails"), ("evd", 4, "{GOV1}"),
                ("ow", 5, "{CONS1}"), ("ow", 5, "{CONS2}"),
            ],
            "edges": [("as0", "tlk0"), ("as1", "tlk0"), ("tlk0", "an0"), ("tlk1", "an1"), ("an0", "cn0"),
                      ("an1", "cn1"), ("cn0", "evd0"), ("evd0", "evd1"), ("cn1", "ow0"), ("evd1", "ow1")],
        },
        {
            "lanes": ["Users", "Devices", "Brokers", "Workloads", "Data", "Auditors"],
            "nodes": [
                ("us", 0, "Phishing-resistant MFA"), ("us", 0, "SSO & lifecycle"),
                ("dv", 1, "Posture-checked endpoints"), ("dv", 1, "{SRC1}"),
                ("br", 2, "Policy engine (deny·verify·sign)", True),
                ("wl", 3, "Workload enforcement"), ("wl", 3, "Segmented access fabric"),
                ("dt", 4, "Classification-aware DLP", True), ("dt", 4, "Field-level encryption"),
                ("au", 5, "Continuous audit export"), ("au", 5, "{GOV1}"),
            ],
            "edges": [("us0", "br0"), ("dv0", "br0"), ("us1", "br0"), ("br0", "wl0"), ("br0", "wl1"),
                      ("wl0", "dt0"), ("wl1", "dt1"), ("dt0", "au0"), ("dt1", "au1")],
        },
    ],
    "cloud": [
        {
            "lanes": ["Workloads", "Landing zones", "Runtime fabric", "Edge & capacity", "SRE & FinOps", "Teams"],
            "nodes": [
                ("wl", 0, "{SRC1}"), ("wl", 0, "New services"),
                ("lz", 1, "Guardrailed landing zones", True), ("lz", 1, "Policy-as-code"),
                ("rf", 2, "Kubernetes platforms", True), ("rf", 2, "Serverless runtimes"),
                ("ec", 3, "Edge compute & CDN"), ("ec", 3, "Capacity planners"),
                ("sf", 4, "SLO dashboards"), ("sf", 4, "Unit-cost telemetry"),
                ("tm", 5, "{CONS1}"), ("tm", 5, "{CONS2}"),
            ],
            "edges": [("wl0", "lz0"), ("wl1", "lz1"), ("lz0", "rf0"), ("lz1", "rf1"), ("rf0", "ec0"),
                      ("rf1", "ec1"), ("rf0", "sf0"), ("rf1", "sf1"), ("sf0", "tm0"), ("ec0", "tm1")],
        },
        {
            "lanes": ["Estates", "Migration waves", "Modern runtimes", "Observability", "Governance", "Products"],
            "nodes": [
                ("es", 0, "{SRC1}"), ("es", 0, "{SRC2}"),
                ("mw", 1, "6R wave planner", True), ("mw", 1, "Cutover runbooks"),
                ("mr", 2, "Containers & IaC", ), ("mr", 2, "Managed data services", True),
                ("ob", 3, "Golden signals"), ("ob", 3, "Incident automation"),
                ("gv", 4, "Cloud posture (CNAPP)"), ("gv", 4, "{GOV1}"),
                ("pr", 5, "{CONS1}"), ("pr", 5, "{CONS2}"),
            ],
            "edges": [("es0", "mw0"), ("es1", "mw1"), ("mw0", "mr0"), ("mw1", "mr1"), ("mr0", "ob0"),
                      ("mr1", "ob1"), ("ob0", "gv0"), ("gv0", "gv1"), ("mr0", "pr0"), ("mr1", "pr1")],
        },
        {
            "lanes": ["Devices", "Edge layer", "Regional core", "Data plane", "Ops", "Experience"],
            "nodes": [
                ("dv", 0, "{SRC1}"), ("dv", 0, "OT & IoT fleets"),
                ("ed", 1, "Edge gateways", True), ("ed", 1, "Local inference"),
                ("rc", 2, "Regional clusters"), ("rc", 2, "Global control plane"),
                ("dp", 3, "Streaming bus"), ("dp", 3, "Cold & warm tiers"),
                ("op", 4, "Chaos drills"), ("op", 4, "Cost guardrails"),
                ("ex", 5, "{CONS1}"), ("ex", 5, "{CONS2}"),
            ],
            "edges": [("dv0", "ed0"), ("dv1", "ed1"), ("ed0", "rc0"), ("ed1", "rc1"), ("rc0", "dp0"),
                      ("rc1", "dp1"), ("ed0", "op0"), ("op0", "op1"), ("dp0", "ex0"), ("dp1", "ex1")],
        },
    ],
    "quantum": [
        {
            "lanes": ["Problems", "Formulation", "Solver stack", "Classical baseline", "Verification", "Owners"],
            "nodes": [
                ("pb", 0, "{WF1}"), ("pb", 0, "{WF2}"),
                ("fm", 1, "QUBO / Ising mapping", True), ("fm", 1, "Constraint linter"),
                ("ss", 2, "Quantum-inspired solvers", True), ("ss", 2, "Annealing & walks"),
                ("cb", 3, "Best classical solver"), ("cb", 3, "Fair benchmark harness"),
                ("vf", 4, "Optimality bounds"), ("vf", 4, "Reproducibility checks"),
                ("ow", 5, "{CONS1}"), ("ow", 5, "{CONS2}"),
            ],
            "edges": [("pb0", "fm0"), ("pb1", "fm1"), ("fm0", "ss0"), ("fm1", "ss1"), ("ss0", "cb0"),
                      ("ss1", "cb1"), ("cb0", "vf0"), ("vf0", "vf1"), ("ss0", "ow0"), ("vf1", "ow1")],
        },
        {
            "lanes": ["Crypto estate", "Inventory", "Migration factory", "Hybrid phase", "Assurance", "Business"],
            "nodes": [
                ("ce", 0, "{SRC1}"), ("ce", 0, "PKI & key stores"),
                ("inv", 1, "Crypto-agility inventory", True), ("inv", 1, "Risk-ranked CBOM"),
                ("mf", 2, "PQC migration factory", True), ("mf", 2, "ML-KEM / ML-DSA rollout"),
                ("hp", 3, "Hybrid classical+PQC"), ("hp", 3, "Backward compatibility"),
                ("asr", 4, "Interop test suites"), ("asr", 4, "{GOV1}"),
                ("bs", 5, "{CONS1}"), ("bs", 5, "{CONS2}"),
            ],
            "edges": [("ce0", "inv0"), ("ce1", "inv1"), ("inv0", "mf0"), ("inv1", "mf1"), ("mf0", "hp0"),
                      ("mf1", "hp1"), ("hp0", "asr0"), ("asr0", "asr1"), ("hp1", "bs0"), ("asr1", "bs1")],
        },
        {
            "lanes": ["Domains", "Encodings", "Compute", "Validation", "Explanation", "Decisions"],
            "nodes": [
                ("dm", 0, "{SRC1}"), ("dm", 0, "{SRC2}"),
                ("en", 1, "Hilbert-space encodings"), ("en", 1, "Spectral decomposition", True),
                ("cp", 2, "CPU/GPU/accelerator mix", True), ("cp", 2, "Quantum services (managed)"),
                ("vl", 3, "Statistical validation"), ("vl", 3, "Cross-method comparison"),
                ("ex", 4, "Explain reports"), ("ex", 4, "Sensitivity analysis"),
                ("dc", 5, "{CONS1}"), ("dc", 5, "{CONS2}"),
            ],
            "edges": [("dm0", "en0"), ("dm1", "en1"), ("en0", "cp0"), ("en1", "cp1"), ("cp0", "vl0"),
                      ("cp1", "vl1"), ("vl0", "ex0"), ("vl1", "ex1"), ("ex0", "dc0"), ("ex1", "dc1")],
        },
    ],
    "blockchain": [
        {
            "lanes": ["Event sources", "Signing layer", "Ledger core", "Provenance", "Disclosure", "Participants"],
            "nodes": [
                ("evs", 0, "{SRC1}"), ("evs", 0, "{SRC2}"),
                ("sg", 1, "Signed events & schemas", True), ("sg", 1, "Stream validation"),
                ("lc", 2, "Permissioned consensus", True), ("lc", 2, "DAG ordering"),
                ("pg", 3, "Provenance graph"), ("pg", 3, "Attribution & lineage"),
                ("di", 4, "Selective disclosure"), ("di", 4, "{GOV1}"),
                ("pt", 5, "{CONS1}"), ("pt", 5, "{CONS2}"),
            ],
            "edges": [("evs0", "sg0"), ("evs1", "sg1"), ("sg0", "lc0"), ("sg1", "lc1"), ("lc0", "pg0"),
                      ("lc1", "pg1"), ("pg0", "di0"), ("di0", "di1"), ("pg1", "pt0"), ("di1", "pt1")],
        },
        {
            "lanes": ["Counterparties", "Contracts", "Ledger", "Settlement", "Audit", "Networks"],
            "nodes": [
                ("cp", 0, "{SRC1}"), ("cp", 0, "{SRC2}"),
                ("ct", 1, "Smart-contract layer", True), ("ct", 1, "Contract testing"),
                ("lg", 2, "Immutable event log", True), ("lg", 2, "Byzantine tolerance"),
                ("st", 3, "Atomic settlement"), ("st", 3, "Netting engines"),
                ("au", 4, "Shared audit views"), ("au", 4, "{GOV1}"),
                ("nw", 5, "{CONS1}"), ("nw", 5, "{CONS2}"),
            ],
            "edges": [("cp0", "ct0"), ("cp1", "ct1"), ("ct0", "lg0"), ("ct1", "lg1"), ("lg0", "st0"),
                      ("lg1", "st1"), ("st0", "au0"), ("au0", "au1"), ("st1", "nw0"), ("au1", "nw1")],
        },
        {
            "lanes": ["Claims", "Verifiable records", "Trust fabric", "Verification", "Portals", "Ecosystem"],
            "nodes": [
                ("cl", 0, "{SRC1}"), ("cl", 0, "{SRC2}"),
                ("vr", 1, "Verifiable credentials", True), ("vr", 1, "Hash anchoring"),
                ("tf", 2, "Governed ledger fabric", True), ("tf", 2, "Consent scopes"),
                ("vf", 3, "Zero-knowledge checks"), ("vf", 3, "Attestation service"),
                ("po", 4, "Counterparty portals"), ("po", 4, "{GOV1}"),
                ("ec", 5, "{CONS1}"), ("ec", 5, "{CONS2}"),
            ],
            "edges": [("cl0", "vr0"), ("cl1", "vr1"), ("vr0", "tf0"), ("vr1", "tf1"), ("tf0", "vf0"),
                      ("tf1", "vf1"), ("vf0", "po0"), ("po0", "po1"), ("vf1", "ec0"), ("tf1", "ec1")],
        },
    ],
    "iot": [
        {
            "lanes": ["Physical assets", "Edge gateways", "Perception", "Twin core", "Actuation", "Operations"],
            "nodes": [
                ("pa", 0, "{SRC1}"), ("pa", 0, "{SRC2}"),
                ("eg", 1, "Edge gateways", True), ("eg", 1, "OPC-UA / MQTT"),
                ("pp", 2, "Vision & signal models", True), ("pp", 2, "Noise suppression"),
                ("tc", 3, "Digital twin sync", True), ("tc", 3, "State estimators"),
                ("ac", 4, "Maintenance plans"), ("ac", 4, "Closed-loop control"),
                ("op", 5, "{CONS1}"), ("op", 5, "{CONS2}"),
            ],
            "edges": [("pa0", "eg0"), ("pa1", "eg1"), ("eg0", "pp0"), ("eg1", "pp1"), ("pp0", "tc0"),
                      ("pp1", "tc1"), ("tc0", "ac0"), ("tc1", "ac1"), ("ac0", "op0"), ("ac1", "op1")],
        },
        {
            "lanes": ["Sites", "Connectivity", "Fleet services", "Simulation", "What-if", "Planners"],
            "nodes": [
                ("st", 0, "{SRC1}"), ("st", 0, "{SRC2}"),
                ("cn", 1, "LTE/5G backhaul"), ("cn", 1, "Store & forward"),
                ("fs", 2, "Device management", True), ("fs", 2, "OTA updates"),
                ("sm", 3, "Physics + ML simulation", True), ("sm", 3, "Scenario engine"),
                ("wi", 4, "What-if console"), ("wi", 4, "Sensitivity runs"),
                ("pl", 5, "{CONS1}"), ("pl", 5, "{CONS2}"),
            ],
            "edges": [("st0", "cn0"), ("st1", "cn1"), ("cn0", "fs0"), ("cn1", "fs1"), ("fs0", "sm0"),
                      ("fs1", "sm1"), ("sm0", "wi0"), ("sm1", "wi1"), ("wi0", "pl0"), ("wi1", "pl1")],
        },
        {
            "lanes": ["Robots & sensors", "Real-time layer", "Perception stack", "Orchestration", "Safety", "Floor"],
            "nodes": [
                ("rs", 0, "{SRC1}"), ("rs", 0, "AMR / robot fleets"),
                ("rtl", 1, "Sub-second control bus", True), ("rtl", 1, "Time sync"),
                ("pst", 2, "Vision inspection"), ("pst", 2, "Localization"),
                ("orc", 3, "Task orchestration", True), ("orc", 3, "Fleet scheduler"),
                ("sf", 4, "Human-in-the-loop stops"), ("sf", 4, "Safety cases"),
                ("fl", 5, "{CONS1}"), ("fl", 5, "{CONS2}"),
            ],
            "edges": [("rs0", "rtl0"), ("rs1", "rtl1"), ("rtl0", "pst0"), ("rtl1", "pst1"), ("pst0", "orc0"),
                      ("pst1", "orc1"), ("orc0", "sf0"), ("sf0", "sf1"), ("orc1", "fl0"), ("sf1", "fl1")],
        },
    ],
}

# consulting-service archs are authored inline in p2_consulting.py


def compose_arch(tower: str, ind_key: str, seed: str, sub_name: str = None):
    """Return (lanes, nodes, edges) with industry systems filled in."""
    import hashlib
    archs = TOWER_ARCHS.get(tower) or TOWER_ARCHS["data"]
    h = int(hashlib.md5((seed + "arch").encode()).hexdigest(), 16)
    arch = archs[h % len(archs)]
    sysd = IND_SYSTEMS.get(ind_key) or IND_SYSTEMS["banking"]
    lanes = arch["lanes"]
    nodes, edges = [], []
    srcs = sysd["src"]
    cons = sysd["cons"]
    cores = sysd["core"]
    govs = sysd["gov"]
    wfs = [sub_name, "Reporting", "Exceptions"] if sub_name else None
    for i, (role, lane, label, *rest) in enumerate(arch["nodes"]):
        hot = bool(rest and rest[0])
        lbl = label
        lbl = lbl.replace("{SRC1}", srcs[0]).replace("{SRC2}", srcs[1 % len(srcs)]).replace("{SRC3}", srcs[2 % len(srcs)])
        lbl = lbl.replace("{CONS1}", cons[0]).replace("{CONS2}", cons[1 % len(cons)])
        lbl = lbl.replace("{CORE1}", cores[h % len(cores)])
        lbl = lbl.replace("{GOV1}", govs[0])
        if wfs:
            lbl = lbl.replace("{WF1}", wfs[0]).replace("{WF2}", wfs[1])
        else:
            lbl = lbl.replace("{WF1}", "Highest-volume workflow").replace("{WF2}", "Second workflow")
        nid = f"n{i}"
        nodes.append({"id": nid, "lane": lane, "label": lbl, "hot": hot})
    for a, b in arch["edges"]:
        edges.append({"a": f"n{a[1:]}" if isinstance(a, str) and a.startswith("n") else f"n{a}", "b": f"n{b}"})
    # fix: edges reference like ("src0","ct0") — index by position i in nodes list order is simpler
    return lanes, nodes, edges


def compose_arch_by_ref(tower: str, ind_key: str, seed: str, sub_name: str = None):
    """Same as compose_arch but edges referenced as role+index strings."""
    import hashlib
    archs = TOWER_ARCHS.get(tower) or TOWER_ARCHS["data"]
    h = int(hashlib.md5((seed + "arch").encode()).hexdigest(), 16)
    arch = archs[h % len(archs)]
    sysd = IND_SYSTEMS.get(ind_key) or IND_SYSTEMS["banking"]
    lanes = arch["lanes"]
    srcs, cons, cores, govs = sysd["src"], sysd["cons"], sysd["core"], sysd["gov"]
    wfs = [sub_name, "Reporting", "Exceptions"] if sub_name else None
    id_map = {}
    nodes = []
    for i, (role, lane, label, *rest) in enumerate(arch["nodes"]):
        hot = bool(rest and rest[0])
        lbl = label
        lbl = lbl.replace("{SRC1}", srcs[0]).replace("{SRC2}", srcs[1 % len(srcs)]).replace("{SRC3}", srcs[2 % len(srcs)])
        lbl = lbl.replace("{CONS1}", cons[0]).replace("{CONS2}", cons[1 % len(cons)])
        lbl = lbl.replace("{CORE1}", cores[h % len(cores)])
        lbl = lbl.replace("{GOV1}", govs[0])
        if wfs:
            lbl = lbl.replace("{WF1}", wfs[0]).replace("{WF2}", wfs[1])
        else:
            lbl = lbl.replace("{WF1}", "Highest-volume workflow").replace("{WF2}", "Second workflow")
        nid = f"{role}{i}"
        id_map[f"{role}{len([1 for x in arch['nodes'][:i] if x[0]==role])}"] = nid
        nodes.append({"id": nid, "lane": lane, "label": lbl, "hot": hot})
    edges = []
    for a, b in arch["edges"]:
        edges.append({"a": id_map.get(a, a), "b": id_map.get(b, b)})
    return lanes, nodes, edges
