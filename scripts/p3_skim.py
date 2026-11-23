#!/usr/bin/env python3
"""Minimal skim digest (12-15 lines/page) + cross-page pattern metrics."""
import html as htmlmod
import os
import re
from collections import Counter

ROOT = "/home/z/my-project/site/out-gh"
OUT = "/home/z/my-project/audit"


def read(p):
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()


def visible(s):
    s = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>|<svg[\s\S]*?</svg>", " ", s, flags=re.I)
    t = htmlmod.unescape(re.sub(r"<[^>]+>", "\n", s))
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    return t


def page_digest(path, label, out):
    s = read(path)
    t = visible(s)
    # trim chrome
    for ns in ["Maintained by the Achala IT Solutions practice council", "CONTACT ACHALA IT SOLUTIONS"]:
        i = t.find(ns)
        if i > 0:
            t = t[:i]
    lines = [f"\n### {label}"]
    grab = t.split("\n")
    # h1 + sub
    h1i = next((i for i, x in enumerate(grab) if len(x) > 8), 0)
    lines.append("H1: " + grab[h1i][:120])
    sub = next((x for x in grab[h1i + 1: h1i + 6] if len(x) > 60), "")
    lines.append("SUB: " + sub[:260])
    # h2s
    h2s = [x.strip().lstrip("#").strip() for x in grab if x.startswith("--- H2:")]
    if not h2s:
        h2s = [x for x in grab if 12 < len(x) < 90 and re.match(r"^[A-Z0-9]", x)][:8]
    lines.append("H2s: " + " || ".join(h[:64] for h in h2s[:9]))
    # kpis
    kps = re.findall(r'kpiLabel[^>]*>([^<]+)<', s)[:6]
    kvs = re.findall(r'kpiValue[^>]*>([^<]+)<', s)[:6]
    if kps:
        lines.append("KPI: " + "; ".join(f"{a}={b}" for a, b in zip(kps, kvs)))
    # arch nodes
    nl = re.findall(r'archNLab[^>]*>([^<]{2,60})<[\s\S]{0,220}?archNSub[^>]*>([^<]{2,90})<', s)[:8]
    if nl:
        lines.append("ARCH: " + " ; ".join(f"{a.strip()}({b.strip()[:44]})" for a, b in nl))
    # evidence / related intro lines
    for marker in ["Where this capability connects", "Patented method underneath"]:
        i = t.find(marker)
        if i >= 0:
            lines.append(f"{marker[:1]}>> " + t[i:i + 170].replace("\n", " / "))
    wc = len(t.split())
    out.append("\n".join(lines) + f"\n(words={wc})")


def main():
    svc = os.path.join(ROOT, "services")
    domains = sorted(d for d in os.listdir(svc) if os.path.isdir(os.path.join(svc, d)))
    all_lines = []
    pages = {}
    # hub
    page_digest(os.path.join(svc, "index.html"), "/services/ (hub)", all_lines)
    for d in domains:
        dpath = os.path.join(svc, d)
        page_digest(os.path.join(dpath, "index.html"), f"/services/{d}/", all_lines)
        for s2 in sorted(x for x in os.listdir(dpath) if os.path.isdir(os.path.join(dpath, x))):
            p = os.path.join(dpath, s2, "index.html")
            page_digest(p, f"/services/{d}/{s2}/", all_lines)
            t = visible(read(p))
            for ns in ["Maintained by the Achala IT Solutions practice council", "CONTACT ACHALA IT SOLUTIONS"]:
                i = t.find(ns)
                if i > 0:
                    t = t[:i]
            pages[f"{d}/{s2}"] = t

    with open(os.path.join(OUT, "skim.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(all_lines))
    print("skim.txt", os.path.getsize(os.path.join(OUT, "skim.txt")))

    # ---- pattern metrics across the 54 inner pages ----
    h2_counter = Counter()
    opener_counter = Counter()
    phrase_counter = Counter()
    for k, t in pages.items():
        heads = [x.strip() for x in t.split("\n") if 10 < len(x.strip()) < 95]
        norm = lambda x: re.sub(r"[^a-z ]", "", x.lower()).strip()
        for h in heads:
            n = norm(h)
            if n:
                h2_counter[n] += 1
        paras = [x.strip() for x in t.split("\n") if len(x.strip()) > 80]
        for p in paras:
            opener_counter[" ".join(p.split()[:6])] += 1
        for ph in [
            "no hand-waving", "you can interrogate", "signed baseline", "named in advance",
            "evidence is named", "run on a bad day", "walk the trail", "auditors can walk",
            "metric you own", "on the page", "not a brochure", "not a call center",
            "reference operating console", "week two", "fortnight",
        ]:
            if ph in t.lower():
                phrase_counter[ph] += 1
    n = len(pages)
    lines2 = [f"\n== PATTERN METRICS over {n} inner pages =="]
    lines2.append("\n-- H2 headings appearing on >20% of pages --")
    for h, c in h2_counter.most_common(40):
        if c >= n * 0.2:
            lines2.append(f"  {c}/{n}  {h}")
    lines2.append("\n-- repeated paragraph openers (>=4 pages) --")
    for o, c in opener_counter.most_common(30):
        if c >= 4:
            lines2.append(f"  {c}x  {o}...")
    lines2.append("\n-- house phrase frequency --")
    for ph, c in phrase_counter.most_common(30):
        lines2.append(f"  {c}/{n}  '{ph}'")
    with open(os.path.join(OUT, "patterns.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines2))
    print("patterns.txt", os.path.getsize(os.path.join(OUT, "patterns.txt")))


if __name__ == "__main__":
    main()
