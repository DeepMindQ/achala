# -*- coding: utf-8 -*-
"""Achala IT Solutions — Content composer: builds full page copy as structured blocks, exports volume JSONs."""

import sys, os, json, hashlib
sys.path.insert(0, os.path.dirname(__file__))

from dqs_ia import (PAGES, build_ia, TOWERS, SERVICES, INDUSTRIES, SUBS, PLATFORMS, SOLUTIONS,
                    SOLUTION_CATEGORIES, CASES, BRAND, ABOUT_PAGE, EDGE_PAGE, LEADERSHIP, VALUES_PAGE,
                    CAREERS_PAGE, NEWSROOM_PAGE, PARTNERS_PAGE, APPROACH_PAGES, CONTACT_PAGES, INSIGHTS,
                    TOWER_ORDER, IND_ORDER, VOL_NAMES)

OUT_DIR = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT_DIR, exist_ok=True)

_svc_by_id = {s["id"]: s for s in SERVICES}
_tower_services = {t: [s for s in SERVICES if s["tower"] == t] for t in TOWER_ORDER}
_ind_subs = {ind: [SUBS[k] for k in SUBS if SUBS[k]["industry"] == ind] for ind in IND_ORDER}
_PLATFORM_TOWER = {"nexus": "agentic", "forge": "data", "swarm": "agentic", "sentinel": "cyber",
                   "twinverse": "iot", "quanta": "quantum", "ledger": "blockchain", "compass": "applied-ai"}
_PLAT_BY_ID = {p[0]: p for p in PLATFORMS}
_SOLUTION_CAT_ORDER = ["growth", "risk", "ops", "people"]


def _h(key):
    return int(hashlib.md5(key.encode("utf-8")).hexdigest(), 16)


def _pick(key, items):
    return items[_h(key) % len(items)]


def B_p(text): return {"t": "p", "x": text}
def B_h2(text): return {"t": "h2", "x": text}
def B_h3(text): return {"t": "h3", "x": text}
def B_hero(text): return {"t": "hero", "x": text}
def B_bullets(items): return {"t": "bullets", "items": items}
def B_table(caption, headers, rows): return {"t": "table", "caption": caption, "headers": headers, "rows": rows}
def B_cta(text): return {"t": "cta", "x": text}
def B_note(text): return {"t": "note", "x": text}


# ------------------------------------------------------------------
# Builders per template
# ------------------------------------------------------------------

def build_home(page):
    blocks = [
        B_hero(BRAND["positioning"]),
        B_p("Achala IT Solutions operates where consulting hands off to engineering: eight proprietary platforms, four global "
            "delivery centers and a commercial model that can link fees to the metrics we commit to moving. Every "
            "engagement begins with falsifiable success criteria and ends with benchmarked evidence — including the "
            "documented 'no' when a program should stop."),
        B_h2("Eight deep-tech towers"),
        B_p("We do not sell generic application development. We sell the capability layers that decide whether an "
            "enterprise competes in the intelligence era:"),
        B_bullets([[TOWERS[t]["name"], TOWERS[t]["tagline"]] for t in TOWER_ORDER]),
        B_h2("Platforms, not just projects"),
        B_p("Our eight platforms encode a decade of delivery patterns as configurable products. Clients start at "
            "pattern 80% — with governance, security and evidence generation built in:"),
        B_bullets([[p[1], p[4]] for p in PLATFORMS]),
        B_h2("Industries we serve"),
        B_p("Twelve industries, each with sub-industry depth and capability pages aligned per sector. "
            "A few examples of how the alignment reads in practice:"),
        B_bullets([[INDUSTRIES[i]["name"], INDUSTRIES[i]["tagline"]] for i in ["banking", "healthcare", "manufacturing", "energy", "retail"]]),
        B_h2(BRAND["metrics_heading"]),
        B_table("The Achala Edge in numbers", ["Proof point", "What it means"],
                [[a, b] for a, b in BRAND["proof_bar"]]),
        B_h2("How we engage"),
        B_p("The Achala Method runs five phases with named gates — Diagnose, Design, Prove, Industrialize, Compound. "
            "No phase proceeds without its evidence: baselines signed by finance, control matrices approved by risk, "
            "value memos that survive capital committees."),
        B_bullets([["Diagnose", "Value Mapping Sprint scores the portfolio; baseline metrics locked with owners."],
                   ["Prove", "PoC with falsifiable criteria on your data — one in three ends with a documented stop, by design."],
                   ["Industrialize", "Staged rollouts on platform rails with SLOs and evidence generated in-flight."],
                   ["Compound", "Challenger programs and conformance monitoring; annual value audit against baseline."]]),
        B_h2("Credentials that survive diligence"),
        B_p("SOC 2 Type II, ISO 27001, ISO 9001, GDPR and CCPA aligned, HIPAA-ready delivery pods, PCI DSS assessment "
            "support, NIST AI RMF aligned and EU AI Act conformity tooling. Zero-exposure architecture by default: "
            "client data is never training material."),
        B_cta("Book an executive briefing — 45 minutes with a practice lead, your metric, and three reference engagements."),
    ]
    return blocks


def build_services_hub(page):
    blocks = [
        B_hero("Consulting and delivery across the deep-tech stack — eight towers, one governed delivery system."),
        B_p("Achala IT Solutions's services are organized into eight towers. Each tower carries named services with defined "
            "deliverables, committed outcome ranges and the platform rails they deploy on. Towers compose: a fraud "
            "program draws on Data & Lakehouse, Agentic AI and Cybersecurity simultaneously."),
        B_h2("The towers"),
        B_bullets([[TOWERS[t]["name"], TOWERS[t]["definition"][:220] + "..."] for t in TOWER_ORDER]),
        B_h2("Tower map"),
        B_table("Service towers at a glance", ["Tower", "Services", "Typical anchor industries"],
                [[TOWERS[t]["name"], str(len(_tower_services[t])),
                  ", ".join(sorted({i for s in _tower_services[t] for i in s["focus"][:3]}))[:120]]
                 for t in TOWER_ORDER]),
        B_h2("How engagements run"),
        B_p("Every service is delivered through the Achala Method — Diagnose, Design, Prove, Industrialize, Compound — "
            "with gates that finance and risk actually sign. Services arrive on platform rails where relevant, so "
            "production hardening (security, replay, monitoring, documentation) is inherited rather than rebuilt."),
        B_h2("Evidence and governance"),
        B_p("Every deliverable arrives with its control mapping: model cards, decision replay, DORA-grade third-party "
            "evidence, EU AI Act technical documentation — generated during delivery, never reconstructed for audit."),
        B_cta("Explore a tower, or book a Value Assessment to sequence the portfolio against your P&L."),
    ]
    return blocks


def build_tower_hub(page, tower_id):
    tw = TOWERS[tower_id]
    services = _tower_services[tower_id]
    inds = sorted({i for s in services for i in s["focus"]})
    kpis = []
    for s in services[:4]:
        kpis.append([s["kpis"][0][0], s["kpis"][0][1]])
    blocks = [
        B_hero(tw["tagline"]),
        B_h2("What this tower covers"),
        B_p(tw["definition"]),
        B_h2("Why this tower, why now"),
        B_p(tw["why_now"]),
        B_h2("Services in this tower"),
        B_bullets([[s["name"], s["promise"]] for s in services]),
        B_h2("Platforms behind the delivery"),
        B_p(" and ".join(tw["platforms"]) + " carry the production rails for this tower — governance, security posture "
            "and evidence generation are inherited from the platform, so programs harden instead of improvising."),
        B_h2("Outcomes we commit to"),
        B_bullets(kpis),
        B_h2("Where the tower applies"),
        B_p("Anchor industries: " + ", ".join(INDUSTRIES[i]["name"] for i in inds if i in INDUSTRIES) + "."),
        B_cta("Explore the services in this tower, or book a briefing with the tower practice lead."),
    ]
    return blocks


def build_service_page(page, svc):
    tw = TOWERS[svc["tower"]]
    blocks = [
        B_hero(svc["promise"]),
        B_h2("Overview"),
        B_p(svc["desc"][0]),
        B_h2("How we deliver"),
        B_p(svc["desc"][1]),
        B_h2("Capabilities"),
        B_bullets([[a, b] for a, b in svc["capabilities"]]),
        B_h2("Deliverables"),
        B_bullets([["Deliverable", d] for d in svc["deliverables"]]),
        B_h2("Technology and standards"),
        B_p("Typical stack and standards: " + ", ".join(svc["stack"]) + "."),
        B_h2("Outcomes we commit to"),
        B_bullets([[a, b] for a, b in svc["kpis"]]),
        B_h2("The first 90 days"),
        B_bullets([
            ["Weeks 1-4", _pick(svc["id"] + "-90a", [
                "baseline metrics locked with named owners; data-readiness assessed against the delivery contracts.",
                "stakeholder map and control ownership agreed; success criteria signed before the first build sprint."])],
            ["Weeks 5-8", _pick(svc["id"] + "-90b", [
                "first working increment on your data, evaluated against the signed criteria; production-path sketch reviewed with risk.",
                "reference architecture adapted to your estate; integration contracts tested against your systems."])],
            ["Weeks 9-13", _pick(svc["id"] + "-90c", [
                "staged rollout plan with SLO instrumentation; evidence pack draft reviewed with audit stakeholders.",
                "operational run model agreed; value memo drafted for the investment committee."])],
        ]),
        B_h2("Related services"),
        _rel_services(svc),
        B_h2("Where it applies"),
        B_p("Anchor industries: " + ", ".join(INDUSTRIES[i]["name"] for i in svc["focus"] if i in INDUSTRIES) +
            ". Platform rails: " + " and ".join(svc["platforms"]) + ". Related tower: " + tw["name"] + "."),
        B_cta("Discuss this service with the practice lead — or request a scoped value assessment for your estate."),
    ]
    return blocks


def _rel_services(svc):
    same = [s for s in SERVICES if s["tower"] == svc["tower"] and s["id"] != svc["id"]]
    start = _h(svc["id"] + "-rel") % max(len(same), 1)
    rel = [same[(start + i) % len(same)] for i in range(min(3, len(same)))]
    return B_bullets([[s["name"], s["promise"]] for s in rel])


def build_industries_hub(page):
    blocks = [
        B_hero("Twelve industries, sub-industry depth, and capability pages that align our towers to your sector's physics."),
        B_p("Industry pages at Achala IT Solutions are not brochures. Each one carries the sector's structural pressures, "
            "regulatory posture, priority programs and proof engagements — then aligns all eight capability towers "
            "at industry level and five priority towers at sub-industry level."),
        B_h2("The industries"),
        B_table("Industries and their focus", ["Industry", "Position", "Example committed outcome"],
                [[INDUSTRIES[i]["name"], INDUSTRIES[i]["tagline"][:95],
                  INDUSTRIES[i]["kpis"][0][0] + " — " + INDUSTRIES[i]["kpis"][0][1]] for i in IND_ORDER]),
        B_h2("How the architecture reads"),
        B_p("Industry hub (the sector's operating picture) → sub-industry pages (the operating units: payments, "
            "prior auth, cold chain, smart cities) → capability pages (a tower applied to the sector, e.g. "
            "Agentic AI for Banking or Computer Vision for Manufacturing). Every capability page carries sector-specific "
            "pressure points, use cases and committed outcomes — never generic service copy."),
        B_h2("Compliance posture by sector"),
        B_p("Regulatory context is first-class content: DORA and Basel in banking, HIPAA and FDA in health, IEC 62443 "
            "in manufacturing, NERC CIP in energy, EUDR in agriculture. Every industry page carries its regime table, "
            "and capability pages reference the obligations that shape delivery."),
        B_cta("Select your industry — or search capabilities directly from the mega menu."),
    ]
    return blocks


def build_industry_hub(page, ind_id):
    ind = INDUSTRIES[ind_id]
    cases = [c for c in CASES if c["industry"] == ind_id]
    blocks = [
        B_hero(ind["tagline"]),
        B_h2("Where the industry stands"),
        B_p(ind["intro"][0]),
        B_h2("The pressure is structural"),
        B_p(ind["intro"][1]),
        B_h2("How Achala IT Solutions responds"),
        B_p(ind["intro"][2]),
        B_h2("Pressure points we hear most"),
        B_bullets([[t, d] for (_, t, d) in [(None, p[1], p[2]) for p in ind["pressures"][:6]]]),
        B_h2("Regulatory posture"),
        B_table("Regimes that shape delivery", ["Regime", "What it means for programs"],
                [[r, i] for r, i in ind["regs"]]),
        B_h2("Priority programs"),
        B_bullets([[t, r] for t, r in ind["priorities"]]),
        B_h2("Proof from this industry"),
        B_bullets([[c["client"], c["headline"]] for c in cases]),
        B_h2("Capability pages for this industry"),
        B_p("All eight towers are aligned at industry level under /industries/" + INDUSTRIES[ind_id]["slug"] +
            "/capabilities/ — from Applied AI to Quantum. Five priority towers are aligned per sub-industry."),
        B_h2("Outcomes we commit to in this sector"),
        B_bullets([[k, v] for k, v in ind["kpis"]]),
        B_cta("Book an industry briefing, or go straight to a capability page from the mega menu."),
    ]
    return blocks


def build_subindustry_page(page, sub):
    ind = INDUSTRIES[sub["industry"]]
    blocks = [
        B_hero(sub["intro"]),
        B_h2("Operating context"),
        B_p("The workflows we industrialize here: " + ", ".join(sub["workflows"]) + ". Each arrives with its current "
            "cycle times measured in the Diagnose phase, and each leaves the program governed by outcome SLOs rather "
            "than anecdotes."),
        B_h2("Pressure points"),
        B_bullets([[t, d] for (_, t, d) in [(None, p[1], p[2]) for p in sub["pains"]]]),
        B_h2("Compliance frame"),
        B_table("Regimes in scope", ["Regime", "Implication"],
                [[r, i] for r, i in sub["regs"]]),
        B_h2("How we help — five priority capabilities"),
        B_bullets([[TOWERS[t]["short"], sub["usecases"][t][1] + " — " + sub["usecases"][t][2]] for t in sub["towers"]]),
        B_h2("Outcomes we commit to"),
        B_bullets([[k, v] for k, v in sub["kpis"]]),
        B_h2("How the engagement runs"),
        B_p(_pick(sub["slug"] + "-run", [
            "A typical program here starts with a two-week diagnostic that measures the workflows named above and locks the baseline, moves through a gated proof on your data, then industrializes on platform rails with the sector's compliance evidence generated in-flight.",
            "Engagements begin with the baseline measurement pack — cycle times, error rates, unit costs for the workflows above — because every committed outcome on this page is reported against that locked baseline, audited annually.",
            "We staff a named pod for this sub-industry pattern: delivery lead, quality owner and control owner, with the follow-the-sun rhythm covering build, run and the conformance monitoring that keeps the design honest after handover."])),
        B_h2("Proof from this industry"),
        B_bullets([[c["client"], c["headline"][:110]] for c in [c for c in CASES if c["industry"] == sub["industry"]][:2]]),
        B_h2("Adjacent units"),
        B_p("Related sub-industry pages: " + ", ".join(s2["name"] for s2 in _ind_subs[sub["industry"]] if s2["slug"] != sub["slug"]) +
            " — each with its own capability alignments under /industries/" + INDUSTRIES[sub["industry"]]["slug"] + "/."),
        B_cta("Start with a capability page — or book a briefing with the industry practice lead."),
    ]
    return blocks


def build_industry_capability(page, ind_id, tower_id):
    ind = INDUSTRIES[ind_id]
    tw = TOWERS[tower_id]
    pains = [p for p in ind["pressures"] if tower_id in p[0]]
    if len(pains) < 3:
        pains = pains + [p for p in ind["pressures"] if tower_id not in p[0]][:3 - len(pains)]
    pains = pains[:3]
    ucs = ind["usecases"].get(tower_id, [])
    svcs = _tower_services[tower_id]
    regs = _pick(f"{ind_id}-{tower_id}-r1", ind["regs"])
    blocks = [
        B_hero(f"How {tw['name']} rewires {ind['name']} — {ind['tagline'].rstrip('.').lower()}, engineered for audit."),
        B_h2("Why this capability matters here"),
        B_p("In " + ind["name"] + ", " + tw["definition"].split(". ")[0].lower() + ". That is the baseline pattern; "
            "the differentiator is what it connects to: " + ", ".join(s["name"].lower() for s in svcs[:3]) +
            " — delivered on " + " and ".join(tw["platforms"]) + " with the sector's regulatory posture built in."),
        B_h2("The pressure points we attack"),
        B_bullets([[t, d] for (_, t, d) in [(None, p[1], p[2]) for p in pains]]),
        B_h2("How we deliver it in this sector"),
        B_p("The delivery pattern composes " + str(len(svcs)) + " services from the " + tw["name"] + " tower — " +
            ", ".join(s["name"] for s in svcs[:4]) + " as the usual core — sequenced through the Achala Method with "
            "sector controls: " + regs[0] + " obligations shape the design from the first sprint."),
        B_h2("Services we deploy in this sector"),
        B_bullets([[s["name"], s["promise"]] for s in svcs[:4]]),
        B_h2("Proof patterns in this industry"),
        B_bullets([[u[0], u[1] + " (" + u[2] + ")"] for u in ucs]),
        B_h2("Outcomes we commit to"),
        B_bullets([[k, v] for k, v in _pick(f"{ind_id}-{tower_id}-k", ind["kpis"]) and [] or []]),
        B_cta("Explore the services behind this capability, or book a briefing with the industry practice lead."),
    ]
    # outcomes bullets (3 chosen deterministically)
    k_all = list(ind["kpis"])
    start = _h(f"{ind_id}-{tower_id}-k") % len(k_all)
    chosen = [k_all[(start + i) % len(k_all)] for i in range(3)]
    blocks[-3] = B_bullets([[k, v] for k, v in chosen])
    # regulatory note
    r2 = _pick(f"{ind_id}-{tower_id}-r2", ind["regs"])
    blocks.insert(-1, B_h2("Governance note"))
    blocks.insert(-1, B_p("Two regimes anchor the control design here: " + regs[0] + " and " + r2[0] + ". " + r2[1] +
                          ". Evidence for both is generated by the delivery itself — control tests, replay trails and "
                          "documentation are artifacts of the program, not a reconstruction project."))
    return blocks


def _scap_services(sub, tower_id, svcs):
    start = _h(f"{sub['slug']}-{tower_id}-p") % len(svcs)
    chosen = [svcs[(start + i) % len(svcs)] for i in range(3)]
    return B_bullets([[s["name"], s["promise"]] for s in chosen])


def build_sub_capability(page, sub, tower_id):
    ind = INDUSTRIES[sub["industry"]]
    tw = TOWERS[tower_id]
    pains = [p for p in sub["pains"] if tower_id in p[0]]
    if len(pains) < 2:
        pains = pains + [p for p in sub["pains"] if tower_id not in p[0]][:2 - len(pains)]
    pains = pains[:2]
    uc = sub["usecases"].get(tower_id)
    ind_ucs = ind["usecases"].get(tower_id, [])
    ind_uc = ind_ucs[_h(f"{sub['slug']}-{tower_id}") % len(ind_ucs)] if ind_ucs else None
    svcs = _tower_services[tower_id]
    core = [svcs[_h(f"{sub['slug']}-{tower_id}-s{i}") % len(svcs)]["name"] for i in range(3)]
    blocks = [
        B_hero(f"{tw['short']} for {sub['name']} — {tw['tagline'].rstrip('.').lower()} applied to the {sub['name'].lower()} operating unit of {ind['name']}."),
        B_h2("Context"),
        B_p(sub["intro"]),
        B_h2("What breaks today"),
        B_bullets([[t, d] for (_, t, d) in [(None, p[1], p[2]) for p in pains]]),
        B_h2("How we deliver it here"),
        B_p("The pattern composes " + ", ".join(core) + " from the " + tw["name"] + " tower, wired into the unit's "
            "workflows (" + ", ".join(sub["workflows"][:3]) + ") on " + " and ".join(tw["platforms"]) +
            ". Governance inherits the sector frame — " + sub["regs"][0][0] + " among others — with evidence "
            "generated by the delivery itself."),
        B_h2("Services behind the pattern"),
        _scap_services(sub, tower_id, svcs),
        B_h2("Use case"),
        B_bullets([[uc[0], uc[1] + " (" + uc[2] + ")"]] if uc else []),
        B_h2("Compliance frame"),
        B_table("Regimes shaping this capability", ["Regime", "Implication"],
                [[r, i] for r, i in (sub["regs"][:2] + ind["regs"][:1])]),
        B_h2("At industry level, the same pattern"),
        B_p("At " + ind["name"] + " level this capability reads as: " + (ind_uc[1] if ind_uc else "") +
            " (" + (ind_uc[2] if ind_uc else "") + "). The sub-industry page narrows it to the unit's workflows, "
            "regimes and KPIs."),
        B_h2("Outcomes we commit to"),
        B_bullets([[k, v] for k, v in sub["kpis"][:2]]),
        B_cta("Book a briefing with the practice lead for this sub-industry, or return to the industry hub."),
    ]
    return blocks


def build_solution_page(page, sol):
    (sid, cat, name, promise, problem, approach, comps, plats, inds, kpis) = sol
    ind_names = ["all industries"] if inds == ["all"] else [INDUSTRIES[i]["name"] for i in inds if i in INDUSTRIES]
    plat_names = []
    for pid in plats:
        p = _PLAT_BY_ID.get(pid.replace("Achala ", "").lower())
        if p:
            plat_names.append(p)
    proof = [c for c in CASES if any(p2.replace("Achala ", "").lower() in [pp[0] for pp in plat_names] or
                                     any(t in [TOWERS[t2]["name"] for t2 in c["towers"]]
                                         for t in _solution_towers(plats)) for p2 in c["platforms"])][:2]
    blocks = [
        B_hero(promise),
        B_h2("The problem this solution exists for"),
        B_p(problem),
        B_h2("Our approach"),
        B_p(approach),
        B_h2("Components"),
        B_bullets([[a, b] for a, b in comps]),
        B_h2("Platform stack"),
        B_p("The solution runs on " + " and ".join(p[1] for p in plat_names) + ": " +
            " ".join(p[4].rstrip(".") + ". " for p in plat_names[:2])),
        B_h2("How it runs in an engagement"),
        B_bullets([
            ["Diagnose", "baseline metrics for this problem locked with owners; current-state decision/data flow mapped in two weeks."],
            ["Prove", "gated pilot on bounded scope with the falsifiable criterion agreed by finance before the first build sprint."],
            ["Industrialize", "staged rollout on the platform stack with SLOs, replay evidence and operator enablement."],
            ["Compound", "challenger models and policies quarterly; conformance monitoring; annual value audit against baseline."],
        ]),
        B_h2("What you get"),
        B_bullets([
            ["Architecture pack", "reference architecture adapted to your estate, with the integration contracts itemized."],
            ["Working system", "the composed capability live on bounded scope, with evidence generation built in."],
            ["Run model", "runbooks, SLO catalog and the named-pod accountability chain for production."],
            ["Value audit kit", "baseline pack, measurement method and the quarterly review template your finance team signs."],
        ]),
        B_h2("Prerequisites and data readiness"),
        B_p(_pick(sid + "-pre", [
            "Prerequisites are modest and named: governed access to the core data sources, a named executive sponsor and a control owner, and a sandbox where the proof can run on real records.",
            "The readiness checklist covers three items: source-system access under your security policy, an operating team willing to trial the new workflow, and agreement on the baseline measurement method before work starts.",
            "Data readiness matters more than data volume: the diagnostic phase surfaces gaps, and the design phase prices them — no program pretends the estate is cleaner than it is."])),
        B_h2("Proof"),
        B_bullets([[c["client"], c["headline"][:110]] for c in proof] if proof else
                  [["Reference calls", "available under NDA — ask for the closest industry match."]]),
        B_h2("Industry fit"),
        B_p("Deployed across " + ", ".join(ind_names) + ". Each industry play adjusts the regulatory frame, the "
            "integration surface and the KPI set — the pattern stays, the physics changes."),
        B_h2("Outcomes we commit to"),
        B_bullets([[k, v] for k, v in kpis]),
        B_cta("Request a solution briefing — or a scoped value assessment for your version of this problem."),
    ]
    return blocks


def _solution_towers(plat_ids):
    tower_names = {"nexus": "Agentic AI & Hyperautomation", "forge": "Data, Analytics & Lakehouse",
                   "swarm": "Agentic AI & Hyperautomation", "sentinel": "Cybersecurity & Zero-Trust",
                   "twinverse": "IoT, Digital Twin & Robotics", "quanta": "Quantum & Advanced Compute",
                   "ledger": "Blockchain & Digital Trust", "compass": "Applied AI & Generative AI"}
    return [tower_names[p.replace("Achala ", "").lower()] for p in plat_ids if p.replace("Achala ", "").lower() in tower_names]


def build_solutions_hub(page):
    blocks = [
        B_hero("24 outcome-based solutions — anchored to named metrics, platform stacks and industry playbooks."),
        B_p("Solutions are how clients buy outcomes rather than towers: a named business problem, a composed "
            "architecture, a platform stack and committed outcomes. They sit above the service towers and below the "
            "case studies — the bridge between capability and proof."),
        B_h2("The four categories"),
        B_bullets([[SOLUTION_CATEGORIES[c], str(len([s for s in SOLUTIONS if s[1] == c])) + " solutions"] for c in _SOLUTION_CAT_ORDER]),
        B_h2("Solution map"),
        B_table("Solutions at a glance", ["Category", "Solution", "Committed outcome"],
                [[SOLUTION_CATEGORIES[s[1]], s[2], s[9][0][0] + " — " + s[9][0][1]] for s in SOLUTIONS]),
        B_h2("How solutions relate to towers"),
        B_p("Each solution composes services from two to four towers, runs on one or two platforms, and carries an "
            "industry playbook per sector. The pattern stays constant; the physics, regulations and KPIs change by "
            "industry."),
        B_cta("Explore a solution — or describe your problem in a briefing and we will map it to the portfolio."),
    ]
    return blocks


def build_platforms_hub(page):
    blocks = [
        B_hero("Eight proprietary platforms encode a decade of deep-tech delivery as configurable products."),
        B_p("Platforms are how Achala IT Solutions turns consulting into leverage: governance, security posture, evidence "
            "generation and delivery patterns arrive pre-built. Clients start at pattern 80% and finish with systems "
            "their auditors can inspect."),
        B_h2("The portfolio"),
        B_bullets([[p[1] + " — " + p[3], p[4]] for p in PLATFORMS]),
        B_h2("How platforms are used in engagements"),
        B_p("Most programs combine two or three platforms: a decision program lands Nexus on Forge rails; an agentic "
            "program lands Swarm under Compass governance; an industrial program lands Twinverse with Sentinel "
            "segmentation. Each platform page carries Overview, Architecture & Trust and Industry Use Cases."),
        B_table("Platform portfolio map", ["Platform", "Category", "Deployment focus"],
                [[p[1], p[3], ", ".join(p[10][:4])] for p in PLATFORMS]),
        B_cta("Explore a platform — or book a technical briefing with the platform team."),
    ]
    return blocks


def build_platform_overview(page, plat):
    (pid, name, slug, cat, promise, overview, modules, trust_para, trust_bullets, integr, use_inds) = plat
    blocks = [
        B_hero(promise),
        B_h2("What it is"),
        B_p(overview[0]),
        B_h2("How it operates"),
        B_p(overview[1]),
        B_h2("Modules"),
        B_bullets([[a, b] for a, b in modules]),
        B_h2("Trust and compliance"),
        B_p(trust_para),
        B_h2("What changes for the business"),
        B_bullets([
            ["Evidence by default", "every artifact the platform produces doubles as audit evidence — no reconstruction projects."],
            ["Pattern leverage", "teams start at pattern 80% and spend their budget on the 20% that is genuinely yours."],
            ["Accountability", "named control owner per deployment; platform telemetry makes the owner's job inspectable."],
        ]),
        B_h2("How programs use it"),
        B_p(_pick(pid + "-use", [
            "Most programs deploy " + name + " inside the customer's landing zone with a Achala pod operating it through a named run model, then transfer operations to client teams once the SLOs have held for two quarters.",
            " " + name + " typically enters an estate during the Prove phase — configured for your controls in the sandbox, hardened through Industrialize, and left running under the customer's own keys with our pods on the follow-the-sun operations rhythm."])),
        B_h2("Integrations"),
        B_p("Certified integration surface: " + ", ".join(integr) + "."),
        B_h2("Where it is deployed"),
        B_p("Primary industry deployments: " + ", ".join(INDUSTRIES[i]["name"] for i in use_inds if i in INDUSTRIES) + "."),
        B_cta("Read the Architecture & Trust page, or book a platform briefing with the engineering team."),
    ]
    return blocks


def build_platform_architecture(page, plat):
    (pid, name, slug, cat, promise, overview, modules, trust_para, trust_bullets, integr, use_inds) = plat
    blocks = [
        B_hero(f"Architecture, security posture and audit evidence for {name} — {cat.lower()} from Achala IT Solutions."),
        B_h2("Reference architecture"),
        B_p("The platform separates three planes. The data plane carries workload (" +
            ", ".join(b for a, b in modules[:3]) + "); the control plane carries policy and orchestration (" +
            ", ".join(b for a, b in modules[3:5]) + "); the evidence plane carries audit, replay and conformity "
            "documentation — the plane most vendors skip and every regulator asks about."),
        B_h2("Security posture"),
        B_p(trust_para),
        B_h2("Trust controls"),
        B_bullets([[a, b] for a, b in trust_bullets]),
        B_h2("Compliance mapping"),
        B_bullets([
            ["SOC 2 Type II / ISO 27001", "platform controls audited; evidence exports mapped to customer audit scopes."],
            ["Sector regimes", "DORA, HIPAA-ready pods, PCI DSS support and GDPR data-residency options where the estate requires them."],
            ["AI-specific", "NIST AI RMF and ISO/IEC 42001 control mapping; EU AI Act documentation generated for high-risk deployments."],
        ]),
        B_h2("Performance envelope"),
        B_p(_pick(pid + "-perf", [
            "The control plane is sized for enterprise scale: decision and orchestration paths carry published latency budgets, and the evidence plane writes append-only logs that never sit on the hot path.",
            "Scaling is horizontal by design — workload planes shard by tenant and region, while the evidence plane compacts to cold storage on schedule, keeping audit queries fast without taxing production throughput."])),
        B_h2("Deployment models"),
        B_bullets([
            ["Customer tenancy", "deployed inside your cloud landing zone; customer-managed keys; your SIEM receives telemetry."],
            ["Achala managed", "operated by our pods under SOC 2 Type II and ISO 27001 with quarterly evidence exports."],
            ["Hybrid / edge", "Twinverse and Sentinel patterns extend to plant, store and site estates with signed boot and 62443-aligned segmentation."],
        ]),
        B_h2("Integration surface"),
        B_p(" " + ", ".join(integr) + ". Adapters to core systems (CRM, ERP, core banking, EHR, WMS/MES, SCADA) are "
            "versioned contracts — one schema change propagates to every consumer."),
        B_cta("Request the architecture pack under NDA — or book a session with the platform security lead."),
    ]
    return blocks


def build_platform_usecases(page, plat):
    (pid, name, slug, cat, promise, overview, modules, trust_para, trust_bullets, integr, use_inds) = plat
    tw_id = _PLATFORM_TOWER[pid]
    rows = []
    for ind_id in use_inds:
        ind = INDUSTRIES.get(ind_id)
        if not ind:
            continue
        ucs = ind["usecases"].get(tw_id, [])
        if ucs:
            u = ucs[_h(f"{pid}-{ind_id}") % len(ucs)]
            rows.append([ind["name"], u[0], u[2]])
    rel = [c for c in CASES if any(p.replace("Achala ", "").lower() == pid for p in c["platforms"])]
    if rel:
        rel_blocks = [B_bullets([[c["client"], c["headline"]] for c in rel[:4]])]
    else:
        rel_blocks = [B_p("Reference engagements available under NDA — ask the platform team for the closest match to your estate.")]
    blocks = [
        B_hero(f"{name} in the field — deployment patterns by industry, with committed outcomes."),
        B_h2("Deployment patterns"),
        B_table(f"{name} across industries", ["Industry", "Pattern", "Committed outcome"],
                rows if rows else [["—", "—", "—"]]),
        B_h2("What a rollout looks like"),
        B_p("Rollouts follow the Achala Method on this platform's rails:"),
        B_bullets([
            ["Diagnose (2-4 weeks)", "baseline metrics locked; data-readiness assessed against the platform's contracts."],
            ["Prove (6-10 weeks)", "pilot on a bounded scope with falsifiable criteria and the platform configured for your controls."],
            ["Industrialize (1-3 quarters)", "staged rollout with SLO instrumentation, replay evidence and operator enablement."],
            ["Compound (ongoing)", "challenger models/policies, conformance monitoring, quarterly value reviews."],
        ]),
        B_h2("The operator's story"),
        B_p(_pick(pid + "-op", [
            "Day to day, the operating team sees one control surface: health, throughput, cost and policy violations for the workloads " + name + " carries. Escalations arrive with the context attached — the runbook, the affected scope, the last passing evidence — instead of a raw alert and a hunch.",
            "Operators describe the change as boring, in the best sense: the platform handles the recoverable failures by policy, pages humans only on user impact, and every intervention is logged into the evidence trail automatically."])),
        B_h2("Integration pattern"),
        B_p(" " + ", ".join(integr) + " — integrated through versioned contracts. Adapters to core systems (CRM, ERP, "
            "core banking, EHR, WMS/MES, SCADA) are maintained like products: schema changes are tested against "
            "consumer suites before release, and one contract update propagates to every human or agent consumer."),
        B_h2("Programs on this platform"),
    ] + rel_blocks + [
        B_cta("Book a platform briefing — or request reference calls with clients running this platform in production."),
    ]
    return blocks


def build_cases_hub(page):
    blocks = [
        B_hero("Anonymized engagements with measured outcomes — the numbers are the story."),
        B_p("Every case below names the client descriptor, the challenge, the architecture built and the measured "
            "outcomes. Client names are withheld under confidentiality; the metrics, durations and team shapes are "
            "real to the engagement and illustrative for planning."),
        B_h2("The portfolio"),
        B_table("36 engagements across 12 industries", ["Industry", "Client", "Headline outcome"],
                [[INDUSTRIES[c["industry"]]["name"], c["client"], c["headline"][:110]] for c in CASES]),
        B_cta("Filter by industry from the menu — or book a briefing and ask for reference calls."),
    ]
    return blocks


def build_case_study(page, case):
    ind = INDUSTRIES[case["industry"]]
    tw_names = [TOWERS[t]["name"] for t in case["towers"]]
    blocks = [
        B_hero(case["headline"]),
        B_h2("Client profile"),
        B_p(case["client"] + " — " + ind["name"] + " engagement delivered by a " + case["facts"][1].lower() +
            " over " + case["facts"][0].lower() + ", " + case["facts"][2] + " scope, commercial model: " +
            case["facts"][3].lower() + "."),
        B_h2("The challenge"),
        B_bullets([["Challenge", ch] for ch in case["challenge"]]),
        B_h2("What Achala IT Solutions built"),
        B_p(case["solution"]),
        B_h2("The delivery pattern"),
        B_p(_pick(case["id"] + "-dp", [
            "The program ran through the Achala Method: a Value Mapping Sprint locked the baseline, a gated PoC produced the capital-grade evidence, and production hardening (replay, SLOs, control tests) was generated by the delivery itself rather than reconstructed for audit.",
            "Delivery followed the standard rhythm — Diagnose with a signed baseline, Prove with falsifiable criteria, Industrialize with staged rollouts — while the control evidence (model cards, decision replay, security tests) accumulated as artifacts of the build.",
            "The engagement was structured for transfer: named pod, documented runbooks, operator enablement, and a Compound phase that keeps challenger programs and conformance monitoring running after handover."])),
        B_h2("Same pattern, adjacent sectors"),
        B_bullets([[_pick(case["id"] + "-adj1", [c for c in CASES if c["industry"] != case["industry"]][:18])["client"],
                    _pick(case["id"] + "-adj1", [c for c in CASES if c["industry"] != case["industry"]][:18])["headline"][:100]],
                   [_pick(case["id"] + "-adj2", [c for c in CASES if c["industry"] != case["industry"]][18:])["client"],
                    _pick(case["id"] + "-adj2", [c for c in CASES if c["industry"] != case["industry"]][18:])["headline"][:100]]]),
        B_h2("Capability stack"),
        B_p("Towers: " + ", ".join(tw_names) + ". Platforms: " + ", ".join(case["platforms"]) + "."),
        B_h2("Outcomes"),
        B_table("Measured outcomes", ["Metric", "Result"], [[k, v] for k, v in case["outcomes"]]),
        B_h2("Engagement facts"),
        B_table("Program facts", ["Dimension", "Detail"],
                [["Duration", case["facts"][0]], ["Team", case["facts"][1]],
                 ["Scope", case["facts"][2]], ["Commercial model", case["facts"][3]]]),
        B_h2("Transfer notes"),
        B_bullets([
            ["What transferred directly", _pick(case["id"] + "-t1", [
                "the decision/data architecture pattern, the control matrix and the run model — adapted per estate in weeks, not quarters.",
                "the platform configuration patterns and the operator enablement curriculum, refined across engagements of this type."])],
            ["What never transfers", _pick(case["id"] + "-t2", [
                "the baseline numbers and the client's specific regulatory posture — your program starts with its own locked baseline.",
                "organizational absorption: adoption paths are designed for each client's operating culture, never assumed."])],
        ]),
        B_note("Client identity withheld under confidentiality. Metrics are reported against the baseline locked in the Diagnose phase; measurement method available under NDA."),
        B_cta("Ask for a reference conversation on this pattern — or map it to your estate in a briefing."),
    ]
    return blocks


def _company_blocks(page):
    pid = page["id"]
    blocks = []
    if pid == "CO-about":
        blocks = [
            B_hero(BRAND["positioning"]),
        ] + [B_p(p) for p in ABOUT_PAGE["paras"]] + [
            B_h2("Facts"),
            B_table("Achala IT Solutions at a glance", ["Dimension", "Detail"], [[a, b] for a, b in ABOUT_PAGE["fact_blocks"]]),
            B_h2("What we deliberately do not do"),
            B_bullets([
                ["No generic application development", "we do not compete on commodity web and mobile builds — the towers above are the portfolio."],
                ["No data as training material", "zero-exposure architecture by default; client data never trains shared models."],
                ["No ungated pilots", "every PoC carries falsifiable criteria and a documented go/redirect/stop decision."],
            ]),
            B_h2("Global footprint"),
            B_table("Delivery centers", ["Location", "City", "Focus", "Address"],
                    [[o[0], o[1], o[2], o[3]] for o in BRAND["offices"]]),
        ]
    elif pid == "CO-edge":
        blocks = [
            B_hero(EDGE_PAGE["paras"][0].split(". ")[0] + "."),
        ] + [B_p(p) for p in EDGE_PAGE["paras"]] + [
            B_h2("The five edges"),
            B_bullets([[a, b] for a, b in EDGE_PAGE["edge_points"]]),
            B_h2(BRAND["metrics_heading"]),
            B_table("Proof points", ["Metric", "Meaning"], [[a, b] for a, b in BRAND["proof_bar"]]),
        ]
    elif pid == "CO-leadership":
        blocks = [
            B_hero("Named accountability from the top: every platform, tower and control carries an executive owner."),
            B_p("Achala IT Solutions's leadership structure mirrors its delivery model — each executive owns a tower portfolio "
                "and the outcomes it commits to. Roles and focus areas below; names and bios are maintained by the "
                "communications team."),
            B_h2("Executive team"),
            B_table("Leadership roles", ["Role", "Name", "Focus"],
                    [[r, n, f] for (r, n, f) in LEADERSHIP]),
            B_h2("Governance bodies"),
            B_p("Three boards govern delivery: the AI Governance Board (model risk, EU AI Act conformity), the "
                "Security Board (zero-trust estate, DORA posture) and the Delivery Quality Board (SLOs, evidence, "
                "value audits). Minutes and decisions are auditable artifacts, not memories."),
            B_h2("How leadership engages with clients"),
            B_p("Executives carry a client portfolio, not just a function: the practice lead who scopes your program "
                "escalates to the tower-owning executive within one level, and the annual value audit for every "
                "outcome-linked engagement is reviewed by the CFO's office against the original baseline pack."),
        ]
    elif pid == "CO-offices":
        blocks = [
            B_hero("Four delivery centers, one accountability chain — strategy in the US, execution around the sun."),
            B_p("Achala IT Solutions runs four centers with distinct mandates. Programs are staffed by named pods that stay "
                "with the outcome — the team that designs your decision hub is accountable for its production "
                "results, wherever they sit."),
            B_h2("The centers"),
            B_table("Global offices", ["Center", "City", "Mandate", "Address"],
                    [[o[0], o[1], o[2], o[3]] for o in BRAND["offices"]]),
            B_h2("Operating rhythm"),
            B_p("Follow-the-sun operations for managed SOC, platform operations and agent-fleet operations; "
                "capability centers of excellence per tower; and a rotation program that moves engineers across "
                "centers so patterns travel with people."),
            B_h2("What each center carries"),
            B_bullets([
                ["US — Tysons Corner", "quantum and advanced compute practice, board advisory, outcome-linked commercial design."],
                ["UK — London", "DORA and regulatory programs, financial-services delivery, European data-residency patterns."],
                ["India — Global Execution Core", "data and platform factories, agentic engineering pods, 24/7 operations depth."],
                ["KSA — Riyadh", "Vision 2030 programs, sovereign delivery models, energy and smart-city practices."],
            ]),
            B_h2("Security zoning across centers"),
            B_p("Delivery pods operate under a single security architecture: zero-exposure defaults, customer-managed "
                "keys for client data, zoned networks per center, and cross-center access governed by the same "
                "zero-trust controls we sell. SOC 2 Type II and ISO 27001 cover the operated estate end to end."),
        ]
    elif pid == "CO-values":
        blocks = [
            B_hero(VALUES_PAGE["paras"][0].split(". ")[0] + "."),
        ] + [B_p(p) for p in VALUES_PAGE["paras"]] + [
            B_h2("The five values"),
            B_bullets([[a, b] for a, b in BRAND["values"]]),
            B_h2("Culture in practice"),
            B_bullets([[a, b] for a, b in VALUES_PAGE["culture_points"]]),
            B_h2("How values bind commercially"),
            B_p("The values are contractual, not decorative: outcome-linked fees only exist because 'outcomes over "
                "output' is enforced; zero-exposure architecture only survives sales pressure because it is a "
                "term of engagement. Culture at Achala IT Solutions is what makes the commercial model safe to sign."),
        ]
    elif pid == "CO-careers":
        blocks = [
            B_hero(CAREERS_PAGE["paras"][0].split(". ")[0] + "."),
        ] + [B_p(p) for p in CAREERS_PAGE["paras"]] + [
            B_h2("What we offer"),
            B_bullets([[a, b] for a, b in CAREERS_PAGE["career_points"]]),
            B_h2("How hiring works"),
            B_bullets([
                ["Craft interview", "a scoped problem from your claimed specialty, worked live with a senior engineer."],
                ["Judgment interview", "an evidence-discipline case: baselines, gates and an honest stop decision."],
                ["Team fit", "a working session with the pod you would join — no separate HR theater."],
            ]),
            B_h2("Open towers"),
            B_p("Hiring concentrates in: applied AI engineering, agentic systems, data platform engineering, "
                "cybersecurity architecture, quantum program delivery, DLT engineering, IoT/twin engineering and the "
                "industry domain practices. Openings: 【careers portal link】."),
        ]
    elif pid == "CO-newsroom":
        blocks = [
            B_hero("Announcements, platform releases and recognitions — maintained by the communications team."),
        ] + [B_p(p) for p in NEWSROOM_PAGE["paras"]] + [
            B_h2("What we publish"),
            B_bullets([
                ["Platform releases", "major capability releases across the eight platforms, with release notes."],
                ["Partnerships", "architecture-level partnerships and what they change for clients."],
                ["Recognition", "analyst placements and industry awards, with context."],
                ["Research notes", "selected insights from the library, cross-posted for media use."],
            ]),
            B_h2("Latest entries"),
            B_bullets([["Entry", ph] for ph in NEWSROOM_PAGE["placeholders"]]),
            B_h2("Media contact"),
            B_p("Press inquiries: 【press email】 · Analyst relations: 【analyst relations email】 · Brand assets and "
                "boilerplate: 【media kit link】. We respond to media requests within one business day."),
        ]
    elif pid == "CO-partners":
        blocks = [
            B_hero(PARTNERS_PAGE["paras"][0].split(". ")[0] + "."),
        ] + [B_p(p) for p in PARTNERS_PAGE["paras"]] + [
            B_h2("Partner tiers"),
            B_bullets([[a, b] for a, b in PARTNERS_PAGE["partner_tiers"]]),
            B_h2("What each partnership changes for clients"),
            B_table("Ecosystem map", ["Tier", "What clients get", "Named partners"],
                    [["Strategic alliances", "joint reference architectures and co-funded pilots",
                      "【hyperscaler and data-platform partners】"],
                     ["Technology partners", "certified integrations and shared support paths",
                      "【security, data, quantum and DLT vendors】"],
                     ["Alliance network", "extended delivery reach in-region",
                      "【regional SI and domain partners】"]]),
            B_h2("Partner principles"),
            B_p("Architecture first, resale never: partnerships exist to compress deployment paths, certify "
                "integrations and share support models. Where partners and Achala platforms overlap, we say so "
                "explicitly in the architecture."),
        ]
    return blocks


def build_company_page(page):
    return _company_blocks(page)


def build_approach_page(page, key):
    ap = APPROACH_PAGES[key]
    blocks = [B_hero(ap["intro"])]
    if key == "method":
        blocks += [
            B_p("The Method exists to prevent the classic failure mode: strategy decks that never survive contact "
                "with production. Each phase ends at a named gate with named signatories — finance, risk, operations."),
            B_h2("The five phases"),
            B_table("Phases and gates", ["Phase", "What happens", "Gate"],
                    [[a, b, c] for a, b, c in ap["phases"]]),
            B_h2("Why gates matter"),
            B_p("Gates convert enthusiasm into evidence. A program cannot enter Industrialize without a value memo; "
                "cannot claim Compound without an annual audit against the original baseline. The gates are the "
                "reason roughly one in three PoCs ends with a documented stop — and why the rest scale with confidence."),
        ]
    elif key == "outcome-linked":
        blocks += [
            B_p("Traditional commercials buy effort; ours buy outcomes. Four models, selectable per program and "
                "mixable within a portfolio:"),
            B_h2("The models"),
            B_bullets([[a, b] for a, b in ap["models"]]),
            B_h2("How measurement works"),
            B_p(ap["governance"]),
            B_h2("Selection guide"),
            B_bullets([
                ["Use an outcome pilot", "when the capability is new to your estate and the capital committee wants evidence before scale."],
                ["Use value-linked fees", "when the metric is unambiguous (loss rate, cycle time, unit cost) and the baseline can be locked cleanly."],
                ["Use a platform subscription", "when the capability is a long-lived utility — decisioning, lakehouse, security operations."],
                ["Use co-innovation", "when the frontier is genuinely unmapped and both sides accept documented negative results."],
            ]),
            B_h2("What we will not do"),
            B_p("We do not sign outcome links on metrics the client cannot measure, on baselines that cannot be "
                "locked, or on outcomes that depend on factors outside the program's control. A failed negotiation "
                "on measurement is better than a disputed invoice."),
        ]
    elif key == "responsible-ai":
        blocks += [
            B_p("Responsible AI at Achala IT Solutions is not a policy page; it is five control layers wired into every "
                "delivery, mapped to NIST AI RMF, ISO/IEC 42001 and the EU AI Act."),
            B_h2("The five layers"),
            B_bullets([[a, b] for a, b in ap["layers"]]),
            B_h2("What this means in practice"),
            B_p("High-risk use cases (credit scoring, employment screening, medical triage) ship with documentation, "
                "human-oversight gates and post-market monitoring as built artifacts. Every model carries a card, an "
                "evaluation report and a named control owner. Zero-exposure architecture means client data is never "
                "training material — enforced by design, evidenced by lineage."),
            B_h2("What conformity looks like"),
            B_bullets([
                ["EU AI Act", "technical documentation, human-oversight evidence and post-market monitoring plans generated per high-risk system."],
                ["Model risk", "SR 11-7/TRIM-aligned validation packs produced during build, accepted by model-risk committees."],
                ["Internal audit", "read-only access to the evidence plane — control tests, decision replay, guardrail configurations."],
            ]),
        ]
    else:
        blocks += [
            B_p("The delivery model balances strategy proximity with execution depth — and keeps one accountability "
                "chain per program from diagnosis to compound."),
            B_h2("Elements"),
            B_bullets([[a, b] for a, b in ap["elements"]]),
            B_h2("Named pods"),
            B_p("Every program runs with a named pod: a delivery lead, a named quality owner and a named control "
                "owner. Escalation paths are published; the follow-the-sun rhythm covers managed SOC, platform "
                "operations and agent-fleet operations."),
        ]
    blocks += [
        B_h2("In practice"),
        B_bullets([[c["client"], c["headline"][:110]]
                   for c in [CASES[0], CASES[12], CASES[19]][:3]]),
        B_p("Every reference engagement above ran on this model — the gates, the measurement discipline and the "
            "commercial alignment are the same machinery in every industry. What changes is the physics."),
    ]
    blocks.append(B_cta("Discuss how the model applies to your program — book a briefing with the practice lead."))
    return blocks


def build_contact_page(page, key):
    cp = CONTACT_PAGES[key]
    blocks = [B_hero(cp["paras"][0].split(". ")[0] + ".")]
    blocks += [B_p(p) for p in cp["paras"]]
    if key == "contact":
        blocks += [
            B_h2("Regional practice leads"),
            B_table("Where to reach us", ["Center", "City", "Practice focus"],
                    [[o[0], o[1], o[2]] for o in BRAND["offices"]]),
            B_h2("What happens next"),
            B_bullets([
                ["Within one business day", "a practice lead (not a call center) responds with the relevant domain pod."],
                ["Within one week", "a 45-minute working session: your metric, our pattern library, three reference engagements."],
                ["Within one month", "if it fits, a Value Assessment proposal — six weeks to a capital-committee-grade roadmap."],
            ]),
        ]
    else:
        blocks += [
            B_h2("How the session runs"),
            B_bullets([
                ["Preparation", "we review your public materials and come with the closest pattern library — no decks assembled for the occasion."],
                ["The session", "your metric and constraints, our three reference engagements, an honest feasibility verdict with a delivery sketch."],
                ["The follow-up", "a two-page readout within 48 hours: pattern, evidence, and the decision we would make in your position."],
            ]),
        ]
        blocks += [
            B_h2("Common questions"),
            B_bullets([
                ["Who attends?", "a practice lead for your domain plus the delivery lead who would run the program — decision-grade people."],
                ["What does it cost?", "nothing. The briefing and readout are how we demonstrate the evidence discipline before you pay for it."],
                ["What if the verdict is no?", "you get the same two-page readout with the reasoning — most engagements are won later, on trust."],
            ]),
        ]
    blocks.append(B_cta("Book a briefing — or request the Value Assessment directly."))
    return blocks


def build_legal_page(page, slug, title, desc):
    return [
        B_hero(f"{title} — Achala IT Solutions."),
        B_p(desc),
        B_p("Achala IT Solutions publishes its legal documents in plain language. Where this template references company "
            "details (registered entities, data-protection officers, jurisdiction-specific rights), the placeholders "
            "mark exactly what counsel must confirm: the " + BRAND["legal_name"] + " entity structure spans the US, "
            "UK, India and KSA, and each publication locale binds to its applicable regime."),
        B_h2("Document control"),
        B_bullets([
            ["Owner", "【legal owner name and title】"],
            ["Effective date", "【effective date】 — superseding version 【previous version date】"],
            ["Review cycle", "annual, or upon material change to processing activities or applicable law"],
        ]),
        B_note("This page is a content template. Legal text must be reviewed and finalized by counsel before publication — placeholders mark where company-specific details are required."),
    ]


def build_insights_hub(page):
    blocks = [
        B_hero("Perspectives from the delivery floor — engineering notes, market views and honest lessons."),
        B_p("The Insights library is organized by tower. Articles are short, evidence-anchored and written by the "
            "practices that ship the work — no vendor-think-piece register."),
        B_p("Every article carries three things: the delivery position (what we believe and why), the evidence "
            "(benchmarks with classical baselines, program numbers), and the transfer path (which services and "
            "platforms deliver the pattern). Where the honest answer is 'it depends', we say what it depends on."),
        B_h2("Categories"),
        B_bullets([[TOWERS[t]["name"], TOWERS[t]["tagline"]] for t in TOWER_ORDER]),
        B_cta("Pick a category — or subscribe for quarterly delivery notes."),
    ]
    return blocks


def build_insights_category(page, tower_id):
    tw = TOWERS[tower_id]
    arts = [i for i in INSIGHTS if i[1] == tower_id]
    blocks = [
        B_hero(f"{tw['short']} insights — {tw['tagline'].rstrip('.').lower()}."),
        B_p("Notes from the " + tw["name"] + " practice: what we are seeing across engagements, what the numbers say, "
            "and where the pattern is moving."),
        B_h2("What this category publishes"),
        B_p("Delivery notes grounded in live programs, benchmark results with their classical baselines, and honest "
            "negative results — the perspectives we wish vendors published when we were on the buying side."),
        B_h2("Latest articles"),
        B_bullets([[a[2], a[3]] for a in arts]),
        B_h2("Cadence"),
        B_p("New notes land with platform releases and program milestones — roughly quarterly per tower — and every "
            "article links to the service pages where the pattern is actually delivered."),
        B_h2("Key questions this category answers"),
        B_bullets([
            ["Is this real in production?", "each note states where the pattern runs today, at what scale, with what evidence."],
            ["What does it cost to be honest?", "benchmark methodology and baselines are published; negative verdicts included."],
        ]),
        B_h2("Where to go deeper"),
        B_p("The services behind these perspectives live under /services/" + tw["slug"] + "/ — each with deliverables, "
            "stack and committed outcomes."),
        B_cta("Discuss with the tower practice lead — or explore the services behind the articles."),
    ]
    return blocks


def build_insight_article(page, ins):
    iid, tw_id, title, thesis, points, stat = ins
    tw = TOWERS[tw_id]
    svcs = _tower_services[tw_id]
    rel = [svcs[_h(f"{iid}-r{i}") % len(svcs)]["name"] for i in range(2)]
    arg_para = title + " is not a slogan; it is a delivery position. " + _pick(f"{iid}-a", [
        "Across engagements the pattern repeats: programs that respect this move faster and survive audit; those that do not pay for it later — usually in the audit itself.",
        "We keep seeing the same economics: teams that internalize this spend their budget on value, while teams that ignore it spend on rework and explanations.",
        "The evidence is consistent across industries — the constraint is rarely technology; it is whether the operating model takes this seriously from sprint one."])
    q1 = _pick(iid + "-q1", [
        "Where exactly does the evidence for each claim live — and can your auditor reach it without a project?",
        "What is the classical baseline every proposed capability must beat, measured on identical data?"])
    q2 = _pick(iid + "-q2", [
        "Which named individual owns the control environment around this capability — not the function, the person?",
        "Who signs the go/no-go gate, and what evidence do they require before signing?"])
    q3 = _pick(iid + "-q3", [
        "What did you stop last quarter, and what did the stop save us?",
        "Show us a negative result you documented — the discipline is the product."])
    blocks = [
        B_hero(thesis),
        B_h2("The argument"),
        B_p(arg_para),
        B_h2("Three things that matter"),
        B_bullets([[f"Point {i+1}", p] for i, p in enumerate(points)]),
        B_h2("Three questions to ask your current vendors"),
        B_bullets([["Question 1", q1], ["Question 2", q2], ["Question 3", q3]]),
        B_h2("Where programs fail with this"),
        B_p(_pick(iid + "-fail", [
            "The failure mode is predictable: enthusiasm funds the demo, budget cycles gate the industrialization, and by the time the governance conversation starts, shadow usage has already created the exposure the review was meant to prevent.",
            "Programs stall when the operating model is treated as an afterthought — the technology works in week six and the organization has not changed in week sixty, so the capability quietly degrades into shelfware.",
            "The expensive mistake is measurement retrofits: without the baseline locked in week one, every outcome claim becomes an argument instead of an audit, and the program loses its budget defense."])),
        B_h2("What we do differently"),
        B_bullets([
            ["Gate the enthusiasm", "falsifiable criteria and locked baselines before build; the demo is the least important artifact."],
            ["Design the operating model", "named owners, run models and escalation paths agreed with the operating team, not for it."],
            ["Generate evidence in-flight", "replay trails, control tests and documentation as artifacts of the build — never reconstructed."],
        ]),
        B_h2("The number that matters"),
        B_p(stat),
        B_h2("Where this shows up in our work"),
        B_p("This perspective is grounded in " + rel[0] + " and " + rel[1] + " within the " + tw["name"] +
            " tower — each carried by our platforms with governance and evidence built in."),
        B_cta("Read the related service pages — or bring this pattern to your estate in a briefing."),
    ]
    return blocks


# ------------------------------------------------------------------
# Dispatcher + export
# ------------------------------------------------------------------

def compose_page(page):
    pid = page["id"]
    if pid == "HOME":
        return build_home(page)
    if pid == "SVCHUB":
        return build_services_hub(page)
    if pid.startswith("TWR-"):
        tower_name = page["l2"]
        tower_id = [t for t in TOWER_ORDER if TOWERS[t]["name"] == tower_name][0]
        return build_tower_hub(page, tower_id)
    if pid.startswith("SVC-"):
        return build_service_page(page, _svc_by_id[pid[4:]])
    if pid == "INDHUB":
        return build_industries_hub(page)
    if pid.startswith("IND-"):
        return build_industry_hub(page, pid[4:])
    if pid.startswith("SUB-"):
        return build_subindustry_page(page, SUBS[pid[4:]])
    if pid.startswith("CAP-"):
        body = pid[4:]
        tw_id = next(t for t in TOWER_ORDER if body.endswith("-" + t))
        ind_id = body[: -(len(tw_id) + 1)]
        return build_industry_capability(page, ind_id, tw_id)
    if pid.startswith("SCAP-"):
        body = pid[5:]
        sub_slug, tw_id = body.rsplit("-", 1)
        # tower ids contain '-', resolve by longest match from end
        for t in TOWER_ORDER:
            if body.endswith("-" + t):
                sub_slug = body[: -(len(t) + 1)]
                tw_id = t
                break
        return build_sub_capability(page, SUBS[sub_slug], tw_id)
    if pid == "SOLHUB":
        return build_solutions_hub(page)
    if pid.startswith("SOL-"):
        sol = [s for s in SOLUTIONS if s[0] == pid[4:]][0]
        return build_solution_page(page, sol)
    if pid == "PLTHUB":
        return build_platforms_hub(page)
    if pid.startswith("PLT-"):
        _, pidname, kind = pid.split("-", 2)
        plat = _PLAT_BY_ID[pidname]
        if kind == "ov":
            return build_platform_overview(page, plat)
        if kind == "ar":
            return build_platform_architecture(page, plat)
        return build_platform_usecases(page, plat)
    if pid.startswith("CASE-"):
        case = [c for c in CASES if c["id"] == pid[5:]][0]
        return build_case_study(page, case)
    if pid == "CASEHUB":
        return build_cases_hub(page)
    if pid.startswith("CO-"):
        return build_company_page(page)
    if pid.startswith("AP-"):
        return build_approach_page(page, pid[3:])
    if pid.startswith("CT-"):
        slug = pid[3:]
        if slug in ("contact", "briefing", "assessment"):
            return build_contact_page(page, slug)
        for s, t, d in CONTACT_PAGES["legal"]:
            if s == slug:
                return build_legal_page(page, s, t, d)
    if pid == "INSHUB":
        return build_insights_hub(page)
    if pid.startswith("INSCAT-"):
        return build_insights_category(page, pid[7:])
    if pid.startswith("INS-"):
        ins = [i for i in INSIGHTS if i[0] == pid[4:]][0]
        return build_insight_article(page, ins)
    raise ValueError(f"Unknown page id {pid}")


def compose_all():
    pages = build_ia()
    volumes = {}
    inventory = []
    for page in pages:
        blocks = compose_page(page)
        words = 0
        for b in blocks:
            if b["t"] in ("p", "hero", "cta", "note"):
                words += len(b["x"].split())
            elif b["t"] in ("h2", "h3"):
                words += len(b["x"].split())
            elif b["t"] == "bullets":
                for it in b["items"]:
                    words += len(str(it[0]).split()) + len(str(it[1]).split())
            elif b["t"] == "table":
                words += len(b["caption"].split())
                for row in b["rows"]:
                    words += sum(len(str(c).split()) for c in row)
        volumes.setdefault(page["volume"], []).append({
            "id": page["id"], "title": page["title"], "url": page["url"], "template": page["template"],
            "breadcrumb": page["breadcrumb"], "seo_title": page["seo_title"],
            "meta_description": page["meta_description"], "blocks": blocks, "words": words,
            "section": page["section"], "l1": page["l1"], "l2": page["l2"], "l3": page["l3"], "l4": page["l4"],
        })
        inventory.append({k: page[k] for k in ("id", "section", "l1", "l2", "l3", "l4", "title", "url",
                                               "template", "seo_title", "meta_description", "word_target",
                                               "volume", "priority", "breadcrumb")})
        inventory[-1]["composed_words"] = words
    for vol, pages_in in volumes.items():
        doc = {"volume": vol, "volume_title": VOL_NAMES[vol], "pages": pages_in}
        with open(os.path.join(OUT_DIR, f"{vol}.json"), "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=1)
    with open(os.path.join(OUT_DIR, "inventory.json"), "w", encoding="utf-8") as f:
        json.dump(inventory, f, ensure_ascii=False, indent=1)
    return volumes, inventory


if __name__ == "__main__":
    volumes, inventory = compose_all()
    total_words = sum(p["words"] for pages in volumes.values() for p in pages)
    print(f"Composed {len(inventory)} pages, total words: {total_words}")
    for v in sorted(volumes):
        w = sum(p['words'] for p in volumes[v])
        print(f"  {v}: {len(volumes[v])} pages, {w} words")
    low = [p for pages in volumes.values() for p in pages if p["words"] < 300]
    print(f"Pages under 300 words: {len(low)}")
    for p in low[:10]:
        print("   ", p["id"], p["words"])
