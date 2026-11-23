# -*- coding: utf-8 -*-
# Phase 2 dictionaries, part 2: modules, telemetry, failure modes,
# deliverable sections, stages and the small fixed sets.

MODULES = {
  "ai data layer": "The curated data substrate models are allowed to learn from — contracts, lineage and consent enforced.",
  "ai defense layer": "Controls for the models themselves: prompt-injection fences, output screening and drift alarms.",
  "budget metering": "Every workload carries a budget; approaching it is an alert, not a month-end surprise.",
  "champion-challenger": "The incumbent and the candidate run side by side on live traffic — promotion is earned on measured deltas.",
  "contract factory": "Data and service contracts generated, versioned and enforced at the boundary — breaking changes fail fast.",
  "cost governance": "Cost ownership assigned where the spend is created — engineering and finance share one ledger.",
  "credential ecosystem": "Issuance, holding and verification designed as one system — not three vendors and a PDF.",
  "data product registry": "Every dataset published like a product — an owner, a contract, a version, a deprecation path.",
  "decision api": "The contract your applications call for a scored decision — latency budgeted, every call logged.",
  "decision analytics": "Which decisions moved the metric, and which just moved — attribution reported per quarter.",
  "decision replay": "Any past decision re-runnable with its inputs — the property auditors test first.",
  "detection-as-code": "Detections versioned, tested and peer-reviewed — the SOC ships like engineering.",
  "durable execution": "Long-running processes that survive crashes and deploys — compensation logic written, not hoped for.",
  "edge fleet": "The devices at the edge managed like a fleet — versions, health and rollouts visible in one place.",
  "evaluation use": "Evaluation runs on every candidate change — quality measured where the decision is made.",
  "evidence exports": "Evidence exported in the format your auditors already use — no screenshots of dashboards.",
  "evidence pack": "The artifacts your auditors ask for — control tests, decision trails and gate reviews in one place.",
  "feature integration": "One definition of a feature, served identically in training and inference.",
  "fleet control tower": "Agent fleets supervised from one place — queues, budgets and health per worker.",
  "governance baseline": "The current state measured honestly first — governance built on the estate you actually have.",
  "governance charter": "Decision rights written down — who decides what, at which gate, with whose evidence.",
  "guardrail configuration": "Guardrails expressed as configuration, reviewed and versioned — safety that ships with the release.",
  "hpc engineering": "Simulation and compute clusters engineered for throughput — jobs scheduled, costs attributed.",
  "identity plane": "One identity layer for people, services and models — every action attributable.",
  "incident response": "Rehearsed response with named roles — the first hour is muscle memory, not improvisation.",
  "maintenance loop": "Findings flow back into the backlog with owners — the system improves by design, not by outage.",
  "model registry": "Every model version with its evaluation record and approval — deployment reads from the registry, nowhere else.",
  "network engineering": "The network treated as a product — capacity, segmentation and observability owned end to end.",
  "pqc program": "Post-quantum migration as an inventory problem first — what must be replaced, by when, owned by whom.",
  "pipeline framework": "One pipeline pattern reused across the estate — retries, lineage and alerting inherited, not reinvented.",
  "policy engine": "Policy evaluated at the boundary, as versioned code — no unwritten rules in the hot path.",
  "policy layer": "Who may do what, evaluated consistently everywhere — the rules your regulators read are the rules that run.",
  "policy-as-artifact": "The policy document and the enforcement config generated from one source — they cannot disagree.",
  "posture guardrails": "Cloud posture enforced by guardrails at provisioning — misconfiguration prevented, not reported.",
  "provenance service": "Where each fact came from, answered as an API call — lineage that survives into production.",
  "readiness engine": "Readiness assessed against explicit criteria — the go/no-go argued with evidence, not enthusiasm.",
  "release machinery": "Releases that are boring: versioned, canaried, reversible — the excitement stays in the roadmap.",
  "role & queue engine": "Work assigned to the right role with the right capacity — queues measured, not guessed.",
  "scenario engine": "What-if runs against the twin or the model — scenarios compared on the metrics the board tracks.",
  "sensor fabric": "Instrumentation engineered end to end — tagging, sampling rates and failure modes decided on purpose.",
  "solver tournament": "Approaches compete on your data, under your constraints; the leaderboard decides, not the brochure.",
  "solver-as-a-service": "Optimization exposed as an API with SLAs, so business systems call it like any other service.",
  "streaming core": "The event spine that keeps decisions current — ordered, replayable and owned.",
  "tokenization stack": "Real assets represented on ledger with the legal wrapper done first, not retrofitted.",
  "twin core": "The synchronization heart of the twin: state estimation, drift detection and what-if replay.",
  "vision integration": "Camera feeds turned into structured events with review paths — vision that ends in action.",
  "watchlist": "High-signal entities tracked continuously — attention spent where it changes outcomes.",
  "zero-trust enforcement": "Every request authenticated, authorized and logged — trust never inherited from network position.",
}

TELEMETRY = {
  "oee uplift": "OEE tracked per line against the signed baseline — the points claimed at each gate are measured on the plant floor, not modeled.",
  "slo attainment": "Attainment reported against the published SLOs each period, with every miss carrying a written cause.",
  "alarm noise": "Alarm volume per shift counted and pruned — the alarms that remain are the ones operators answer.",
  "alert false-positive rate": "False positives measured per detection; the ones that cry wolf get tuned or retired.",
  "approval cycle time": "Approval latency measured per decision type, with the queue that caused the wait named.",
  "attestation verification": "Access attestations verified on schedule, with exceptions closed or escalated — not carried forward forever.",
  "audit evidence prep": "Evidence gathered continuously during the period, so the audit opens prepared instead of panicked.",
  "audit finding closure": "Finding closure tracked to the named owner with a date — the list shrinks or the reason is written down.",
  "batch window": "Batch windows measured against the plan every run — the number reported is the observed one.",
  "change failure rate": "Change failures counted per release path; the rate drives the release process, not the slide deck.",
  "citation precision": "Citations verified against source text on every release; precision published to the owning team.",
  "constraint violations": "Constraint breaches counted per plan cycle — a plan that violates a constraint never ships silently.",
  "cost per completed task": "Unit cost measured per completed task and trended — attributed to the team that can move it.",
  "cost per deployed service": "Service-level cost reported monthly, owned by the team that owns the service.",
  "cost per resolved query": "Cost per resolved query trended against the baseline — efficiency argued with the meter, not the estimate.",
  "dispute resolution time": "Dispute cycle time measured from raise to resolution, with the stage that stalled it identified.",
  "energy per unit": "Energy per unit measured and reported with the production numbers — efficiency and output on one page.",
  "environment lead time": "Lead time from request to running environment measured per path — the slow paths get engineered.",
  "freshness slo attainment": "Freshness attainment published per dataset — data age is uptime, treated the same way.",
  "grounded-answer rate": "The share of answers backed by retrievable evidence, sampled and verified weekly.",
  "lateral-movement dwell time": "Dwell time measured in exercises and incidents alike — segmentation proven by the clock.",
  "margin captured": "Margin attributable to the program reconciled with finance quarterly — claimed value and booked value kept identical.",
  "mean time to contain": "Containment time measured per incident class, rehearsed quarterly, reported honestly after every event.",
  "p95 response latency": "p95 latency reported from production traffic per decision path — regressions block the release.",
  "pipeline breakage mttr": "Breakage restored and measured — the repair clock starts at alert, not at someone noticing.",
  "plan quality gap": "The gap between plan and actual reported per cycle — planners see where their assumptions lied.",
  "planner override rate": "Overrides counted and reviewed monthly — a high rate is a model problem or a trust problem, and both are fixable.",
  "privileged session coverage": "Privileged sessions recorded and reviewed — coverage reported as the measured percentage, not the intention.",
  "query p95": "Query latency measured at p95 from real workloads — the number users feel is the number reported.",
  "queue utilization": "Queue depth and utilization reported per work stream — capacity argued with data at the weekly review.",
  "reconciliation breaks": "Breaks counted at source per cycle, with aging reported — none carried past the quarter unexplained.",
  "reviewer override rate": "Reviewer overrides sampled and reviewed — the reasons coded so the model can learn or the policy can change.",
  "rollback time": "Rollback rehearsed and timed — the number reported is from the last rehearsal, not the brochure.",
  "scrap & rework": "Scrap and rework measured per line and attributed to cause — the baseline signed, the movement audited.",
  "settlement cycle time": "Settlement elapsed time measured end to end, with each hand-off timed separately.",
  "solve time": "Solve time reported per problem class against the benchmark registry — improvement claimed only where measured.",
  "straight-through processing": "Straight-through share measured per process, with the exception paths named and owned.",
  "toil hours per sprint": "Toil counted per sprint and reviewed — automation backlog prioritized by the hours it returns.",
  "unplanned downtime": "Downtime measured per asset against the baseline — every event carries a cause and a countermeasure.",
  "warehouse spend per query": "Spend per query attributed to the team that wrote it — the meter everyone can see.",
}

FAILURES = {
  "agent sprawl": "Every agent ships with a scoped task, an owner and a budget — sprawl treated as a design smell, not a growth stage.",
  "alert flood": "Alerts deduplicated and correlated before they reach a human — the pages that remain are pages worth answering.",
  "audit theater": "Controls tested where the work happens, with evidence generated as a by-product — the audit becomes a walkthrough, not a reconstruction.",
  "black-box plans": "Every plan exposes its constraints and trade-offs — the schedule explains itself or it does not ship.",
  "constraint hiding": "Constraints declared up front and checked by the linter — feasibility argued in seconds, not discovered in the plant.",
  "cost creep": "Unit costs on a published budget with alerts at the threshold — creep is caught by the meter, not by the invoice.",
  "cost invisibility": "Every decision carries its cost attribution — nothing ships that cannot explain what it spends.",
  "duplicated work": "One registry, one contract per capability — the second team building the same connector gets introduced to the first.",
  "flat-network habits": "Segmentation applied where flat networks used to be — lateral movement dies on a denied connection.",
  "key fragility": "Keys rotated on ceremony with HSM custody — the compromise of one secret is never the compromise of the estate.",
  "ledger worship": "The ledger used where tamper-evidence earns its cost — everything else stays a database with a backup.",
  "metric anarchy": "One definition per metric, owned and versioned — the dashboard and the board pack cannot disagree.",
  "ot/it blur": "Plant and enterprise zones separated by design — analytics reads, control stays deterministic.",
  "observability theater": "Dashboards tied to SLOs and owned by teams — a graph nobody alerts on is a decoration.",
  "on-chain pii": "Personal data never written on-ledger — hashes and references only, verified in design review.",
  "override culture": "Overrides counted and reviewed monthly — silence around overrides is the finding, not the fix.",
  "pii escape": "Personal data fenced at the boundary with redaction before any model or analyst sees it.",
  "runaway loops": "Agent loops budgeted and capped — a runaway worker stops at the wallet, not at the incident review.",
  "silent prompt drift": "Prompts versioned and evaluated like code — a change to a prompt is a change to the product.",
  "silent schema drift": "Contracts enforced at the boundary — schema drift fails the pipeline loudly, in minutes.",
  "snowflake infrastructure": "Pilot estates retired on a date with an owner — snowflakes melt on purpose.",
  "solver worship": "Every optimization run benchmarked against the best classical solver — the winner ships, every time.",
  "twin decay": "Twin drift measured against sensors on a schedule — a stale twin is flagged, not trusted.",
  "ungrounded fluency": "Answers require retrievable evidence — fluency without grounding fails the eval and stays off the menu.",
}

RECEIVE = {
  "baseline diagnostic": "The starting position for every metric in scope, measured with your team and signed before build work begins.",
  "certified delivery pod": "A named team with the clearances your estate requires — the same people from diagnosis to handover.",
  "decision and control map": "Every decision the system makes, who owns it, and where the human checkpoint sits.",
  "evidence pack": "The artifacts your auditors ask for — control tests, decision trails and gate reviews in one place.",
  "joint architecture pack": "The target architecture drawn against your estate, with interfaces and owners made explicit.",
  "support map": "Who answers when something breaks — named roles, response expectations and the escalation path.",
  "value ledger": "The running record of measured deltas against the signed baseline, reconciled with your finance team.",
}

GET = {
  "architecture pack": "The design drawn against your estate — components, owners and the interfaces between them.",
  "working system": "The thing itself, running in your environment — not a demo, not a prototype on someone's laptop.",
  "run model": "How it is operated after handover — runbooks, on-call shape and the training your teams receive.",
  "value audit kit": "The method and worksheets that let your own analysts reproduce every delta we claim.",
}

STAGES = {
  "diagnose": "We measure the starting position and lock the baseline with your team — no build work begins before the number is agreed.",
  "prove": "A bounded pilot on your real data, with the gate review scheduled before the first commit is written.",
  "industrialize": "Runbooks, enablement and the control trail that let your teams operate it without us in the room.",
  "compound": "Quarterly re-audits and a ranked backlog of the next decisions worth automating — value that accumulates on purpose.",
}

ROLLOUT = {
  "diagnose (2-4 weeks)": "Baseline measured and signed, the metric and owner named, the risk envelope agreed in writing.",
  "prove (6-10 weeks)": "The pilot runs on real data with a control group — the gate review happens whether the news is good or not.",
  "industrialize (1-3 quarters)": "Hardening, enablement and scale-out in that order — no rollout faster than the evidence.",
  "compound (ongoing)": "The next decisions enter the same loop — the backlog ranked by measured value per week of effort.",
}

FIRST90 = {
  "weeks 1-4": "Baseline measured and signed, owners named, the decision map drafted from how work actually flows.",
  "weeks 5-8": "The pilot runs on real data against a control group, with the first gate review on the calendar.",
  "weeks 9-13": "The measured delta reviewed at the gate; the scale decision made on evidence, with the runbook already drafted.",
}

VENDORQ = {
  "question 1": "Ask for the baseline: how was the starting position measured, and who signed it?",
  "question 2": "Ask for the trail: can your auditors replay any decision the system made last week, end to end?",
  "question 3": "Ask for the unit cost: what does one decision cost to run, and who owns keeping it down?",
}

DIFFERENTLY = {
  "design the operating model": "The operating model is designed first — who decides what, at which gate, holding which evidence.",
  "gate the enthusiasm": "Every stage has a gate with real stop authority — scope expands on measured deltas, not on momentum.",
  "generate evidence in-flight": "Evidence is generated while the work happens, so the audit is a walkthrough, not an archaeology project.",
}

TRANSFER = {
  "what transferred directly": "What moved unchanged between sectors, and why it was safe to move — stated plainly.",
  "what never transfers": "What does not transfer between estates, and the adaptation it needs — named before the pilot, not after.",
}

DETAILS = {
  "evidence": "The evidence behind the claim, attached — method note, measurement window and who verified it.",
  "scope": "What is in scope and, as importantly, what is not — written before the pilot starts.",
  "timing": "The realistic schedule with the gate dates on it — including the decision points where the program can stop.",
}

KEYQ = {
  "is this real in production?": "The references here run in production today — the pages name the shape of the deployment and what it took.",
  "what does it cost to be honest?": "Evaluation, audit trails and guardrails cost real engineering time — the honest answer includes that line item.",
}

COMPLIANCE = {
  "ai-specific": "AI-specific obligations mapped to controls — model risk, transparency and human oversight, owned by name.",
  "soc 2 type ii / iso 27001": "The control estate mapped to SOC 2 and ISO 27001 criteria, evidence produced continuously.",
  "sector regimes": "Sector rules translated into controls per jurisdiction — the mapping is data, reviewed when the regime moves.",
}

DEPLOY = {
  "customer tenancy": "Deployed inside your tenancy, your keys, your logs — the default for regulated estates.",
  "achala managed": "Operated by us under contract — SLOs published, changes gated, your auditors given a walkthrough path.",
  "hybrid / edge": "Split by design: what must stay local stays local, what benefits from scale scales.",
}

CHANGES = {
  "accountability": "Decision ownership named per metric — the org chart and the system agree on who answers.",
  "evidence by default": "Evidence generated as a by-product of doing the work — audit readiness stops being a season.",
  "pattern apply": "The pattern is applied to your estate, not imposed on it — adaptations recorded where they differ.",
  "pattern draw on": "The program draws on the pattern library where it fits and departs from it where your estate says otherwise.",
  "pattern use": "The pattern is used where it fits; where your estate differs, the difference is written down and owned.",
}

TOWER_DESC = {
  "applied ai & generative ai": "Strategy through production operations — models evaluated, retrieval grounded, cost per answer owned.",
  "applied ai & genai": "Strategy through production operations — models evaluated, retrieval grounded, cost per answer owned.",
  "agentic ai & hyperautomation": "Digital workers with roles, budgets and human checkpoints — every action logged and reversible.",
  "data, analytics & lakehouse": "Pipelines, governance and products on a lakehouse contract — reports that reconcile, lineage you can trace.",
  "data & lakehouse": "Pipelines, governance and products on a lakehouse contract — reports that reconcile, lineage you can trace.",
  "cybersecurity & zero-trust": "Identity-first security for people, machines and models — detection, response and audit in one program.",
  "cyber & zero-trust": "Identity-first security for people, machines and models — detection, response and audit in one program.",
  "cloud, edge & platform engineering": "Reliable estates at lower unit cost — hybrid multicloud, edge fleets and SRE discipline.",
  "cloud, edge & platform": "Reliable estates at lower unit cost — hybrid multicloud, edge fleets and SRE discipline.",
  "quantum & advanced compute": "Optimization and PQC migration — every quantum-inspired run benchmarked against the best classical solver.",
  "quantum & advanced compute": "Optimization and PQC migration — every quantum-inspired run benchmarked against the best classical solver.",
  "blockchain & digital trust": "Permissioned networks, credentials and provenance — digital trust regulators can inspect.",
  "iot, digital twin & robotics": "From sensor data to actuation — industrial IoT fabrics, twins and vision that close the loop.",
  "iot, twin & robotics": "From sensor data to actuation — industrial IoT fabrics, twins and vision that close the loop.",
}

# ── pools for variable-label sections (use {L} slot) ─────────────────────
OUTCOME_POOL = [
  "{L} is tracked weekly against the baseline signed in week two — the number at each gate is the number finance sees.",
  "{L} has a named owner and a fortnightly reading; the gate review compares it to the signed baseline, not to a promise.",
  "Progress on {L} is measured in your environment, on your data — the method note ships with the number so your analysts can reproduce it.",
  "{L} is part of the steering pack from week two: current value, signed baseline and the delta since the last gate, on one line.",
  "We commit to {L} as a measured outcome — reported every fortnight, audited at the gate, owned by a name on both sides.",
  "{L} moves at gates, not in slideware: the value claimed at each gate is reconciled with your team before it enters the ledger.",
  "The commitment on {L} is written into the engagement charter — scope, owner and the measurement method agreed before delivery begins.",
  "{L} is reported against the signed baseline with the evidence attached; if the number stops moving, the program says so.",
]

PRESSURE_POOL = [
  "{L} is one of the pressures we hear first in estates like yours — the diagnostic puts a measured number on it before anything is promised.",
  "{L} shows up in the first conversations with every team we meet in this space; the design gate assigns it an owner and a countermeasure.",
  "When {L} is the pain, the baseline audit usually confirms it is structural, not personal — the fix is designed for the system, not the people.",
  "{L} costs real money every quarter it goes unmeasured; the first two weeks of the engagement exist to price it honestly.",
  "We treat {L} as a symptom with a cause — the diagnosis traces it to the decision or the contract that produces it.",
  "{L} is where programs like this usually start: unglamorous, measurable and worth more than the technology conversation it replaces.",
]

CASE_REF_POOL = [
  "The measured delta and the method note are written up on the case page — anonymized by agreement, baseline audited.",
  "Written up as a case study: the baseline, the measured outcome and the method, with client identity withheld by agreement.",
  "The engagement is documented on its case page — what was measured, what moved and how the evidence was gathered.",
  "You can read the shape of this engagement on the case page: baseline locked early, outcome measured against it, method available under NDA.",
]

INSIGHT_REF = [
  "The full argument is in the article — with the vendor questions to bring to your next evaluation meeting.",
  "Written up as a viewpoint on the Insights page, including what we would do differently.",
  "The article carries the thesis, the counter-argument and the checklist we use on real programs.",
]

PORTFOLIO_FALLBACK = [
  "{L} connects to this work through the decision layer — the pattern above is what makes the link concrete.",
  "Where {L} fits: the same baseline-and-gate discipline applies, with the surfaces adapted to what that part of the portfolio actually runs.",
  "{L} shares the control trail with this capability — evidence captured once, reused everywhere it is audited.",
  "The portfolio link to {L} is deliberate: shared platforms, one delivery standard, no bespoke governance per program.",
]

STAT_FREE = [
  "Measured against the signed baseline each gate; the delta and its method note are reported, not promised.",
  "Tracked in the steering pack from week two, owned by a named engineer, reported honestly at every gate.",
  "The measurement method is agreed with your team first, so the number at the gate is a number both sides trust.",
  "Reported per fortnight against the signed baseline — improvements claimed only where the measurement shows them.",
  "The current reading, the signed baseline and the gate-by-gate delta live in one ledger your finance team can audit.",
]
