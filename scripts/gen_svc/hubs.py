#!/usr/bin/env python3
"""Tower hubs (8) + services hub (1): portfolio consoles, unique per hub."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *

def gen():
    tw = {}

    # ── Tower hub: Agentic AI & Hyperautomation ──
    tw["services_agentic-ai-hyperautomation.json"] = [
        hero("Hyperautomation succeeds as workforce design, not as tool rollout. Agentic AI & Hyperautomation runs seven practices that mine the work, prove the ROI, build governed agent fleets and orchestrate the workflows between them — every practice with its own console, its own failure taxonomy and its own evidence gates."),
        h2("Seven practices from mining to fleet management"),
        p("The practice set covers the full arc: process and task mining finds where the work actually is; intelligent document processing handles the unstructured intake; agentic process automation builds the tool-using loops; autonomous workflow orchestration makes them durable; decision intelligence governs the judgment layer; the digital workforce manages the fleet; and systems integration wires it all into the estate. Each practice page carries its own interactive console — the portfolio view below shows how the seven compose."),
        table("The seven practices — what each one owns and its signature deliverable",
              ["Practice", "Owns", "Signature deliverable"],
              [
                ["Process & Task Mining", "The evidence base — what actually happens", "Variant map + costed automation shortlist"],
                ["Intelligent Document Processing", "Unstructured intake with calibrated confidence", "Straight-through pipeline with designed review tail"],
                ["Agentic Process Automation", "Tool-using agent loops with containment", "Governed fleet with run ledger + eval harness"],
                ["Autonomous Workflow Orchestration", "Durable long-running processes", "Saga graphs with rehearsed compensation"],
                ["Decision Intelligence Systems", "The judgment layer — signal to action", "Four-layer decision path with audit trail"],
                ["Digital Workforce & Multi-Agent Orchestration", "Fleet governance at scale", "Agent registry with identity and budgets"],
                ["Hyperautomation & Systems Integration", "The fabric between them", "Actuation registry + fragility-ranked estate"],
              ]),
        h2("Why automation programs stall — and what the discipline is instead"),
        p("Programs stall in the same three places: candidates chosen by opinion (mining fixes that), agents deployed without containment (the failure taxonomies on each practice page fix that), and fleets that grow without governance (the registry discipline fixes that). The seven practices are sequenced deliberately — mining before automation, contracts before orchestration, identity before scale — and each practice's console is the working evidence model its delivery holds itself to."),
        idash(
            "Hyperautomation portfolio — the seven practices on one console",
            badge="Interactive · portfolio model",
            kpis_=[
                kpi("Practices live", "7", delta="one program, one contract system", dir_="flat", spark=[2, 3, 4, 5, 6, 7, 7]),
                kpi("Portfolio containment", "78%", delta="blended across fleets", dir_="up", spark=[52, 58, 64, 68, 72, 75, 78]),
                kpi("Cost / action trend", "−64%", delta="year over year", dir_="down", spark=[0, -12, -24, -35, -47, -56, -64]),
                kpi("Automations governed", "216", delta="all with owners", dir_="up", spark=[40, 80, 120, 150, 180, 200, 216]),
                kpi("Mining→production", "23", delta="candidates shipped", dir_="up", spark=[4, 8, 12, 15, 18, 21, 23]),
            ],
            tabs=[
                tab("Practice adoption", [
                    w_line("Practice adoption curves — where programs actually progress",
                           ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8"],
                           [{"name": "Mining", "points": [62, 78, 88, 93, 96, 97, 98, 98]},
                            {"name": "IDP", "points": [40, 55, 66, 74, 80, 84, 87, 89]},
                            {"name": "Agent loops", "points": [20, 32, 44, 55, 63, 70, 75, 79]},
                            {"name": "Fleet governance", "points": [8, 15, 24, 34, 44, 53, 60, 66]}],
                           unit="% maturity", note_="Click to isolate. Mining matures first because evidence precedes automation; fleet governance is the slow-compounding practice — programs that skip it pay later."),
                    w_radar("Capability depth by practice — where the tower is strongest",
                            ["Mining", "IDP", "Agent loops", "Orchestration", "Decisions", "Fleet", "Integration"],
                            [{"name": "Delivery depth", "points": [92, 90, 86, 88, 84, 82, 90]},
                             {"name": "Sector breadth", "points": [88, 84, 80, 86, 78, 76, 88]}],
                            note_="Toggle series. Depth stays above 80 everywhere — the tower's internal bar for opening a practice to clients."),
                ]),
                tab("Estate fragility", [
                    w_heat("Automation estate by practice × sector — where depth runs deepest",
                           ["Mining", "IDP", "Agent loops", "Orchestration", "Fleet"],
                           ["Banking", "Insurance", "Healthcare", "Manufacturing", "Retail"],
                           [[92, 88, 70, 74, 82], [88, 94, 74, 70, 80], [78, 92, 66, 72, 70], [74, 62, 70, 88, 68], [80, 76, 72, 66, 86]],
                           unit="depth index",
                           note_="Hover cells for depth. IDP carries the healthcare and insurance flagship records; manufacturing depth sits in orchestration and fleet — pick your sector cell and the practice page below it."),
                ]),
            ],
            note_="Reference portfolio model: depth indices and adoption bands from delivery, not client telemetry.",
        ),
        h2("How automation engagements run"),
        p("Every engagement starts with the two-week diagnostic (mining-led): the candidate list ranked by costed pain, the containment plan, and the wave map. The first build proves the loop on one queue with the full evidence chain — ledger, eval harness, shadow mode — and the program then scales by wave with the console live from week six. Governance artifacts (tool contracts, policies, registries) are deliverables, not documents: they are wired into the pipelines that run the fleet."),
        bullets([
            ["Evidence-first sequencing", "Mining before automation, contracts before orchestration, identity before scale — the stall points are sequenced out"],
            ["Containment as deliverable", "Tool contract registry, policy layer, eval harness, run ledger — shipped with every fleet"],
            ["Console from week six", "The steering committee reads the same numbers delivery does — no status decks"],
            ["Governance that scales", "Agent registry, actuation registry, capability registries — the fleet grows without ungoverned accretion"],
        ]),
        cta("Bring the process your CFO calls expensive and your auditors call fragile — the two-week diagnostic ranks what should be automated, what should not, and what the first governed fleet looks like."),
    ]

    # ── Tower hub: Applied AI & Generative AI ──
    tw["services_applied-ai-generative-ai.json"] = [
        hero("Applied AI earns its place in the P&L or it does not belong in the estate. Applied AI & Generative AI runs seven practices that take ideas through falsifiable PoCs, build the platform rails once, tune and operate models with eval harnesses, and deploy multimodal and conversational systems that survive production — every practice with its own console and signed gate structure."),
        h2("Seven practices from hypothesis to operating model"),
        p("The practice set is the value pipeline: AI PoC & value validation kills weak ideas fast and funds strong ones with arithmetic; enterprise AI strategy builds the portfolio machine; GenAI platform engineering lays the shared rails; LLM fine-tuning & model operations runs the tuning treadmill; RAG & knowledge systems, conversational AI and multimodal vision systems are the product-facing practices. Each page carries its own console — the portfolio view shows how they compose into an AI estate that ships."),
        table("The seven practices — what each owns and its signature deliverable",
              ["Practice", "Owns", "Signature deliverable"],
              [
                ["AI PoC & Value Validation", "Fund-or-kill discipline", "Four-gate structure with frozen case set"],
                ["Enterprise AI Strategy & Roadmapping", "The operating model", "Scored portfolio + risk tiers + named owners"],
                ["GenAI Platform Engineering", "The shared rails", "Gateway, registry, harness, scoreboard"],
                ["LLM Fine-Tuning & Model Ops", "The tuning treadmill", "Three-eval-family promotion with provenance"],
                ["RAG & Enterprise Knowledge", "Cited answers over your corpus", "Groundedness harness + freshness SLAs"],
                ["Conversational AI & Digital Humans", "Voice and chat channels", "Latency budgets + containment with CSAT"],
                ["Multimodal AI & Vision-Language", "Perception tasks", "Per-task eval bars + edge deployment economics"],
              ]),
        h2("Why AI programs stall — and what the discipline is instead"),
        p("AI estates stall on the same three gaps: no gate discipline (PoCs that cannot die become productions that cannot work), no platform (forty teams re-solving inference and safety), no evaluation (models ship on demo quality and regress silently). The seven practices close each gap deliberately: gates before scaling, platform before portfolio wave three, harnesses before model choice. The portfolio console below carries the depth evidence per practice."),
        idash(
            "Applied AI portfolio — the seven practices on one console",
            badge="Interactive · portfolio model",
            kpis_=[
                kpi("Practices live", "7", delta="gates signed per practice", dir_="flat", spark=[2, 3, 5, 5, 6, 7, 7]),
                kpi("PoC kill rate", "68%", delta="honest — graveyard published", dir_="flat", spark=[50, 55, 60, 62, 65, 67, 68]),
                kpi("Eval coverage", "87%", delta="of production gen-AI flows", dir_="up", spark=[40, 52, 61, 70, 78, 84, 87]),
                kpi("Cost / 1k tokens", "0.0021", delta="blended after routing", dir_="down", spark=[0.008, 0.0065, 0.005, 0.0038, 0.0029, 0.0024, 0.0021]),
                kpi("Onboard → prod", "6.5 d", delta="platform onboarding", dir_="down", spark=[28, 22, 17, 13, 10, 8, 6.5]),
            ],
            tabs=[
                tab("Portfolio value", [
                    w_scatter("The AI estate by value and readiness — bubbles at risk tier",
                              [sc_pt(78, 66, "Claims triage", "Tier-1"), sc_pt(64, 48, "Quality vision", "Tier-2"),
                               sc_pt(88, 24, "Underwriting assist", "Tier-1"), sc_pt(52, 72, "Service summaries", "Tier-3"),
                               sc_pt(70, 30, "Contract intel", "Tier-2"), sc_pt(58, 76, "Invoice exception", "Tier-2"),
                               sc_pt(44, 55, "Forecasting", "Tier-2"), sc_pt(82, 12, "Dynamic pricing", "Tier-1")],
                              ["Tier-1", "Tier-2", "Tier-3"], "Value (0-100)", "Readiness (0-100)",
                              note_="Hover for names. The funded slate comes from the upper band with tiered controls attached — the map is the strategy practice's working artifact."),
                    w_bar("Gate outcomes by stage — where candidates die honestly",
                          ["Gate 1", "Gate 2", "Gate 3", "Gate 4", "Funded"],
                          [{"name": "Candidates reaching (n)", "points": [64, 38, 25, 15, 11]},
                           {"name": "Surviving (%)", "points": [59, 66, 60, 73, 73]}],
                          note_="Click to isolate. The funnel is the value-validation practice's honesty: two-thirds die, and the graveyard is published internally — that is what keeps hypotheses sharp."),
                ]),
                tab("Capability heat", [
                    w_heat("Practice depth by sector — where applied AI runs deepest",
                           ["PoC gates", "Platform", "Fine-tuning", "RAG", "Voice", "Vision"],
                           ["Banking", "Healthcare", "Retail", "Manufacturing", "Public sector"],
                           [[90, 84, 78, 88, 74, 72], [82, 78, 70, 92, 68, 80], [84, 86, 76, 78, 82, 84], [78, 80, 84, 66, 70, 92], [80, 76, 68, 82, 76, 70]],
                           unit="depth index",
                           note_="Hover cells for depth. RAG carries healthcare's flagship record; vision carries manufacturing's — pick your sector cell and the practice page below it."),
                ]),
            ],
            note_="Reference portfolio model: gate outcomes and depth indices from delivery, not client telemetry.",
        ),
        h2("How applied AI engagements run"),
        p("Strategy engagements run seventy days (scored estate, tier map, operating model with names); platform builds run ninety (gateway, registry, harness, scoreboard, two onboarded features); product practices run one quarter each with their consoles live from week six. The PoC discipline underwrites all of it: fixed budgets, frozen case sets, pre-written gates. The practices compose — strategy hands the platform its first two workloads, the platform hands the product practices their rails."),
        bullets([
            ["Gates before scale", "PoC kill discipline underwrites every portfolio wave — the graveyard is published"],
            ["Platform once, applied everywhere", "Gateway, registry, harness and scoreboard — no team re-solves inference"],
            ["Harnesses before model choice", "Evaluation is an engineering artifact — models ship on scores, not demos"],
            ["Consoles as steering", "Every practice carries its live console — the numbers are the status meeting"],
        ]),
        cta("Bring the AI ambition and the stalled portfolio. The scored estate and gate structure land in seventy days — fundable at the next board."),
    ]

    # ── Tower hub: Blockchain & Digital Trust ──
    tw["services_blockchain-digital-trust.json"] = [
        hero("Digital trust is engineering plus governance, in that order. Blockchain & Digital Trust runs six practices that tokenize assets with enforceable legal wrappers, build DLT networks that survive their own upgrades, run chain analytics that hold up in filings, issue verifiable credentials that actually get adopted, anchor provenance trails that survive audits, and engineer smart contracts that cannot be patched — so they are right before they ship."),
        h2("Six practices from tokenization to contract assurance"),
        p("The practice set covers the trust stack: asset tokenization and DLT networks build the rails; smart contract engineering and provenance traceability build the evidence; blockchain analytics and decentralized identity build the compliance and adoption layers. Each practice carries its own console — lifecycle duties, custody posture, trail integrity, network operations — and the portfolio view shows how they compose."),
        table("The six practices — what each owns and its signature deliverable",
              ["Practice", "Owns", "Signature deliverable"],
              [
                ["Asset Tokenization", "Legal-engineering product", "Lifecycle evidence chain + custody drills"],
                ["Blockchain Analytics & Compliance", "Defensible evidence", "Versioned derivations + mock examinations"],
                ["Decentralized Identity", "Credential ecosystems", "Trust registry + four-check verification"],
                ["Enterprise DLT Networks", "Consortium operations", "Staged upgrades + onboarding kit"],
                ["Provenance & Traceability", "Actor-bound trails", "Recall drill + attestation-strength grid"],
                ["Smart Contract Engineering", "Unpatchable correctness", "Invariant sheet + ceremony-gated deploys"],
              ]),
        h2("Why trust programs fail — and what the discipline is instead"),
        p("Trust programs fail on governance gaps, not cryptography: tokens without enforceable wrappers, networks that improvise upgrades, analytics that cannot show derivations, credentials nobody adopts because issuance is a form. The six practices close each gap with evidence-first engineering — the consoles on each page are the working models, and the portfolio view carries the depth record."),
        idash(
            "Digital trust portfolio — the six practices on one console",
            badge="Interactive · portfolio model",
            kpis_=[
                kpi("Practices live", "6", delta="evidence packs signed", dir_="flat", spark=[2, 3, 4, 5, 6, 6, 6]),
                kpi("Reconciliation deltas", "0", delta="across asset programs", dir_="flat", spark=[3, 2, 1, 0, 0, 0, 0]),
                kpi("Drill pass rate", "94%", delta="custody, recall, upgrade drills", dir_="up", spark=[62, 70, 78, 84, 89, 92, 94]),
                kpi("Credentials issued", "412k", delta="across ecosystems", dir_="up", spark=[40, 90, 160, 240, 310, 370, 412]),
                kpi("Audit findings (high)", "0", delta="last cycle, all towers", dir_="flat", spark=[2, 1, 1, 0, 0, 0, 0]),
            ],
            tabs=[
                tab("Trust depth", [
                    w_radar("Practice depth — what the tower holds itself to",
                            ["Tokenization", "Analytics", "Identity", "DLT ops", "Provenance", "Contracts"],
                            [{"name": "Delivery depth", "points": [88, 86, 84, 90, 86, 92]},
                             {"name": "Evidence rigor", "points": [92, 94, 86, 88, 90, 94]}],
                            note_="Toggle series. Evidence rigor sits above delivery depth by design — trust programs are judged by their evidence packs first."),
                    w_donut("Where digital-trust spend concentrates — engagement mix",
                            ["Tokenization", "Analytics & compliance", "Identity", "DLT networks", "Provenance", "Contracts"],
                            [24, 22, 16, 14, 15, 9],
                            unit="% of engagements",
                            note_="Click segments to pin. Tokenization and analytics lead the mix; identity is the fastest compounding practice by adoption."),
                ]),
                tab("Sector depth", [
                    w_heat("Practice depth by sector — where digital trust runs deepest",
                           ["Tokenization", "Analytics", "Identity", "DLT", "Provenance", "Contracts"],
                           ["Banking", "Public sector", "Manufacturing", "Logistics", "Energy"],
                           [[92, 88, 74, 80, 72, 84], [70, 66, 92, 84, 62, 70], [62, 60, 58, 66, 92, 78], [58, 62, 54, 60, 88, 66], [74, 58, 52, 70, 82, 76]],
                           unit="depth index",
                           note_="Hover cells for depth. Provenance carries manufacturing and logistics flagship records; identity carries the public-sector record — pick your sector cell and the practice page below."),
                ]),
            ],
            note_="Reference portfolio model: depth indices and drill pass rates from delivery, not client telemetry.",
        ),
        h2("How digital-trust engagements run"),
        p("Trust engagements are governance-heavy by design: the claim mapping or trust registry comes first, the evidence pack is generated from operating data (not assembled for the audit), and every drill — custody, recall, upgrade, recovery — is rehearsed on schedule with results filed. The practices compose: provenance trails anchor into the DLT network; credentials ride the identity fabric; contracts deploy under ceremony with their assurance bundles."),
        bullets([
            ["Governance before cryptography", "Claim mappings, trust registries and network terms — the technical rails execute what governance decides"],
            ["Evidence from operations", "Reconciliation certificates, drill results and derivations generated from running systems"],
            ["Drills on schedule", "Custody, recall, upgrade and recovery drills rehearsed — resilience is practiced, not asserted"],
            ["Audit-ready by construction", "Evidence packs generated from the same data the platform runs on — no drift between versions"],
        ]),
        cta("Bring the trust problem the auditors keep circling — the practice map and evidence-pack design land in the first diagnostic, and the drills follow on schedule."),
    ]

    # ── Tower hub: Cloud, Edge & Platform Engineering ──
    tw["services_cloud-edge-platform-engineering.json"] = [
        hero("Cloud, edge and platform engineering is the estate's load-bearing work: modernization that ratchets instead of rewrites, edge fleets that keep deciding when the WAN dies, FinOps that prices unit economics, mission-critical systems that are rehearsed rather than hoped for, the multicloud fabric that makes placement policy real, and the platform and SRE practices that make the whole estate operable."),
        h2("Seven practices from modernization to reliability"),
        p("The practice set covers the infrastructure arc: cloud-native modernization and hybrid multicloud architecture shape the estate; edge computing extends it to physics; FinOps prices it; mission-critical engineering hardens it; platform engineering makes it pleasant to build on; SRE makes it trustworthy. Each practice carries its own console — wave plans, fleet health, burn rates, drill evidence — and the portfolio view shows how they compose."),
        table("The seven practices — what each owns and its signature deliverable",
              ["Practice", "Owns", "Signature deliverable"],
              [
                ["Cloud-Native Modernization", "The strangler program", "Wave plan with ratchet discipline"],
                ["Edge Computing & Infrastructure", "The offline fleet", "Placement map + store-and-forward contracts"],
                ["FinOps & Sustainable Computing", "Unit economics", "Allocation model + commitment ladder"],
                ["High-Performance & Mission-Critical", "The rehearsed core", "Drill calendar + certification file"],
                ["Hybrid & Multicloud Architecture", "The fabric", "Placement policy + consistency plane"],
                ["Platform Engineering & DevEx", "The golden paths", "IDP with scorecards + exception registry"],
                ["SRE & Reliability Engineering", "The trust contract", "SLO documents + budget gating"],
              ]),
        h2("Why infrastructure programs stall — and what the discipline is instead"),
        p("Infrastructure programs stall on the same three patterns: rewrites that bet the quarter on a cutover weekend (the ratchet fixes that), cost programs that report invoices instead of unit economics (the allocation model fixes that), and reliability programs with SLOs nobody enforces (the budget mechanism fixes that). The seven practices close each pattern deliberately — and the portfolio console carries the depth evidence."),
        idash(
            "Cloud & platform portfolio — the seven practices on one console",
            badge="Interactive · portfolio model",
            kpis_=[
                kpi("Practices live", "7", delta="wave plans signed", dir_="flat", spark=[3, 4, 5, 6, 6, 7, 7]),
                kpi("Legacy surface", "38%", delta="of original call volume", dir_="down", spark=[100, 88, 74, 63, 52, 44, 38]),
                kpi("Waste eliminated", "23.4%", delta="FinOps rightsizing pass", dir_="up", spark=[0, 4, 9, 14, 18, 21, 23]),
                kpi("Budget health", "31%", delta="30d consumption, healthy", dir_="flat", spark=[68, 55, 48, 42, 37, 34, 31]),
                kpi("Golden-path adoption", "89%", delta="of production services", dir_="up", spark=[45, 55, 63, 71, 78, 84, 89]),
            ],
            tabs=[
                tab("Wave tracker", [
                    w_line("Infrastructure wave progress — modernization, edge, platform",
                           ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8"],
                           [{"name": "Extraction waves", "points": [8, 18, 30, 44, 58, 70, 80, 88]},
                            {"name": "Edge rollout", "points": [5, 14, 26, 40, 55, 68, 79, 87]},
                            {"name": "Platform adoption", "points": [12, 24, 38, 52, 64, 75, 83, 89]}],
                           unit="% complete", note_="Click to isolate. The three programs compound: platform adoption accelerates extraction, edge rollout inherits the placement discipline — the tracks are one program."),
                ]),
                tab("Estate health", [
                    w_heat("Practice depth by sector — where infrastructure work runs deepest",
                           ["Modernization", "Edge", "FinOps", "Mission-crit", "Platform", "SRE"],
                           ["Banking", "Telecom", "Manufacturing", "Public sector", "Retail"],
                           [[88, 70, 84, 92, 82, 90], [74, 92, 80, 76, 78, 82], [80, 88, 74, 70, 84, 78], [76, 62, 78, 84, 80, 86], [78, 74, 88, 68, 86, 80]],
                           unit="depth index",
                           note_="Hover cells for depth. Mission-critical carries the banking flagship record; edge carries telecom's — pick your sector cell and the practice page below it."),
                ]),
            ],
            note_="Reference portfolio model: wave bands and depth indices from delivery, not client telemetry.",
        ),
        h2("How infrastructure engagements run"),
        p("Modernization runs in waves with ratchet discipline (no cutover weekends); edge programs run in cohorts with WAN-kill drills; FinOps lands in one quarter (allocation model, unit costs, commitment ladder); mission-critical runs on its drill calendar from week four; platform programs baseline DORA before they build. The practices share one rule: infrastructure is judged by its operating evidence — consoles live, drills run, budgets enforced."),
        bullets([
            ["Ratchet, never big-bang", "Traffic shifts by config with reconciliation certificates — the quarter is never bet on a weekend"],
            ["Offline-first edge", "Placement by physics, store-and-forward with reconciliation — disconnection is designed"],
            ["Unit economics, not invoices", "Cost per transaction/inference/ticket, owned by teams — FinOps becomes operational"],
            ["Drills over diagrams", "Resilience proven by rehearsed failover with measured RTO — the certification file exists because drills ran"],
        ]),
        cta("Bring the estate work everyone agrees is necessary and nobody has sequenced — the wave map and first drill land in the diagnostic, and the ratchet follows."),
    ]

    # ── Tower hub: Cybersecurity & Zero-Trust ──
    tw["services_cybersecurity-zero-trust.json"] = [
        hero("Cybersecurity is an engineering discipline with a governance surface. Cybersecurity & Zero-Trust runs seven practices that secure the AI estate, measure the cloud attack surface, turn compliance into running systems, rehearse cyber recovery, modernize identity, run detection-as-code SOCs, and implement zero trust as a staged program — every practice with its own console and evidence pack."),
        h2("Seven practices from AI security to zero trust"),
        p("The practice set covers the modern attack surface: AI security protects the models and their guardrails; cloud security posture measures the surface; compliance engineering turns frameworks into pipelines; cyber resilience rehearses the recovery; identity modernization rebuilds the fabric; threat intelligence and the managed SOC run detection as code; zero-trust architecture implements the decision fabric. Each practice carries its own console — the portfolio view shows how they compose."),
        table("The seven practices — what each owns and its signature deliverable",
              ["Practice", "Owns", "Signature deliverable"],
              [
                ["AI Security & Model Protection", "The AI attack surface", "Guardrail boundaries + red-team suites"],
                ["Cloud Security & Posture", "The measured surface", "Guardrail-as-code + class-based SLAs"],
                ["Compliance, Audit & Digital Trust", "The running frameworks", "Unified control map + evidence pipelines"],
                ["Cyber Resilience & Incident Recovery", "The rehearsed recovery", "Clean-room restore + crisis playbooks"],
                ["Identity & Access Modernization", "The identity fabric", "Access graph + lifecycle automation"],
                ["Threat Intelligence & Managed SOC", "Detection quality", "Detection-as-code + purple-team accountability"],
                ["Zero-Trust Architecture", "The decision fabric", "PDP/PEP fabric + decision ledger"],
              ]),
        h2("Why security programs stall — and what the discipline is instead"),
        p("Security programs stall on the same three gaps: findings without classes (the fix queue never drains), controls without evidence (audits become archaeology), and alerts without quality (the pager trains people to ignore it). The seven practices close each gap: class-based fix SLAs, evidence pipelines from operating data, detection-as-code with published precision. The portfolio console carries the depth record."),
        idash(
            "Cybersecurity portfolio — the seven practices on one console",
            badge="Interactive · portfolio model",
            kpis_=[
                kpi("Practices live", "7", delta="evidence packs warm", dir_="flat", spark=[3, 4, 5, 6, 6, 7, 7]),
                kpi("Critical misconfigs", "3", delta="was 214 — SLAs held", dir_="down", spark=[214, 150, 96, 52, 21, 8, 3]),
                kpi("Evidence freshness", "97.4%", delta="controls automated 78%", dir_="up", spark=[41, 55, 66, 76, 84, 91, 97]),
                kpi("Drill RTO / target", "9.5/12 h", delta="tier-1, rehearsed", dir_="down", spark=[26, 19, 15, 12, 11, 10, 9.5]),
                kpi("Pages / week", "2.1", delta="SOC precision 91%", dir_="down", spark=[41, 28, 18, 11, 6, 3, 2]),
            ],
            tabs=[
                tab("Coverage", [
                    w_line("Security program progress — posture, identity, detection",
                           ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8"],
                           [{"name": "Posture SLAs held %", "points": [42, 58, 70, 80, 86, 90, 93, 95]},
                            {"name": "Identity lifecycle %", "points": [30, 44, 58, 70, 80, 87, 92, 95]},
                            {"name": "Detection coverage %", "points": [34, 45, 54, 62, 68, 74, 78, 81]}],
                           unit="%", note_="Click to isolate. Posture fixes fastest because guardrails prevent recurrence; identity compounds through lifecycle automation; detection climbs as coverage is priced against sector threats."),
                ]),
                tab("Sector depth", [
                    w_heat("Practice depth by sector — where security work runs deepest",
                           ["AI security", "Posture", "Compliance", "Resilience", "Identity", "SOC", "ZT"],
                           ["Banking", "Healthcare", "SaaS/Tech", "Manufacturing", "Public sector"],
                           [[92, 84, 88, 80, 86, 82, 78], [84, 74, 92, 88, 82, 74, 72], [86, 90, 84, 74, 88, 90, 84], [72, 78, 76, 90, 70, 68, 80], [78, 72, 94, 82, 84, 76, 74]],
                           unit="depth index",
                           note_="Hover cells for depth. Compliance carries the public-sector flagship; AI security carries banking's — pick your sector cell and the practice page below it."),
                ]),
            ],
            note_="Reference portfolio model: coverage bands and depth indices from delivery, not client telemetry.",
        ),
        h2("How security engagements run"),
        p("Security engagements are evidence-first: the posture census lands in three weeks (class taxonomy, dedup by class), the access graph in four, the SOC coverage baseline in three. Programs then run on cadence — weekly posture reports, quarterly evidence packs and purple teams, drills on calendar. The practices compose: the identity fabric feeds zero-trust decisions; the SOC consumes the decision ledger; compliance reads everyone's evidence."),
        bullets([
            ["Classes, not tickets", "Misconfigurations fixed by class with SLAs — the queue drains because recurrence is prevented"],
            ["Evidence from operations", "Audits as report exports — the control map stays queryable"],
            ["Recovery rehearsed", "Clean-room restores at production scale — resilience you can underwrite"],
            ["Detection as software", "Versioned rules with replay-tested precision — the pager earns its pages"],
        ]),
        cta("Bring the security estate where findings flood and audits consume quarters — the census and class taxonomy land in three weeks, and the evidence pipelines follow."),
    ]

    # ── Tower hub: Data, Analytics & Lakehouse ──
    tw["services_data-analytics-lakehouse.json"] = [
        hero("Data stops being a liability when it becomes infrastructure with contracts. Data, Analytics & Lakehouse runs seven practices that price risk models with validation files, rebuild pipelines on lakehouse foundations, turn datasets into products with contracts, certify the semantic layer, migrate estates by ratchet, govern master data with measurable precision, and run streaming decisioning with honest semantics."),
        h2("Seven practices from risk models to streaming decisions"),
        p("The practice set covers the data estate: advanced risk analytics and real-time streaming decisioning are the decision practices; data engineering modernization and lakehouse migration are the foundation practices; data monetization, enterprise BI and master data governance are the trust practices. Each practice carries its own console — backtests, SLA burn, cutover trackers, match precision — and the portfolio view shows how they compose."),
        table("The seven practices — what each owns and its signature deliverable",
              ["Practice", "Owns", "Signature deliverable"],
              [
                ["Advanced Risk & Predictive Analytics", "Priced uncertainty", "Validation files + priced signals"],
                ["Data Engineering & Pipeline Modernization", "Reliable foundations", "Ingestion contracts + quality gates"],
                ["Data Monetization & Analytics Products", "Products with contracts", "Evidence-based catalog + legal gates"],
                ["Enterprise BI & Executive Analytics", "Certified semantics", "One definition per metric, owned"],
                ["Lakehouse Architecture & Migration", "The replatforming ratchet", "Reconciliation certificates per table"],
                ["Master Data, Governance & Cataloging", "Entity truth", "Match precision published per version"],
                ["Real-Time Streaming & Decisioning", "Sub-second decisions", "Latency budgets + replayable decisions"],
              ]),
        h2("Why data programs stall — and what the discipline is instead"),
        p("Data programs stall on the same three patterns: silent failures nobody notices until a board meeting, definitions that multiply until the numbers argue, and migrations that never finish. The practices close each: quality gates with quarantine, one semantic definition per metric, reconciliation certificates per table. The portfolio console carries the depth record."),
        idash(
            "Data portfolio — the seven practices on one console",
            badge="Interactive · portfolio model",
            kpis_=[
                kpi("Practices live", "7", delta="contracts signed per practice", dir_="flat", spark=[3, 4, 5, 6, 6, 7, 7]),
                kpi("SLA adherence", "99.4%", delta="freshness budgets per table", dir_="up", spark=[82, 88, 92, 95, 97, 98, 99]),
                kpi("Metric disputes", "0", delta="certified semantic layer", dir_="down", spark=[14, 10, 7, 4, 2, 1, 0]),
                kpi("Reconciliation deltas", "0", delta="across migration waves", dir_="flat", spark=[12, 6, 3, 1, 0, 0, 0]),
                kpi("Duplicate rate", "1.4%", delta="customer master, was 18%", dir_="down", spark=[18, 14, 10, 7, 4, 2, 1.4]),
            ],
            tabs=[
                tab("Estate health", [
                    w_line("Data estate health — reliability, semantics, migration",
                           ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8"],
                           [{"name": "Pipeline SLA %", "points": [82, 88, 92, 95, 97, 98, 99, 99.4]},
                            {"name": "Certified usage %", "points": [34, 46, 58, 68, 76, 82, 87, 90]},
                            {"name": "Legacy footprint %", "points": [100, 88, 76, 66, 57, 50, 44, 38]}],
                           unit="%", note_="Click to isolate. Reliability fixes first (contracts at ingestion), semantics follow (the layer needs trusted foundations), migration runs as the ratchet underneath."),
                ]),
                tab("Sector depth", [
                    w_heat("Practice depth by sector — where data work runs deepest",
                           ["Risk", "Engineering", "Products", "BI", "Migration", "MDM", "Streaming"],
                           ["Banking", "Insurance", "Retail", "Manufacturing", "Healthcare"],
                           [[92, 84, 78, 86, 80, 82, 88], [90, 78, 74, 82, 76, 86, 72], [70, 80, 88, 84, 78, 76, 90], [68, 88, 72, 70, 84, 88, 86], [82, 76, 70, 78, 74, 92, 74]],
                           unit="depth index",
                           note_="Hover cells for depth. Risk carries banking's flagship; MDM carries healthcare's; streaming carries retail's — pick your sector cell and the practice page below."),
                ]),
            ],
            note_="Reference portfolio model: health bands and depth indices from delivery, not client telemetry.",
        ),
        h2("How data engagements run"),
        p("Data engagements are contract-first: the silent-failure audit and source contracts land in weeks one to three; the semantic layer certifies the five executive-critical metrics first; migrations run by cohort with dual-run reconciliation; master data programs measure precision against adjudicated truth before they merge anything. The practices compose — the lakehouse feeds the semantic layer, contracts feed the products, the catalog makes governance enforceable."),
        bullets([
            ["Contracts at ingestion", "Schema, freshness, ownership per source — breaking changes alert producers in minutes"],
            ["One definition per metric", "The semantic layer ends the metric-argument era — dashboards consume, never contain"],
            ["Ratchet migrations", "Dual-run with reconciliation certificates — the legacy footprint falls on schedule"],
            ["Precision before merges", "Match engines measured against adjudicated truth — wrong merges priced above missed matches"],
        ]),
        cta("Bring the data estate nobody trusts on Tuesday mornings — the silent-failure audit lands in three weeks, and the contracts follow on the two worst domains."),
    ]

    # ── Tower hub: IoT, Digital Twin & Robotics ──
    tw["services_iot-digital-twin-robotics.json"] = [
        hero("Physical operations become measurable when the sensor fabric is trusted. IoT, Digital Twin & Robotics runs seven practices that deploy vision at the edge, manage device fleets for a decade, synchronize digital twins against reality, instrument the plant's brownfield honestly, predict failures from physics, integrate robots with safety certification, and optimize estates at building and district scale."),
        h2("Seven practices from camera fleets to smart districts"),
        p("The practice set covers the physical estate: computer vision and connected products are the device practices; digital twins and sensor fabric are the state practices; predictive maintenance, robotics and smart infrastructure are the operations practices. Each carries its own console — fleet health, sync lag, P-F economics, exception MTTR — and the portfolio view shows how they compose."),
        table("The seven practices — what each owns and its signature deliverable",
              ["Practice", "Owns", "Signature deliverable"],
              [
                ["Computer Vision & Edge AI", "The camera fleet", "Per-camera contracts + active-learning loop"],
                ["Connected Products & Smart Devices", "The decade fleet", "A/B OTA with rollback proof + entitlements"],
                ["Digital Twin Platform Engineering", "Synchronized state", "Fidelity ladders + divergence alarms"],
                ["Industrial IoT & Sensor Fabric", "The foundation layer", "Unit contracts + Purdue-aligned segmentation"],
                ["Predictive Maintenance & Asset Intelligence", "The P-F curve", "Teardown-confirmed precision + CMMS loop"],
                ["Robotics & Autonomous Systems", "The integrated fleet", "Safety case + exception desk"],
                ["Smart Infrastructure, Buildings & Cities", "The estate platform", "M&V-verified savings + privacy by design"],
              ]),
        h2("Why IoT programs stall — and what the discipline is instead"),
        p("IoT programs stall on the same three patterns: pilots that never scale (fleet discipline fixes that), twins that drift silently (divergence alarms fix that), and integrations that ignore the plant's reality (brownfield-first design fixes that). The practices close each pattern — and the portfolio console carries the depth record."),
        idash(
            "IoT & robotics portfolio — the seven practices on one console",
            badge="Interactive · portfolio model",
            kpis_=[
                kpi("Practices live", "7", delta="fleet contracts signed", dir_="flat", spark=[2, 3, 5, 5, 6, 7, 7]),
                kpi("Assets instrumented", "1,842", delta="P1+P2 tiers complete", dir_="up", spark=[210, 420, 700, 1000, 1300, 1600, 1842]),
                kpi("Unplanned downtime", "−58%", delta="teardown-confirmed alerts", dir_="down", spark=[0, -12, -24, -35, -44, -52, -58]),
                kpi("Fleet OTA success", "99.7%", delta="48k devices, rollback proof", dir_="up", spark=[94, 96, 97.5, 98.5, 99.2, 99.5, 99.7]),
                kpi("Exception MTTR", "4.6 min", delta="robot fleet trust metric", dir_="down", spark=[22, 15, 10, 7, 6, 5, 4.6]),
            ],
            tabs=[
                tab("Fleet maturity", [
                    w_line("Physical estate maturity — sensing, twins, automation",
                           ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8"],
                           [{"name": "Sensing coverage %", "points": [20, 35, 50, 62, 74, 82, 89, 93]},
                            {"name": "Twinned assets %", "points": [10, 22, 36, 50, 62, 72, 80, 86]},
                            {"name": "Automated tasks %", "points": [5, 12, 22, 34, 46, 58, 68, 76]}],
                           unit="%", note_="Click to isolate. Sensing precedes twins (state needs truth), automation compounds on both — the sequence is the discipline."),
                ]),
                tab("Sector depth", [
                    w_heat("Practice depth by sector — where physical work runs deepest",
                           ["Vision", "Devices", "Twins", "Sensor fabric", "Predictive", "Robotics", "Smart infra"],
                           ["Manufacturing", "Logistics", "Utilities", "Real estate", "Agriculture"],
                           [[92, 84, 88, 90, 92, 88, 74], [70, 86, 76, 82, 80, 84, 70], [76, 70, 82, 88, 86, 62, 92], [66, 72, 78, 74, 70, 58, 90], [80, 76, 72, 84, 78, 66, 72]],
                           unit="depth index",
                           note_="Hover cells for depth. Predictive carries manufacturing's flagship; smart infrastructure carries real estate's — pick your sector cell and the practice page below."),
                ]),
            ],
            note_="Reference portfolio model: maturity bands and depth indices from delivery, not client telemetry.",
        ),
        h2("How physical-estate engagements run"),
        p("Physical engagements start where the physics is: the asset inventory via passive discovery, the criticality map signed with the plant team, the sampling rates set by the fault frequencies that matter. Programs then run in cohorts — cameras by station, devices by SKU, robots by zone — with the exception desks and drift queues instrumented from the start. Safety cases are living artifacts, and the consoles serve the operators first."),
        bullets([
            ["Brownfield first", "Protocol translation with unit contracts — the plant's reality is engineered around, not ignored"],
            ["Physics before models", "Fault frequencies, P-F curves and fidelity ladders — the ML layer learns on physics"],
            ["Fleet discipline", "Per-device contracts, staged OTA with rollback proof, drift queues instrumented"],
            ["Safety as living artifact", "Risk assessments re-triggered by layout changes — the certification mindset"],
        ]),
        cta("Bring the plant, fleet or estate where operations run on folklore — the asset inventory and criticality map land in six weeks, and the fabric follows with contracts."),
    ]

    # ── Tower hub: Quantum & Advanced Compute ──
    tw["services_quantum-advanced-compute.json"] = [
        hero("Advanced compute earns its budget with evidence. Quantum & Advanced Compute runs six practices that speed simulations with verification, benchmark quantum optimization honestly, run QML with documented negative results, migrate cryptography on the harvest clock, build the readiness governance, and advise on emerging compute with benchmarks instead of keynotes."),
        h2("Six practices from HPC speedups to emerging compute"),
        p("The practice set covers the compute frontier: HPC & simulation engineering is the workhorse; quantum optimization and QML are the honest-experimentation practices; post-quantum cryptography is the mandatory clock; readiness strategy is the governance layer; emerging compute advisory keeps the watch. Each carries its own console — Amdahl curves, benchmark gaps, CBOM exposure, portfolio clocks — and the portfolio view shows how they compose."),
        table("The six practices — what each owns and its signature deliverable",
              ["Practice", "Owns", "Signature deliverable"],
              [
                ["HPC & Simulation Engineering", "Wall-clock speedups", "Parallelization audits + KAT verification"],
                ["Quantum Optimization", "Honest benchmarks", "Advantage envelopes per problem class"],
                ["Quantum ML & Simulation", "Credible research", "Experiment ledger with negative results"],
                ["Post-Quantum Cryptography", "The mandatory clock", "CBOM + hybrid migration with signed caps"],
                ["Quantum Readiness & Strategy", "The governance layer", "Three-clock register + board arithmetic"],
                ["Neuromorphic & Emerging Compute", "The verified watch", "Workload-fit benchmarks + kill criteria"],
              ]),
        h2("Why advanced-compute programs fail — and what the discipline is instead"),
        p("Advanced-compute programs fail on the same three patterns: hardware ordered before the parallelization audit, advantage claims without envelopes, and readiness programs with no decision triggers. The practices close each: audits before procurement, benchmarks against tuned baselines, registers with owners and triggers. The portfolio console carries the evidence."),
        idash(
            "Quantum & advanced compute portfolio — the six practices on one console",
            badge="Interactive · portfolio model",
            kpis_=[
                kpi("Practices live", "6", delta="benchmarks signed per practice", dir_="flat", spark=[2, 3, 4, 5, 5, 6, 6]),
                kpi("Parallel efficiency", "82%", delta="at 1,024 ranks, post-audit", dir_="up", spark=[44, 55, 63, 70, 75, 79, 82]),
                kpi("Benchmark honesty", "100%", delta="claims carry envelopes", dir_="flat", spark=[60, 75, 85, 92, 96, 99, 100]),
                kpi("HNDL-exposed flows", "38", delta="migrating on the clock", dir_="down", spark=[38, 32, 26, 20, 14, 9, 6]),
                kpi("Board pack live", "5/5", delta="questions answered with arithmetic", dir_="up", spark=[1, 2, 3, 3, 4, 5, 5]),
            ],
            tabs=[
                tab("Frontier tracker", [
                    w_line("Advanced-compute progress — HPC, quantum, PQC",
                           ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8"],
                           [{"name": "HPC efficiency %", "points": [44, 55, 63, 70, 75, 79, 82, 84]},
                            {"name": "PQC hybrid coverage %", "points": [8, 20, 32, 44, 52, 58, 64, 70]},
                            {"name": "Advantage envelope (vars)", "points": [60, 80, 100, 120, 140, 160, 180, 200]}],
                           note_="Click to isolate. HPC delivers now, PQC is the mandatory clock, the advantage envelope tracks hardware honestly — the three lines run on different clocks by design."),
                ]),
                tab("Sector clocks", [
                    w_heat("Practice depth by sector — where advanced compute matters most",
                           ["HPC", "Optimization", "QML", "PQC", "Strategy", "Emerging"],
                           ["Banking", "Pharma", "Chemicals", "Energy", "Public sector"],
                           [[84, 88, 62, 92, 84, 66], [78, 66, 92, 78, 80, 70], [72, 60, 88, 70, 78, 72], [86, 82, 58, 84, 76, 78], [70, 64, 52, 88, 90, 60]],
                           unit="depth index",
                           note_="Hover cells for depth. QML carries pharma and chemicals flagship records; PQC carries banking's and public sector's — the clocks differ by sector, and so does the investment."),
                ]),
            ],
            note_="Reference portfolio model: efficiency bands and envelope sizes from delivery benchmarks, not vendor claims.",
        ),
        h2("How advanced-compute engagements run"),
        p("Advanced-compute engagements are evidence-first: the parallelization audit precedes every hardware conversation; the benchmark rig runs classical baselines before quantum claims; the CBOM prices exposure before migration sequencing; the readiness register writes decision triggers before the budget discussion. The practices compose — readiness governs what the technical practices measure, and the technology watch feeds the register."),
        bullets([
            ["Audits before hardware", "Serial fractions priced, Amdahl ceilings made visible — the solver changes before the cluster order"],
            ["Benchmarks with envelopes", "Advantage stated per problem class and instance size — claims scoped, never global"],
            ["Negative results documented", "The experiment ledger records losses with configs — the wins stay credible"],
            ["Triggers over hype", "The register's decision fires are commitments — readiness survives the hype cycle"],
        ]),
        cta("Bring the advanced-compute question the board cannot evaluate — the register and benchmark plan land in four weeks, and the first audited speedup follows."),
    ]

    # ── Services hub ──
    tw["services.json"] = [
        hero("Eight expertise domains, 54 engineering practices, one governed delivery system. Whichever domain you enter, the contract is identical: a measured baseline, a signed gate structure, a live interactive console on every practice page, and an evidence pack generated from operations — not assembled for the audit."),
        h2("How the eight domains divide the work"),
        p("The domains are cut along the lines work actually flows: Applied AI and Agentic AI cover the intelligence estate (from models to fleets); Data, Analytics & Lakehouse covers the information foundations; Cloud, Edge & Platform Engineering covers the infrastructure; Cybersecurity & Zero-Trust covers the trust surface; IoT, Digital Twin & Robotics covers the physical estate; Blockchain & Digital Trust covers verifiable evidence; Quantum & Advanced Compute covers the frontier with honest clocks. Thirteen consulting practices wrap the estate with capacity, ERP, testing and design. Every practice page opens with its own interactive delivery console — the portfolio map below is the front door."),
        table("The engagement ladder — four rungs, no leaps of faith",
              ["Rung", "What happens", "What you hold"],
              [
                ["Two-week diagnostic", "Estate measured, candidates ranked, gates drafted", "Signed baseline + scored gate map"],
                ["First build (one wave)", "The loop proven end-to-end with evidence chain", "Working system + console live"],
                ["Program waves", "Ratcheted scaling with drills and reviews", "Operating rhythm + governance artifacts"],
                ["Run & compound", "Evidence packs stay warm, registries reviewed", "Estate that appreciates, not depreciates"],
              ]),
        h2("The operating contract behind every service page"),
        p("Four commitments hold across all 54 practices. First: no page is a brochure — each carries a live interactive console with the gate thresholds and target bands delivery holds itself to. Second: every practice names its failure taxonomy — what breaks, what it costs, what ships with the build. Third: every practice is sector-aware — pick your industry on any page and the explorer shows what we deliver for that exact combination, with the sector brief one click away. Fourth: every engagement ends with artifacts that appreciate — registries, harnesses, ledgers, consoles — because a services relationship should compound."),
        idash(
            "The services portfolio — eight domains on one console",
            badge="Interactive · front door",
            kpis_=[
                kpi("Expertise domains", "8", delta="54 practices behind them", dir_="flat", spark=[8, 8, 8, 8, 8, 8, 8]),
                kpi("Practices with consoles", "54", delta="one per page, all unique", dir_="up", spark=[12, 24, 36, 45, 50, 53, 54]),
                kpi("Sectors covered", "12", delta="with sector briefs per practice", dir_="flat", spark=[12, 12, 12, 12, 12, 12, 12]),
                kpi("Industries × practices", "648", delta="combinations mapped", dir_="up", spark=[200, 320, 440, 540, 600, 630, 648]),
                kpi("Console uniqueness", "100%", delta="no two pages alike", dir_="flat", spark=[60, 75, 85, 92, 96, 99, 100]),
            ],
            tabs=[
                tab("Domain map", [
                    w_scatter("The eight domains — delivery depth vs sector breadth",
                              [sc_pt(88, 84, "Data & Lakehouse", "Foundations"), sc_pt(86, 82, "Cybersecurity", "Foundations"),
                               sc_pt(84, 78, "Applied AI", "Intelligence"), sc_pt(83, 76, "Agentic AI", "Intelligence"),
                               sc_pt(82, 74, "Cloud & Platform", "Foundations"), sc_pt(80, 72, "IoT & Robotics", "Physical"),
                               sc_pt(78, 70, "Blockchain Trust", "Physical"), sc_pt(75, 66, "Quantum", "Frontier")],
                              ["Foundations", "Intelligence", "Physical", "Frontier"], "Delivery depth (0-100)", "Sector breadth (0-100)",
                              note_="Hover for domains. Foundations run deepest because everything compounds on them; the frontier domain runs on honest clocks. Every domain's hub page links its practices with their own consoles."),
                    w_donut("Engagement mix across the estate — where programs start",
                            ["Data & Lakehouse", "Cybersecurity", "Cloud & Platform", "Applied AI", "Agentic AI", "IoT & Robotics", "Blockchain", "Quantum"],
                            [22, 19, 17, 14, 12, 10, 4, 2],
                            unit="% of engagements",
                            note_="Click segments to pin. Programs usually start on foundations or trust, then compound into intelligence and physical practices — the ladder on this page is the same map."),
                ]),
                tab("Sector heat", [
                    w_heat("Delivery depth by domain × sector — pick your cell, then the domain",
                           ["Applied AI", "Agentic", "Data", "Cyber", "Cloud", "IoT", "Blockchain", "Quantum"],
                           ["Banking", "Insurance", "Healthcare", "Manufacturing", "Retail", "Public sector"],
                           [[86, 80, 84, 90, 78, 76], [78, 82, 86, 84, 80, 70], [88, 74, 82, 84, 86, 78], [90, 76, 78, 88, 74, 84], [84, 78, 86, 82, 88, 72], [72, 70, 78, 86, 84, 92]],
                           unit="depth index",
                           note_="Hover cells for depth. This grid is the site's honest map: every cell above 60 carries delivery record — pick your sector column and enter the domain hub behind it."),
                ]),
            ],
            note_="Reference portfolio model: depth indices and engagement mix from delivery, not client telemetry.",
        ),
        h2("Where sector depth sits — and how to read it"),
        p("Depth is claimed per sector × practice combination and earned through delivery: the explorer on every practice page marks flagship combinations with an red dot and links the full sector brief — workflows, controls and reference cases for that exact pairing. Twelve industries × 54 practices = 648 mapped combinations; the sector-brief pages carry the regulatory posture, the workflow-level scope and the delivery record behind each flagship dot."),
        bullets([
            ["A console on every page", "Interactive delivery consoles with gate thresholds — the numbers are the status meeting"],
            ["A failure taxonomy per practice", "What breaks, what it costs, what ships with the build — stated on the page"],
            ["Sector briefs for 648 combinations", "Pick industry + practice — the explorer links the exact sector brief"],
            ["Artifacts that appreciate", "Registries, harnesses, ledgers, consoles — the relationship compounds"],
        ]),
        cta("Start with the two-week diagnostic — it ends with a signed baseline and a scored gate map for your estate, whichever domain you land in."),
    ]

    total = 0
    for fname, blocks in tw.items():
        w = write_page(fname, blocks)
        total += w
        print(f"  {fname:52s} {w:5d} words")
    print(f"HUBS DONE — {len(tw)} pages, {total} words")

if __name__ == "__main__":
    gen()
