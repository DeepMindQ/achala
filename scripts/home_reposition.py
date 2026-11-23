#!/usr/bin/env python3
"""Rebuild home.json: reposition Achala IT Solutions as an IT services & consulting company
with patented IP as the differential strategy. Keeps extras schema intact (stats,
domains, industries, cases, insights, platforms) and recomputes the word count."""
import json, re

P = "site/src/content/pages/home.json"
old = json.load(open(P))

blocks = [
 {"t": "hero", "x": "Achala IT Solutions is an IT services and consulting company. Fifty-four deep-tech practices and thirteen consulting practices — from strategy to managed operations — with eight patented method families pre-configured in eight proprietary platforms, and every engagement gated on a metric your board signs."},
 {"t": "h2", "x": "What we do"},
 {"t": "p", "x": "Achala IT Solutions is a global IT services and consulting firm with 2,400+ engineers, consultants, data scientists and domain specialists across four delivery centers. The engagement surface covers the whole estate: digital transformation programs, data migration, software engineering pods, testing and quality engineering, application modernization, Azure cloud, ERP cores, managed operations and end-user support — alongside deep-tech programs in applied AI, agentic automation, data platforms, cybersecurity and advanced compute."},
 {"t": "p", "x": "Every engagement starts with a baseline your finance team signs. Every quarter ends with a measured delta against that baseline. When a program should stop, we say so in writing. That discipline — not a model architecture — is what most enterprise technology programs are missing, and it is the first thing we install."},
 {"t": "p", "x": "What separates us is the intellectual property we bring on day one. Eight patented method families developed by our research programme arrive pre-configured inside eight proprietary platforms, so programs start from a configured 80 percent baseline and the budget goes to the 20 percent that is genuinely yours."},
 {"t": "h2", "x": "Two ways in: eight expertise domains, thirteen consulting practices"},
 {"t": "p", "x": "Deep-tech programs enter through one of eight expertise domains; classic-estate work enters through the consulting practices. Both tracks run the same release gates on the same patented platforms — a fraud program draws on data engineering, agentic automation and cybersecurity at the same time, under one delivery plan."},
 {"t": "bullets", "items": [
  ["Applied AI & Generative AI", "Strategy, model selection, retrieval, evaluation and production operations. AI measured on the P&L, from enterprise strategy to deployed systems."],
  ["Agentic AI & Hyperautomation", "Digital workers that run inside your systems with defined roles, budgets and human checkpoints. Every action is logged and reversible."],
  ["Data, Analytics & Lakehouse", "Pipelines, lakehouse and governance: reports that reconcile, lineage you can trace, access control that does not slow teams down."],
  ["Cybersecurity & Zero-Trust", "Identity-first architecture for people, machines and models, with detection, response and AI-specific controls in one program."],
  ["Cloud, Edge & Platform Engineering", "Hybrid and edge estates engineered for reliability and cost per workload, with internal platforms your teams actually adopt."],
  ["Quantum & Advanced Compute", "Optimization, simulation and post-quantum cryptography migration — applied where the mathematics pays back, benchmarked against classical methods."],
  ["Blockchain & Digital Trust", "Permissioned networks, tokenization and verifiable credentials with the reporting supervisors expect."],
  ["IoT, Digital Twin & Robotics", "Sensor integration, digital twins and robotics: see, simulate and act on physical assets in one loop."],
 ]},
 {"t": "h2", "x": "Consulting across the classic estate"},
 {"t": "p", "x": "Thirteen consulting practices in four groups cover the classic estate — and the advisor is the builder: the team that recommends the roadmap is the team that delivers it, under the same gate contract as every expertise domain."},
 {"t": "bullets", "items": [
  ["Data & Analytics", "Decision products, migration factories and platform moves for the classic data estate."],
  ["Engineering & Quality", "Engineering pods that ship into your controls, and quality engineered in — not tested after."],
  ["Cloud & Operations", "Azure estates end to end, managed operations and end-user support with SLAs you can audit."],
  ["Advisory & Enterprise", "Transformation programs, managed capacity, zero-trust advisory and ERP cores that land process and controls."],
 ]},
 {"t": "h2", "x": "The IP differential"},
 {"t": "p", "x": "Most engagements elsewhere start from a blank page and a staffing plan. Ours start from configured intellectual property: the patented method families arrive as platform baselines, teams start near 80 percent readiness, and the gates prove the delta against your signed baseline. Commercially it flexes to the deal — license, embed or co-develop, with co-ownership terms available on accelerators built specifically for you."},
 {"t": "p", "x": "The eight method families — graph-native contextual intelligence, quantum-inspired optimization, federated learning with homomorphic encryption, multi-layer decision validation, energy-aware workload orchestration, generative workflow automation, self-evolving enterprise learning loops and multimodal pattern recognition — are in production use inside named platforms. The mapping from method to platform to service is on the patented-intelligence page."},
 {"t": "h2", "x": "Where we work"},
 {"t": "p", "x": "Twelve industries, each with sub-industry depth: the sector's regulatory posture, priority programs and capability alignment are mapped on every industry page. Examples of how that reads in practice:"},
 {"t": "bullets", "items": [
  ["Banking & Financial Services", "Real-time fraud and risk decisions, resilient core operations and AI controls that pass supervisory review."],
  ["Healthcare & Life Sciences", "Clinical data interoperability, ambient documentation and AI programs under clinical governance."],
  ["Manufacturing & Industrial", "Sensor-driven quality, digital twins and shop-floor automation tied to OEE and yield."],
  ["Energy & Utilities", "Grid analytics, trading optimization and operational safety for the energy transition."],
  ["Retail & Consumer Goods", "Pricing, availability and personalization programs measured directly on margin."],
 ]},
 {"t": "p", "x": "The full sector list — insurance, telecom, logistics, public sector, education, technology and agriculture — is on the industries hub, and every sub-industry page aligns the five domains that matter most there."},
 {"t": "h2", "x": "Achala IT Solutions in numbers"},
 {"t": "table",
  "caption": "Achala IT Solutions at a glance",
  "headers": ["Proof point", "What it means"],
  "rows": [
   ["350+", "enterprise engagements delivered"],
   ["40+", "countries served from 4 global delivery centers"],
   ["2,400+", "engineers, consultants, data scientists and domain specialists"],
   ["8", "proprietary platforms in production with clients"],
   ["8", "patented method families — the IP differential in every engagement"],
   ["630+", "published delivery playbooks across industries and capabilities"],
  ]},
 {"t": "h2", "x": "How we engage"},
 {"t": "p", "x": "Delivery runs on a five-phase method with named gates: Diagnose, Design, Prove, Industrialize, Compound. No phase proceeds without its evidence — the baseline audit, the risk budget, the pilot's measured delta, the production runbook, the quarterly re-audit. Commercial models can link fees to the metrics we commit to moving."},
 {"t": "bullets", "items": [
  ["Week 1", "A 45-minute executive briefing: your metric, our pattern library, three reference engagements."],
  ["Weeks 2–6", "A value assessment: baseline audit, six-week capital-committee-grade roadmap, fixed price."],
  ["Quarter 1", "The first production pilot: bounded scope, named control owner, measured delta at the gate."],
 ]},
 {"t": "cta", "x": "Bring the metric you need to move. We will show you the pattern, the platform and the baseline we would sign."},
]

def wc(b):
    if b["t"] == "bullets":
        return sum(len((a + " " + c).split()) for a, c in b["items"])
    if b["t"] == "table":
        return sum(len(" ".join(r).split()) for r in b["rows"]) + len(" ".join(b["headers"]).split()) + len(b["caption"].split())
    return len(b.get("x", "").split())

words = sum(wc(b) for b in blocks)

stats = old["extras"]["stats"]
for s in stats:
    if s["label"] == "patented method families behind every delivery":
        s["label"] = "patented method families — the IP differential in every engagement"
    if s["label"] == "platforms in production — Nexus, Forge, Swarm and five more":
        s["label"] = "proprietary platforms — the productized form of the patented methods"
    if s["label"] == "engineers, data scientists and domain specialists":
        s["label"] = "engineers, consultants, data scientists and domain specialists"

out = dict(old)
out["seo_title"] = "Achala IT Solutions — IT services & consulting with patented IP | AI, cloud, data, security, ERP"
out["meta_description"] = "IT services and consulting: 8 deep-tech expertise domains and 13 consulting practices, every engagement powered by 8 patented method families and 8 proprietary platforms — gated on signed metrics. SOC 2 · ISO 27001."
out["blocks"] = blocks
out["words"] = words
# confidentiality guard: the entity and inventor names must never appear
dump = json.dumps(out)
for banned in ["Strategemist", "Hyderabad", "Ravi Shanker", "Pisupati"]:
    assert banned not in dump, f"banned name in home.json: {banned}"

json.dump(out, open(P, "w"), indent=1, ensure_ascii=False)
print("home.json rebuilt · blocks:", len(blocks), "· words:", words)
