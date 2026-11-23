"""Wave A3 — residual fact fixes: offices, leadership, delivery model, credentials."""
import json, os, glob, re

ROOT = "/home/z/my-project/achala"
P = os.path.join(ROOT, "site/src/content/pages")

def load(fn):
    return json.load(open(os.path.join(P, fn)))

def save(fn, d):
    json.dump(d, open(os.path.join(P, fn), "w"), indent=1, ensure_ascii=False)

OFFICE_ROWS = [
    ["India — Headquarters", "Achala IT Solutions Private Limited, Floor 10, 285 FD by Phoenix, Financial District, Nanakramguda, Hyderabad, Telangana 500089"],
    ["India — Registered office", "3rd Floor, Plot No 342 & 343, Road Number 7, Kakateeya Hills, Hyderabad, Telangana 500081"],
    ["Germany — European Hub", "Achala GmbH, C/O Sulzer GmbH, Frankfurter Ring 162, 80807 Munich, Germany"],
    ["Bulgaria — EU Delivery Center", "Achala Sulzer Ltd., MHQ Building, 115 Tsarigradsko Shose Blvd, Floor 3, Sofia 1784, Bulgaria"],
]

# 1. global-offices.json
d = load("global-offices.json")
patched_tables = 0
for b in d.get("blocks", []):
    if b.get("t") == "table":
        if b.get("headers") and b["headers"][0] in ("Office", "Region", "Location", "Dimension"):
            b["rows"] = OFFICE_ROWS
            b["headers"] = ["Office", "Address"]
            patched_tables += 1
    if b.get("t") == "hero" and ("four delivery" in b.get("x", "") or "Tysons" in b.get("x", "")):
        b["x"] = "Achala IT Solutions delivers from three global locations — Hyderabad (India HQ), Munich (Germany) and Sofia (Bulgaria) — combining India-scale engineering with European proximity through our Sulzer GmbH partnership."
if patched_tables == 0:
    d["blocks"].append({"t": "table", "caption": "Achala IT Solutions locations", "headers": ["Office", "Address"], "rows": OFFICE_ROWS})
d["meta_description"] = "Achala IT Solutions delivers from Hyderabad (India HQ), Munich (Germany) and Sofia (Bulgaria). Contact: +91 7337444922 · info@achalasolutions.com."
save("global-offices.json", d)
print("global-offices rewritten, tables patched:", patched_tables)

# 2. leadership.json
d = load("leadership.json")
for b in d.get("blocks", []):
    if b.get("t") == "hero":
        b["x"] = "The leadership of Achala IT Solutions Private Limited — founded in 2009 by engineers and consultants who still run delivery today."
    if b.get("t") == "table":
        b["caption"] = "Management team"
        b["headers"] = ["Name", "Role", "Background"]
        b["rows"] = [
            ["Rajesh Raju", "CEO & Co-Founder", "25+ years in technology and consulting. Founder of Achala IT Solutions in 2009. B.E. Mechanical Engineering, IIT Madras; MBA, University of Chicago Booth. Management consulting experience with Fortune 500 clients across product marketing, innovation, M&A and BPO."],
            ["Jyotish Vegesna", "COO & Co-Founder", "13+ years across technology, consulting, product development and operations in automotive, fintech and healthcare. B.Tech Information Technology, SRKR Engineering College. Also COO of Achala Health and Achala Sulzer Ltd."],
            ["Venkat Paturu", "Vice President, Software Engineering", "Leads the engineering organization and delivery pods across all practices."],
            ["Sandeep Puli", "Vice President, Product & Startup Management", "Product strategy and startup engagements."],
            ["Satish Malla", "Vice President, Human Resources", "People, culture and talent operations."],
            ["Srinivas Adur", "Vice President, Quality and Automation", "Quality engineering, test automation and delivery assurance."],
            ["Vijay Saradhy Kotra", "Vice President, Product Management (APAC)", "Product management for APAC engagements."],
            ["Ankit Gujrati", "Vice President, SAP & Mainframes", "Enterprise core systems and the SAP practice."],
        ]
    if b.get("t") == "p" and "2,400" in b.get("x", ""):
        b["x"] = "A 300-strong team — including 200+ IT specialists — led by practicing engineers: the people who sign the engagement are the people who run it."
d["seo_title"] = "Leadership Team | Achala IT Solutions"
d["meta_description"] = "Meet the leadership of Achala IT Solutions: CEO Rajesh Raju and COO Jyotish Vegesna, with the vice presidents who run engineering, quality, HR, product and the SAP practice."
save("leadership.json", d)
print("leadership rewritten")

# 3. delivery-model + home + newsroom: contextual patches
def patch(fn, repls):
    f = os.path.join(P, fn)
    if not os.path.exists(f):
        return 0
    t = open(f, encoding="utf-8").read()
    o = t
    for a, b in repls:
        t = t.replace(a, b)
    if t != o:
        open(f, "w", encoding="utf-8").write(t)
        return 1
    return 0

GEN = [
    ("Tysons Corner, Virginia, USA", "Hyderabad, Telangana, India"),
    ("Tysons Corner", "Hyderabad"),
    ("United States — Global Headquarters", "India — Global Headquarters"),
    ("United States — global headquarters", "India — global headquarters"),
    ("United Kingdom — European Hub", "Germany — European Hub"),
    ("London, United Kingdom", "Munich, Germany"),
    ("Kingdom of Saudi Arabia — Growth Engine", "Bulgaria — EU Delivery Center"),
    ("Riyadh (KAFD), Saudi Arabia", "Sofia, Bulgaria (Achala Sulzer Ltd.)"),
    ("Saudi Arabia", "Bulgaria"),
    ("Vision 2030 programs, sovereign delivery, smart-city and energy practices", "European shoring model with Sulzer GmbH — automotive and manufacturing delivery."),
    ("Strategic leadership, board advisory, quantum and advanced compute practices", "AI labs, platform engineering and global delivery management."),
    ("European delivery, DORA and regulatory programs, financial services practice", "Automotive and manufacturing delivery for European clients."),
    ("India — Global Execution Core", "India — Headquarters & Global Delivery"),
    ("four global delivery centers", "global delivery centers in Hyderabad, Munich and Sofia"),
    ("across four delivery centers", "across global delivery centers in Hyderabad, Munich and Sofia"),
    ("2,400+ engineers, scientists and domain specialists", "300+ employees, including 200+ IT specialists"),
    ("2,400+ engineers", "300+ engineers and specialists"),
    ("2,400+", "300+"),
    ("350+ delivered across 40+ countries", "300+ projects delivered for global clients"),
    ("350+ enterprise engagements delivered", "300+ projects delivered"),
    ("40+ countries served from 4 global delivery centers", "global delivery from India, Germany and Bulgaria"),
    ("founded in 2016, incorporated in the United States", "founded in 2009 in Hyderabad, India"),
    ("Founded", "Founded"),
    ("2016, incorporated in the United States", "2009, Hyderabad, India"),
    ("SOC 2 Type II", "ISO/IEC 27001"),
    ("SOC 2-audited", "ISO/IEC 27001-certified"),
    ("HIPAA-ready delivery pods", "GDPR-aligned delivery pods"),
    ("HIPAA-ready", "GDPR-aligned"),
]
patched = 0
for f in glob.glob(os.path.join(P, "*.json")):
    bn = os.path.basename(f)
    if bn in ("about-us.json", "contact.json", "global-offices.json", "leadership.json", "home.json"):
        continue
    t = open(f, encoding="utf-8").read()
    o = t
    for a, b in GEN:
        t = t.replace(a, b)
    if t != o:
        open(f, "w", encoding="utf-8").write(t)
        patched += 1
print("generic fact patches across", patched, "page files")

# 4. home.json blocks (already extras-rewritten; blocks may carry old facts)
t = open(os.path.join(P, "home.json"), encoding="utf-8").read()
o = t
for a, b in GEN:
    t = t.replace(a, b)
if t != o:
    open(os.path.join(P, "home.json"), "w", encoding="utf-8").write(t)
print("home.json blocks patched:", t != o)

# 5. residual scan
bad = []
for f in glob.glob(os.path.join(P, "*.json")):
    t = open(f, encoding="utf-8", errors="ignore").read()
    for term in ["Tysons", "Riyadh", "2,400", "incorporated in the United States", "KAFD"]:
        if term in t:
            bad.append((os.path.basename(f), term))
print("residual flags:", bad if bad else "NONE — pages clean")
