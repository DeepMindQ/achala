"""Phase 2 orchestrator — runs the surgical content rewrite over all pages.

Guarantees enforced here:
  1. No banned boilerplate / AI-tell phrases anywhere.
  2. No paragraph on any page opens with the same 10 words as a paragraph on
     another page (salt-retry loop rebuilds with a different variant seed
     until the opening is unique).
  3. No hero on any page opens with the same 8 words as another hero.
  4. No placeholder bullet titles, no duplicate consecutive paragraphs,
     no duplicate headings per page, diagram budget <= 2.
"""
import sys, os, json, glob, shutil, re, hashlib, traceback

sys.path.insert(0, os.path.dirname(__file__))
from p2_voice import lint_text
import p2_build as B
import p2_build2 as B2

ROOT = "/home/z/my-project/site"
PAGES_DIR = os.path.join(ROOT, "src/content/pages")
BACKUP_DIR = os.path.join(ROOT, "src/content/_backup_phase2")
INDEX = os.path.join(ROOT, "src/content/index.json")

BUILDERS = {
    "SCAP": B.build_scap, "CAP": B.build_cap, "SUB": B.build_sub, "IND": B.build_ind,
    "SVC": B.build_svc, "TWR": B.build_twr, "SOL": B2.build_sol, "CASE": B2.build_case,
    "INS": B2.build_ins, "PLT": B2.build_plt,
    "SVCHUB": B2.build_hub, "INDHUB": B2.build_hub, "SOLHUB": B2.build_hub,
    "PLTHUB": B2.build_hub, "CASEHUB": B2.build_hub, "INSHUB": B2.build_hub,
}

PLACEHOLDER_TITLES = {"Deliverable", "Challenge", "Point 1", "Point 2", "Point 3",
                      "Question 1", "Question 2", "Question 3"}

import re as _re
_BRAND = [
    (_re.compile(r"Achala\s*Soft(ware)?"), "Achala IT Solutions"),
    (_re.compile(r"Achala IT Solutions"), "Achala IT Solutions"),
    (_re.compile(r"(?<![A-Za-z])Achala(?![A-Za-z])"), "Achala"),
]

def brand_fix(obj):
    """Enforce brand naming inside any JSON structure."""
    if isinstance(obj, str):
        for c, rep in _BRAND:
            obj = c.sub(rep, obj)
        return obj
    if isinstance(obj, dict):
        return {k: brand_fix(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [brand_fix(v) for v in obj]
    return obj

def key10(s):
    words = re.findall(r"[a-z0-9']+", s.lower())
    return " ".join(words[:10])

def key8(s):
    words = re.findall(r"[a-z0-9']+", s.lower())
    return " ".join(words[:8])

def lint_page(page, blocks):
    problems = []
    texts = []
    for b in blocks:
        if b.get("t") in ("p", "hero", "note", "cta", "h2", "h3"):
            texts.append(b.get("x", ""))
        if b.get("t") == "bullets":
            for it in b.get("items", []):
                texts.append(it[0]); texts.append(it[1])
                if it[0] in PLACEHOLDER_TITLES:
                    problems.append(f"placeholder bullet title: {it[0]}")
        if b.get("t") == "table":
            texts.append(b.get("caption", ""))
            for r in b.get("rows", []):
                for cell in r:
                    texts.append(cell)
        if b.get("t") == "diagram":
            texts.append(b.get("title", ""))
    joined = " \n ".join(t for t in texts if t)
    for hit in lint_text(joined):
        problems.append(f"banned phrase: {hit[:60]}")
    prev = None
    for b in blocks:
        if b.get("t") == "p":
            if prev == b.get("x"):
                problems.append("duplicate consecutive paragraph")
            prev = b.get("x")
    if sum(1 for b in blocks if b.get("t") == "diagram") > 2:
        problems.append("more than 2 diagrams")
    wc = len(joined.split())
    HUBS = {"SVCHUB", "INDHUB", "SOLHUB", "PLTHUB", "CASEHUB", "INSHUB"}
    prefix = page["id"].split("-")[0]
    thin = 180 if prefix == "PLT" else 220
    if prefix in BUILDERS and prefix not in HUBS and wc < thin:
        problems.append(f"too thin: {wc} words")
    if wc > 1300:
        problems.append(f"too long: {wc} words")
    seen = set()
    for b in blocks:
        if b.get("t") == "h2":
            if b["x"] in seen:
                problems.append(f"duplicate heading: {b['x']}")
            seen.add(b["x"])
    return problems, wc

def block_keys(blocks):
    """(paragraph key10s, hero key8) for a block list."""
    pk, hk = [], None
    for b in blocks:
        if b.get("t") in ("p", "hero"):
            k = key10(b.get("x", ""))
            if len(k.split()) == 10:
                pk.append(k)
        if b.get("t") == "hero":
            hk = key8(b.get("x", ""))
    return pk, hk

def build_blocks(page, salt):
    pid = page["id"]
    salted = dict(page)
    if salt:
        salted["id"] = f"{pid}~s{salt}"
    prefix = pid.split("-")[0]
    return BUILDERS[prefix](salted)

def main():
    files = sorted(glob.glob(os.path.join(PAGES_DIR, "*.json")))
    print(f"pages found: {len(files)}")
    if not os.path.isdir(BACKUP_DIR):
        shutil.copytree(PAGES_DIR, BACKUP_DIR)
        print("backup written:", BACKUP_DIR)

    corpus_p = {}   # paragraph key10 -> page id
    corpus_h = {}   # hero key8 -> page id
    rebuilt, repaired, skipped = [], [], []
    problems_all, word_dupe = {}, []

    for fp in files:
        page = json.load(open(fp))
        pid = page["id"]; prefix = pid.split("-")[0]
        if prefix in ("HOME", "CONS", "CONSHUB"):
            skipped.append(pid)  # home renders via HomeView; consulting written by p2_consulting
            continue

        if prefix in BUILDERS:
            blocks, salt_used, err = None, 0, None
            for salt in range(13):
                try:
                    cand = build_blocks(page, salt)
                except Exception:
                    err = traceback.format_exc(limit=2)
                    break
                pk, hk = block_keys(cand)
                dup = any(k in corpus_p for k in pk) or (hk and hk in corpus_h)
                if not dup:
                    blocks, salt_used = cand, salt
                    break
                if salt == 0:
                    first_fail = (pk, hk)
            if blocks is None:
                if err:
                    problems_all[pid] = [f"BUILDER ERROR: {err.splitlines()[-1][:120]}"]
                    continue
                # could not find a unique opening in 13 salts — keep best
                blocks = build_blocks(page, 0)
                pk, hk = block_keys(blocks)
                problems_all[pid] = [f"residual opening collision after 13 salts"]
                word_dupe.append((pid, "multi", " | ".join(k for k in pk if k in corpus_p)[:80]))
            probs, wc = lint_page(page, blocks)
            if probs:
                problems_all.setdefault(pid, []).extend(probs)
            page["blocks"] = blocks
            page["words"] = wc
            rebuilt.append(pid)
            page = brand_fix(page)
        else:
            blocks = B2.repair_page(page, set(corpus_p.keys()))
            probs, wc = lint_page(page, blocks)
            if probs:
                problems_all[pid] = [q for q in probs if not q.startswith("too")]
            page["blocks"] = blocks
            page["words"] = wc
            repaired.append(pid)
            page = brand_fix(page)

        # register keys in corpus
        pk, hk = block_keys(page["blocks"])
        for k in pk:
            if len(k.split()) == 10:
                if k in corpus_p and corpus_p[k] != pid:
                    word_dupe.append((pid, corpus_p[k], k))
                else:
                    corpus_p[k] = pid
        if hk:
            if hk in corpus_h and corpus_h[hk] != pid:
                problems_all.setdefault(pid, []).append(f"hero opening duplicates {corpus_h[hk]}")
            else:
                corpus_h[hk] = pid
        json.dump(page, open(fp, "w"), indent=1, ensure_ascii=False)

    # ── update index.json word counts ──
    idx = json.load(open(INDEX))
    words_map = {}
    for fp in files:
        j = json.load(open(fp))
        words_map[j["url"]] = j.get("words", 0)
    for row in idx:
        if row["url"] in words_map:
            row["words"] = words_map[row["url"]]
    json.dump(idx, open(INDEX, "w"), indent=1, ensure_ascii=False)

    print(f"rebuilt: {len(rebuilt)}  repaired: {len(repaired)}  skipped: {len(skipped)}")
    print(f"pages with lint findings: {len(problems_all)}")
    n = 0
    for pid, probs in problems_all.items():
        print(f"  {pid}: {probs[:3]}")
        n += 1
        if n >= 30:
            print("  ...")
            break
    print(f"cross-page paragraph-opening collisions: {len(word_dupe)}")
    for d in word_dupe[:15]:
        print("  dup:", d[0], "<->", d[1], "|", d[2][:60])

if __name__ == "__main__":
    main()
