"""Wave A2 — Achala content surgery: real facts into brand.json, home.json, about-us, contact;
platform slug remap nexus->eems etc.; patent-claim neutralization."""
import json, os, re, glob

ROOT = "/home/z/my-project/achala"
P = os.path.join(ROOT, "site/src/content/pages")

# ── 1. platform slug remap (files, URLs, names) ─────────────────────────────
PLAT = {
    "nexus":     ("eems",             "EEMS Platform",                  "AI-powered emergency response platform — dispatch, fleet readiness and field coordination for 50,000+ daily cases across 9 states."),
    "forge":     ("fms",              "Fleet Management System",        "Real-time tracking, predictive maintenance, telematics and compliance management — keeping mission-critical fleets ready."),
    "swarm":     ("kyc",              "KYC Management System",          "Document verification and face recognition that onboard customers in 5 minutes — 60% faster than manual cycles."),
    "sentinel":  ("telemedicine",     "Tele Medicine Platform",         "AI-driven remote evaluation, diagnosis and treatment — one platform for virtual care at scale."),
    "twinverse": ("bi-analytics",     "BI & Analytics Platform",        "150+ built-in dashboards for hospital operations — 25% operational-efficiency lift at KIMS Hospitals."),
    "quanta":    ("token-management", "Token Management System",        "AI-led queue and token management that cut laboratory queues by 20-30% at AIG Hospitals."),
    "ledger":    ("patient-portal",   "Patient Priority Portal",        "Self-service patient journeys — registration, pre-assessment and lab-report dispatch without the queues."),
    "compass":   ("driisti",          "Driisti — Smart Vision Glasses", "AI-enabled smart vision glasses for the visually challenged, and assistive devices for elderly care."),
}
OLD_SLUGS = list(PLAT.keys())

# 1a. rename files
renamed = 0
for old, (new, name, desc) in PLAT.items():
    for f in glob.glob(os.path.join(P, "platforms_%s*.json" % old)):
        base = os.path.basename(f)
        nb = base.replace("platforms_%s" % old, "platforms_%s" % new, 1)
        os.rename(f, os.path.join(P, nb))
        renamed += 1
print("platform files renamed:", renamed)

# 1b. global path/word replace across site/src text files
def all_text_files():
    for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, "site/src")):
        dirnames[:] = [d for d in dirnames if d not in {"node_modules", ".next", "out", ".next-export"}]
        for fn in filenames:
            if os.path.splitext(fn)[1] in {".ts", ".tsx", ".json", ".css", ".md"}:
                yield os.path.join(dirpath, fn)

count = 0
for p in all_text_files():
    try:
        t = open(p, encoding="utf-8").read()
    except Exception:
        continue
    o = t
    for old, (new, name, desc) in PLAT.items():
        t = t.replace("/platforms/%s/" % old, "/platforms/%s/" % new)
    for old, (new, name, desc) in PLAT.items():
        t = t.replace("Achala Nexus", "EEMS Platform").replace("Achala Forge", "Fleet Management System")
        t = t.replace("Achala Swarm", "KYC Management System").replace("Achala Sentinel", "Tele Medicine Platform")
        t = t.replace("Achala Twinverse", "BI & Analytics Platform").replace("Achala Quanta", "Token Management System")
        t = t.replace("Achala Ledger", "Patient Priority Portal").replace("Achala Compass", "Driisti Smart Vision Glasses")
    t = t.replace("the Achala platform portfolio", "the Achala platform portfolio")
    if t != o:
        open(p, "w", encoding="utf-8").write(t)
        count += 1
print("platform remap files touched:", count)

# 1c. stamp real names/descs on platform main pages
for old, (new, name, desc) in PLAT.items():
    f = os.path.join(P, "platforms_%s.json" % new)
    if not os.path.exists(f):
        continue
    d = json.load(open(f))
    d["title"] = name
    d["seo_title"] = "%s | Achala IT Solutions" % name
    if "blocks" in d:
        for b in d["blocks"]:
            if b.get("t") == "hero":
                b["x"] = desc
    json.dump(d, open(f, "w"), indent=1, ensure_ascii=False)
print("platform main pages stamped")

# ── 2. brand.json — the Achala fact sheet ───────────────────────────────────
brand = {
    "name": "Achala IT Solutions",
    "legalName": "Achala IT Solutions Private Limited",
    "tagline": "Transforming industries through AI acceleration",
    "positioning": "Achala IT Solutions is an AI-first, platform-driven engineering company offering full-cycle software product engineering — from POC to industrialization — for Fortune 500 enterprises, SMEs and startups across mobility, healthcare, manufacturing and financial services.",
    "promise": "AI acceleration you can measure: every solution lands with named outcomes, production-grade engineering and 24x7 operations support.",
    "stats": [
        {"value": "300+", "label": "projects delivered across mobility, healthcare, BFSI and manufacturing"},
        {"value": "95%", "label": "client retention across long-run engagements"},
        {"value": "50,000+", "label": "daily emergency cases handled by the EEMS platform across 9 states"},
        {"value": "200+", "label": "IT specialists in engineering, data, AI and quality"},
        {"value": "24x7", "label": "operations and support for mission-critical systems"},
        {"value": "2009", "label": "founded in Hyderabad — global delivery from India, Germany and Bulgaria"}
    ],
    "credentials": [
        "ISO/IEC 27001",
        "TISAX",
        "GDPR-aligned delivery",
        "NASSCOM AI Game Changers 2021 — Innovators",
        "T-AIM (Telangana AI Mission) — first cohort",
        "Sulzer GmbH strategic partnership",
    ],
    "offices": [
        {"title": "India — Headquarters", "city": "Financial District, Nanakramguda, Hyderabad", "desc": "Engineering core, AI labs and global delivery management."},
        {"title": "Germany — European Hub", "city": "Munich (c/o Sulzer GmbH)", "desc": "Automotive and manufacturing delivery for European clients."},
        {"title": "Bulgaria — EU Delivery Center", "city": "Sofia (Achala Sulzer Ltd.)", "desc": "European shoring model with Sulzer GmbH partnership."},
    ],
    "emails": {
        "general": "info@achalasolutions.com",
        "press": "info@achalasolutions.com",
        "careers": "info@achalasolutions.com",
    },
    "phones": {"inquiries": "+91 7337444922", "hr": "+91 9030015539"},
    "social": {
        "linkedin": "https://www.linkedin.com/company/achala-it-solutions-pvt-ltd/",
        "facebook": "https://www.facebook.com/Achala-it-Solutions-Pvt-Ltd-2009-100557234648701/",
        "twitter": "https://twitter.com/AchalaIt",
        "instagram": "https://www.instagram.com/achala_itsolutions/",
    },
    "site": "https://www.achalasolutions.com",
    "brandTokens": {
        "palette": {
            "brand": "#d20000",
            "brandHover": "#a80000",
            "brandDeep": "#8f0000",
            "brandTextOnDark": "#ff9d96",
            "brandTint": "#fdecec",
            "steel950": "#0e2230",
            "steel900": "#16334a",
            "steel800": "#2b5672",
            "steel700": "#3a6983",
            "steel600": "#477a95",
            "steel500": "#568aa6",
            "mist": "#f5f8fa",
            "line": "#e3e8ec",
            "body": "#4a5a66"
        },
        "logoAssets": {
            "full": "/achala-logo.png",
            "reversed": "/achala-logo-white.png",
            "mono": "/achala-logo-mono.png",
            "favicon": "/icon.svg",
            "ogImage": "/og-default.png"
        },
        "usageRules": [
            "Brand red #d20000 is the accent: keep to roughly 10% of any view",
            "On white, red text only via brandDeep #8f0000 at 18px+ bold; body-safe red on steel blue is #ff9d96",
            "Primary buttons: solid brand red with white bold label; hover #a80000",
            "Dark surfaces use the steel-blue ramp (#0e2230 - #568aa6)",
            "Logo: use the approved artwork as provided; never recolor, stretch, shadow or rotate"
        ]
    }
}
json.dump(brand, open(os.path.join(ROOT, "site/src/content/brand.json"), "w"), indent=1, ensure_ascii=False)
print("brand.json rewritten")

# ── 3. home.json extras — real stats + real platforms ───────────────────────
hf = os.path.join(P, "home.json")
home = json.load(open(hf))
home["seo_title"] = "Achala IT Solutions | AI-Driven IT Solutions & Digital Engineering"
home["meta_description"] = "Achala IT Solutions is an AI-first, platform-driven engineering company — transforming industries through AI acceleration for mobility, healthcare, manufacturing and financial services. 300+ projects · 95% client retention · ISO/IEC 27001."
home["title"] = "Home"
ex = home.get("extras", {})
ex["stats"] = brand["stats"]
ex["platforms"] = [
    {"name": name, "url": "/platforms/%s/" % new, "desc": desc}
    for old, (new, name, desc) in PLAT.items()
]
home["extras"] = ex
json.dump(home, open(hf, "w"), indent=1, ensure_ascii=False)
print("home.json extras rewritten — platforms:", len(ex["platforms"]))

# ── 4. about-us.json — the real Achala story ────────────────────────────────
about = {
    "id": "CO-about",
    "title": "About Achala IT Solutions",
    "url": "/about-us/",
    "template": "company_page",
    "breadcrumb": "About Us > About Achala IT Solutions",
    "seo_title": "About Achala IT Solutions | AI-First, Platform-Driven Engineering",
    "meta_description": "Achala IT Solutions Private Limited — founded in 2009 in Hyderabad, an AI-first, platform-driven engineering company with global delivery from India, Germany and Bulgaria. 300+ projects, 95% client retention.",
    "blocks": [
        {"t": "hero", "x": "Achala IT Solutions Private Limited, founded in 2009, is a leading AI-first solutions and platform-driven company offering full-cycle software product engineering services. Headquartered in Hyderabad with global presence in Munich and Sofia, we empower Fortune 500 enterprises, SMEs and startups."},
        {"t": "p", "x": "Achala was built on a simple conviction: industries transform when AI moves out of the lab and into production. That is why our teams own the whole arc — from proof-of-concept to industrialization — across generative AI, ML, data and analytics engineering, quality engineering, connected devices and IoT, design engineering, mobile application development and DevOps."},
        {"t": "p", "x": "Today our platforms run in production where failure is not an option: the EEMS platform handles 50,000+ daily emergency cases across 9 states, our KYC systems verify customers in under 5 minutes, hospital BI deployments at KIMS Hospitals deliver 150+ dashboards, and our telematics work has optimized workforce efficiency by up to 40% for automotive clients."},
        {"t": "p", "x": "We are recognized as Innovators in the NASSCOM #AI Game Changers 2021 program and were selected for the first cohort of the Telangana AI Mission (T-AIM) revv-up accelerator. In partnership with Sulzer GmbH — one of the 25 largest IT service providers in the German automotive industry — we operate Achala Sulzer Ltd. in Sofia, offering clients flexible and global shoring models."},
        {"t": "h2", "x": "Vision and mission"},
        {"t": "p", "x": "Vision: empowering next-generation businesses to unlock the full potential of the digital landscape through our expertise in data, apps and analytics, supported by cutting-edge technologies like AI, ML, IoT, Cloud and Mobility in the Industry 4.0 era."},
        {"t": "p", "x": "Mission: to revolutionize the digital landscape through innovative AI-driven solutions and platform-driven services, empowering businesses worldwide to thrive in the age of technology."},
        {"t": "h2", "x": "Facts"},
        {"t": "table", "caption": "Achala IT Solutions at a glance", "headers": ["Dimension", "Detail"],
         "rows": [
            ["Founded", "2009, Hyderabad, India"],
            ["People", "300+ employees, including 200+ IT specialists"],
            ["Global presence", "Hyderabad (HQ) · Munich, Germany · Sofia, Bulgaria"],
            ["Projects", "300+ delivered; 95% client retention"],
            ["Flagship platforms", "EEMS, Fleet Management System, KYC Management System, Tele Medicine, BI & Analytics, Token Management, Patient Priority Portal, Driisti Smart Vision Glasses"],
            ["Recognitions", "NASSCOM AI Game Changers 2021 (Innovators) · T-AIM first cohort"],
            ["Credentials", "ISO/IEC 27001 · TISAX · GDPR-aligned delivery"],
         ]},
        {"t": "h2", "x": "Management team"},
        {"t": "table", "caption": "Leadership", "headers": ["Name", "Role", "Background"],
         "rows": [
            ["Rajesh Raju", "CEO & Co-Founder", "25+ years in technology and consulting. Founder of Achala IT Solutions in 2009. Bachelors in Mechanical Engineering from IIT Madras; MBA from the University of Chicago Booth. Management consulting experience with Fortune 500 clients across product marketing, new product innovation, M&A and BPO."],
            ["Jyotish Vegesna", "COO & Co-Founder", "13+ years in technology, consulting, product development and operations across automotive, fintech and healthcare. Bachelors in Information Technology from SRKR Engineering College. Also COO of Achala Health and Achala Sulzer Ltd."],
            ["Venkat Paturu", "Vice President, Software Engineering", "Leads engineering organization and delivery pods."],
            ["Sandeep Puli", "Vice President, Product & Startup Management", "Product strategy and startup engagements."],
            ["Satish Malla", "Vice President, Human Resources", "People, culture and talent operations."],
            ["Srinivas Adur", "Vice President, Quality and Automation", "Quality engineering, test automation and delivery assurance."],
            ["Vijay Saradhy Kotra", "Vice President, Product Management (APAC)", "Product management for APAC engagements."],
            ["Ankit Gujrati", "Vice President, SAP & Mainframes", "Enterprise core systems and SAP practice."],
         ]},
        {"t": "h2", "x": "How we engage"},
        {"t": "bullets", "items": [
            ["POC to industrialization", "We take AI solutions from proof-of-concept to production-grade platforms — the full arc, not a demo."],
            ["Platform-first delivery", "Flagship platforms — EEMS, FMS, KYC, Tele Medicine, BI — arrive configured, then tailored to your estate."],
            ["Global shoring with Sulzer", "Flexible delivery across Hyderabad, Munich and Sofia under a fair-partnership continuity model."],
            ["24x7 operations", "Mission-critical systems stay mission-critical: round-the-clock support with audited SLAs."],
            ["Compliance-ready engineering", "ISO/IEC 27001, TISAX and GDPR-aligned practices built into delivery for automotive and regulated clients."],
        ]},
    ],
}
json.dump(about, open(os.path.join(P, "about-us.json"), "w"), indent=1, ensure_ascii=False)
print("about-us.json rewritten")

# ── 5. contact.json — real offices, phones, emails, socials ─────────────────
contact = {
    "id": "CO-contact",
    "title": "Contact Achala IT Solutions",
    "url": "/contact/",
    "template": "contact_page",
    "breadcrumb": "Contact > Contact Achala IT Solutions",
    "seo_title": "Contact Achala IT Solutions | Hyderabad · Munich · Sofia",
    "meta_description": "Reach Achala IT Solutions: +91 7337444922, info@achalasolutions.com. Offices in Hyderabad (India), Munich (Germany) and Sofia (Bulgaria).",
    "blocks": [
        {"t": "hero", "x": "Tell us what you are building. A practice lead — not a call-center — replies with the fastest path from POC to production."},
        {"t": "h2", "x": "Offices"},
        {"t": "table", "caption": "Achala IT Solutions locations", "headers": ["Office", "Address"],
         "rows": [
            ["India — Headquarters", "Achala IT Solutions Private Limited, Floor 10, 285 FD by Phoenix, Financial District, Nanakramguda, Hyderabad, Telangana 500089"],
            ["India — Registered office", "Achala IT Solutions Private Limited, 3rd Floor, Plot No 342 & 343, Road Number 7, Kakateeya Hills, Hyderabad, Telangana 500081"],
            ["Germany", "Achala GmbH, C/O Sulzer GmbH, Frankfurter Ring 162, 80807 Munich, Germany"],
            ["Bulgaria", "Achala Sulzer Ltd., MHQ Building, 115 Tsarigradsko Shose Blvd, Floor 3, Sofia 1784, Bulgaria"],
         ]},
        {"t": "h2", "x": "Talk to us"},
        {"t": "bullets", "items": [
            ["Inquiries", "+91 7337444922"],
            ["Human resources", "+91 9030015539"],
            ["Email", "info@achalasolutions.com"],
            ["Achala Sulzer", "info@achalasulzer.eu"],
        ]},
        {"t": "h2", "x": "Follow Achala"},
        {"t": "bullets", "items": [
            ["LinkedIn", "https://www.linkedin.com/company/achala-it-solutions-pvt-ltd/"],
            ["Facebook", "https://www.facebook.com/Achala-it-Solutions-Pvt-Ltd-2009-100557234648701/"],
            ["X (Twitter)", "https://twitter.com/AchalaIt"],
            ["Instagram", "https://www.instagram.com/achala_itsolutions/"],
        ]},
        {"t": "p", "x": "Prefer email? Write to info@achalasolutions.com and a practice lead will respond within one business day. For partnership and press queries, use the same address with the subject line you prefer — we route it internally."},
    ],
}
# preserve any existing template-specific fields not in blocks (e.g. form config)
try:
    old = json.load(open(os.path.join(P, "contact.json")))
    for k, v in old.items():
        if k not in contact and k not in ("blocks", "seo_title", "meta_description", "title"):
            contact[k] = v
except Exception:
    pass
json.dump(contact, open(os.path.join(P, "contact.json"), "w"), indent=1, ensure_ascii=False)
print("contact.json rewritten")

# ── 6. patent-claim neutralization in content ───────────────────────────────
n = 0
for p in glob.glob(os.path.join(P, "*.json")):
    try:
        t = open(p, encoding="utf-8").read()
    except Exception:
        continue
    o = t
    t = t.replace("Patented methods — proven in production", "AI accelerators — proven in production")
    t = re.sub(r"patented method famil(y|ies)", r"proprietary method famil\1", t, flags=re.I)
    t = t.replace("Patented method families", "Proprietary method families")
    t = t.replace("patented-IP differential", "acceleration differential")
    t = t.replace("patented IP", "proprietary IP")
    t = t.replace("Patent ", "Method family ")
    if t != o:
        open(p, "w", encoding="utf-8").write(t)
        n += 1
print("patent-claim neutralization files:", n)

# ── 7. residual check ───────────────────────────────────────────────────────
bad = []
for f in glob.glob(os.path.join(P, "*.json")):
    t = open(f, encoding="utf-8", errors="ignore").read()
    for term in ["Tysons", "2,400", "350+ enterprise", "2016", "Riyadh", "Solvay"]:
        if term in t:
            bad.append((os.path.basename(f), term))
print("fact-residue flags:", bad[:12] if bad else "none in pages dir")
