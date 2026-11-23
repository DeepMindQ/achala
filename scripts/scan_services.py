#!/usr/bin/env python3
"""Scan the Services section of the Achala site: pages, depth, structure."""
import os, json, glob, re

SITE = '/home/z/my-project/site'
pages_dir = os.path.join(SITE, 'src/content/pages')

# 1. find services-related JSONs by filename
files = sorted(os.listdir(pages_dir))
svc = [f for f in files if f.startswith(('services', 'svc', 'service'))]
print(f'=== services-named page JSONs ({len(svc)}) ===')
for f in svc:
    p = os.path.join(pages_dir, f)
    try:
        d = json.load(open(p, encoding='utf-8'))
    except Exception as e:
        print(' PARSE FAIL', f, e); continue
    blocks = d.get('blocks', [])
    words = d.get('words', 0)
    title = d.get('title', '')[:60]
    types = {}
    for b in blocks:
        types[b.get('t', '?')] = types.get(b.get('t', '?'), 0) + 1
    charts = sum(types.get(k, 0) for k in ('chart', 'visual', 'diagram', 'arch'))
    print(f'  {f:52s} words={words:5d} blocks={len(blocks):3d} charts={charts} l1={d.get("l1","")[:22]!r} l2={d.get("l2","")[:28]!r}')

# 2. how the nav refers to services
nav = json.load(open(os.path.join(SITE, 'src/content/nav.json'), encoding='utf-8'))
def walk(items, depth=0, path=''):
    for it in items:
        name = it.get('name') or it.get('label') or ''
        href = it.get('href') or it.get('url') or ''
        kids = it.get('children') or it.get('items') or it.get('groups') or []
        if 'service' in href.lower() or 'service' in name.lower() or depth <= 1:
            print('  ' * depth + f'- {name} -> {href}')
        if isinstance(kids, list) and depth < 2:
            walk(kids, depth + 1, path)
print('=== nav structure (top 2 levels) ===')
if isinstance(nav, dict):
    for k, v in nav.items():
        if isinstance(v, list):
            print('KEY:', k)
            walk(v)
        else:
            print('KEY:', k, type(v))
else:
    walk(nav)
