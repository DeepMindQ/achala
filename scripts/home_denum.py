#!/usr/bin/env python3
"""Wave 5c: strip count-branding from home.json copy — every paragraph reads like
TCS/Infosys/Wipro brand copy; hard numbers stay only in the facts strip/table."""
import json

P = "site/src/content/pages/home.json"
d = json.load(open(P))

B = d["blocks"]
def find(t, x_sub):
    for b in B:
        if b.get("t") == t and x_sub in b.get("x", ""):
            return b
    raise SystemExit(f"not found: {t} / {x_sub[:40]}")

find("hero", "Ambition")["x"] = (
    "Ambition, engineered. Outcomes, proven. Achala IT Solutions is a global IT services, consulting and business "
    "solutions partner. We consult, build and run the technology your business depends on — from ERP and cloud to "
    "AI and data — powered by our own patented methods and platforms, with every program measured on a metric your "
    "board already tracks."
)
find("p", "2,400+ engineers")["x"] = (
    "Achala IT Solutions is a global IT services, consulting and business solutions partner, with a worldwide team of "
    "engineers, consultants and domain specialists backed by dedicated delivery centers across three continents. We "
    "consult on strategy, build and modernize the systems that run your business, and operate them day to day — "
    "always with named owners, signed baselines and evidence your auditors can walk."
)
find("p", "Eight patented method families developed by our research programme")["x"] = (
    "What separates us is the intellectual property we bring on day one. Patented method families developed by our "
    "research programme arrive pre-configured inside our proprietary platforms, so programs start from a configured "
    "baseline and the budget goes to the work that is genuinely yours."
)
find("h2", "Two ways in")["x"] = "Two ways in: deep expertise and consulting, one delivery system"
find("p", "Deep-tech programs enter through one of")["x"] = (
    "Deep-tech programs enter through an expertise domain; classic-estate work enters through the consulting "
    "practices. Both tracks run the same release gates on the same patented platforms — a fraud program draws on "
    "data engineering, agentic automation and cybersecurity at the same time, under one delivery plan."
)
find("h2", "Consulting across the classic estate")["x"] = "Consulting that ends in delivery"
find("p", "Thirteen consulting practices in four groups")["x"] = (
    "Our consulting groups cover the classic estate — and the advisor is the builder: the team that recommends the "
    "roadmap delivers it, under the same gate contract as every expertise domain."
)
find("h2", "The IP differential")  # keep h2 label
find("p", "Most engagements elsewhere start from a blank page")["x"] = (
    "Most engagements elsewhere start from a blank page and a staffing plan. Ours start from configured "
    "intellectual property: the patented method families arrive as platform baselines, teams start near full "
    "readiness, and the gates prove the delta against your signed baseline. Commercially it flexes to the deal — "
    "license, embed or co-develop, with co-ownership terms available on accelerators built specifically for you."
)
find("p", "are in production use inside named platforms")["x"] = (
    "The method families — graph-native contextual intelligence, quantum-inspired optimization, federated learning "
    "with homomorphic encryption, multi-layer decision validation, energy-aware workload orchestration, generative "
    "workflow automation, self-evolving enterprise learning loops and multimodal pattern recognition — are in "
    "production use inside named platforms. The mapping from method to platform to service is on the "
    "patented-intelligence page."
)
find("p", "regulatory posture, priority programs")["x"] = (
    "We work across the industries that run the economy. Each industry page maps the sector's regulatory posture, "
    "priority programs and the capabilities that matter there. Examples of how that reads in practice:"
)
find("p", "The full sector list")["x"] = (
    "The full sector list — insurance, telecom, logistics, public sector, education, technology and agriculture — "
    "is on the industries hub, and every sub-industry page aligns the domains that matter most there."
)
find("p", "Delivery runs on a")["x"] = (
    "Delivery runs on a method with named gates: Diagnose, Design, Prove, Industrialize, Compound. No phase "
    "proceeds without its evidence — the baseline audit, the risk budget, the pilot's measured delta, the production "
    "runbook, the quarterly re-audit. Commercial models can link fees to the metrics we commit to moving."
)

d["meta_description"] = (
    "Achala IT Solutions is a global IT services, consulting and business solutions partner — from ERP and cloud to AI "
    "and data — powered by patented delivery IP and gated on signed metrics. SOC 2 · ISO 27001."
)

def wc(b):
    if b["t"] == "bullets": return sum(len((a+" "+c).split()) for a,c in b["items"])
    if b["t"] == "table": return sum(len(" ".join(r).split()) for r in b["rows"]) + len(" ".join(b["headers"]).split()) + len(b["caption"].split())
    return len(b.get("x","").split())
d["words"] = sum(wc(b) for b in B)

dump = json.dumps(d)
for banned in ["Strategemist", "Hyderabad", "Ravi Shanker", "Pisupati"]:
    assert banned not in dump, banned
json.dump(d, open(P, "w"), indent=1, ensure_ascii=False)
print("home.json de-numbered · words:", d["words"])
