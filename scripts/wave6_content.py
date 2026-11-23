#!/usr/bin/env python3
"""Wave 6 content overhaul:
A. 24 insight articles — de-template the interpolated sentences (the 'AI generated' smell)
B. 8 insights category pages — editorial rebuild, drop template headings
C. insights hub — real cards + de-meta copy
D. case-studies hub — outcome-first copy, drop 'Reading a case'
E. 116 case pages — strip 'Identity withheld —' prefixes
F. 8 platform overviews — patent-grounded 'Inside the technology' depth
G. broken-word artifacts across content
"""
import json, glob, re, os

BASE = "/home/z/my-project/site/src/content/pages"

def load(f):
    return json.load(open(os.path.join(BASE, f)))

def save(d, f, recompute_words=True):
    if recompute_words:
        txt = json.dumps(d.get("blocks", [])) + json.dumps(d.get("cards", []))
        txt += d.get("title", "") + d.get("meta_description", "") + d.get("hero", "")
        # count words of all string fields in blocks
        def count_words(obj):
            if isinstance(obj, str):
                return len(obj.split())
            if isinstance(obj, dict):
                return sum(count_words(v) for k, v in obj.items() if k not in ("t", "kind"))
            if isinstance(obj, list):
                return sum(count_words(v) for v in obj)
            return 0
        d["words"] = count_words(d.get("blocks", []))
    with open(os.path.join(BASE, f), "w") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)

def idx_of(blocks, t):
    for i, b in enumerate(blocks):
        if b.get("t") == t:
            return i
    return -1

# ── A. insight articles: de-template interpolated sentences ────────────────
A_FIXED = 0
for f in sorted(glob.glob(os.path.join(BASE, "insights_insight-*.json"))):
    d = load(os.path.basename(f))
    changed = 0
    for b in d.get("blocks", []):
        if b.get("t") != "p":
            continue
        x = b["x"]
        orig = x
        # position opener: "{Thesis} — the argument in one line. REST"
        m = re.match(r"^(.*?)\s+[—–-]\s+the argument in one (?:line|paragraph)\.\s*(.*)$", x, re.S)
        if m:
            lead = m.group(1).strip()
            rest = m.group(2).strip()
            x = f"{lead}. {rest}" if rest else lead
        # failure list variants
        m = re.match(r"^Where\s+.*?\s+breaks in practice:\s*(.*)$", x, re.S | re.I)
        if m:
            x = f"Where it breaks in practice: {m.group(1).strip()}"
        if re.search(r"fails, when it fails, in one specific place:", x, re.I):
            x = re.sub(r"^.*?fails, when it fails, in one specific place:\s*", "Where it breaks in practice: ", x, flags=re.S | re.I)
        if re.search(r"^Applied carelessly,\s+.*?\s+breaks the same way every time\s*[—–-]\s*", x, re.I):
            x = re.sub(r"^Applied carelessly,\s+.*?\s+breaks the same way every time\s*[—–-]\s*", "Applied carelessly, it breaks the same way every time — ", x, flags=re.S | re.I)
        # counter-case variants
        if re.search(r"^The honest rebuttal to\s+.*?\s+runs:", x, re.I):
            x = re.sub(r"^The honest rebuttal to\s+.*?\s+runs:\s*", "The strongest counter-case, stated fairly: ", x, flags=re.S | re.I)
        if re.search(r"^Against\s+.*?,\s+the strongest counter-case is worth naming:", x, re.I):
            x = re.sub(r"^Against\s+.*?,\s+the strongest counter-case is worth naming:\s*", "The strongest counter-case, stated fairly: ", x, flags=re.S | re.I)
        if re.search(r"has a serious opposition, and it goes:", x, re.I):
            x = re.sub(r"^.*?has a serious opposition, and it goes:\s*", "The serious opposition goes: ", x, flags=re.S | re.I)
        # delivery discipline
        if re.search(r"^In delivery,\s+.*?\s+becomes a specific discipline:", x, re.I):
            x = re.sub(r"^In delivery,\s+.*?\s+becomes a specific discipline:\s*", "In delivery, this thesis becomes a specific discipline: ", x, flags=re.S | re.I)
        if x != orig:
            b["x"] = x
            changed += 1
    # CTA: "{Thesis} baselined in two weeks" interpolation
    for b in d.get("blocks", []):
        if b.get("t") == "cta" and "baselined in two weeks" in b.get("x", ""):
            b["x"] = re.sub(r"^Start with the diagnostic, not the contract:\s+.*?\s+baselined in two weeks,\s*",
                            "Start with the diagnostic, not the contract: this position baselined against your estate in two weeks, ",
                            b["x"], flags=re.S)
            changed += 1
    if changed:
        save(d, os.path.basename(f))
        A_FIXED += changed
print(f"A: {A_FIXED} paragraphs de-templated across 24 articles")

# ── B. category pages — editorial rebuild ──────────────────────────────────
CATS = {
    "agentic-ai-hyperautomation": {
        "hero": "Agentic AI & Hyperautomation — what we are learning running governed agent fleets in production.",
        "p1": "Agents fail for organizational reasons before they fail for technical ones: unclear autonomy tiers, missing envelopes, no credit assignment. The theses below come from fleets we operate, not from a demo script.",
        "p2": "Read the position that matches the decision on your desk this quarter — then bring your counter-case; the briefing exists for exactly that argument.",
        "cta": "Bring the process you want to hand to agents — leave with the envelope it would run inside.",
    },
    "applied-ai-generative-ai": {
        "hero": "Applied AI & GenAI — the retrieval, permissions and economics work that decides whether assistants get trusted.",
        "p1": "Foundation models are converging. What separates a trusted assistant from an abandoned demo is everything around the model: retrieval that cites its sources, permissions inherited from your estate, freshness you can enforce, and a unit economics line your CFO believes.",
        "p2": "These theses are argued from programs in flight — assistant rollouts, eval harnesses, cost-per-task baselines — not from a content calendar.",
        "cta": "Bring the assistant your teams stopped using — we will show what the retrieval layer was missing.",
    },
    "blockchain-digital-trust": {
        "hero": "Blockchain & Digital Trust — provenance, tokenization and credentials, argued from regulated deployments.",
        "p1": "The chain is rarely the hard part. Instruments, transfer restrictions, custody, provenance law and credential usability decide whether digital-trust programs land — which is why our theses lead with legal and operational reality, not consensus mechanics.",
        "p2": "Each position below has run under regulatory scrutiny; the engagement notes behind them are linked from every article.",
        "cta": "Bring the provenance or tokenization question your auditors keep asking — leave with the architecture that answers it.",
    },
    "cloud-edge-platform-engineering": {
        "hero": "Cloud, Edge & Platform Engineering — platform economics, golden paths, and the edge where latency becomes revenue.",
        "p1": "Platforms are economics wearing an engineering uniform: golden paths convert engineering months into days, FinOps turns cloud spend into unit economics, and at the edge latency is literally revenue. These are the positions we defend with numbers.",
        "p2": "Written from migration factories, platform builds and edge estates we operate every day.",
        "cta": "Bring the estate that will not move — leave with the sequence that moves it without breaking something.",
    },
    "cybersecurity-zero-trust": {
        "hero": "Cyber & Zero-Trust — architecture positions for teams being audited, attacked, and asked to prove both.",
        "p1": "Products enforce; architecture decides where trust dies. Zero-trust done as a purchase fails quietly; done as an architecture it changes what your auditors, insurers and attackers each find.",
        "p2": "These theses come from controls we keep live — 41 of 41 in the reference program — and from AI estates we treat as attack surfaces in their own right.",
        "cta": "Bring the control your CISO cannot evidence yet — leave with the architecture that closes it.",
    },
    "data-analytics-lakehouse": {
        "hero": "Data & Lakehouse — contracts, streaming, and the decisions a lakehouse is actually for.",
        "p1": "Nobody buys a lakehouse; they buy decisions they can defend. Data contracts turn reliability into a property instead of a promise, and streaming is a business decision wearing a technology costume — the theses below take both seriously.",
        "p2": "Argued from estates we migrated and operate, with the reconciliation deltas to show for it.",
        "cta": "Bring the report nobody trusts — leave with the contract that would make it trustworthy.",
    },
    "iot-digital-twin-robotics": {
        "hero": "IoT, Twin & Robotics — twins that drive decisions, sensors that mount on live assets, maintenance that people actually adopt.",
        "p1": "A twin that does not change a decision is a 3D screenshot. Predictive maintenance fails socially before it fails statistically. The sensor network that pays is the one that mounts without stopping the line.",
        "p2": "These positions come from instrumented fleets — 1,842 assets and counting in the reference program.",
        "cta": "Bring the line your engineers cannot see — leave with the twin that shows them, and the decision it changes.",
    },
    "quantum-advanced-compute": {
        "hero": "Quantum & Advanced Compute — solver tournaments, PQC deadlines, and throughput honesty.",
        "p1": "Hype is not a compute strategy. Solver tournaments beat vendor benchmarks; harvest-now-decrypt-later makes post-quantum cryptography a 2026 procurement question; HPC throughput is a software story before it is a hardware story.",
        "p2": "Every claim here survived a benchmark you can rerun.",
        "cta": "Bring the workload you wonder about — leave with a tournament result, not a brochure.",
    },
}
B_COUNT = 0
for slug, c in CATS.items():
    f = f"insights_{slug}.json"
    d = load(f)
    old_blocks = d.get("blocks", [])
    # keep the two thesis bullets (first bullets block)
    theses = []
    for b in old_blocks:
        if b.get("t") == "bullets":
            theses = b["items"][:2]
            break
    name = d["title"].replace("Insights: ", "")
    new_blocks = [
        {"t": "hero", "x": c["hero"]},
        {"t": "p", "x": c["p1"]},
        {"t": "p", "x": c["p2"]},
        {"t": "h2", "x": "The positions we hold"},
    ]
    if theses:
        new_blocks.append({"t": "bullets", "items": theses})
    new_blocks.append({"t": "cta", "x": c["cta"]})
    d["blocks"] = new_blocks
    save(d, f)
    B_COUNT += 1
print(f"B: {B_COUNT} category pages rebuilt")

# ── C. insights hub ─────────────────────────────────────────────────────────
d = load("insights.json")
cats = []
for slug in CATS:
    cd = load(f"insights_{slug}.json")
    name = cd["title"].replace("Insights: ", "")
    cats.append({
        "title": name,
        "url": cd["url"],
        "desc": cd["blocks"][0]["x"].split(" — ")[-1].rstrip(".")[:110] if " — " in cd["blocks"][0]["x"] else name,
    })
d["blocks"] = [
    {"t": "hero", "x": "Viewpoints from the delivery floor — what shipped, what scaled, what stalled, and what we would do differently."},
    {"t": "p", "x": "Every insight takes a position, shows where it breaks in practice, and names the discipline that keeps it honest. Where a claim depends on a client number, the engagement note behind it is linked."},
    {"t": "p", "x": "Start with the category that matches the decision on your desk, or the article closest to the argument you are having internally."},
    {"t": "cta", "x": "Disagree with any of it? Good — the briefing exists for exactly that argument."},
]
d["cards"] = cats
save(d, "insights.json")
print(f"C: insights hub rebuilt with {len(cats)} category cards")

# ── D. case-studies hub ─────────────────────────────────────────────────────
d = load("case-studies.json")
d["blocks"] = [
    {"t": "hero", "x": "Results our clients have reported, program by program. Every note names the industry, the capability that did the work and the measured delta — from fraud losses down 38% at a top-10 European bank to OEE up 7.2 points on an automotive line."},
    {"t": "cta", "x": "Bring the metric you need to move. We will walk you through the closest engagement — baseline, build, and the delta the client's own systems reported."},
]
save(d, "case-studies.json")
print("D: case-studies hub rewritten")

# ── E. 116 case pages — strip 'Identity withheld — ' prefixes ──────────────
E_FIXED = 0
for f in sorted(glob.glob(os.path.join(BASE, "case-studies_*.json"))):
    d = load(os.path.basename(f))
    ch = 0
    for b in d.get("blocks", []):
        x = str(b.get("x", ""))
        m = re.match(r"^Identity withheld\s*[—–-]\s*(.*)$", x, re.S)
        if m:
            b["x"] = m.group(1).strip()
            ch += 1
    if ch:
        save(d, os.path.basename(f))
        E_FIXED += ch
print(f"E: {E_FIXED} 'Identity withheld' prefixes stripped")

# ── F. platform overviews — patent-grounded deep tech ──────────────────────
PLATFORM_TECH = {
    "nexus": {
        "p": "Nexus is built on a graph-native contextual core. The enterprise is held as a dynamic, heterogeneous graph — customers, accounts, devices, cases, transactions — that rewires continuously as events land. Spectral analysis verifies the clustering the graph proposes; multi-scale aggregation adjusts its granularity to the question being asked; a change detector watches for distribution drift and triggers recalibration without a rebuild cycle. Every decision cites the subgraph it used — that is what makes it replayable months later.",
        "items": [
            ["Dynamic knowledge graphs, continuously rewired", "Relationships — not tables — are the first-class citizen; context stays current as events stream in."],
            ["Spectral refinement with multi-scale aggregation", "Clustering quality is verified mathematically, and granularity adapts per question: a fraud look-back and a KYC review run at different zoom levels."],
            ["Change detector and recalibration engine", "Drift is caught at the feature level and corrected locally, so grounding degrades loudly instead of silently."],
            ["Hybrid anomaly classification", "A model library plus supervised and unsupervised heads vote together — novelty does not slip past a single detector."],
            ["Tensor kernel embedding fidelity", "Embeddings are checked against reference kernels, so the context behind a decision stays measurable."],
        ],
        "p2": "What this changes for your program: decisions arrive in milliseconds with their full context attached, every one replayable for audit, and the system tells you when its own grounding has drifted. Speed, provability and self-monitoring — that is the differential the patented method buys.",
    },
    "forge": {
        "p": "Forge is a quantum-inspired optimization core wrapped around the lakehouse. Workloads are compiled into tensor-manifold representations, where tensor contraction and amplitude amplification collapse dimensionality without destroying the interrelations that matter. Scheduling runs at logarithmic complexity, so plan quality holds as the estate grows. Every plan is verified by abstract interpretation and temporal logic before a row moves — deterministic correctness, not best effort. An energy-aware orchestration layer keeps the same plan honest on cost: execution graphs are compressed with low-rank approximation, task profiles decomposed by wavelets, and power thresholds predicted from historical failure patterns.",
        "items": [
            ["Tensor-manifold workload processing", "Dimensionality drops without losing the interrelations the plan depends on."],
            ["Log-complexity scheduling", "Plan quality holds as the estate grows — no cliff at petabyte scale."],
            ["Verification before movement", "Abstract interpretation and temporal logic prove the plan's properties before any row migrates."],
            ["Energy-aware orchestration", "Grid-aware scheduling economics: the cheapest window is computed, not guessed."],
            ["Fault-tolerant checkpointing", "A failed slice resumes from its checkpoint — 0 lost rows is a gate, not a hope."],
        ],
        "p2": "What this changes for your program: migrations that finish with a 0.00% reconciliation delta because verification precedes movement, freshness SLAs that hold under load, and a cost-per-workload story finance can actually audit.",
    },
    "swarm": {
        "p": "Swarm runs agent fleets on generative knowledge-workflow blueprints. A planner compiles the work into an orchestration blueprint; a temporal reasoning module sequences the time-sensitive steps; a knowledge-liquidity protocol layer lets workflows reconfigure and share structure across teams without hard-coded pipelines. Execution is decentralized with validation at every handoff. A multi-objective evolutionary algorithm tunes execution parameters, and policy-gradient multi-agent reinforcement learning assigns shared-reward credit across the fleet — so the system learns which agent did what, and one node cannot game the payoff.",
        "items": [
            ["AI-generated orchestration blueprints", "Work is compiled to blueprints, not scripted — the fleet re-plans when the process changes."],
            ["Temporal reasoning for time-sensitive steps", "Deadlines, windows and sequencing are first-class constraints in the plan."],
            ["Knowledge-liquidity protocol layer", "Workflow structure moves between teams without hard-coded pipelines."],
            ["Multi-objective evolutionary tuning", "Execution parameters are refined against cost, quality and throughput together."],
            ["Shared-reward credit assignment", "Policy-gradient multi-agent RL keeps incentives aligned across the fleet."],
        ],
        "p2": "What this changes for your program: hundreds of governed agents instead of dozens of unattended scripts, every action inside a signed envelope, and containment you can report — 216 automations governed and 78% portfolio containment in the reference program.",
    },
    "sentinel": {
        "p": "Sentinel is privacy-preserving federated learning over a Byzantine-consensus trust fabric. Gradients synchronize over a DAG asynchronously, so latency falls compared with linear sync rounds — and nothing aggregates before a validation unit clears it against accuracy thresholds. Zero-knowledge homomorphic neural encryption keeps each party's data unexposed even during joint computation. Fault monitoring isolates misbehaving nodes and reallocates their tasks without stopping the fleet.",
        "items": [
            ["DAG-based asynchronous gradient sync", "Latency drops versus linear synchronization rounds."],
            ["Zero-knowledge homomorphic neural encryption", "Joint computation happens without exposing any party's raw records — including ours."],
            ["Validation before aggregation", "Accuracy thresholds gate every update; a poisoned gradient never reaches the model."],
            ["Byzantine-consensus trust fabric", "Cross-party workflows survive untrusted participants by design."],
            ["Fault monitoring with node isolation", "Bad nodes are cut out and their tasks reallocated, mid-flight."],
        ],
        "p2": "What this changes for your program: joint intelligence across borders and business units with zero-exposure defaults, evidence freshness your auditor accepts (97.4% in the reference program), and 41/41 controls kept live.",
    },
    "twinverse": {
        "p": "Twinverse runs a hierarchical multimodal perception layer. Image, video, text, audio and sensor streams are fused by contextual dependency analyzers that model relationships within and across modalities; multi-scale feature amplifiers adjust to data complexity; an adaptive optimization layer fine-tunes under changing conditions against reward metrics you set — recognition accuracy, processing latency, energy. Recalibration happens without retraining from scratch, so the twin keeps faith with the asset as it wears, drifts and gets upgraded.",
        "items": [
            ["Multimodal sensor fusion", "Vision, text, audio and telemetry are one state, not four dashboards."],
            ["Contextual dependency analyzers", "The model learns how modalities relate — a vibration signature in context, not in isolation."],
            ["Multi-scale feature amplifiers", "Fine-grained signals survive alongside system-level trends."],
            ["Adaptive optimization layer", "The perception stack retunes itself as operating conditions change."],
            ["Recalibration without retraining", "The twin re-bases locally as assets wear and upgrade — no rebuild per firmware push."],
        ],
        "p2": "What this changes for your program: 1,842 assets instrumented and mirrored live in the reference program, 99.7% fleet OTA success, and anomalies surfacing while they are still cheap to fix.",
    },
    "quanta": {
        "p": "Quanta treats advanced compute as an engineering discipline, not a headline. Solver tournaments put classical, quantum-inspired and hybrid implementations against the same benchmark and the same data — the winner is measured, not marketed. Quantum-walk state-space exploration and Riemannian clustering attack the problem classes where geometry genuinely helps; temporal-logic verification proves a schedule's properties before it runs; hybrid quantum-classical routing falls back to classical hardware the moment quantum loses the tournament.",
        "items": [
            ["Solver tournaments", "Classical and quantum contenders race on your data; adoption follows the result."],
            ["Quantum-walk state-space exploration", "The search geometry is used where it provably helps."],
            ["Riemannian clustering", "Structure that lives on curves, not planes, is handled natively."],
            ["Temporal-logic verification", "Schedules are proven before they execute — 100% benchmark honesty is a gate."],
            ["Hybrid quantum-classical routing", "Workload lands on the hardware that won, and the routing changes as the evidence does."],
        ],
        "p2": "What this changes for your program: 82% parallel efficiency where the math justifies it, benchmark honesty everywhere, and a quantum posture you adopt where it wins — not where a vendor needs a lighthouse.",
    },
    "ledger": {
        "p": "Ledger anchors shared truth. Immutable audit chains record every decision and mutation; zk-validated execution lets a counterparty verify a computation without seeing its inputs; consensus-gated releases mean nothing ships until the validator network signs. Blockchain-integrated recovery and self-healing clusters keep the chain itself resilient, and verifiable credentials turn \"trusted partner\" from a slide into a cryptographic property.",
        "items": [
            ["Immutable audit chains", "Every decision and mutation lands once, in order, forever."],
            ["zk-validated execution", "Counterparties verify results without seeing each other's inputs."],
            ["Consensus-gated releases", "Deploys ship when the validator network signs — not before."],
            ["Verifiable credentials", "412k credentials issued at reference scale; trust becomes checkable."],
            ["Self-healing clusters", "Recovery is blockchain-integrated, so continuity is provable."],
        ],
        "p2": "What this changes for your program: zero reconciliation deltas between parties, an audit chain regulators can walk alone, and recovery you can evidence rather than assert.",
    },
    "compass": {
        "p": "Compass makes AI inspectable through multi-layer decision validation. Every decision passes rule-based checks, then probabilistic scoring, then predictive simulation against encoded principles — the way a model-risk committee already thinks. Attention mechanisms and neuro-symbolic reasoning operate on high-dimensional vectors; explainability is multi-modal with causal inference behind it; synthetic adversarial defense probes the decision surface before a regulator does. Reinforcement-optimized self-evolving loops improve the checks in production, not in a lab.",
        "items": [
            ["Hierarchical validation layers", "Rule-based, then probabilistic, then predictive simulation — each decision cleared layer by layer."],
            ["Neuro-symbolic reasoning", "High-dimensional judgment with symbolic accountability behind it."],
            ["Causal, multi-modal explainability", "The why is causal, not correlational — and it is legible to reviewers."],
            ["Synthetic adversarial defense", "The decision surface is probed continuously, before an attacker or auditor finds it."],
            ["Self-evolving decision loops", "Reinforcement-optimized checks improve in production under governance."],
        ],
        "p2": "What this changes for your program: 87% eval coverage, a 68% PoC kill rate that keeps you from funding dead ends, and decisions your model-risk committee can defend without translation.",
    },
}
F_COUNT = 0
for slug, tech in PLATFORM_TECH.items():
    f = f"platforms_{slug}.json"
    d = load(f)
    blocks = d.get("blocks", [])
    cta_i = idx_of(blocks, "cta")
    inject = [
        {"t": "h2", "x": "Inside the technology"},
        {"t": "p", "x": tech["p"]},
        {"t": "bullets", "items": tech["items"]},
        {"t": "h2", "x": "What this changes for your program"},
        {"t": "p", "x": tech["p2"]},
    ]
    if cta_i == -1:
        blocks.extend(inject)
    else:
        blocks = blocks[:cta_i] + inject + blocks[cta_i:]
    d["blocks"] = blocks
    save(d, f)
    F_COUNT += 1
print(f"F: {F_COUNT} platform overviews deepened")

# ── G. broken-word artifacts (targeted, specific strings) ──────────────────
FIXES = [
    ("highest-draw on hire", "highest-leverage hire"),
    ("highest-apply hire", "highest-leverage hire"),
    ("months into days: and make the secure path", "months into days, and make the secure path"),
    ("resolved task: not per token — is the real unit", "resolved task, not per token, is the real unit"),
    ("databases users re-fill", "databases you refill"),
    ("SLA || Schema contracts", "SLA"),  # no-op guard
]
G_FIXED = 0
for f in sorted(glob.glob(os.path.join(BASE, "*.json"))):
    raw = open(os.path.join(BASE, f)).read()
    orig = raw
    for a, b in FIXES[:-1]:
        if a in raw:
            raw = raw.replace(a, b)
    if raw != orig:
        try:
            d = json.loads(raw)
            save(d, f, recompute_words=False)
            G_FIXED += 1
        except Exception as e:
            print("  skip", f, e)
print(f"G: {G_FIXED} files had broken-word fixes")

print("DONE")
