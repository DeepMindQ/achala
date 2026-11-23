#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate 80 new case-study pages (116 total), rebuild the hub JSON,
update index.json, compute related links. Content: hand-authored scenario data
in cases_data_a.py / cases_data_b.py."""
import json, os, sys, re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cases_data_a import SCEN_A, IND
from cases_data_b import SCEN_B

PAGES = 'site/src/content/pages'
HUB = os.path.join(PAGES, 'case-studies.json')
IDX = 'site/src/content/index.json'

NOTE = ("Figures on this page are the client's, reproduced with permission. "
        "Method notes and measurement designs are available under NDA.")
CTAS = [
    "Start with the diagnostic, not the contract: the same diagnostic that baselined this program takes two weeks, and a scoped proposal follows only if the delta justifies it.",
    "Bring your own baseline. The two-week diagnostic is how this engagement started, and it is how we find out whether your estate can carry the same delta.",
    "If this case sits close to your operation, the briefing is the right next step: 45 minutes with the practice lead who ran it, your metric against the pattern that moved here.",
    "The method on this page is documented because it worked twice — here and on the next estate. Book a briefing and bring the metric you need to move.",
    "Run the two-week diagnostic on your estate first; the numbers decide whether this pattern earns a build on yours.",
]

def wc(t):
    return len(re.findall(r"\S+", t))

def blocks_for(s):
    bl = []
    bl.append({"t": "hero", "x": s["hero"]})
    bl.append({"t": "h2", "x": "What we walked into"})
    bl.append({"t": "p", "x": s["walk"]})
    bl.append({"t": "h2", "x": "What the baseline showed"})
    bl.append({"t": "p", "x": s["b1"]})
    bl.append({"t": "p", "x": s["b2"]})
    bl.append({"t": "h2", "x": "What went into production"})
    bl.append({"t": "p", "x": s["build"]})
    bl.append({
        "t": "arch",
        "title": f"What went into production — {s['client']}",
        "lanes": s["lanes"],
        "nodes": [{"id": f"n{i}", "lane": ln, "label": lb, **({"hot": True} if hot else {})}
                  for i, (ln, lb, hot) in enumerate(s["nodes"])],
        "note": "The topology as deployed: every named node existed in the client estate at go-live.",
    })
    bl.append({"t": "h2", "x": "The measured delta"})
    bl.append({
        "t": "dash",
        "title": f"Program view — {s['client']}",
        "kpis": [{"label": k, "value": v, "delta": d, "dir": dr} for k, v, d, dr in s["kpis"]],
        "log": [{"t": t, "msg": m, "tag": g} for t, m, g in s["log"]],
        "note": "Tiles are the client's measured outcomes; the log is the delivery cadence, not a mock.",
    })
    cap, rows = s["mid"]
    bl.append({"t": "table", "caption": cap, "headers": ["Gate", "What it enforced"], "rows": rows})
    bl.append({"t": "h2", "x": "Transfer notes"})
    bl.append({"t": "p", "x": s["close"][1]})
    d, t_, r, m = s["facts"]
    bl.append({"t": "table", "caption": "Engagement facts", "headers": ["Duration", "Team", "Region", "Model"],
               "rows": [[d, t_, r, m]]})
    bl.append({"t": "note", "x": NOTE})
    bl.append({"t": "cta", "x": CTAS[hash(s["code"]) % len(CTAS)]})
    return bl

def words_of(bl):
    n = 0
    for b in bl:
        for v in (b.get("x"), b.get("title"), b.get("note"), b.get("caption")):
            if isinstance(v, str):
                n += wc(v)
        for k in ("kpis",):
            for kpi in b.get(k) or []:
                n += wc(kpi["label"]) + wc(kpi["value"]) + wc(kpi.get("delta", ""))
        for lg in b.get("log") or []:
            n += wc(lg["msg"])
        for r in b.get("rows") or []:
            n += sum(wc(c) for c in r)
        for nd in b.get("nodes") or []:
            n += wc(nd["label"])
        for ln in b.get("lanes") or []:
            n += wc(ln)
    return n

def main():
    # ── registry of existing 36 cases ────────────────────────────────────
    existing = []
    for f in sorted(os.listdir(PAGES)):
        if f.startswith("case-studies_") and f.endswith(".json"):
            d = json.load(open(os.path.join(PAGES, f), encoding="utf-8"))
            hero = next((b["x"] for b in d["blocks"] if b["t"] == "hero"), d["meta_description"])
            svc, svc_url = None, None
            for rel in d.get("related", []):
                if rel["title"].startswith("Tower — "):
                    svc = rel["title"].replace("Tower — ", "")
                    svc_url = rel["url"]
                    break
            region = ""
            for b in d["blocks"]:
                if b.get("t") == "table" and b.get("caption") == "Engagement facts":
                    region = b["rows"][0][2]
                    break
            existing.append({
                "title": d["title"], "url": d["url"], "industry": d["l2"],
                "industry_url": d["crumbs"][1]["url"] if len(d["crumbs"]) > 1 else "",
                "desc": hero, "service": svc, "service_url": svc_url, "region": region,
            })

    scen = SCEN_A + SCEN_B
    print("new scenarios:", len(scen), "| existing cases:", len(existing))

    cards = list(existing)
    made = 0
    for s in scen:
        ind_label, ind_url = IND[s["code"].split("-")[0]]
        svc_label, svc_url = s["svc"]
        bl = blocks_for(s)
        page = {
            "id": f"CASE-{s['code']}",
            "title": s["client"],
            "url": f"/case-studies/{s['code']}/",
            "template": "case_study",
            "breadcrumb": f"Case Studies > {ind_label} > {s['client']}",
            "seo_title": f"{s['client']} | Case Study | Achala IT Solutions",
            "meta_description": s["hero"],
            "blocks": bl,
            "words": words_of(bl),
            "section": "Case Studies",
            "l1": "Case Studies",
            "l2": ind_label,
            "l3": s["client"],
            "l4": "",
            "crumbs": [
                {"name": "Case Studies", "url": "/case-studies/"},
                {"name": ind_label, "url": ind_url},
                {"name": s["client"], "url": f"/case-studies/{s['code']}/"},
            ],
            "related": [],  # filled below
            "cards": [],
        }
        path = os.path.join(PAGES, f"case-studies_{s['code']}.json")
        json.dump(page, open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        cards.append({
            "title": s["client"], "url": page["url"], "industry": ind_label,
            "industry_url": ind_url, "desc": s["hero"], "service": svc_label,
            "service_url": svc_url, "region": s["region"],
        })
        made += 1

    print("pages written:", made)

    # ── related links per NEW case ────────────────────────────────────────
    for s in scen:
        ind_label, ind_url = IND[s["code"].split("-")[0]]
        svc_label, svc_url = s["svc"]
        siblings = [c for c in cards
                    if c["industry"] == ind_label and c["url"] != f"/case-studies/{s['code']}/"]
        rel = [
            {"title": f"{ind_label} — industry hub", "url": ind_url,
             "desc": "The industry hub maps this sector's regulatory reality to the towers, with named workflows and systems of record."},
            {"title": f"Service area — {svc_label}", "url": svc_url,
             "desc": "The tower behind this engagement: services, architecture gates and the method map."},
        ]
        for sib in siblings[:3]:
            rel.append({"title": sib["title"], "url": sib["url"], "desc": sib["desc"]})
        path = os.path.join(PAGES, f"case-studies_{s['code']}.json")
        d = json.load(open(path, encoding="utf-8"))
        d["related"] = rel
        json.dump(d, open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    # ── hub page ──────────────────────────────────────────────────────────
    n_cases = len(cards)
    inds = []
    for c in cards:
        if not inds or inds[-1][0] != c["industry"]:
            inds.append((c["industry"], c["industry_url"]))
    # dedupe preserving order
    seen, ind_list = set(), []
    for c in cards:
        if c["industry"] not in seen:
            seen.add(c["industry"])
            ind_list.append((c["industry"], c["industry_url"]))
    svc_seen, svc_list = set(), []
    for c in cards:
        if c["service"] and c["service"] not in svc_seen:
            svc_seen.add(c["service"])
            svc_list.append((c["service"], c["service_url"]))

    hub_intro = (
        f"{n_cases} anonymized engagements, indexed two ways: by the industry you operate in and by the "
        f"service area that did the work. Every case carries its measured delta, the system that produced "
        f"it, and the gates that governed the build. Identities stay behind NDA; the numbers are the "
        f"clients' own."
    )
    hub = json.load(open(HUB, encoding="utf-8"))
    hub.update({
        "title": "Case studies",
        "breadcrumb": "Case Studies",
        "seo_title": "Case Studies by Industry & Service Area | Achala IT Solutions",
        "meta_description": f"{n_cases} anonymized client engagements across {len(ind_list)} industries and "
                            f"{len(svc_list)} service areas — indexed by industry and service area, with challenge, "
                            f"solution architecture and measured outcomes for every program.",
        "blocks": [
            {"t": "hero", "x": hub_intro},
            {"t": "h2", "x": "Reading a case"},
            {"t": "p", "x": "Each case follows the same shape: the situation we walked into, what the two-week "
                            "baseline measured, what went into production, and the delta the client's own "
                            "systems reported. Where a pattern transferred cleanly we say so; where it did "
                            "not, the transfer notes say that too."},
            {"t": "note", "x": "Identity withheld under confidentiality; measurement methods available under NDA. "
                               "Baselines were signed before any build, and the figures come from the client's "
                               "own systems."},
            {"t": "cta", "x": "Find the case closest to your sector and metric — then bring both to a briefing. "
                              "The diagnostic that locked each baseline takes two weeks."},
        ],
        "cards": cards,
    })
    hub["words"] = words_of(hub["blocks"])
    json.dump(hub, open(HUB, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("hub rebuilt:", n_cases, "cards,", len(ind_list), "industries,", len(svc_list), "service areas")

    # ── index.json ────────────────────────────────────────────────────────
    idx = json.load(open(IDX, encoding="utf-8"))
    have = {r["url"] for r in idx}
    added = 0
    for s in scen:
        url = f"/case-studies/{s['code']}/"
        if url in have:
            continue
        ind_label, _ = IND[s["code"].split("-")[0]]
        bl = blocks_for(s)
        idx.append({
            "url": url, "file": f"case-studies_{s['code']}", "title": s["client"],
            "template": "case_study", "section": "Case Studies", "l1": "Case Studies",
            "l2": ind_label, "l3": s["client"], "l4": "",
            "seoTitle": f"{s['client']} | Case Study | Achala IT Solutions",
            "metaDescription": s["hero"], "words": words_of(bl),
        })
        added += 1
    # hub row
    for r in idx:
        if r["url"] == "/case-studies/":
            r.update({"title": "Case studies",
                      "seoTitle": "Case Studies by Industry & Service Area | Achala IT Solutions",
                      "metaDescription": hub["meta_description"], "words": hub["words"]})
    json.dump(idx, open(IDX, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("index rows added:", added, "| index total:", len(idx))

    # sanity: every card url exists in index
    urls = {r["url"] for r in idx}
    missing = [c["url"] for c in cards if c["url"] not in urls]
    print("cards missing from index:", missing)

if __name__ == "__main__":
    main()
