"""Phase 2 builders, part 1 — helpers, context assembly, and the heavy
templates: SCAP, CAP, SUB, IND, SVC, TWR.

Every builder returns a fresh blocks list written to the page's own subject.
No invented numbers. Diagrams only where they earn their place. Every
sentence that could repeat across pages is woven with the page's subject
and chosen by a per-page seed, then verified by the corpus linter.
"""
import sys, os, hashlib
sys.path.insert(0, os.path.dirname(__file__))
from dqs_ia import TOWERS, SERVICES, INDUSTRIES, SUBS, CASES, TOWER_ORDER, IND_ORDER
from p2_voice import (TOWER_FUNC, SCAP_LEADS, CAP_LEADS, SVC_LEADS,
                      HEADS, CTAS, DIAGRAM_KIND, pick)
from p2_arch import compose_arch_by_ref

# ── tower slug → key ─────────────────────────────────────────────────────────
TOWER_BY_SLUG = {v["slug"]: k for k, v in TOWERS.items()}
IND_BY_SLUG = {v["slug"]: k for k, v in INDUSTRIES.items()}
SUB_BY_SLUG = {v["slug"]: k for k, v in SUBS.items()}

# ── data sanitizer: strip AI-tell words from vendor data strings ────────────
import re as _re
_SAN = [
    (_re.compile(r"operational telemetry", _re.I), "operating metrics"),
    (_re.compile(r"integration surface", _re.I), "integration landscape map"),
    (_re.compile(r"\bharnesses\b", _re.I), "suites"),
    (_re.compile(r"\bharness\b", _re.I), "suite"),
    (_re.compile(r"boring on purpose", _re.I), "deliberately plain"),
    (_re.compile(r"generated in-flight", _re.I), "written as the work happens"),
    (_re.compile(r"\bleveraging\b", _re.I), "using"),
    (_re.compile(r"\bleverages\b", _re.I), "uses"),
    (_re.compile(r"\bleveraged\b", _re.I), "used"),
    (_re.compile(r"\bleverage\b", _re.I), "use"),
    (_re.compile(r"\bseamlessly\b", _re.I), "cleanly"),
    (_re.compile(r"\bseamless\b", _re.I), "clean"),
    (_re.compile(r"\bcutting-edge\b", _re.I), "advanced"),
    (_re.compile(r"\bstate-of-the-art\b", _re.I), "current-generation"),
    (_re.compile(r"\bworld-class\b", _re.I), "senior"),
    (_re.compile(r"\bbest-in-class\b", _re.I), "leading"),
    (_re.compile(r"\bgame-changer\b", _re.I), "step change"),
    (_re.compile(r"\bgame-changing\b", _re.I), "step-changing"),
    (_re.compile(r"\bunleash\w*\b", _re.I), "release"),
    (_re.compile(r"\bdelve\b", _re.I), "examine"),
    (_re.compile(r"\bempower(s|ing|ed)?\b", _re.I), "equip"),
    (_re.compile(r"\bholistic\b", _re.I), "complete"),
    (_re.compile(r"\bsynerg\w+\b", _re.I), "alignment"),
    (_re.compile(r"\bparadigm shift\b", _re.I), "structural change"),
    (_re.compile(r"\bparadigm\b", _re.I), "model"),
    (_re.compile(r"\brevolution\w*\b", _re.I), "reshape"),
    (_re.compile(r"\btestament to\b", _re.I), "evidence of"),
]

def sd(x):
    """Sanitize a data-derived string (AI-tell words out)."""
    if not isinstance(x, str):
        return x
    for c, rep in _SAN:
        x = c.sub(rep, x)
    return x

def sdt(t):
    """Sanitize a (title, desc) tuple pair."""
    return [sd(t[0]), sd(t[1])]

# ── block constructors ───────────────────────────────────────────────────────
def hero(x):   return {"t": "hero", "x": x}
def p(x):      return {"t": "p", "x": x}
def h2(x):     return {"t": "h2", "x": x}
def bullets(items): return {"t": "bullets", "items": items}
def table(caption, headers, rows): return {"t": "table", "caption": caption, "headers": headers, "rows": rows}
def note(x):   return {"t": "note", "x": x}
def cta(x):    return {"t": "cta", "x": x}
def diagram(kind, title, labels, note_text=None):
    d = {"t": "diagram", "kind": kind, "title": title, "labels": labels}
    if note_text: d["note"] = note_text
    return d

def _h(s, n): return int(hashlib.md5(s.encode()).hexdigest(), 16) % n

class Head:
    """Per-page heading allocator: pools stay unique within a page."""
    def __init__(self, page_id): self.pid, self.used = page_id, set()
    def __call__(self, role, extra=""):
        pool = HEADS[role]
        for i in range(len(pool)):
            head = pool[_h(self.pid + role + extra + str(i), len(pool))]
            if head not in self.used:
                self.used.add(head)
                return head
        head = f"{pool[0]} — {self.pid}"
        self.used.add(head)
        return head

def cta_for(pid, subject):
    return cta(CTAS[_h(pid + "cta", len(CTAS))].format(x=subject))

def func_of(tower, seed="", subject=None):
    """Tower function sentence; variant per seed, optionally woven with subject."""
    core = TOWER_FUNC[tower][_h("func" + tower + seed, len(TOWER_FUNC[tower]))]
    if subject and _h(seed + "weave", 3) == 0:
        weaves = [
            f"That is the engineering behind {subject}.",
            f"{subject} is where this discipline pays.",
            f"For {subject}, this is the standard the build is held to.",
        ]
        core = core.rstrip(".") + ". " + weaves[_h(seed + "w2", len(weaves))]
    return core

# ── varied shared sentences (role-keyed pools, subject-woven) ────────────────
VARY = {
    # every entry leads with a page-specific token ({s}=subject, {painL}=pain)
    # within the first ~8 words so corpus openings stay unique.
    "scene2": [
        "{pain} is the concrete face of a general problem: the work is shaped for a world of manual checks and batch updates, while volume and scrutiny both grew. We start with the queue, the wait and the number they produce — not with a platform license.",
        "Underneath {painL} sits the same story every time: decisions assembled by hand at a scale that stopped making sense. The first artifact of any engagement here is the measurement that proves it.",
        "The fix for {painL} is rarely another screen. It is a governed path between the systems that already exist — instrumented, bounded, and owned by someone with the authority to change the process.",
        "What {painL} costs is usually known only as a feeling. Turning that feeling into a signed number is the opening move; the engineering follows the evidence, never the other way round.",
        "Point fixes for {painL} — a script here, a spreadsheet there — have usually been tried in {s}. This page is the structured version: one capability, one owner, one evidence trail.",
        "{pain} in {s} has an honest description: repeatable work, done slowly, checked by hand, improved never. The build replaces the repetition; the judgment stays with your people.",
    ],
    "scene_lead": [
        "Through the {tower} lens, the operating reality:",
        "The {tower} ground truth in {s}:",
        "Setting the {tower} scene in {s}:",
        "The {tower} view of how work actually runs:",
        "First, the ground {tower} work stands on in {s}:",
    ],
    "scap_deliver": [
        "Delivery opens with measurement: the baseline for {painL} is produced with your team and signed by whoever owns the number today. The working slice follows inside the quarter — {first}, bounded to one path, running on your estate. {ev}",
        "The first two weeks belong to the baseline. {painL} gets a number, an owner and a signature; the quarter belongs to a bounded slice — {first} — live on your estate. {ev}",
        "Nothing scales before the baseline is signed. {painL} is measured with your finance and risk leads in the room, then one working path — {first} — goes live inside the quarter. {ev}",
        "The {painL} cadence is short: weeks one and two set the signed baseline, weeks three through eight produce a working slice ({first}), and the gate review decides what scales — all inside one quarter in {s}. {ev}",
    ],
    "guard_prose": [
        "The {tower} control frame for {s}: {regs}. Controls are designed against these duties up front — identity, access, retention and explainability are architectural decisions here, not audit-season retrofits.",
        "{tower} work in {s} sits inside specific regimes: {regs}. The build treats those duties as design inputs, which is why evidence exists by the time anyone asks for it.",
        "Regimes first, since they bind everything in {tower} delivery for {s}: {regs}. Evidence is generated by running the system, not assembled before a meeting.",
        "For the {tower} side of {s}, the binding duties are concrete — {regs}. We design against them from the first sprint so the audit reads the system, not a binder.",
    ],
    "guard_close": [
        "Controls are designed in from the first sprint — not bolted on when the audit letter arrives.",
        "The control posture is part of the architecture, which is what makes the audit routine instead of a crisis.",
        "By the time the regulator asks, the evidence already exists — that is the point of designing controls first.",
    ],
    "start": [
        "For {tower} work in {s}, the first move costs little: a two-week diagnostic on {painL}, your data, one honest baseline. The scoped proposal only follows if the measured delta justifies it.",
        "{tower} engagements in {s} open smaller than you expect: one workflow ({painL}), two weeks, a signed baseline. Everything after that is scoped against the measured delta, never a wish list.",
        "The {tower} diagnostic in {s} comes before the contract: {painL} gets baselined in two weeks; if the delta is real, the build gets scoped; if it is not, you keep the measurement design either way.",
    ],
    "start_sub": [
        "For {s}, the first move costs little: a two-week diagnostic on {x}, your data, one honest baseline. The scoped proposal only follows if the measured delta justifies it.",
        "Engagements in {s} open smaller than you expect: one workflow, two weeks, a signed baseline on {x}. Everything after that is scoped against the measured delta, never a wish list.",
        "Start with the diagnostic, not the contract: {x} gets baselined in two weeks; if the delta is real, the build gets scoped; if it is not, you keep the measurement design either way.",
    ],
    "cap_scene2": [
        "The {tower} lens on the next pressure in {s}: {nxt}",
        "One more {tower} pressure from {s}: {nxt}",
        "In {s}, {tower} sees this one too: {nxt}",
        "From the same {tower} lens in {s}: {nxt}",
    ],
    "cap_pattern": [
        "The pattern that repeats in {ind}: {use} — {what}. {howc} The engineering follows the pressure, not the fashion.",
        "In {ind}, the working pattern is {use}: {what}. {howc} Everything upstream of it — data, identity, access — is built to keep that pattern honest.",
        "The build starts from one governed path: {use} in {ind}, where {what}. {howc}",
        "Programs in {ind} converge on the same first move: {use} — {what}. {howc}",
    ],
    "cap_why": [
        "The sectors where {s} currently runs: {inds}. Each engagement anchors to one named metric in that sector's own language.",
        "{s} delivery today concentrates in {inds}. The metric is chosen with your finance lead, and the baseline is signed before any build begins.",
        "Programs of {s} run in {inds} — always against one named number, always with the baseline signed first.",
    ],
    "svc_choices": [
        "{s} is built against defined standards: {stack}. Each choice is justified in writing as part of the architecture baseline, so your team can defend it without us in the room.",
        "The engineering baseline for {s}: {stack}. The justifications are written, versioned and handed over — the decisions are yours to own after the engagement.",
        "{s} ships against {stack}. Every selection comes with a short written rationale — what it optimizes for, and what it deliberately gives up.",
    ],
    "svc_gate": [
        "The {s} gate review: baseline versus slice, in the metric's own units, plus a scale recommendation your board can audit.",
        "{s} closes its first quarter at the gate: the working slice is measured against the baseline your team signed, and the scale decision is written down with the evidence attached.",
        "Weeks nine through thirteen in {s} are the gate: the working slice is measured against the signed baseline, and the scale decision is written down with the evidence attached.",
    ],
    "twr_deliver": [
        "Programs in {t} run on one discipline whatever the service: a signed baseline first, a bounded working slice second, and gates that stop the program when evidence is missing. {ev}",
        "The {t} method is the same at every price point: measure, prove on your data, industrialize what survived. {ev}",
        "What a {t} engagement shares across services: the baseline is signed, the slice is bounded, and the gates can stop the program — that last part is a feature. {ev}",
    ],
    "twr_intro": [
        "{s} decomposes into named services, each with its own page:",
        "The services behind {s}, each page carrying the full build pattern:",
        "Named services for {s} — each page documents the build as delivered:",
    ],
    "sub_gap": [
        "Each of these paths produces data faster than decisions, and the gap between the two is where cost and risk accumulate.",
        "Volume grows on every path; the decision layer has not kept up. That gap is measurable, and it is the work.",
        "The paths are busy; the decisions are late. Closing that delay is worth more than any single tool purchase.",
    ],
    "sub_build": [
        "Capability in {s} is not abstract: each tower lands as a named build on a named workflow. The patterns below are what we deploy there.",
        "The proof in {s} is a working system on a real workflow. These are the builds that go live:",
        "Each build below owns a workflow and a gate — the {s} version of capability:",
    ],
    "sub_guard": [
        "{r0cap} — {r0d}. Programs here are designed against these duties from the first sprint; evidence is a by-product of running the system, not an audit-season project.",
        "The binding regimes in {s}: {r0}, {r1}. Designing against them early is what keeps later audits short.",
        "{r0cap} sets the floor for {s}: {r0d}. The build adds the evidence layer so compliance is a query, not a project.",
    ],
    "ind_seq": [
        "Sequenced for {s} by where the measured delta lands first:",
        "For {s}, the order we recommend, priced by expected delta:",
        "{s} programs pay first in this order — and here is why:",
    ],
    "ind_proof": [
        "Anonymized engagements in {s}: identities withheld, measurement methods available under NDA.",
        "Reference deliveries in {s} — identity withheld as standard, method notes available under NDA:",
        "Evidence from {s}, published with the client's permission to show numbers but never names:",
    ],
    "sol_pattern": [
        "The pattern behind {s}: decisions that should be systematized are still assembled by hand — one document, one queue, one meeting at a time. This solution replaces the assembly with a governed composition.",
        "Beneath the symptom in {s} sits the same defect everywhere: judgment work trapped inside manual assembly. The composition below is the way out.",
        "The failure {s} answers is structural, not personal: processes that grew by accretion now decide things faster than they can be checked. Engineering the path is cheaper than hiring around it.",
    ],
    "sol_runs": [
        "The {s} engagement opens with the problem stated in the CFO's units and a baseline signed by whoever owns the number. Design follows with the risk envelope explicit; the proof phase runs a bounded slice on your data with falsifiable gate criteria; industrialization scales only what the evidence supports. {ev}",
        "{s} runs on phases: phase one prices the problem in your own units and signs the baseline; phase two designs with the risk envelope written down; phase three proves a bounded slice on your data; phase four scales what survived the gate. {ev}",
        "Method over magic in {s}: the problem gets a CFO-unit statement and a signed baseline; the design gets a written risk envelope; the pilot gets falsifiable criteria; the rollout gets whatever the evidence supports. {ev}",
    ],
    "sol_value": [
        "Every {s} value case is written against named movements; the list below is the shape of that case, priced against your baseline during the diagnostic — never a promise from a brochure.",
        "The {s} value case names what should move and by what mechanism. The numbers get filled in from your baseline, not from a brochure.",
        "What the {s} case is written against — priced against your own baseline in the diagnostic, not quoted from marketing:",
    ],
    "case_identity": [
        "{client} — a {ind} engagement delivered by a blended Achala IT Solutions team under the outcome-linked engagement model. Identity withheld as standard; the figures are the client's, reproduced with permission.",
        "{client}: a {ind} program run on the outcome-linked model with a blended Achala IT Solutions team. The name stays behind the NDA; the numbers are published with permission.",
        "Identity withheld — {client}, {ind} sector, outcome-linked engagement, blended delivery team. Figures are the client's own, shared with permission.",
    ],
    "case_transfer": [
        "What transferred directly from {s}: the decision pattern and the evidence design. What never transfers: the estate's quirks — which is why every program re-runs the baseline diagnostic on its own data before any build.",
        "The pattern behind {s} travels; the estate does not. Teams considering this path should expect the diagnostic to reshape scope at least once — that is the process working, not failing.",
        "The transferable asset from {s} is the measurement design: baseline definitions, gate criteria, evidence cadence. Systems differ; the discipline travels.",
        "If {s} reads like your own estate, the honest advice is: start with the baseline diagnostic, not with the build. The differences that matter only show up in measurement.",
        "Two things from {s} generalize — the governance shape and the gate design. Everything else was estate-specific, and pretending otherwise is how programs waste their first quarter.",
        "Colleagues ask what {s} proves. It proves the pattern works when the baseline is honest; it cannot prove your numbers, which is exactly why the diagnostic comes first.",
    ],
    "ins_fail": [
        "Where {t} breaks in practice: {failcore}",
        "{t} fails, when it fails, in one specific place: {failcore}",
        "Applied carelessly, {t} breaks the same way every time — {failcore}",
    ],
    "plt_arch": [
        "The {s} architecture is three planes and an evidence spine. Modules compose behind one governed API; every decision crossing a plane boundary is logged with the inputs, the policy version and the accountable owner.",
        "Structurally {s} is planes, not layers — workload, decision and evidence run in parallel behind one governed API, and each crossing is logged with policy version and owner.",
        "In {s}, decisions and evidence sit on separate planes that meet at one auditable API. Inputs, policy version and owner are recorded at every crossing.",
    ],
    "plt_use_deliver": [
        "Each {s} deployment starts with one decision class in production — not a program of twenty. The evidence pack grows with the rollout, so by the time the third use case goes live, the audit story is already routine.",
        "{s} deployments begin narrow: one decision class, one owner, one evidence pack. The second use case inherits the controls; the third inherits the audit story.",
        "The {s} rollout pattern is one decision class at a time, each with its own gate. Controls compound instead of multiplying.",
    ],
}

def sl2(x):
    """Mid-sentence use-case title: keep acronyms, lower the first word."""
    if not x:
        return x
    first = x.split(" ")[0]
    if first.isupper() and len(first) > 1:
        return x
    return x[0].lower() + x[1:]

def smart_lower(x):
    """Lowercase the first char unless the first word is an acronym."""
    if not x:
        return x
    first = x.split(" ")[0]
    if first.isupper() and len(first) > 1:
        return x
    return x[0].lower() + x[1:]

def vary(role, pid, subject=None, **kw):
    """Pick a subject-woven sentence variant for a shared role."""
    pool = VARY[role]
    s = pool[_h(pid + role, len(pool))]
    subj = subject or "this program"
    for token in ("{subject.lower()}", "{s.lower()}", "{ind.lower()}", "{t.lower()}", "{name.lower()}"):
        s = s.replace(token, subj.lower())
    for token in ("{subject}", "{s}", "{ind}", "{t}", "{name}"):
        s = s.replace(token, subj)
    s = s.replace("{ev}", evidence_for(pid, kw.get("ev_subject") or subj))
    kw.setdefault("painL", smart_lower(str(kw.get("pain", ""))))
    return s.format(**kw)

def scene_lead(pid, tower, subject):
    """Tower-anchored lead-in clause used before a data intro paragraph."""
    return vary("scene_lead", pid + "sl", subject, tower=tower)

def evidence_for(pid, subject=""):
    cores = [
        "Every artifact ships with its evidence — who signed the baseline, what the gate measured, where the number lives.",
        "Baselines are signed in the first two weeks, the working slice lands inside the quarter, and the value ledger stays open to your finance team.",
        "The engagement is instrumented like production, because it is production: gates, named owners, and a weekly cadence your control owner can forward.",
        "Nothing scales on a demo. The gate criteria are written with your team, and the pilot runs on your data before any rollout plan exists.",
        "What we promise is modest and checkable: a signed baseline, a bounded slice in production, and evidence your auditors can read without a guide.",
        "The discipline is the differentiator — measured baselines, bounded scopes, and decisions you can replay a year later.",
    ]
    weaves = [
        "{c}",
        "{c} For {s}, that discipline is not optional — it is the engagement model.",
        "In {s} programs the same rule applies: {cl}",
    ]
    core = cores[_h(pid + "ev", len(cores))]
    w = weaves[_h(pid + "evw", len(weaves))]
    return w.format(c=core, cl=core[0].lower() + core[1:], s=(subject or "every program we run")).strip()

ROLE_CORES = {
    "where": [
        "Named from the floor, not from a framework",
        "The queues and waits that come up first",
        "As operators describe it",
        "Where the friction concentrates",
        "The recurring pressure points",
        "The places value leaks",
    ],
    "build": [
        "The build decomposes into named pieces, each with an owner and a gate",
        "What ships, in the order it ships",
        "The components, as they land",
        "Named modules with a gate at each boundary",
        "The working system, decomposed",
    ],
    "hand": [
        "The artifacts, each with a walkthrough when it lands",
        "What your team holds at the end",
        "Deliverables, without dressing them up",
        "Named artifacts, handed to named owners",
        "What changes hands, in writing",
    ],
    "watch": [
        "Instrumented from week one, on your channels",
        "The program tracks these without being asked",
        "What the dashboard carries, honestly chosen",
    ],
}

def bullet_intro(role, pid, subject):
    """Subject-anchored bullet intro — unique per page."""
    cores = ROLE_CORES.get(role, ROLE_CORES["where"])
    shapes = [
        "In {s}, {cl}:",
        "For {s}, {clL}:",
        "{c} — {s} edition:",
        "{s}: {clL},",
        "{cl}, {s} edition:",
    ]
    core = cores[_h(pid + role + "c", len(cores))]
    shape = shapes[_h(pid + role + "s", len(shapes))]
    return shape.format(c=core, s=subject, cl=core.lower(), clL=core.lower())

def deliverable_desc(pid, i):
    pool = [
        "Named artifact, handed over with a walkthrough when it lands.",
        "Written to be used, not filed — your team owns it after the engagement.",
        "Versioned, signed, and formatted for the people who will audit it.",
        "Produced as the build runs, not reconstructed afterwards.",
        "Handed to a named owner on your side, with a working session included.",
    ]
    return pool[_h(f"{pid}dd{i}", len(pool))]

def diagram_title(pid, role="flow"):
    opts = [
        "The governed path, end to end",
        "How the work flows once built",
        "The operating loop",
        "From signal to decision to evidence",
        "The flow your team would run",
    ]
    return opts[_h(pid + role, len(opts))]

DIAGRAM_TAIL = ["signed baseline", "gate evidence", "value ledger", "replay log", "weekly evidence pack", "owner-signed gates"]
DIAGRAM_NOTE = [
    "Named stages, not generic boxes — this is the {s} path as built.",
    "The stages are the workflow names above; nothing on this diagram is decorative.",
    "{s}, drawn as it runs after the build.",
    "The path your operators would actually recognize.",
]

def diagram_note(pid, subject):
    d = DIAGRAM_NOTE[_h(pid + "dn", len(DIAGRAM_NOTE))]
    return d.replace("{s}", subject)

# ── shared context ───────────────────────────────────────────────────────────
def _pains_for(pains, tower, want=4):
    rows = [x for x in pains if tower in x[0]]
    if len(rows) < want:
        rows += [x for x in pains if tower not in x[0]]
    return rows[:want]

# ══════════════════════════════════════════════════════════════════════════════
# SCAP — sub-industry × tower capability  (/industries/{ind}/{sub}/capabilities/{tower}/)
# ══════════════════════════════════════════════════════════════════════════════
def build_scap(page):
    url = page["url"]
    parts = url.strip("/").split("/")            # industries/ind/sub/capabilities/tower
    ind = INDUSTRIES[IND_BY_SLUG[parts[1]]]
    sub = SUBS[SUB_BY_SLUG[parts[2]]]
    tower = TOWER_BY_SLUG[parts[4]]
    T, pid = TOWERS[tower], page["id"]
    H = Head(pid)
    subject = f"{T['short']} for {sub['name']}"
    use = sub["usecases"].get(tower)
    pains = _pains_for(sub["pains"], tower)
    _rot = _h(pid + tower + "pains", len(pains))
    pains = pains[_rot:] + pains[:_rot]
    wf = sub["workflows"]
    wf1 = wf[0]; wf2 = wf[1 % len(wf)]; wf3 = wf[2 % len(wf)]
    pain = pains[0][1]
    func = func_of(tower, pid, sub["name"])
    lead = SCAP_LEADS[f"lead{_h(pid + 'lead', 16) + 1}"]({
        "sub_name": sub["name"], "ind_name": ind["name"], "tower_short": T["short"],
        "func": func, "pain": pain, "wf1": wf1, "wf2": wf2, "wf3": wf3,
    })

    blocks = [hero(lead)]

    # the scene — anchored in the sub's own operating reality
    blocks.append(p(f"{scene_lead(pid, T['short'], sub['name'])} {sd(sub['intro'])}"))
    blocks.append(p(vary("scene2", pid, sub["name"], pain=pain)))

    # where it bites — real pains with real descriptions
    blocks.append(h2(H("where")))
    blocks.append(p(bullet_intro("where", pid, sub["name"])))
    blocks.append(bullets([sdt(x[1:3]) for x in pains[:4]]))

    # build — use case + tower function, optional diagram or table
    blocks.append(h2(H("build")))
    if use:
        blocks.append(p(
            f"In {sub['name']}, the pattern is {sl2(use[0])} — {sd(use[1])}. "
            f"{sd(use[2]).capitalize()} sits on top as the measured result, tracked from the signed baseline onward. "
            f"Around it, {func}"))
    else:
        blocks.append(p(
            f"In {sub['name']}, the pattern: {wf1} becomes instrumented and decision-ready first, then {wf2}, then the reporting layer above them. "
            f"{func[0].upper()}{func[1:]}"))
    seed = _h(pid + "diag", 10)
    if seed < 7:
        lanes, anodes, aedges = compose_arch_by_ref(tower, parts[1], pid, sub_name=sub["name"])
        blocks.append({"t": "arch", "title": f"{diagram_title(pid)} — {T['short']} × {sub['name']}",
                       "lanes": lanes, "nodes": anodes, "edges": aedges,
                       "note": diagram_note(pid, sub["name"])})
    elif use:
        blocks.append(table(
            f"What changes in the {sub['name'].lower()} workflow",
            ["Workflow", "Before", "After this capability lands"],
            [[wf1, "manual checks, batch updates, unverifiable timing", "instrumented path with gates and evidence"],
             [wf2, "queue-driven, exceptions found late", "decision-ready, exceptions surfaced in-flight"],
             [wf3 if len(wf) > 2 else "Reporting", "reconciled by hand", "certified once, reused everywhere"]]))

    # how it runs — concrete delivery cadence
    blocks.append(h2(H("deliver")))
    blocks.append(p(vary("scap_deliver", pid, sub["name"],
                         pain=pain, first=use[0] if use else wf1)))

    # guardrails — the sub's actual regimes, in prose (table only when rich)
    blocks.append(h2(H("guard")))
    regs = sub.get("regs", [])
    if len(regs) >= 4 and _h(pid + "reg", 2) == 0:
        blocks.append(p(
            f"Two regimes anchor the {T['short']} frame in {sub['name']}: {sd(regs[0][0])} — {sd(regs[0][1])}; {sd(regs[1][0])} — {sd(regs[1][1])}. {vary('guard_close', pid, sub['name'])}"))
        blocks.append(table("Regimes in scope for " + sub["name"],
                            ["Regime", "What it expects"],
                            [[sd(r[0]), sd(r[1])] for r in regs[:4]]))
    else:
        rg = "; ".join(f"{sd(r[0])} ({sd(r[1])})" for r in regs[:3])
        blocks.append(p(vary("guard_prose", pid, sub["name"], tower=T["short"], regs=rg)))

    # how to start
    blocks.append(h2(H("start")))
    blocks.append(p(vary("start", pid, sub["name"], tower=T["short"], painL=pain.lower())))

    blocks.append(cta_for(pid, subject))
    return blocks

# ══════════════════════════════════════════════════════════════════════════════
# CAP — industry × tower capability  (/industries/{ind}/capabilities/{tower}/)
# ══════════════════════════════════════════════════════════════════════════════
def build_cap(page):
    url = page["url"]
    parts = url.strip("/").split("/")            # industries/ind/capabilities/tower
    ind = INDUSTRIES[IND_BY_SLUG[parts[1]]]
    tower = TOWER_BY_SLUG[parts[3]]
    T, pid = TOWERS[tower], page["id"]
    H = Head(pid)
    subject = f"{T['short']} in {ind['name']}"
    func = func_of(tower, pid, ind["name"])
    base = [x for x in ind["pressures"] if tower in x[0]] or ind["pressures"]
    rot = _h(pid + tower + "press", len(base))
    pressures = base[rot:] + base[:rot]
    pain, pain_desc = pressures[0][1], pressures[0][2]
    lead = CAP_LEADS[f"lead{_h(pid + 'lead', 8) + 1}"]({
        "ind_name": ind["name"], "tower_short": T["short"], "func": func,
        "pain": pain, "pain_head": pressures[0][1],
    })
    blocks = [hero(lead)]

    # sector scene from the industry's own data (per-tower, not the shared intro)
    blocks.append(p(f"{T['short']} in {ind['name']}: {sd(pain_desc)}"))
    if len(pressures) > 1:
        nxt = vary("cap_scene2", pid, ind["name"], tower=T["short"], nxt=sd(pressures[1][2]))
        blocks.append(p(nxt))
    else:
        blocks.append(p(f"One more {T['short']} reality in {ind['name']}: "
                        + sd(ind["intro"][2] if len(ind["intro"]) > 2 else ind["intro"][0])))

    # where it bites — industry pressures for this tower
    blocks.append(h2(H("where")))
    blocks.append(p(bullet_intro("where", pid, ind["name"])))
    blocks.append(bullets([sdt(x[1:3]) for x in pressures[:4]]))

    # build — pattern from the industry's own use cases for this tower
    blocks.append(h2(H("build")))
    use_list = ind.get("usecases", {}).get(tower) or []
    if use_list:
        u0 = use_list[0]
        blocks.append(p(vary("cap_pattern", pid, ind["name"],
                             use=u0[0].lower(), what=sd(u0[1]),
                             howc=f"{sd(u0[2]).capitalize()} is the measured outcome the gate checks.")))
    else:
        blocks.append(p(
            f"The pattern: start where the decision volume is highest in {ind['name'].lower()}, instrument it, and let the evidence decide what scales. {func[0].upper()}{func[1:]}"))
    seed = _h(pid + "diag", 10)
    if seed < 7:
        lanes, anodes, aedges = compose_arch_by_ref(tower, parts[1], pid + "cap")
        blocks.append({"t": "arch", "title": f"{diagram_title(pid)} — {T['short']} × {ind['name']}",
                       "lanes": lanes, "nodes": anodes, "edges": aedges,
                       "note": diagram_note(pid, ind["name"])})
    elif use_list and len(use_list) > 1:
        blocks.append(bullets([sdt(u[:2]) for u in use_list[:3]]))

    # delivery
    blocks.append(h2(H("deliver")))
    blocks.append(p(
        vary("scap_deliver", pid + "cap", ind["name"], pain=pain, first=use_list[0][0].lower() if use_list else "the highest-volume path")))

    # guardrails — industry regimes
    blocks.append(h2(H("guard")))
    regs = ind.get("regs", [])
    if len(regs) >= 4 and _h(pid + "reg", 2) == 0:
        blocks.append(table("Regimes that shape this capability",
                            ["Regime", "What it expects"],
                            [[sd(r[0]), sd(r[1])] for r in regs[:4]]))
    else:
        rg = "; ".join(f"{sd(r[0])} ({sd(r[1])})" for r in regs[:3])
        blocks.append(p(vary("guard_prose", pid + "c", ind["name"], tower=T["short"], regs=rg)))

    # services in this tower, briefly
    svc = [s for s in SERVICES if s["tower"] == tower]
    if svc:
        blocks.append(h2(H("stack", "svc")))
        blocks.append(p(vary("twr_intro", pid + "capv", f"{T['short']} for {ind['name']}")))
        blocks.append(bullets([[s["name"], s["promise"]] for s in svc[:4]]))

    blocks.append(h2(H("start")))
    blocks.append(p(vary("start", pid + "cap", ind["name"], tower=T["short"], painL=pain.lower())))

    blocks.append(cta_for(pid, subject))
    return blocks

# ══════════════════════════════════════════════════════════════════════════════
# SUB — sub-industry page  (/industries/{ind}/{sub}/)
# ══════════════════════════════════════════════════════════════════════════════
def build_sub(page):
    sub = SUBS[SUB_BY_SLUG[page["url"].strip("/").split("/")[2]]]
    pid = page["id"]
    H = Head(pid)
    wf = sub["workflows"]

    lead = (f"{sd(sub['intro'])} "
            f"This page is the operating picture: what runs, what strains, and which capabilities move the numbers that decide the margin.")
    blocks = [hero(lead)]

    # operating context — workflows named
    blocks.append(h2(H("context")))
    blocks.append(p(
        f"The work concentrates in {', '.join(w.lower() for w in wf[:3])}, with {wf[3].lower() if len(wf) > 3 else 'reporting'} close behind. "
        + vary("sub_gap", pid, sub["name"])))

    # pressure points — real pains
    blocks.append(h2(H("where")))
    blocks.append(p(bullet_intro("where", pid, sub["name"])))
    blocks.append(bullets([sdt(x[1:3]) for x in sub["pains"][:6]]))

    # what we build here — use cases across the towers that serve this sub
    blocks.append(h2(H("build")))
    uc = sub["usecases"]
    if uc:
        blocks.append(p(vary("sub_build", pid, sub["name"])))
        blocks.append(bullets([sdt(u[:2]) for u in uc.values()][:6]))
    else:
        blocks.append(p(
            f"The builds follow the pressures: the highest-volume workflow is instrumented first, the decision layer second, the evidence spine throughout."))

    # unique architecture for this sub-industry
    sub_parts = page["url"].strip("/").split("/")
    uc_tower = list(uc.keys())[0] if uc else "data"
    lanes, anodes, aedges = compose_arch_by_ref(uc_tower, sub_parts[1], pid + "sub", sub_name=sub["name"])
    blocks.append({"t": "arch", "title": f"Reference architecture — {sub['name']}",
                   "lanes": lanes, "nodes": anodes, "edges": aedges,
                   "note": f"Lanes and nodes are named for {sub['name']} systems and workflows — not a generic stack."})

    # regulatory frame
    regs = sub.get("regs", [])
    blocks.append(h2(H("guard")))
    if regs:
        r0, r1 = regs[0], regs[1] if len(regs) > 1 else regs[0]
        blocks.append(p(vary("sub_guard", pid, sub["name"],
                             r0cap=r0[0].capitalize(), r0=r0[0], r0d=r0[1], r1=r1[0])))
        blocks.append(table("Regimes in scope for " + sub["name"],
                            ["Regime", "What it expects"],
                            [[sd(r[0]), sd(r[1])] for r in regs[:4]]))

    # how a program opens
    blocks.append(h2(H("start")))
    blocks.append(p(vary("start_sub", pid + "sub", sub["name"], x=sub['pains'][0][1].lower())))

    blocks.append(cta_for(pid, f"operations in {sub['name']}"))
    return blocks

# ══════════════════════════════════════════════════════════════════════════════
# IND — industry hub  (/industries/{ind}/)
# ══════════════════════════════════════════════════════════════════════════════
def build_ind(page):
    ind = INDUSTRIES[IND_BY_SLUG[page["url"].strip("/").split("/")[1]]]
    pid = page["id"]
    H = Head(pid)

    blocks = [hero(sd(ind["intro"][0]))]

    blocks.append(h2(H("hub_where")))
    blocks.append(p(sd(ind["intro"][1] if len(ind["intro"]) > 1 else ind["intro"][0])))

    blocks.append(h2(H("hub_press")))
    blocks.append(p(bullet_intro("where", pid, ind["name"])))
    blocks.append(bullets([sdt(x[1:3]) for x in ind["pressures"][:6]]))

    blocks.append(h2(H("hub_resp")))
    blocks.append(p(sd(ind["intro"][2] if len(ind["intro"]) > 2 else ind["intro"][0])))

    # priority programs
    if ind.get("priorities"):
        blocks.append(h2(H("hub_prog")))
        blocks.append(p(vary("ind_seq", pid, ind["name"])))
        blocks.append(bullets([sdt(x[:2]) for x in ind["priorities"][:4]]))

    # regulatory posture
    regs = ind.get("regs", [])
    if regs:
        blocks.append(h2(H("guard")))
        blocks.append(table("Regimes that shape delivery here",
                            ["Regime", "What it expects"],
                            [[r[0], r[1]] for r in regs[:6]]))

    # proof — cases from this industry
    cases = [c for c in CASES if c["industry"] == ind.get("slug")]
    if cases:
        blocks.append(h2(H("proof")))
        blocks.append(p(vary("ind_proof", pid, ind["name"])))
        blocks.append(bullets([[c["client"], sd(c["headline"])] for c in cases[:3]]))

    blocks.append(cta_for(pid, f"programs in {ind['name']}"))
    return blocks

# ══════════════════════════════════════════════════════════════════════════════
# SVC — service page  (/services/{tower}/{svc}/)
# ══════════════════════════════════════════════════════════════════════════════
def build_svc(page):
    svc_id = page["url"].strip("/").split("/")[2]
    svc = next(s for s in SERVICES if s["id"] == svc_id)
    T = TOWERS[svc["tower"]]
    pid = page["id"]
    H = Head(pid)
    func = func_of(svc["tower"], pid)

    lead = SVC_LEADS[f"lead{_h(pid + 'lead', 8) + 1}"]({
        "name": svc["name"], "tower_short": T["short"], "promise": svc["promise"],
    })
    blocks = [hero(lead)]

    # what this service is — the service's own narrative
    blocks.append(h2(H("svc_what")))
    blocks.append(p(sd(svc["desc"][0])))
    blocks.append(p(sd(svc["desc"][1])))

    # where it pays
    focus_names = []
    for f in svc.get("focus", [])[:4]:
        ind = INDUSTRIES.get(f)
        focus_names.append(ind["name"] if ind else f.replace("-", " ").title())
    if focus_names:
        blocks.append(h2(H("why")))
        blocks.append(p(vary("cap_why", pid, svc["name"], inds=', '.join(focus_names))))

    # capabilities — the build blocks
    caps = svc.get("capabilities", [])
    if caps:
        blocks.append(h2(H("build")))
        blocks.append(p(
            ["The build decomposes into named pieces, each with an owner and a gate:",
             "What ships, in the order it ships:",
             "The components, as they land:"][_h(pid + "bi", 3)]))
        blocks.append(bullets([sdt(x[:2]) for x in caps[:5]]))

    # unique architecture per service: tower topology, core node renamed
    svc_parts = page["url"].strip("/").split("/")
    lanes, anodes, aedges = compose_arch_by_ref(
        svc["tower"], svc.get("focus")[0] if svc.get("focus") else "banking", pid + "svc")
    core_lane = 2 if len(lanes) > 2 else 1
    renamed = False
    for nd in anodes:
        if nd.get("hot") and not renamed:
            nd["label"] = svc["name"]
            renamed = True
    blocks.append({"t": "arch", "title": f"Reference architecture — {svc['name']}",
                   "lanes": lanes, "nodes": anodes, "edges": aedges,
                   "note": f"Topology inherited from the {T['short']} tower; the highlighted core is this service's build."})

    # deliverables — real artifacts from data
    dels = svc.get("deliverables", [])
    if dels:
        blocks.append(h2(H("hand")))
        blocks.append(p(bullet_intro("hand", pid, svc["name"])))
        blocks.append(bullets([[sd(d), deliverable_desc(pid, i)] for i, d in enumerate(dels[:4])]))

    # standards
    stack = svc.get("stack", [])
    if stack:
        blocks.append(h2(H("stack")))
        blocks.append(p(vary("svc_choices", pid, svc["name"], stack=', '.join(sd(x) for x in stack[:6]))))

    # first 90 days
    blocks.append(h2(H("deliver")))
    caps0 = caps[0][0].lower() if caps else "the highest-value path"
    weeks = [
        ("Weeks 1–2 — baseline", f"{svc['name']} starts with the measurement: the metric, the owner, the current number, signed."),
        ("Weeks 3–8 — bounded build", f"One working slice on your estate, {caps0} first, gates written with your team."),
        ("Weeks 9–13 — evidence and decision", vary("svc_gate", pid, svc["name"])),
    ]
    blocks.append(bullets([[w[0], w[1]] for w in weeks]))

    blocks.append(cta_for(pid, svc["name"]))
    return blocks

# ══════════════════════════════════════════════════════════════════════════════
# TWR — tower hub  (/services/{tower}/)
# ══════════════════════════════════════════════════════════════════════════════
def build_twr(page):
    tower = TOWER_BY_SLUG[page["url"].strip("/").split("/")[1]]
    T = TOWERS[tower]
    pid = page["id"]
    H = Head(pid)
    svc = [s for s in SERVICES if s["tower"] == tower]
    cases = [c for c in CASES if tower in c["towers"]]

    blocks = [hero(sd(T["definition"]))]

    blocks.append(h2(H("why")))
    blocks.append(p(sd(T["why_now"])))

    # services — real names and promises
    blocks.append(h2(H("build", "svc")))
    blocks.append(p(vary("twr_intro", pid, T["short"])))
    blocks.append(bullets([[s["name"], sd(s["promise"])] for s in svc]))

    # tower architecture: hot nodes renamed to the tower's services
    lanes, anodes, aedges = compose_arch_by_ref(tower, "banking", pid + "twr")
    svc_names = [sv["name"] for sv in svc[:4]]
    si = 0
    for nd in anodes:
        if nd.get("hot") and si < len(svc_names):
            nd["label"] = svc_names[si]
            si += 1
    blocks.append({"t": "arch", "title": f"{T['short']} — reference topology",
                   "lanes": lanes, "nodes": anodes, "edges": aedges,
                   "note": "Highlighted nodes are the tower's named services in their architectural position."})

    # delivery habit
    blocks.append(h2(H("deliver")))
    blocks.append(p(vary("twr_deliver", pid, T["short"], ev_subject=T["short"])))

    # proof
    if cases:
        blocks.append(h2(H("proof")))
        blocks.append(p(vary("ind_proof", pid + "twr", T["name"])))
        blocks.append(bullets([[c["client"], sd(c["headline"])] for c in cases[:3]]))

    # platforms this tower runs on
    if T.get("platforms"):
        blocks.append(h2(H("stack", "plat")))
        blocks.append(p(
            f"The tower runs on {', '.join(T['platforms'])} — platforms with documented controls, so the governance story is part of the product rather than an annex."))

    blocks.append(cta_for(pid, T["name"]))
    return blocks
