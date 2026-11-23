# -*- coding: utf-8 -*-
"""Long-tail hand-rewrite: every remaining page type gets hand-authored copy in
the Achala voice (CXO-facing, corporate, concrete), parameterized by domain,
industry and practice name. Structural blocks (tables, archs, dashboards,
diagrams, bullets beyond the intro) are preserved; heroes, intro paragraphs
and CTAs are rewritten. Facts stay within already-published claims."""

import json, os, sys

ROOT = "/home/z/my-project/achala/site"
PAGES = os.path.join(ROOT, "src/content/pages")
stats = {"n": 0, "types": {}}

# ── hand-authored domain voices (8) ─────────────────────────────────────────
DOMAINS = {
    "Agentic AI & Hyperautomation": {
        "promise": "agents that execute real process steps under explicit grants, with the supervision layer your risk team signs off",
        "value": "Achala builds this as production infrastructure, not a pilot: every agent is versioned, every permission is scoped, every handoff to a person is logged. The result is automation your operations and compliance teams can both stand behind.",
        "cta": "Bring one process to a 45-minute Achala briefing. We will show the agent design, the supervision model and the baseline it would be measured against.",
            "who": "COOs and operations leads carrying process cost, and the risk officers who must approve what the agents touch.",
    "hub_hero": "Achala's Agentic AI & Hyperautomation domain turns validated AI agents into a governed digital workforce. Eight practices cover the full path — from decision intelligence and process orchestration to document operations — each one landing agents into production under explicit grants, budgets and audit trails.",
    },
    "Applied AI & Generative AI": {
        "promise": "models that earn their place on the P&L, deployed with the evaluation discipline regulators and boards expect",
        "value": "Achala ships applied AI with its evidence attached: evaluation harnesses, drift monitoring and measured deltas against your baseline. If a model does not beat the baseline, we say so — that honesty is why clients keep the programs running.",
        "cta": "Bring one AI use case to an Achala briefing. We will show the evaluation plan, the reference architecture and the metric it would move.",
            "who": "product and business leaders with a P&L line to move, and CDOs consolidating AI governance.",
    "hub_hero": "Achala's Applied AI & Generative AI domain takes AI from promising demo to dependable production. Eight practices span strategy, GenAI platform engineering, retrieval systems and multimodal products — every deployment carrying its own evaluation record and business metric.",
    },
    "Blockchain & Digital Trust": {
        "promise": "shared-record networks and tokenized assets with governance your regulators can inspect",
        "value": "Achala runs permissioned networks where every participant sees the same truth and no one can change it alone. Consensus rules, key ceremonies and inspection exports are documented from day one — shared trust that survives an audit.",
        "cta": "Bring one shared-record problem to an Achala briefing. We will show the network design, the consensus rules and the regulator views it produces.",
            "who": "CFOs and operations heads reconciling across organizations, and the regulators who demand inspection views.",
    "hub_hero": "Achala's Blockchain & Digital Trust domain builds the record-sharing layer between organizations. Eight practices cover consortium design, tokenization, provenance and audit chains — production networks where trading partners, regulators and auditors all read the same history.",
    },
    "Cloud, Edge & Platform Engineering": {
        "promise": "estates that move to cloud without breaking anything — and run measurably cheaper once there",
        "value": "Achala stages every migration with reconciliation gates: the old system and the new one run side by side until the numbers match. Rollback plans are written before cutover, not after incidents.",
        "cta": "Bring one estate challenge to an Achala briefing. We will show the migration sequence, the reconciliation plan and the cost curve it produces.",
            "who": "CTOs and infrastructure leads carrying estate cost, and program boards that cannot afford a failed migration.",
    "hub_hero": "Achala's Cloud, Edge & Platform Engineering domain modernizes the estate your business runs on. Eight practices cover hybrid multicloud, edge fleets, cloud-native rebuilds, SRE discipline and mission-critical systems — every move gated by reconciliation, every platform owned.",
    },
    "Cybersecurity & Zero-Trust": {
        "promise": "zero-trust controls deployed with the evidence pack attached",
        "value": "Achala implements security your auditors can walk alone: control tests that run continuously, findings filed automatically, frameworks mapped to ISO 27001, SOC 2, TISAX and NIS2. Security posture becomes something you show, not something you claim.",
        "cta": "Bring one threat model to an Achala briefing. We will show the control set, the test regime and the evidence pack it generates.",
            "who": "CISOs and audit committees, and program owners facing TISAX, HIPAA or NIS2 scrutiny.",
    "hub_hero": "Achala's Cybersecurity & Zero-Trust domain protects people, machines and models. Eight practices cover zero-trust architecture, AI security, governance and testing — controls deployed with continuous evidence, built for regulated estates from banking to automotive supply chains.",
    },
    "Data, Analytics & Lakehouse": {
        "promise": "data platforms your finance team, your risk team and your auditors all trust",
        "value": "Achala builds lakehouses with data contracts: producers and consumers agree on schema and quality, breaks are caught at the boundary, and every table carries an owner and a freshness target. Decisions downstream become defensible.",
        "cta": "Bring one data domain to an Achala briefing. We will show the contract, the pipeline design and the cost picture it would run under.",
            "who": "CDOs and finance leaders who need numbers both sides sign, and teams tired of disputed data.",
    "hub_hero": "Achala's Data, Analytics & Lakehouse domain turns scattered data estates into decision-grade platforms. Eight practices cover lakehouse architecture, streaming, migration factories and decision products — governed so well that finance signs the numbers without a meeting.",
    },
    "IoT, Digital Twin & Robotics": {
        "promise": "sensor data turned into operational decisions, with the safety discipline physical systems demand",
        "value": "Achala connects devices, twins and control loops with rollback built in: firmware staged and signed, actuation authorized and logged, model drift measured against reality. Physical operations get software-grade discipline.",
        "cta": "Bring one production line or asset class to an Achala briefing. We will show the twin, the control loop and the safety gates it runs behind.",
            "who": "plant, fleet and device operations leaders, and engineering heads accountable for safe actuation.",
    "hub_hero": "Achala's IoT, Digital Twin & Robotics domain closes the loop between sensors and action. Eight practices cover industrial IoT fabrics, twin platforms, vision systems and connected devices — engineered for plants, fleets and hospitals where actuation must be safe.",
    },
    "Quantum & Advanced Compute": {
        "promise": "advanced compute evaluated honestly against the best classical baseline, before you commit budget",
        "value": "Achala benchmarks every candidate method against a tuned classical solver on your data, and publishes the ledger — result, hardware, cost. Where quantum wins, you invest with confidence; where it does not, you know before the money is spent.",
        "cta": "Bring one optimization problem to an Achala briefing. We will show the benchmark plan, the baseline and the go/no-go criteria.",
            "who": "strategy and innovation leaders evaluating emerging compute, and CFOs who want evidence before spend.",
    "hub_hero": "Achala's Quantum & Advanced Compute domain evaluates emerging compute with investor discipline. Eight practices cover problem formulation, benchmarking, quantum-inspired optimization and workload placement — every recommendation backed by a reproducible run ledger.",
    },
}

# ── hand-authored industry voices (12) ──────────────────────────────────────
INDUSTRIES = {
    "Agriculture & Food Systems": {
        "hook": "seasonality leaves no room for guesswork: input costs, yields and quality decisions all land in a narrow window",
        "cap": "Achala brings production AI to the farm gate — from input planning and precision agronomy to cold-chain and compliance — with results measured per hectare.",
        "hub_hero": "Agriculture and food businesses run on narrow windows: sow, spray, harvest, ship. Achala's programs for Agriculture & Food Systems put data and AI behind those windows — input cost decisions, precision agronomy at cooperative scale, cold-chain visibility and food-safety compliance — with published results like input cost per hectare down 14%.",
        "case_ctx": "Agricultural operations live by the season: one wrong input decision or one cold-chain gap shows up in yield, quality or compliance. The Achala team started where that cost concentrates —",
    },
    "Banking & Financial Services": {
        "hook": "every decision is regulated, every millisecond is margin, and every audit trail has to be complete",
        "cap": "Achala builds for DORA-era banking: decision platforms, KYC in about 5 minutes, fraud and credit models with replay — evidence that satisfies the regulator in minutes, not weeks.",
        "hub_hero": "Banking runs on trust and milliseconds. Achala's programs for Banking & Financial Services cover instant-payment decisioning, fraud control, KYC onboarding in about 5 minutes and regulated reporting — built for DORA and model-risk expectations, with decision replay that satisfies the regulator in minutes.",
        "case_ctx": "Banking margins live between risk and speed: approve too slowly and the customer leaves, approve too fast and the losses follow. The Achala program started where that tension is sharpest —",
    },
    "Education & Research": {
        "hook": "student experience and research output both depend on systems that simply work at term-start scale",
        "cap": "Achala supports universities and EdTech platforms with systems that survive enrolment peaks — portals, analytics and AI services under GDPR-aligned delivery.",
        "hub_hero": "Education runs on calendars, not quarters: enrolment peaks, exam cycles and grant deadlines decide everything. Achala's programs for Education & Research deliver student portals, learning platforms and research data infrastructure that hold up at term-start scale, under GDPR-aligned delivery.",
        "case_ctx": "Education institutions feel technology failures at enrolment and results time, when volume spikes and patience does not. The Achala program started with the peak load —",
    },
    "Energy & Utilities": {
        "hook": "the grid does not forgive latency: forecasting, balancing and asset decisions all carry physical consequences",
        "cap": "Achala brings production AI to grid forecasting, asset health and field operations under NERC CIP discipline — decisions with physical consequences, made defensibly.",
        "hub_hero": "Energy and utilities balance physics, regulation and margin in real time. Achala's programs for Energy & Utilities cover grid forecasting, asset health, field workforce systems and NERC CIP-aligned security — AI with physical consequences, engineered to be defensible.",
        "case_ctx": "Utility operations carry physical consequence: a forecasting miss or an asset failure cascades fast. The Achala program started where that consequence concentrates —",
    },
    "Healthcare & Life Sciences": {
        "hook": "patient outcomes and regulatory scrutiny arrive together, so every system has to be fast and defensible",
        "cap": "Achala runs hospital-scale platforms under HIPAA-grade discipline — emergency response at 50,000+ daily cases, laboratory queues down 20-30%, telemedicine and patient portals in production.",
        "hub_hero": "Healthcare technology has to be fast and defensible at the same time. Achala's programs for Healthcare & Life Sciences run at state scale today: emergency response for 50,000+ daily cases, patient portals that cut laboratory queues 20-30%, telemedicine and assistive devices — all under HIPAA-grade and GxP-aware delivery.",
        "case_ctx": "Hospitals feel technology gaps in patient waiting times and staff overtime, both visible within a quarter. The Achala program started with the patient journey —",
    },
    "Insurance & Risk": {
        "hook": "pricing, claims and capital decisions all need model governance that Solvency II reviewers accept",
        "cap": "Achala builds claims triage, pricing and underwriting platforms with model-risk documentation built in — Solvency II-aligned, with decisions auditors can walk alone.",
        "hub_hero": "Insurance decisions compound: pricing shapes the book, claims shape the loss ratio, and both need governance Solvency II reviewers accept. Achala's programs for Insurance & Risk cover claims triage, pricing platforms, fraud detection and model governance — decision platforms with the documentation already in them.",
        "case_ctx": "Insurers feel process gaps in loss adjustment expense and customer churn, both of them slow, both of them measurable. The Achala program started with the claims journey —",
    },
    "Logistics & Supply Chain": {
        "hook": "margin hides in routing, dwell time and fleet utilization — and never sits still",
        "cap": "Achala builds routing, telematics and warehouse decision systems with measured utilization gains — up to 40% workforce efficiency in published fleet deployments.",
        "hub_hero": "Logistics margin hides in routing, dwell and utilization, and it never sits still. Achala's programs for Logistics & Supply Chain cover fleet telematics with up to 40% efficiency gains, warehouse decision systems and cross-border visibility under C-TPAT — measured per route, per shift.",
        "case_ctx": "Logistics operations lose money in the gaps: idle fleets, dwell time and manual re-planning. The Achala program started with the route economics —",
    },
    "Manufacturing & Industrial": {
        "hook": "the plant floor punishes latency twice: once in throughput, once in quality",
        "cap": "Achala connects plant data to decisions under IEC 62443 discipline — twin-based optimization, vision quality systems and maintenance prediction in production.",
        "hub_hero": "Manufacturing punishes latency twice: throughput first, quality second. Achala's programs for Manufacturing & Industrial connect plant data to decisions — digital twins, vision-based quality systems, predictive maintenance — deployed under IEC 62443 discipline with actuation that can be rolled back.",
        "case_ctx": "Plants feel data gaps in scrap rates and unplanned downtime, both traceable to decisions made hours earlier. The Achala program started at the line —",
    },
    "Public Sector & Government": {
        "hook": "citizen services run at population scale under procurement and audit rules that exclude improvisation",
        "cap": "Achala delivers citizen-facing platforms and emergency systems at state scale — 50,000+ daily cases in production — under FedRAMP-style audit discipline.",
        "hub_hero": "Public-sector technology runs at population scale under rules that exclude improvisation. Achala's programs for Public Sector & Government deliver citizen service platforms and emergency response systems — one deployment handles 50,000+ daily cases across 9 states — with audit discipline throughout.",
        "case_ctx": "Public services feel technology gaps at the counter, where waiting times are political. The Achala program started with the citizen journey —",
    },
    "Retail & Consumer Goods": {
        "hook": "pricing, availability and experience decisions repeat thousands of times a day, per store",
        "cap": "Achala builds pricing, assortment and store-operations decision systems under PCI DSS — decisions per store, per day, measured on margin.",
        "hub_hero": "Retail decisions repeat thousands of times a day per store: price, replenish, staff, promote. Achala's programs for Retail & Consumer Goods build the decision systems behind those repeats — pricing, assortment, store operations and loyalty — under PCI DSS, measured on margin.",
        "case_ctx": "Retail chains feel decision gaps in margin per store, visible in the weekly numbers. The Achala program started with the pricing and availability flow —",
    },
    "Technology & SaaS": {
        "hook": "release velocity is the business model, so platform reliability is a revenue line",
        "cap": "Achala builds the platforms and SRE discipline product companies sell on — SOC 2 and ISO 27001 aligned, release-safe by design.",
        "hub_hero": "For technology and SaaS companies, release velocity is the business model and platform reliability is a revenue line. Achala's programs for Technology & SaaS cover cloud-native rebuilds, SRE discipline, data platforms and AI features — SOC 2 and ISO 27001 aligned, shipped release-safe.",
        "case_ctx": "Product companies feel platform gaps in churn and support cost, both visible in cohort data. The Achala program started with the release pipeline —",
    },
    "Telecom, Media & Entertainment": {
        "hook": "subscriber experience is decided in milliseconds, at national scale",
        "cap": "Achala builds network-adjacent decision systems and subscriber platforms under NIS2 — personalization, credit control and capacity decisions at streaming speed.",
        "hub_hero": "Telecom and media decisions happen in milliseconds at national scale: capacity, credit control, personalization, content delivery. Achala's programs for Telecom, Media & Entertainment build those decision systems under NIS2 — latency-bounded, subscriber-aware and measurable.",
        "case_ctx": "Operators feel decision gaps in churn and support volume, both visible in monthly cohorts. The Achala program started with the subscriber journey —",
    },
}

# ── small hand templates per page type ──────────────────────────────────────
def meta_of(hero):
    s = hero.split(". ")[0].strip()
    return s if s.endswith(".") else s + "."

HERO_VARIANTS = [
    "{title} from Achala IT Solutions: {promise}. Part of the {domain} domain — 54 practices, one delivery standard, every engagement measured against a signed business baseline.",
    "{title} is one of the 54 Achala practices in the {domain} domain: {promise}. The team that scopes your program is the team that industrializes it — under the same delivery standard as every Achala engagement.",
]
CTA_VARIANTS = [
    "{cta}",
    "{cta} The first session costs nothing but the hour.",
]

def clean_meta(m):
    return (m or "").strip()

def apply_service(page, row):
    dom = row.get("l2") or ""
    v = DOMAINS.get(dom) or DOMAINS["Applied AI & Generative AI"]
    title = page["title"]
    h = HERO_VARIANTS[hash(title) % 2].format(title=title, promise=v["promise"], domain=dom)
    cta = CTA_VARIANTS[hash(title) % 2].format(cta=v["cta"])
    return {"hero": h, "meta": meta_of(h), "intro_p": f"{title} is delivered by an Achala practice team that stays through industrialization. " + v["value"] + " Who this is for: " + v["who"], "cta": cta}

def apply_hub(page, row):
    dom = row.get("l2") or row.get("title") or ""
    v = DOMAINS.get(dom) or DOMAINS["Applied AI & Generative AI"]
    return {"hero": v["hub_hero"], "meta": meta_of(v["hub_hero"])}

def apply_industry_hub(page, row):
    ind = row.get("l2") or ""
    v = INDUSTRIES.get(ind)
    if not v:
        return None
    return {"hero": v["hub_hero"], "meta": meta_of(v["hub_hero"])}

def apply_capability(page, row):
    ind = row.get("l2") or ""
    sub = row.get("l3") or ""
    cap = row.get("l4") or page["title"]
    v = INDUSTRIES.get(ind)
    if not v:
        return None
    if row.get("template") == "industry_capability":
        h = f"{ind}: {cap} that ships. Achala runs {cap} as a production discipline for this sector — {v['hook']}."
        p = f"{cap} in {ind} is delivered by an Achala practice team that stays through industrialization: {v['cap']} The baseline is signed before delivery starts, and the gates evidence every move."
        return {"hero": h, "meta": meta_of(h), "first_p": p}
    if row.get("template") == "sub_capability":
        h = f"{sub} in {ind}: {cap} as a production discipline. Achala tailors {cap} to the {sub.lower()} reality — {v['hook']}."
        p = f"Inside {sub}, Achala runs {cap} under the same delivery standard as every engagement: {v['cap']} The baseline is signed before delivery starts."
        return {"hero": h, "meta": meta_of(h), "first_p": p}
    h = f"{sub} in {ind} — an Achala sector brief. {v['hook']} This page maps the workflows, systems of record and Achala capabilities that apply here."
    p = f"Achala covers {sub} through the {ind.lower()} program stack: {v['cap']} The capability pages below take you one level deeper."
    return {"hero": h, "meta": meta_of(h), "first_p": p}

def apply_case(page, row):
    ind = row.get("l2") or ""
    v = INDUSTRIES.get(ind)
    if not v:
        return None
    client = row.get("l3") or page["title"]
    return {"case_p": f"{client}: " + v["case_ctx"].rstrip() + ". The baseline signed in week two made the cost visible in units the finance team already owns, and the engagement ran under the standard Achala charter — a named metric, a named control owner and gates that evidence every move."}

def apply_insight(page, row):
    t = page["title"]
    h = f"{t} — an Achala delivery-floor perspective. Written by the practice that ran the work: what shipped, what scaled and the vendor questions worth asking before you commit."
    return {"hero": h, "meta": meta_of(h)}

def apply_insight_cat(page, row):
    t = row.get("l2") or page["title"]
    h = f"{t} — viewpoints from the Achala delivery floor. Each piece takes a position, shows where it breaks in practice and names the questions to ask any vendor, including us."
    return {"hero": h, "meta": meta_of(h)}

def apply_solution(page, row):
    t = page["title"]
    ind = row.get("l2") or ""
    h = f"{t} — an Achala packaged solution: a named business problem, a composed architecture from two to four service domains, and a value case written in units a CFO recognizes. Sized and piloted in weeks, measured on the metric it exists to move."
    return {"hero": h, "meta": meta_of(h)}

def apply_consulting(page, row):
    t = page["title"]
    h = f"{t} from Achala IT Solutions: advisory that ends in a delivered system. The team that recommends is the team that builds — one two-week diagnostic, one signed baseline, delivery under the same gates as every Achala expertise domain."
    p = f"{t} runs on a fixed rhythm at Achala: a two-week diagnostic that makes the cost visible, a baseline both sides sign, and delivery through the same evidence gates as our platform programs. No advice without ownership of the outcome."
    return {"hero": h, "meta": meta_of(h), "first_p": p}

def apply_partner(page, row):
    t = page["title"]
    h = f"{t} — validated in delivery with Achala. Alliance programs earn their place by working inside Achala engagements: joint reference architectures, shared support paths and results clients can check."
    return {"hero": h, "meta": meta_of(h)}

def apply_leadership(page, row):
    p = (page.get("profile") or {})
    name = p.get("name") or page["title"]
    role = p.get("role") or row.get("l2") or "leadership"
    h = f"{name} leads {role} at Achala IT Solutions — practicing delivery first, then leading it. The profile below covers focus areas, programs overseen and how to reach the desk."
    return {"hero": h, "meta": meta_of(h)}

def apply_newsroom(page, row):
    t = page["title"]
    h = f"{t} — official Achala IT Solutions newsroom. Announcements here reflect what has shipped or been certified, with dates and sources, in the company's own words."
    return {"hero": h, "meta": meta_of(h)}

def apply_approach(page, row):
    h = "The Achala delivery method, page by page: the diagnostic that makes cost visible, the baseline both sides sign, the gates that bind every move and the evidence that travels with the program. One standard, all domains."
    return {"hero": h, "meta": meta_of(h)}

def apply_company(page, row):
    t = page["title"]
    if "values" in (row.get("url") or ""):
        h = "The values Achala hires on and reviews against: delivery ownership, evidence over claims, client data protected as if it were our own, and respect across a 300+ person, three-country team."
        return {"hero": h, "meta": meta_of(h)}
    if "global-offices" in (row.get("url") or ""):
        h = "Achala IT Solutions delivers from Hyderabad (India), Munich (Germany) and Sofia (Bulgaria) — one delivery standard across three countries, with the Achala Sulzer partnership giving European clients fair-shoring continuity."
        return {"hero": h, "meta": meta_of(h)}
    return None

HANDLERS = {
    "service_page": apply_service,
    "expertise_hub": apply_hub,
    "industry_hub": apply_industry_hub,
    "industry_capability": apply_capability,
    "sub_capability": apply_capability,
    "subindustry_page": apply_capability,
    "case_study": apply_case,
    "insight_article": apply_insight,
    "insights_category": apply_insight_cat,
    "solution_page": apply_solution,
    "consulting_service": apply_consulting,
    "partner_page": apply_partner,
    "leadership_profile": apply_leadership,
    "newsroom_article": apply_newsroom,
    "approach_page": apply_approach,
    "company_page": apply_company,
}

def rewrite(path):
    d = json.load(open(path, encoding="utf-8"))
    spec = HANDLERS.get(d.get("template"))
    if not spec:
        return False
    row = {"l1": d.get("l1"), "l2": d.get("l2"), "l3": d.get("l3"), "l4": d.get("l4"), "url": d.get("url"), "title": d.get("title"), "template": d.get("template")}
    repl = spec(d, row)
    if not repl:
        return False
    blocks = d.get("blocks", [])
    changed = False
    # hero
    if "hero" in repl and blocks and blocks[0].get("t") == "hero":
        blocks[0]["x"] = repl["hero"]; changed = True
    # intro paragraph(s)
    if "intro_p" in repl:
        for b in blocks:
            if b.get("t") == "p":
                b["x"] = repl["intro_p"]; changed = True
                break
    if "first_p" in repl:
        # replace the first p after the first h2 (or the first p if no h2 yet)
        seen_h2 = False
        for b in blocks:
            if b.get("t") == "h2":
                seen_h2 = True
                continue
            if b.get("t") == "p" and (seen_h2 or blocks[0].get("t") != "hero"):
                b["x"] = repl["first_p"]; changed = True
                break
    if "case_p" in repl:
        # first p after the first h2, whatever it is titled
        seen_h2 = False
        for b in blocks:
            if b.get("t") == "h2":
                seen_h2 = True
                continue
            if seen_h2 and b.get("t") == "p":
                b["x"] = repl["case_p"]; changed = True
                break
    # cta
    if "cta" in repl and blocks and blocks[-1].get("t") == "cta":
        blocks[-1]["x"] = repl["cta"]; changed = True
    if "meta" in repl and repl["meta"]:
        d["meta_description"] = repl["meta"]; changed = True
    if changed:
        d["words"] = sum(len(str(v).split()) for b in blocks for v in [b.get("x", ""), json.dumps(b.get("items", "")), json.dumps(b.get("rows", ""))])
        json.dump(d, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        stats["n"] += 1
        stats["types"][d["template"]] = stats["types"].get(d["template"], 0) + 1
    return changed

for fn in sorted(os.listdir(PAGES)):
    if fn.endswith(".json"):
        rewrite(os.path.join(PAGES, fn))

print("rewritten:", stats["n"])
for k, v in sorted(stats["types"].items(), key=lambda x: -x[1]):
    print(f"  {v:4} {k}")
