# -*- coding: utf-8 -*-
"""Achala IT Solutions — 31 authored expansion pages for the website build.
These pages join the 602 drafted pages: 8 leadership profiles, 12 partner
alliance pages, 3 careers subpages, 8 newsroom releases.

Names used on leadership profiles are PLACEHOLDERS flagged `placeholder: true`
and must be replaced with real executives before launch (see README).
Partner pages describe delivery ecosystems; alliance status is 'in validation'
until Achala IT Solutions confirms each partnership legally.
"""

LEADER = [
    # role, slug, name (PLACEHOLDER), mandate, focus areas, bio paragraphs
    ("Chief Executive Officer", "chief-executive-officer", "Adrian R. Menon",
     "Sets the outcome-linked engagement model and the platform-first strategy across the group.",
     ["Group strategy", "Commercial model", "Board advisory"],
     ["The Chief Executive Officer owns the promise every Achala IT Solutions engagement is built on: fees that can be linked to named metrics, delivery pods that arrive audit-ready, and a platform portfolio that compounds across clients rather than a services catalogue that resets to zero each quarter.",
      "Under this mandate, the group runs eight proprietary platforms in production with clients across 40+ countries, four delivery centers in the United States, the United Kingdom, India and Saudi Arabia, and an engagement model in which every program begins with falsifiable success criteria and ends with benchmarked evidence — including the documented decision to stop when the evidence says stop.",
      "The office also chairs the Responsible AI review board and the zero-exposure security council, keeping the two commitments that differentiate the firm — measurable outcomes and zero client-data exposure — above every commercial pressure."]),
    ("Chief Technology Officer", "chief-technology-officer", "Elena V. Whitfield",
     "Owns the eight-platform architecture, engineering standards and the responsible-AI framework.",
     ["Platform architecture", "Engineering standards", "AI governance"],
     ["The Chief Technology Officer is accountable for the engineering substance behind the Achala IT Solutions portfolio: Achala Nexus for decision intelligence, Forge for data and lakehouse engineering, Swarm for agentic fleets, Sentinel for zero-trust security, Twinverse for digital twins, Quanta for quantum readiness, Ledger for digital trust and Compass for field intelligence.",
      "This office publishes the engineering standards every delivery pod inherits — reference architectures, evaluation harnesses, replayable decision records and deployment gates — so that a program delivered in Riyadh is indistinguishable in quality from one delivered in London or Tysons Corner.",
      "The CTO also owns the Responsible AI Framework in engineering terms: model cards, evaluation evidence, drift monitoring and human-authority controls that make every autonomous system auditable by default."]),
    ("Chief AI & Data Officer", "chief-ai-data-officer", "Sanjay K. Iyer",
     "Leads applied AI research, retrieval architectures and the data-contracts practice.",
     ["Applied AI", "Retrieval architecture", "Data contracts"],
     ["The Chief AI & Data Officer runs the practices that decide whether enterprise AI produces auditable value or expensive theatre: applied AI delivery, retrieval architecture, evaluation engineering and the data-contracts discipline that underpins Achala Forge.",
      "The office maintains the firm's position that the durable advantage in enterprise AI sits in the retrieval layer — permissions, freshness and provenance — rather than in any single foundation model, and turns that position into delivery artifacts: source-cited answer platforms, evaluation harnesses that catch regression before clients do, and contracts that make data quality an interface, not a hope.",
      "Every generative system Achala IT Solutions ships is answerable to a benchmark pack agreed before build — the office owns that pack and publishes the negative results alongside the wins."]),
    ("Chief Security Officer", "chief-security-officer", "Marcus T. Bell",
     "Owns the zero-exposure architecture, security operations and compliance posture.",
     ["Zero-trust architecture", "Security operations", "Compliance"],
     ["The Chief Security Officer owns the control set behind the firm's founding commitment: zero critical data-exposure incidents since inception. Client data is never training material; enclaves, tenant isolation and customer-managed keys are the default architecture, not an add-on.",
      "This office runs security operations for managed platforms at 99.99% availability, leads the SOC 2 Type II and ISO 27001 programs, and maintains the HIPAA-ready and PCI-supporting delivery pods that let regulated clients move fast without moving loose.",
      "As agentic systems enter client estates, the office defines the policy envelopes that grant autonomy by evidence and revoke it the same way — every agent operates inside an auditable boundary with a named control owner."]),
    ("Chief Delivery Officer", "chief-delivery-officer", "Priya N. Sharma",
     "Runs the four global delivery centers and the first-90-days engagement machinery.",
     ["Delivery centers", "Engagement machinery", "Quality gates"],
     ["The Chief Delivery Officer converts the sales promise into shipped outcomes across four delivery centers — Tysons Corner, London, Hyderabad and Riyadh — and the pods of 2,400+ engineers, data scientists and domain specialists who work inside them.",
      "The office owns the first-90-days machinery that every engagement runs: the value-mapping sprint that locks baselines, the evidence pack that names owners and metrics, and the delivery gates that make progress inspectable rather than reported.",
      "Delivery quality is measured, not asserted: phase-gate evidence, client engagement ratings averaging 4.9 out of 5, and a bench that rotates platform lessons across industries so each program starts where the last one proved."]),
    ("Chief Commercial Officer", "chief-commercial-officer", "Daniel H. Mercer",
     "Owns client portfolio, partnerships in validation and outcome-linked commercials.",
     ["Client portfolio", "Alliances", "Commercial models"],
     ["The Chief Commercial Officer owns the client portfolio across 40+ countries and the commercial models that make Achala IT Solutions accountable: outcome-linked fees tied to named metrics, platform subscriptions with service levels, and transformation programs with evidence-gated phases.",
      "This office manages the technology alliance program — cloud, data, silicon and platform partners currently in validation — under a simple rule: no alliance is announced until its obligations, certifications and client references survive legal review.",
      "The office also publishes the commercial playbooks clients see first: value assessments, briefing formats and the reference-engagement packs that let a prospect verify claims before signing."]),
    ("Chief People Officer", "chief-people-officer", "Fatima A. Al-Rashid",
     "Builds the talent system: hiring bars, guilds, and the AI-era skills ladder.",
     ["Talent system", "Guilds", "Skills ladder"],
     ["The Chief People Officer builds the talent engine behind a selective firm: hiring bars that favor evidence over eloquence, guilds that move platform knowledge across geographies, and a skills ladder that treats AI-era capability as learnable rather than magical.",
      "The office runs development programs in partnership with delivery leadership — rotation across platforms and industries, certification tracks for cloud, data and security, and the human-centered adoption practice that treats change management as engineered work.",
      "Culture is treated as an operating system: outcomes over output, evidence first, zero-exposure security and engineered autonomy are the four behaviors the office hires, promotes and measures against."]),
    ("Chief Financial Officer", "chief-financial-officer", "Jonathan P. Reeves",
     "Owns group finance, the outcome-linked revenue model and investor reporting.",
     ["Group finance", "Revenue model", "Investor reporting"],
     ["The Chief Financial Officer owns group finance for a firm whose commercial model is unusual by design: fees that can be linked to the metrics its engagements commit to moving. Making that model durable requires baselines that survive audit, measurement methods agreed before work begins and revenue recognized against evidence rather than optimism.",
      "The office manages the financial machinery across four delivery centers and the eight-platform portfolio — platform subscriptions with service levels, managed-services run rates and transformation programs — with the discipline of a company that reports to clients almost as often as it reports to investors.",
      "Transparency is the operating rule: unit economics per platform, per geography and per engagement model, reviewed quarterly and reflected in the pricing clients actually see."]),
]

PARTNERS = [
    # slug, name, focus, what-we-build paragraphs (2), scenarios list, note
    ("aws", "AWS", "Cloud, data and agentic workloads on Amazon Web Services",
     "Achala IT Solutions engineering pods deliver applied AI, lakehouse and agentic-automation workloads on AWS infrastructure for regulated enterprises — from Bedrock-based generative platforms behind permission-aware retrieval, to SageMaker model estates under full evaluation governance, to Lake Formation estates engineered to survive audit.",
     "The delivery pattern is platform-first: reference architectures for zero-trust landing zones, customer-managed-key enclaves for sensitive estates, and cost-governed pipelines whose unit economics are measured rather than assumed. Programs run with the same evidence gates as every Achala IT Solutions engagement, with AWS services chosen for managed reliability over novelty.",
     ["Generative AI platforms with source-cited answers on Bedrock", "Real-time fraud and decisioning streams on Kinesis and Lambda", "Lakehouse estates on S3, Glue and Lake Formation with data contracts", "Agentic workflow fleets orchestrated on ECS and Step Functions"]),
    ("microsoft-azure", "Microsoft Azure", "Enterprise AI, data and hybrid estates on Microsoft Azure",
     "Achala IT Solutions delivers decision-intelligence and lakehouse programs on Azure for clients whose estates center on Microsoft technology — Azure OpenAI platforms with provenance-first retrieval, Fabric and Synapse estates under data contracts, and hybrid architectures that extend Zero-Trust controls to the edge.",
     "Where Azure Arc and hybrid operations matter, pods engineer the control plane once and let estates inherit it: policy-as-code, private networking, customer-managed keys and the evidence trails regulated clients need. Entra-based identity is treated as the security backbone for both human and agentic actors.",
     ["Azure OpenAI retrieval platforms with citation-grade answers", "Fabric and Synapse lakehouse estates with contract-governed quality", "Hybrid zero-trust estates under Arc with policy-as-code", "Databricks-on-Azure governed platforms for regulated analytics"]),
    ("google-cloud", "Google Cloud", "Analytics, AI and multi-cloud data platforms on Google Cloud",
     "Achala IT Solutions builds analytics and AI platforms on Google Cloud where BigQuery's serverless economics and Vertex AI's model operations fit the client estate — BigQuery lakehouses under contract governance, Vertex pipelines with evaluation gates, and Looker semantic layers that turn governed data into decision surfaces.",
     "Pods also deliver multi-cloud patterns for clients whose estates straddle providers: interoperable data contracts, portability-conscious architectures and cost telemetry that keeps serverless enthusiasm from becoming invoice surprise.",
     ["BigQuery lakehouse estates with contract-governed pipelines", "Vertex AI model estates with evaluation and drift gates", "Looker semantic layers as governed decision surfaces", "Multi-cloud data portability and cost-governance patterns"]),
    ("nvidia", "NVIDIA", "Accelerated computing for AI factories and inference at scale",
     "Achala IT Solutions engineers accelerated-compute programs on NVIDIA infrastructure for clients whose AI ambition outruns their GPU governance: inference factories sized and scheduled for unit economics, RAG and multimodal platforms accelerated end-to-end, and digital-twin workloads that lean on Omniverse-class simulation.",
     "The practice treats GPUs as a production capacity to be planned, not rented ad hoc: token-level cost telemetry, batch-vs-realtime scheduling, model right-sizing and fallback paths that keep service levels intact when demand spikes.",
     ["AI inference factories with token-level cost governance", "End-to-end accelerated RAG and multimodal platforms", "GPU capacity planning, scheduling and right-sizing programs", "Omniverse-class simulation pipelines for digital twins"]),
    ("snowflake", "Snowflake", "Governed data sharing and Snowflake-native applications",
     "Achala IT Solutions delivers Snowflake estates for enterprises that need sharing without losing governance: data products published as governed shares, Snowpark pipelines under contract tests, and native applications that put decision surfaces where the data already lives.",
     "The practice pairs Snowflake's marketplace economics with the data-contract discipline: schemas that announce change before making it, freshness SLAs that are monitored rather than promised, and cost guardrails that keep warehouse enthusiasm inside the budget envelope.",
     ["Governed data-sharing networks across business units and partners", "Snowpark pipelines under data-contract quality gates", "Snowflake-native decision applications", "Cost guardrails and warehouse governance programs"]),
    ("databricks", "Databricks", "Lakehouse engineering, MLops and real-time analytics on Databricks",
     "Achala IT Solutions is a lakehouse-first firm, and Databricks estates are where much of that doctrine ships: Unity Catalog as the governance spine, Delta Live Tables under contract tests, MLflow model estates with evaluation gates and Feature Store disciplines that keep training-serving skew a remembered bug rather than a live one.",
     "Programs range from regulated analytics estates in banking and healthcare to streaming decision platforms where Delta and Structured Streaming feed real-time fraud, pricing and operations decisions with evidence attached.",
     ["Unity Catalog governance spines for regulated estates", "Delta Live Tables pipelines under data contracts", "MLflow model estates with evaluation and drift gates", "Streaming decision platforms for fraud, pricing and operations"]),
    ("intel", "Intel", "Edge silicon, confidential computing and cost-efficient AI",
     "Achala IT Solutions delivers edge and confidential-computing programs on Intel technology where client economics demand efficiency over extravagance: inference at the edge on optimized silicon, confidential-computing enclaves that keep sensitive workloads attested, and cost-engineered AI deployments that match the model to the hardware deliberately.",
     "The practice matters most where data gravity, latency or privacy rules make central-cloud answers wrong: factory floors, hospital perimeters, bank branches and grid substations — the territory of Achala Twinverse and Compass platforms.",
     ["Edge inference programs on optimized Intel silicon", "Confidential-computing enclaves with attestation trails", "Cost-engineered model-to-hardware matching", "Edge fabric operations for industrial and regulated estates"]),
    ("red-hat", "Red Hat", "OpenShift platforms, platform engineering and hybrid operations",
     "Achala IT Solutions builds internal platform organizations on Red Hat technology: OpenShift estates engineered as products with paved roads, Ansible-driven configuration that survives audit, and hybrid operations that treat developer experience as a reliability discipline.",
     "Platform engineering is one of Achala IT Solutions's eight towers, and OpenShift is where several client estates already live; pods meet clients where they are, turning clusters into platforms with golden paths, self-service guardrails and measured unit costs.",
     ["OpenShift internal developer platforms with paved roads", "Ansible automation estates with audit-grade traceability", "Hybrid operations with measured reliability and unit cost", "Golden-path migrations from hand-built clusters"]),
    ("servicenow", "ServiceNow", "Workflow digitization and agentic operations on ServiceNow",
     "Achala IT Solutions delivers workflow and operations programs on ServiceNow for enterprises whose back offices run on it: ITOM and ITSM modernization with evidence-based SLAs, workflow digitization under zero-trust controls, and agentic operations where Achala Swarm fleets act through ServiceNow with human-authority gates.",
     "The practice treats ServiceNow as the system of action for enterprise operations: decision records, replayable approvals and the auditable envelopes that let automation act without giving up control.",
     ["ITOM and ITSM modernization with measured SLAs", "Workflow digitization under zero-trust architecture", "Swarm agentic fleets acting through governed ServiceNow", "Decision-record and replay architectures for operations"]),
    ("salesforce", "Salesforce", "Customer-platform intelligence and Data Cloud programs",
     "Achala IT Solutions delivers customer-platform programs on Salesforce where the CRM is the operational heart: Customer 360 architectures, Data Cloud implementations that unify profiles under consent governance, and decision services that bring Achala Nexus scoring into flows agents actually use.",
     "The practice respects what Salesforce already does well and engineers around what it cannot: provenance-grade identity, consent-scoped activation and measurement that ties every activation back to the metrics the business committed to.",
     ["Customer 360 identity spines with consent governance", "Data Cloud implementations with activation measurement", "Nexus decision services inside agent and marketing flows", "Service and sales workflow intelligence programs"]),
    ("sap", "SAP", "Enterprise-core modernization and RISE-era data programs",
     "Achala IT Solutions delivers programs around the SAP core for enterprises modernizing on RISE-era architectures: S/4HANA migration decisioning, BTP-side extensions under clean-core discipline, and data extraction pipelines that turn SAP gold copies into lakehouse assets without breaking provenance.",
     "The practice treats the ERP as the system of record it is — never rebuilt in shadow, always integrated by contract: finance-grade data quality, audit-ready lineage and change windows that respect what the business cannot break.",
     ["S/4HANA migration decisioning and readiness programs", "BTP extensions under clean-core discipline", "SAP-to-lakehouse pipelines with finance-grade lineage", "Master-data governance for enterprise-core modernization"]),
    ("ibm", "IBM", "Hybrid infrastructure, watsonx AI and mainframe-era modernization",
     "Achala IT Solutions delivers hybrid-infrastructure and AI programs with IBM technology for estates where z/OS, Power and Red Hat coexist: watsonx model platforms under evaluation governance, API-layer modernization that turns mainframe transactions into governed services, and quantum-readiness programs that pair with Achala Quanta practice.",
     "The practice is deliberately pragmatic about modernization: strangler patterns that move risk incrementally, evidence gates at every cutover, and the regulatory traceability that mainframe-era industries — banking, insurance, public sector — cannot operate without.",
     ["watsonx AI platforms under evaluation governance", "Mainframe transaction modernization via governed API layers", "Hybrid infrastructure programs across z/OS, Power and Linux", "Quantum-readiness programs paired with the Quanta practice"]),
]

CAREERS_SUBS = [
    ("working-here", "Working Here",
     "What it is like to build a career inside an outcome-linked engineering firm — guilds, evidence-first reviews and work that ships.",
     ["Achala IT Solutions runs on evidence, and careers here are built the same way. Work is organized in pods of engineers, data scientists and domain specialists who own outcomes together; reviews are anchored to artifacts — the model that shipped, the control that held, the metric that moved — rather than to hours or theatre.",
      "Four guilds run across the firm — platform engineering, applied AI, security and delivery — and membership rotates deliberately: a data engineer who has seen banking fraud streams brings different instincts to a healthcare lakehouse than one who has not. Rotation is engineered, not accidental.",
      "The firm operates from four delivery centers — Tysons Corner, London, Hyderabad and Riyadh — with pods arranged so client time zones share working hours with at least one center. Remote and hybrid arrangements are designed per program, not per preference, and written down like everything else."]),
    ("open-positions", "Open Positions",
     "Roles across the eight towers, four delivery centers and the platform groups — with the hiring bar stated in evidence terms.",
     ["Hiring at Achala IT Solutions asks for evidence, not adjectives. Engineering roles are evaluated against shipped work; data-science roles against benchmarks the candidate can defend; delivery roles against programs whose outcomes are still measurable today.",
      "Open roles span the eight towers — applied AI and generative systems, agentic automation, data and lakehouse, cybersecurity and zero-trust, cloud and platform engineering, quantum readiness, digital trust and IoT with robotics — plus the platform groups behind Achala Nexus, Forge, Swarm, Sentinel, Twinverse, Quanta, Ledger and Compass.",
      "Current openings are listed per delivery center and per tower. If none matches, send an evidence pack anyway; the firm hires selectively ahead of demand for the practices that keep filling."]),
    ("benefits-development", "Benefits & Development",
     "Compensation, certification tracks, rotation programs and the skills ladder that treats AI-era capability as learnable.",
     ["Compensation is benchmarked against outcome: base pay per delivery center, program bonuses tied to the same evidence gates clients see, and certification tracks funded by the firm across cloud, data, security and AI disciplines.",
      "Development follows the skills ladder: from pod engineer to platform specialist to practice lead, with each rung defined by artifacts owned rather than years served. Rotation across platforms and industries is part of the ladder, not a favor.",
      "Benefits are engineered per geography — health coverage, retirement, leave and family support at or above local market for each of the four delivery centers — and published internally so the comparison is honest."]),
]

NEWSROOM = [
    ("achalasolutions-launches-new-digital-platform", "Achala IT Solutions launches its new digital platform",
     "2026-11-20",
     "The new achalasolutions.com goes live with 600+ pages of industry- and service-aligned engineering content, reflecting the firm's eight technology towers and outcome-linked engagement model.",
     ["Achala IT Solutions Corporation today launched its new corporate website at www.achalasolutions.com — a 600-plus-page platform that maps the firm's eight deep technology towers to twelve industries and 48 sub-industries, with capability pages that show exactly how each tower applies where a client lives.",
      "The launch consolidates the firm's digital presence around the outcome-linked engagement model: every service page names the metrics an engagement targets, the first-90-days plan and the evidence gates that make progress inspectable. Case studies are published in anonymized, verifiable style with measurement methods available under NDA.",
      "The platform ships with the zero-exposure posture the firm applies to client work: no third-party tracking beyond consented analytics, a GDPR-aligned consent banner as the default, and full accessibility conformance targets at WCAG 2.2 AA."]),
    ("achala-nexus-general-availability", "Achala Nexus reaches general availability for decision intelligence",
     "2026-10-28",
     "The decision-intelligence hub behind real-time credit, claims, pricing and fraud decisions is now generally available with replay, champion-challenger and full evidence trails.",
     ["Achala IT Solutions today announced general availability of Achala Nexus, the decision-intelligence hub that unifies predictive models, business rules and agentic reasoning behind one governed decision API. Nexus serves high-volume enterprise choices — credit, claims, pricing, triage, fraud and routing — with champion-challenger testing and replayable decision records as native features.",
      "Every decision Nexus makes can be replayed with the exact feature values, model versions and policy states that produced it — the property that turns model governance from a quarterly scramble into a query. Early deployments in banking and insurance reported decision-latency reductions measured in orders of magnitude alongside audit packs regulators accepted without rework.",
      "General availability covers managed deployment in all four delivery regions with 99.99% availability service levels, customer-managed key enclaves and the zero-exposure data posture applied across the platform portfolio."]),
    ("iso-27001-and-soc-2-renewals", "ISO 27001 and SOC 2 Type II programs renewed across delivery centers",
     "2026-10-14",
     "Annual audits reconfirm the control set behind the firm's zero-exposure record across all four delivery centers.",
     ["Achala IT Solutions's ISO 27001 certification and SOC 2 Type II attestation programs were renewed following annual audit cycles across the Tysons Corner, London, Hyderabad and Riyadh delivery centers. The audits reconfirm the control environment behind the firm's zero critical data-exposure record since inception.",
      "The control set now includes the AI-specific extensions introduced this year: evaluation evidence retention, model-change traceability and the policy envelopes that govern agentic systems operating inside client estates.",
      "Clients can request the current attestation summaries and control-scope documents through their engagement leads; shared-assessment packs (CAIQ-style) are available under NDA."]),
    ("riyadh-delivery-center-expansion", "Riyadh delivery center expands to serve Vision 2030 programs",
     "2026-09-30",
     "The KAFD-based center doubles its sovereign-delivery capacity for smart-city, energy and public-sector programs in the Kingdom.",
     ["Achala IT Solutions expanded its Riyadh delivery center at King Abdullah Financial District, doubling capacity for sovereign-delivery programs across smart cities, energy and public sector. The center anchors the firm's Vision 2030 portfolio, including twin-city operations and grid-intelligence programs.",
      "The expansion adds sovereign data-operations capacity — programs in which data residency, workforce composition and regulatory alignment are engineered requirements rather than afterthoughts — and a quantum-readiness lab operated with the firm's Quanta practice.",
      "Hiring in the Kingdom prioritizes national talent for the practices the center serves: digital-twin engineering, field-intelligence platforms and the security operations that sovereign programs require."]),
    ("responsible-ai-framework-v2", "Responsible AI Framework version 2.0 published",
     "2026-09-16",
     "The framework now covers agentic systems end-to-end: policy envelopes, authority gates, evaluation evidence and drift response.",
     ["Achala IT Solutions published version 2.0 of its Responsible AI Framework, extending coverage from model governance to agentic systems: policy envelopes that grant autonomy by evidence, authority gates that keep humans in the loop where judgment is not pattern-shaped, and drift-response runbooks that treat model decay as an operational event rather than a surprise.",
      "The framework aligns with the EU AI Act's conformity tooling and the NIST AI Risk Management Framework, and is applied as delivery artifacts — model cards, evaluation packs, replayable decision records — rather than as policy documents alone.",
      "Version 2.0 is available to clients and prospects through engagement leads; a public summary is published in the firm's insights library."]),
    ("quantum-readiness-lab", "Quanta practice opens quantum-readiness lab for PQC migration",
     "2026-08-27",
     "The lab benchmarks post-quantum migration paths for regulated estates: crypto-agility audits, HSM inventories and harvest-now-decrypt-later exposure mapping.",
     ["Achala IT Solutions opened a quantum-readiness lab within its Quanta and Advanced Compute practice, focused on the engineering floor of quantum strategy: post-quantum cryptography migration for regulated estates. The lab runs crypto-agility audits, hardware-security-module inventories and harvest-now-decrypt-later exposure mapping for clients in banking, public sector and critical infrastructure.",
      "The lab's benchmark packs cover optimization pilots on quantum and quantum-inspired hardware with the same evidence discipline applied elsewhere in the firm: falsifiable criteria agreed before the pilot, results published whether positive or negative.",
      "Initial lab capacity serves programs in the United Kingdom and Saudi Arabia, with United States capacity planned alongside the next Quanta platform release."]),
    ("hyperautomation-swarm-release", "Achala Swarm release adds governed agent fleets at enterprise scale",
     "2026-08-12",
     "The agentic-automation platform's latest release introduces fleet budgets, authority gates and cross-agent replay as standard controls.",
     ["Achala Swarm, the firm's agentic-automation platform, shipped its largest release to date: agent fleets with spend and action budgets, authority gates that escalate on evidence thresholds, and cross-agent replay that reconstructs any multi-step workflow end-to-end.",
      "The release reflects a year of production operation inside client estates in financial services, telecommunications and manufacturing, where digital workers now run document-heavy operations under the same policy envelopes as human operators.",
      "Swarm's zero-exposure posture carries across the release: agents operate inside tenant boundaries with customer-managed keys, and no client data ever leaves the estate for training purposes."]),
    ("client-rating-4-9-milestone", "Client engagement rating holds at 4.9 across 350+ engagements",
     "2026-07-30",
     "The firm's half-year engagement review reports a 4.9/5 average rating and outcome-linked fees now standard across transformation programs.",
     ["Achala IT Solutions's half-year engagement review reported an average client rating of 4.9 out of 5 across its portfolio of more than 350 delivered engagements in over 40 countries. Outcome-linked commercial models — fees partially tied to named metrics — are now standard across the firm's transformation programs.",
      "The review attributes retention to the operating machinery clients can inspect: baseline metrics locked in diagnosis, phase-gate evidence packs, and the practice of publishing negative results internally so delivery pods learn from them.",
      "The firm's engagement-rating methodology is available to clients and prospects on request, along with reference engagements matched by industry and tower."]),
]

def new_pages():
    """Return list of page dicts in the same shape as volume pages."""
    pages = []
    # --- leadership profiles ---
    for role, slug, name, mandate, focus, paras in LEADER:
        blocks = [
            {"t": "hero", "x": f"{role} — the mandate behind Achala IT Solutions's {mandate.split('.')[0].lower()}."},
            {"t": "p", "x": mandate},
        ]
        for para in paras:
            blocks.append({"t": "p", "x": para})
        blocks.append({"t": "h2", "x": "Portfolio of focus"})
        blocks.append({"t": "bullets", "items": [[f, "Owned as a standing mandate of this office, reported through the firm's governance cadence."] for f in focus]})
        blocks.append({"t": "cta", "x": "Book a briefing with this office through the executive briefing desk — 45 minutes with a practice lead, your metric and three reference engagements."})
        pages.append({
            "id": f"leader-{slug}", "title": role, "url": f"/leadership/{slug}/",
            "template": "leadership_profile", "breadcrumb": f"Home > About Us > Leadership > {role}",
            "seo_title": f"{role} | Achala IT Solutions Leadership"[:60],
            "meta_description": (role + " at Achala IT Solutions — " + mandate)[:155].rstrip(),
            "words": sum(len(p.split()) for p in paras) + 60,
            "section": "Company", "l1": "About Us", "l2": "Leadership", "l3": role, "l4": "",
            "profile": {"role": role, "name": name, "focus": focus, "placeholder": True},
        })
    # --- partner pages ---
    for slug, name, focus, p1, p2, scenarios in PARTNERS:
        blocks = [
            {"t": "hero", "x": f"What Achala IT Solutions engineers on {name} — delivery ecosystems for {focus.lower()}."},
            {"t": "p", "x": p1},
            {"t": "p", "x": p2},
            {"t": "h2", "x": f"Delivery scenarios on {name}"},
            {"t": "bullets", "items": [[s.split(" on ")[0].split(" with ")[0].split(" for ")[0], s] for s in scenarios]},
            {"t": "note", "x": "Alliance status: in validation. Partnership tiers, certifications and client references for this alliance are published only after legal and reference verification completes."},
            {"t": "cta", "x": "Planning a program on this platform? Book a briefing with the matching practice lead and bring your constraint — regulatory, security or capital."},
        ]
        pages.append({
            "id": f"partner-{slug}", "title": f"{name} Alliance", "url": f"/partner-ecosystem/{slug}/",
            "template": "partner_page", "breadcrumb": f"Home > About Us > Partner Ecosystem > {name}",
            "seo_title": f"Achala IT Solutions on {name} — Delivery Ecosystem"[:60],
            "meta_description": f"What Achala IT Solutions engineers on {name}: {focus}. Delivery scenarios, evidence gates and the alliance validation status."[:155].rstrip(),
            "words": len((p1 + p2).split()) + 80,
            "section": "Company", "l1": "About Us", "l2": "Partner Ecosystem", "l3": name, "l4": "",
            "partner": {"name": name, "focus": focus, "scenarios": scenarios},
        })
    # --- careers subpages ---
    for slug, title, blurb, paras in CAREERS_SUBS:
        blocks = [{"t": "hero", "x": blurb}]
        for para in paras:
            blocks.append({"t": "p", "x": para})
        blocks.append({"t": "cta", "x": "Send an evidence pack to careers@achalasolutions.com — shipped work, benchmarks you can defend, programs still measurable today."})
        pages.append({
            "id": f"careers-{slug}", "title": title, "url": f"/careers/{slug}/",
            "template": "careers_page", "breadcrumb": f"Home > About Us > Careers > {title}",
            "seo_title": f"{title} | Achala IT Solutions Careers"[:60],
            "meta_description": (title + " at Achala IT Solutions — " + blurb)[:155].rstrip(),
            "words": sum(len(p.split()) for p in paras) + 40,
            "section": "Company", "l1": "About Us", "l2": "Careers", "l3": title, "l4": "",
        })
    # --- newsroom releases ---
    for slug, title, date, blurb, paras in NEWSROOM:
        blocks = [
            {"t": "hero", "x": blurb},
            {"t": "p", "x": f"{date} — " + paras[0]},
        ]
        for para in paras[1:]:
            blocks.append({"t": "p", "x": para})
        blocks.append({"t": "cta", "x": "Press contact: press@achalasolutions.com. Analysts and journalists can request briefing packs through the newsroom desk."})
        pages.append({
            "id": f"news-{slug}", "title": title, "url": f"/newsroom/{slug}/",
            "template": "newsroom_article", "breadcrumb": f"Home > About Us > Newsroom > {title}",
            "seo_title": f"{title} | Achala IT Solutions Newsroom"[:60],
            "meta_description": blurb[:155].rstrip(),
            "words": sum(len(p.split()) for p in paras) + 30,
            "section": "Company", "l1": "About Us", "l2": "Newsroom", "l3": title, "l4": "",
            "published": date,
        })
    return pages


if __name__ == "__main__":
    ps = new_pages()
    print("authored pages:", len(ps))
    from collections import Counter
    print(Counter(p['template'] for p in ps))
