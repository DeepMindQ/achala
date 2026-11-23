# -*- coding: utf-8 -*-
"""Emit manual TOC entries (H1-only, approximate page numbers) for a volume JSON."""
import sys, json, math

def approx_pages(words):
    return max(1, math.ceil(words / 330.0))

def main(path):
    doc = json.load(open(path, encoding="utf-8"))
    entries = []
    page = 1
    for p in doc["pages"]:
        entries.append({"level": 1, "text": p["title"], "page": str(page)})
        page += approx_pages(p.get("words", 0))
    print(json.dumps(entries, ensure_ascii=False))

if __name__ == "__main__":
    main(sys.argv[1])
