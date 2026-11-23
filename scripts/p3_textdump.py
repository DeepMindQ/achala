#!/usr/bin/env python3
"""Dump readable text of every built page (home + services hub + 8 domain hubs + 54 subpages)
from the gh-pages export, into per-domain audit files under audit/."""
import html as htmlmod
import os
import re

ROOT = "/home/z/my-project/site/out-gh"
OUT = "/home/z/my-project/audit"
os.makedirs(OUT, exist_ok=True)


def read(p):
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()


def strip_scripts_styles(s):
    s = re.sub(r"<script[\s\S]*?</script>", " ", s, flags=re.I)
    s = re.sub(r"<style[\s\S]*?</style>", " ", s, flags=re.I)
    s = re.sub(r"<svg[\s\S]*?</svg>", " [svg] ", s, flags=re.I)
    return s


def textify(s):
    s = strip_scripts_styles(s)
    s = re.sub(r"<(h[1-6])[^>]*>", lambda m: "\n\n#" * 1 + "# " if m.group(1) in ("h1", "h2") else "\n## ", s)
    # simpler: mark headings
    s = re.sub(r"<h1[^>]*>", "\n\n=== H1: ", s)
    s = re.sub(r"<h2[^>]*>", "\n\n--- H2: ", s)
    s = re.sub(r"<h3[^>]*>", "\n  . H3: ", s)
    s = re.sub(r"<h4[^>]*>", "\n    . H4: ", s)
    s = re.sub(r"</h[1-6]>", "\n", s)
    s = re.sub(r"<(p|div|li|tr|figcaption|summary|button|a|td)[^>]*>", "\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = htmlmod.unescape(s)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n\s*\n\s*\n+", "\n\n", s)
    return s.strip()


def clean_noise(t):
    """Drop obvious chrome repeated on every page."""
    noise_starts = [
        "Maintained by the Achala IT Solutions practice council",
        "CONTACT ACHALA IT SOLUTIONS",
        "Book an executive briefing — 45 minutes",
    ]
    for ns in noise_starts:
        i = t.find(ns)
        if i > 0:
            t = t[:i]
    return t


def dump(path, out_lines, label):
    if not os.path.exists(path):
        out_lines.append(f"!! MISSING {path}")
        return
    t = clean_noise(textify(read(path)))
    out_lines.append(f"\n{'='*90}\nPAGE: {label}\n{'='*90}\n{t}\n")


def main():
    # home
    lines = []
    dump(os.path.join(ROOT, "index.html"), lines, "/ (homepage)")
    with open(os.path.join(OUT, "home.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    svc = os.path.join(ROOT, "services")
    domains = sorted(
        d for d in os.listdir(svc) if os.path.isdir(os.path.join(svc, d))
    )
    for d in domains:
        dpath = os.path.join(svc, d)
        lines = []
        dump(os.path.join(svc, "index.html"), lines, "/services/ (hub)")
        dump(os.path.join(dpath, "index.html"), lines, f"/services/{d}/ (domain hub)")
        subs = sorted(x for x in os.listdir(dpath) if os.path.isdir(os.path.join(dpath, x)))
        for s in subs:
            dump(os.path.join(dpath, s, "index.html"), lines, f"/services/{d}/{s}/")
        with open(os.path.join(OUT, f"svc__{d}.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(d, "->", f"svc__{d}.txt", len(subs), "subs")


if __name__ == "__main__":
    main()
