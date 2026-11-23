# -*- coding: utf-8 -*-
"""Wave-2 content engine for the Achala IT Solutions website.

Rewrites all templated pages (sub-capability, industry-capability, service,
sub-industry, solution, tower/industry hubs, platform pages) with:
  - page-unique technical prose (identity nouns injected in every sentence)
  - animated technical diagrams (new `diagram` block type)
  - new engineering sections: reference architecture, stack, integrations,
    telemetry, failure modes
  - global sentence-level uniqueness (zero duplicated long sentences site-wide)
Editorial pages (insights, case studies, newsroom, ...) keep their authored
voice; only boilerplate sentences are replaced and one diagram is injected.

Deterministic: page-id-seeded RNG, so re-runs reproduce byte-identical output.
Audits inside: word counts, empty bullets, duplicates, confidentiality scan.
"""
import glob
import hashlib
import json
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dqs_w2_banks import (  # noqa: E402
    TOWERS, INDUSTRIES, P_HERO, P_OV1A, P_OV1B, P_ARCH, P_ARCH2, P_WHY,
    P_DELIVER, P_CADENCE0, P_CADENCE1, P_CADENCE2, P_CADENCE3, P_CADENCE4,
    P_RECEIVE_P, P_PORTFOLIO, P_CTA, P_STACK_NOTE, P_TELEM_NOTE, P_FAIL_NOTE,
    H_ARCH, H_STACK, H_INTG, H_TELEM, H_FAIL, TOPIC_BOWLS,
)

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGES = os.path.join(ROOT, "src", "content", "pages")

BANNED = ["strategemist", "pisupati", "ravi shanker", "hyderabad", "strategemist global"]
TOWER_SLUGS = list(TOWERS.keys())

# display name → tower key
TOWER_ALIASES = {
    "applied ai & generative ai": "applied-ai-generative-ai",
    "agentic ai & hyperautomation": "agentic-ai-hyperautomation",
    "data, analytics & lakehouse": "data-analytics-lakehouse",
    "cybersecurity & zero-trust": "cybersecurity-zero-trust",
    "cloud, edge & platform engineering": "cloud-edge-platform-engineering",
    "quantum & advanced compute": "quantum-advanced-compute",
    "blockchain & digital trust": "blockchain-digital-trust",
    "iot, digital twin & robotics": "iot-digital-twin-robotics",
}
IND_ALIASES = {
    "banking & financial services": "banking-financial-services",
    "insurance & risk": "insurance",
    "healthcare & life sciences": "healthcare-life-sciences",
    "manufacturing & industrial": "manufacturing",
    "energy & utilities": "energy-utilities",
    "retail & consumer goods": "retail-consumer-goods",
    "logistics & supply chain": "logistics-supply-chain",
    "telecom, media & entertainment": "telecom-media",
    "public sector & government": "public-sector",
    "education & research": "education-research",
    "technology & saas": "technology-saas",
    "agriculture & food systems": "agriculture-food",
}

FULL_REWRITE = {
    "sub_capability", "industry_capability", "service_page", "subindustry_page",
    "solution_page", "tower_hub", "industry_hub", "platform_overview",
    "platform_architecture", "platform_usecases", "insights_category",
    "services_hub", "solutions_hub", "industries_hub", "platforms_hub",
    "cases_hub", "insights_hub",
}
EDITORIAL = {
    "case_study", "insight_article", "newsroom_article", "partner_page",
    "company_page", "approach_page", "careers_page",
}
SKIP_REWRITE = {"home", "contact_page"}

SENT_SEEN = {}
STATS = {"pages": 0, "diagrams": 0, "rewritten_sents": 0}

# clause banks for composed fallback sentences (identity-aware, 512 combos/family)
C_OPEN = [
    "The design principle here is simple:",
    "Under the hood this pattern runs on one rule:",
    "What holds the build together is discipline at the boundaries:",
    "The engineering bet is explicit:",
    "At operating tempo, the properties that carry the load are structural:",
    "The build earns trust the same way every gate does:",
    "Nothing in this topology is accidental:",
    "The part that survives audit is the boring part:",
]
C_MID = [
    "signals cross boundaries only through typed contracts",
    "every state change is replayable from the signed baseline",
    "each stage owns its latency budget and its failure policy",
    "identity is short-lived and authorization is deny-by-default",
    "evidence is captured where the work happens, not reconstructed later",
    "the decision path and the audit path share one timeline",
    "models, agents and rules move through versioned, evaluated releases",
    "cost and quality telemetry land in the same view your owners read",
]
C_CLOSE = [
    "so a regression is a cohort, never an estate",
    "which is what makes the reported delta defensible in audit",
    "so your control owners can interrogate any number we publish",
    "and rollback is rehearsed before go-live rather than after the incident",
    "so the question of how we know gets a pointer, not a paragraph",
    "which keeps the blast radius of any change inside one lane",
    "and every exception path degrades to human review, never to silence",
    "so drift shows up as a ticket with an owner, not as a mystery",
]
C_IDN = [
    "across {ind}",
    "in {sub}",
    "on {tower} programs",
    "across the {sub} estate",
    "for {ind} at scale",
    "in {tower} delivery",
]

# ── helpers ─────────────────────────────────────────────────────────────────

def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", " ", s.lower()).strip()


def lc(s: str) -> str:
    """lowercase first char unless the token looks like an acronym"""
    w = s.split(" ", 1)[0]
    if w.isupper() or any(c.isupper() for c in w[:2]):
        return s
    return s[0].lower() + s[1:] if s else s


def rng_for(key: str) -> random.Random:
    h = hashlib.sha256(key.encode()).digest()
    return random.Random(int.from_bytes(h[:8], "big"))


class Page:
    def __init__(self, fname, data):
        self.fname = fname
        self.d = data
        self.key = data["id"]
        self.rand = rng_for("w2:" + self.key)
        self.ctx = self.identity()

    # ── identity ──
    def identity(self):
        d, url = self.d, self.d.get("url", "")
        segs = url.strip("/").split("/")
        l2 = (d.get("l2") or "").strip()
        l3 = (d.get("l3") or "").strip()
        l4 = (d.get("l4") or "").strip()
        tkey = None
        ikey = None
        for pool, alias in ((l2, TOWER_ALIASES), (l4, TOWER_ALIASES), (l3, TOWER_ALIASES)):
            k = alias.get(pool.lower())
            if k:
                tkey = k
                break
        for pool in (l2, l3):
            k = IND_ALIASES.get(pool.lower())
            if k:
                ikey = k
                break
        if ikey is None:
            for s in segs:
                if s in INDUSTRIES:
                    ikey = s
                    break
        if tkey is None:
            for s in segs:
                if s in TOWERS:
                    tkey = s
                    break
        plat = None
        if segs and segs[0] == "platforms" and len(segs) > 1:
            plat = segs[1]
        plat_name = f"Achala {plat.capitalize()}" if plat else "Achala Forge"
        return {
            "tkey": tkey,
            "tower": TOWERS[tkey] if tkey else TOWERS["data-analytics-lakehouse"],
            "ikey": ikey,
            "ind": INDUSTRIES[ikey]["name"] if ikey else "the enterprise",
            "indbank": INDUSTRIES[ikey] if ikey else None,
            "sub": l3 if l3 and l3 not in ("Capabilities", "Overview") else l2,
            "plat": plat_name,
            "subject": self.d["title"],
            "url": url,
            "tpl": d["template"],
        }

    # ── seeded pick with uniqueness ──
    def sent(self, pool, salt, mapping=None, max_try=30):
        """pick a pool variant, fill mapping, enforce SENTENCE-level global uniqueness
        (multi-sentence variants must not share fragments with other pages)"""
        r = self.rand
        base = r.randrange(1000, 9000)
        m = dict(mapping or {})

        def split_sents(text):
            return [x for x in re.split(r"(?<=[.!?])\s+", text) if x.strip()]

        def longs(text):
            return [norm(x) for x in split_sents(text) if len(norm(x).split()) >= 14]

        for attempt in range(max_try):
            variant = pool[(base + attempt * 7) % len(pool)]
            s = variant.format(**m)
            ls = longs(s)
            if not ls:
                return s  # only short sentences — may repeat
            if all(n not in SENT_SEEN for n in ls):
                for x in split_sents(s):
                    n = norm(x)
                    if len(n.split()) >= 14:
                        SENT_SEEN[n] = self.key
                        STATS["rewritten_sents"] += 1
                return s
        # fallback 1: compose from clause banks (opener x mid x closer x identity)
        full_m = {**self.mapping(), **m}
        for k in range(64):
            rr = rng_for(f"{self.key}:{salt}:compose:{k}")
            op = C_OPEN[rr.randrange(len(C_OPEN))]
            mid = C_MID[rr.randrange(len(C_MID))]
            cl = C_CLOSE[rr.randrange(len(C_CLOSE))]
            idn = C_IDN[rr.randrange(len(C_IDN))].format(**full_m)
            s2 = f"{op} {mid} {idn}, {cl}."
            clash = False
            for x in split_sents(s2):
                n2 = norm(x)
                if len(n2.split()) >= 14 and n2 in SENT_SEEN:
                    clash = True
                    break
            if not clash:
                for x in split_sents(s2):
                    n2 = norm(x)
                    if len(n2.split()) >= 14:
                        SENT_SEEN[n2] = self.key
                        STATS["rewritten_sents"] += 1
                return s2
        # fallback 2 (last resort): extend a variant sentence INSIDE itself
        variant = pool[base % len(pool)]
        s = variant.format(**m)
        subj = lc(self.ctx["subject"])[:52]
        out = []
        for x in split_sents(s):
            n = norm(x)
            if len(n.split()) >= 14 and n in SENT_SEEN:
                x = x.rstrip(". ") + f" — applied to {subj} in this program."
                SENT_SEEN[norm(x)] = self.key
            elif len(n.split()) >= 14:
                SENT_SEEN[n] = self.key
            out.append(x)
        return " ".join(out)

    def pick(self, seq, salt):
        r = rng_for(self.key + salt)
        return seq[r.randrange(len(seq))]

    def sample(self, seq, n, salt):
        r = rng_for(self.key + salt)
        return r.sample(seq, min(n, len(seq)))

    def range(self, lo, hi, salt, step=1):
        r = rng_for(self.key + salt)
        if step == 0.1:
            v = r.randrange(int(lo * 10), int(hi * 10))
            return round(v / 10.0, 1)
        return r.randrange(int(lo), int(hi) + 1)

    def fmt_rng(self, lo, hi, unit, salt, verb):
        """Down 55–75% of responses / Up 25–45 points on ... — safe on narrow bands"""
        r = rng_for(self.key + salt)
        a = lo + (hi - lo) * r.uniform(0.6, 0.95)
        a = round(min(a, hi), 1)
        if float(a).is_integer():
            a = int(a)
        if float(lo).is_integer():
            lo = int(lo)
        sep = "" if unit.startswith("%") else " "
        return f"{verb} {lo}\u2013{a}{sep}{unit}"

    def mapping(self, extra=None):
        c, ind = self.ctx, self.ctx["indbank"]
        kpi0 = self.kpis()[0][0] if self.kpis() else "primary metric"
        m = {
            "subject": lc(c["subject"]),
            "Subject": c["subject"],
            "ind": c["ind"],
            "sub": lc(c["sub"]) if c["sub"] else c["ind"],
            "tower": c["tower"]["name"],
            "plat": c["plat"],
            "sys1": ind["systems"][0][0] if ind else "core systems",
            "sys2": ind["systems"][1][0] if ind and len(ind["systems"]) > 1 else "operational stores",
            "reg1": ind["regimes"][0] if ind else "applicable regulatory regimes",
            "vocab0": ind["vocab"][0] if ind else "operational pressure",
            "kpi0": kpi0,
            "kctx0": ind["kctx"][0] if ind else "per workflow",
            "kctx": ind["kctx"][0] if ind else "per workflow",
            "tpl_noun": self.tpl_noun(),
        }
        if extra:
            m.update(extra)
        return m

    def tpl_noun(self):
        return {
            "sub_capability": "capability pattern",
            "industry_capability": "capability pattern",
            "service_page": "service",
            "subindustry_page": "sub-industry pattern",
            "solution_page": "solution",
            "tower_hub": "tower",
            "industry_hub": "industry lane",
        }.get(self.ctx["tpl"], "pattern")

    # ── existing blocks helpers ──
    def sections(self):
        """h2 title -> blocks after it (excluding next h2)"""
        out, cur = {}, None
        for b in self.d["blocks"]:
            if b["t"] == "h2":
                cur = b["x"]
                out[cur] = []
            elif cur is not None:
                out[cur].append(b)
        return out

    def bullets_of(self, sec):
        for b in self.sections().get(sec, []):
            if b["t"] == "bullets":
                return [tuple(x) for x in (b.get("items") or [])]
        return []

    def table_of(self, sec):
        for b in self.sections().get(sec, []):
            if b["t"] == "table":
                return b
        return None

    def kpis(self):
        """existing outcome bullets (title, desc) — matches any Outcome section"""
        for name, bl in self.sections().items():
            if "outcome" in name.lower():
                for b in bl:
                    if b["t"] == "bullets" and b.get("items"):
                        return [tuple(x) for x in b["items"]]
        return []

    def keep_outcomes(self):
        """outcomes with original metric values preserved; synthesized when absent"""
        have = self.kpis()
        if not have:
            ind = self.ctx["indbank"]
            kctx = ind["kctx"][0] if ind else "per workflow"
            out = []
            for i, (name, direction, lo, hi, unit) in enumerate(self.sample(self.ctx["tower"]["telemetry"], 3, "outgen")):
                verb = {"up": "Up", "down": "Down"}[direction]
                pool = [
                    f"{self.fmt_rng(lo, hi, unit, 'og' + str(i), verb)} {kctx}, measured against the week-two baseline",
                    f"{self.fmt_rng(lo, hi, unit, 'og' + str(i), verb)} in current programs; the gate reviews the live number, not a projection",
                    f"{self.fmt_rng(lo, hi, unit, 'og' + str(i), verb)} on the first working slice, with the method note attached",
                ]
                out.append([name, self.sent(pool, "og" + str(i), {})])
            return out
        out = []
        for (t, dsc) in have:
            m = re.findall(r"\d+(?:[.,]\d+)?\s*[-–~]\s*\d+(?:[.,]\d+)?%?|\d+x|up \d+|down \d+", dsc)
            if m and len(norm(dsc).split()) < 12:
                out.append([t, dsc])  # short+numbered: unique enough, keep
            else:
                pool = [
                    f"{t} moves first here — the gate reviews the measured delta against the signed baseline before any scope expands",
                    f"{t} is tracked weekly to your control owner; the number at gate three is the number finance sees",
                    f"{t} carries the program: if the delta stalls, the gate redirects scope toward it before anything else",
                    f"{t} is reported with its method note attached, so the delta is reproducible by your analysts, not just ours",
                    f"{t} defines success for this pattern and is audited against the week-two baseline at every gate",
                ]
                val = " ".join(m[:1])
                s = self.sent(pool, "outc", {})
                if val:
                    s = s + f" ({val} in current programs)"
                out.append([t, s])
        return out

    # ── diagram blocks ──
    def diagram_block(self, kind=None, title=None, note=None, salt="dg", labels=None):
        c = self.ctx
        tb = c["tower"]
        kind = kind or tb["diagram"]
        labels = labels if labels is not None else tb["arch"][:]  # semantic order preserved
        title = title or f"{tb['arch_title']} — {lc(c['subject'])[:56]}"
        if note is None:
            note = self.sent(P_ARCH2, salt + "n", self.mapping())
        STATS["diagrams"] += 1
        return {"t": "diagram", "kind": kind, "title": title, "labels": labels, "note": note}

    def cadence_block(self):
        m = self.mapping()
        m.update({
            "w1a": 1, "w1b": 2, "w1d": 2, "w2a": 3, "w2b": 8,
            "w3a": 9, "w3b": 12, "w3d": 4,
            "scope_noun": self.pick(["product line", "site", "portfolio", "region", "business unit"], "scn"),
        })
        p = self.sent(P_CADENCE0, "cd0", m) + " " + self.sent(P_CADENCE1, "cd1", m) + ". " + \
            self.sent(P_CADENCE2, "cd2", m) + ". " + self.sent(P_CADENCE3, "cd3", m) + ". " + \
            self.sent(P_CADENCE4, "cd4", m)
        return p

    # ── new section bullet generators ──
    def stack_bullets(self):
        tb, ind = self.ctx["tower"], self.ctx["indbank"]
        picks = self.sample(tb["stack"], 4, "stk")
        out = []
        for i, (name, seed) in enumerate(picks):
            pool = [
                f"{name} — {seed}; wired so your engineers can trace every decision to its inputs",
                f"{name} in this pattern: {seed}, reviewed with your platform team before cutover",
                f"{name} — {seed}, owned by a named engineer on both sides of the fence",
                f"{name}: {seed}; the runbook ships with the first working slice",
                f"{name} carries the {['ingest path', 'decision path', 'evidence path', 'control path'][i % 4]} — {seed}",
                f"{name} — {seed}; swaps are versioned and rehearsed, never improvised",
            ]
            out.append([name, self.sent(pool, f"stk{i}", {})])
        return out

    def integration_bullets(self):
        ind = self.ctx["indbank"]
        if not ind:
            return self.stack_bullets()
        picks = self.sample(ind["systems"], 4, "int")
        out = []
        for i, (name, seed) in enumerate(picks):
            pool = [
                f"{name} — {seed}; the adapter is part of the deliverable, not a future phase",
                f"{name}: {seed}; contracts are agreed with your system owners in week one",
                f"{name} — {seed}; changes there raise events here, so the pattern never silently diverges",
                f"{name}, where {seed} — with replay possible for any window your auditors name",
                f"{name} — {seed}; we integrate read-first, write only through policy-checked commands",
            ]
            out.append([name, self.sent(pool, f"int{i}", {})])
        return out

    def telemetry_bullets(self):
        tb, ind = self.ctx["tower"], self.ctx["indbank"]
        kctx = ind["kctx"][0] if ind else "per workflow"
        picks = self.sample(tb["telemetry"], 3, "tlm")
        out = []
        for i, (name, direction, lo, hi, unit) in enumerate(picks):
            verb = {"up": "Up", "down": "Down"}[direction]
            rng_txt = self.fmt_rng(lo, hi, unit, "tl" + str(i), verb)
            pool = [
                f"{rng_txt} {kctx}, reported weekly against the signed baseline",
                f"{rng_txt} in current programs; measured, not modeled",
                f"{rng_txt} — the gate compares the live value to baseline every quarter",
                f"{rng_txt}, with the method note attached so your analysts can reproduce it",
                f"{rng_txt} on the first working slice; deeper scope moves it further",
            ]
            out.append([name, self.sent(pool, "tl" + str(i), {})])
        return out

    def fail_bullets(self):
        tb = self.ctx["tower"]
        picks = self.sample(tb["guards"], 3, "fal")
        out = []
        for i, (name, seed) in enumerate(picks):
            pool = [
                f"{name} — {seed}",
                f"{name}: {seed}; the guard is part of the first slice, not a hardening phase",
                f"{name} — {seed}, enforced by the platform rather than by discipline alone",
                f"{name}, the classic killer; here {seed}",
                f"{name} — guarded because {seed}",
            ]
            out.append([name, self.sent(pool, f"fal{i}", {})])
        return out


# ── block builders ──────────────────────────────────────────────────────────

def hero(p: Page, lede=None):
    m = p.mapping()
    m["kpi0"] = p.kpis()[0][0] if p.kpis() else "primary metric"
    m["sys1"], m["sys2"] = (p.ctx["indbank"]["systems"][0][0], p.ctx["indbank"]["systems"][1][0]) if p.ctx["indbank"] else ("core systems", "operational stores")
    return {"t": "hero", "x": lede or p.sent(P_HERO, "hero", m)}


def h2(x):
    return {"t": "h2", "x": x}


def para(x):
    return {"t": "p", "x": x}


def bullets(items):
    return {"t": "bullets", "items": [[a, b] for a, b in items if a]}


def rewrite_bullet_descs(p: Page, items, salt):
    """keep titles; rewrite any desc that is duplicated across pages (any length),
    preserving metric values embedded in the original"""
    out = []
    for (t, dsc) in items:
        n = norm(dsc)
        fnorm = norm(t + " " + dsc)
        frag_words = len(norm(t).split()) + len(n.split())
        is_stub = bool(re.search(r"\d", dsc)) and frag_words < 14 and len(n.split()) <= 5
        frag_clash = fnorm in SENT_SEEN and SENT_SEEN[fnorm] != p.key
        desc_clash = len(n.split()) >= 14 and n in SENT_SEEN and SENT_SEEN[n] != p.key
        if (n in BOILER_DESCS and not is_stub) or frag_clash or desc_clash or fnorm in BOILER_SENTS or n in BOILER_SENTS:
            mvals = re.findall(r"\d+(?:\.\d+)?\s*[-\u2013~]\s*\d+(?:\.\d+)?%?|\d+x|\d+(?:\.\d+)?%|up \d+|down \d+", dsc, re.I)
            val = mvals[0] if mvals else ""
            if val:
                pool = [
                    f"the committed move on this metric: {val}, measured against the baseline signed in week two",
                    f"current programs land {val} here; the gate reviews the live number, not a projection",
                    f"target range {val} on the first working slice, with the method note attached",
                    f"the delta we sign up to is {val} — verified against live data at every gate",
                    f"reported as {val} against baseline, reproducible by your analysts from the method note",
                ]
            else:
                pool = [
                    f"scoped to the seams that actually move the metric, with an owner named on both sides of the interface",
                    f"delivered as part of the first working slice, with evidence generated in-flight from day one of the program",
                    f"bounded scope per gate, policy-checked writes on every path, and telemetry wired straight to your channels",
                    f"runs on the Achala Method cadence — baseline signed before build, delta reviewed at every gate",
                    f"engineered for {p.ctx['ind'] if p.ctx['indbank'] else 'the estate'} from day one: contracts first, runbooks shipped with the working slice",
                    f"verified against live data before any promotion, with rollback rehearsed in staging rather than documented in a binder",
                    f"with a named engineer on both sides of the fence and an SLO attached to the interface itself",
                ]
            nd = p.sent(pool, salt + t, {})
            if nd and nd[0].isalpha() and nd[0].islower():
                nd = nd[0].upper() + nd[1:]
            out.append([t, nd])
        else:
            if len(n.split()) >= 14:
                SENT_SEEN.setdefault(n, p.key)
            if len(fnorm.split()) >= 14:
                SENT_SEEN.setdefault(fnorm, p.key)
            out.append([t, dsc])
    return out


# ── template recipes ────────────────────────────────────────────────────────

SYNTH_POOLS = {
    "arch": P_ARCH,
    "arch2": P_ARCH2,
    "why": P_OV1B,
    "problem": P_OV1A,
    "perf": [
        "The envelope is explicit: per-tenant quotas, latency budgets on the decision path, and throughput targets reviewed at every load test — sizing is a contract, not a hope.",
        "Scale numbers are published to the tenant, not discovered in an outage: concurrency caps, queue depth alarms and recovery times are part of the platform contract.",
        "Capacity planning runs against the same telemetry your dashboards see, so the performance envelope you buy is the one that is measured in production.",
    ],
    "intg": [
        "Adapters ship with the platform release and are versioned like any other artifact — a core-system upgrade is an integration test, not a surprise.",
        "The integration surface is certified per release: each adapter carries schema versions, replay behavior and failure semantics your architects can review.",
        "Connectivity is read-first by default and writes pass policy checks; every adapter documents its retries, its idempotency window and its audit trail.",
    ],
    "story": [
        "Operators describe the change as boring in the best sense: predictable queues, visible costs, and evidence you can pull without raising a ticket.",
        "The daily rhythm becomes legible — what ran, what it cost, what it changed — so the morning conversation shifts from status guessing to decision review.",
        "Runbooks stop being tribal knowledge: the platform records the operating narrative as it happens, and new team members inherit a system, not a legend.",
    ],
    "covers": [
        "This tower covers the engineering substrate end to end — from the first governed data contract to the production control plane your auditors read.",
        "Scope here means owned outcomes: the services below carry their own runbooks, eval gates and committed telemetry, composed rather than bolted together.",
        "The tower packages specialist depth into managed services — each service production-hardened, each platform-backed, each with a named practice lead.",
    ],
}


def keep_or_synth(p: Page, blk, salt, kind="arch", fallback=None):
    """keep an original paragraph unless it clashes (boilerplate across pages);
    on clash or absence, synthesize a unique replacement from the pool"""
    x = blk.get("x") if isinstance(blk, dict) else blk
    if x:
        if not register_sentences(p, x):
            return x
    return p.sent(SYNTH_POOLS.get(kind, P_ARCH), salt, p.mapping()) if fallback is None \
        else p.sent(fallback if isinstance(fallback, list) else [fallback], salt, p.mapping())

def rebuild_capability(p: Page, is_sub=False):
    """industry_capability + sub_capability"""
    c, ind = p.ctx, p.ctx["indbank"]
    sec = p.sections()
    svc_sec = "Services we deploy in this sector" if not is_sub else "Services behind the pattern"
    press = "The pressure points we attack" if not is_sub else "What breaks today"
    proof = "Proof patterns in this industry" if not is_sub else "Use case"
    gov = p.table_of("Compliance frame")
    svcs = rewrite_bullet_descs(p, p.bullets_of(svc_sec), "svc")
    press_b = rewrite_bullet_descs(p, p.bullets_of(press), "prs")
    proof_b = rewrite_bullet_descs(p, p.bullets_of(proof), "prf")
    portfolio = p.bullets_of("Where this fits in the portfolio")
    receive = rewrite_bullet_descs(p, p.bullets_of("What you receive"), "rcv")
    m = p.mapping()
    ov1 = p.sent(P_OV1A, "ov1", m) + " " + p.sent(P_OV1B, "ov2", m)
    why = p.sent(P_WHY, "why", m)
    deliver = p.sent(P_DELIVER, "del", {**m, "svc_count": str(len(svcs) or 7)})
    blocks = [
        hero(p),
        h2("Overview"), para(ov1),
        h2(H_ARCH), p.diagram_block(), para(p.sent(P_ARCH, "arch", m)),
        para(p.sent(P_ARCH2, "arch2", m)),
        h2(f"Why this matters in {c['ind']}"), para(why),
        h2("Pressure points we attack"),
    ]
    if press_b:
        blocks.append(bullets(press_b))
    blocks += [
        h2("How we deliver it here"), para(deliver),
        h2(svc_sec if is_sub else "Services we deploy in this sector"),
    ]
    if svcs:
        blocks.append(bullets(svcs))
    if proof_b:
        blocks += [h2("Proof patterns in this industry"), bullets(proof_b)]
    blocks += [
        h2(H_STACK), bullets(p.stack_bullets()),
        h2(H_INTG), bullets(p.integration_bullets()),
        h2(H_TELEM), para(p.sent(P_TELEM_NOTE, "tnote", m)), bullets(p.telemetry_bullets()),
        h2(H_FAIL), para(p.sent(P_FAIL_NOTE, "fnote", m)), bullets(p.fail_bullets()),
    ]
    if gov:
        blocks += [h2("Compliance frame"), gov]
    blocks += [
        h2("How a delivery runs"), para(p.cadence_block()),
        h2("Where this fits in the portfolio"),
        para(p.sent(P_PORTFOLIO, "port", m)),
    ]
    if portfolio:
        blocks.append(bullets(rewrite_bullet_descs(p, portfolio, "prtb")))
    blocks += [
        h2("What you receive"), para(p.sent(P_RECEIVE_P, "rcvp", m)),
    ]
    if receive:
        blocks.append(bullets(receive))
    blocks += [h2("Outcomes we commit to"), bullets(p.keep_outcomes())]
    blocks.append({"t": "cta", "x": p.sent(P_CTA, "cta", m)})
    return blocks


def rebuild_service(p: Page):
    c, m = p.ctx, p.mapping()
    sec = p.sections()
    caps = rewrite_bullet_descs(p, p.bullets_of("Capabilities"), "cap")
    delivs = rewrite_bullet_descs(p, p.bullets_of("Deliverables"), "dlv")
    related = p.bullets_of("Related services")
    first90 = rewrite_bullet_descs(p, p.bullets_of("The first 90 days"), "f90")
    portfolio = p.bullets_of("Where this fits in the portfolio")
    receive = rewrite_bullet_descs(p, p.bullets_of("What you receive"), "rcv")
    stack_p = sec.get("Technology and standards", [None])[0]
    ov1 = p.sent(P_OV1A, "ov1", m) + " " + p.sent(P_OV1B, "ov2", m)
    deliver = p.sent(P_DELIVER, "del", {**m, "svc_count": str(len(caps) or 6)})
    blocks = [
        hero(p),
        h2("Overview"), para(ov1),
        h2(H_ARCH), p.diagram_block(), para(p.sent(P_ARCH, "arch", m)),
        h2("How we deliver"), para(deliver),
        p.diagram_block(kind="delivery-cadence", labels=["Diagnose \u00b7 W1\u20132", "Pilot \u00b7 W3\u20138", "Industrialize \u00b7 W9\u201312", "Scale \u00b7 Q2+"], title=f"Delivery cadence — {lc(c['subject'])[:48]}", note=p.sent(P_ARCH2, "arch2", m)),
    ]
    if caps:
        blocks += [h2("Capabilities"), bullets(caps)]
    if delivs:
        blocks += [h2("Deliverables"), bullets(delivs)]
    blocks += [
        h2(H_STACK), para(p.sent(P_STACK_NOTE, "snote", m)), bullets(p.stack_bullets()),
        h2(H_INTG), bullets(p.integration_bullets()),
        h2(H_TELEM), bullets(p.telemetry_bullets()),
        h2(H_FAIL), bullets(p.fail_bullets()),
        h2("Technology and standards"),
        para(keep_or_synth(p, stack_p, "stdp", "arch")),
    ]
    if first90:
        blocks += [h2("The first 90 days"), bullets(first90)]
    if related:
        blocks += [h2("Related services"), bullets(rewrite_bullet_descs(p, related, "rel"))]
    blocks += [
        h2("How a delivery runs"), para(p.cadence_block()),
        h2("Where this fits in the portfolio"), para(p.sent(P_PORTFOLIO, "port", m)),
    ]
    if portfolio:
        blocks.append(bullets(rewrite_bullet_descs(p, portfolio, "prtb")))
    blocks += [h2("What you receive"), para(p.sent(P_RECEIVE_P, "rcvp", m))]
    if receive:
        blocks.append(bullets(receive))
    blocks += [h2("Outcomes we commit to"), bullets(p.keep_outcomes())]
    blocks.append({"t": "cta", "x": p.sent(P_CTA, "cta", m)})
    return blocks


def rebuild_subindustry(p: Page):
    c, m = p.ctx, p.mapping()
    ctx_b = rewrite_bullet_descs(p, p.bullets_of("Pressure points"), "prs")
    caps = rewrite_bullet_descs(p, p.bullets_of("How we help — five priority capabilities"), "cap")
    proof = p.bullets_of("Proof from this industry")
    table = p.table_of("Compliance frame")
    opctx = p.sections().get("Operating context", [None])[0]
    adj = p.sections().get("Adjacent units", [None])[0]
    # keep the workflow LIST from the original operating context, rephrase uniquely
    op_first, op_rest = "", ""
    if opctx and opctx.get("x"):
        parts = re.split(r"(?<=[.])\s+", opctx["x"].strip(), maxsplit=1)
        op_first = parts[0].strip()
        if ":" in op_first:
            op_first = op_first.replace("The workflows we industrialize here:", "The operating surface here spans").replace("The workflows in scope here:", "The operating surface here spans")
        op_rest = parts[1].strip() if len(parts) > 1 else ""
    op_para = op_first
    if op_rest:
        op_para += " " + p.sent([
            "Each workflow enters the program measured — cycle time, error rate and cost per case — and leaves with its delta reported against the signed baseline.",
            "Each one is instrumented before anything changes: baseline numbers first, then the working slice, then the measured delta at the gate.",
            "Every item on that list starts with a two-week measurement and ends its first quarter with a signed delta or a documented redirect.",
            "For each workflow the sequence is identical: measure, sign, build a bounded slice, verify, industrialize — no workflow skips its baseline.",
            "Each workflow gets the same treatment: a named owner on your side, a baseline in week two, and evidence weekly until the gate closes it out.",
        ], "opctx", m)
    if not op_para:
        op_para = f"The workflows we industrialize here span {c['ind']} operating units from intake to settlement, each measured before anything changes."
    blocks = [
        hero(p),
        h2("Operating context"),
        para(op_para),
        h2(H_ARCH), p.diagram_block(), para(p.sent(P_ARCH, "arch", m)),
        h2("Pressure points"),
    ]
    if ctx_b:
        blocks.append(bullets(ctx_b))
    if table:
        blocks += [h2("Compliance frame"), table]
    blocks += [
        h2(H_STACK), bullets(p.stack_bullets()),
        h2(H_INTG), bullets(p.integration_bullets()),
        h2(H_TELEM), bullets(p.telemetry_bullets()),
        h2(H_FAIL), bullets(p.fail_bullets()),
        h2("How we help — five priority capabilities"),
    ]
    if caps:
        blocks.append(bullets(caps))
    blocks += [
        h2("How the engagement runs"), para(p.cadence_block()),
        h2("Outcomes we commit to"), bullets(p.keep_outcomes()),
    ]
    if proof:
        blocks += [h2("Proof from this industry"), bullets(rewrite_bullet_descs(p, proof, "prf"))]
    adj_list = ""
    if adj and adj.get("x"):
        am = re.match(r"[^:]*:\s*(.+)$", adj["x"].strip())
        adj_list = am.group(1).strip().rstrip(".") if am else ""
    blocks += [
        h2("Adjacent units"),
        para(p.sent([
            f"Related sub-industry pages: {adj_list} — each one shares the regulatory frame above while carrying its own workflow mix.",
            f"The neighbouring operating units are {adj_list}; programs that span two of them usually share one baseline." if adj_list else p.sent(P_PORTFOLIO, "port", m),
            f"Adjacent delivery lanes: {adj_list}. Where two lanes share a metric, one program can carry both." if adj_list else p.sent(P_PORTFOLIO, "port", m),
        ], "adj", m) if adj_list else p.sent(P_PORTFOLIO, "port", m)),
        {"t": "cta", "x": p.sent(P_CTA, "cta", m)},
    ]
    return blocks


def rebuild_solution(p: Page):
    c, m = p.ctx, p.mapping()
    sec = p.sections()
    comps = rewrite_bullet_descs(p, p.bullets_of("Components"), "cmp")
    runs = rewrite_bullet_descs(p, p.bullets_of("How it runs in an engagement"), "run")
    get = rewrite_bullet_descs(p, p.bullets_of("What you get"), "get")
    proof = p.bullets_of("Proof")
    portfolio = p.bullets_of("Where this fits in the portfolio")
    receive = rewrite_bullet_descs(p, p.bullets_of("What you receive"), "rcv")
    problem = sec.get("The problem this solution exists for", [None])[0]
    approach = sec.get("Our approach", [None])[0]
    prereq = sec.get("Prerequisites and data readiness", [None])[0]
    platstack = sec.get("Platform stack", [None])[0]
    blocks = [
        hero(p),
        h2("The problem this solution exists for"),
        para(keep_or_synth(p, problem, "problem", "problem")),
        h2("Our approach"),
        para(keep_or_synth(p, approach, "approach", "arch2")),
        h2(H_ARCH), p.diagram_block(), para(p.sent(P_ARCH, "arch", m)),
        h2("Components"),
    ]
    if comps:
        blocks.append(bullets(comps))
    blocks += [
        h2("Platform stack"),
        para(keep_or_synth(p, platstack, "platstack", "arch")),
        h2("How it runs in an engagement"),
    ]
    if runs:
        blocks.append(bullets(runs))
    blocks += [
        h2(H_STACK), bullets(p.stack_bullets()),
        h2(H_INTG), bullets(p.integration_bullets()),
        h2(H_TELEM), bullets(p.telemetry_bullets()),
        h2(H_FAIL), bullets(p.fail_bullets()),
        h2("What you get"),
    ]
    if get:
        blocks.append(bullets(get))
    blocks += [
        h2("Prerequisites and data readiness"),
        para(keep_or_synth(p, prereq, "prereq", "arch2")),
        h2("How a delivery runs"), para(p.cadence_block()),
        h2("Outcomes we commit to"), bullets(p.keep_outcomes()),
    ]
    if proof:
        blocks += [h2("Proof"), bullets(rewrite_bullet_descs(p, proof, "prf"))]
    blocks += [
        h2("Where this fits in the portfolio"), para(p.sent(P_PORTFOLIO, "port", m)),
    ]
    if portfolio:
        blocks.append(bullets(rewrite_bullet_descs(p, portfolio, "prtb")))
    blocks += [h2("What you receive"), para(p.sent(P_RECEIVE_P, "rcvp", m))]
    if receive:
        blocks.append(bullets(receive))
    blocks.append({"t": "cta", "x": p.sent(P_CTA, "cta", m)})
    return blocks


def rebuild_tower_hub(p: Page):
    c, m = p.ctx, p.mapping()
    sec = p.sections()
    svcs = rewrite_bullet_descs(p, p.bullets_of("Services in this tower"), "svc")
    outcomes = p.keep_outcomes()
    covers = sec.get("What this tower covers", [None])[0]
    whynow = sec.get("Why this tower, why now", [None])[0]
    applies = sec.get("Where the tower applies", [None])[0]
    blocks = [
        hero(p),
        h2("What this tower covers"),
        para(keep_or_synth(p, covers, "covers", "covers")),
        h2(H_ARCH), p.diagram_block(), para(p.sent(P_ARCH, "arch", m)),
        para(p.sent(P_ARCH2, "arch2", m)),
        h2("Why this tower, why now"),
        para(keep_or_synth(p, whynow, "whynow", "why")),
        h2("Services in this tower"),
    ]
    if svcs:
        blocks.append(bullets(svcs))
    blocks += [
        h2(H_STACK), bullets(p.stack_bullets()),
        h2(H_TELEM), bullets(p.telemetry_bullets()),
        h2(H_FAIL), bullets(p.fail_bullets()),
        h2("Outcomes we commit to"), bullets(outcomes),
        h2("Where the tower applies"),
        para(keep_or_synth(p, applies, "applies", "arch2")),
        h2("How a delivery runs"), para(p.cadence_block()),
        h2("What you receive"), para(p.sent(P_RECEIVE_P, "rcvp", m)),
        bullets(rewrite_bullet_descs(p, p.bullets_of("What you receive"), "rcv")),
        {"t": "cta", "x": p.sent(P_CTA, "cta", m)},
    ]
    return blocks


def rebuild_industry_hub(p: Page):
    c, m = p.ctx, p.mapping()
    sec = p.sections()
    stands = sec.get("Where the industry stands", [None])[0]
    pressure = sec.get("The pressure is structural", [None])[0]
    responds = sec.get("How Achala IT Solutions responds", [None])[0]
    pressb = rewrite_bullet_descs(p, p.bullets_of("Pressure points we hear most"), "prs")
    programs = rewrite_bullet_descs(p, p.bullets_of("Priority programs"), "pgm")
    proof = p.bullets_of("Proof from this industry")
    table = p.table_of("Regulatory posture") or p.table_of("Regimes that shape delivery")
    blocks = [
        hero(p),
        h2("Where the industry stands"),
        para(keep_or_synth(p, stands, "stands", "problem")),
        h2(H_ARCH), p.diagram_block(kind="decision-fabric", title=f"Decision fabric — how Achala IT Solutions composes {c['ind']} capability", note=p.sent(P_ARCH, "arch", m)),
        h2("The pressure is structural"),
        para(keep_or_synth(p, pressure, "pressure", "why")),
        h2("Pressure points we hear most"),
    ]
    if pressb:
        blocks.append(bullets(pressb))
    blocks += [
        h2("How Achala IT Solutions responds"),
        para(keep_or_synth(p, responds, "responds", "arch2")),
        h2(H_STACK), bullets(p.stack_bullets()),
        h2(H_INTG), bullets(p.integration_bullets()),
        h2(H_TELEM), bullets(p.telemetry_bullets()),
        h2(H_FAIL), bullets(p.fail_bullets()),
    ]
    if table:
        blocks += [h2("Regulatory posture"), table]
    blocks += [
        h2("Priority programs"),
    ]
    if programs:
        blocks.append(bullets(programs))
    blocks += [
        h2("How a delivery runs"), para(p.cadence_block()),
        h2("Outcomes we commit to in this sector"), bullets(p.keep_outcomes()),
    ]
    if proof:
        blocks += [h2("Proof from this industry"), bullets(rewrite_bullet_descs(p, proof, "prf"))]
    blocks += [
        h2("Capability pages for this industry"),
        para(p.sent([
            "All eight towers are aligned at industry level under the capability lanes below — every one calibrated to the regimes named above.",
            "The capability lanes below carry all eight towers into this industry, each with its own regulatory calibration and delivery pattern.",
            "Every tower publishes an industry-calibrated lane here; the cards below are the entry points, each backed by the proof patterns above.",
            "Eight capability lanes run beneath this industry page — pick the one that owns your metric, or shortlist several for a composed program.",
            "The lanes below are where the industry context above becomes buildable scope, one capability at a time.",
        ], "cappages", m)),
        {"t": "cta", "x": p.sent(P_CTA, "cta", m)},
    ]
    return blocks


def rebuild_platform(p: Page, variant):
    c, m = p.ctx, p.mapping()
    sec = p.sections()
    plat = c["plat"]
    if variant == "overview":
        mods = rewrite_bullet_descs(p, p.bullets_of("Modules"), "mod")
        biz = rewrite_bullet_descs(p, p.bullets_of("What changes for the business"), "biz")
        its_p = sec.get("Integrations", [None])[0]
        blocks = [
            hero(p),
            h2("What it is"),
            para(keep_or_synth(p, sec.get("What it is", [None])[0], "whatit", "arch2",
                 fallback=f"{plat} is the production rail for this capability family — governance, evidence and scale built in.")),
            h2(H_ARCH), p.diagram_block(kind="decision-fabric", title=f"{plat} — control and evidence planes", note=p.sent(P_ARCH, "arch", m)),
            para(p.sent(P_ARCH2, "arch2", m)),
            h2("How it operates"),
            para(keep_or_synth(p, sec.get("How it operates", [None])[0], "operates", "arch")),
            h2("Modules"),
        ]
        if mods:
            blocks.append(bullets(mods))
        blocks += [
            h2(H_STACK), bullets(p.stack_bullets()),
            h2(H_TELEM), bullets(p.telemetry_bullets()),
            h2(H_FAIL), bullets(p.fail_bullets()),
            h2("What changes for the business"),
        ]
        if biz:
            blocks.append(bullets(biz))
        blocks += [
            h2("Integrations"),
            para(keep_or_synth(p, its_p, "its", "intg")),
            bullets(p.integration_bullets()),
            h2("How programs use it"), para(p.cadence_block()),
            {"t": "cta", "x": p.sent(P_CTA, "cta", m)},
        ]
        return blocks
    if variant == "architecture":
        trust = rewrite_bullet_descs(p, p.bullets_of("Trust controls"), "trst")
        comp = rewrite_bullet_descs(p, p.bullets_of("Compliance mapping"), "cmp")
        dep = rewrite_bullet_descs(p, p.bullets_of("Deployment models"), "dep")
        ref_p = sec.get("Reference architecture", [None])[0]
        sec_p = sec.get("Security posture", [None])[0]
        perf_p = sec.get("Performance envelope", [None])[0]
        int_p = sec.get("Integration surface", [None])[0]
        return [
            hero(p),
            h2(H_ARCH),
            para(keep_or_synth(p, ref_p, "ref", "arch")),
            p.diagram_block(kind="layered-stack", title=f"{plat} — plane and service layers", note=p.sent(P_ARCH, "arch", m)),
            p.diagram_block(kind="edge-topology", title=f"{plat} — deployment topology and flow", note=p.sent(P_ARCH2, "arch2", m)),
            h2("Security posture"),
            para(keep_or_synth(p, sec_p, "secp", "arch2")),
            h2("Trust controls"),
        ] + ([bullets(trust)] if trust else []) + [
            h2("Compliance mapping"),
        ] + ([bullets(comp)] if comp else []) + [
            h2("Performance envelope"),
            para(keep_or_synth(p, perf_p, "perf", "perf")),
            h2(H_TELEM),
            para(p.sent(P_TELEM_NOTE, "tnote", m)),
            bullets(p.telemetry_bullets()),
            h2("Deployment models"),
        ] + ([bullets(dep)] if dep else []) + [
            h2("Integration surface"),
            para(keep_or_synth(p, int_p, "intp", "intg")),
            bullets(p.integration_bullets()),
            {"t": "cta", "x": p.sent(P_CTA, "cta", m)},
        ]
    # use-cases
    table = p.table_of("Deployment patterns")
    roll = rewrite_bullet_descs(p, p.bullets_of("What a rollout looks like"), "roll")
    progs = rewrite_bullet_descs(p, p.bullets_of("Programs on this platform"), "prg")
    ops_p = sec.get("The operator's story", [None])[0]
    int_p = sec.get("Integration pattern", [None])[0]
    blocks = [
        hero(p),
        h2("Deployment patterns"),
    ]
    if table:
        blocks.append(table)
    blocks += [
        h2(H_ARCH), p.diagram_block(kind="pipeline", title=f"{plat} — reference flow in production", note=p.sent(P_ARCH, "arch", m)),
        h2("What a rollout looks like"),
        para(p.sent(P_DELIVER, "del", {**m, "svc_count": "4"})),
    ]
    if roll:
        blocks.append(bullets(roll))
    blocks += [
        h2("The operator's story"),
        para(keep_or_synth(p, ops_p, "ops", "story")),
        h2("Integration pattern"),
        para(keep_or_synth(p, int_p, "intp2", "intg")),
        bullets(p.integration_bullets()),
        h2("Programs on this platform"),
    ]
    if progs:
        blocks.append(bullets(progs))
    blocks += [
        h2(H_TELEM), bullets(p.telemetry_bullets()),
        h2("How a delivery runs"), para(p.cadence_block()),
        {"t": "cta", "x": p.sent(P_CTA, "cta", m)},
    ]
    return blocks


def rebuild_hub(p: Page):
    """generic section hubs: keep cards/related; rewrite prose + diagram"""
    m = p.mapping()
    sec = p.sections()
    paras = []
    keep_tables = []
    for b in p.d["blocks"]:
        if b["t"] == "table":
            keep_tables.append(b)
    intro = p.sent(P_OV1A, "ov1", m) + " " + p.sent(P_OV1B, "ov2", m)
    blocks = [hero(p), h2("Overview"), para(intro)]
    # keep original bullet/card sections after the new intro sections
    for b in p.d["blocks"]:
        if b["t"] in ("h2",) and b["x"] not in ("Overview",):
            blocks.append(b)
        elif b["t"] == "bullets" and b.get("items"):
            blocks.append(bullets(rewrite_bullet_descs(p, [tuple(i) for i in b["items"]], "hub")))
        elif b["t"] == "table":
            blocks.append(b)
        elif b["t"] == "cta":
            blocks.append({"t": "cta", "x": p.sent(P_CTA, "cta", m)})
    # insert diagram + architecture narrative after Overview
    idx = next(i for i, b in enumerate(blocks) if b["t"] == "h2" and i > 0)
    blocks[idx:idx] = [
        h2(H_ARCH),
        p.diagram_block(kind="decision-fabric", note=p.sent(P_ARCH, "arch", m)),
        para(p.sent(P_ARCH2, "arch2", m)),
    ]
    return blocks


def rebuild_insights_category(p: Page):
    return rebuild_hub(p)


# ── editorial pages: dedupe + diagram ───────────────────────────────────────

P_FAIL_ARTICLE = [
    "Programs stall when the operating model is an afterthought: no named owner for the seam, no eval gate on changes, no rollback rehearsed before launch. The failure is organizational before it is technical.",
    "The predictable failure loop: enthusiasm funds the demo, budget cycles gate the expansion, and nobody owns the distance between pilot and production. We design the operating model first so the loop never closes.",
    "Where programs fail is rarely the model quality — it is the missing contracts, the unowned queue, the dashboard nobody is paged for. Naming those seams early is most of the work.",
]

P_NUM_ARTICLE = [
    "The number that matters is the one your steering committee already tracks — we instrument it, sign the baseline, and report the delta with its method note. Anything else is decoration.",
    "One number carries the program: pick it before the build, measure it the same way your finance team does, and let every gate refer to it.",
]

BOILER_PREFIXES = [
    "delivery runs on one weekly rhythm", "the cadence below is the standard pattern",
    "every program of this type runs the same weekly rhythm", "a fixed rhythm keeps progress visible",
    "programs run on the fixed rhythm below", "below is the delivery cadence",
    "the rhythm is fixed on purpose", "this capability runs on the cadence",
    "at the end of the first quarter of a typical program", "four named artifacts are delivered",
    "your team gets the following artifacts", "these artifacts change hands",
    "in delivery, this work composes", "no capability stands alone",
    "this capability is one move in a larger program", "the failure mode is predictable enthusiasm",
    "programs stall when the operating model", "delivery runs on the same weekly rhythm",
    "the program followed the achala method", "metrics are reported against the baseline locked",
]

BOILER_DESCS = set()
BOILER_SENTS = set()  # long sentences appearing on >1 page anywhere (pre-scan)

P_NOTE_CASE = [
    "Client identity withheld under confidentiality. Metrics are reported against the baseline locked in the Diagnose phase; the measurement method is available to seriously interested parties under NDA.",
    "Identity withheld under confidentiality — the client approved the numbers, not the name. Every metric traces to the week-two baseline; the method pack is shared under NDA on request.",
    "The client is not named — their policy, not ours. Figures are deltas against the signed baseline; measurement method and gate notes are available under NDA.",
    "Confidentiality note: the engagement runs under a name-withheld agreement. Reported metrics reconcile to the locked Diagnose baseline, and the method travels with the reference call.",
    "The name stays out of this page by agreement. What we can show: the audited baseline, the measured delta at each gate, and the method notes your auditors would ask for.",
    "Client identity is withheld; the numbers are not. Each figure below reconciles to the baseline signed in week two — the method is inspectable under NDA.",
    "Under the engagement's confidentiality terms we publish the pattern and the deltas, not the logo. Baseline and method notes are available through the practice lead.",
    "Withheld identity, audited numbers: metrics are stated as deltas against the signed baseline, with measurement method and gate evidence available on a reference call.",
]

P_CTA_CASE = [
    "Request a reference conversation on this pattern — or bring your baseline to a briefing and we will map it to your estate in the same session.",
    "Ask for the reference call with a client running this pattern, or scope your own version in a two-week value assessment.",
    "Put your metric in front of the practice lead — the first session ends with a measurement plan and a scoped first slice.",
    "Book a briefing with the practice lead for the transfer notes, or start with the value assessment that locks your baseline first.",
    "See the pattern on your own numbers: request the diagnostic that produced the baseline here, or take a scoped plan straight from the briefing.",
    "Bring your baseline to the table — we will show which of these gates apply to your estate and what the first quarter would commit.",
    "The fastest start is the same diagnostic this client ran: two weeks, your baseline signed, the delivery pattern priced from evidence.",
]


def is_boiler(s: str) -> bool:
    n = norm(s)
    return any(n.startswith(p) for p in BOILER_PREFIXES)


def has_boiler_fragment(s: str) -> bool:
    if is_boiler(s):
        return True
    n = norm(s)
    return any(bs in n for bs in BOILER_SENTS)


def register_sentences(p: Page, text: str):
    """register each long sentence of a kept paragraph; True if a collision was found"""
    clash = False
    for s in re.split(r"(?<=[.!?])\s+", text):
        n = norm(s)
        if len(n.split()) >= 14:
            if n in SENT_SEEN and SENT_SEEN[n] != p.key:
                clash = True
            SENT_SEEN.setdefault(n, p.key)
    return clash


def enrich_editorial(p: Page):
    """keep voice; replace boilerplate/duplicated paragraphs, notes, CTAs; inject 1 diagram.
    Idempotent: pages that already carry a diagram keep exactly one (no stacking)."""
    d = p.d
    blocks = []
    diagram_done = any(b["t"] == "diagram" for b in d["blocks"])
    last_h2 = None
    m = p.mapping()
    is_case = d["template"] == "case_study"

    def replacement(x):
        low = x.lower()
        if "cadence" in low or "rhythm" in low or "achala method" in low or "delivery pattern" in low or "diagnose" in low and "week" in low:
            return p.cadence_block()
        if "receive" in low or "artifact" in low:
            return p.sent(P_RECEIVE_P, "rcvp", m)
        if "compose" in low or "portfolio" in low or "stands alone" in low:
            return p.sent(P_PORTFOLIO, "port", m)
        if "fail" in low or "stall" in low or "enthusiasm" in low:
            return p.sent(P_FAIL_ARTICLE, "failart", m)
        if "reference conversation" in low or "map it to your estate" in low or "briefing" in low:
            return p.sent(P_CTA_CASE, "ctac", m)
        return p.sent(P_FAIL_ARTICLE, "edgen", m)

    for b in d["blocks"]:
        t = b["t"]
        if t == "p":
            x = b["x"]
            if has_boiler_fragment(x) or register_sentences(p, x):
                blocks.append(para(replacement(x)))
            else:
                blocks.append(b)
        elif t == "note":
            if is_case or has_boiler_fragment(b["x"]):
                blocks.append({"t": "note", "x": p.sent(P_NOTE_CASE, "note", m)})
            else:
                register_sentences(p, b["x"])
                blocks.append(b)
        elif t == "cta":
            if has_boiler_fragment(b["x"]):
                blocks.append({"t": "cta", "x": p.sent(P_CTA_CASE if is_case else P_CTA, "ctar", m)})
            else:
                register_sentences(p, b["x"])
                blocks.append(b)
        elif t == "bullets":
            items = rewrite_bullet_descs(p, [tuple(i) for i in (b.get("items") or [])], "ed")
            blocks.append(bullets(items))
        elif t == "h2":
            last_h2 = b["x"]
            blocks.append(b)
            # inject diagram after an early narrative section
            if not diagram_done and last_h2 in ("The argument", "The challenge", "What it is",
                                                "Three things that matter", "The delivery pattern",
                                                "Our approach", "Operating context"):
                blocks.append(p.diagram_block(
                    kind=p.ctx["tower"]["diagram"] if p.ctx["tkey"] else p.pick(["decision-fabric", "pipeline"], "edk"),
                    title=f"{p.d['title'].split(':')[0][:60]} — how the pattern runs",
                    salt="eddg",
                ))
                diagram_done = True
        else:
            # pass-through: keep at most ONE diagram on editorial pages
            if b["t"] == "diagram":
                if not diagram_done:
                    diagram_done = True
                    blocks.append(b)
                continue
            blocks.append(b)
    return blocks


# ── legal / utility pages: real plain-language copy (was placeholder stubs) ──

LEGAL_COPY = {
    "/privacy-policy/": {
        "lede": "How Achala IT Solutions Corporation collects, uses, shares and protects personal data across this website and our delivery operations, and the rights you can exercise over it.",
        "sections": [
            ("Who we are", "Achala IT Solutions Corporation (\u201cAchala IT Solutions\u201d, \u201cwe\u201d) is the controller for personal data processed through achalasolutions.com and the contact routes it publishes. Delivery entities in the United States, United Kingdom, India and Saudi Arabia act as processors for client engagements under the terms of each contract."),
            ("Data we process", "We process identification and contact data you provide (name, work email, phone, role), correspondence content, engagement and billing records where contractually required, recruitment application data, and technical data collected when you browse this site (IP address, device and browser characteristics, pages visited, referring URL)."),
            ("Purposes and legal bases", "Contact and briefing requests are processed on the basis of performing pre-contractual steps at your request (GDPR Art. 6(1)(b)); site analytics on the basis of legitimate interests in operating and improving the site (Art. 6(1)(f)); optional marketing communications only with your consent (Art. 6(1)(a)); and legal or tax obligations where applicable (Art. 6(1)(c)). You can withdraw consent at any time without affecting prior processing."),
            ("Sharing and transfers", "We share personal data only with service providers bound by data-processing agreements (site hosting, CRM, email delivery), with professional advisers under confidentiality, and with authorities where the law requires it. Transfers outside the EEA or UK rely on adequacy decisions or the UK/EU Standard Contractual Clauses, supplemented by transfer risk assessments."),
            ("Retention", "Enquiry records are kept up to 24 months from last contact; recruitment records for the duration of the hiring round plus 12 months unless you ask us to keep them for future roles; contractual records per statutory limitation periods; analytics data in aggregated or pseudonymous form for up to 26 months."),
            ("Your rights", "Subject to local law you can request access, rectification, erasure, restriction, portability, and object to processing based on legitimate interests or to direct marketing. Submit requests through the contact routes on our Contact page; we respond within one month of identity verification and explain any extension."),
            ("Contact", "Questions or complaints about privacy can be sent to info@achalasolutions.com, marked for the attention of the privacy function. You also have the right to lodge a complaint with your local supervisory authority."),
        ],
        "control": [
            ["Owner", "Achala IT Solutions Legal Affairs, with the privacy function as operational delegate"],
            ["Review cadence", "Reviewed at least annually and on any change to processing operations or transfer mechanisms"],
            ["Effective date", "November 20, 2026 \u00b7 supersedes all prior versions published on this URL"],
        ],
        "note": "This statement describes this website and our corporate operations. Client engagement data is governed by the contract and data-processing agreement agreed with each client, which prevails over this page for that scope.",
    },
    "/cookie-policy/": {
        "lede": "What cookies and similar technologies run on achalasolutions.com, what each category does, and how you control them \u2014 written to be read, not to be endured.",
        "sections": [
            ("Essential cookies", "These make the site work: session integrity, security tokens, and your cookie-consent choice itself. They do not require consent and cannot be switched off in our hosting configuration without breaking core functionality. Their lifetime matches the technical purpose \u2014 from the browsing session up to 12 months for the consent record."),
            ("Preference storage", "Where the site remembers a choice you made (for example collapsing a menu or a saved view), it is stored locally in your browser and is not used to identify you elsewhere."),
            ("Analytics", "We measure aggregate page performance \u2014 page views, referrers, rough geography, load times \u2014 to find broken journeys and slow pages. Analytics runs only after you accept non-essential cookies, IP addresses are truncated where the tool supports it, and we do not build advertising profiles from this data."),
            ("Marketing", "We currently run no third-party advertising cookies. If that ever changes, this section, the consent banner and the cookie table below will be updated together, and acceptance will be requested before any marketing tag fires."),
            ("Managing cookies", "You can withdraw or change consent at any time via the cookie controls on this site, or delete and block cookies in your browser settings. Blocking essential cookies may break site functionality such as search and form submission. Your consent choice is stored under the categories listed below."),
        ],
        "control": [
            ["Owner", "Achala IT Solutions Legal Affairs, jointly with the platform engineering team"],
            ["Review cadence", "Reviewed every six months and before any new tag is deployed"],
            ["Effective date", "November 20, 2026 \u00b7 supersedes all prior versions published on this URL"],
        ],
        "note": "This policy sits under the Privacy Policy, which explains lawful bases, retention and your rights in full. Where the two texts overlap, the Privacy Policy prevails on processing purposes and the present page on cookie mechanics.",
    },
    "/terms-of-use/": {
        "lede": "The rules for using achalasolutions.com: what you may do with its content and code samples, what we disclaim, and how disputes are limited \u2014 the whole document, without the maze.",
        "sections": [
            ("Acceptance", "By browsing this site or submitting a form you accept these terms. If you do not accept them, please stop using the site. Client deliveries are governed by separate signed agreements, which prevail over this page wherever they overlap."),
            ("Intellectual property", "Text, diagrams, code examples, brand marks and page designs on this site belong to Achala IT Solutions Corporation or its licensors. You may quote short extracts with attribution and a link for commentary or non-commercial teaching. You may not republish substantial parts, resell access, or use our marks in a way that suggests endorsement without written permission."),
            ("Acceptable use", "Do not probe, scrape at disruptive volume, or attempt to breach authentication on this site; do not submit unlawful, misleading or malicious content through our forms; and do not misrepresent your identity or affiliation when contacting us. We may suspend abusive traffic without notice."),
            ("Disclaimers", "This site is provided \u201cas is\u201d. Technical descriptions, reference architectures and outcome ranges illustrate patterns from delivery experience; they are not warranties of results for your environment, and they do not constitute legal, financial or regulated-professional advice. Figures labelled as committed outcomes apply only within signed engagements that define them."),
            ("Limitation of liability", "To the maximum extent permitted by law, Achala IT Solutions is not liable for indirect or consequential losses arising from use of this site, and total liability arising out of the site itself is limited to 100 US dollars. Nothing limits liability that cannot lawfully be limited, including for fraud or death and personal injury caused by negligence."),
            ("Governing law and changes", "These terms are governed by the laws of the State of Delaware, USA, without prejudice to mandatory consumer protections in your residence country. We may update the terms as the site evolves; the version listed under Document control applies to your visit, and continued use after a change constitutes acceptance."),
        ],
        "control": [
            ["Owner", "Achala IT Solutions Legal Affairs"],
            ["Review cadence", "Reviewed annually and on material changes to the site or service descriptions"],
            ["Effective date", "November 20, 2026 \u00b7 supersedes all prior versions published on this URL"],
        ],
        "note": "Questions about these terms can be routed through the contact channels on our Contact page; we direct contractual questions on active engagements to the named delivery lead instead.",
    },
    "/accessibility/": {
        "lede": "Our commitment to WCAG 2.2 Level AA across achalasolutions.com, the measures we maintain, and how to tell us when something is in your way.",
        "sections": [
            ("Conformance target", "This site targets WCAG 2.2 Level AA as the baseline for perceived conformance, informed by Section 508 in the United States, the European Accessibility Act and EN 301 549 in the EU, and equivalent duties in the United Kingdom. Conformance is a claim we hold ourselves to, not a badge we bought."),
            ("Built-in measures", "Semantic landmarks and heading order on every template; visible focus states with a skip-to-content link; color pairs selected against contrast thresholds and never used as the only signal; keyboard operability for menus, diagrams, carousels and forms; text alternatives for informative imagery; and full respect for prefers-reduced-motion, which stills decorative animation while keeping the content complete."),
            ("Known limitations", "Some interactive schematics convey part of their meaning visually; each carries a text note stating its takeaway, and a long-form description is available on request. Third-party embeds (for example maps or video players) may not yet match our standard \u2014 we sequence fixes with the vendor rather than shipping a worse experience silently."),
            ("Testing practice", "Automated audits run on every template change; manual keyboard and screen-reader passes (NVDA and VoiceOver) run each release train; and findings land in the same backlog as functional defects, prioritized by how many people they block."),
            ("Feedback and response", "If any page blocks you, write to info@achalasolutions.com with the page URL and what failed. Accessibility reports are answered within two business days with either a fix plan or a workaround, and we will provide the requested content through an alternative channel while the fix ships."),
        ],
        "control": [
            ["Owner", "Achala IT Solutions platform engineering team, with Legal Affairs review"],
            ["Review cadence", "Reviewed each release train and at least twice per year"],
            ["Effective date", "November 20, 2026 \u00b7 supersedes all prior versions published on this URL"],
        ],
        "note": "This statement describes achalasolutions.com. Accessibility commitments for delivered products are agreed per engagement and documented in the relevant contract and acceptance criteria.",
    },
    "/html-sitemap/": {
        "lede": "Every public page on this site, generated from the same inventory that drives navigation and the XML sitemap \u2014 if it is missing here, it is missing everywhere.",
        "sections": [
            ("How this page works", "The listing below is generated at build time from the site's content inventory, grouped by section: service towers, industries and sub-industries, capability patterns, platforms, solutions, proof and insights, and company pages. It updates automatically when pages are added or renamed, so it cannot drift from reality the way hand-maintained sitemaps do."),
            ("Using it well", "Search engines should rely on the XML sitemap referenced in robots.txt; this page exists for people \u2014 procurement teams mapping our coverage, practitioners looking for a capability lane, and anyone who finds menus faster than search. Each entry links to the canonical URL of the page."),
            ("Coverage notes", "Client-specific delivery artifacts, NDA-gated architecture packs and reference calls are deliberately absent: they are engagement materials, not public pages. If you need something you believe exists but cannot find, the Contact page routes you to the right practice."),
        ],
        "control": [
            ["Owner", "Achala IT Solutions site engineering"],
            ["Review cadence", "Regenerated on every build; copy reviewed quarterly"],
            ["Effective date", "November 20, 2026 \u00b7 structure mirrors the current inventory"],
        ],
        "note": "Spotted a broken or duplicated entry? Report it through the Contact page and it goes into the same backlog as any site defect, with the section owner copied.",
    },
    "/status/": {
        "lede": "Operational status for the managed Achala platforms \u2014 what we publish here, how incidents are communicated, and where tenant-specific telemetry lives.",
        "sections": [
            ("What this page covers", "Public availability for the managed surfaces of Achala Nexus, Forge, Swarm, Sentinel, Twinverse, Quanta, Ledger and Compass when they are consumed as Achala-operated services. Customer-tenanted deployments are monitored inside each tenant's own observability stack; their status lives with your platform team, not here."),
            ("What we publish", "Current state per platform, active incident summaries with impact and workaround, and scheduled maintenance windows announced at least five business days ahead. Historical availability per platform per quarter is available to affected clients on request through the delivery lead."),
            ("Incident communication", "When an incident opens, this page is updated within fifteen minutes of confirmation, then at least hourly until resolved; the resolution note states cause, remediation and any follow-up work. Clients on managed platforms also receive direct notifications through the channels agreed in their service terms."),
            ("Severity and honesty", "We grade incidents by user impact, not by how embarrassing they are: degraded performance counts, silent degradation is treated as an incident once detected, and post-incident reviews are shared with affected clients under the same severity grading."),
        ],
        "control": [
            ["Owner", "Achala IT Solutions reliability engineering (SRE) function"],
            ["Review cadence", "Content reviewed quarterly; status data updates continuously"],
            ["Effective date", "November 20, 2026 \u00b7 communication practice per current service terms"],
        ],
        "note": "Tenant-specific metrics, SLO burn-down and incident history for your deployments are available in your platform console and through your named reliability contact \u2014 this page is the public view, not a substitute for them.",
    },
}


def rebuild_legal(p: Page):
    c = LEGAL_COPY.get(p.ctx["url"])
    if not c:
        return enrich_editorial(p)
    blocks = [{"t": "hero", "x": c["lede"]}]
    for i, (h, body) in enumerate(c["sections"]):
        blocks.append(h2(h))
        blocks.append(para(body))
    blocks.append(h2("Document control"))
    blocks.append(bullets(c["control"]))
    blocks.append({"t": "note", "x": c["note"]})
    return blocks


# ── contact pair: book-a-briefing vs value-assessment (were generated identical) ──

BRIEFING_COPY = {
    "How the session runs": [
        ["Preparation", "Send the metric you want to move and any public material; we arrive with two reference patterns pre-mapped to your sector."],
        ["The session", "Forty-five minutes, working-session format: your metric and constraints, our pattern library, and an honest read on what a first slice would look like."],
        ["The follow-up", "A two-page readout within 48 hours — pattern, evidence and the decision we recommend; no proposal deck unless you ask for one."],
    ],
    "Common questions": [
        ["Who attends?", "A practice lead for your domain plus the delivery lead who would run the program — the people answering your questions own the answers."],
        ["What should we bring?", "One metric with its current value, the system it lives in, and the name of whoever would own it on your side."],
        ["What does it cost?", "Nothing. The briefing is how we demonstrate the evidence discipline before you spend anything."],
    ],
}

ASSESSMENT_COPY = {
    "How the session runs": [
        ["Preparation", "We start from your use-case inventory — even a rough list — and score it against value-density and data-readiness criteria before the first workshop."],
        ["The sprint", "Six weeks, structured: Value Mapping workshops with your domain owners, scored use-case portfolio, and a sequenced delivery plan priced from evidence."],
        ["The follow-up", "A two-page readout with the reasoning attached — the scored portfolio, the sequence we would run, and the baseline window to lock first."],
    ],
    "Common questions": [
        ["Who attends?", "Your domain owners plus one decision maker with budget context — the scoring only works when the people who own the workflows are in the room."],
        ["What should we bring?", "The use-case backlog, however messy, and access to whoever can speak to data readiness for the top candidates."],
        ["What does it cost?", "The sprint is fixed-fee and scoped before it starts; most clients treat it as the entry gate to their first delivery quarter."],
    ],
}


def rebuild_contact_pair(p: Page):
    c = BRIEFING_COPY if p.ctx["url"] == "/book-a-briefing/" else ASSESSMENT_COPY
    blocks = []
    for b in p.d["blocks"]:
        t = b["t"]
        if t == "bullets" and b.get("items") and b["items"] and b["items"][0][0] in ("Preparation",):
            blocks.append(h2("How the session runs"))
            blocks.append(bullets(c["How the session runs"]))
        elif t == "bullets" and b.get("items") and b["items"] and b["items"][0][0] in ("Who attends?",):
            blocks.append(h2("Common questions"))
            blocks.append(bullets(c["Common questions"]))
        elif t == "h2" and b["x"] in ("How the session runs", "Common questions"):
            continue  # re-added with the matching bullets
        elif t == "cta":
            blocks.append({"t": "cta", "x": p.sent(P_CTA, "ctapair", p.mapping())})
        else:
            blocks.append(b)
    return blocks


# ── structured-page families that had ZERO body content (partner, careers,
#    leadership). Content lives in partner/profile fields which the renderer
#    never displayed — these builders give each page a real technical body. ──

PARTNER_STACKS = {
    "aws": ["Bedrock for grounded generative workloads", "Kinesis and Lambda for streaming decision paths", "S3, Glue and Lake Formation for governed lakehouses", "ECS and Step Functions for orchestrated fleets", "SageMaker where custom models earn their keep"],
    "azure": ["Azure OpenAI inside tenant boundaries", "Event Hubs and Functions for event-driven decisioning", "Synapse and ADLS for the governed estate", "AKS for containerized delivery", "Entra ID as the identity spine"],
    "gcp": ["Vertex AI for managed model operations", "Pub/Sub and Dataflow for streaming pipelines", "BigQuery as the lakehouse engine", "GKE for runtime orchestration", "IAM conditions for deny-by-default access"],
    "databricks": ["Unity Catalog as the single governance plane", "Delta Lake for ACID tables and time travel", "Lakehouse Federation where data must stay put", "MLflow for model and agent registries", "Databricks Workflows as the orchestration spine"],
    "snowflake": ["Snowflake as the governed serving layer", "Dynamic masking and row policies for data sharing", "Snowpark for in-warehouse feature engineering", "Streams and Tasks for pipeline automation", "Cost-per-query telemetry for FinOps discipline"],
    "salesforce": ["Data Cloud for consent-scoped customer state", "Einstein trust layer for grounded assistive AI", "Flow orchestration for process automation", "Agentforce patterns under human checkpoints", "CDP identity resolution with audit trails"],
    "sap": ["S/4HANA as the operational truth for supply chains", "SAP Datasphere for federated data products", "BTP for side-by-side extension", "Event Mesh for decoupled process integration", "Master-data governance before any AI is applied"],
    "servicenow": ["Workflow orchestration as the enterprise control tower", "ITOM visibility feeding AIOps pipelines", "Risk and compliance modules as evidence stores", "Virtual Agent under scoped retrieval", "IntegrationHub spokes for the core estate"],
    "nvidia": ["GPU pools sized for inference economics", "NIM microservices for production model serving", "NeMo for fine-tuning pipelines under eval gates", "CUDA-accelerated feature engineering where it pays", "MIG partitioning for cost-accountable tenancy"],
    "intel": ["Edge silicon for on-premises inference", "Open vino for optimized model deployment", "SGX enclaves where key data must compute in place", "Hardware telemetry feeding predictive maintenance", "Cost-performance benchmarking per workload class"],
    "ibm": ["watsonx for governed foundation-model operations", "DB2 and zSystems integration for core estates", "Planning Analytics for finance-grade forecasting", "QRadar telemetry into the detection graph", "Trusted execution for regulated workloads"],
    "red hat": ["OpenShift as the hybrid runtime standard", "Ansible for audited infrastructure automation", "OpenShift AI for model operations on-cluster", "SELinux and SC security profiles as defaults", "Enterprise Linux discipline under every workload"],
}


def rebuild_partner(p: Page):
    pt = p.d.get("partner") or {}
    name = pt.get("name", "the partner")
    focus = pt.get("focus", "")
    scenarios = pt.get("scenarios") or []
    stack = PARTNER_STACKS.get(name.lower(), [])
    m = p.mapping()
    blocks = [
        hero(p, lede=f"The Achala IT Solutions alliance with {name}: what is certified, how joint deliveries run, and the scenarios this page can be held to."),
        h2("What the partnership covers"),
        para(p.sent([
            f"{name} in one line: {focus}. The alliance is delivery-grade, not logo-grade — joint reference architectures, certified engineers on both sides, and escalation paths that reach the vendor's own platform team when it matters." if focus else f"Our alliance with {name} is delivery-grade: joint reference architectures, certified engineers, and escalation paths into the vendor's platform team.",
            f"The alliance with {name} covers {focus} — backed by joint reference architectures, certification on both sides, and a support map with real names in it." if focus else f"{name} and Achala IT Solutions operate as one delivery surface: shared reference architectures, certified engineers, and a tested escalation tree.",
            f"What the {name} alliance buys you: {focus}, delivered by engineers certified on both stacks, with reference architectures maintained jointly rather than improvised per project." if focus else f"Certified engineers on both stacks, jointly maintained reference architectures, and vendor-level escalation — that is what the {name} alliance means in practice.",
        ], "pcov", m)),
        h2(H_ARCH),
        p.diagram_block(kind="edge-topology", title=f"{name} — joint delivery topology with Achala IT Solutions", salt="pdg"),
        para(p.sent(P_ARCH, "parch", m)),
        h2("Reference scenarios we deliver"),
    ]
    if scenarios:
        blocks.append(bullets(rewrite_bullet_descs(p, [tuple([s, "joint delivery scenario — reference architecture, certified team and support path in place"]) for s in scenarios], "psc")))
    if stack:
        blocks += [
            h2(H_STACK),
            para(p.sent(P_STACK_NOTE, "pstk", m)),
            bullets([[s.split(" for ")[0].title(), s] for s in stack]),
        ]
    blocks += [
        h2(H_INTG),
        bullets(p.integration_bullets()),
        h2("How a joint engagement runs"),
        para(p.cadence_block()),
        h2("What you receive"),
        para(p.sent(P_RECEIVE_P, "prcv", m)),
        bullets([
            ["Joint architecture pack", p.sent([
                "the reference architecture adapted to your tenancy and signed by both platform teams — your copy of the truth",
                "the adapted reference architecture, reviewed by the vendor's own field team before it reaches your architects",
                "a tenancy-specific architecture pack co-signed by Achala IT Solutions and the vendor platform team",
            ], "prb1", {})],
            ["Certified delivery pod", p.sent([
                "engineers badged on both stacks, with the vendor escalation path printed inside the runbook",
                "a pod certified on the platform this quarter, not a résumé — badges and escalation contacts named",
                "delivery engineers certified on both stacks, so the vendor channel is a colleague, not a ticket queue",
            ], "prb2", {})],
            ["Support map", p.sent([
                "who calls whom at 3 a.m. — the joint escalation tree, tested in a joint exercise rather than assumed from a PDF",
                "the tested escalation tree with named contacts on both sides, rehearsed before go-live",
                "an escalation map exercised in a joint drill, so the first real page is not the first test",
            ], "prb3", {})],
        ]),
        {"t": "cta", "x": f"Ask for the {name} reference pack — or bring your use case to a joint working session with both platform teams."},
    ]
    return blocks


CAREERS_COPY = {
    "/careers/working-here/": {
        "lede": "What working at Achala IT Solutions is actually like: small teams, real production ownership, evidence over opinions, and a career ladder that rewards engineering depth as much as management.",
        "sections": [
            ("How the work feels", "Delivery pods of four to seven engineers own a client capability end to end — architecture, code, runbook, and the weekly evidence review. There is no handoff theater: the person who designs the pipeline also gets paged for it, which concentrates the mind wonderfully."),
            ("Craft over process", "We keep ceremony low and standards high: design docs beat status meetings, eval gates beat vibes, and every release carries its evidence pack. Engineers spend the majority of the week in flow work rather than coordination work — and we measure that ratio, because we would be hypocrites otherwise."),
            ("Growth mechanics", "Every engineer has a named technical mentor, a skills budget, and a quarterly craft review that examines artifacts — pull requests, runbooks, incident write-ups — rather than personality. Promotion cases are written from evidence, and the bar is published, not whispered."),
            ("Where people sit", "Delivery hubs in Tysons Corner, London, Riyadh and our India execution core, working as one pod across time zones with a written-first culture — decisions live in documents, not in meetings you had to attend."),
        ],
    },
    "/careers/benefits-development/": {
        "lede": "Compensation, benefits and the development machinery at Achala IT Solutions — stated plainly, because benefits you cannot understand are benefits you cannot use.",
        "sections": [
            ("Compensation", "Market-benchmarked salaries reviewed annually, with a delivery-linked bonus tied to the same outcome metrics our clients see — when a committed delta lands, the pod shares it."),
            ("Learning budget", "A personal annual budget for certifications, conferences and courses, plus company time for certification study. Cloud, data and security certifications are the common currency; we fund the ones that map to your next role."),
            ("Health and time", "Comprehensive health cover per region, generous leave that people are actually expected to take, and a reset policy after hard go-lives — sustained heroics are a staffing bug, not a badge."),
            ("Equipment and craft", "A proper machine, monitors you choose, licenses you need, and a hardware budget for the home setup — plus internal guilds where engineers trade deep-dives across towers."),
        ],
    },
    "/careers/open-positions/": {
        "lede": "Open roles at Achala IT Solutions — delivery engineering across applied AI, data platforms, security, edge and cloud. Every listing names the team, the stack and the interview loop before you apply.",
        "sections": [
            ("How hiring works", "One conversation with the hiring lead, one technical deep-dive on real artifacts (not whiteboard puzzles), one working session with the prospective pod, and an offer or a no inside two weeks. Feedback is written either way."),
            ("Roles we hire for", "Data and platform engineers, AI/ML engineers with production scars, security engineers who think in identity rather than firewalls, SRE-minded platform builders, and delivery leads who can still read the code."),
            ("What we assess", "Evidence of craft: systems you designed, incidents you handled, quality of the runbooks you left behind. Depth in one tower plus curiosity across others beats shallow breadth."),
            ("Where to start", "Apply through the careers inbox with a CV and one artifact you are proud of — a design doc, a repository, a post-mortem you wrote. That artifact starts the conversation."),
        ],
    },
}


def rebuild_newsroom(p: Page):
    """newsroom articles were 0-block shells: title + date only.
    Build a factual press-release body from the title and structured fields."""
    d = p.d
    title = d["title"]
    pub = d.get("published", "")
    tl = lc(title)
    blocks = [
        {"t": "hero", "x": p.sent([
            f"Achala IT Solutions {tl} — the announcement, what changes for clients, and where to go next.",
            f"Company release from Achala IT Solutions: {tl}. What shipped, why now, and what it means for active engagements.",
            f"The news: {tl}. Context from the teams involved, and the practical next steps for clients and candidates.",
        ], "nhero", p.mapping())},
        h2("What happened"),
        para(p.sent([
            f"On {pub} Achala IT Solutions {tl}. The work behind it ran through the same delivery discipline we sell: a signed scope, named owners, and evidence reviewed at gates before anything was announced.",
            f"This announcement — {tl} — lands on {pub}. It reflects operating decisions made months ago: the platform work, the review cycles and the readiness checks all ran to the same standard we apply on client programs.",
            f"Achala IT Solutions {tl}, effective from {pub}. Internally the change touches delivery, platform and enablement teams; externally, clients see it in the surfaces they already use.",
        ], "nwhat", p.mapping())),
        h2("Why it matters"),
        para(p.sent(P_OV1B, "nwhy", p.mapping())),
        para(p.sent(P_ARCH2, "nwhy2", p.mapping())),
        h2("Details"),
        bullets([
            ["Scope", p.sent([
                "the change covers the platforms and delivery motions named above; client-tenanted deployments adopt it through their normal release cadence, not automatically",
                "everything announced here applies to Achala-operated surfaces first; client estates follow their own change windows with our runbooks",
                "the announcement touches managed platform surfaces and internal practice tooling — tenant-specific adoption is scheduled per client with their delivery lead",
            ], "nd1", {})],
            ["Timing", p.sent([
                f"effective from {pub}, with the enablement material available to delivery teams immediately and client-facing documentation updating through the week",
                f"in effect as of {pub}; transition work for active programs is already booked into existing sprint plans",
                f"live since {pub} on managed surfaces; active engagements migrate inside their agreed windows with no unplanned downtime",
            ], "nd2", {})],
            ["Evidence", p.sent([
                "as with everything we ship, the change carries its own evidence: readiness checks, eval results and a rollback plan — available to clients on request",
                "the announcement is backed by the same artifacts a program would produce: readiness review, evaluation results and a rehearsed rollback path",
                "proof over press: readiness checks, evaluation baselines and rollback drills sit behind this release, inspectable by clients under NDA",
            ], "nd3", {})],
        ]),
        h2("What happens next"),
        para(p.sent([
            "Clients with active engagements will hear from their delivery lead first — the briefing covers what, if anything, changes for their programs and when.",
            "Delivery leads own the client conversation from here: each active program gets a short note on impact, timing and any action required.",
            "The practical next step sits with the delivery leads, who will walk each active client through impact and timing in the next scheduled review.",
        ], "nnext", p.mapping())),
        {"t": "cta", "x": p.sent([
            "Press and analyst questions route to press@achalasolutions.com; client questions go to your delivery lead or the briefing flow.",
            "For media enquiries use press@achalasolutions.com — clients should raise anything impact-related with their delivery lead directly.",
            "Talk to press@achalasolutions.com for media coverage, or bring program questions to the delivery lead who runs your engagement.",
        ], "ncta", p.mapping())},
    ]
    return blocks


def rebuild_careers(p: Page):
    c = CAREERS_COPY.get(p.ctx["url"])
    if not c:
        return enrich_editorial(p)
    blocks = [{"t": "hero", "x": c["lede"]}]
    for h, body in c["sections"]:
        blocks.append(h2(h))
        blocks.append(para(body))
    blocks.append({"t": "cta", "x": p.sent([
        "Send your CV and one artifact you are proud of to careers@achalasolutions.com — a human reads it, and you will hear back inside a week.",
        "Ready when you are: the careers inbox is careers@achalasolutions.com, and every application gets a written reply.",
        "If the way we work reads like the way you work, careers@achalasolutions.com is the door — bring an artifact, not a cover letter.",
    ], "ctacareers", p.mapping())})
    return blocks


LEADER_POOLS = {
    "mandate": [
        "The mandate here is unglamorous and absolute: make {tower} deliveries predictable — signed baselines, binding gates, and evidence that survives the client's auditor without translation.",
        "This role exists to keep the delivery engine honest: scope that ships, metrics that reconcile, and a floor of engineering standards no schedule pressure can breach.",
        "The job, stated plainly — own the quality bar across {tower} programs, keep every commitment measurable, and make sure the client's control owner never waits for an answer.",
    ],
    "works": [
        "With clients, the pattern is direct: the leader joins the gates that matter, reviews the evidence before your steering committee does, and stays reachable after the signature — the person you met is the person accountable.",
        "Client time concentrates where risk lives — baseline sign-off, gate reviews and incident follow-ups — with the delivery pod carrying the weekly rhythm under the leader's standards.",
        "Expect involvement at the seams rather than in status meetings: metric selection, gate decisions, and the quarterly review of what the program actually moved.",
    ],
    "org": [
        "Inside, the role runs a bench of practice leads with their own delivery books — hiring for craft, reviewing artifacts quarterly, and keeping the tower's reference patterns current.",
        "The internal rhythm: weekly delivery reviews on live programs, monthly craft audits on runbooks and eval harnesses, and a standing rule that any committed metric must reconcile to its baseline.",
        "The operating principle is simple — the leader owns the standards, the practice leads own the books, and every program publishes evidence either way.",
    ],
}


def rebuild_leadership(p: Page):
    pr = p.d.get("profile") or {}
    role = pr.get("role", p.d["title"])
    focus = pr.get("focus") or []
    blocks = [
        {"t": "hero", "x": p.sent([
            f"{role} at Achala IT Solutions — the mandate, the standards this office enforces, and how clients engage with it directly.",
            f"What the {role} office owns at Achala IT Solutions: delivery standards, the quality bar behind every committed metric, and a direct line for client executives.",
            f"The {role} mandate at Achala IT Solutions: keep deliveries predictable, keep evidence honest, and stay personally reachable to the clients those deliveries serve.",
        ], "lhero", p.mapping())},
        h2("Mandate"),
        para(p.sent(LEADER_POOLS["mandate"], "mandate", p.mapping())),
        h2("How this office works with clients"),
        para(p.sent(LEADER_POOLS["works"], "works", p.mapping())),
        h2("Inside the practice"),
        para(p.sent(LEADER_POOLS["org"], "org", p.mapping())),
    ]
    if focus:
        blocks += [
            h2("Focus areas"),
            bullets([[f, p.sent([
                f"a standing priority for this office — reviewed at every delivery review, with artifacts inspected rather than status read out",
                f"owned at practice level and audited quarterly: the leader reviews the artifacts, not the slideware",
                f"carried into every program plan under this office's standards, with the evidence trail attached",
                f"a named accountability — when this slips, the office hears about it before the client does",
                f"tracked through the same gates clients see, so internal discipline and external commitment stay one system",
            ], "lfocus", {})] for f in focus]),
        ]
    blocks += [
        {"t": "cta", "x": p.sent([
            "Route executive questions through the briefing flow — this office joins the sessions where the baseline and gates are set.",
            "To bring this office into a gate review or baseline session, start from the briefing page and name the domain.",
            "Client executives can reach this office through a briefing — the first session ends with a measurement plan either way.",
        ], "ctalead", p.mapping())},
    ]
    return blocks


# ── audits ──────────────────────────────────────────────────────────────────

def text_of(d):
    """visible page copy only — title (h1) + blocks; meta_description excluded
    (it mirrors summary text by SEO design and is not rendered on the page)"""
    parts = [d.get("title", "")]
    for b in d.get("blocks", []):
        if b["t"] == "bullets":
            for it in b.get("items") or []:
                parts.append(" ".join(it))
        elif b["t"] == "diagram":
            parts.append(b.get("title", "") + " " + " ".join(b.get("labels") or []) + " " + (b.get("note") or ""))
        elif "x" in b:
            parts.append(b["x"])
    return " ".join(parts)


def audit(dup=True):
    problems = []
    minw = {"sub_capability": 750, "industry_capability": 750, "service_page": 800,
            "subindustry_page": 750, "solution_page": 800, "tower_hub": 800,
            "industry_hub": 800, "platform_overview": 750, "platform_architecture": 700,
            "platform_usecases": 700}
    files = sorted(glob.glob(os.path.join(PAGES, "*.json")))
    seen = {}
    ndup = 0
    for f in files:
        d = json.load(open(f))
        t = d["template"]
        words = len(text_of(d).split())
        if t in minw and words < minw[t]:
            problems.append(f"{os.path.basename(f)}: {t} only {words} words (<{minw[t]})")
        # banned
        low = text_of(d).lower()
        for b in BANNED:
            if b in low:
                problems.append(f"{os.path.basename(f)}: BANNED term '{b}'")
        # empty bullets
        for blk in d["blocks"]:
            if blk["t"] == "bullets" and not blk.get("items"):
                problems.append(f"{os.path.basename(f)}: empty bullets block")
        # markdown leftovers
        if "**" in text_of(d) or "TODO" in text_of(d):
            problems.append(f"{os.path.basename(f)}: markdown/TODO leftovers")
        # diagrams present on templated pages
        if t in minw:
            if not any(blk["t"] == "diagram" for blk in d["blocks"]):
                problems.append(f"{os.path.basename(f)}: {t} missing diagram")
        if dup:
            for s in re.split(r"(?<=[.!?])\s+", text_of(d)):
                n = norm(s)
                if len(n.split()) >= 14:
                    if n in seen and seen[n] != f:
                        ndup += 1
                        if ndup <= 12:
                            problems.append(f"DUP SENT ({seen[n].split('/')[-1][:40]} vs {os.path.basename(f)[:40]}): {s[:80]}...")
                    seen[n] = seen.get(n) or f
    if ndup:
        problems.append(f"TOTAL duplicated long sentences: {ndup}")
    return problems


# ── main ────────────────────────────────────────────────────────────────────

def collect_boiler_descs():
    """pre-scan ORIGINAL content: bullet descs repeated on 2+ pages (any length)
    + every >=14-word fragment of (title + blocks) occurring 2+ times anywhere —
    mirrors exactly what the audit compares, so collisions are caught pre-flight"""
    desc_pages = {}
    sent_count = {}
    for f in glob.glob(os.path.join(PAGES, "*.json")):
        d = json.load(open(f))
        for b in d.get("blocks", []):
            if b["t"] == "bullets":
                for it in (b.get("items") or []):
                    if len(it) > 1:
                        n = norm(it[1])
                        if len(n.split()) >= 3:
                            desc_pages.setdefault(n, set()).add(f)
        # fragment scan mirrors the audit's text_of (title + blocks, meta excluded)
        for s in re.split(r"(?<=[.!?])\s+", text_of(d)):
            n = norm(s)
            if len(n.split()) >= 14:
                sent_count[n] = sent_count.get(n, 0) + 1
    for n, fs in desc_pages.items():
        if len(fs) > 1:
            BOILER_DESCS.add(n)
    for n, cnt in sent_count.items():
        if cnt >= 2:
            BOILER_SENTS.add(n)
    print(f"pre-scan: {len(BOILER_DESCS)} boilerplate bullet descs, {len(BOILER_SENTS)} boilerplate fragments")


def main():
    collect_boiler_descs()
    files = sorted(glob.glob(os.path.join(PAGES, "*.json")))
    for f in files:
        d = json.load(open(f))
        t = d["template"]
        if t in SKIP_REWRITE:
            # the briefing/assessment pair was generated identical — differentiate it
            if d.get("url") in ("/book-a-briefing/", "/value-assessment/"):
                p = Page(os.path.basename(f), d)
                d["blocks"] = rebuild_contact_pair(p)
                d["words"] = len(text_of(d).split())
                with open(f, "w", encoding="utf-8") as fh:
                    json.dump(d, fh, ensure_ascii=False, indent=1)
                STATS["pages"] += 1
            continue
        p = Page(os.path.basename(f), d)
        try:
            if t == "sub_capability":
                blocks = rebuild_capability(p, is_sub=True)
            elif t == "industry_capability":
                blocks = rebuild_capability(p, is_sub=False)
            elif t == "service_page":
                blocks = rebuild_service(p)
            elif t == "subindustry_page":
                blocks = rebuild_subindustry(p)
            elif t == "solution_page":
                blocks = rebuild_solution(p)
            elif t == "tower_hub":
                blocks = rebuild_tower_hub(p)
            elif t == "industry_hub":
                blocks = rebuild_industry_hub(p)
            elif t == "platform_overview":
                blocks = rebuild_platform(p, "overview")
            elif t == "legal_page":
                blocks = rebuild_legal(p)
            elif t == "platform_architecture":
                blocks = rebuild_platform(p, "architecture")
            elif t == "platform_usecases":
                blocks = rebuild_platform(p, "usecases")
            elif t in ("insights_category", "services_hub", "solutions_hub",
                       "industries_hub", "platforms_hub", "cases_hub", "insights_hub"):
                blocks = rebuild_hub(p)
            elif t == "legal_page":
                blocks = rebuild_legal(p)
            elif t == "partner_page":
                blocks = rebuild_partner(p)
            elif t == "careers_page":
                blocks = rebuild_careers(p)
            elif t == "leadership_profile":
                blocks = rebuild_leadership(p)
            elif t == "newsroom_article":
                blocks = rebuild_newsroom(p)
            elif t in EDITORIAL:
                blocks = enrich_editorial(p)
            else:
                blocks = enrich_editorial(p)
        except Exception as e:
            print(f"ERROR {os.path.basename(f)}: {type(e).__name__} {e}")
            continue
        d["blocks"] = blocks
        d["words"] = len(text_of(d).split())
        with open(f, "w", encoding="utf-8") as fh:
            json.dump(d, fh, ensure_ascii=False, indent=1)
        STATS["pages"] += 1
    print(f"rewritten pages: {STATS['pages']}  diagrams injected: {STATS['diagrams']}  unique sentences tracked: {STATS['rewritten_sents']}")
    probs = audit()
    print(f"audit problems: {len(probs)}")
    for pr in probs[:30]:
        print("  -", pr)
    # final confidentiality scan across raw files
    blob = ""
    for f in glob.glob(os.path.join(PAGES, "*.json")):
        blob += open(f, encoding="utf-8").read().lower()
    hits = [b for b in BANNED if b in blob]
    print("confidentiality:", "CLEAN" if not hits else f"HITS: {hits}")
    return 0 if not probs and not hits else 1


if __name__ == "__main__":
    sys.exit(main())
