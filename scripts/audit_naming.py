#!/usr/bin/env python3
"""Audit brand naming + confidentiality tokens across site src (and docs).

Reports every occurrence of:
  - 'Achala IT Solutions' NOT followed by 'ware'  (the forbidden abbreviation)
  - 'Achala IT Solutions' / 'Achala IT Solutions' camel/short variants in user-visible strings
  - 'Achala IT Solutionsware' (current standard, count only)
  - confidentiality tokens: Strategemist / Pisupati / Shanker / Hyderabad
Outputs /tmp/naming_report.json  (file -> [{line, col, text}])
"""
import json, os, re, sys

ROOTS = ["/home/z/my-project/site/src", "/home/z/my-project/docs"]
DOCS = "/home/z/my-project/docs"
EXTS = {".ts", ".tsx", ".js", ".jsx", ".json", ".css", ".md", ".html", ".txt"}

PAT_ABBR = re.compile(r"Achala\s?Soft(?!ware)")   # forbidden abbreviations
PAT_FULL = re.compile(r"Achala IT Solutionsware")
PAT_ACHALA = re.compile(r"Achala(?!u)")            # bare Achala usage (context check)
CONFID = re.compile(r"Strategemist|Pisupati|Shanker", re.I)

def walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {"node_modules", ".next", "out"}]
        for fn in filenames:
            if os.path.splitext(fn)[1] in EXTS:
                yield os.path.join(dirpath, fn)

PAT_FULL = re.compile(r"Data[qQ] Software")
report = {"abbr": {}, "full_count": 0, "confidential": {}, "bare_achala": {}}
total_abbr = 0
for root in ROOTS + [DOCS]:
    for path in walk(root):
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                for i, line in enumerate(f, 1):
                    for m in PAT_ABBR.finditer(line):
                        report["abbr"].setdefault(path, []).append(
                            {"line": i, "col": m.start(), "text": line.strip()[:160]})
                        total_abbr += 1
                    full_count = len(PAT_FULL.findall(line))
                    report["full_count"] += full_count
                    if CONFID.search(line):
                        report["confidential"].setdefault(path, []).append(
                            {"line": i, "text": line.strip()[:160]})
        except OSError:
            pass

print(json.dumps({
    "files_with_abbr": len(report["abbr"]),
    "total_abbr_occurrences": total_abbr,
    "total_Achala_Software_full": report["full_count"],
    "confidential_files": {k: len(v) for k, v in report["confidential"].items()},
}, indent=2))

with open("/tmp/naming_report.json", "w") as f:
    json.dump(report, f, indent=2)
print("full detail -> /tmp/naming_report.json")
