#!/usr/bin/env python3
"""Achala content rewrite pass 1:
   - kill AI-flavor phrases (leverage/harness/landscape...)
   - rewrite 96 templated 'applied to' + 78 'as delivered' heroes
   - deduplicate the 10 most-repeated paragraphs (variant pools)
   - vary the top CTA messages
   All deterministic (md5-seeded). JSON formatting preserved (indent=1, no trailing NL)."""
import json, glob, re, hashlib, os, sys

ROOT = '/home/z/my-project/site/src/content/pages'

def h(s: str, n: int) -> int:
    return int(hashlib.md5(s.encode()).hexdigest(), 16) % n

# ── 1. banned-phrase replacements ─────────────────────────────────────────
BANNED = [
    (r'\bleverages\b', ['uses', 'draws on', 'applies']),
    (r'\bleveraging\b', ['using', 'drawing on', 'applying']),
    (r'\bleveraged\b', ['used', 'drew on', 'applied']),
    (r'\bleverage\b', ['use', 'draw on', 'apply']),
    (r'\bharnessing\b', ['applying', 'putting to work', 'using']),
    (r'\bharnesses\b', ['applies', 'puts to work']),
    (r'\bharness\b', ['apply', 'put to work', 'use']),
    (r'\bdelve into\b', ['examine']),
    (r'\bdelve\b', ['look']),
    (r'\bunleash\w*\b', ['release']),
    (r'\bgame-?changer\b', ['step change']),
    (r'\bseamlessly\b', ['cleanly']),
    (r'\bseamless\b', ['clean']),
    (r'\bcutting-edge\b', ['advanced']),
    (r'\bstate-?of-?the-?art\b', ['current-generation']),
    (r'\bworld-?class\b', ['senior']),
    (r'\bbest-?in-?class\b', ['leading']),
    (r'\brevolution\w*\b', ['reshape']),
    (r'\bparadigm shift\b', ['operating shift']),
    (r'\bsynergies\b', ['overlaps']),
    (r'\bsynergy\b', ['overlap']),
    (r'\bholistic\b', ['end-to-end']),
    (r'\btransformative\b', ['material']),
    (r'\bempowering\b', ['equipping']),
    (r'\bempowers\b', ['equips']),
    (r'\bempower\b', ['equip']),
]

def fix_banned(text: str, seed: str) -> str:
    for pat, opts in BANNED:
        def rep(m):
            return opts[h(seed + m.group(0), len(opts))]
        text = re.sub(pat, rep, text, flags=re.I)
    return text

def walk_strings(node, seed, fn):
    """apply fn to every string; returns count of changed strings"""
    n = 0
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(v, str):
                nv = fn(v, seed + k)
                if nv != v:
                    node[k] = nv
                    n += 1
            elif isinstance(v, (dict, list)):
                n += walk_strings(v, seed + k, fn)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            if isinstance(v, str):
                nv = fn(v, seed + str(i))
                if nv != v:
                    node[i] = nv
                    n += 1
            elif isinstance(v, (dict, list)):
                n += walk_strings(v, seed + str(i), fn)
    return n

# ── 2. hero rewrites ──────────────────────────────────────────────────────
HERO_A = [
    "{S}, shipped on a signed baseline: the scope we take, the weekly delivery rhythm, the platform rails underneath, and the delta we commit to at every gate.",
    "How Achala IT Solutions delivers {S} — bounded scope, a fixed weekly cadence, the platforms it runs on, and outcomes written into the contract.",
    "{S} in production: what gets built, who owns each control, how the pilot widens into an industrial deployment, and the metrics that gate each phase.",
    "The working definition of {S} at Achala IT Solutions: scope we sign, the cadence you can plan around, platform evidence generated in-flight, and outcomes measured against your baseline.",
    "{S} without the theater — a measured baseline first, a gated pilot on your data, then industrialization with runbooks your team can run.",
    "What {S} looks like when it has to survive an audit: scoped deliverables, weekly evidence, named control owners and a committed delta per gate.",
    "{S}, delivered by a named pod: the scope, the rhythm, the rails, and the numbers we are willing to be measured on.",
    "A practical build of {S}: two weeks to a signed baseline, six to a working pilot, twelve to an industrialized deployment with the delta reported against week zero.",
]
HERO_B = [
    "{T} inside {I}: the operating realities we design for, the delivery pattern we run, the services and platforms involved, and the outcomes we commit to.",
    "How {T} lands in {I} — the constraints that shape the build, the gated delivery pattern, and the deltas we commit against your baseline.",
    "{T} for {I}: what the sector's controls demand, what we build on the platform rails, and the outcomes written into the engagement.",
    "Applying {T} to {I}: the context that decides the design, the weekly cadence, the towers involved, and committed outcomes per gate.",
    "{T} in the {I} context — regulation-first design, a fixed delivery rhythm, and outcomes your board can audit.",
    "What {T} changes for {I}: the processes we target, the controls we inherit, the platforms underneath, and the measured delta at every gate.",
    "{T}, tuned for {I}: sector-specific design decisions, the delivery pattern with named owners, and outcomes gated on signed metrics.",
    "A working build of {T} for {I}: the operating context that shapes it, the services sequenced through the method, and the deltas we commit to.",
]
RE_HERO_A = re.compile(r'^(.*?) as delivered by Achala IT Solutions: scope, delivery pattern, the platforms involved and the outcomes we commit to at each gate\.$')
RE_HERO_B = re.compile(r'^(.*?) applied to (.*?)\. This page sets out the operating context, the delivery pattern we run, the services and platforms involved, and the outcomes we commit to\.$')

# ── 3. paragraph dedup variant pools ──────────────────────────────────────
CADENCE_BODY = "Weeks 1–2 lock the baseline: the current metric is measured with your team and signed before build starts. Weeks 3–8 deliver the pilot on bounded scope — one decision path, one workflow, one plant or one portfolio — with a control owner named on your side. Weeks 9–12 industrialize what worked: runbooks, monitoring, enablement and a measured delta against the signed baseline. Anything that misses its gate is stopped or redirected with a documented decision, not quietly extended."
CADENCE_LEADS = {
    "The engagement cadence below is the standard pattern for this capability. ": [
        "The cadence below is the standard pattern for this capability, and it does not flex by account. ",
        "Below is the delivery cadence for this capability — the same pattern on every engagement. ",
        "This capability runs on the cadence set out below; the rhythm is fixed, the scope is signed. ",
    ],
    "Delivery follows the same weekly rhythm on every program of this type. ": [
        "Every program of this type runs the same weekly rhythm, so your team can plan around it. ",
        "The weekly rhythm below is identical across programs of this type. ",
        "Delivery runs on one weekly rhythm for every program of this type. ",
    ],
    "Programs run on a fixed rhythm so progress is visible from week one. ": [
        "The rhythm is fixed on purpose: progress becomes visible from week one, not after the first steering meeting. ",
        "Programs run on the fixed rhythm below, chosen so progress is legible from week one. ",
        "A fixed rhythm keeps progress visible from week one — here is the one we run. ",
    ],
}
CADENCE_VARIANTS = [
    None,  # keep original body (assigned when h() lands on it)
    "Weeks 1–2 lock the baseline with your team: the current metric is measured, signed and stored as the reference for every later gate. Weeks 3–8 run the pilot on deliberately narrow scope — one decision path, one workflow, one plant or one portfolio — with a control owner named on your side. Weeks 9–12 industrialize what worked: runbooks, monitoring, enablement and a measured delta against the signed baseline. Anything that misses its gate is stopped or redirected with a documented decision, never quietly extended.",
    "Weeks 1–2 are measurement only: we lock the current metric with your team and both sides sign it before a line of build starts. Weeks 3–8 deliver a bounded pilot — one decision path, one workflow, one plant or one portfolio — with a named control owner on your side. Weeks 9–12 turn what worked into runbooks, monitoring and enablement, then report the measured delta against the baseline. A missed gate means a documented stop-or-redirect decision, not a quiet extension.",
    "The first two weeks lock the baseline: your team and ours measure the current metric together and sign it. Weeks 3–8 carry the pilot on bounded scope — a single decision path, workflow, plant or portfolio — and a control owner on your side owns the evidence. Weeks 9–12 industrialize: runbooks, monitoring, enablement, and a measured delta against the signed baseline. Missing a gate produces a documented decision to stop or redirect — never a silent extension.",
    "Weeks 1–2 measure and sign the baseline with your team; nothing builds against an unsigned number. Weeks 3–8 prove the pattern on deliberately bounded scope — one decision path, one workflow, one plant or one portfolio — under a control owner named on your side. Weeks 9–12 industrialize what worked into runbooks, monitoring and enablement, closing with a measured delta against the baseline. Every gate is pass, stop or redirect, in writing.",
    "The first quarter of the rhythm is verification: weeks 1–2 measure the current metric with your team and lock it by signature. Weeks 3–8 deliver the pilot on bounded scope — one decision path, one workflow, one plant or one portfolio — with your control owner receiving evidence weekly. Weeks 9–12 industrialize: runbooks, monitoring, enablement and the measured delta against the signed baseline. Gates are binding: miss one and the program stops or redirects with a documented decision.",
    "Weeks 1–2 belong to measurement: the baseline metric is captured with your team and signed before build starts. Weeks 3–8 run a bounded pilot — one decision path, one workflow, one plant or one portfolio — steered by a control owner on your side. Weeks 9–12 convert the pilot into runbooks, monitoring and enablement, and close with a measured delta against the signed baseline. Anything that misses a gate is stopped or redirected on the record.",
]
CADENCE_INTRO = "The first quarter closes with the following artifacts handed over and walkthrough with your team:"
CADENCE_INTRO_VARIANTS = [
    "By the end of the first quarter, these artifacts are handed over and walked through with your team:",
    "The quarter closes with a handover walkthrough of the following artifacts:",
    "At the end of the first quarter your team receives these artifacts, each walked through line by line:",
    "These artifacts change hands at the end of the first quarter, with a live walkthrough for your team:",
    "The first quarter ends with an artifact handover — the list below, walked through with your team:",
    "Your team gets the following artifacts at quarter close, each with a guided walkthrough:",
]
P_TAIL_VARIANTS = {
    "A typical program here starts with a two-week diagnostic that measures the workflows named above and locks the baseline, moves through a gated proof on your data, then industrializes on platform rails with the sector's compliance evidence generated in-flight.": [
        "A typical program opens with a two-week diagnostic that measures the workflows named above and locks the baseline, then runs a gated proof on your data before industrializing on platform rails — with the sector's compliance evidence produced in-flight, not reconstructed afterwards.",
        "Programs here begin with a two-week diagnostic: the workflows named above get measured, the baseline gets locked. A gated proof on your data follows, then industrialization on platform rails with compliance evidence generated as the work runs.",
        "The standard program shape: a two-week diagnostic locks the baseline for the workflows above, a gated proof on your data demonstrates the delta, and platform rails carry industrialization while the sector's compliance evidence is generated in-flight.",
        "Start with a two-week diagnostic that measures the workflows above and locks the baseline. Then a gated proof on your data. Then industrialization on platform rails — compliance evidence for the sector generated in-flight along the way.",
    ],
    "Engagements begin with the baseline measurement pack — cycle times, error rates, unit costs for the workflows above — because every committed outcome on this page is reported against that locked baseline, audited annually.": [
        "Every engagement opens with the baseline measurement pack — cycle times, error rates and unit costs for the workflows above. Every committed outcome on this page is reported against that locked baseline, and the baseline is audited annually.",
        "We start with the baseline measurement pack: cycle times, error rates, unit costs across the workflows above. It matters because each committed outcome here is reported against that locked baseline — audited annually.",
        "The first artifact is always the baseline measurement pack — cycle times, error rates and unit costs for the workflows named above. Outcomes committed on this page are only meaningful against it, which is why it is audited annually.",
    ],
    "The engagement was structured for transfer: named pod, documented runbooks, operator enablement, and a Compound phase that keeps challenger programs and conformance monitoring running after handover.": [
        "Transfer was designed in from day one: a named pod, documented runbooks, operator enablement, and a Compound phase that keeps challenger programs and conformance monitoring alive after handover.",
        "The engagement was built to be handed over: named pod, runbooks in writing, operators enabled, and a Compound phase running challenger programs and conformance monitoring after the exit.",
        "Structure followed the transfer principle — named pod, documented runbooks, enabled operators, and a Compound phase that kept challenger programs plus conformance monitoring running post-handover.",
    ],
    "The program ran through the Achala Method: a Value Mapping Sprint locked the baseline, a gated PoC produced the capital-grade evidence, and production hardening (replay, SLOs, control tests) was generated by the delivery itself rather than reconstructed for audit.": [
        "The program followed the Achala Method: a Value Mapping Sprint locked the baseline, a gated PoC produced capital-grade evidence, and production hardening — replay, SLOs, control tests — fell out of the delivery itself instead of being reconstructed for audit.",
        "Delivery ran on the Achala Method: the Value Mapping Sprint locked the baseline, the gated PoC generated capital-grade evidence, and production hardening (replay, SLOs, control tests) emerged from the work itself rather than a post-hoc audit rebuild.",
        "The Achala Method shaped the program: baseline locked in a Value Mapping Sprint, capital-grade evidence from a gated PoC, and production hardening — replay, SLOs, control tests — generated by delivery, not reconstructed for auditors.",
    ],
    "We staff a named pod for this sub-industry pattern: delivery lead, quality owner and control owner, with the follow-the-sun rhythm covering build, run and the conformance monitoring that keeps the design honest after handover.": [
        "This sub-industry pattern gets a named pod: delivery lead, quality owner, control owner — running a follow-the-sun rhythm that covers build, run, and the conformance monitoring that keeps the design honest after handover.",
        "Staffing follows the sub-industry pattern: a named pod with a delivery lead, quality owner and control owner, working follow-the-sun across build, run and post-handover conformance monitoring.",
        "A named pod carries this sub-industry pattern — delivery lead, quality owner, control owner — on a follow-the-sun rhythm spanning build, run and the conformance monitoring that keeps the design honest once we hand over.",
    ],
}
RE_COMPOSES = re.compile(r'^The delivery pattern composes (\d+) services from the (.*?) tower — (.*?) as the usual core — sequenced through the Achala Method with sector controls: (.*?) obligations shape the design from the first sprint\.$')
COMPOSES_VARIANTS = [
    "Delivery composes {N} services from the {T} tower — {CORE} as the usual core — sequenced through the Achala Method, with {CTRL} obligations shaping the design from the first sprint.",
    "The pattern pulls {N} services from the {T} tower ({CORE} form the usual core) and sequences them through the Achala Method; {CTRL} obligations shape the design from sprint one.",
    "{N} services from the {T} tower make up the delivery pattern — {CORE} as the usual core — run through the Achala Method with {CTRL} obligations baked into the design from the first sprint.",
    "Under the hood the pattern composes {N} {T} services — {CORE} as the usual core — sequenced by the Achala Method, with {CTRL} obligations shaping design decisions from the first sprint onward.",
]

# ── 4. CTA variants ───────────────────────────────────────────────────────
CTA_VARIANTS = {
    "Book a briefing with the practice lead for this sub-industry, or return to the industry hub.": [
        "Bring this pattern to a 45-minute briefing with the sub-industry practice lead — or head back to the industry hub.",
        "Book a briefing with this sub-industry's practice lead, or explore the rest of the industry hub.",
        "A 45-minute briefing with the practice lead maps this pattern to your estate; the industry hub has the full picture.",
        "Talk to the sub-industry practice lead in a working briefing — or keep browsing the industry hub.",
        "Map this to your estate: book the practice lead for a briefing, or return to the industry hub.",
    ],
    "Explore the services behind this capability, or book a briefing with the industry practice lead.": [
        "Open the services behind this capability, or book a briefing with the industry practice lead.",
        "The services underneath this capability are one click away — or book time with the industry practice lead.",
        "Read the services that carry this capability, or bring your context to a briefing with the practice lead.",
        "Go deeper into the services behind this capability — or put your metric in front of the industry practice lead.",
    ],
    "Discuss this service with the practice lead — or request a scoped value assessment for your estate.": [
        "Take this service to the practice lead in a working session — or ask for a scoped value assessment of your estate.",
        "Talk through this service with the practice lead, or request a value assessment scoped to your estate.",
        "Put this service in front of the practice lead — or have a value assessment scoped against your baseline.",
    ],
    "Start with a capability page — or book a briefing with the industry practice lead.": [
        "Begin with a capability page, or book a briefing with the industry practice lead.",
        "Pick a capability to go deeper — or take your metric straight to the industry practice lead.",
        "The capability pages break this down further; the industry practice lead can map it to your estate in a briefing.",
    ],
    "Ask for a reference conversation on this pattern — or map it to your estate in a briefing.": [
        "Request a reference conversation on this pattern — or map it to your estate in a working briefing.",
        "A reference conversation on this pattern can be arranged; a briefing maps it to your estate first.",
    ],
    "Read the related service pages — or bring this pattern to your estate in a briefing.": [
        "The related service pages go deeper — or bring this pattern to your estate in a briefing.",
        "Continue through the related services, or put this pattern in front of your estate in a briefing.",
    ],
}

def pick(seed: str, pool) -> str:
    return pool[h(seed, len(pool))]

# ── main pass ─────────────────────────────────────────────────────────────
stats = {"files": 0, "heroes_a": 0, "heroes_b": 0, "cadence": 0, "cadence_intro": 0,
         "tail": 0, "composes": 0, "cta": 0, "banned": 0}

for f in sorted(glob.glob(os.path.join(ROOT, '*.json'))):
    pid = os.path.basename(f)[:-5]
    d = json.load(open(f, encoding='utf-8'))
    changed = False
    for b in d.get('blocks', []):
        t = b.get('t')
        x = b.get('x')
        if not isinstance(x, str):
            continue
        if t == 'hero':
            m = RE_HERO_A.match(x)
            if m:
                b['x'] = pick(pid + 'heroA', HERO_A).replace('{S}', m.group(1))
                stats['heroes_a'] += 1
                changed = True
                continue
            m = RE_HERO_B.match(x)
            if m:
                b['x'] = pick(pid + 'heroB', HERO_B).replace('{T}', m.group(1)).replace('{I}', m.group(2))
                stats['heroes_b'] += 1
                changed = True
                continue
        elif t == 'p':
            if x == CADENCE_INTRO:
                b['x'] = pick(pid + 'ci' + str(stats['cadence_intro']), CADENCE_INTRO_VARIANTS)
                stats['cadence_intro'] += 1
                changed = True
                continue
            matched_lead = None
            for lead, leads in CADENCE_LEADS.items():
                if x.startswith(lead) and x[len(lead):] == CADENCE_BODY:
                    matched_lead = lead
                    break
            if matched_lead:
                lead_v = pick(pid + 'cl', CADENCE_LEADS[matched_lead])
                body_v = pick(pid + 'cb', CADENCE_VARIANTS) or CADENCE_BODY
                b['x'] = lead_v + body_v
                stats['cadence'] += 1
                changed = True
                continue
            if x in P_TAIL_VARIANTS:
                b['x'] = pick(pid + 'pt', P_TAIL_VARIANTS[x])
                stats['tail'] += 1
                changed = True
                continue
            m = RE_COMPOSES.match(x)
            if m:
                b['x'] = pick(pid + 'cp', COMPOSES_VARIANTS).format(
                    N=m.group(1), T=m.group(2), CORE=m.group(3), CTRL=m.group(4))
                stats['composes'] += 1
                changed = True
                continue
        elif t == 'cta':
            if x in CTA_VARIANTS:
                b['x'] = pick(pid + 'cta', CTA_VARIANTS[x])
                stats['cta'] += 1
                changed = True
                continue
    # banned-phrase pass over every string field
    nb = walk_strings(d, pid, fix_banned)
    if nb:
        stats['banned'] += nb
        changed = True
    if changed:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(json.dumps(d, ensure_ascii=False, indent=1))
        stats['files'] += 1

print(stats)
