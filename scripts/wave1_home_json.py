#!/usr/bin/env python3
"""Wave 1 homepage content: rewrite home.json extras — stats (A-07..A-11),
domains reorder + flagship metrics + platform pairing (A-19/21/39),
insights to 6 (A-45), SEO title/description (A-49/50)."""
import json

P = "/home/z/my-project/site/src/content/pages/home.json"
d = json.load(open(P, encoding="utf-8"))
ex = d["extras"]

# ── stats strip (A-07 single render lives in HomeView; A-08/09/10/11 content) ──
ex["stats"] = [
    {"value": "1.9M", "label": "decisions/day under management — reference program"},
    {"value": "148 ms", "label": "decision p95, within SLO — reference program"},
    {"value": "100%", "label": "of releases gated on signed evidence"},
    {"value": "350+", "label": "engagements delivered · 116 published with measured deltas"},
    {"value": "40+", "label": "countries served from 4 global delivery centers"},
    {"value": "8", "label": "platforms in production — Nexus, Forge, Swarm and five more"},
    {"value": "8", "label": "patented method families behind every delivery"},
    {"value": "2,400+", "label": "engineers, data scientists and domain specialists"},
]

# ── domains (A-21 buyer-intent order; A-19 flagship metric; A-39 pairing) ──
DOMAIN_ORDER = [
    ("Data, Analytics & Lakehouse", {"metric": "99.4% freshness SLA · 0 metric disputes", "plat": "Achala Forge", "start": True}),
    ("Agentic AI & Hyperautomation", {"metric": "78% portfolio containment · 216 automations governed", "plat": "Achala Swarm", "start": True}),
    ("Applied AI & Generative AI", {"metric": "87% eval coverage · 68% PoC kill rate enforced", "plat": "Achala Nexus"}),
    ("Cybersecurity & Zero-Trust", {"metric": "97.4% evidence freshness · drill RTO 9.5 h vs 12 h target", "plat": "Achala Sentinel"}),
    ("Cloud, Edge & Platform Engineering", {"metric": "23.4% waste eliminated · 38% legacy surface retired", "plat": "Achala Forge"}),
    ("IoT, Digital Twin & Robotics", {"metric": "1,842 assets instrumented · −58% unplanned downtime", "plat": "Achala Twinverse"}),
    ("Blockchain & Digital Trust", {"metric": "0 reconciliation deltas · 412k credentials issued", "plat": "Achala Ledger"}),
    ("Quantum & Advanced Compute", {"metric": "82% parallel efficiency · 100% benchmark honesty", "plat": "Achala Quanta"}),
]
by_name = {dm["name"]: dm for dm in ex["domains"]}
new_domains = []
for name, add in DOMAIN_ORDER:
    dm = by_name.get(name)
    if not dm:
        raise SystemExit("missing domain in home.json: " + name)
    dm = dict(dm)
    dm["metric"] = add["metric"]
    dm["plat"] = add["plat"]
    dm["start"] = add.get("start", False)
    new_domains.append(dm)
ex["domains"] = new_domains

# ── insights → 6 (A-45), domain-diverse, real meta descriptions ──
idx = json.load(open("/home/z/my-project/site/src/content/index.json", encoding="utf-8"))
rows = [r for r in idx if r["template"] == "insight_article"]
picked, seen = [], set()
for r in rows:
    if r["l2"] in seen:
        continue
    picked.append(r)
    seen.add(r["l2"])
    if len(picked) == 6:
        break
ex["insights"] = [
    {"title": r["title"], "url": r["url"], "desc": r["metaDescription"], "tag": r["l2"]}
    for r in picked
]
if len(ex["insights"]) < 6:
    for r in rows:
        if all(r["url"] != it["url"] for it in ex["insights"]):
            ex["insights"].append({"title": r["title"], "url": r["url"], "desc": r["metaDescription"], "tag": r["l2"]})
        if len(ex["insights"]) == 6:
            break

# ── SEO (A-49/50) ──
d["seo_title"] = "Achala IT Solutions — decision intelligence with evidence | AI, data, security, cloud"
d["meta_description"] = (
    "Eight expertise domains, 54 practices. Every engagement gated on a signed metric, "
    "every decision carrying evidence. SOC 2 · ISO 27001."
)

json.dump(d, open(P, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("stats:", len(ex["stats"]), "| domains:", len(ex["domains"]), "| insights:", len(ex["insights"]))
for it in ex["insights"]:
    print("  ", it["tag"], "→", it["title"][:58])
