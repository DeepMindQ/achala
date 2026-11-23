"""Home page full hand-rewrite — plain professional voice, extensive, interlinked."""
import json

P = '/home/z/my-project/site/src/content/pages/home.json'
d = json.load(open(P))

d['title'] = 'Home'
d['seo_title'] = 'Achala IT Solutions | Deep-Tech IT Services & Consulting'
d['meta_description'] = ('Achala IT Solutions builds the AI and data systems enterprises run on: applied AI, '
                         'agentic automation, data platforms, cybersecurity and advanced compute — '
                         'delivered by 2,400+ engineers across 4 global centers.')

d['blocks'] = [
    {"t": "hero", "x": "Achala IT Solutions builds the AI and data systems enterprises run on. Applied AI, agentic automation, data platforms, cybersecurity and advanced compute — delivered by named teams, measured against a signed baseline, and handed over with the evidence your auditors ask for."},

    {"t": "h2", "x": "What we do"},
    {"t": "p", "x": "Achala IT Solutions is a global IT services and consulting firm with 2,400+ engineers, data scientists and domain specialists across four delivery centers. We take on programs where the outcome can be measured before and after: a fraud model's approval rate, a plant's unplanned downtime, a contact center's cost per case, a grid's balancing cost."},
    {"t": "p", "x": "Every engagement starts with a baseline your finance team signs. Every quarter ends with a measured delta against that baseline. When a program should stop, we say so in writing. That discipline — not a model architecture — is what most enterprise AI programs are missing, and it is the first thing we install."},

    {"t": "h2", "x": "Eight service towers, one delivery system"},
    {"t": "p", "x": "Our services are organized into eight towers. Each tower carries named services with defined deliverables, and the towers compose on shared platforms: a fraud program draws on data engineering, agentic automation and cybersecurity at the same time, under one delivery plan."},
    {"t": "bullets", "items": [
        ["Applied AI & Generative AI", "Strategy, model selection, retrieval, evaluation and production operations. AI measured on the P&L, from enterprise strategy to deployed systems."],
        ["Agentic AI & Hyperautomation", "Digital workers that run inside your systems with defined roles, budgets and human checkpoints. Every action is logged and reversible."],
        ["Data, Analytics & Lakehouse", "Pipelines, lakehouse and governance: reports that reconcile, lineage you can trace, access control that does not slow teams down."],
        ["Cybersecurity & Zero-Trust", "Identity-first architecture for people, machines and models, with detection, response and AI-specific controls in one program."],
        ["Cloud, Edge & Platform Engineering", "Hybrid and edge estates engineered for reliability and cost per workload, with internal platforms your teams actually adopt."],
        ["Quantum & Advanced Compute", "Optimization, simulation and post-quantum cryptography migration — applied where the mathematics pays back, benchmarked against classical methods."],
        ["Blockchain & Digital Trust", "Permissioned networks, tokenization and verifiable credentials with the reporting supervisors expect."],
        ["IoT, Digital Twin & Robotics", "Sensor integration, digital twins and robotics: see, simulate and act on physical assets in one loop."]
    ]},

    {"t": "h2", "x": "Platforms, not just projects"},
    {"t": "p", "x": "Each tower runs on one of our eight proprietary platforms. The platforms arrive pre-configured with the controls, evidence generation and delivery patterns our teams have standardized — clients start from a configured 80 percent baseline and spend their budget on the 20 percent that is genuinely theirs."},
    {"t": "bullets", "items": [
        ["Achala Nexus", "The decision hub: contextual graphs, policy checks and full decision replay for audit."],
        ["Achala Forge", "The data platform every program builds on: ingestion, quality, lineage and access control."],
        ["Achala Swarm", "Multi-agent orchestration with queues, budgets, escalation paths and audit trails."],
        ["Achala Sentinel", "Security controls for people, machines and models, with evidence collected continuously."],
        ["Achala Twinverse", "Simulation and operations for physical assets, from sensor data to actuation."],
        ["Achala Quanta", "Optimization workloads on quantum-inspired algorithms, benchmarked against classical solvers."],
        ["Achala Ledger", "Permissioned ledger networks with regulatory reporting built in."],
        ["Achala Compass", "Model governance: validation, monitoring and documentation your risk committee can review."]
    ]},

    {"t": "h2", "x": "Where we work"},
    {"t": "p", "x": "Twelve industries, each with sub-industry depth: the sector's regulatory posture, priority programs and capability alignment are mapped on every industry page. Examples of how that reads in practice:"},
    {"t": "bullets", "items": [
        ["Banking & Financial Services", "Real-time fraud and risk decisions, resilient core operations and AI controls that pass supervisory review."],
        ["Healthcare & Life Sciences", "Clinical data interoperability, ambient documentation and AI programs under clinical governance."],
        ["Manufacturing & Industrial", "Sensor-driven quality, digital twins and shop-floor automation tied to OEE and yield."],
        ["Energy & Utilities", "Grid analytics, trading optimization and operational safety for the energy transition."],
        ["Retail & Consumer Goods", "Pricing, availability and personalization programs measured directly on margin."]
    ]},
    {"t": "p", "x": "The full sector list — insurance, telecom, logistics, public sector, education, technology and agriculture — is on the industries hub, and every sub-industry page aligns the five towers that matter most there."},

    {"t": "h2", "x": "The research behind the delivery"},
    {"t": "p", "x": "Our platforms embed eight proprietary method families developed by our research programme: graph-native contextual intelligence, quantum-inspired optimization, federated learning with homomorphic encryption, multi-layer decision validation, energy-aware workload orchestration, generative workflow automation, self-evolving enterprise learning loops and multimodal pattern recognition. Each method is in production use inside named platforms — the mapping from method to platform to service is on the patented-intelligence page."},

    {"t": "h2", "x": "Achala IT Solutions in numbers"},
    {"t": "table", "caption": "Achala IT Solutions at a glance", "headers": ["Proof point", "What it means"], "rows": [
        ["350+", "enterprise engagements delivered"],
        ["40+", "countries served from 4 global delivery centers"],
        ["2,400+", "engineers, data scientists and domain specialists"],
        ["8", "proprietary platforms in production with clients"],
        ["8", "proprietary method families developed by our research programme"],
        ["630+", "published delivery playbooks across industries and capabilities"]
    ]},

    {"t": "h2", "x": "How we engage"},
    {"t": "p", "x": "Delivery runs on a five-phase method with named gates: Diagnose, Design, Prove, Industrialize, Compound. No phase proceeds without its evidence — the baseline audit, the risk budget, the pilot's measured delta, the production runbook, the quarterly re-audit. Commercial models can link fees to the metrics we commit to moving."},
    {"t": "bullets", "items": [
        ["Week 1", "A 45-minute executive briefing: your metric, our pattern library, three reference engagements."],
        ["Weeks 2–6", "A value assessment: baseline audit, six-week capital-committee-grade roadmap, fixed price."],
        ["Quarter 1", "The first production pilot: bounded scope, named control owner, measured delta at the gate."]
    ]},

    {"t": "cta", "x": "Bring the metric you need to move. We will show you the pattern, the platform and the baseline we would sign."}
]

d['words'] = 780
json.dump(d, open(P, 'w'), indent=1, ensure_ascii=False)
print('home.json rewritten,', len(d['blocks']), 'blocks')
