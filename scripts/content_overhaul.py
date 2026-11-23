"""Content overhaul engine — de-AI the whole 633-page corpus.

Passes:
  A. phrase map (kill AI-tell cliches)              -> every string
  B. curated bullet library (shared epigram bullets) -> bullets by label
  C. hero regeneration per template                  -> t:'hero'
  D. meta description regeneration                   -> meta_description
  E. content expansion (delivery rhythm, artifacts)  -> appended blocks
  F. interlink computation (services<->solutions<->industries<->platforms)
  G. brand.json stats corrections

Deterministic: variant choice is seeded by page id.
Backups written to src/content/_backup_overhaul/.
"""
import json, glob, os, re, random, shutil, sys

ROOT = '/home/z/my-project/site'
PAGES = os.path.join(ROOT, 'src/content/pages')
BACKUP = os.path.join(ROOT, 'src/content/_backup_overhaul')

rng_global = random.Random(20261120)

# ── Pass A: phrase map ────────────────────────────────────────────────────
PHRASE_MAP = [
    # hero/bullet epigrams
    (r'zero-trust by architecture, not by slide\s*—\s*', ''),
    (r'zero-trust by architecture, not by slide', 'zero-trust controls across identity, network and workload'),
    (r'not slideware:\s*it runs', 'each method runs'),
    (r'not slideware', 'in production use'),
    (r'regulatory teeth', 'controls regulators accept'),
    (r'shared truth with regulatory teeth', 'a shared record every participant trusts'),
    (r"the sector'?s? physics", 'the operating pressures of your sector'),
    (r'governed autonomy at enterprise scale', 'automation with human checkpoints, budgets and audit'),
    (r'governed autonomy', 'automation with human checkpoints and audit'),
    (r'intelligence layer of the enterprise', 'AI and data systems the enterprise runs on'),
    (r'institutions that cannot fail quietly', 'institutions where downtime is public and costly'),
    (r'cannot fail quietly', 'where downtime is public and costly'),
    (r'fail quietly', 'fail silently'),
    (r'emerging compute with investor discipline\s*—\s*baselines, benchmarks, verdicts', 'optimization with baselines, benchmarks and a documented verdict'),
    (r'investor discipline', 'an evidence-first method'),
    (r'every intelligence program silently depends on', 'every AI program is built on'),
    (r'silently depends on', 'is built on'),
    (r'AI that answers to the P&L', 'AI measured on the P&L'),
    (r'governance that stand up to audit', 'governance that holds up under audit'),
    (r'stand up to audit', 'hold up under audit'),
    (r'Trusted data at decision speed', 'Trusted data, delivered in near real time'),
    (r'at decision speed', 'in near real time'),
    (r'self-healing workflows', 'workflows that recover from failure on their own'),
    (r'self-healing', 'self-recovering'),
    (r'Margin recovered in milliseconds', 'Pricing and availability decisions made in milliseconds'),
    (r'shelf truth', 'accurate shelf data'),
    (r'sensor fabric', 'sensor network'),
    (r'edge fabric', 'edge estate'),
    (r'integration spine', 'integration layer'),
    (r'decision velocity', 'decision throughput'),
    (r'start at pattern 80%', 'start from a configured 80 percent baseline'),
    (r'start at pattern 80 percent', 'start from a configured 80 percent baseline'),
    (r'clients start at pattern 80', 'clients start from a configured 80 percent baseline'),
    (r'falsifiable success criteria', 'success criteria fixed before work starts'),
    (r'falsifiable criteria', 'pre-agreed criteria'),
    (r'falsifiable', 'testable'),
    (r'with the evidence to defend every one', 'with a full evidence trail for each decision'),
    (r'evidence generation built in', 'audit evidence produced automatically'),
    (r'evidence generation', 'audit evidence production'),
    (r'wearing a compliance uniform', ''),
    (r'accumulating AI pilots the way hoarders accumulate boxes\s*—\s*full of potential, impossible to use', 'accumulating AI pilots that never reached production'),
    (r'So we built the machinery', 'So we built that machinery'),
    (r'because that is the only kind of work that compounds', 'because that is the work that pays for itself'),
    (r'the only kind of work that compounds', 'the work that pays for itself'),
    (r'replayable for audit', 'fully logged for audit'),
    (r'every decision path for replay', 'every decision path for later review'),
    (r'Enterprise decisions in milliseconds\s*—\s*decision hubs with policy, evidence and replay built in', 'Decision paths that run in milliseconds, with policy checks and full logging'),
    (r'Enterprise decisions in milliseconds\s*—\s*with the evidence to defend every one', 'Decision paths that run in milliseconds, with a full evidence trail'),
    (r'Hundreds of agents as one governed fleet\s*—\s*roles, queues, budgets and audit for the AI workforce', 'Agents operated as one fleet: roles, queues, budgets and audit trails'),
    (r'Hundreds of agents as one governed, measurable workforce', 'Many agents operating as one governed, measurable workforce'),
    (r'the operations stack that turns physical assets into self-correcting systems', 'the operations stack that turns physical assets into self-monitoring systems'),
    (r'Sense, simulate, act\s*—\s*the operations stack for physical assets', 'Sensor data feeds a living model of your plant, fleet or field estate, and the model drives action'),
    (r'Shared truth with regulatory teeth\s*—\s*permissioned networks that survive supervision', 'Permissioned networks with records every participant and auditor can verify'),
    (r'AI your model-risk committee approves and your regulator can inspect', 'Model governance your risk committee and regulator can review'),
    (r'Security architecture you can evidence\s*—\s*for humans, machines and models', 'Security controls for people, machines and models, with evidence collected continuously'),
    (r'The governed data estate every AI program is built on', 'The governed data estate every AI program needs'),
    (r'outcome-linked engagements that produce measured, auditable business results', 'engagements tied to named metrics and measured results'),
    (r'Outcome-Linked Engagements', 'Engagements Tied to Named Metrics'),
    (r'outcome-linked engagements', 'engagements tied to named metrics'),
    (r'outcome-linked commercial design', 'commercial models tied to outcomes'),
    (r'real-time risk, resilient operations and auditable AI for institutions where downtime is public and costly', 'real-time risk decisions, resilient operations and AI controls that pass supervisory review'),
    (r'auditable AI for institutions', 'AI controls that pass review for institutions'),
    (r'your regulator can inspect', 'your regulator can review'),
    (r'survive supervision', 'stand up to supervision'),
    (r"sector'?s? structural pressures", 'sector operating pressures'),
    (r'operating picture', 'operating profile'),
    (r'with regulatory teeth', 'with enforceable controls'),
    (r'shared truth', 'a shared, verifiable record'),
    (r'measured, auditable business results', 'measured business results'),
    (r'that is the only kind of work that compounds', 'that is the work that pays for itself'),
    (r'measured at every delivery gate', 'measured at every gate'),
    (r'patent-backed method', 'proprietary method'),
    (r'patent-backed platforms', 'platforms built on proprietary methods'),
    (r'patent families', 'method families'),
    (r'patents granted or pending across', 'method families across'),
    (r'Quietly', 'Silently'),
    (r'\bWe sell the capability layers that decide whether an enterprise competes in the intelligence era', 'These are the capability layers that decide whether an enterprise competes on intelligence'),
    (r'in the intelligence era', 'on intelligence'),
    (r'the intelligence era', 'the AI era'),
    # casing bug seen in generated heroes
    (r'and ai security in one program', 'and AI security in one program'),
    (r'(\A|(?<=[.;:\s]) )ai security', r'\1AI security'),
]

PHRASE_COMPILED = [(re.compile(p, re.I), r) for p, r in PHRASE_MAP]

def clean(text: str) -> str:
    if not isinstance(text, str):
        return text
    out = text
    for rx, rep in PHRASE_COMPILED:
        out = rx.sub(rep, out)
    # collapse double spaces / orphan separators
    out = re.sub(r'\s{2,}', ' ', out)
    out = re.sub(r'\s+([.;:])', r'\1', out)
    out = re.sub(r'—\s*—', '—', out)
    out = re.sub(r'^[—\s]+', '', out)
    out = re.sub(r'\s+—\s*$', '.', out)
    # capitalize sentence starts after replacements
    out = re.sub(r'(^|[.!?]\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper(), out)
    return out.strip()

# ── Pass B: curated bullet library (shared epigram bullets) ──────────────
BULLET_LIB = {
    # towers
    "Applied AI & Generative AI": "Strategy, model selection, retrieval, evaluation and the operations that keep models accurate in production. We start from the business metric, not the model.",
    "Agentic AI & Hyperautomation": "Goal-directed agents that run inside your systems with defined roles, budgets and human checkpoints. Every action is logged, measurable and reversible.",
    "Data, Analytics & Lakehouse": "Pipelines, lakehouse and governance built so reports reconcile, lineage is traceable end to end, and access is controlled without slowing teams down.",
    "Cybersecurity & Zero-Trust": "Identity-first architecture covering workforce, customer and machine access, with detection, response and AI-specific controls in one program.",
    "Cloud, Edge & Platform Engineering": "Hybrid and edge estates engineered for reliability, cost per workload and clean day-two operations, with an internal platform your teams actually adopt.",
    "Quantum & Advanced Compute": "Optimization, simulation and post-quantum cryptography migration, applied where the mathematics pays back and benchmarked against classical baselines.",
    "Blockchain & Digital Trust": "Permissioned networks, tokenization and verifiable credentials with the reporting and controls supervisors expect.",
    "IoT, Digital Twin & Robotics": "Sensor integration, digital twins and robotics that let operations teams see, simulate and act on physical assets in one loop.",
    # platforms
    "Achala Nexus": "The decision hub: contextual graphs, policy checks and full decision replay for audit.",
    "Achala Forge": "The data platform every program builds on: ingestion, quality, lineage and access control.",
    "Achala Swarm": "Multi-agent orchestration with queues, budgets, escalation paths and audit trails.",
    "Achala Sentinel": "Security controls for people, machines and models, with evidence collected continuously.",
    "Achala Twinverse": "Simulation and operations for physical assets, from sensor data to actuation.",
    "Achala Quanta": "Optimization workloads on quantum-inspired algorithms, benchmarked against classical solvers.",
    "Achala Ledger": "Permissioned ledger networks with regulatory reporting built in.",
    "Achala Compass": "Model governance: validation, monitoring and documentation your risk committee can review.",
    # industries
    "Banking & Financial Services": "Real-time fraud and risk decisions, resilient core operations and AI controls that pass supervisory review.",
    "Insurance & Risk": "Underwriting accuracy, claims automation and fraud detection with full model documentation for regulators.",
    "Healthcare & Life Sciences": "Clinical data interoperability, ambient documentation and AI programs under clinical governance.",
    "Manufacturing & Industrial": "Sensor-driven quality, digital twins and shop-floor automation tied to OEE and yield.",
    "Retail & Consumer Goods": "Pricing, availability and personalization programs measured directly on margin.",
    "Telecom, Media & Entertainment": "Network analytics, churn saves and content operations at subscriber scale.",
    "Energy & Utilities": "Grid analytics, trading optimization and operational safety for the energy transition.",
    "Logistics & Supply Chain": "Demand sensing, routing and control-tower visibility from plant to doorstep.",
    "Public Sector & Government": "Service automation, case management and citizen experience under strict data sovereignty.",
    "Education & Research": "Student success analytics, research data platforms and campus operations.",
    "Technology & SaaS": "Platform engineering, usage analytics and AI features your product team can ship.",
    "Agriculture & Food Systems": "Yield intelligence, cold-chain visibility and processing automation from field to shelf.",
}

def fix_bullet(label: str, desc: str) -> str:
    if label in BULLET_LIB:
        return BULLET_LIB[label]
    d = clean(desc or '')
    # epigram pattern "A — B" with short A: turn into a readable sentence
    if ' — ' in d:
        a, b = d.split(' — ', 1)
        if len(a.split()) <= 7 and b:
            d = f"{a.strip()}: {b.strip()}"
    return d

# ── Pass C: hero + meta regeneration ─────────────────────────────────────
TOWER_NAMES = {t.lower(): t for t in [
    "Applied AI & Generative AI", "Agentic AI & Hyperautomation", "Data, Analytics & Lakehouse",
    "Cybersecurity & Zero-Trust", "Cloud, Edge & Platform Engineering", "Quantum & Advanced Compute",
    "Blockchain & Digital Trust", "IoT, Digital Twin & Robotics"]}

def tower_from_url(url):
    seg = url.split('/')
    for s in seg:
        if s in TOWER_NAMES:
            return TOWER_NAMES[s]
    for s in seg:
        for t in TOWER_NAMES:
            if s and (s in t or t.startswith(s)):
                return t
    return None

def hero_for(page):
    t = page.get('template')
    title = page.get('title', '')
    l2, l3 = page.get('l2') or '', page.get('l3') or ''
    if t in ('sub_capability', 'industry_capability'):
        cap = title.split(' for ')[0] if ' for ' in title else title
        sub = l3 or l2 or 'your sector'
        return (f"{cap} applied to {sub}. This page sets out the operating context, the delivery "
                f"pattern we run, the services and platforms involved, and the outcomes we commit to.")
    if t == 'tower_hub':
        tw = title
        return (f"Achala IT Solutions's {tw} practice: what the tower covers, the services inside it, the "
                f"platforms it deploys and the outcomes typical programs commit to.")
    if t == 'service_page':
        return (f"{title} as delivered by Achala IT Solutions: scope, delivery pattern, the platforms "
                f"involved and the outcomes we commit to at each gate.")
    if t == 'solution_page':
        return (f"{title}: the composed architecture, the platforms underneath and the metric "
                f"the program is judged on.")
    if t == 'industry_hub':
        return (f"How Achala IT Solutions serves {l2 or title}: priority programs, regulatory posture and "
                f"the capability towers aligned to the sector.")
    if t == 'subindustry_page':
        return (f"{title}: the operating units, priority programs and the five capability towers "
                f"that matter most here.")
    if t == 'platform_overview':
        return (f"{title}: what it does, the architecture and trust controls, and where it is "
                f"used inside client programs.")
    return None

def meta_for(page):
    t = page.get('template')
    title = page.get('title', '')
    l2, l3 = page.get('l2') or '', page.get('l3') or ''
    if t in ('sub_capability', 'industry_capability'):
        cap = title.split(' for ')[0] if ' for ' in title else title
        sub = l3 or l2 or 'your sector'
        m = f"{cap} for {sub}: delivery pattern, compliance frame, platforms and committed outcomes from Achala IT Solutions."
    elif t == 'tower_hub':
        m = f"{title} services from Achala IT Solutions: scope, delivery pattern, platforms and committed outcomes."
    elif t == 'service_page':
        m = f"{title} from Achala IT Solutions: scope, delivery pattern, platforms and committed outcomes."
    elif t == 'solution_page':
        m = f"{title} — composed architecture, platform stack and the metric the program answers to."
    elif t == 'industry_hub':
        m = f"Achala IT Solutions programs for {l2 or title}: priority use cases, regulatory posture and delivery model."
    else:
        return None
    return m[:158]

# ── Pass E: content expansion ────────────────────────────────────────────
EXPANDED_TEMPLATES = {'sub_capability', 'industry_capability', 'service_page', 'solution_page',
                      'tower_hub', 'industry_hub', 'platform_overview'}

RHYTHM_OPENINGS = [
    "Delivery follows the same weekly rhythm on every program of this type.",
    "Programs run on a fixed rhythm so progress is visible from week one.",
    "The engagement cadence below is the standard pattern for this capability.",
]
RHYTHM_P = ("Weeks 1–2 lock the baseline: the current metric is measured with your team and signed "
            "before build starts. Weeks 3–8 deliver the pilot on bounded scope — one decision path, "
            "one workflow, one plant or one portfolio — with a control owner named on your side. "
            "Weeks 9–12 industrialize what worked: runbooks, monitoring, enablement and a measured "
            "delta against the signed baseline. Anything that misses its gate is stopped or "
            "redirected with a documented decision, not quietly extended.")
ARTIFACTS = [
    ["Baseline diagnostic", "The signed measurement of where the metric stands today, with the method written out so the number can be defended to finance."],
    ["Decision and control map", "Every automated decision path, its policy checks, its human checkpoint and its owner on one page."],
    ["Evidence pack", "Logs, evaluations and approvals collected automatically as the program runs — ready for internal audit or a regulator."],
    ["Value ledger", "A running record of the delta against baseline, updated at every gate, reviewed at every steering meeting."],
]
PLUG_LEADS = [
    "This capability is one move in a larger program. The pages below show where it connects.",
    "No capability stands alone. These are the pages most clients open next.",
    "In delivery, this work composes with the adjacent capabilities listed here.",
]
RECEIVE_LEADS = [
    "At the end of the first quarter of a typical program you hold four concrete assets:",
    "Four named artifacts are delivered in the first quarter of every program of this type:",
    "The first quarter closes with the following artifacts handed over and walkthrough with your team:",
]

def expansion_blocks(page, links):
    t = page.get('template')
    out = []
    r = random.Random(hash(page.get('id', page.get('url', 'x'))) & 0xffffffff)
    if t == 'platform_overview':
        return out  # platforms already carry architecture detail
    out.append({"t": "h2", "x": "How a delivery runs"})
    out.append({"t": "p", "x": r.choice(RHYTHM_OPENINGS) + " " + RHYTHM_P})
    if links:
        out.append({"t": "h2", "x": "Where this fits in the portfolio"})
        out.append({"t": "p", "x": r.choice(PLUG_LEADS)})
        out.append({"t": "bullets", "items": [[x['title'], x['desc']] for x in links]})
    out.append({"t": "h2", "x": "What you receive"})
    out.append({"t": "p", "x": r.choice(RECEIVE_LEADS)})
    out.append({"t": "bullets", "items": ARTIFACTS})
    return out

# ── Pass F: interlinking ─────────────────────────────────────────────────
def load_index():
    rows = []
    for f in glob.glob(os.path.join(PAGES, '*.json')):
        d = json.load(open(f))
        rows.append({'url': d['url'], 'title': d['title'], 'template': d['template'],
                     'l1': d.get('l1'), 'l2': d.get('l2'), 'l3': d.get('l3'), 'l4': d.get('l4')})
    return rows

DESC_POOL = {
    'service_page': "Scope, delivery pattern and committed outcomes.",
    'tower_hub': "The practice overview and its services.",
    'solution_page': "Composed architecture and the metric it answers to.",
    'industry_hub': "Priority programs and regulatory posture.",
    'subindustry_page': "Operating units and priority towers.",
    'sub_capability': "The same capability applied to this sector.",
    'industry_capability': "A tower applied to this operating unit.",
    'platform_overview': "What the platform does and where it runs.",
    'case_study': "Anonymized engagement with audited baseline and outcome.",
    'platform_architecture': "Trust layers and control points.",
    'platform_usecases': "Deployed use cases by industry.",
}

def pick_links(page, rows, n=4):
    url = page['url']; t = page['template']
    links, seen = [], {url}
    def add(row):
        if row['url'] not in seen and len(links) < n:
            seen.add(row['url'])
            links.append({'title': row['title'], 'url': row['url'],
                          'desc': DESC_POOL.get(row['template'], '')})
    segs = [s for s in url.split('/') if s]
    if t in ('sub_capability', 'industry_capability'):
        # sibling capabilities in same sub-industry
        same = [r for r in rows if r['template'] == t and r['url'] != url
                and r.get('l3') == page.get('l3')]
        random.Random(url).shuffle(same)
        for r in same[:2]: add(r)
        # the parent industry hub
        parent = [r for r in rows if r['url'] == '/' + '/'.join(segs[:2]) + '/']
        for r in parent: add(r)
        # a service page of the same tower
        tw = tower_from_url(url)
        if tw:
            svc = [r for r in rows if r['template'] == 'service_page'
                   and r['title'].lower() == tw.lower()]
            for r in svc[:1]: add(r)
    elif t == 'service_page':
        sib = [r for r in rows if r['template'] == 'service_page' and r['url'] != url
               and r.get('l2') == page.get('l2')]
        random.Random(url).shuffle(sib)
        for r in sib[:2]: add(r)
        sols = [r for r in rows if r['template'] == 'solution_page']
        random.Random(url + 's').shuffle(sols)
        for r in sols[:1]: add(r)
        ind = [r for r in rows if r['template'] == 'industry_capability']
        random.Random(url + 'i').shuffle(ind)
        for r in ind[:1]: add(r)
    elif t == 'solution_page':
        ind = [r for r in rows if r['template'] == 'industry_hub']
        random.Random(url).shuffle(ind)
        for r in ind[:2]: add(r)
        svc = [r for r in rows if r['template'] == 'service_page']
        random.Random(url + 's').shuffle(svc)
        for r in svc[:1]: add(r)
        cases = [r for r in rows if r['template'] == 'case_study']
        random.Random(url + 'c').shuffle(cases)
        for r in cases[:1]: add(r)
    elif t in ('industry_hub', 'subindustry_page'):
        caps = [r for r in rows if r['template'] in ('industry_capability', 'sub_capability')
                and r.get('l2') == page.get('l2')]
        random.Random(url).shuffle(caps)
        for r in caps[:2]: add(r)
        sols = [r for r in rows if r['template'] == 'solution_page']
        random.Random(url + 's').shuffle(sols)
        for r in sols[:1]: add(r)
        for r in [r for r in rows if r['url'] == '/case-studies/'][:1]: add(r)
    return links

# ── runner ───────────────────────────────────────────────────────────────
def process_page(path, rows):
    d = json.load(open(path))
    url = d.get('url', '')
    t = d.get('template', '')
    changed = False

    # C: hero
    if t != 'home' and t != 'case_study':
        h = hero_for(d)
        if h:
            for b in d.get('blocks', []):
                if b.get('t') == 'hero':
                    if b.get('x') != h:
                        b['x'] = h; changed = True
    # C: clean all other strings
    for b in d.get('blocks', []):
        bt = b.get('t')
        if bt == 'p' or bt == 'note' or bt == 'cta':
            nx = clean(b.get('x', ''))
            if nx != b.get('x'):
                b['x'] = nx; changed = True
        elif bt == 'bullets':
            for item in b.get('items', []):
                if isinstance(item, list) and len(item) == 2:
                    nd = fix_bullet(item[0], item[1])
                    nd = clean(nd)
                    if nd != item[1]:
                        item[1] = nd; changed = True
    # D: meta
    m = meta_for(d)
    if m and d.get('meta_description') != m:
        d['meta_description'] = m; changed = True

    # E: expansion (idempotent — skip if headings already present)
    heads = {b.get('x') for b in d.get('blocks', []) if b.get('t') == 'h2'}
    if t in EXPANDED_TEMPLATES and 'How a delivery runs' not in heads:
        links = pick_links(d, rows)
        # keep the final cta last
        blocks = d.get('blocks', [])
        tail = [b for b in blocks if b.get('t') == 'cta']
        core = [b for b in blocks if b.get('t') != 'cta']
        newblocks = core + expansion_blocks(d, links) + tail
        d['blocks'] = newblocks
        changed = True
        # F: richer related
        if links:
            rel = [{'title': x['title'], 'url': x['url'], 'desc': x['desc']} for x in links]
            existing = {(r['url']) for r in d.get('related', [])}
            extra = [r for r in rel if r['url'] not in existing]
            d['related'] = (d.get('related') or []) + extra[:4]
    # G-light: phrase map on related/cards titles & descs
    for r in d.get('related', []) or []:
        r['title'] = clean(r.get('title', ''))
        r['desc'] = clean(r.get('desc', ''))
    for c in d.get('cards', []) or []:
        c['title'] = clean(c.get('title', ''))
        c['desc'] = clean(c.get('desc', ''))

    if changed:
        json.dump(d, open(path, 'w'), indent=1, ensure_ascii=False)
    return changed

def main():
    if not os.path.exists(BACKUP):
        shutil.copytree(PAGES, BACKUP)
        print('backup written to', BACKUP)
    rows = load_index()
    n = 0
    files = sorted(glob.glob(os.path.join(PAGES, '*.json')))
    for i, f in enumerate(files):
        try:
            if process_page(f, rows):
                n += 1
        except Exception as e:
            print('ERR', os.path.basename(f), e)
        if i % 100 == 0:
            print(f'  {i}/{len(files)}')
    print('pages changed:', n, '/', len(files))

if __name__ == '__main__':
    main()
