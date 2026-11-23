"""Wave A1 — Achala rebrand mechanical replacement across the achala clone.
Ordered rules: longest/most-specific first. Case-pair handling for brand strings.
"""
import os, re, sys

ROOT = "/home/z/my-project/achala"
SKIP_DIRS = {"node_modules", ".next", "out", "out-gh", ".next-export", ".research", ".git"}
TEXT_EXTS = {".ts", ".tsx", ".js", ".mjs", ".cjs", ".json", ".css", ".scss", ".html",
             ".md", ".mdx", ".txt", ".xml", ".yml", ".yaml", ".py", ".sh", ".webmanifest", ".svg"}

# (pattern, replacement) — plain substring, applied in order
PLAIN = [
    # domains / emails / handles first
    ("dataqsoft", "achalasolutions"),
    ("DataQSoft", "Achala IT Solutions"),
    ("Dataqsoft", "Achala IT Solutions"),
    # full brand names
    ("Dataq Software", "Achala IT Solutions"),
    ("DATAQ SOFTWARE", "ACHALA IT SOLUTIONS"),
    ("dataq software", "Achala IT Solutions"),
    ("DataQ Soft", "Achala IT Solutions"),
    ("Dataq Soft", "Achala IT Solutions"),
    # paths / repo refs
    ("/DataQ", "/achala"),
    ("DeepMindQ/DataQ", "DeepMindQ/achala"),
    ("DataQ/", "achala/"),
    # generic brand token, all casings
    ("DataQ", "Achala"),
    ("Dataq", "Achala"),
    ("DATAQ", "ACHALA"),
    ("dataq", "achala"),
    # leftover brand-colour wording
    ("Achala Orange", "Achala Red"),
    ("orange dot", "red dot"),
]

# (regex, replacement) — case-insensitive hex / rgb triplets
REGEX = [
    (r"#FE5722", "#d20000"),
    (r"#E04A17", "#a80000"),
    (r"#C2410C", "#8f0000"),
    (r"#FE9C77", "#ff9d96"),
    (r"#FFF3EE", "#fdecec"),
    (r"#FF9A62", "#ff8a7c"),
    (r"#FEC5A6", "#ffc0ba"),
    (r"#18142D", "#2b5672"),
    (r"#0F0C20", "#0e2230"),
    (r"#14102A", "#16334a"),
    (r"#221D3A", "#3a6983"),
    (r"#2C2648", "#477a95"),
    (r"#3A3358", "#568aa6"),
    (r"254,\s*87,\s*34", "210, 0, 0"),
    (r"24,\s*20,\s*45", "43, 86, 114"),
    (r"#FE5722([0-9A-Fa-f]{0,2})\b", r"#d20000\g<1>"),
]

changed = 0
files_touched = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    for fn in filenames:
        ext = os.path.splitext(fn)[1].lower()
        if ext not in TEXT_EXTS:
            continue
        p = os.path.join(dirpath, fn)
        try:
            raw = open(p, "rb").read()
            text = raw.decode("utf-8")
        except Exception:
            continue
        orig = text
        for pat, rep in PLAIN:
            text = text.replace(pat, rep)
        for pat, rep in REGEX:
            text = re.sub(pat, rep, text, flags=re.IGNORECASE)
        if text != orig:
            open(p, "w", encoding="utf-8").write(text)
            changed += 1
            files_touched.append(os.path.relpath(p, ROOT))

# ---- file / dir renames so slugs and asset names match replaced references ----
renamed = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    for fn in list(filenames):
        if "dataq" in fn.lower() and not fn.startswith("."):
            src = os.path.join(dirpath, fn)
            dst = os.path.join(dirpath, re.sub(r"dataq", "achala", fn, flags=re.IGNORECASE))
            if src != dst and not os.path.exists(dst):
                os.rename(src, dst)
                renamed.append((os.path.relpath(src, ROOT), os.path.relpath(dst, ROOT)))
    for d in list(dirnames):
        if "dataq" in d.lower():
            src = os.path.join(dirpath, d)
            dst = os.path.join(dirpath, re.sub(r"dataq", "achala", d, flags=re.IGNORECASE))
            if src != dst and not os.path.exists(dst):
                os.rename(src, dst)
                renamed.append((os.path.relpath(src, ROOT) + "/", os.path.relpath(dst, ROOT) + "/"))

print("files content-updated:", changed)
print("files/dirs renamed: %d" % len(renamed))
for a, b in renamed:
    print("   %s -> %s" % (a, b))

# residual check: any case-insensitive 'dataq' left?
residual = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    for fn in filenames:
        ext = os.path.splitext(fn)[1].lower()
        if ext not in TEXT_EXTS:
            continue
        p = os.path.join(dirpath, fn)
        try:
            t = open(p, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        n = len(re.findall(r"dataq", t, re.IGNORECASE))
        if n:
            residual.append((os.path.relpath(p, ROOT), n))
print("\nRESIDUAL 'dataq' occurrences: %d in %d files" % (sum(n for _, n in residual), len(residual)))
for r, n in residual[:15]:
    print("   %4d  %s" % (n, r))
