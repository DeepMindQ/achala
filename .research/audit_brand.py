"""Audit the achala clone for every brand string, color, domain, contact detail that must change."""
import os, re, json
from collections import Counter

ROOT = "/home/z/my-project/achala"
SCAN_DIRS = ["site/src", "site/public", "scripts", ".github"]
SKIP_DIR_PARTS = {"node_modules", ".next", "out", "out-gh", ".next-export", ".research", "tsbuildinfo"}
TEXT_EXT = {".ts", ".tsx", ".js", ".json", ".css", ".html", ".md", ".txt", ".yml", ".yaml", ".py", ".xml", ".webmanifest"}

PATTERNS = [
    ("brand_Dataq Software", re.compile(r"Dataq Software", re.I)),
    ("brand_DataQ_bare", re.compile(r"\bDataQ\b")),
    ("brand_dataqsoft_domain", re.compile(r"dataqsoft\.com", re.I)),
    ("brand_DataQ_path", re.compile(r"/DataQ\b")),
    ("color_orange_FE5722", re.compile(r"#FE5722", re.I)),
    ("color_navy_18142D", re.compile(r"#18142D", re.I)),
    ("color_orange_siblings", re.compile(r"#(?:FE|FF)57(?:2|3)[0-9A-Fa-f]|fe572[0-9a-f]", re.I)),
    ("contact_info_dataqsoft", re.compile(r"info@dataqsoft\.com", re.I)),
    ("deepmindq_host", re.compile(r"deepmindq\.github\.io", re.I)),
    ("strategemist_leak", re.compile(r"Strategemist|Pisupati|Ravi Shanker", re.I)),
]

hits = {name: [] for name, _ in PATTERNS}
files_scanned = 0
for scan_root in SCAN_DIRS:
    base = os.path.join(ROOT, scan_root)
    if not os.path.isdir(base):
        continue
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_PARTS and not d.endswith("tsbuildinfo")]
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext not in TEXT_EXT:
                continue
            p = os.path.join(dirpath, fn)
            try:
                if os.path.getsize(p) > 3_000_000:
                    continue
                text = open(p, "rb").read().decode("utf-8", errors="ignore")
            except Exception:
                continue
            files_scanned += 1
            rel = os.path.relpath(p, ROOT)
            for name, pat in PATTERNS:
                n = len(pat.findall(text))
                if n:
                    hits[name].append((rel, n))

print("files scanned:", files_scanned)
total = 0
for name, items in hits.items():
    c = sum(n for _, n in items)
    total += c
    print("\n== %s : %d occurrences in %d files ==" % (name, c, len(items)))
    for rel, n in sorted(items, key=lambda x: -x[1])[:18]:
        print("   %4d  %s" % (n, rel))
    if len(items) > 18:
        print("   ... +%d more files" % (len(items) - 18))

# also list image/asset files in public that look like logo/brand
print("\n== public assets possibly brand-related ==")
pub = os.path.join(ROOT, "site/public")
for dirpath, dirnames, filenames in os.walk(pub):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_PARTS]
    for fn in filenames:
        if any(k in fn.lower() for k in ["logo", "favicon", "icon", "og", "apple", "touch", "brand", "manifest"]):
            p = os.path.join(dirpath, fn)
            print("   %s (%d bytes)" % (os.path.relpath(p, ROOT), os.path.getsize(p)))
