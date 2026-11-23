# -*- coding: utf-8 -*-
"""Phase 2 content rewrite engine.

Removes the machine-template residue from content JSONs:
  1. Nine platitude stems repeated across bullets/paragraphs on 600+ pages
  2. Fabricated precision stats ("Down 50-65.2%", "Target range 38%")
Replaces them with honest, label-matched, human-written descriptions.

Idempotent: re-running on rewritten files changes nothing.
"""
import json, os, re, sys, hashlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from phase2_stack import STACK
from phase2_dicts import (MODULES, TELEMETRY, FAILURES, RECEIVE, GET, STAGES,
                          ROLLOUT, FIRST90, VENDORQ, DIFFERENTLY, TRANSFER,
                          DETAILS, KEYQ, COMPLIANCE, DEPLOY, CHANGES,
                          TOWER_DESC, OUTCOME_POOL, PRESSURE_POOL,
                          CASE_REF_POOL, INSIGHT_REF, PORTFOLIO_FALLBACK,
                          STAT_FREE)
from phase2_paras import PARAS, INDUSTRY_PARA_KEY, DIAGRAM_NOTES, CTA_LINES, NOTE_LINES

D = 'site/src/content/pages'
STEMS = ['The part that survives audit', 'The engineering bet is explicit',
         'The design principle here', 'Under the hood this pattern',
         'Nothing in this topology', 'The build earns trust',
         'At operating tempo', 'What holds the build together',
         'The rhythm is engineered']
STATPAT = re.compile(
    r'(Down \d+[–-]\d+(\.\d+)?%|Target range \d+%|Reported as \d+%'
    r'|\d+[–-]\d+(\.\d+)?% (lower|faster|better|up|down|fewer)'
    r'|\b\d+(\.\d+)?\s?x\b (their|margin|weight))')
INDUSTRY_PARAS = [
  "In {IND}, the regulatory lens decides what a good decision looks like — {T} exists to make that decision defensible at the speed the sector actually runs at.",
  "{T} earns its place in {IND} by sitting on a decision path the regulator can inspect — the pattern below is built for exactly that inspection.",
  "The case for {T} in {IND} rests on measurement: the baseline is signed with your team, the delta is audited at the gate, and the method note survives the review.",
  "{IND} punishes decisions that cannot explain themselves. {T} is engineered so every decision carries its reasons, its owner and its evidence from day one.",
  "What changes in {IND} is the cost of being wrong: {T} is designed around the controls and auditability that keep that cost bounded.",
  "{T} adapts the standard pattern to {IND} — the governance is sector-calibrated, the delivery standard is not.",
]
GENERIC_PARAS = [
    "{T} runs on the same delivery standard as the rest of the portfolio: measure first, gate honestly, and let the evidence decide what scales.",
    "The sections below describe {T} the way we deliver it — the pattern, the stack, the guards and the artifacts your team holds at the first quarter close.",
    "{T} is described here in operational terms: who owns what, where the evidence lives, and what stops the program if the numbers stop moving.",
    "What follows is the working detail of {T} — written for the people who will run it, not for a brochure.",
]

def norm(s):
    return s.strip().lower()

def h(*parts):
    return int(hashlib.md5('||'.join(str(p) for p in parts).encode()).hexdigest(), 16)

def pick(pool, *keyparts):
    return pool[h(*keyparts) % len(pool)]

def first_sentence(text, cap=150):
    m = re.match(r'(.+?\.)', text or '', re.S)
    s = (m.group(1) if m else (text or '')).strip()
    if len(s) > cap:
        s = s[:cap].rsplit(' ', 1)[0].rstrip(',') + '.'
    return s

def load_pages():
    out = {}
    for f in os.listdir(D):
        if f.endswith('.json'):
            out[f] = os.path.join(D, f)
    return out

def build_reference_dicts(files):
    svc_desc, ind_desc, case_titles = {}, {}, set()
    for f, p in files.items():
        try:
            data = json.load(open(p, encoding='utf-8'))
        except Exception:
            continue
        t = data.get('template')
        title = (data.get('title') or '').strip()
        hero = ''
        for b in data.get('blocks', []):
            if b.get('t') == 'hero':
                hero = b.get('x', '')
                break
        if t == 'service_page' and title and hero:
            svc_desc[norm(title)] = first_sentence(hero)
        elif t == 'industry_hub' and title and hero:
            ind_desc[norm(title)] = first_sentence(hero)
        elif t == 'case_study' and title:
            case_titles.add(title)
    return svc_desc, ind_desc, case_titles

def resolve_bullet(page_id, section, label, desc, ctx):
    """Return the honest replacement description for a template bullet."""
    key = norm(label)
    seed = (page_id, section, label)
    # fixed dictionaries, most specific first
    if section == 'What you receive' and key in RECEIVE:
        return RECEIVE[key]
    if section in ('What you get',) and key in GET:
        return GET[key]
    if section in ('How it runs in an engagement',) and key in STAGES:
        return STAGES[key]
    if section in ('What a rollout looks like',) and key in ROLLOUT:
        return ROLLOUT[key]
    if section in ('The first 90 days',) and key in FIRST90:
        return FIRST90[key]
    if section in ('Three questions to ask your current vendors',) and key in VENDORQ:
        return VENDORQ[key]
    if section in ('What we do differently',) and key in DIFFERENTLY:
        return DIFFERENTLY[key]
    if section in ('Transfer notes',) and key in TRANSFER:
        return TRANSFER[key]
    if section in ('Details',) and key in DETAILS:
        return DETAILS[key]
    if section in ('Key questions this category answers',) and key in KEYQ:
        return KEYQ[key]
    if section in ('Compliance mapping',) and key in COMPLIANCE:
        return COMPLIANCE[key]
    if section in ('Deployment models',) and key in DEPLOY:
        return DEPLOY[key]
    if section in ('What changes for the business',) and key in CHANGES:
        return CHANGES[key]
    if section in ('Failure modes & the guards we ship',) and key in FAILURES:
        return FAILURES[key]
    if section in ('Operational telemetry',) and key in TELEMETRY:
        return TELEMETRY[key]
    if section in ('How we help — five priority capabilities', 'The towers', 'Categories') and key in TOWER_DESC:
        return TOWER_DESC[key]
    # label-based dictionaries
    if key in STACK:
        return STACK[key]
    if key in MODULES:
        return MODULES[key]
    if key in TOWER_DESC:
        return TOWER_DESC[key]
    if key in ctx.svc_desc:
        return ctx.svc_desc[key]
    if key in ctx.ind_desc:
        return ctx.ind_desc[key]
    # case entities
    if label.strip() in ctx.case_titles:
        return pick(CASE_REF_POOL, seed)
    # section pools
    if section == 'Outcomes we commit to':
        return pick(OUTCOME_POOL, seed).replace('{L}', label.strip())
    if section.startswith('Pressure points'):
        return pick(PRESSURE_POOL, seed).replace('{L}', label.strip())
    if section == 'Latest articles':
        return pick(INSIGHT_REF, seed)
    if section == 'Where this fits in the portfolio':
        return pick(PORTFOLIO_FALLBACK, seed).replace('{L}', label.strip())
    return pick(OUTCOME_POOL, seed).replace('{L}', label.strip())

class Ctx:
    pass

def para_for(page_id, section, title, old):
    seed = (page_id, section)
    title = re.split(r'\s+—\s+', title)[0]  # 'Achala Forge — Overview' -> 'Achala Forge'
    if section.startswith(INDUSTRY_PARA_KEY):
        ind = section[len(INDUSTRY_PARA_KEY):].strip()
        return pick(INDUSTRY_PARAS, seed).replace('{IND}', ind).replace('{T}', title)
    if section in PARAS:
        return pick(PARAS[section], seed).replace('{T}', title)
    return pick(GENERIC_PARAS, seed).replace('{T}', title)

METRIC_SLOT = re.compile(r'your ([A-Za-z][^,.;]{2,60}?) measured and signed', re.I)

def page_title(data):
    return data.get('title') or data.get('breadcrumb') or ''

def rewrite_file(path, page_id, ctx, report):
    data = json.load(open(path, encoding='utf-8'))
    changed = False
    title = page_title(data)
    cur = None
    for b in data.get('blocks', []):
        t = b.get('t')
        if t == 'h2':
            cur = b.get('x', '')
        elif t == 'p':
            x = b.get('x', '')
            if any(s in x for s in STEMS):
                b['x'] = para_for(page_id, cur or 'Overview', title, x)
                report['paras'] = report.get('paras', 0) + 1
                report.setdefault('para_sections', {}).setdefault(cur or 'Overview', 0)
                report['para_sections'][cur or 'Overview'] += 1
                changed = True
        elif t == 'diagram':
            note = b.get('note') or ''
            if any(s in note for s in STEMS) or STATPAT.search(note):
                kind = b.get('kind') if b.get('kind') in DIAGRAM_NOTES else 'pipeline'
                b['note'] = pick(DIAGRAM_NOTES[kind], (page_id, b.get('title'), note[:30]))
                report['diagram_notes'] = report.get('diagram_notes', 0) + 1
                changed = True
        elif t == 'cta':
            x = b.get('x', '')
            slot = METRIC_SLOT.search(x)
            dirty = any(s in x for s in STEMS) or STATPAT.search(x) or (slot and slot.group(1).strip().lower() != 'baseline')
            if dirty:
                tpl = data.get('template') or 'service_page'
                pool = CTA_LINES.get(tpl) or CTA_LINES['service_page']
                b['x'] = pick(pool, (page_id, 'cta'))
                report['cta'] = report.get('cta', 0) + 1
                changed = True
        elif t == 'note':
            x = b.get('x', '')
            if any(s in x for s in STEMS) or STATPAT.search(x):
                b['x'] = pick(NOTE_LINES, (page_id, 'note', x[:30]))
                report['notes'] = report.get('notes', 0) + 1
                changed = True
        elif t == 'bullets':
            items = b.get('items', [])
            for it in items:
                if not (isinstance(it, (list, tuple)) and len(it) >= 2):
                    continue
                label, desc = it[0], it[1]
                dirty = any(s in desc for s in STEMS) or STATPAT.search(desc)
                if not dirty:
                    continue
                new = resolve_bullet(page_id, cur or '', label, desc, ctx)
                if new and new != desc:
                    it[0] = label.strip()
                    it[1] = new
                    report['bullets'] = report.get('bullets', 0) + 1
                    report.setdefault('bullet_sections', {}).setdefault(cur or '?', 0)
                    report['bullet_sections'][cur or '?'] += 1
                    changed = True
    if changed:
        # recompute words
        words = 0
        for b in data.get('blocks', []):
            if b.get('t') in ('p', 'h2', 'hero'):
                words += len((b.get('x') or '').split())
            elif b.get('t') == 'bullets':
                for it in b.get('items', []):
                    if isinstance(it, (list, tuple)):
                        words += len((' '.join(str(x) for x in it)).split())
                    elif isinstance(it, str):
                        words += len(it.split())
        data['words'] = words
        json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return changed

def main():
    files = load_pages()
    ctx = Ctx()
    ctx.svc_desc, ctx.ind_desc, ctx.case_titles = build_reference_dicts(files)
    report = {}
    n_changed = 0
    for f, p in sorted(files.items()):
        page_id = f[:-5]
        if rewrite_file(p, page_id, ctx, report):
            n_changed += 1
    print(f'pages changed: {n_changed}')
    print(f'paragraphs rewritten: {report.get("paras", 0)}')
    print(f'bullets rewritten: {report.get("bullets", 0)}')
    print('\nparagraph sections:')
    for k, v in sorted(report.get('para_sections', {}).items(), key=lambda x: -x[1]):
        print(f'  {v:5}  {k}')
    print('\nbullet sections:')
    for k, v in sorted(report.get('bullet_sections', {}).items(), key=lambda x: -x[1]):
        print(f'  {v:5}  {k}')

if __name__ == '__main__':
    main()
