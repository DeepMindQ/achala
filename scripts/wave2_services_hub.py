#!/usr/bin/env python3
"""Wave 2 — Services hub content rebuild (approved change register, services-hub portion).

Implements the approved change themes for /services/:
  W2-01  Buyer+proof H1 & lede (hero rewrite)
  W2-02  Domain table gains a concrete "Flagship build" column (real published cases)
  W2-03  NEW unique hub architecture — eight domains composing on one governed spine
         (every node carries its managed metric; edges carry real handoffs)
  W2-04  NEW engagement console (idash) — KPI tiles + 3 domain-language tabs
  W2-05  Sector-depth heatmap recast + non-empty note (counts reconciled to 336 briefs)
  W2-06  NEW interactive industry selector (12 industries × cross-domain engagement view)
  W2-07  Engagement ladder tightened (kept)
  W2-08  Operating contract: clause cards (bullets) + patent-neutral method paragraph
  W2-09  NEW buyer FAQ (4 Q&A, question-shaped) + FAQ JSON-LD for services_hub
  W2-10  Outcome-framed unique CTA
  W2-11  Domain cards: practice/brief count chips + metric-bearing descriptions
  W2-12  Related rail + evidence wiring (anonymized builds, verified URLs)
Also: FAQ JSON-LD rule fixed site-wide (question-shaped bullets only).

Outputs:
  - scripts/wave2_baseline_services_hub.json   (before-state snapshot)
  - scripts/wave2_register.json                (change register for traceability)
  - site/src/content/pages/services.json       (rebuilt)
"""
import json, re, sys
from pathlib import Path

SITE = Path("/home/z/my-project/site")
REF = json.load(open("/home/z/my-project/scripts/wave2_hub_ref.json"))
PAGES = SITE / "src/content/pages"
OUT = PAGES / "services.json"

current = json.load(open(OUT))
json.dump(current, open("/home/z/my-project/scripts/wave2_baseline_services_hub.json", "w"), indent=1)

# ── grounding data ────────────────────────────────────────────────────────
def dom(slug):
    """domain explorer entries keyed by industry slug"""
    return REF[slug]

def kpi(slug, domain, idx):
    return dom(domain)[slug]["kpis"][idx]

INDUSTRY_HUBS = REF["_industry_hubs"]  # name -> url

DOMAIN_SLUGS = {
    "Applied AI & Generative AI": "applied-ai-generative-ai",
    "Agentic AI & Hyperautomation": "agentic-ai-hyperautomation",
    "Data, Analytics & Lakehouse": "data-analytics-lakehouse",
    "Cybersecurity & Zero-Trust": "cybersecurity-zero-trust",
    "Cloud, Edge & Platform Engineering": "cloud-edge-platform-engineering",
    "Quantum & Advanced Compute": "quantum-advanced-compute",
    "Blockchain & Digital Trust": "blockchain-digital-trust",
    "IoT, Digital Twin & Robotics": "iot-digital-twin-robotics",
}
PRACTICE_COUNTS = {
    "Applied AI & Generative AI": 7, "Agentic AI & Hyperautomation": 7,
    "Data, Analytics & Lakehouse": 7, "Cybersecurity & Zero-Trust": 7,
    "Cloud, Edge & Platform Engineering": 7, "Quantum & Advanced Compute": 6,
    "Blockchain & Digital Trust": 6, "IoT, Digital Twin & Robotics": 7,
}

# per-domain sector-brief counts — recomputed from the heatmap block (real page counts)
heat = next(b for b in current["blocks"] if b["t"] == "chart" and b.get("variant") == "heatmap")
HEAT_CATS = heat["cats"]                     # 12 industries, in order
HEAT_SERIES = heat["series"]                 # 8 domains, points aligned to cats
DOMAIN_ORDER = [s["name"] for s in HEAT_SERIES]
SUB_BRIEFS = sum(sum(s["points"]) for s in HEAT_SERIES)   # sub-industry-level briefs (240)
# industry-level capability pages: /industries/<ind>/capabilities/<dom>/ (1 per industry × domain)
IND_LEVEL = 0
for f in PAGES.glob("*.json"):
    u = json.load(open(f)).get("url", "")
    if re.fullmatch(r"/industries/[^/]+/capabilities/[^/]+/", u):
        IND_LEVEL += 1
TOTAL_BRIEFS = SUB_BRIEFS + IND_LEVEL
domain_briefs = {s["name"]: sum(s["points"]) for s in HEAT_SERIES}
industry_briefs = {c: sum(s["points"][i] for s in HEAT_SERIES) for i, c in enumerate(HEAT_CATS)}
assert SUB_BRIEFS == 240 and IND_LEVEL == 96 and TOTAL_BRIEFS == 336, \
    f"brief counts drifted: sub={SUB_BRIEFS} ind-level={IND_LEVEL} total={TOTAL_BRIEFS}"

# case evidence per industry (verified against the page index below)
CASES = {
    "banking-financial-services": [("A top-10 European retail bank", "/case-studies/bank-01/"), ("A tier-1 US bank", "/case-studies/bank-03/")],
    "insurance": [("A top-5 global P&C insurer", "/case-studies/ins-01/"), ("A leading life insurer (North America)", "/case-studies/ins-02/")],
    "healthcare-life-sciences": [("A 12-hospital US health system", "/case-studies/hc-01/"), ("A European biopharma group", "/case-studies/hc-03/")],
    "manufacturing": [("A global automotive OEM", "/case-studies/mfg-01/"), ("A specialty chemicals producer", "/case-studies/mfg-02/")],
    "retail-consumer-goods": [("A top-3 grocery retailer (800+ stores)", "/case-studies/ret-01/"), ("A global fashion group", "/case-studies/ret-02/")],
    "telecom-media": [("A tier-1 European operator", "/case-studies/tel-01/"), ("A North American cable operator", "/case-studies/tel-03/")],
    "energy-utilities": [("A European TSO-DSO group", "/case-studies/en-01/"), ("A global integrated energy major", "/case-studies/en-02/")],
    "logistics-supply-chain": [("A global 3PL (40+ countries)", "/case-studies/log-01/"), ("A parcel network (12M parcels/week)", "/case-studies/log-03/")],
    "public-sector": [("A national digital-government agency", "/case-studies/pub-01/"), ("A national tax administration", "/case-studies/pub-02/")],
    "education-research": [("A public research university (38,000 students)", "/case-studies/edu-01/"), ("A national EdTech platform (2M learners)", "/case-studies/edu-02/")],
    "technology-saas": [("A B2B SaaS platform (Series D)", "/case-studies/tech-01/"), ("A global gaming studio (live-service title, 15M MAU)", "/case-studies/tech-03/")],
    "agriculture-food": [("A European agri-cooperative (4,200 farms)", "/case-studies/agr-01/"), ("A global coffee trader", "/case-studies/agr-03/")],
}

# ── the industry selector: 12 cross-domain engagement views ───────────────
# kpis = (domain_slug, index) picks; plays reference each domain's published targets
INDUSTRIES = [
 dict(slug="banking-financial-services", flagship=True,
  hook=("KYC refresh backlogs, sanctions-alert triage and reconcile-everything month-ends run on a regulator's clock, not yours. "
        "We ground the advisory layer, automate the operations layer and lock the audit layer on one governed spine — so the model that advises, the agent that acts and the ledger that proves it share the same controls."),
  kpis=[("agentic-ai-hyperautomation", 0), ("cybersecurity-zero-trust", 0), ("applied-ai-generative-ai", 1)],
  plays=["Applied AI: a grounded advisory assistant whose every policy answer carries a citation your risk team accepts — 99% citation coverage at 5 s p95",
         "Agentic AI: straight-through processing on agent-handled operations with logged kill reasons — 69% STP at $0.24 per completed action",
         "Cybersecurity & Digital Trust: critical-threat containment in 15 minutes and hash-linked evidence packs produced in minutes, not weeks"],
  systems=["KYC/case suites and watchlist tools", "SWIFT gpi and payment-rail events", "SR 11-7 / OCC 2011-12 evidence"]),
 dict(slug="insurance", flagship=True,
  hook=("FNOL intake, submission triage and reserve refresh surge at catastrophe season while adjusters keep the judgment calls. "
        "We automate the document-heavy front end, ground the policy-wording citations and attest the payouts — every step logged for market-conduct exam."),
  kpis=[("agentic-ai-hyperautomation", 0), ("applied-ai-generative-ai", 0), ("blockchain-digital-trust", 0)],
  plays=["Agentic AI: claims auto-adjudicated all the way to settlement — 67% straight-through with a 19% adjuster override rate",
         "Applied AI: submission auto-summaries underwriters actually adopt — 50% adoption with 100% wording-citation fidelity",
         "Blockchain & Digital Trust: parametric payouts released on attested events — 99% with 85% claims-provenance coverage"],
  systems=["ACORD-coded PAS queues and FNOL channels", "Telematics feeds and repair-network APIs", "State DOI market-conduct exam files"]),
 dict(slug="healthcare-life-sciences", flagship=True,
  hook=("Prior-authorization queues, trial-document review and cold-chain custody run against HIPAA and GxP clocks. "
        "We ground the clinical evidence, instrument the estate and gate every release — the safety interlocks test before any patient-facing change ships."),
  kpis=[("applied-ai-generative-ai", 2), ("iot-digital-twin-robotics", 1), ("data-analytics-lakehouse", 2)],
  plays=["Applied AI: prior-auth packets assembled in 9 minutes with 100% PHI-redaction coverage and 79% clinician acceptance",
         "IoT & Digital Twin: cold-chain twins at 93% fidelity with excursion alerts that arrive on time, 100% of the time",
         "Data & Lakehouse: a PHI-governed clinical layer with zero purpose-limit violations and a 99% freshness SLA"],
  systems=["EHR/RCM queues and clearinghouse loops", "Cold-chain sensors and LIMS records", "HIPAA privacy-rule and GxP Part-11 evidence"]),
 dict(slug="manufacturing", flagship=True,
  hook=("Unplanned line stops, NCR backlogs and recall drills that cannot reconstruct history in hours. "
        "We instrument the plant, disposition the work orders with agents and seal every action into an evidence packet your auditor can replay."),
  kpis=[("applied-ai-generative-ai", 0), ("iot-digital-twin-robotics", 0), ("cybersecurity-zero-trust", 0)],
  plays=["Applied AI: document extraction at 92% first-pass accuracy and root-cause search time cut by 48%",
         "IoT & Robotics: capture fidelity at 97% across lines with twins that hold 98% accuracy after changeovers",
         "Cybersecurity & Zero-Trust: 100% of IT-OT crossings under explicit control with zero line-impact incidents per quarter"],
  systems=["MES/SCADA historians and NCR queues", "Line PLCs, vision sensors and edge gateways", "ISO 9001 / IATF 16949 audit evidence"]),
 dict(slug="retail-consumer-goods", flagship=False,
  hook=("Peak trade punishes fragile stacks, deduction disputes eat margin, and provenance claims need proof. "
        "We harden the store edge, resolve the exceptions with agents and anchor the provenance claims your regulators and customers both check."),
  kpis=[("applied-ai-generative-ai", 0), ("agentic-ai-hyperautomation", 0), ("iot-digital-twin-robotics", 0)],
  plays=["Applied AI: dialog containment at 44% with 84% CSAT on contained sessions and dignified escalation quality at 91%",
         "Agentic AI: PO exceptions auto-resolved at 63% with 100% of agent actions reconciled back to ERP",
         "IoT & Robotics: shelf-vision accuracy at 91% per store feeding a demand signal store-hour decisions trust"],
  systems=["POS/ERP estate and deduction workbenches", "Store-edge cameras and shelf sensors", "PCI-DSS scope and provenance-claim audits"]),
 dict(slug="telecom-media", flagship=False,
  hook=("Order fallout, streaming decision latency and OSS/BSS change risk define the margin. "
        "We recover the fallout with agents, decide on the stream in milliseconds and pin the change windows with drill-tested controls."),
  kpis=[("agentic-ai-hyperautomation", 0), ("data-analytics-lakehouse", 0), ("cloud-edge-platform-engineering", 0)],
  plays=["Agentic AI: order fallout auto-recovered at 67% with repeat fallout held to a 5% rate",
         "Data & Lakehouse: streaming decisions at 361 ms p99 with an exactly-once decision audit",
         "Cloud, Edge & Platform: latency budgets met per tier at 93% with OSS workload MTTR at 14 minutes"],
  systems=["OSS/BSS stacks and order orchestration", "Network telemetry and edge fleet", "Service-assurance audit calendars"]),
 dict(slug="energy-utilities", flagship=False,
  hook=("OT zones must never share fate with IT, procedures must surface at the point of work, and regulators reconstruct decisions. "
        "We segment the estate, ground the field procedures and twin the assets — with the reconstruction clock measured in minutes."),
  kpis=[("applied-ai-generative-ai", 0), ("iot-digital-twin-robotics", 1), ("cybersecurity-zero-trust", 0)],
  plays=["Applied AI: procedure retrieval at the point of work, 84% — with version-stale answers blocked at 100%",
         "IoT & Digital Twin: asset-twin state fidelity at 96% driving an 83% work-order auto-creation rate",
         "Cybersecurity & Zero-Trust: 100% OT-zone policy compliance with zero segmentation violations on record"],
  systems=["OT historians and switch-order packets", "Substation edge and field identities", "NERC-CIP / ISO 27001 evidence packs"]),
 dict(slug="logistics-supply-chain", flagship=False,
  hook=("Detention disputes, EDI exceptions and customs calendars punish every unautomated handoff. "
        "We triage the exceptions with agents, anchor the EDI events at source and keep the control tower fresh enough to act on."),
  kpis=[("agentic-ai-hyperautomation", 0), ("data-analytics-lakehouse", 0), ("blockchain-digital-trust", 1)],
  plays=["Agentic AI: exceptions auto-triaged at 59% with detention disputes resolved inside 8 days",
         "Data & Lakehouse: control-tower event freshness at 4 s p95 with 96% carrier-message conformance",
         "Blockchain & Digital Trust: customs documents verified one-scan at 89% with dispute evidence packs at 100% coverage"],
  systems=["TMS/EDI networks and customs brokers", "Track-and-trace telematics", "Customs-calendar and trade-compliance files"]),
 dict(slug="public-sector", flagship=False,
  hook=("Statute-bound answers, citable decision trails and peak-day benefits availability — under public scrutiny. "
        "We ground the casework in the statute, assemble the cases for review and enforce the privacy domains by design."),
  kpis=[("applied-ai-generative-ai", 0), ("cloud-edge-platform-engineering", 0), ("blockchain-digital-trust", 0)],
  plays=["Applied AI: statute-bound answer coverage at 97% with a 100% citable decision trail and 39% caseworker research time returned",
         "Cloud, Edge & Platform: peak-day benefits availability at 99% with 100% residency-bound placement compliance",
         "Blockchain & Digital Trust: citizen-held credentials with 100% issuer audit-trail completeness"],
  systems=["Case-management suites and statute corpora", "Benefits platforms and citizen wallets", "Oversight and records-request evidence"]),
 dict(slug="education-research", flagship=False,
  hook=("Term-cycle identity churn, FERPA-class data walls and verification queues that stall admissions. "
        "We ground the advising, automate the verification packets and issue credentials employers can check in one scan."),
  kpis=[("blockchain-digital-trust", 0), ("applied-ai-generative-ai", 0), ("data-analytics-lakehouse", 1)],
  plays=["Blockchain & Digital Trust: credentials issued to wallet at 99% with one-scan employer verification at 94%",
         "Applied AI: adviser-grounded query resolution at 75% with academic-integrity guards enforced at 100%",
         "Data & Lakehouse: cohort metrics at 99% point-in-time correctness under 100% FERPA-class access compliance"],
  systems=["SIS/LMS estates and verification queues", "Campus identity and lab equipment", "FERPA / accreditation audit files"]),
 dict(slug="technology-saas", flagship=False,
  hook=("Support tickets, model abuse and infra burn rate compound at growth scale. "
        "We contain the conversations, gate the deploys with posture checks and price the platform per customer with honest unit costs."),
  kpis=[("cybersecurity-zero-trust", 1), ("cloud-edge-platform-engineering", 0), ("applied-ai-generative-ai", 0)],
  plays=["Cybersecurity & AI Security: posture gates blocking bad deploys at 96% with model-layer defense at 90% coverage",
         "Cloud, Edge & Platform: golden-path adoption at 69% with infra cost held at $1.13 per customer",
         "Applied AI: support containment at 48% with 100% eval-suite gate coverage before any answer ships"],
  systems=["Product telemetry and billing events", "CI/CD and model-serving estates", "SOC 2 / ISO 27001 control evidence"]),
 dict(slug="agriculture-food", flagship=False,
  hook=("Certification audits, subsidy dossiers and cold-chain custody decide whether produce moves or stalls. "
        "We anchor the certification events, prove the cold chain and price the platform per hectare so co-ops can actually run it."),
  kpis=[("blockchain-digital-trust", 0), ("iot-digital-twin-robotics", 1), ("cloud-edge-platform-engineering", 2)],
  plays=["Blockchain & Digital Trust: certification events anchored at source, 89% — with subsidy proof completeness at 97%",
         "IoT & Digital Twin: cold-chain certification evidence at 95% from field sensors at 95% capture fidelity",
         "Cloud, Edge & Platform: store-and-forward data survival at 97% at $0.09 data cost per hectare managed"],
  systems=["Co-op ERPs and certification bodies", "Field sensors and cold-chain loggers", "GlobalG.A.P. / subsidy-audit evidence"]),
]

def build_industries():
    out = []
    for spec in INDUSTRIES:
        slug = spec["slug"]
        name = next(e["name"] for e in (dom(d)[slug] for d in DOMAIN_SLUGS.values() if slug in dom(d)))
        kpis = []
        for dslug, idx in spec["kpis"]:
            k = kpi(slug, dslug, idx)
            kpis.append({"label": k["label"], "value": k["value"]})
        systems = spec["systems"]
        ev = [{"title": t, "url": u} for t, u in CASES[slug]]
        out.append({
            "slug": slug,
            "name": name,
            "flagship": spec["flagship"],
            "hook": spec["hook"],
            "plays": spec["plays"],
            "kpis": kpis,
            "capUrl": INDUSTRY_HUBS[name],
            "systems": systems,
            "evidence": ev,
        })
    return out

# ── idash widgets (grounded on domain-console values) ─────────────────────
def top_industry_briefs():
    rows = sorted(industry_briefs.items(), key=lambda kv: -kv[1])[:6]
    cats = [n for n, _ in rows]
    pts = [v for _, v in rows]
    return {"kind": "bar", "title": "Capability briefs published per industry — the depth is countable",
            "cats": cats, "series": [{"name": "Published briefs", "points": pts}]}

IDASH = {
    "t": "idash",
    "title": "The engagement console — what a governed program reports every week",
    "kpis": [
        {"label": "Practices in production", "value": "54", "delta": "across the eight domains", "dir": "up", "spark": [12, 20, 28, 36, 44, 50, 54]},
        {"label": "Portfolio containment", "value": "78%", "delta": "blended across agent fleets", "dir": "up", "spark": [52, 58, 64, 68, 72, 75, 78]},
        {"label": "Unplanned downtime", "value": "−58%", "delta": "instrumented fleets, YoY", "dir": "down", "spark": [0, -12, -24, -35, -47, -52, -58]},
        {"label": "Evidence freshness", "value": "97.4%", "delta": "audit packs, weekly cycle", "dir": "up", "spark": [88, 90, 92, 94, 95, 96, 97.4]},
        {"label": "Change failure rate", "value": "6%", "delta": "governed change tiers", "dir": "down", "spark": [14, 12, 11, 9, 8, 7, 6]},
    ],
    "tabs": [
        {"name": "Delivery quality", "widgets": [
            {"kind": "line", "title": "Gate pass rate vs rework — governed releases, eight quarters",
             "cats": ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8"],
             "series": [{"name": "First-pass gate clears, %", "points": [71, 74, 78, 81, 84, 86, 89, 91]},
                        {"name": "Rework returned, %", "points": [18, 16, 14, 12, 11, 10, 9, 8]}]},
            {"kind": "bar", "title": "Evidence-pack preparation by control family, days",
             "cats": ["Model risk", "Access reviews", "Change records", "Privacy", "Resilience"],
             "series": [{"name": "Days to produce", "points": [9, 6, 4, 5, 7]}]},
        ]},
        {"name": "Cost & cycle", "widgets": [
            {"kind": "line", "title": "Unit-cost trend, indexed to baseline = 100 — reference program",
             "cats": ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8"],
             "series": [{"name": "Cost per 1k calls", "points": [100, 94, 88, 81, 74, 69, 65, 62]},
                        {"name": "Cost per completed action", "points": [100, 92, 83, 74, 66, 58, 50, 44]},
                        {"name": "Infra cost per workload", "points": [100, 97, 94, 91, 89, 87, 86, 85]}]},
            {"kind": "bar", "title": "Cycle time, entry to production — the four rungs in weeks",
             "cats": ["Diagnostic", "Provability sprint", "Build slice", "Industrialization"],
             "series": [{"name": "Weeks", "points": [2, 4, 12, 6]}]},
        ]},
        {"name": "Sector coverage", "widgets": [
            top_industry_briefs(),
            {"kind": "line", "title": "Anonymized evidence builds published, cumulative",
             "cats": ["FY24 Q1", "FY24 Q2", "FY24 Q3", "FY24 Q4", "FY25 Q1", "FY25 Q2", "FY25 Q3", "FY25 Q4"],
             "series": [{"name": "Builds", "points": [34, 52, 71, 88, 98, 107, 112, 116]}]},
        ]},
    ],
    "note": "Reference-program console: values are blended from the eight domain consoles and carry the same provenance discipline — every number is illustrative until your diagnostic signs the baseline.",
}

# ── the hub architecture (unique to this page) ────────────────────────────
ARCH = {
    "t": "arch",
    "title": "One governed spine under eight domains — the composition enterprises actually buy",
    "lanes": ["Decide & act", "Feed & run", "Protect & prove", "Sense & compute", "The governed spine"],
    "nodes": [
        {"id": "applied", "lane": 0, "label": "Applied AI & GenAI", "hot": True, "sub": "grounded answer rate · cost per 1k calls"},
        {"id": "agentic", "lane": 0, "label": "Agentic AI", "hot": True, "sub": "automation coverage · checkpoint fidelity"},
        {"id": "data", "lane": 1, "label": "Data & Lakehouse", "hot": True, "sub": "freshness SLA · lineage completeness"},
        {"id": "cloud", "lane": 1, "label": "Cloud & Platform", "sub": "change failure rate · unit cost"},
        {"id": "cyber", "lane": 2, "label": "Cybersecurity", "hot": True, "sub": "containment time · evidence freshness"},
        {"id": "dlt", "lane": 2, "label": "Digital Trust", "sub": "reconciliation deltas · attestation coverage"},
        {"id": "iot", "lane": 3, "label": "IoT & Twin", "sub": "twin fidelity · freshness p95"},
        {"id": "quantum", "lane": 3, "label": "Quantum & HPC", "sub": "verified advantage · PQC coverage"},
        {"id": "baseline", "lane": 4, "label": "Signed baseline", "hot": True, "sub": "metric owner signs — no metric, no build"},
        {"id": "gates", "lane": 4, "label": "Named gates", "hot": True, "sub": "evidenced releases · named gate owners"},
        {"id": "evidence", "lane": 4, "label": "Audited evidence", "hot": True, "sub": "exit numbers finance can reconcile"},
        {"id": "scale", "lane": 4, "label": "Industrialize", "sub": "run-books · SRE · rung four"},
    ],
    "edges": [
        {"a": "applied", "b": "agentic", "label": "decision consumed by agents"},
        {"a": "data", "b": "applied", "label": "governed features feed models"},
        {"a": "iot", "b": "data", "label": "telemetry lands under contract"},
        {"a": "cyber", "b": "gates", "label": "deny-by-default policy"},
        {"a": "dlt", "b": "evidence", "label": "hash-linked attestations"},
        {"a": "cloud", "b": "scale", "label": "golden paths to rung four"},
        {"a": "quantum", "b": "cloud", "label": "hybrid scheduling"},
        {"a": "agentic", "b": "gates", "label": "releases clear checkpoints"},
        {"a": "applied", "b": "baseline", "label": "metric signed up front"},
        {"a": "data", "b": "evidence", "label": "lineage audited end-to-end"},
        {"a": "cyber", "b": "evidence", "label": "drill results archived"},
        {"a": "iot", "b": "scale", "label": "fleet run-books"},
    ],
    "badges": [
        {"label": "Expertise domains", "value": "8"},
        {"label": "Practices", "value": "54"},
        {"label": "Capability briefs", "value": str(TOTAL_BRIEFS)},
        {"label": "Evidence builds", "value": "116"},
    ],
    "note": "Left to right: the four working lanes are how enterprises buy — decide, feed, protect, sense. Every lane lands on the same governed spine, so whichever domain you enter, the signed-baseline → evidenced-gates → audited-exit contract holds.",
}

# ── domain table rows (with flagship builds from published cases) ─────────
DOMAIN_TABLE = {
    "t": "table",
    "caption": "The eight domains at a glance — size, the metric each is managed on, and a published build behind it",
    "headers": ["Expertise domain", "Practices", "Managed on", "Flagship build"],
    "rows": [
        ["Applied AI & Generative AI", "7", "Grounded answer rate, cost per 1k calls", "Grounded advisory assistant, top-10 European bank — 99% citation coverage"],
        ["Agentic AI & Hyperautomation", "7", "Automation coverage, human-checkpoint fidelity", "Claims auto-adjudication, top-5 global insurer — 67% straight to settlement"],
        ["Data, Analytics & Lakehouse", "7", "Freshness SLA, lineage completeness", "Streaming decisioning, tier-1 operator — 361 ms p99, exactly-once audit"],
        ["Cybersecurity & Zero-Trust", "7", "Containment time, evidence freshness", "OT-zone segmentation, European TSO-DSO — zero violations on record"],
        ["Cloud, Edge & Platform Engineering", "7", "Change failure rate, unit cost", "Peak-trade readiness, top-3 grocer — 100% availability across the peak"],
        ["Quantum & Advanced Compute", "6", "Verified advantage, PQC coverage", "Grid optimization screening, global energy major — 8% verified gain"],
        ["Blockchain & Digital Trust", "6", "Reconciliation deltas, attestation coverage", "Parametric payouts on attested events, top-5 insurer — 99%"],
        ["IoT, Digital Twin & Robotics", "7", "Twin fidelity, freshness p95", "Cold-chain twins, 12-hospital health system — 93% fidelity"],
    ],
}

# ── FAQ (question-shaped → feeds FAQ JSON-LD) ─────────────────────────────
FAQ = {
    "t": "bullets",
    "items": [
        ["Which domain owns our problem?", "Enter where the metric lives: a decision that gets better is Applied AI; work that stops leaking money is Agentic AI; data nobody trusts is Data & Lakehouse; proof your regulator accepts is Cybersecurity or Digital Trust. If the problem spans seams — most do — the hub architecture shows how the domains compose on one spine, and the briefing maps it for your estate."],
        ["What does the two-week diagnostic actually end with?", "A signed baseline, an estate map, a scored gate map for your controls and a build order with named owners. You keep the documents whichever way the engagement goes — that is deliberate, because the diagnostic is designed to be the cheapest way to price the truth."],
        ["Can we skip the ladder and start at build?", "Only when the evidence you already hold supports it: a verified baseline from an audit or a prior program can collapse the first rung. Nobody buys a large program on a hypothesis here — the provability sprint exists precisely so a fund-or-kill verdict arrives before a big commitment."],
        ["Where do the patented methods fit?", "Eight patented method families sit underneath the release gates. Where a family strengthens a gate, the service page names it and links the method map — so you can read what the method does without asking for a briefing first."],
    ],
}

# ── cards, related, evidence ───────────────────────────────────────────────
CARDS = [
    {"title": "Applied AI & Generative AI", "tag": f"{PRACTICE_COUNTS['Applied AI & Generative AI']} practices · {domain_briefs['Applied AI & Generative AI']} sector briefs",
     "desc": "Strategy to production models measured on the P&L — grounded answers with citations your risk team accepts, eval-gated before anything ships.", "url": "/services/applied-ai-generative-ai/"},
    {"title": "Agentic AI & Hyperautomation", "tag": f"{PRACTICE_COUNTS['Agentic AI & Hyperautomation']} practices · {domain_briefs['Agentic AI & Hyperautomation']} sector briefs",
     "desc": "Digital workers that recover from failure on their own — policy-bounded tool use, risk-placed human checkpoints and logs built for exam day.", "url": "/services/agentic-ai-hyperautomation/"},
    {"title": "Data, Analytics & Lakehouse", "tag": f"{PRACTICE_COUNTS['Data, Analytics & Lakehouse']} practices · {domain_briefs['Data, Analytics & Lakehouse']} sector briefs",
     "desc": "Trusted data in near real time — contracts on every metric, lineage that survives model-risk review and freshness your operations can run on.", "url": "/services/data-analytics-lakehouse/"},
    {"title": "Cybersecurity & Zero-Trust", "tag": f"{PRACTICE_COUNTS['Cybersecurity & Zero-Trust']} practices · {domain_briefs['Cybersecurity & Zero-Trust']} sector briefs",
     "desc": "Identity, detection, resilience and AI security as one program — containment measured in minutes, evidence packs that produce themselves.", "url": "/services/cybersecurity-zero-trust/"},
    {"title": "Cloud, Edge & Platform Engineering", "tag": f"{PRACTICE_COUNTS['Cloud, Edge & Platform Engineering']} practices · {domain_briefs['Cloud, Edge & Platform Engineering']} sector briefs",
     "desc": "Hybrid estates and internal platforms engineered for unit cost — golden paths your teams adopt and change windows that hold at peak.", "url": "/services/cloud-edge-platform-engineering/"},
    {"title": "Quantum & Advanced Compute", "tag": f"{PRACTICE_COUNTS['Quantum & Advanced Compute']} practices · {domain_briefs['Quantum & Advanced Compute']} sector briefs",
     "desc": "Quantum readiness, optimization and PQC migration — advantage claims verified against classical baselines, or they do not reach the board pack.", "url": "/services/quantum-advanced-compute/"},
    {"title": "Blockchain & Digital Trust", "tag": f"{PRACTICE_COUNTS['Blockchain & Digital Trust']} practices · {domain_briefs['Blockchain & Digital Trust']} sector briefs",
     "desc": "DLT networks, tokenization and verifiable credentials — a shared record whose attestations anchor audit and settle disputes in hours.", "url": "/services/blockchain-digital-trust/"},
    {"title": "IoT, Digital Twin & Robotics", "tag": f"{PRACTICE_COUNTS['IoT, Digital Twin & Robotics']} practices · {domain_briefs['IoT, Digital Twin & Robotics']} sector briefs",
     "desc": "Sensing, simulating, acting — physical assets turned into self-monitoring systems whose twins survive changeovers and audits alike.", "url": "/services/iot-digital-twin-robotics/"},
]

RELATED = [
    {"title": "The Achala Method", "url": "/our-approach/the-achala-method/", "tag": "Method", "desc": "The delivery method and gates behind the operating contract — read it before you compare proposals."},
    {"title": "Evidence library — 116 builds", "url": "/case-studies/", "tag": "Proof", "desc": "Anonymized builds with measured deltas, filterable by industry and service area."},
    {"title": "Industries", "url": "/industries/", "tag": "Sectors", "desc": "Twelve sector playbooks with the regulations, workflows and controls that bind them."},
    {"title": "Platforms", "url": "/platforms/", "tag": "Product estate", "desc": "The productized estate the practices deploy on — consoles, portals and reference architectures."},
    {"title": "Book a practice briefing", "url": "/book-a-briefing/", "tag": "Start here", "desc": "45 minutes with the practice lead — your metric, our method, a straight feasibility read."},
]

EVIDENCE = [
    {"title": "A top-10 European retail bank", "url": "/case-studies/bank-01/", "ind": "Banking & Financial Services"},
    {"title": "A global automotive OEM", "url": "/case-studies/mfg-01/", "ind": "Manufacturing & Industrial"},
    {"title": "A 12-hospital US health system", "url": "/case-studies/hc-01/", "ind": "Healthcare & Life Sciences"},
]

# ── narrative blocks ────────────────────────────────────────────────────────
H2_DIVIDE = {
    "t": "h2", "x": "How the eight domains divide the work",
    "sub": "Cut along the seams where enterprises actually buy — what decides, what acts, what feeds the decision, what protects it, what runs it — and the metric each domain is managed on.",
}
P_DIVIDE = ("Enterprises do not buy \"AI\" or \"cloud\"; they buy a decision that gets better, a process that stops leaking money, "
            "a platform that stops failing at peak, and proof their regulator will accept. The eight domains below are cut exactly on those "
            "seams, and each one is managed on the metric it exists to move. Read the table for the shape of each domain, the architecture "
            "for how they compose, and the console for what a governed program reports once it runs.")
H2_DEPTH = {
    "t": "h2", "x": "Where the sector depth sits — and how to read it",
    "sub": f"Published structure, not claims: {TOTAL_BRIEFS} written capability briefs across 12 industries × 8 domains — {IND_LEVEL} industry-level and {SUB_BRIEFS} sub-industry, each with workflows, controls and the regulation that binds them.",
}
P_DEPTH = ("Depth is a structure you can count. Every domain × industry pair carries one industry-level capability page — "+str(IND_LEVEL)+" in "
           "total — and the matrix below counts the deeper sub-industry briefs ("+str(SUB_BRIEFS)+" of them): each names the workflows we "
           "automate, the controls we evidence and the regulator who audits them. Use the matrix to see whether your sector's hard problems "
           "already have a written method here, then open the selector beneath it to turn any row into a concrete engagement view.")
HEATMAP = {
    "t": "chart", "variant": "heatmap",
    "title": "Published sector depth — capability briefs per domain × industry",
    "cats": HEAT_CATS,
    "series": HEAT_SERIES,
    "note": "Cell = count of sub-industry capability pages for that domain × industry (240 sub-industry briefs; the 96 industry-level pages complete the 336). The selector below turns any row into the concrete engagement behind the count.",
}
EXPLORER = {
    "t": "explorer",
    "title": "Pick your industry — see the engagement we would run",
    "intro": "Twelve industries, one selector. Each panel shows the entry problem we meet first, the cross-domain build we propose, the three targets we sign, the estate it lands on and the anonymized builds behind the numbers.",
    "service": "All eight domains",
    "practiceNote": "The targets shown are the flagship values each domain signs for in this sector — they reconcile to the domain pages, which carry the full gate map.",
    "industries": build_industries(),
}
H2_LADDER = {
    "t": "h2", "x": "The engagement ladder — four rungs, no leaps of faith",
    "sub": "Diagnostic, provability sprint, delivery slice, industrialization — enter at the rung your evidence supports.",
}
P_LADDER = ("Work enters at the rung that matches the evidence you already hold. The ladder is deliberately short: the provability sprint "
            "exists so that nobody buys a large program on a hypothesis, and the diagnostic exists so the first conversation is about your "
            "estate rather than our slideware. Each rung ends with artifacts you keep — the documents are the exit criteria, not a courtesy.")
LADDER_TABLE = next(b for b in current["blocks"] if b["t"] == "table" and b.get("headers", [""])[0] == "Rung")
H2_CONTRACT = {
    "t": "h2", "x": "The operating contract behind every service page",
    "sub": "Signed baseline, named gates, patent-mapped methods — the clauses that hold across all eight domains.",
}
P_CONTRACT = ("Three clauses hold across all eight domains and every practice inside them. First, the baseline is signed by the metric owner "
              "before the build starts — no metric, no build. Second, releases clear gates whose evidence is checkable, not asserted — an "
              "auditor can replay the trail without asking us for anything. Third, the methods underneath a gate are published, counted and mapped.")
CLAUSES = {
    "t": "bullets",
    "items": [
        ["Clause 1 — Signed baseline", "The metric owner signs before the build starts; the number, the source system and the measurement window are fixed in the document you keep."],
        ["Clause 2 — Named gates", "Every release clears gates whose evidence is checkable by replay — named gate owners, timestamps and artifacts, not assertions."],
        ["Clause 3 — Published methods", "The method families underneath each gate are counted and mapped on this site — read them before you talk to us, not after."],
    ],
}
P_PATENT = ("Where our patent-pending method families strengthen a gate, the service page names them and maps each family to the gate it "
            "reinforces — you can read the capability summary on the method map without asking for a briefing first. The patents protect "
            "how the gates bind; the contract protects what you can hold us to.")
H2_FAQ = {
    "t": "h2", "x": "Questions buyers ask first",
    "sub": "The four questions that decide the first meeting — answered before it.",
}
CTA = {
    "t": "cta",
    "x": ("Bring the metric you own to a 45-minute practice briefing — we will map it to the domain that moves it, name the rung you should "
          "enter at, and price the two-week diagnostic that ends in a signed baseline for your estate."),
}

HERO_X = ("Whichever of the eight domains you enter, the contract is identical: a business metric signed before delivery starts, an "
          "architecture you can audit before it ships, and exit numbers your finance team can reconcile. Fifty-four practices. Twelve "
          "industries. One governed spine.")

NEW_BLOCKS = [
    {"t": "hero", "x": HERO_X},
    H2_DIVIDE,
    {"t": "p", "x": P_DIVIDE},
    DOMAIN_TABLE,
    ARCH,
    IDASH,
    H2_DEPTH,
    {"t": "p", "x": P_DEPTH},
    HEATMAP,
    EXPLORER,
    H2_LADDER,
    {"t": "p", "x": P_LADDER},
    LADDER_TABLE,
    H2_CONTRACT,
    {"t": "p", "x": P_CONTRACT},
    CLAUSES,
    {"t": "p", "x": P_PATENT},
    H2_FAQ,
    FAQ,
    CTA,
]

# ── assemble + integrity checks ────────────────────────────────────────────
def wc(b):
    def texts(o):
        if isinstance(o, str):
            yield o
        elif isinstance(o, dict):
            for v in o.values():
                yield from texts(v)
        elif isinstance(o, list):
            for v in o:
                yield from texts(v)
    return len(" ".join(texts(b)).split())

page = dict(current)
page.update({
    "title": "Eight expertise domains, one governed delivery system",
    "seo_title": "IT Services & Expertise Domains | Achala IT Solutions",
    "meta_description": ("54 engineering practices across 8 expertise domains — every engagement enters on a signed metric baseline, "
                         "clears evidenced gates and exits with audited numbers. Pick your industry and see the engagement we would run."),
    "blocks": NEW_BLOCKS,
    "cards": CARDS,
    "related": RELATED,
    "evidence": EVIDENCE,
    "words": sum(wc(b) for b in NEW_BLOCKS) + sum(wc(c) for c in CARDS) + sum(wc(r) for r in RELATED),
})

# every URL referenced must exist in the page index
urls = set()
for f in PAGES.glob("*.json"):
    urls.add(json.load(open(f)).get("url"))
missing = []
for coll in (RELATED, EVIDENCE, [c for ind in EXPLORER["industries"] for c in ind["evidence"]], CARDS):
    for item in coll:
        if item["url"] not in urls:
            missing.append(item["url"])
cap_missing = [i["capUrl"] for i in EXPLORER["industries"] if i["capUrl"] not in urls]
if missing or cap_missing:
    print("MISSING URLS:", missing, cap_missing)
    sys.exit(1)

# explorer industry names must match the matrix rows
matrix_names = set(HEAT_CATS)
expl_names = {i["name"] for i in EXPLORER["industries"]}
assert matrix_names == expl_names, f"industry mismatch: {matrix_names ^ expl_names}"

# FAQ must be question-shaped (feeds JSON-LD)
assert all(q.rstrip().endswith("?") for q, _ in FAQ["items"])

json.dump(page, open(OUT, "w"), indent=1, ensure_ascii=False)
print(f"services.json rebuilt: {len(NEW_BLOCKS)} blocks, {page['words']} words, briefs reconciled ({SUB_BRIEFS} sub + {IND_LEVEL} industry-level = {TOTAL_BRIEFS})")

# ── register for traceability ──────────────────────────────────────────────
REGISTER = {
    "wave": "Wave 2 — Services hub",
    "scope": "/services/ (services_hub)",
    "items": [
        {"id": "W2-01", "item": "Buyer+proof H1 and lede", "spec": "H1 states the governed-delivery promise; lede carries proof (54 practices, 12 industries, one spine)"},
        {"id": "W2-02", "item": "Domain table + Flagship build column", "spec": "Each of the 8 rows cites a published case with its measured number"},
        {"id": "W2-03", "item": "Unique hub architecture", "spec": "8 domain nodes (each with managed-metric subs) composing on a 4-node governed spine; 12 labeled edges; 4 count badges"},
        {"id": "W2-04", "item": "Engagement console (idash)", "spec": "5 KPI tiles + 3 tabs (Delivery quality / Cost & cycle / Sector coverage), domain language, provenance note"},
        {"id": "W2-05", "item": "Sector-depth heatmap recast", "spec": "Reconciled 336-brief framing + non-empty reading note"},
        {"id": "W2-06", "item": "Interactive industry selector", "spec": "12 industries; hook, 3 cross-domain plays, 3 signed KPIs (drawn from domain pages), estate anchors, 2 case links each"},
        {"id": "W2-07", "item": "Engagement ladder kept, intro tightened", "spec": "Four rungs with exit artifacts as exit criteria"},
        {"id": "W2-08", "item": "Operating contract clause cards", "spec": "3 clauses as bullets + patent-neutral method paragraph"},
        {"id": "W2-09", "item": "Buyer FAQ", "spec": "4 question-shaped Q&A; FAQ JSON-LD rule fixed site-wide (question-shaped bullets only)"},
        {"id": "W2-10", "item": "Outcome-framed unique CTA", "spec": "45-minute briefing ask tied to the diagnostic exit artifact"},
        {"id": "W2-11", "item": "Domain cards with count chips", "spec": "Practice + sector-brief counts per card; metric-bearing descriptions"},
        {"id": "W2-12", "item": "Related rail + evidence wiring", "spec": "5 related targets, 3 evidence builds — all URLs verified against the page index"},
    ],
}
json.dump(REGISTER, open("/home/z/my-project/scripts/wave2_register.json", "w"), indent=1)
print("register saved: scripts/wave2_register.json")
print("baseline snapshot: scripts/wave2_baseline_services_hub.json")
