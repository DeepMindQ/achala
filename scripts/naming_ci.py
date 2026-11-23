#!/usr/bin/env python3
"""Naming + confidentiality CI gate (BG-008 / BG-014 / BG-017) + content lint (E-20).

HARD RULES enforced before any static export leaves the machine:
  1. Brand naming  — the only allowed brand string is "Achala IT Solutions".
     Forbidden: "Achala IT Solutions", "Achala IT Solutions", "Achala IT Solutionsware", bare "Achala".
  2. Confidentiality — the R&D programme source entity must never appear:
     forbidden: "Strategemist", "Pisupati", "VSS Ravi Shanker".
     (Note: Hyderabad as Achala IT Solutions's own delivery-center city is ALLOWED;
      the forbidden strings are the secret entity and personnel names.)
  3. Content lint (E-20, Wave 0):
     a. HARD trust guards — fail the build immediately:
        - the "Live view" badge string (static data must never claim liveness)
        - the absolute footer claim "Zero critical data-exposure incidents"
        - the retired "Towers" taxonomy noun (site-wide term is "Expertise")
     b. RATCHET sameness metrics — fail only when a metric grows beyond its
        blessed baseline (the Wave 3/4 backlog holds the current counts; the
        gate proves regressions cannot return while later waves run them down):
        - empty arch node subs / edge labels
        - paragraph openers shared across >2 pages
        - identical CTA/intro strings used on >10 pages
        - service pages missing persona/fit markers

Scans site/src + site/public (+ sitemap/robots feeds) for text-bearing files.
Exit 1 = gate failed; wired into `npm run export` so a bad build cannot ship.

Usage: python3 scripts/naming_ci.py [--fix] [--bless]
      --fix attempts safe replacements for the brand-naming violations only.
      --bless rewrites the sameness baseline to the current measured values.
"""
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"
SCAN_ROOTS = [SITE / "src", SITE / "public"]
TEXT_EXT = {
    ".ts", ".tsx", ".js", ".jsx", ".json", ".css", ".scss", ".md", ".mdx",
    ".html", ".txt", ".xml", ".svg", ".webmanifest", ".csv",
}

BRAND_RULES = [
    # (compiled pattern, replacement, label) — legacy DataQ strings must never appear
    (re.compile(r"(?i)dataq[-\s]*soft(ware)?"), "Achala IT Solutions", "legacy 'DataQ Soft(ware)' brand"),
    (re.compile(r"(?i)dataqsoft"), "achalasolutions", "legacy dataqsoft domain/brand"),
    (re.compile(r"(?i)(?<![A-Za-z])dataq(?![A-Za-z])"), "Achala", "legacy bare DataQ token"),
]

CONFIDENTIAL_RULES = [
    (re.compile(r"(?i)strategemist"), "our R&D programme", "secret entity name"),
    (re.compile(r"(?i)pisupati"), "[removed]", "secret personnel"),
    (re.compile(r"(?i)vss\s+ravi\s+shanker|ravi\s+shanker"), "[removed]", "secret personnel"),
]


def iter_files():
    for root in SCAN_ROOTS:
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if p.is_file() and (p.suffix.lower() in TEXT_EXT or p.name in ("CNAME", "robots.txt")):
                yield p


def main() -> int:
    fix = "--fix" in sys.argv
    brand_viol = []          # (path, label, count)
    confid_viol = []         # (path, label, count)
    brand_ok_count = 0
    for f in iter_files():
        try:
            s = f.read_text(encoding="utf-8")
        except Exception:
            continue
        orig = s
        # confidentiality first (higher severity, no auto-fix in CI)
        for pat, _repl, label in CONFIDENTIAL_RULES:
            n = len(pat.findall(s))
            if n:
                confid_viol.append((str(f.relative_to(SITE)), label, n))
        for pat, repl, label in BRAND_RULES:
            n = len(pat.findall(s))
            if n:
                brand_viol.append((str(f.relative_to(SITE)), label, n))
                if fix:
                    s = pat.sub(repl, s)
        brand_ok_count += len(re.findall(r"Achala IT Solutions", s))
        if fix and s != orig:
            f.write_text(s, encoding="utf-8")

    print(f"[naming_ci] files scanned: {sum(1 for _ in iter_files())}")
    print(f"[naming_ci] 'Achala IT Solutions' occurrences: {brand_ok_count}")

    if brand_viol:
        print("[naming_ci] BRAND VIOLATIONS:")
        for path, label, n in sorted(brand_viol):
            print(f"  {path}: {label} x{n}")
    if confid_viol:
        print("[naming_ci] CONFIDENTIALITY VIOLATIONS (never auto-fixed):")
        for path, label, n in sorted(confid_viol):
            print(f"  {path}: {label} x{n}")

    if brand_viol or confid_viol:
        print("[naming_ci] GATE FAILED — export blocked.")
        return 1
    print("[naming_ci] GATE PASSED — brand naming + confidentiality clean.")
    return 0


# ═══════════════════════════════════════════════════════════════════════════
# E-20 content lint (Wave 0) — trust guards + sameness ratchet
# ═══════════════════════════════════════════════════════════════════════════

BASELINE_FILE = Path(__file__).resolve().parent / "content_lint_baseline.json"

# Hard trust guards: any hit fails the build. These strings must never return.
HARD_TRUST_PATTERNS = [
    (re.compile(r"Live view"), '"Live view" badge (static data must not claim liveness)'),
    (re.compile(r"Zero critical data-exposure incidents"), "absolute incident claim (unverifiable legal exposure)"),
    (re.compile(r"(?i)A tower applied to this operating unit"), 'retired "Towers" system-generated phrase'),
]

PAGES_DIR_NAME = "pages"

# persona/fit markers a service page must carry (D-S15..D-S18 vocabulary)
PERSONA_MARKERS = [
    "If you own", "If you run", "Who this is for", "You will feel this",
    "fit/no-fit", "Fit check", "Built for the", "persona",
]


def _lint_files():
    """Yield (path, text) for content JSONs + site components."""
    for p in (SITE / "src" / "content" / PAGES_DIR_NAME).glob("*.json"):
        yield p, p.read_text(encoding="utf-8", errors="ignore")
    for p in (SITE / "src" / "components" / "site").glob("*.tsx"):
        yield p, p.read_text(encoding="utf-8", errors="ignore")


def content_lint(bless: bool = False):
    """Return (ok, report_lines). Hard guards fail immediately; ratchet
    metrics fail only when worse than the blessed baseline."""
    import json as _json
    import collections

    report: list[str] = []
    hard_fail = False

    # ── a. hard trust guards ────────────────────────────────────────────────
    for path, text in _lint_files():
        rel = str(path.relative_to(SITE))
        for rx, label in HARD_TRUST_PATTERNS:
            n = len(rx.findall(text))
            if n:
                hard_fail = True
                report.append(f"  HARD [{label}] x{n} in {rel}")

    # ── b. ratchet metrics ──────────────────────────────────────────────────
    empty_notes = 0
    opener_pages: dict[str, set] = collections.defaultdict(set)
    cta_pages: dict[str, set] = collections.defaultdict(set)
    persona_missing = 0
    service_pages = 0

    for p in (SITE / "src" / "content" / PAGES_DIR_NAME).glob("*.json"):
        try:
            d = _json.loads(p.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            continue
        blob = _json.dumps(d, ensure_ascii=False)
        empty_notes += len(re.findall(r'"sub"\s*:\s*""', blob)) + len(
            re.findall(r'"label"\s*:\s*""', blob)
        )
        tpl = d.get("template", "")
        first_opener = None
        for b in d.get("blocks", []):
            if b.get("t") == "cta" and isinstance(b.get("x"), str) and len(b["x"]) > 40:
                cta_pages[b["x"][:140]].add(p.name)
            if b.get("t") == "p" and isinstance(b.get("x"), str) and len(b["x"]) > 60 and first_opener is None:
                first_opener = " ".join(b["x"].split()[:8])
        if first_opener:
            opener_pages[first_opener].add(p.name)
        if tpl == "service_page":
            service_pages += 1
            if not any(m in blob for m in PERSONA_MARKERS):
                persona_missing += 1

    dup_opener_touch = sum(len(v) for v in opener_pages.values() if len(v) > 2)
    shared_ctas = sum(1 for v in cta_pages.values() if len(v) > 10)

    metrics = {
        "empty_arch_notes": empty_notes,
        "opener_pages_over2": dup_opener_touch,
        "cta_strings_over10": shared_ctas,
        "service_pages_missing_persona": persona_missing,
    }

    if bless:
        BASELINE_FILE.write_text(_json.dumps(metrics, indent=1), encoding="utf-8")
        report.append(f"  baseline blessed → {BASELINE_FILE.name}: {metrics}")
        return True, report

    base = {}
    if BASELINE_FILE.exists():
        base = _json.loads(BASELINE_FILE.read_text(encoding="utf-8"))
    else:
        # first run without a baseline: bless implicitly so the gate starts clean
        BASELINE_FILE.write_text(_json.dumps(metrics, indent=1), encoding="utf-8")
        base = metrics
        report.append("  [lint] no baseline found — blessed current values implicitly")

    ratchet_fail = False
    for key, now in metrics.items():
        allowed = base.get(key, now)
        if now > allowed:
            ratchet_fail = True
            report.append(f"  RATCHET FAIL {key}: now {now} > baseline {allowed}")
        else:
            report.append(f"  ratchet ok {key}: {now}/{allowed}")

    ok = not (hard_fail or ratchet_fail)
    return ok, report


if __name__ == "__main__":
    code = main()
    bless = "--bless" in sys.argv
    lint_ok, lint_report = content_lint(bless=bless)
    print("[content_lint] E-20 sameness + trust gate:")
    for line in lint_report:
        print(line)
    if lint_ok:
        print("[content_lint] GATE PASSED — trust guards clean, sameness at/below baseline.")
    else:
        print("[content_lint] GATE FAILED — export blocked.")
    sys.exit(code if code else (0 if lint_ok else 1))
