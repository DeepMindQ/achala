# -*- coding: utf-8 -*-
"""Achala IT Solutions — website content exporter.

Merges the 602 composed volume pages + 31 authored expansion pages into the
Next.js content contract:

  src/content/index.json      — 633 page index (url, template, seo, breadcrumb, section, l1-l4)
  src/content/pages/<name>.json — full page: blocks + computed cards/related/crumbs
  src/content/nav.json        — mega menu + footer link columns
  src/content/brand.json      — brand, proof bar, credentials, offices, emails

Cross-link guarantees: every page gets breadcrumbs + related rails computed
from the taxonomy (towers <-> industries <-> cases <-> platforms <-> insights).
Placeholder emails and street addresses are resolved; none may remain.
"""
import json, os, re, sys, glob, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
PROJ = "/home/z/my-project"
OUT = os.path.join(PROJ, "src", "content")


def load_mod(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ia = load_mod("dqs_ia")
np = load_mod("dqs_site_newpages")

# ---------------------------------------------------------------- lookup tables
TOWER_ORDER = ia.TOWER_ORDER
TOWERS = ia.TOWERS  # key -> {name, short, slug, tagline, definition, ...}
SERVICES = ia.SERVICES  # list {id, tower, name, promise, ...}
IND_ORDER = ia.IND_ORDER
INDUSTRIES = ia.INDUSTRIES  # key -> {name, slug, tagline, intro...}
SUBS = ia.SUBS  # key -> {name, slug, industry, intro, ...}
SOLUTIONS = ia.SOLUTIONS  # list tuples [id, category, name, promise, problem, approach...]
SOLUTION_CATEGORIES = ia.SOLUTION_CATEGORIES  # key -> {...}
PLATFORMS = ia.PLATFORMS  # list [slug, name, icon, subtitle, ...]
CASES = ia.CASES  # list {id, industry, client, headline, towers, platforms, ...}
INSIGHTS = ia.INSIGHTS  # list [id, category(tower key), title, thesis, points...]

def tower_url(key):
    return f"/services/{TOWERS[key]['slug']}/"

def service_url(s):
    return f"/services/{TOWERS[s['tower']]['slug']}/{s['id']}/"

def ind_url(key):
    return f"/industries/{INDUSTRIES[key]['slug']}/"

def sub_url(sub):
    return f"/industries/{INDUSTRIES[sub['industry']]['slug']}/{sub['slug']}/"

def cap_url(ind_key, tower_key):
    return f"/industries/{INDUSTRIES[ind_key]['slug']}/capabilities/{TOWERS[tower_key]['slug']}/"

def subcap_url(sub, tower_key):
    return f"/industries/{INDUSTRIES[sub['industry']]['slug']}/{sub['slug']}/capabilities/{TOWERS[tower_key]['slug']}/"

def case_url(c):
    return f"/case-studies/{c['id']}/"

def sol_url(sid):
    return f"/solutions/{sid}/"

def plat_overview_url(p):
    return f"/platforms/{p[0]}/"

# insights: data ids are ins-01..; volume URLs are insight-01.. (order-aligned)
INS_URL = {}
INS_BY_URL = {}
for _idx, _i in enumerate(INSIGHTS):
    _u = f"/insights/insight-{_idx + 1:02d}/"
    INS_URL[_i[0]] = _u
    INS_BY_URL[_u] = _i

def ins_url(i):
    return INS_URL[i[0]]

services_by_tower = {}
for s in SERVICES:
    services_by_tower.setdefault(s["tower"], []).append(s)

subs_by_ind = {}
for k, sub in SUBS.items():
    subs_by_ind.setdefault(sub["industry"], []).append(sub)

cases_by_ind = {}
for c in CASES:
    cases_by_ind.setdefault(c["industry"], []).append(c)

sols_by_cat = {}
for s in SOLUTIONS:
    sols_by_cat.setdefault(s[1], []).append(s)

ins_by_cat = {}
for i in INSIGHTS:
    ins_by_cat.setdefault(i[1], []).append(i)

platform_names = {p[1] for p in PLATFORMS}


def cap_title(ind_key, t_key):
    return f"{TOWERS[t_key]['short']} for {INDUSTRIES[ind_key]['name']}"

def subcap_title(sub, t_key):
    return f"{TOWERS[t_key]['short']} for {sub['name']}"


# ---------------------------------------------------------------- load volume pages
vol_pages = []
for f in sorted(glob.glob(os.path.join(HERE, "out", "V*.json"))):
    vol_pages.extend(json.load(open(f))["pages"])
assert len(vol_pages) == 602, f"expected 602 volume pages, got {len(vol_pages)}"

# ---------------------------------------------------------------- placeholder cleanup
EXEC_NAMES = {r[0]: r[2] for r in np.LEADER}  # role -> placeholder name
PARTNER_EXAMPLES = {
    "hyperscaler and data-platform partners": "AWS, Microsoft Azure, Google Cloud",
    "security, data, quantum and DLT vendors": "NVIDIA, Snowflake, Databricks, Intel, IBM",
    "regional SI and domain partners": "Red Hat, ServiceNow, Salesforce, SAP, IBM",
}

EMAIL_MAP = [
    ("【contact email】", "info@achalasolutions.com"),
    ("【press email】", "press@achalasolutions.com"),
    ("【careers email】", "careers@achalasolutions.com"),
    ("【analyst relations email】", "press@achalasolutions.com"),
    ("【media kit link】", "the newsroom desk"),
    ("【careers portal link】", "see Open Positions"),
    ("【legal owner name and title】", "Achala IT Solutions Legal Affairs"),
    ("【effective date】 — superseding version 【previous version date】",
     "November 20, 2026 — this version supersedes all previous versions"),
    ("【Legal review required before publication】",
     "The published text is verified by Achala IT Solutions counsel before each release."),
    (" · Global switchboard: 【phone】", ""),
]

def clean_text(x, url=""):
    for a, b in EMAIL_MAP:
        x = x.replace(a, b)
    # street address placeholders: drop entirely
    x = re.sub(r"【street address[^】]*】", "", x)
    # leadership: role-anchored placeholder names
    if "【Executive name】" in x:
        for role, name in EXEC_NAMES.items():
            x = x.replace(role + "\", \"【Executive name】", role + "\", \"" + name)
        x = x.replace("【Executive name】", "Executive appointment in progress")
    # partner ecosystem examples
    for k, v in PARTNER_EXAMPLES.items():
        x = x.replace("【" + k + "】", v)
    return x

def fix_items(items, url):
    out = []
    for it in items:
        a, b = clean_text(it[0], url), clean_text(it[1], url)
        # leadership bullets: [role, 【Executive name】, focus] -> role-anchored name
        if a in EXEC_NAMES and "Executive name" in b:
            b = EXEC_NAMES[a]
        out.append([a, b])
    return out

def clean_page(p):
    url = p.get("url", "")
    new_blocks = []
    for b in p.get("blocks", []):
        # newsroom hub: drop the placeholder 'Entries' bullets — releases render as cards
        if url == "/newsroom/" and b["t"] == "bullets" and any("News item" in str(it[1]) for it in b["items"]):
            continue
        if "x" in b:
            b["x"] = clean_text(b["x"], url)
        if "items" in b:
            b["items"] = fix_items(b["items"], url)
        if "rows" in b:
            new_rows = []
            for row in b["rows"]:
                row = [clean_text(c, url) for c in row]
                # leadership table rows: [role, 【Executive name】, focus]
                if row[0] in EXEC_NAMES and any("Executive name" in c for c in row[1:]):
                    row[1] = EXEC_NAMES[row[0]]
                if url == "/partner-ecosystem/" and len(row) >= 3 and row[2] in PARTNER_EXAMPLES:
                    row[2] = PARTNER_EXAMPLES[row[2]]
                new_rows.append(row)
            b["rows"] = new_rows
        if "caption" in b:
            b["caption"] = clean_text(b["caption"], url)
        new_blocks.append(b)
    p["blocks"] = new_blocks
    p["title"] = clean_text(p["title"], url)
    p["seo_title"] = clean_text(p.get("seo_title", ""), url)
    p["meta_description"] = clean_text(p.get("meta_description", ""), url)
    p["breadcrumb"] = clean_text(p.get("breadcrumb", ""), url)
    return p

leftovers = []
for p in vol_pages:
    clean_page(p)
raw = json.dumps(vol_pages, ensure_ascii=False)
for m in re.finditer(r"【[^】]*】", raw):
    leftovers.append(m.group(0))
if leftovers:
    print("LEFTOVER PLACEHOLDERS:", sorted(set(leftovers)))
    sys.exit(1)
print("placeholder cleanup: OK (no 【…】 remains in 602 volume pages)")

# ---------------------------------------------------------------- crumb resolver
crumb_index = {}  # after pages built: name -> url

# ---------------------------------------------------------------- related/cards builders
def related_for(p, page_by_url):
    t = p["template"]
    rel, cards = [], []

    if t == "services_hub":
        cards = [{"title": TOWERS[k]["name"], "url": tower_url(k), "tag": "Tower",
                  "desc": TOWERS[k]["tagline"]} for k in TOWER_ORDER]
    elif t == "tower_hub":
        key = next(k for k in TOWER_ORDER if TOWERS[k]["slug"] in p["url"])
        cards = [{"title": s["name"], "url": service_url(s), "tag": "Service",
                  "desc": s["promise"]} for s in services_by_tower.get(key, [])]
        rel = [{"title": TOWERS[k]["name"], "url": tower_url(k), "desc": TOWERS[k]["tagline"]}
               for k in TOWER_ORDER if k != key][:4]
    elif t == "service_page":
        s = next(x for x in SERVICES if service_url(x) == p["url"])
        siblings = [x for x in services_by_tower[s["tower"]] if x["id"] != s["id"]][:4]
        rel = [{"title": "Tower overview — " + TOWERS[s["tower"]]["name"], "url": tower_url(s["tower"]),
                "desc": TOWERS[s["tower"]]["tagline"]}]
        rel += [{"title": cap_title(IND_ORDER[i], s["tower"]), "url": cap_url(IND_ORDER[i], s["tower"]),
                 "desc": INDUSTRIES[IND_ORDER[i]]["tagline"]} for i in range(4)]
        for c in [c for c in CASES if s["tower"] in c["towers"]][:2]:
            rel.append({"title": c["client"], "url": case_url(c), "desc": c["headline"]})
        cards = [{"title": x["name"], "url": service_url(x), "tag": "Same tower",
                  "desc": x["promise"]} for x in siblings]
    elif t == "industries_hub":
        cards = [{"title": INDUSTRIES[k]["name"], "url": ind_url(k), "tag": "Industry",
                  "desc": INDUSTRIES[k]["tagline"]} for k in IND_ORDER]
    elif t == "industry_hub":
        key = next(k for k in IND_ORDER if INDUSTRIES[k]["slug"] in p["url"])
        cards = [{"title": sub["name"], "url": sub_url(sub), "tag": "Sub-industry",
                  "desc": sub["intro"][:110] + "…"} for sub in subs_by_ind.get(key, [])]
        rel = [{"title": cap_title(key, k), "url": cap_url(key, k), "desc": TOWERS[k]["tagline"]}
               for k in TOWER_ORDER]
        rel += [{"title": c["client"], "url": case_url(c), "desc": c["headline"]}
                for c in cases_by_ind.get(key, [])[:4]]
    elif t == "subindustry_page":
        sub = next(v for v in SUBS.values() if sub_url(v) == p["url"])
        key = sub["industry"]
        cards = [{"title": subcap_title(sub, k), "url": subcap_url(sub, k), "tag": "Capability",
                  "desc": TOWERS[k]["tagline"]} for k in TOWER_ORDER]
        rel = [{"title": INDUSTRIES[key]["name"] + " — industry hub", "url": ind_url(key),
                "desc": INDUSTRIES[key]["tagline"]}]
        rel += [{"title": sib["name"], "url": sub_url(sib), "desc": sib["intro"][:110] + "…"}
                for sib in subs_by_ind[key] if sib["slug"] != sub["slug"]][:3]
        rel += [{"title": c["client"], "url": case_url(c), "desc": c["headline"]}
                for c in cases_by_ind.get(key, [])[:3]]
    elif t == "industry_capability":
        m = re.match(r"/industries/([^/]+)/capabilities/([^/]+)/", p["url"])
        ind_key = next(k for k in IND_ORDER if INDUSTRIES[k]["slug"] == m.group(1))
        t_key = next(k for k in TOWER_ORDER if TOWERS[k]["slug"] == m.group(2))
        sub_list = subs_by_ind.get(ind_key, [])
        cards = [{"title": subcap_title(s, t_key), "url": subcap_url(s, t_key), "tag": "Sub-industry depth",
                  "desc": TOWERS[t_key]["tagline"]} for s in sub_list]
        rel = [{"title": "Service page — " + TOWERS[t_key]["name"], "url": tower_url(t_key),
                "desc": TOWERS[t_key]["tagline"]},
               {"title": INDUSTRIES[ind_key]["name"] + " — industry hub", "url": ind_url(ind_key),
                "desc": INDUSTRIES[ind_key]["tagline"]}]
        rel += [{"title": cap_title(ind_key, k), "url": cap_url(ind_key, k), "desc": TOWERS[k]["tagline"]}
                for k in TOWER_ORDER if k != t_key][:4]
    elif t == "sub_capability":
        m = re.match(r"/industries/([^/]+)/([^/]+)/capabilities/([^/]+)/", p["url"])
        ind_key = next(k for k in IND_ORDER if INDUSTRIES[k]["slug"] == m.group(1))
        sub = next(v for v in SUBS.values() if v["slug"] == m.group(2))
        t_key = next(k for k in TOWER_ORDER if TOWERS[k]["slug"] == m.group(3))
        rel = [{"title": "Parent capability — " + cap_title(ind_key, t_key), "url": cap_url(ind_key, t_key),
                "desc": INDUSTRIES[ind_key]["tagline"]},
               {"title": "Service page — " + TOWERS[t_key]["name"], "url": tower_url(t_key),
                "desc": TOWERS[t_key]["tagline"]},
               {"title": sub["name"] + " — sub-industry hub", "url": sub_url(sub),
                "desc": sub["intro"][:110] + "…"}]
        rel += [{"title": subcap_title(sub, k), "url": subcap_url(sub, k), "desc": TOWERS[k]["tagline"]}
                for k in TOWER_ORDER if k != t_key][:4]
    elif t == "solutions_hub":
        cards = [{"title": s[2], "url": sol_url(s[0]), "tag": s[1].title(), "desc": s[3]}
                 for s in SOLUTIONS]
    elif t == "solution_page":
        s = next(x for x in SOLUTIONS if sol_url(x[0]) == p["url"])
        rel = [{"title": "Solutions overview", "url": "/solutions/", "desc": "24 outcome-linked solutions in four categories."}]
        rel += [{"title": x[2], "url": sol_url(x[0]), "desc": x[3]}
                for x in sols_by_cat[s[1]] if x[0] != s[0]][:4]
        cards = [{"title": x[2], "url": sol_url(x[0]), "tag": s[1].title(), "desc": x[3]}
                 for x in sols_by_cat[s[1]] if x[0] != s[0]][:4]
    elif t == "platforms_hub":
        cards = [{"title": p2[1] + " — " + p2[3], "url": plat_overview_url(p2), "tag": "Platform",
                  "desc": p2[3]} for p2 in PLATFORMS]
    elif t in ("platform_overview", "platform_architecture", "platform_usecases"):
        p2 = next(x for x in PLATFORMS if x[0] in p["url"])
        rel = [{"title": p2[1] + " — Overview", "url": plat_overview_url(p2), "desc": p2[3]},
               {"title": p2[1] + " — Architecture & Trust", "url": f"/platforms/{p2[0]}/architecture/",
                "desc": "Architecture, controls and evidence trails."},
               {"title": p2[1] + " — Industry Use Cases", "url": f"/platforms/{p2[0]}/use-cases/",
                "desc": "Where the platform is in production."}]
        rel += [{"title": c["client"], "url": case_url(c), "desc": c["headline"]}
                for c in CASES if p2[1] in c["platforms"]][:4]
    elif t == "cases_hub":
        cards = [{"title": c["client"], "url": case_url(c), "tag": INDUSTRIES[c["industry"]]["name"],
                  "desc": c["headline"]} for c in CASES]
    elif t == "case_study":
        c = next(x for x in CASES if case_url(x) == p["url"])
        rel = [{"title": INDUSTRIES[c["industry"]]["name"] + " — industry hub", "url": ind_url(c["industry"]),
                "desc": INDUSTRIES[c["industry"]]["tagline"]}]
        rel += [{"title": "Tower — " + TOWERS[k]["name"], "url": tower_url(k), "desc": TOWERS[k]["tagline"]}
                for k in c["towers"][:2]]
        rel += [{"title": x["client"], "url": case_url(x), "desc": x["headline"]}
                for x in cases_by_ind[c["industry"]] if x["id"] != c["id"]][:2]
    elif t == "insights_hub":
        cards = [{"title": "Insights: " + TOWERS[k]["short"], "url": f"/insights/{k}/",
                  "tag": "Category", "desc": TOWERS[k]["tagline"]} for k in TOWER_ORDER]
    elif t == "insights_category":
        slug = re.match(r"/insights/([^/]+)/", p["url"]).group(1)
        key = next(k for k in TOWER_ORDER if TOWERS[k]["slug"] == slug)
        cards = [{"title": i[2], "url": ins_url(i), "tag": TOWERS[key]["short"], "desc": i[3]}
                 for i in ins_by_cat.get(key, [])]
        rel = [{"title": "Tower — " + TOWERS[key]["name"], "url": tower_url(key),
                "desc": TOWERS[key]["tagline"]}]
    elif t == "insight_article":
        i = INS_BY_URL[p["url"]]
        rel = [{"title": "Category — " + TOWERS[i[1]]["short"], "url": f"/insights/{i[1]}/",
                "desc": TOWERS[i[1]]["tagline"]},
               {"title": "Tower — " + TOWERS[i[1]]["name"], "url": tower_url(i[1]),
                "desc": TOWERS[i[1]]["tagline"]}]
        rel += [{"title": x[2], "url": ins_url(x), "desc": x[3]}
                for x in ins_by_cat[i[1]] if x[0] != i[0]][:3]
    elif t == "company_page":
        company_urls = ["/about-us/", "/why-achala-soft/", "/leadership/", "/global-offices/",
                        "/values-culture/", "/careers/", "/newsroom/", "/partner-ecosystem/"]
        u = p["url"]
        if u == "/leadership/":
            cards = [{"title": r[0], "url": f"/leadership/{r[1]}/", "tag": "Executive office",
                      "desc": r[3]} for r in np.LEADER]
        elif u == "/careers/":
            cards = [{"title": t, "url": f"/careers/{s}/", "tag": "Careers", "desc": b}
                     for s, t, b, _ in np.CAREERS_SUBS]
        elif u == "/newsroom/":
            cards = [{"title": t, "url": f"/newsroom/{s}/", "tag": d, "desc": b}
                     for s, t, d, b, _ in np.NEWSROOM]
        elif u == "/partner-ecosystem/":
            cards = [{"title": nm, "url": f"/partner-ecosystem/{s}/", "tag": "Alliance in validation", "desc": f}
                     for s, nm, f, _, _, _ in np.PARTNERS]
        else:
            cards = []
        rel = [{"title": x["title"], "url": x["url"], "desc": ""}
               for x in vol_pages if x["template"] == "company_page" and x["url"] != u]
        if u == "/leadership/":
            rel = rel  # already have cards; keep company rail
        rel += [{"title": "Contact Achala IT Solutions", "url": "/contact/", "desc": "Book a briefing or a value assessment."}]
    elif t == "approach_page":
        rel = [{"title": x["title"], "url": x["url"], "desc": ""}
               for x in vol_pages if x["template"] == "approach_page" and x["url"] != p["url"]]
        rel += [{"title": "Why Achala IT Solutions — The Achala Edge", "url": "/why-achala-soft/", "desc": "The proof points behind the method."}]
    elif t == "contact_page":
        rel = [{"title": x["title"], "url": x["url"], "desc": ""}
               for x in vol_pages if x["template"] == "contact_page" and x["url"] != p["url"]]
    elif t == "legal_page":
        rel = [{"title": x["title"], "url": x["url"], "desc": ""}
               for x in vol_pages if x["template"] == "legal_page" and x["url"] != p["url"]][:5]
    elif t == "leadership_profile":
        r = next(x for x in np.LEADER if x[1] in p["url"])
        rel = [{"title": "Leadership — overview", "url": "/leadership/", "desc": "The eight offices that run the firm."}]
        rel += [{"title": x[0], "url": f"/leadership/{x[1]}/", "desc": x[3]}
                for x in np.LEADER if x[1] != r[1]][:4]
        rel += [{"title": "About Achala IT Solutions", "url": "/about-us/", "desc": "The firm in numbers."},
                {"title": "Contact Achala IT Solutions", "url": "/contact/", "desc": "Book a briefing."}]
        cards = [{"title": "Values & Culture", "url": "/values-culture/", "tag": "Company",
                  "desc": "Outcomes over output; evidence first; engineered autonomy."},
                 {"title": "Careers at Achala IT Solutions", "url": "/careers/", "tag": "Careers",
                  "desc": "Evidence-based hiring across four delivery centers."}]
    elif t == "partner_page":
        r = next(x for x in np.PARTNERS if x[0] in p["url"])
        rel = [{"title": "Partner Ecosystem — overview", "url": "/partner-ecosystem/", "desc": "Alliances under one validation rule."}]
        rel += [{"title": x[1], "url": f"/partner-ecosystem/{x[0]}/", "desc": x[2]}
                for x in np.PARTNERS if x[0] != r[0]][:5]
    elif t == "careers_page":
        r = next(x for x in np.CAREERS_SUBS if x[0] in p["url"])
        rel = [{"title": "Careers — overview", "url": "/careers/", "desc": "Evidence-based hiring across four delivery centers."}]
        rel += [{"title": x[1], "url": f"/careers/{x[0]}/", "desc": x[2]}
                for x in np.CAREERS_SUBS if x[0] != r[0]]
    elif t == "newsroom_article":
        r = next(x for x in np.NEWSROOM if x[0] in p["url"])
        rel = [{"title": "Newsroom", "url": "/newsroom/", "desc": "Releases and announcements."}]
        rel += [{"title": x[1], "url": f"/newsroom/{x[0]}/", "desc": x[3]}
                for x in np.NEWSROOM if x[0] != r[0]][:4]
    return rel, cards


# ---------------------------------------------------------------- assemble all pages
all_pages = list(vol_pages) + np.new_pages()
for p in all_pages:
    clean_page(p)
assert len(all_pages) == 633, f"expected 633, got {len(all_pages)}"
assert len({p["url"] for p in all_pages}) == 633, "duplicate urls"

# crumb index: resolve names to urls
for p in all_pages:
    crumb_index[p["title"]] = p["url"]
crumb_index.update({
    "About Us": "/about-us/", "Services": "/services/", "Industries": "/industries/",
    "Solutions": "/solutions/", "Platforms": "/platforms/", "Case Studies": "/case-studies/",
    "Insights": "/insights/", "Capabilities": None, "Home": "/",
})

def build_crumbs(p):
    names = [c.strip() for c in p.get("breadcrumb", "").split(">") if c.strip()]
    if not names:
        names = ["Home", p["title"]]
    out = []
    for n in names:
        url = crumb_index.get(n)
        out.append({"name": n, "url": url})
    if out and out[-1]["url"] is None:
        out[-1]["url"] = p["url"]
    return out

page_by_url = {p["url"]: p for p in all_pages}
URL_SET = set(page_by_url.keys())

def _ok(links):
    return [l for l in links if l.get("url") in URL_SET]

for p in all_pages:
    rel, cards = related_for(p, page_by_url)
    p["crumbs"] = build_crumbs(p)
    p["related"] = _ok(rel)
    p["cards"] = _ok(cards)

# home extras
home = page_by_url["/"]
proof = next(b for b in home["blocks"] if b["t"] == "table")
stats = [{"value": r[0], "label": r[1]} for r in proof["rows"]]
featured_cases = []  # populated below
feat_cases = []
for key in ["banking", "insurance", "manufacturing"]:
    lst = cases_by_ind.get(key) or []
    if lst:
        c = lst[0]
        feat_cases.append({"title": c["client"], "url": case_url(c), "desc": c["headline"],
                           "tag": INDUSTRIES[key]["name"]})
feat_insights = [{"title": i[2], "url": ins_url(i), "desc": i[3], "tag": TOWERS[i[1]]["short"]}
                 for i in [INSIGHTS[7], INSIGHTS[11], INSIGHTS[23]]]
home["extras"] = {
    "stats": stats,
    "towers": [{"name": TOWERS[k]["name"], "url": tower_url(k), "desc": TOWERS[k]["tagline"]}
               for k in TOWER_ORDER],
    "industries": [{"name": INDUSTRIES[k]["name"], "url": ind_url(k)} for k in IND_ORDER],
    "cases": feat_cases,
    "insights": feat_insights,
    "platforms": [{"name": p2[1], "url": plat_overview_url(p2), "desc": p2[3]} for p2 in PLATFORMS],
}
# towers tagline used in home hero bullets already; fine.

# ---------------------------------------------------------------- nav.json
def col(label, url, children=None):
    return {"label": label, "url": url, "children": children or []}

mega_services = [col(TOWERS[k]["name"], tower_url(k),
                     [col(s["name"], service_url(s)) for s in services_by_tower[k]])
                 for k in TOWER_ORDER]
mega_industries = [col(INDUSTRIES[k]["name"], ind_url(k),
                       [col(s["name"], sub_url(s)) for s in subs_by_ind[k]])
                   for k in IND_ORDER]
mega_solutions = [col(SOLUTION_CATEGORIES[k], "/solutions/",
                      [col(s[2], sol_url(s[0])) for s in sols_by_cat[k]])
                  for k in SOLUTION_CATEGORIES]
mega_platforms = [col(p2[1], plat_overview_url(p2),
                      [col("Architecture & Trust", f"/platforms/{p2[0]}/architecture/"),
                       col("Industry Use Cases", f"/platforms/{p2[0]}/use-cases/")])
                  for p2 in PLATFORMS]
mega_insights = [col("Insights: " + TOWERS[k]["short"], f"/insights/{k}/") for k in TOWER_ORDER]
mega_about = [col("About Achala IT Solutions", "/about-us/"), col("Why Achala IT Solutions", "/why-achala-soft/"),
              col("Our Approach", "/our-approach/the-achala-method/",
                  [col(x["title"], x["url"]) for x in vol_pages if x["template"] == "approach_page"]),
              col("Leadership", "/leadership/"), col("Global Offices", "/global-offices/"),
              col("Values & Culture", "/values-culture/"), col("Careers", "/careers/"),
              col("Newsroom", "/newsroom/"), col("Partner Ecosystem", "/partner-ecosystem/")]

nav = {
    "primary": [
        {"label": "Services", "url": "/services/", "mega": mega_services, "wide": True},
        {"label": "Industries", "url": "/industries/", "mega": mega_industries, "wide": True},
        {"label": "Solutions", "url": "/solutions/", "mega": mega_solutions, "wide": True},
        {"label": "Platforms", "url": "/platforms/", "mega": mega_platforms, "wide": True},
        {"label": "Case Studies", "url": "/case-studies/", "mega": None},
        {"label": "Insights", "url": "/insights/", "mega": mega_insights, "wide": True},
        {"label": "About Us", "url": "/about-us/", "mega": mega_about},
    ],
    "cta": {"label": "Book a Briefing", "url": "/book-a-briefing/"},
}

footer_cols = [
    {"title": "Services", "links": [col(TOWERS[k]["short"], tower_url(k)) for k in TOWER_ORDER]},
    {"title": "Industries", "links": [col(INDUSTRIES[k]["name"], ind_url(k)) for k in IND_ORDER[:6]]
     + [col("All industries", "/industries/")]},
    {"title": "Platforms", "links": [col(p2[1], plat_overview_url(p2)) for p2 in PLATFORMS]},
    {"title": "Company", "links": [col("About Achala IT Solutions", "/about-us/"), col("Leadership", "/leadership/"),
                                   col("Careers", "/careers/"), col("Newsroom", "/newsroom/"),
                                   col("Partner Ecosystem", "/partner-ecosystem/"),
                                   col("Global Offices", "/global-offices/")]},
    {"title": "Contact & Legal", "links": [col("Contact", "/contact/"),
                                           col("Book a Briefing", "/book-a-briefing/"),
                                           col("Value Assessment", "/value-assessment/"),
                                           col("Privacy Policy", "/privacy-policy/"),
                                           col("Terms of Use", "/terms-of-use/"),
                                           col("Cookie Policy", "/cookie-policy/"),
                                           col("Accessibility", "/accessibility/")]},
]

# ---------------------------------------------------------------- brand.json
BRAND = ia.BRAND
brand = {
    "name": BRAND["name"],
    "legalName": BRAND["legal_name"],
    "tagline": BRAND["tagline"],
    "positioning": BRAND["positioning"],
    "promise": BRAND["promise"],
    "stats": [{"value": v, "label": l} for v, l in BRAND["proof_bar"]],
    "credentials": BRAND["credentials"],
    "offices": [{"title": t, "city": c, "desc": d} for t, c, d, _street in BRAND["offices"]],
    "emails": {"general": "info@achalasolutions.com", "press": "press@achalasolutions.com",
               "careers": "careers@achalasolutions.com"},
    "site": "https://www.achalasolutions.com",
}

# ---------------------------------------------------------------- SEO polish
SUFFIX = {
    "home": [],
    "tower_hub": ["Achala IT Solutions"], "service_page": ["Achala IT Solutions"],
    "services_hub": ["Achala IT Solutions"], "industries_hub": ["Achala IT Solutions"],
    "solutions_hub": ["Achala IT Solutions"], "platforms_hub": ["Achala IT Solutions"],
    "cases_hub": ["Achala IT Solutions"], "insights_hub": ["Achala IT Solutions"],
    "industry_hub": ["Industry", "Achala IT Solutions"], "subindustry_page": ["Achala IT Solutions"],
    "industry_capability": ["Achala IT Solutions"], "sub_capability": ["Achala IT Solutions"],
    "solution_page": ["Solution", "Achala IT Solutions"],
    "platform_overview": ["Achala IT Solutions"], "platform_architecture": ["Achala IT Solutions"],
    "platform_usecases": ["Achala IT Solutions"],
    "case_study": ["Case Study", "Achala IT Solutions"],
    "insight_article": ["Insight", "Achala IT Solutions"], "insights_category": ["Insights", "Achala IT Solutions"],
    "company_page": ["Achala IT Solutions"], "approach_page": ["Achala IT Solutions"],
    "contact_page": ["Achala IT Solutions"], "legal_page": ["Achala IT Solutions"],
    "leadership_profile": ["Leadership", "Achala IT Solutions"], "partner_page": ["Achala IT Solutions"],
    "careers_page": ["Careers", "Achala IT Solutions"], "newsroom_article": ["Newsroom", "Achala IT Solutions"],
}

def make_title(main, parts):
    parts = list(parts)
    while parts:
        cand = main + " | " + " | ".join(parts)
        if len(cand) <= 60:
            return cand
        parts.pop()
    if len(main) <= 60:
        return main
    return main[:57].rsplit(" ", 1)[0].rstrip(",;:") + "…"

def fix_meta(d):
    d = re.sub(r"\.{3}\s*$", "", d.strip()).rstrip()
    # last complete sentence boundary within 152 chars
    best = -1
    for m in re.finditer(r"[.] (?=[A-Z\u201c(])|\.[)\u201d]", d):
        if m.start() + 1 <= 152:
            best = m.start() + 1
    if best >= 50:
        return d[:best]
    if len(d) <= 154:
        return d if d.endswith(".") else d + "."
    cut = d[:148].rsplit(" ", 1)[0].rstrip(",;:")
    return cut + "."

for p in all_pages:
    p["seo_title"] = make_title(p["title"], SUFFIX.get(p["template"], ["Achala IT Solutions"]))
    p["meta_description"] = fix_meta(p.get("meta_description", ""))
_home = next(p for p in all_pages if p["url"] == "/")
_home["seo_title"] = "Achala IT Solutions | IT Services & Consulting for the Intelligence Era"
_home["meta_description"] = ("Achala IT Solutions engineers the intelligence layer of the enterprise — applied AI, "
                             "agentic automation, data platforms, cybersecurity and emerging compute.")

# ---------------------------------------------------------------- write outputs
os.makedirs(os.path.join(OUT, "pages"), exist_ok=True)

def fname(url):
    if url == "/":
        return "home"
    return "_".join(seg for seg in url.strip("/").split("/"))

index_rows = []
for p in all_pages:
    name = fname(p["url"])
    payload = dict(p)
    with open(os.path.join(OUT, "pages", name + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
    index_rows.append({
        "url": p["url"], "file": name, "title": p["title"], "template": p["template"],
        "section": p["section"], "l1": p.get("l1", ""), "l2": p.get("l2", ""),
        "l3": p.get("l3", ""), "l4": p.get("l4", ""),
        "seoTitle": p.get("seo_title", ""), "metaDescription": p.get("meta_description", ""),
        "words": p.get("words", 0),
    })

section_order = ["Home", "Services", "Industries", "Solutions", "Platforms", "Case Studies",
                 "Company", "Approach", "Insights", "Contact & Legal"]
index_rows.sort(key=lambda r: (section_order.index(r["section"]) if r["section"] in section_order else 99, r["url"]))
with open(os.path.join(OUT, "index.json"), "w", encoding="utf-8") as f:
    json.dump(index_rows, f, ensure_ascii=False, separators=(",", ":"))
with open(os.path.join(OUT, "nav.json"), "w", encoding="utf-8") as f:
    json.dump({"nav": nav, "footer": footer_cols}, f, ensure_ascii=False, separators=(",", ":"))
with open(os.path.join(OUT, "brand.json"), "w", encoding="utf-8") as f:
    json.dump(brand, f, ensure_ascii=False, separators=(",", ":"))

# ---------------------------------------------------------------- report
from collections import Counter
tmpl_c = Counter(r["template"] for r in index_rows)
sec_c = Counter(r["section"] for r in index_rows)
total_words = sum(r["words"] for r in index_rows)
print("pages written:", len(index_rows), "| sections:", dict(sec_c))
print("templates:", dict(tmpl_c))
print("total words:", total_words)
# verify every related url + card url + crumb url resolves
def_page_urls = {r["url"] for r in index_rows}
bad = []
for p in all_pages:
    for r in p["related"]:
        if r["url"] not in def_page_urls:
            bad.append(("related", p["url"], r["url"]))
    for c in p["cards"]:
        if c["url"] not in def_page_urls:
            bad.append(("card", p["url"], c["url"]))
    for c in p["crumbs"]:
        if c["url"] is not None and c["url"] not in def_page_urls:
            bad.append(("crumb", p["url"], c["url"]))
print("broken internal links:", len(bad))
for b in bad[:12]:
    print("  ", b)
if bad:
    sys.exit(1)
print("LINK GRAPH OK — 0 broken internal links")
