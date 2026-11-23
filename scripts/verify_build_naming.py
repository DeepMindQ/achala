#!/usr/bin/env python3
"""Verify the BUILT site (out/) uses 'Achala IT Solutions' everywhere, has zero
'Achala IT Solutions'/bare-'Achala' text and zero confidentiality tokens."""
import os, re, json, html

OUT = "/home/z/my-project/site/out"
abbr = re.compile(r"Achala\s?Soft(?!ware)|Achala IT Solutions(?![A-Za-z0-9])")
bare = re.compile(r"Achala(?![A-Za-z0-9])")
confid = re.compile(r"Strategemist|Pisupati|Shanker", re.I)
full = re.compile(r"Data[qQ] Software")
# bare Achala inside visible text (strip tags first) vs attribute URLs (achalasolutions.com ok)
tag = re.compile(r"<[^>]+>")

hits = {"abbr": [], "bare_visible": [], "confid": []}
n_files = 0
n_full = 0
for dirpath, dirnames, filenames in os.walk(OUT):
    dirnames[:] = [d for d in dirnames if d != "pagefind"]
    for fn in filenames:
        if not fn.endswith((".html", ".xml", ".txt", ".json")):
            continue
        path = os.path.join(dirpath, fn)
        n_files += 1
        text = open(path, encoding="utf-8", errors="replace").read()
        n_full += len(full.findall(text))
        for m in abbr.finditer(text):
            hits["abbr"].append((path, text[max(0, m.start()-60):m.end()+60]))
        if confid.search(text):
            hits["confid"].append(path)
        visible = tag.sub(" ", text)
        for m in bare.finditer(visible):
            hits["bare_visible"].append((path, visible[max(0, m.start()-70):m.end()+70].replace("\n", " ")))

print(json.dumps({
    "files_scanned": n_files,
    "full_name_count": n_full,
    "abbr_hits": len(hits["abbr"]),
    "bare_Achala_in_visible_text": len(hits["bare_visible"]),
    "confidentiality_hits": len(hits["confid"]),
}, indent=2))
for path, ctx in (hits["abbr"] + hits["bare_visible"])[:10]:
    print("HIT:", path.replace(OUT, ""), "|", html.unescape(ctx)[:140].strip())
for path in hits["confid"][:10]:
    print("CONFID:", path.replace(OUT, ""))
