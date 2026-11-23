#!/usr/bin/env python3
"""Fix brand naming across the site: use 'Achala IT Solutions' everywhere, never
'Achala IT Solutions' / 'Achala IT Solutions' / bare 'Achala'. Also anonymize the patent KB doc.

Passes (case-sensitive, ordered):
  1. 'Achala IT Solutions'  NOT followed by 'ware'  -> 'Achala IT Solutions'
  2. 'Achala IT Solutions'   NOT followed by alnum    -> 'Achala IT Solutions'
  3. bare 'Achala'  NOT followed by alnum    -> 'Achala'   (Achala Nexus, etc.)

Never touches: lowercase domains (achalasolutions.com), emails, identifiers with
trailing alnum (AchalaFoo). Writes a replacement log to /tmp/naming_fix_log.json.
"""
import json, os, re

SRC = "/home/z/my-project/site/src"
PUB = "/home/z/my-project/site/public"
KB = "/home/z/my-project/docs/patent_knowledge_base.md"
EXTS = {".ts", ".tsx", ".js", ".jsx", ".json", ".css", ".md", ".svg", ".html"}

P1 = re.compile(r"Achala IT Solutions(?!ware)")
P2 = re.compile(r"Achala IT Solutions(?![A-Za-z0-9])")
P3 = re.compile(r"Achala(?![A-Za-z0-9])")

KB_RULES = [
    # (pattern, replacement) applied only to the KB doc
    (re.compile(r"^# Patent Knowledge Base \(8 Form 2 specs, Strategemist Global Pvt Ltd, Hyderabad — inventor Pisupati VSS Ravi Shanker\).*$", re.M),
     "# Patent Knowledge Base (8 filed specification families — private R&D programme)\n\nCONFIDENTIALITY: never name the applicant entity, its city, any inventor,\nor any filing detail anywhere on the website or in client-facing material.\nOn the site these families are referenced only as \"our research programme\",\n\"patented method families\" or by capability — never by source."),
    (re.compile(r"^- Applicant entity: Strategemist Global Pvt Ltd\. Do not claim Achala ownership of the patents in site copy\.$", re.M),
     "- Applicant identity is confidential. Never claim, deny or discuss ownership\n  on the site; capabilities may be mapped indirectly into services, solutions\n  and industries copy without naming any source."),
]

def walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {"node_modules", ".next", "out"}]
        for fn in filenames:
            if os.path.splitext(fn)[1] in EXTS:
                yield os.path.join(dirpath, fn)

log = {}
p1 = p2 = p3 = 0
for path in list(walk(SRC)) + list(walk(PUB)):
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    orig = text
    n1 = len(P1.findall(text)); text = P1.sub("Achala IT Solutions", text); p1 += n1
    n2 = len(P2.findall(text)); text = P2.sub("Achala IT Solutions", text); p2 += n2
    n3 = len(P3.findall(text)); text = P3.sub("Achala", text); p3 += n3
    if text != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        log[path] = {"p1": n1, "p2": n2, "p3": n3}

# scrub the internal KB doc (names + confidentiality rules)
if os.path.exists(KB):
    with open(KB, encoding="utf-8") as f:
        text = f.read()
    for pat, rep in KB_RULES:
        text = pat.sub(rep, text)
    with open(KB, "w", encoding="utf-8") as f:
        f.write(text)
    log[KB] = {"scrubbed": True}

with open("/tmp/naming_fix_log.json", "w") as f:
    json.dump(log, f, indent=2)
print(f"pass1 Achala IT Solutions->Achala IT Solutions: {p1}")
print(f"pass2 Achala IT Solutions->Achala IT Solutions:  {p2}")
print(f"pass3 Achala->Achala:               {p3}")
print(f"files changed: {len(log)}  (log -> /tmp/naming_fix_log.json)")
