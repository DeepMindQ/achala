# -*- coding: utf-8 -*-
"""Achala IT Solutions — Information architecture engine: 601-page tree with slugs, menus, SEO meta, volumes."""

import sys, os, hashlib
sys.path.insert(0, os.path.dirname(__file__))

from dqs_data_towers import TOWERS, SERVICES
from dqs_data_industries_a import INDUSTRIES_A
from dqs_data_industries_b import INDUSTRIES_B
from dqs_data_subs_a import SUBS_A
from dqs_data_subs_b import SUBS_B
from dqs_data_solutions import SOLUTIONS, PLATFORMS, SOLUTION_CATEGORIES
from dqs_data_cases import CASES
from dqs_data_brand import (BRAND, ABOUT_PAGE, EDGE_PAGE, LEADERSHIP, VALUES_PAGE, CAREERS_PAGE,
                            NEWSROOM_PAGE, PARTNERS_PAGE, APPROACH_PAGES, CONTACT_PAGES, INSIGHTS)

INDUSTRIES = {**INDUSTRIES_A, **INDUSTRIES_B}
SUBS = {**SUBS_A, **SUBS_B}
BRAND_SLUG = "achala-soft"

PAGES = []          # ordered list of page dicts
_PAGE_INDEX = {}    # id -> page

def _add(pid, section, l1, l2, l3, l4, title, url, template, seo_title, meta_desc, word_target, volume, priority, block):
    p = {"id": pid, "section": section, "l1": l1, "l2": l2, "l3": l3, "l4": l4,
         "title": title, "url": url, "template": template, "seo_title": seo_title,
         "meta_description": meta_desc, "word_target": word_target, "volume": volume,
         "priority": priority, "breadcrumb": " > ".join([x for x in [l1, l2, l3, l4] if x]) or "Home",
         "nav_block": block}
    PAGES.append(p)
    _PAGE_INDEX[pid] = p
    return p

def _seo(page_name, context, suffix="Achala IT Solutions"):
    t = f"{page_name} | {context} | {suffix}"
    return t[:60].rstrip()

def _meta(promise_like):
    m = promise_like.strip()
    if len(m) > 155:
        m = m[:152].rstrip() + "..."
    return m

VOL_NAMES = {
    "V01": "Volume 01 — Home & Services",
    "V02": "Volume 02 — Industries A (Hubs & Sub-Industries)",
    "V03": "Volume 03 — Industries B (Hubs & Sub-Industries)",
    "V04": "Volume 04 — Industry Capability Pages A",
    "V05": "Volume 05 — Industry Capability Pages B",
    "V06": "Volume 06 — Sub-Industry Capability Pages A",
    "V07": "Volume 07 — Sub-Industry Capability Pages B",
    "V08": "Volume 08 — Solutions & Platforms",
    "V09": "Volume 09 — Case Studies",
    "V10": "Volume 10 — Company, Approach & Contact",
    "V11": "Volume 11 — Insights Library",
}

TOWER_ORDER = ["applied-ai", "agentic", "data", "cyber", "cloud", "quantum", "blockchain", "iot"]
IND_ORDER = ["banking", "insurance", "healthcare", "manufacturing", "retail", "telecom",
             "energy", "logistics", "public-sector", "education", "technology", "agriculture"]
IND_SLUGS_A = set(IND_ORDER[:6])

VOL_OF_IND_HUB = {ind: ("V02" if ind in IND_SLUGS_A else "V03") for ind in IND_ORDER}
VOL_OF_CAP = {ind: ("V04" if ind in IND_SLUGS_A else "V05") for ind in IND_ORDER}


def build_ia():
    global PAGES, _PAGE_INDEX
    PAGES, _PAGE_INDEX = [], {}

    # ---------- 1. Home ----------
    _add("HOME", "Home", "", "", "", "", "Home", "/",
         "home",
         _seo("Achala IT Solutions", "IT Services & Consulting for the Intelligence Era"),
         _meta("Achala IT Solutions engineers the intelligence layer of the enterprise — applied AI, agentic automation, data platforms, cybersecurity and emerging compute with outcome-linked engagements."),
         900, "V01", "P0", "core")

    # ---------- 2. Services ----------
    svc_towers = [TOWERS[t] for t in TOWER_ORDER]
    _add("SVCHUB", "Services", "Services", "", "", "", "Services Overview", "/services/",
         "services_hub",
         _seo("Services", "8 Deep-Tech Towers — Achala IT Solutions"),
         _meta("Eight deep-tech service towers — applied AI, agentic automation, data & lakehouse, cybersecurity, cloud & edge, quantum, blockchain and IoT — engineered for auditable outcomes."),
         850, "V01", "P0", "core")
    for i, tw in enumerate(svc_towers, 1):
        _add(f"TWR-{i:02d}", "Services", "Services", tw["name"], "", "", tw["name"], f"/services/{tw['slug']}/",
             "tower_hub",
             _seo(tw["name"], "Deep-Tech Services — Achala IT Solutions"),
             _meta(tw["tagline"]),
             850, "V01", "P0", "core")
    for s in SERVICES:
        tw = TOWERS[s["tower"]]
        _add(f"SVC-{s['id']}", "Services", "Services", tw["name"], s["name"], "", s["name"],
             f"/services/{tw['slug']}/{s['id']}/", "service_page",
             _seo(s["name"], tw["short"]),
             _meta(s["promise"]),
             700, "V01", "P0" if s["tower"] in ("applied-ai", "agentic", "data") else "P1", "leaf")

    # ---------- 3. Industries ----------
    _add("INDHUB", "Industries", "Industries", "", "", "", "Industries Overview", "/industries/",
         "industries_hub",
         _seo("Industries", "12 Sectors, Deep-Tech Aligned — Achala IT Solutions"),
         _meta("Achala IT Solutions serves 12 industries with capability pages aligned per sector and sub-industry — banking, insurance, healthcare, manufacturing, retail, telecom, energy, logistics, public sector, education, technology and agriculture."),
         650, "V02", "P0", "core")
    for ind_id in IND_ORDER:
        ind = INDUSTRIES[ind_id]
        vol_hub = VOL_OF_IND_HUB[ind_id]
        _add(f"IND-{ind_id}", "Industries", "Industries", ind["name"], "", "", ind["name"],
             f"/industries/{ind['slug']}/", "industry_hub",
             _seo(ind["name"], "Industry Solutions — Achala IT Solutions"),
             _meta(ind["tagline"]),
             950, vol_hub, "P0", "core")
        # sub-industries (collect from SUBS)
        ind_subs = [SUBS[k] for k in SUBS if SUBS[k]["industry"] == ind_id]
        for sb in ind_subs:
            _add(f"SUB-{sb['slug']}", "Industries", "Industries", ind["name"], sb["name"], "", sb["name"],
                 f"/industries/{ind['slug']}/{sb['slug']}/", "subindustry_page",
                 _seo(sb["name"], ind["name"]),
                 _meta(sb["intro"][:152] + "...") if len(sb["intro"]) > 155 else _meta(sb["intro"]),
                 700, vol_hub, "P1", "leaf")
        # industry x tower capability pages
        for tw_id in TOWER_ORDER:
            tw = TOWERS[tw_id]
            vol_cap = VOL_OF_CAP[ind_id]
            _add(f"CAP-{ind_id}-{tw_id}", "Industries", "Industries", ind["name"], "Capabilities", tw["name"],
                 f"{tw['short']} for {ind['name']}",
                 f"/industries/{ind['slug']}/capabilities/{tw['slug']}/", "industry_capability",
                 _seo(f"{tw['short']} for {ind['name']}", "Capabilities"),
                 _meta(f"How Achala IT Solutions applies {tw['name']} in {ind['name']}: {ind['tagline']}"),
                 700, vol_cap, "P1", "leaf")
            # sub-industry x tower capability pages
            for sb in ind_subs:
                if tw_id in sb["towers"]:
                    _add(f"SCAP-{sb['slug']}-{tw_id}", "Industries", "Industries", ind["name"], sb["name"], tw["name"],
                         f"{tw['short']} for {sb['name']}",
                         f"/industries/{ind['slug']}/{sb['slug']}/capabilities/{tw['slug']}/", "sub_capability",
                         _seo(f"{tw['short']} for {sb['name']}", ind["name"]),
                         _meta(f"Deep-tech capabilities for {sb['name']}: {sb['intro'][:110]}..."),
                         620, "V06" if ind_id in IND_SLUGS_A else "V07", "P2", "leaf")

    # ---------- 4. Solutions ----------
    _add("SOLHUB", "Solutions", "Solutions", "", "", "", "Solutions Overview", "/solutions/",
         "solutions_hub",
         _seo("Solutions", "Outcome-Based Programs — Achala IT Solutions"),
         _meta("24 outcome-based solutions across growth, risk, operations and workforce — each anchored to named metrics, platforms and industry playbooks."),
         600, "V08", "P0", "core")
    for (sid, cat, name, promise, problem, approach, comps, plats, inds, kpis) in SOLUTIONS:
        _add(f"SOL-{sid}", "Solutions", "Solutions", SOLUTION_CATEGORIES[cat], name, "", name,
             f"/solutions/{sid}/", "solution_page",
             _seo(name, SOLUTION_CATEGORIES[cat]),
             _meta(promise),
             650, "V08", "P1", "leaf")

    # ---------- 5. Platforms ----------
    _add("PLTHUB", "Platforms", "Platforms", "", "", "", "Platforms Overview", "/platforms/",
         "platforms_hub",
         _seo("Platforms", "8 Proprietary Platforms — Achala IT Solutions"),
         _meta("Eight proprietary platforms — Nexus, Forge, Swarm, Sentinel, Twinverse, Quanta, Ledger, Compass — encoding a decade of deep-tech delivery into configurable products."),
         700, "V08", "P0", "core")
    for (pid, name, slug, cat, promise, overview, modules, trust_para, trust_bullets, integr, use_inds) in PLATFORMS:
        _add(f"PLT-{pid}-ov", "Platforms", "Platforms", name, "Overview", "", f"{name} — Overview",
             f"/platforms/{slug}/", "platform_overview",
             _seo(name, cat), _meta(promise), 700, "V08", "P1", "core")
        _add(f"PLT-{pid}-ar", "Platforms", "Platforms", name, "Architecture & Trust", "", f"{name} — Architecture & Trust",
             f"/platforms/{slug}/architecture/", "platform_architecture",
             _seo(f"{name} Architecture", "Security & Trust"),
             _meta(f"Architecture, security posture and compliance evidence for {name} — {cat} from Achala IT Solutions."),
             620, "V08", "P1", "leaf")
        _add(f"PLT-{pid}-uc", "Platforms", "Platforms", name, "Industry Use Cases", "", f"{name} — Industry Use Cases",
             f"/platforms/{slug}/use-cases/", "platform_usecases",
             _seo(f"{name} Use Cases", "By Industry"),
             _meta(f"How {name} is deployed across industries: {', '.join(use_inds[:4])} and more."),
             620, "V08", "P1", "leaf")

    # ---------- 6. Case studies ----------
    _add("CASEHUB", "Case Studies", "Case Studies", "", "", "", "Case Studies Overview", "/case-studies/",
         "cases_hub",
         _seo("Case Studies", "Anonymized Client Outcomes — Achala IT Solutions"),
         _meta("36 anonymized client engagements across 12 industries — with challenge, solution architecture and measured outcomes for every program."),
         550, "V09", "P0", "core")
    for c in CASES:
        _add(f"CASE-{c['id']}", "Case Studies", "Case Studies", INDUSTRIES[c['industry']]['name'], c["client"], "",
             c["client"], f"/case-studies/{c['id']}/", "case_study",
             _seo(c["client"], INDUSTRIES[c['industry']]["name"]),
             _meta(c["headline"]),
             600, "V09", "P1", "leaf")

    # ---------- 7. Company ----------
    company_pages = [
        ("CO-about", "Company", ABOUT_PAGE["title"], f"/{ABOUT_PAGE['slug']}/", ABOUT_PAGE["title"],
         "Company profile, delivery centers and credentials of Achala IT Solutions.", "V10", "P0"),
        ("CO-edge", "Company", EDGE_PAGE["title"], f"/{EDGE_PAGE['slug']}/", EDGE_PAGE["title"],
         "Five reasons clients choose Achala IT Solutions: platforms, evidence, controls, commercials, accountability.", "V10", "P0"),
        ("CO-leadership", "Company", "Leadership", "/leadership/", "Leadership",
         "Leadership roles and accountability structure across the Achala IT Solutions platform portfolio.", "V10", "P1"),
        ("CO-offices", "Company", "Global Offices", "/global-offices/", "Global Offices",
         "Four global delivery centers — US, UK, India and KSA — with practice focus per location.", "V10", "P1"),
        ("CO-values", "Company", VALUES_PAGE["title"], f"/{VALUES_PAGE['slug']}/", VALUES_PAGE["title"],
         "The operating culture behind Achala IT Solutions: evidence rituals, no-go discipline, zero-exposure security.", "V10", "P1"),
        ("CO-careers", "Company", CAREERS_PAGE["title"], f"/{CAREERS_PAGE['slug']}/", CAREERS_PAGE["title"],
         "Careers across eight deep-tech towers with credential pathways and global rotation.", "V10", "P1"),
        ("CO-newsroom", "Company", NEWSROOM_PAGE["title"], f"/{NEWSROOM_PAGE['slug']}/", NEWSROOM_PAGE["title"],
         "News, platform releases and recognitions from Achala IT Solutions.", "V10", "P2"),
        ("CO-partners", "Company", PARTNERS_PAGE["title"], f"/{PARTNERS_PAGE['slug']}/", PARTNERS_PAGE["title"],
         "Architecture-level partner ecosystem across hyperscalers, data, security, quantum and DLT.", "V10", "P1"),
    ]
    for pid, sec, title, url, seo_name, desc, vol, prio in company_pages:
        _add(pid, sec, "About Us", title, "", "", title, url, "company_page",
             _seo(seo_name, "About Achala IT Solutions"), _meta(desc), 550, vol, prio, "core" if prio == "P0" else "leaf")

    # ---------- 8. Approach ----------
    approach_meta = {
        "method": ("The Achala Method", "Five phases with named gates — Diagnose, Design, Prove, Industrialize, Compound.", "P0"),
        "outcome-linked": ("Outcome-Linked Engagements", "Commercial models aligned to the metric: outcome pilots, value-linked fees, platform subscriptions.", "P0"),
        "responsible-ai": ("Responsible AI Framework", "Five control layers mapped to NIST AI RMF, ISO 42001 and the EU AI Act.", "P0"),
        "delivery-model": ("Global Delivery Model", "Four delivery centers, named pods, follow-the-sun operations.", "P1"),
    }
    for key, ap in APPROACH_PAGES.items():
        name, desc, prio = approach_meta[key]
        _add(f"AP-{key}", "Approach", "About Us", "Our Approach", name, "", name,
             f"/our-approach/{ap['slug']}/", "approach_page",
             _seo(name, "Our Approach"), _meta(desc), 600, "V10", prio, "core" if prio == "P0" else "leaf")

    # ---------- 9. Insights ----------
    _add("INSHUB", "Insights", "Insights", "", "", "", "Insights Library", "/insights/",
         "insights_hub",
         _seo("Insights", "Deep-Tech Perspectives — Achala IT Solutions"),
         _meta("Perspectives across eight deep-tech domains — retrieval economics, agentic policy, PQC clocks, provenance compliance and more.", ),
         500, "V11", "P0", "core")
    for tw_id in TOWER_ORDER:
        tw = TOWERS[tw_id]
        _add(f"INSCAT-{tw_id}", "Insights", "Insights", tw["name"], "", "", f"Insights: {tw['short']}",
             f"/insights/{tw['slug']}/", "insights_category",
             _seo(f"{tw['short']} Insights", "Perspectives"),
             _meta(f"Achala IT Solutions perspectives on {tw['name']}: engineering notes, market views and delivery lessons."),
             420, "V11", "P2", "leaf")
    for ins in INSIGHTS:
        slug = ins[0].replace("ins-", "insight-")
        tw = TOWERS[ins[1]]
        title = ins[2]
        _add(f"INS-{ins[0]}", "Insights", "Insights", tw["name"], title, "", title,
             f"/insights/{slug}/", "insight_article",
             _seo(title, f"{tw['short']} Insights"),
             _meta(ins[3]),
             500, "V11", "P2", "leaf")

    # ---------- 10. Contact & Legal ----------
    ct_items = [
        ("CT-contact", "Contact & Legal", CONTACT_PAGES["contact"]["title"], "/contact/", "P0"),
        ("CT-briefing", "Contact & Legal", CONTACT_PAGES["briefing"]["title"], "/book-a-briefing/", "P0"),
        ("CT-assessment", "Contact & Legal", CONTACT_PAGES["assessment"]["title"], "/value-assessment/", "P1"),
    ]
    for pid, sec, title, url, prio in ct_items:
        _add(pid, sec, "Contact", title, "", "", title, url, "contact_page",
             _seo(title, "Contact Achala IT Solutions"),
             _meta("Engage Achala IT Solutions: executive briefings, value assessments and practice-lead responses within one business day."),
             420, "V10", prio, "core" if prio == "P0" else "leaf")
    for slug, title, desc in CONTACT_PAGES["legal"]:
        _add(f"CT-{slug}", "Contact & Legal", title, "", "", "", title, f"/{slug}/", "legal_page",
             _seo(title, "Legal"), _meta(desc), 380, "V10", "P2", "leaf")

    return PAGES


def ia_stats():
    from collections import Counter
    c = Counter(p["section"] for p in PAGES)
    return c


if __name__ == "__main__":
    pages = build_ia()
    print(f"TOTAL PAGES: {len(pages)}")
    for k, v in ia_stats().items():
        print(f"  {k:20s} {v}")
    # volume counts
    vols = {}
    for p in pages:
        vols.setdefault(p["volume"], []).append(p)
    for v in sorted(vols):
        print(f"  {v}: {len(vols[v])} pages — {VOL_NAMES[v]}")
    # level counts
    l4 = [p for p in pages if p["l4"]]
    print(f"Pages with L4 (sub-sub-sub): {len(l4)}")
    assert len(pages) == 602, f"Expected 602 pages, got {len(pages)}"
    print("IA OK")
