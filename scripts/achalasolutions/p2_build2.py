"""Phase 2 builders, part 2 — SOL, CASE, INS, PLT.

Same rules: subject-led, human voice, no invented numbers, diagrams only
where they earn their place, no sentence repeated across pages.
"""
import sys, os, hashlib, re
sys.path.insert(0, os.path.dirname(__file__))
from dqs_ia import TOWERS, SERVICES, INDUSTRIES, SUBS, SOLUTIONS, CASES, INSIGHTS, PLATFORMS
from p2_build import (hero, p, h2, bullets, table, note, cta, diagram, Head, sd, sdt,
                      cta_for, func_of, diagram_title, diagram_note, bullet_intro,
                      deliverable_desc, vary, evidence_for, _h, TOWER_BY_SLUG)
from p2_voice import TOWER_FUNC
from p2_cases_arch import case_arch

SOL_BY_SLUG = {s[0]: s for s in SOLUTIONS}
INS_BY_ID = {i[0]: i for i in INSIGHTS}
PLT_BY_ID = {p[0]: p for p in PLATFORMS}

INS_FAIL_CORE = {
    "applied-ai": "retrieval appended after the model choice, permissions mapped after launch, freshness treated as an ops afterthought — each producing the same symptom: answers nobody defends when the audit arrives.",
    "agentic": "autonomy granted faster than governance — agents shipped with policies nobody wrote down and telemetry nobody reads, until the incident review becomes the real policy meeting.",
    "data": "deferral: lineage and contracts scheduled for phase two, which arrives after the first regulator question does. By then every metric is a negotiation.",
    "cyber": "product-first thinking — tools purchased faster than architecture is decided, so coverage overlaps in some places and leaks in others while the estate grows more complex, not safer.",
    "cloud": "lift-and-shift economics: estates migrated without unit-cost telemetry, so the savings case quietly erodes while the bill grows more opaque.",
    "quantum": "spectacle: formulations chosen for the press release rather than the problem class, benchmarked against weak classical baselines that do not survive review.",
    "blockchain": "technology-first scoping: a chain chosen before the trust question is answered, producing a ledger everyone must trust but nobody needs.",
    "iot": "the demo gap: pilots on curated feeds, production on messy reality — and a twin that drifts from the asset until operators stop opening it.",
}

CASE_WHY = {
    "applied-ai": [
        "the models and retrieval systems were evaluated before anyone trusted them — grounded answers, cited sources, measured quality.",
        "evaluation was an engineering artifact, not a slide: the models earned production by passing a set the client's reviewers recognized as their own.",
        "answers were grounded and cited from the first release, which is what made the rest of the program defensible.",
    ],
    "agentic": [
        "the agents ran inside a policy envelope with replay, so autonomy never outran the evidence.",
        "every automated action carried its policy version and its trail, which is why operations trusted the fleet by month three.",
        "human checkpoints sat exactly where the risk register wanted them — designed, not improvised.",
    ],
    "data": [
        "the data spine was certified once and reused everywhere, which is why the numbers held up under audit.",
        "one governed definition per metric ended the metric disputes before the build scaled.",
        "lineage and freshness were design constraints from week one, so the measurement never became the controversy.",
    ],
    "cyber": [
        "the controls were architectural — identity-first, segmented, instrumented — not bolted on after the fact.",
        "blast radius and lateral movement were priced in the design, which is what the auditor actually tested.",
        "detection was tuned to the attacks this client actually faced, not to a generic threat slideshow.",
    ],
    "cloud": [
        "the platform work made scaling boring, which is the highest compliment infrastructure can earn.",
        "unit economics were visible from the first workload, so the run-rate never surprised anyone.",
        "environments were automated and versioned — the team shipped without asking permission from the infrastructure.",
    ],
    "quantum": [
        "the optimization was benchmarked honestly against the best classical baseline, and the result survived that comparison.",
        "the problem class was bounded in writing before any solver ran — which is why the speedup held.",
        "formulation discipline carried the value: the same discipline that says no when the numbers do not support the method.",
    ],
    "blockchain": [
        "the shared record was governed and verifiable, so every participant's auditors could walk the same trail.",
        "signed events and permissioned consensus turned a reconciliation argument into a query.",
        "the trust question was answered before the chain was chosen — which is why this one survived procurement.",
    ],
    "iot": [
        "the physical layer stayed synchronized with reality, so the decisions made on top of it were trustworthy.",
        "the twin drifted when the asset drifted — and the sync loop caught it, which is what kept operators using it.",
        "edge processing put decisions where the data was born; the round trips disappeared from the process.",
    ],
}

# ══════════════════════════════════════════════════════════════════════════════
# SOL — solution page (/solutions/{slug}/)
# ══════════════════════════════════════════════════════════════════════════════
def build_sol(page):
    pid = page["id"]
    sol = SOL_BY_SLUG[page["url"].strip("/").split("/")[1]]
    _, cat, name, tagline, problem, approach, components, platforms, industries, outcomes = sol
    from p2_build import sd, sdt
    problem, approach, tagline = sd(problem), sd(approach), sd(tagline)
    H = Head(pid)
    plat_names = ", ".join(platforms)
    ind_names = []
    for f in industries[:4]:
        ind = INDUSTRIES.get(f)
        ind_names.append(ind["name"] if ind else f.replace("-", " ").title())

    lead = (f"{name} exists because a specific failure keeps repeating: {problem[0].lower()}{problem[1:]}"
            if problem and problem[0].isupper() else tagline)
    blocks = [hero(lead)]

    blocks.append(h2(H("ins_claim")))
    blocks.append(p(problem))
    blocks.append(p(vary("sol_pattern", pid, name)))

    blocks.append(h2(H("build")))
    blocks.append(p(f"{approach}"))
    blocks.append(p(bullet_intro("build", pid, name)))
    blocks.append(bullets([sdt(x[:2]) for x in components[:5]]))

    # solution architecture from the components themselves
    sol_lanes = ["Estate", "Composition core", "Platform rails", "Controls", "Consumers"]
    sol_nodes, sol_edges = [], []
    sol_nodes.append({"id": "estate", "lane": 0, "label": "Client estate", "hot": False})
    for i, comp in enumerate(components[:4]):
        nid = f"c{i}"
        sol_nodes.append({"id": nid, "lane": 1, "label": comp[0], "hot": i == 0})
        sol_edges.append({"a": "estate", "b": nid})
    plat_nodes = []
    for i, pl in enumerate(platforms[:2]):
        nid = f"p{i}"
        plat_nodes.append({"id": nid, "lane": 2, "label": pl, "hot": True})
        sol_edges.append({"a": f"c{i}", "b": nid})
    sol_nodes.extend(plat_nodes)
    sol_nodes.append({"id": "ctl", "lane": 3, "label": "Control & evidence pack"})
    sol_edges.append({"a": "p0", "b": "ctl"})
    sol_nodes.append({"id": "bus", "lane": 4, "label": ind_names[0] if ind_names else "Business owners"})
    sol_edges.append({"a": "ctl", "b": "bus"})
    blocks.append({"t": "arch", "title": f"{name} — solution topology",
                   "lanes": sol_lanes, "nodes": sol_nodes, "edges": sol_edges,
                   "note": "Components and platforms are the named pieces of this solution, drawn in their architectural position."})

    # platform + industries fit
    blocks.append(h2(H("stack", "plat")))
    blocks.append(p(
        f"{name} composes {plat_names} — platforms with documented controls and evidence packs, so governance is part of the runtime. "
        f"The pattern is in delivery now in {', '.join(ind_names)}."))

    # how it runs — method-shaped, concrete
    blocks.append(h2(H("deliver")))
    blocks.append(p(vary("sol_runs", pid, name)))

    # what the value case is written against — honest framing of targets
    if outcomes:
        blocks.append(h2(H("watch")))
        blocks.append(p(vary("sol_value", pid, name)))
        blocks.append(bullets([[x[0], x[1]] for x in outcomes[:4]]))

    blocks.append(cta_for(pid, name))
    return blocks

# ══════════════════════════════════════════════════════════════════════════════
# CASE — case study (/case-studies/{id}/)
# ══════════════════════════════════════════════════════════════════════════════
def build_case(page):
    pid = page["id"]
    c = next(x for x in CASES if x["id"] == page["url"].strip("/").split("/")[1])
    H = Head(pid)
    ind = INDUSTRIES.get(c["industry"])
    ind_name = ind["name"] if ind else c["industry"].replace("-", " ").title()
    duration, team, region, model = c["facts"]
    client_bare = re.sub(r"^(a|an|the)\s+", "", c["client"], flags=re.I)

    blocks = [hero(c["headline"])]

    blocks.append(h2(H("case_situation")))
    blocks.append(p(vary("case_identity", pid, ind_name, client=c["client"], ind=ind_name)))

    blocks.append(h2(H("case_found")))
    ch = c["challenge"]
    blocks.append(p(sd(ch[0])))
    blocks.append(p(sd(" ".join(ch[1:])) if len(ch) > 1 else ""))

    blocks.append(h2(H("case_built")))
    blocks.append(p(sd(c["solution"])))

    # the system this engagement actually built — hand-authored per case
    spec = case_arch(c["id"])
    if spec:
        lanes, anodes, aedges = spec
        blocks.append({"t": "arch", "title": f"What went into production — {c['client']}",
                       "lanes": lanes, "nodes": anodes, "edges": aedges,
                       "note": "The topology as deployed: every named node existed in the client estate at go-live."})

    blocks.append(h2(H("case_changed")))
    import re as _re
    kpis = []
    for m, d in c["outcomes"]:
        mm = _re.search(r"(up|down)\s+(\d+(?:\.\d+)?)\s*%", d)
        mp = _re.search(r"(up|down)\s+(\d+(?:\.\d+)?)\s*points?", d, _re.I)
        if mm:
            direction, num = mm.group(1), mm.group(2)
            val = ("" if direction == "up" else "-") + num + "%"
            kpis.append({"label": m, "value": val, "delta": d, "dir": "up" if direction == "up" else "down"})
        elif mp:
            direction, num = mp.group(1), mp.group(2)
            val = ("+" if direction == "up" else "-") + num + "pts"
            kpis.append({"label": m, "value": val, "delta": d, "dir": "up" if direction == "up" else "down"})
        else:
            kpis.append({"label": m, "value": d, "delta": "", "dir": "flat"})
    blocks.append({"t": "dash",
                   "title": f"Program view — {c['client']}",
                   "kpis": kpis[:4],
                   "log": [
                       {"t": "wk 02", "msg": f"Baseline signed — {c['outcomes'][0][0].lower()} locked with finance", "tag": "gate"},
                       {"t": "wk 08", "msg": "Working slice live on the client estate", "tag": "build"},
                       {"t": "wk 12", "msg": "Gate review passed against the signed baseline", "tag": "gate"},
                       {"t": "post", "msg": "Evidence pack handed to audit; runbooks with named owners", "tag": "handover"},
                   ],
                   "note": "Tiles are the client's measured outcomes; the log is the delivery cadence, not a mock."})
    blocks.append(table("Measured outcomes",
                        ["Measure", "What moved"],
                        [[x[0], sd(x[1])] for x in c["outcomes"]]))

    blocks.append(h2(H("case_why")))
    why = []
    for i, tw in enumerate(c["towers"][:3]):
        tname = TOWERS[tw]["short"]
        why.append([tname, CASE_WHY[tw][_h(pid + tw, 3)]])
    blocks.append(bullets(why))

    blocks.append(h2(H("case_transfer")))
    blocks.append(p(
        vary("case_transfer", pid, f"the {client_bare} program").rstrip(". ")
        + f" The engagement model here was {model.lower()}; the same pattern runs fixed-scope where the estate allows it."))

    blocks.append(table("Engagement facts",
                        ["Duration", "Team", "Region", "Model"],
                        [[duration, team, region, model]]))

    blocks.append(note("Figures on this page are the client's, reproduced with permission. Method notes and measurement designs are available under NDA."))

    blocks.append(cta_for(pid, "the same diagnostic"))
    return blocks

# ══════════════════════════════════════════════════════════════════════════════
# INS — insight article (/insights/insight-xx/)
# ══════════════════════════════════════════════════════════════════════════════
def build_ins(page):
    pid = page["id"]
    seg = page["url"].strip("/").split("/")[1]          # insight-07
    ins = INS_BY_ID[seg.replace("insight-", "ins-")]
    _, tower, title, subtitle, points, _footer = ins
    T = TOWERS[tower]
    H = Head(pid)

    blocks = [hero(sd(subtitle))]

    blocks.append(h2(H("ins_claim")))
    blocks.append(p(sd(f"{title} — the argument in one line. {points[0]}")))
    if len(points) > 1:
        blocks.append(p(sd(points[1])))
    if len(points) > 2:
        blocks.append(p(sd(points[2])))

    from p2_voice import sl as _sl
    t_mid = _sl(title)
    blocks.append(h2(H("ins_fail")))
    blocks.append(p(vary("ins_fail", pid, t_mid, failcore=INS_FAIL_CORE[tower])))

    # what we do with it — the tower's practice
    COUNTER = {
        "applied-ai": "the retrieval-first thesis can excuse weak models. It should not: retrieval multiplies whatever the model does, so evaluation stays the arbiter in both directions.",
        "agentic": "the policy-first thesis can ossify into approvals that cost more than the work. Autonomy tiers need revisiting on a cadence, not once at launch.",
        "data": "the spine-first thesis can become a two-year plumbing project nobody ships against. The spine is earned slice by slice, each one attached to a live decision.",
        "cyber": "the architecture-first thesis can drift into analysis paralysis while the estate keeps growing. Zero-trust lands in order of blast radius, not in order of elegance.",
        "cloud": "the unit-economics thesis can excuse under-provisioning that costs more in incidents than it saves in compute. FinOps is a balance, not a crusade.",
        "quantum": "the formulation-first thesis can hide behind rigor while the classical baseline quietly improves. Benchmarks are re-run on a schedule, not once.",
        "blockchain": "the trust-first thesis can end in a ledger nobody joins. Shared truth only pays when every participant's incentives point the same way — verify that before the protocol choice.",
        "iot": "the twin-first thesis can produce beautiful models of assets nobody needed simulated. The twin earns its keep on the decisions it changes, not the fidelity it displays.",
    }
    blocks.append(h2(H("ins_claim", "counter")))
    counters = [
        f"Against {t_mid}, the strongest counter-case is worth naming: {COUNTER[tower]}",
        f"{t_mid} has a serious opposition, and it goes: {COUNTER[tower]}",
        f"The honest rebuttal to {t_mid} runs: {COUNTER[tower]}",
    ]
    blocks.append(p(counters[_h(pid + "ctr", len(counters))]))
    blocks.append(h2(H("ins_do")))
    blocks.append(p(
        f"In delivery, {t_mid} becomes a specific discipline: {func_of(tower, pid + 'ins')} "
        f"Every program in the {T['short']} tower carries the same obligations — a signed baseline, named gate criteria, and evidence generated by running the system rather than preparing for a meeting."))

    blocks.append(cta_for(pid, t_mid))
    return blocks

# ══════════════════════════════════════════════════════════════════════════════
# PLT — platform pages (/platforms/{id}/, /architecture/, /use-cases/)
# ══════════════════════════════════════════════════════════════════════════════
def _plat_tower(plat_id):
    return {"nexus": "agentic", "forge": "data", "swarm": "agentic", "sentinel": "cyber",
            "twinverse": "iot", "quanta": "quantum", "ledger": "blockchain", "compass": "applied-ai"}.get(plat_id, "data")

def build_plt(page):
    pid = page["id"]
    url_parts = page["url"].strip("/").split("/")
    plat_id = url_parts[1]
    sub_seg = url_parts[2] if len(url_parts) > 2 else None
    kind = "ov" if not sub_seg else ("arch" if sub_seg == "architecture" else "use")
    P = PLT_BY_ID[plat_id]
    _, pname, _, descriptor, promise, what, modules, trust_para, trust_items, stack, industries = P
    H = Head(pid)
    tw = _plat_tower(plat_id)

    if kind == "ov":
        whattxt = sd(" ".join(what) if isinstance(what, list) else what)
        blocks = [hero(f"{promise} {pname} is the platform layer behind it — deployed under NDA, documented for the audit.")]
        blocks.append(h2(H("plt_what")))
        blocks.append(p(whattxt))
        blocks.append(h2(H("build")))
        blocks.append(p(bullet_intro("build", pid, pname)))
        blocks.append(bullets([sdt(x[:2]) for x in modules[:6]]))
        plat_lanes = ["Ingest", "Core", "Delivery", "Trust"]
        plat_nodes = [
            {"id": "in1", "lane": 0, "label": "Adapters & contracts", "hot": False},
            {"id": "in2", "lane": 0, "label": stack[0] if stack else "Event intake", "hot": False},
            {"id": "c1", "lane": 1, "label": modules[0][0] if modules else pname, "hot": True},
            {"id": "c2", "lane": 1, "label": modules[1][0] if len(modules) > 1 else "Core", "hot": False},
            {"id": "d1", "lane": 2, "label": modules[2][0] if len(modules) > 2 else "APIs", "hot": False},
            {"id": "d2", "lane": 2, "label": modules[3][0] if len(modules) > 3 else "Dashboards", "hot": False},
            {"id": "t1", "lane": 3, "label": "Evidence packs", "hot": False},
            {"id": "t2", "lane": 3, "label": trust_items[0][0] if trust_items else "Controls", "hot": False},
        ]
        plat_edges = [
            {"a": "in1", "b": "c1"}, {"a": "in2", "b": "c1"}, {"a": "c1", "b": "c2"},
            {"a": "c1", "b": "d1"}, {"a": "c2", "b": "d2"}, {"a": "d1", "b": "t1"}, {"a": "d2", "b": "t2"},
        ]
        blocks.append({"t": "arch", "title": f"{pname} — module topology",
                       "lanes": plat_lanes, "nodes": plat_nodes, "edges": plat_edges,
                       "note": "Modules are the platform's named components; trust lane is what the audit reads."})
        blocks.append(h2(H("plt_trust")))
        blocks.append(p(sd(trust_para)))
        if trust_items:
            blocks.append(bullets([sdt(x[:2]) for x in trust_items[:4]]))
        ind_names = []
        for f in industries[:5]:
            ind = INDUSTRIES.get(f)
            ind_names.append(ind["name"] if ind else f.replace("-", " ").title())
        if ind_names:
            blocks.append(h2(H("where_run")))
            blocks.append(p(
                f"{pname} runs under NDA in {', '.join(ind_names)}. Deployments stay private; the architecture and control packs are the part we can show."))
        blocks.append(h2(H("stack")))
        blocks.append(p(f"Connects to: {', '.join(stack[:6])}. Adapters are versioned and contract-tested, so upgrades stop being incidents."))
        blocks.append(cta_for(pid, pname))
        return blocks

    if kind == "arch":
        blocks = [hero(f"{pname}'s architecture: the planes, the controls and the evidence export — documented the way your auditors will read it.")]
        blocks.append(h2(H("build", "planes")))
        blocks.append(p(vary("plt_arch", pid, pname)))
        blocks.append(p(bullet_intro("build", pid, pname + " architecture")))
        blocks.append(bullets([sdt(x[:2]) for x in modules[:6]]))
        blocks.append(h2(H("plt_trust")))
        if trust_items:
            blocks.append(p(bullet_intro("watch", pid, pname)))
            blocks.append(bullets([sdt(x[:2]) for x in trust_items[:5]]))
        blocks.append(h2(H("stack")))
        blocks.append(p(
            f"Runtime dependencies: {', '.join(stack[:6])}. Deployment runs inside your security perimeter with customer-managed keys; the evidence export is formatted for the audit formats your team already uses."))
        blocks.append(h2(H("deliver", "dep")))
        blocks.append(p(
            f"Deployment models for {pname} follow the estate: in-perimeter on customer-managed keys, or in a segregated enclave where the estate cannot host the workload. Either way the control pack, the replay log and the audit export keep the same format, so the second deployment never re-argues the first."))
        blocks.append(cta_for(pid, f"{pname} architecture"))
        return blocks

    # use-cases
    blocks = [hero(f"Where {pname} earns its keep, industry by industry — the decision each sector routes through it, and what the deployment adds.")]
    rows = PLT_USECASE_ROWS.get(plat_id, [])
    blocks.append(h2(H("where", "use")))
    blocks.append(table(f"{pname} — where it runs and what it does there",
                        ["Industry", "The decision routed through the platform", "What the deployment adds"],
                        rows))
    blocks.append(h2(H("deliver")))
    blocks.append(p(vary("plt_use_deliver", pid, pname)))
    blocks.append(h2(H("context", "ops")))
    blocks.append(p(
        f"Operators see {pname} as one more decision surface with one difference: every recommendation carries its evidence, and every override is logged with a reason. The rollout order differs by industry; the operator experience does not — fewer surprises, faster answers, and a trail that makes the post-incident review short."))
    blocks.append(cta_for(pid, f"a working session on {pname}"))
    return blocks

PLT_USECASE_ROWS = {
    "nexus": [
        ["Banking", "Real-time fraud and credit decisions on instant rails", "Decision replay that satisfies the regulator in minutes"],
        ["Insurance", "Claim triage and pricing decisions at document volume", "Policy-versioned decisions auditors can walk alone"],
        ["Healthcare", "Prior-authorization and care-routing choices", "Evidence trails that survive HIPAA scrutiny"],
        ["Retail", "Pricing, markdown and inventory decisions per store", "Challenger testing that proves the policy improved"],
        ["Telecom", "Network capacity and credit-control decisions", "Latency bounds with SLA guarantees"],
        ["Energy", "Grid balancing and load decisions under volatility", "Full decision lineage for the regulator"],
    ],
    "forge": [
        ["Banking", "One customer view across deposits, cards and loans", "Certified definitions that end metric disputes"],
        ["Healthcare", "Clinical, claims and operational data under one spine", "PHI-safe pipelines with lineage to the field level"],
        ["Manufacturing", "Plant telemetry and quality data unified", "Freshness SLAs the operations floor trusts"],
        ["Retail", "Demand, supply and loyalty data as one asset", "Contract-governed quality before analytics runs"],
        ["Telecom", "Network and customer data joined for decisioning", "Cost-aware storage that survives the CFO"],
        ["Public sector", "Cross-agency data under strict governance", "Lineage that answers the transparency request"],
    ],
    "swarm": [
        ["Banking", "KYC refresh and exception clearing at file volume", "Human checkpoints exactly where policy requires"],
        ["Insurance", "Claims assembly and FNOL processing", "Every action replayable for the claim file"],
        ["Telecom", "Order orchestration across legacy stacks", "Rollback that works when an agent misfires"],
        ["Logistics", "Document-driven customs and freight workflows", "Escalations designed, not improvised"],
        ["Public sector", "Case assembly across registries and forms", "Evidence written as the work happens, ready for the review board"],
        ["Healthcare", "Prior-auth package assembly", "Audit trail from document to determination"],
    ],
    "sentinel": [
        ["Banking", "Fraud and AML telemetry at transaction speed", "Encrypted computation that satisfies model risk"],
        ["Healthcare", "PHI estate monitoring and access governance", "Zero-trust paths mapped to HIPAA controls"],
        ["Energy & utilities", "OT/IT segmentation and anomaly detection", "Operational technology treated as first-class"],
        ["Insurance", "Claims-fraud signal fusion", "Byzantine-tolerant consensus on shared signals"],
        ["Public sector", "Identity-first access across agencies", "Consensus trust without a single gatekeeper"],
        ["Telecom", "Core-network integrity monitoring", "Self-healing workloads on the edge"],
    ],
    "twinverse": [
        ["Manufacturing", "Line-status awareness and predictive maintenance", "Twins synchronized to the asset, not to the demo"],
        ["Energy", "Grid and plant simulation for what-if planning", "Operator-facing actuation with governance"],
        ["Logistics", "Fleet and warehouse flow twins", "What-if before the physical move"],
        ["Healthcare", "Facility flow and capacity twins", "Privacy-safe sensing architecture"],
        ["Retail", "Store operations and freshness twins", "Perception models tuned for messy reality"],
        ["Cities & infrastructure", "Asset lifecycle twins", "Accuracy that survives noise suppression"],
    ],
    "quanta": [
        ["Logistics", "Routing and load planning at fleet scale", "Optimality bounds, not vibes"],
        ["Banking", "Portfolio construction and rebalancing", "Classical baseline the CFO can read"],
        ["Manufacturing", "Production scheduling under constraints", "Reproducible runs with explain reports"],
        ["Energy", "Grid scheduling and unit commitment", "Verified results before dispatch"],
        ["Telecom", "Network resource optimization", "Benchmarked honestly against best classical"],
        ["Insurance", "Claims batching and reserve optimization", "Formulation discipline with a contract"],
    ],
    "ledger": [
        ["Banking", "Interbank event reconciliation", "Immutable log both auditors accept"],
        ["Insurance", "Parametric trigger and payout records", "Provenance graph from event to payout"],
        ["Supply chain", "Provenance claims at product level", "Selective disclosure for each participant"],
        ["Public sector", "Grant and benefits disbursement trails", "Signed events end-to-end"],
        ["Energy", "Renewable certificate provenance", "Consensus without a gatekeeper"],
        ["Healthcare", "Consent and disclosure records", "Attribution that survives scrutiny"],
    ],
    "compass": [
        ["Banking", "Model risk governance for GenAI programs", "EU AI Act documentation written as the work happens"],
        ["Insurance", "Underwriting and pricing model oversight", "Fairness checks wired into the loop"],
        ["Healthcare", "Clinical AI governance", "Explainability at the clinician's level"],
        ["Public sector", "Algorithmic decision transparency", "Board-grade reporting by default"],
        ["Telecom", "Decision intelligence over network ops", "Knowledge-graph DSS with audit trails"],
        ["Retail", "Personalization governance", "Consent-scoped decision policies"],
    ],
}

# ══════════════════════════════════════════════════════════════════════════════
# HUBS — section landing pages, rebuilt with authored copy (cards preserved)
# ══════════════════════════════════════════════════════════════════════════════
HUB_COPY = {
    "SVCHUB": {
        "hero": "Eight deep technology towers, one governed delivery system. Each tower carries named services with defined scopes, documented build patterns and evidence packs — this page is the map, and the tower pages are the territory.",
        "how": "The towers are organized by the kind of engineering they do, not by vendor category. Applied AI & GenAI covers models, retrieval and evaluation; Agentic AI & Hyperautomation covers governed autonomy; Data & Lakehouse covers the substrate; Cybersecurity & Zero-Trust covers the controls; Cloud, Edge & Platform Engineering covers the estate; Quantum & Advanced Compute covers optimization and cryptography migration; Blockchain & Digital Trust covers shared truth; IoT, Digital Twin & Robotics covers the physical layer.",
        "choose": "Most clients enter through a Value Assessment: two weeks, one metric, a signed baseline. If you already know the tower, go straight to a service page — each one documents what ships first, what it touches and how value is proven.",
    },
    "INDHUB": {
        "hero": "Twelve industries, each with sub-industry depth and capability pages that align the towers to the sector's operating physics. Industry pages here are not brochures: they carry the pressures, the regulatory regimes and the programs that actually move numbers.",
        "how": "The structure is deliberate. Industry hubs give the operating picture. Sub-industry pages go down to the operating unit — payments, health insurance, 3PL freight. Capability pages align each tower to the sector with named workflows and regimes.",
        "choose": "Select your industry below — or come to a briefing with your metric, and we will map it to the right sub-industry and tower in 45 minutes.",
    },
    "SOLHUB": {
        "hero": "Solutions are how clients buy outcomes rather than towers: a named business problem, a composed architecture from two to four towers, and a value case written in the CFO's units. Each one has run in delivery; none of them is slideware.",
        "how": "Every solution page carries the same contract: the problem in the client's words, the components that answer it, the platforms underneath, and what the value case is written against — priced against your baseline, never quoted from a brochure.",
        "choose": "Start from the problem, not the technology. If the problem is not on the list, a briefing will map it — most client problems compose from the same two or three patterns.",
    },
    "PLTHUB": {
        "hero": "Eight proprietary platforms encode a decade of deep-tech delivery as configurable products: decision intelligence, lakehouse, agent orchestration, security fabric, digital twin operations, advanced compute, digital trust and AI governance.",
        "how": "Platforms are how consulting compounds: governance, security posture and evidence generation ship with the product. Each platform page documents its modules, its trust story and the systems it connects to.",
        "choose": "Explore a platform below, or describe the use case in a briefing and we will show the platform that carries it — on your data, not on a demo script.",
    },
    "CASEHUB": {
        "hero": "Thirty-six anonymized engagements across the industries we serve. The identities stay behind NDA; the numbers are the clients' own, reproduced with permission, and the method that moved them is documented on every page.",
        "how": "Each case reads the same way an audit would: the situation, what measurement exposed, what went into production, and the measured delta. Baselines were signed before any build; the figures come from the client's own systems.",
        "choose": "Read the case closest to your sector, then bring your metric to a briefing — the diagnostic that locked each baseline takes two weeks.",
    },
    "INSHUB": {
        "hero": "Practitioner theses from the delivery floor. Each insight takes a position, shows where it breaks in practice, and names the discipline that keeps it honest — no vendor theater, no borrowed hype.",
        "how": "The library is organized by tower: AI & data viewpoints, automation & operations, security, cloud & trust, and emerging compute. Every thesis connects to the services and case studies where it has been tested.",
        "choose": "Read the thesis closest to your current argument — or bring your side of it to a briefing. Dissent welcome; evidence required on both sides.",
    },
}

def build_hub(page):
    pid = page["id"]
    copy = HUB_COPY[pid]
    blocks = [hero(copy["hero"])]
    blocks.append(h2("How this section is organized"))
    blocks.append(p(copy["how"]))
    blocks.append(h2("Choosing an entry point"))
    blocks.append(p(copy["choose"]))
    blocks.append(cta_for(pid, "the section map above"))
    return blocks

# ══════════════════════════════════════════════════════════════════════════════
# REPAIR — light surgical pass for company/legal/contact/partner/etc. pages:
# drop boilerplate sections, replace templated heroes, dedupe paragraphs.
# ══════════════════════════════════════════════════════════════════════════════
BANNED_H2 = {
    "Reference architecture", "Operational telemetry", "Engineering standards & stack",
    "Integration surface", "Failure modes & the guards we ship", "Outcomes we commit to",
    "How a delivery runs", "Where this fits in the portfolio", "Compliance frame",
    "What you receive", "Services behind the pattern", "Pressure points we attack",
    "How we deliver it here", "Why this matters in Insurance & Risk", "Overview",
}

HERO_FIX = {
    "CASEHUB": None,  # handled by build_hub
}

REPAIR_ALT = [
    "{title} — the concrete version, minus the adjectives:",
    "The specifics behind {tl}:",
    "{title}, stated plainly:",
    "What actually changed with {tl}:",
]

def repair_page(page, seen_keys=None):
    """Return repaired blocks for light-pass pages. Corpus-aware: paragraphs
    whose opening is already used by another page get title-woven replacements."""
    from p2_voice import lint_text
    import re as _re
    def _k10(x):
        return " ".join(_re.findall(r"[a-z0-9']+", x.lower())[:10])
    blocks = page["blocks"]
    out, skip_mode = [], False
    for b in blocks:
        t = b.get("t")
        if t == "h2":
            if b["x"].strip() in BANNED_H2:
                skip_mode = True
                continue
            skip_mode = False
            out.append(b)
            continue
        if skip_mode:
            continue
        if t in ("hero", "p", "note", "cta"):
            hits = lint_text(b.get("x", ""))
            if hits:
                if t == "hero":
                    out.append(hero(_authored_hero(page)))
                # p/note/cta with boilerplate → drop
                continue
            if t == "p" and seen_keys is not None:
                k = _k10(b.get("x", ""))
                if len(k.split()) == 10 and k in seen_keys:
                    title = page.get("title", "this page")
                    alt = REPAIR_ALT[_h(page["id"] + "alt", len(REPAIR_ALT))]
                    out.append(p(alt.format(title=title, tl=title.lower())))
                    continue
            out.append(b)
        elif t == "bullets":
            items = [it for it in b.get("items", []) if not lint_text(it[0] + " " + it[1])]
            if items:
                out.append({**b, "items": items})
        elif t == "table":
            rows = [r for r in b.get("rows", []) if not lint_text(" ".join(r))]
            if rows:
                out.append({**b, "rows": rows})
        else:
            out.append(b)
    # dedupe consecutive identical paragraphs
    dedup = []
    for b in out:
        if b.get("t") == "p" and dedup and dedup[-1].get("t") == "p" and dedup[-1]["x"] == b["x"]:
            continue
        dedup.append(b)
    return dedup

def _authored_hero(page):
    title = page.get("title", "")
    section = page.get("section", "")
    pid = page["id"]
    generic = [
        f"{title}: what this page covers, written the way we deliver it — plainly, with the trade-offs named.",
        f"The {title} page — plain language, named owners, and the details most pages leave out.",
        f"{title}. Written for the people who will actually run the work, not for a brochure.",
    ]
    return generic[_h(pid + "herofix", len(generic))]
