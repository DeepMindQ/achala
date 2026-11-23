# -*- coding: utf-8 -*-
# Phase 2 paragraph rewriters — honest, human-voiced paragraphs per section.
# {T} = page title, {IND} = industry name, {TW} = tower name when derivable.

# Each section: list of variants. The engine picks deterministically per page,
# avoiding within-page duplicates of the same variant.

PARAS = {
  "Reference architecture": [
    "The architecture for {T} is deliberately auditable: every stage exposes its inputs, its owner and its failure policy, and the decision path shares a timeline with the audit path. Nothing important happens off the record.",
    "What holds {T} together is discipline at the boundaries — typed contracts between stages, versioned releases, and a replay trail for every decision. The diagram above shows how the pieces compose; the gate reviews are what keep them honest.",
    "The reference pattern behind {T} is boring on purpose: contracts at every boundary, an owner per component, and evidence captured where the work happens. Boring architecture is what survives contact with an audit.",
    "We engineer {T} so that regressions are cohorts, not surprises: each stage owns its latency budget and failure policy, and rollback is rehearsed before go-live rather than after the incident.",
    "{T} runs on a structure your control owners can interrogate — the decision plane, the evidence plane and the governance plane stay separate in design and reconciled in operation.",
    "Every component in {T} has a contract, a version and a named owner. When something drifts, the ticket goes to a person, not to a committee — that is what the reference architecture is for.",
  ],
  "How a delivery runs": [
    "A delivery for {T} runs on rhythm, not ritual: the baseline is signed in the first weeks, evidence is generated as the work happens, and the gate at each stage has real stop authority. Programs that miss their evidence stop.",
    "The rhythm for {T}: measure first, prove on real data, industrialize what survived the gate, and review the delta every fortnight with the people accountable for the number.",
    "{T} follows the same delivery pattern as every Achala program — baseline, bounded pilot, gate review, then scale. The difference from a traditional program is that each step produces evidence your auditors can walk.",
    "Delivery on {T} is sequenced so the measurement always precedes the build: two weeks of baseline before the pilot, a scheduled gate before any scale-out, and a fortnightly reading against the signed number.",
    "We run {T} in gates: each one reviews measured deltas against the signed baseline with your named owners in the room, and each one can stop the program. That is the discipline most enterprise programs are missing.",
  ],
  "Where this fits in the portfolio": [
    "{T} is one entry in a wider portfolio that shares platforms, contracts and a delivery standard. The fit matters: programs compose on the same rails, so what one program builds, the next inherits.",
    "Inside the portfolio, {T} draws on the shared platforms — the same governance, the same evidence trail, the same unit-cost discipline. No bespoke stack per program, no orphaned governance.",
    "The reason {T} sits where it does in the portfolio: it composes with the neighboring capabilities on shared contracts, and it hands its evidence to the same ledger your finance team already reads.",
    "{T} rarely ships alone. The portfolio view shows the services and platforms it draws on — and the ones it feeds — so sequencing decisions are made with the whole estate in view.",
    "This page is part of a portfolio engineered to compose: {T} shares the decision layer, the audit trail and the platform rails with the entries around it.",
  ],
  "Overview": [
    "{T} in one paragraph: we measure the starting position honestly, design against your actual estate, and let the measured delta — not the deck — decide what scales.",
    "The short version of {T}: named metrics, named owners, evidence that travels. The sections below walk through the pattern, the components and the commitments.",
    "{T} exists because the hard part of this work is not the model — it is the measurement, the ownership and the audit trail. That is what this page describes.",
    "This page covers {T} the way we deliver it: the pattern, the stack it runs on, the guards we ship and the artifacts your team holds at the first quarter close.",
  ],
  "How the engagement runs": [
    "An engagement on {T} starts with a two-week baseline audit, runs a bounded pilot against a control group, and reaches its first gate with measured deltas — before any scale decision is made.",
    "The engagement pattern for {T}: diagnose, prove, industrialize, compound. Each gate reviews evidence with your named owners, and each gate can stop the program.",
    "We run {T} the way we run every program: the metric is signed before delivery, the pilot is bounded, and the scale decision follows the measured delta, not the momentum.",
  ],
  "Operating context": [
    "The operating context for {T} is set by your regulatory reality, your decision pressure and the estate you actually run — the design starts from those three, not from a reference model.",
    "{T} is delivered inside your operating context: the rules you are held to, the latency your decisions need, and the systems your teams already trust.",
    "Before proposing anything, we map the context {T} will run in — regulators, decision cadence, existing contracts — because the design that ignores context fails at the gate.",
  ],
  "The argument": [
    "The argument for {T} is simple: decisions made on stale information cost more than the platform that would make them current — and the gap is measurable in weeks, not years.",
    "{T} rests on one claim: enterprises that industrialize measurement ship faster and defend it in audit. The pages that follow show the mechanics, not just the claim.",
    "Why {T}: because the differentiated advantage has moved to the data layer and the operating model around it. The technology is the commodity; the discipline is the moat.",
  ],
  "The delivery pattern": [
    "The delivery pattern behind {T} is the one this site describes everywhere: signed baseline, bounded pilot, gates with stop authority, and a value ledger your finance team can audit.",
    "{T} uses the standard Achala delivery pattern — nothing bespoke about the governance, everything bespoke about the design. That split is deliberate.",
    "What repeats across programs like {T} is the pattern; what never repeats is your baseline. The pattern carries the discipline, your estate sets the design.",
  ],
  "Where programs fail with this": [
    "Programs like {T} rarely fail on the technology. They fail on unnamed ownership, unmeasured baselines and ungated scope — the three failure modes the guards on this page are built for.",
    "The honest list of where {T} programs go wrong: no signed baseline, gates without stop authority, evidence reconstructed after the fact. Each has a named guard in the sections above.",
    "We can describe exactly where {T} programs stall, because we have inherited enough of them: contract-less integrations, drift without owners and dashboards nobody alerts on. The pattern exists to prevent precisely these.",
  ],
  "Prerequisites and data readiness": [
    "{T} has honest prerequisites: named owners for the source systems, contracts for the data that crosses boundaries, and access your security team has approved in writing.",
    "Before {T} starts, three things need to exist: a metric your board recognizes, data access under an approved path, and a named owner on each source system. The readiness check takes two weeks and says no when it should.",
    "The readiness work for {T} is unglamorous and decisive — data contracts, access paths and owner names. Programs that skip it discover the gaps at the first gate, which is the most expensive place to find them.",
  ],
  "Why it matters": [
    "{T} matters because the decision it improves is made hourly, and a small change in its quality compounds across the year — which is why we measure it before we promise anything.",
    "The reason {T} earns a program rather than a pilot: it sits on a decision path with budget attached, where measured deltas become money rather than slides.",
    "{T} matters where it sits — on the path between a signal and an action. Programs on decision paths pay back measurably; programs on reporting paths usually do not.",
  ],
  "Platform stack": [
    "{T} runs on platforms you likely already own, composed on contracts rather than replaced by magic — the stack below names each piece and the job it is actually doing.",
    "The stack for {T} is assembled per estate, but the pattern is stable: one event spine, one governance plane, one decision layer — and no component without a named owner.",
    "Every item in the {T} stack earns its place on measured cost and performance, not on vendor momentum. Where a component is already serving you well, we integrate it instead of replacing it.",
  ],
  "How a joint engagement runs": [
    "A joint engagement on {T} runs with your team in the driving seats that matter: your owners sign the baseline, your analysts reproduce the deltas, and your auditors walk the trail without us in the room.",
    "The joint pattern for {T}: our pod does the build, your named owners hold the gates, and the evidence is generated in systems your teams already operate.",
    "Joint delivery on {T} is designed for handover from the first week — runbooks written as we go, decisions mapped to your owners, nothing that only we can operate.",
  ],
  "How programs use it": [
    "Programs use {T} where a decision needs to be current and defensible at once — scored in-flight, logged end to end, and reviewed at the same gates as every other program.",
    "In practice, {T} enters a program at the decision layer: the systems keep their jobs, the decisions get a contract, an owner and a trail.",
    "Teams adopt {T} one decision at a time — first the one with budget attached, then the neighbors that share its data. The pattern spreads on measured deltas.",
  ],
  "Capability pages for this industry": [
    "The capability pages for {IND} map each technology to the decisions it actually touches in your sector — written against the regulatory reality, not the brochure.",
    "Each page below takes one capability into {IND} specifically: the constraints, the decision cadence and the evidence your regulator expects.",
    "The pages linked here are {IND}-specific on purpose — a pattern that ignores sector regulation is a demo, and this site does not publish demos.",
  ],
  "Integration pattern": [
    "The integration pattern for {T} is read-first and contract-first: integrate to the system of record without copying it, and let typed contracts govern what crosses the boundary.",
    "{T} integrates through contracts, not through point-to-point goodwill — each connection has a schema, an owner and a failure policy agreed before it goes live.",
    "Integration for {T} follows one rule: the system of record stays authoritative. Decisions and analytics read from it; nothing writes back without a reviewable path.",
  ],
  "Mandate": [
    "The mandate for {T} is written, not assumed: the metric, the owner, the risk envelope and the gates — four lines your board can read.",
    "{T} operates under a mandate that names what it may decide, what it may only recommend, and who answers when either boundary is tested.",
    "We start {T} by writing the mandate down — decision rights, budget authority and stop conditions — because unstated mandates are how programs drift.",
  ],
  "How this office works with clients": [
    "This office works with clients the way every Achala delivery works: named teams, signed baselines, gates with evidence — with regional time zones covered by the pod, not by heroics.",
    "Clients of this office get the same delivery standard as everywhere else in the portfolio — the local part is language, time zones and regulatory familiarity, not a different method.",
    "From this office, {T} programs are run by pods that stay with the engagement from diagnosis to handover — the same people your auditors will meet.",
  ],
  "Inside the practice": [
    "Inside the practice, {T} work is organized around decisions rather than tools: a small pod of engineers and domain leads, a shared evidence standard, and gates that mean what they say.",
    "The practice behind {T} is deliberately small per program — senior people, short feedback loops, and a rule that whoever designs it also sees it run.",
    "What the practice looks like day to day: baseline work in the client's systems, evaluation runs before every release, and gate reviews where the number argues with the roadmap.",
  ],
  "What happened": [
    "What happened: the baseline was signed in the first two weeks, the pilot ran against a control group, and the measured delta went to the gate — the account below stays close to that evidence.",
    "The account here is deliberately plain: what was measured, what was built, what the gate reviews found. The case page carries the numbers and the method note.",
    "This is what happened, reconstructed from the engagement's own evidence trail rather than from memory — the case page holds the measured deltas.",
  ],
  "What happens next": [
    "What happens next: the gate decision, the scale plan and the runbook handover — each scheduled on the calendar, each with its evidence attached.",
    "The next steps are the boring ones that make programs stick: runbooks, enablement for the teams who will operate it, and the quarterly re-audit in the diary.",
    "After the gate, the program enters the loop it will stay in: fortnightly readings, quarterly re-audits and a ranked backlog of the next decisions worth automating.",
  ],
  "Adjacent units": [
    "The units adjacent to this one share contracts and evidence trails — a change here is visible there, which is exactly why the portfolio composes instead of colliding.",
    "Adjacent units draw on the same platforms and the same governance, so integration between them is a contract review, not a project.",
    "What borders this unit matters: the shared decision layer means improvements here raise the baseline for the neighbors without a migration.",
  ],
  "The operator's story": [
    "The operator's story is the one that matters: what the day looks like after the program, what alarms they answer, and what they would not go back to.",
    "Told by the operator: the runbooks they actually open, the overrides they still make, and the evidence trail that ended the arguments about whose number was right.",
    "We record the operator's story at handover, not at kickoff — it is the test of whether the system was industrialized or merely installed.",
  ],
  "Performance envelope": [
    "The performance envelope for {T} is published: latency, quality and cost bands the system is engineered to hold, with breaches treated as incidents, not as rounding.",
    "Every claim about {T} lives inside a measured envelope — what it holds at load, where it degrades first, and what the rollback path costs.",
    "We publish the envelope rather than the peak: the conditions under which {T} performs, and the monitoring that notices when it leaves them.",
  ],
  "In practice": [
    "In practice, {T} looks like fewer meetings about whose number is right, and more meetings about what to do next — because the evidence trail settled the first question.",
    "In practice the change is structural: decisions arrive with their evidence attached, and the arguments move from data quality to business choices.",
    "What it looks like in practice: one ledger for the metric, one trail for the decision, and gates that run on time because the evidence is already assembled.",
  ],
  "Where this shows up in our work": [
    "{T} shows up in our work wherever a decision is repeated enough for measurement to matter and regulated enough for evidence to be mandatory.",
    "You will find this pattern in the case pages and the industry hubs — the same structure: baseline, bounded build, measured delta, named owner.",
    "The footprint of {T} across our work is visible in the portfolio — the programs that share its platforms also share its evidence standard.",
  ],
  "Where the tower applies": [
    "This tower applies where the constraint is decision quality under regulation — the services below are the ones we deploy first in estates like that.",
    "The tower's services earn their place by the decisions they touch: if a service does not move a measured metric, it is not in the default kit.",
    "Applied where it matters: the tower maps to decision paths with budget attached — everything else is optional and priced as such.",
  ],
}

INDUSTRY_PARA_KEY = "Why this matters in "


# ── diagram captions (block type 'diagram', field 'note') ────────────────
DIAGRAM_NOTES = {
  "pipeline": [
    "Each stage passes its output forward under a typed contract — schema, owner and freshness agreed in advance; the audit path shares the timeline with the data path.",
    "The flow is linear on purpose: every hop owns its latency budget and failure policy, and a regression in one stage is a cohort, never an estate-wide surprise.",
    "What the diagram shows: ingestion, transformation and serving as separate responsibilities with named owners — no stage silently trusts the one before it.",
    "Contracts between stages are enforced at the boundary, so schema drift fails loudly in minutes instead of quietly in a quarter.",
    "The pipeline is measured end to end; each stage reports its own freshness and cost, which is what makes the unit economics arguable.",
  ],
  "decision-fabric": [
    "Signals, context and policy converge at the decision layer; every scored decision is logged with its inputs so it can be replayed at audit.",
    "The fabric routes each decision through the same contract: score with reasons, policy check, human checkpoint where the mandate says so.",
    "What the diagram shows: decisions as first-class records — the decision, its evidence and its owner bound together from creation.",
    "Every path through the fabric ends in either an executed action with a trail or a reviewed exception — nothing dissipates into a dashboard.",
    "The decision layer is shared infrastructure: one contract per consumer, one ledger per decision, one owner per metric.",
  ],
  "zero-trust-mesh": [
    "Every request verifies independently — identity, posture and policy checked at each edge, so trust is never inherited from network position.",
    "What the diagram shows: the verification mesh around people, services and models — each hop authenticated, authorized and logged.",
    "Lateral movement dies here: workload identity and micro-segmentation mean one compromised node is one node, not the estate.",
    "The mesh treats models like any other principal — scoped credentials, audited calls and the same revocation path as people.",
    "Verification is continuous, not perimeter-shaped: sessions re-check as posture changes, and the evidence lands in the same trail your auditors read.",
  ],
  "edge-topology": [
    "What runs at the edge is chosen by physics, not fashion: latency, bandwidth and autonomy constraints decide placement — and the fleet is managed as one estate.",
    "The topology shows the split: local actuation where the round trip forbids the cloud, regional aggregation where scale pays, cloud where the models train.",
    "Edge nodes ship with the same controls as the core — identity, monitoring and rollback — because a branch office is not a demilitarized zone.",
    "Data flows uphill under contract: what the center learns from the edge is agreed, versioned and auditable like every other boundary.",
    "The fleet updates on staged rollouts with health gates — a bad model version cannot take the whole estate down at once.",
  ],
  "orchestration-loop": [
    "The loop is closed on purpose: plan, execute, measure, replay — each agent action lands in the same trail the gate reviews read.",
    "What the diagram shows: orchestration as a control loop with budgets — agents act inside policy envelopes and hand off before the envelope ends.",
    "Human checkpoints are placed where the mandate says money or commitments move; everywhere else the loop runs and records.",
    "Every iteration is replayable — the inputs, the policy state and the outputs — which is what turns an agent demo into an auditable system.",
    "The orchestration layer owns sequencing and recovery; the workers own their single tasks; the ledger owns the truth about what happened.",
  ],
  "delivery-cadence": [
    "The cadence is the governance: baseline at the start, evidence generated as work happens, gates with stop authority on fixed dates.",
    "What the diagram shows: the rhythm of a program that measures before it builds — no gate runs on reconstructed evidence.",
    "Each gate reviews the measured delta against the signed baseline with the owners in the room; the calendar does the enforcing.",
    "The fortnightly reading and the quarterly re-audit are the loop's heartbeat — the program cannot drift far between two beats.",
    "Cadence is what separates discipline from intention: this diagram is the calendar, and the calendar is the control.",
  ],
  "twin-loop": [
    "The twin stays honest by closing the loop with sensors: state estimated, drift measured, and what-if runs rehearsed before actuation.",
    "What the diagram shows: perception, synchronization and actuation as one loop — with the human operator holding the final gate.",
    "The twin is only as good as its last synchronization; drift is measured on a schedule and flagged rather than trusted.",
    "Actuation paths are guard-banded — the optimization can propose, the envelope decides, and the plant floor stays inside engineering limits.",
    "Scenario runs replay against the synchronized state, so the plan you ship has already met the conditions you fear.",
  ],
  "optimization-funnel": [
    "Every formulation enters the funnel with its constraints declared; infeasible candidates die in seconds, and survivors are benchmarked against the best classical solver.",
    "What the diagram shows: candidate solutions narrowed by feasibility, then benchmark, then gate — the winner ships with its evidence.",
    "The benchmark registry keeps the tournament honest: same problems, same constraints, results recorded whatever wins.",
    "Optimization earns its place by measured delta on the planning metric — the funnel exists to stop solver worship before it starts.",
    "Formulation is the craft: most of the value is decided when the problem is encoded, long before any solver runs.",
  ],
  "ledger-chain": [
    "What goes on-ledger is what must be tamper-evident — commitments, consents and attestations; the bulk stays off-chain, linked by hash.",
    "What the diagram shows: the split between ledger and systems of record — anchors for trust, databases for scale, contracts between them.",
    "Writes are governed by consensus among known parties; reads are provable without trusting the writer.",
    "The chain anchors evidence, not data dumps — audit exports re-verify against the anchor and fail loudly if history has been edited.",
    "Trust here is architectural: counterparties verify instead of reconcile, and the dispute conversation starts from a shared record.",
  ],
  "layered-stack": [
    "The stack reads bottom-up: platform rails, governance plane, decision layer, experience — each layer contract-tested against the one below.",
    "What the diagram shows: separation of concerns as an operational choice — replace a layer without renegotiating the whole estate.",
    "Ownership maps to layers: one team per stratum, contracts at the interfaces, no shared blind spots.",
    "Governance sits as its own layer on purpose — it is enforced where the boundaries are, not administered from a slide.",
    "The layering is what makes the estate auditable: any claim can be traced down through the contracts that carry it.",
  ],
}

# ── CTA band lines (block type 'cta') ────────────────────────────────────
CTA_LINES = {
  "case_study": [
    "Run the same diagnostic on your estate: the baseline that anchored this program takes two weeks, and yours is measured the same way.",
    "Bring your metric to a briefing — we will walk the method behind this engagement and what it would take to measure yours.",
    "The diagnostic that locked this baseline is a two-week exercise; the briefing explains what it would find in your estate.",
    "See the method behind this case at a briefing: the measurement, the gates and the evidence your auditors would ask for.",
  ],
  "sub_capability": [
    "Start with a value assessment: your baseline measured and signed in two weeks, then a delivery plan priced from evidence.",
    "Book a briefing with the practice lead — 45 minutes on your metric, our method and an honest read on feasibility.",
    "The first step is measurement, not a proposal: two weeks to sign a baseline you would defend in front of your board.",
    "Talk to the practice lead about this capability — bring the decision you need to move, leave with a measurement plan.",
    "A value assessment prices the delta in your estate before anything is signed — two weeks, your data, one honest number.",
  ],
  "insight_article": [
    "Bring this thesis to your next evaluation meeting — or bring it to us; the briefing is 45 minutes and the first hour of thinking is free.",
    "If the argument lands, the next step is small: a working session with the practice lead to test it against your estate.",
    "Test the thesis against your own data — a value assessment is the shortest honest path from argument to evidence.",
    "Talk to the practice lead — bring your context, and we will argue the counter-case as seriously as the case.",
  ],
  "industry_capability": [
    "Start with a sector-calibrated value assessment: your baseline measured against the rules you are actually held to.",
    "Book a briefing with the industry practice — the method is the same, the regulatory mapping is yours.",
    "The first step is a measured baseline in your sector context — two weeks, your data, the controls your regulator expects.",
    "Talk to the industry practice lead about where this capability pays back first in estates like yours.",
  ],
  "platform_overview": [
    "See the platform against your use case — a working session, not a demo script, with your data shape on the table.",
    "Book a platform session: we bring the architecture, you bring the use case, and the evaluation criteria are yours.",
    "The next step is a working session on your use case — the platform's evidence trail included.",
    "Arrange a briefing with the platform team — architecture, controls and the unit economics, on the record.",
  ],
  "platform_usecases": [
    "Pick the use case closest to yours and bring it to a working session — the reference flows adapt to your estate, not the reverse.",
    "Book a working session on your scenario: the flows on this page are the starting point, your constraints are the rest.",
    "Talk to the platform team about your use case — the reference flows translate quickly once your constraints are on the table.",
  ],
  "insights_category": [
    "Read the viewpoints, then argue with them — the briefing exists for the arguments that survive.",
    "The library is the thesis; the briefing is where it meets your estate. Bring the category that hurts most.",
    "Subscribe to the briefing or book one — both start from the same evidence-first view of the category.",
  ],
  "leadership_profile": [
    "Reach out directly — the profile lists the practice areas and the briefing calendar; responses come from the person, not a pipeline.",
    "Book time with the practice lead directly — the calendar on the contact page is real, and the first conversation is a working one.",
    "Contact the practice directly — briefings are 45 minutes, working-session format, no pitch deck required.",
  ],
  "newsroom_article": [
    "For press enquiries, use the newsroom contact — named inbox, one business day response.",
    "Media contact details are on the contact page — a named inbox with a one-business-day response expectation.",
    "Questions on this release go to the newsroom inbox — answered by a person within one business day.",
  ],
  "service_page": [
    "Start with a value assessment: two weeks, your portfolio value concentration measured and signed, a delivery plan priced from evidence.",
    "Book an executive briefing — 45 minutes with the practice lead: your metric, our method, an honest feasibility read.",
    "The first step is a signed baseline, not a proposal — the value assessment exists to price the delta before anything is committed.",
  ],
  "subindustry_page": [
    "Start with a value assessment calibrated to your sub-sector — the regulatory mapping is part of the two weeks.",
    "Book a briefing with the sector practice: your metric, your regime, and an honest read on the first measurable move.",
    "The measurement comes first: two weeks to a signed baseline under the rules your sub-sector is actually held to.",
  ],
  "platform_architecture": [
    "Walk the architecture with the platform team — a working session that includes the evidence trail your auditors would test.",
    "Book an architecture session: the diagrams on this page, walked live, with your integration constraints on the table.",
    "Bring your integration questions to the platform team — the session covers the contract surfaces and the audit path.",
  ],
  "approach_page": [
    "Test the method against your program: a briefing walks the gates and the evidence each one demands.",
    "The briefing is a working review of your current program against this method — gates, evidence and where yours would stop.",
    "Bring a live program to the table; we will map it to the gates and show what the evidence trail would have caught.",
  ],
  "contact_page": [
    "Use the named inboxes on this page — every message reaches a person, and the response lands within one business day.",
    "Pick the inbox that fits your question; the response comes from the practice, not a ticketing queue.",
  ],
  "platforms_hub": [
    "Book a platform briefing — the portfolio walked against your estate, with the evidence standards each platform carries.",
    "Talk to the platform group: one session covers the portfolio map and the two platforms that fit your estate.",
  ],
  "services_hub": [
    "Book an executive briefing — the tower map walked against your metric, and an honest read on where to start.",
    "The briefing maps your metric to the right tower and the first measurable move — 45 minutes, no deck.",
  ],
  "solutions_hub": [
    "Book a briefing with the solution practice — the patterns on this page mapped to the metric you own.",
    "Bring the metric; the session maps it to the solution patterns and the first measurable move.",
  ],
  "tower_hub": [
    "Book a briefing with the tower lead — 45 minutes: your metric, the tower's method, and the first measurable move.",
    "Talk to the tower practice: the briefing covers the services, the evidence standard and where programs like yours start.",
  ],
  "solution_page": [
    "Start with a value assessment — the pattern priced against your estate in two weeks, baseline signed or the answer is no.",
    "Book a briefing on this solution: the pattern, the prerequisites and the measured delta it targets in estates like yours.",
  ],
}

# ── note blocks (case studies) ───────────────────────────────────────────
NOTE_LINES = [
  "Client identity, baselines and raw figures stay under agreement; the method note and the measurement shape are shareable in a briefing.",
  "The engagement's evidence trail is available to your auditors under NDA — the same standard every Achala program carries.",
  "Figures on this page are the client's, reproduced with permission; the method note explaining how each was measured is shareable under NDA.",
  "Anonymity is contractual; the measurement discipline is not — the same gates and evidence standards apply on every engagement.",
]
