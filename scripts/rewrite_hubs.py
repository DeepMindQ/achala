"""Hub page hero/intro rewrites (services, industries, platforms, solutions, about, why)."""
import json

R = '/home/z/my-project/site/src/content/pages/'

FIX = {
 'services.json': {
   'hero': "Consulting and delivery across eight deep-tech towers, run as one delivery system with shared platforms and named gates.",
   'p1': "Achala IT Solutions's services are organized into eight towers. Each tower carries named services with defined deliverables and the platform rails they deploy on. Towers compose: a fraud program draws on data engineering, agentic automation and cybersecurity at the same time, under one delivery plan and one accountable lead.",
 },
 'industries.json': {
   'hero': "Twelve industries with sub-industry depth — each page maps the sector's programs, regulatory posture and the capability towers aligned to it.",
   'p1': "Every industry page carries the sector's operating pressures, regulatory posture, priority programs and proof engagements — then aligns all eight capability towers at industry level and the five priority towers at sub-industry level.",
   'p2': "Industry hub (the sector's operating profile) → sub-industry pages (the operating units: payments, prior auth, cold chain, smart cities) → capability pages (a tower applied to the sector, e.g. Agentic AI for Banking or Computer Vision for Manufacturing). Every capability page carries the same structure: context, delivery pattern, compliance frame and committed outcomes.",
 },
 'platforms.json': {
   'hero': "Eight proprietary platforms encode our delivery patterns as configurable products — governance, security controls and evidence generation arrive pre-built.",
   'p1': "Platforms are how Achala IT Solutions turns consulting into leverage: each platform ships with the controls, evidence generation and delivery patterns our teams have standardized. Clients start from a configured 80 percent baseline and spend their budget on the 20 percent that is genuinely theirs.",
 },
 'solutions.json': {
   'hero': "24 outcome-based solutions: a named business problem, a composed architecture, a platform stack and a metric the program answers to.",
   'p1': "Solutions sit between the service towers and the case studies: a named business problem with a composed architecture, the platforms underneath and committed outcomes. They are how clients buy outcomes rather than capabilities.",
 },
 'about-us.json': {
   'hero': "Achala IT Solutions is a global IT services and consulting company that builds the AI and data systems enterprises run on — 2,400+ engineers across four delivery centers, eight proprietary platforms in production.",
   'p1': "Achala IT Solutions was founded on a simple observation: enterprises were accumulating AI pilots that never reached production. The gap was rarely model capability; it was the operating machinery around it — data contracts, decision ownership, monitoring and audit. So we built that machinery first: decision hubs with replay, data estates with contracts, agent fleets with policy envelopes, and governance that produces evidence continuously instead of annually.",
 },
 'why-achala-soft.json': {
   'hero': "Why enterprises choose Achala IT Solutions: named baselines, named control owners, proprietary platforms and a delivery method that documents every gate.",
 },
}

for f, fix in FIX.items():
    p = R + f
    d = json.load(open(p))
    blocks = d['blocks']
    for b in blocks:
        if b['t'] == 'hero' and 'hero' in fix:
            b['x'] = fix['hero']
    # replace first p with p1
    pis = [i for i, b in enumerate(blocks) if b['t'] == 'p']
    if 'p1' in fix and pis:
        blocks[pis[0]]['x'] = fix['p1']
    if 'p2' in fix and len(pis) > 1:
        blocks[pis[1]]['x'] = fix['p2']
    # clean any remaining bullets in these pages via clean()
    import sys, os
    sys.path.insert(0, '/home/z/my-project/scripts')
    from content_overhaul import clean, fix_bullet
    for b in blocks:
        if b['t'] == 'p':
            b['x'] = clean(b['x'])
        elif b['t'] == 'bullets':
            for it in b['items']:
                it[1] = clean(fix_bullet(it[0], it[1]))
        elif b['t'] == 'cta':
            b['x'] = clean(b['x'])
    d['meta_description'] = fix['hero'][:158]
    d['seo_title'] = d['seo_title']
    json.dump(d, open(p, 'w'), indent=1, ensure_ascii=False)
    print('rewritten', f)
