# -*- coding: utf-8 -*-
"""Copy data for brand.json, hub pages and global phrase cleanup.
Infosys-inspired voice: plain, concrete, outcome-first."""

BRAND = {
    "tagline": "Making IT possible",
    "positioning": "Achala IT Solutions builds AI-first platforms and engineering services that take enterprise programs from proof of concept to production. Founded in 2009, ISO/IEC 27001 certified and TISAX-audited, with delivery teams in India, Germany and Bulgaria.",
    "promise": "We commit to a business metric before delivery starts, and we report against it every month.",
}

# per-file rewrites: hero + meta_description + targeted paragraph replacements
HUBS = {
    "services": {
        "hero": "Achala runs 54 engineering practices across 8 expertise domains, from AI and data to cloud, security and IoT. Each engagement starts with a business metric you sign before delivery begins, and every domain works to the same delivery standard.",
        "meta": "54 engineering practices across 8 expertise domains — AI, data, cloud, security, IoT and more. Every engagement is measured against a signed business baseline.",
        "repl": {
            "Whichever of the eight domains you enter, the contract is identical: a business metric signed before delivery starts, an architecture you can audit before it ships, and exit numbers your finance team can reconcile. Fifty-four practices. Twelve industries. One governed spine.": "Whichever domain you enter, the working agreement is the same: a business metric signed before delivery starts, an architecture you can review before it ships, and results your finance team can reconcile. Fifty-four practices, twelve industries, one delivery standard.",
            "Each domain card opens its hub — the practices, the reference architectures, the sector briefs and the metric the domain is managed on.": "Each domain page lists its practices, reference architectures, sector briefs and the metric the domain is managed on.",
        },
    },
    "industries": {
        "hero": "Achala works in twelve industries, each with sub-industry pages that map our services to the sector's regulations, systems of record and daily workflows. Start with your industry and see the programs we have run there.",
        "meta": "Twelve industries with sub-industry depth. Each page maps the sector's regulations, systems and workflows to the Achala services that serve them.",
        "repl": {
            "Twelve industries, each with sub-industry depth and capability pages that align the domains to the sector's operating physics. Industry pages here are not brochures: they carry the": "Twelve industries, each with sub-industry pages that map our services to the sector's regulations, systems of record and daily workflows. Every industry page carries the",
            "Twelve industries, one operating discipline": "Twelve industries, one delivery standard",
            "Sub-industries": "Sub-industries",
        },
    },
    "solutions": {
        "hero": "Achala solutions package a named business problem with the architecture, platforms and metric to solve it. Twenty-four solutions are available today, each one composed from two to four service domains and measured in units a CFO recognizes.",
        "meta": "24 packaged solutions: a named business problem, a composed architecture, a platform stack and a metric the program is measured on.",
        "repl": {
            "Solutions are how clients buy outcomes rather than domains: a named business problem, a composed architecture from two to four domains, and a value case written in the CFO's units.": "Clients buy outcomes, not domains. Each solution packages a named business problem with a composed architecture from two to four service domains and a value case written in units a CFO recognizes.",
            "24 outcome-linked solutions": "24 packaged solutions",
        },
    },
    "consulting": {
        "hero": "Thirteen consulting and engineering practices covering data migration, software development, testing, application modernization, experience design, IT services, cloud, ERP and cybersecurity. The team that advises you is the team that builds — one diagnostic, one signed baseline, one accountable delivery.",
        "meta": "Thirteen IT consulting and engineering practices: data migration, software development, testing, modernization, IT services, cloud, ERP and cybersecurity.",
        "repl": {
            "Thirteen consulting and engineering practices, one governed delivery system. Data migration, software development, testing, application modernization, experience design, IT service": "Thirteen consulting and engineering practices under one delivery standard. Data migration, software development, testing, application modernization, experience design, IT service",
        },
    },
    "case-studies": {
        "hero": "116 anonymized client engagements, indexed by industry and by service area. Every case note carries the measured result, the system that produced it and the gates that governed the build.",
        "meta": "116 anonymized client engagements across 12 industries and 8 service areas, each with its measured result and delivery record.",
        "repl": {
            "The case index": "The case index",
            "Indexed by industry and service area — every case carries its measured delta and the gates that governed the build.": "Indexed by industry and service area. Every case carries its measured result and the gates that governed the build.",
        },
    },
    "insights": {
        "hero": "Practical writing from the delivery floor: what ships, what scales and what stalls in production AI, data and security programs. Each piece takes a position and includes the questions you should ask any vendor, including us.",
        "meta": "Perspectives from the delivery floor on production AI, data platforms, security and emerging compute — with the vendor questions to ask.",
        "repl": {
            "Practitioner theses from the delivery floor. Each insight takes a position, shows where it breaks in practice, and names the discipline that keeps it honest — no vendor theater, no": "Practical writing from the delivery floor. Each insight takes a position, shows where it breaks in practice, and names the discipline that keeps it honest. No",
            "Practitioner theses from the delivery floor — published with vendor questions included.": "Written by the people who ran the work — vendor questions included.",
        },
    },
    "about-us": {
        "hero": "Achala IT Solutions Private Limited, founded in 2009, is an AI-first, platform-driven engineering company with full-cycle software product engineering services. Headquartered in Hyderabad with delivery teams in Munich and Sofia, the company runs 300+ people — including 200+ IT specialists — and holds ISO/IEC 27001 certification with TISAX-audited, GDPR-aligned delivery.",
        "meta": "Achala IT Solutions — founded 2009, Hyderabad HQ with delivery teams in Munich and Sofia. 300+ people, ISO/IEC 27001, TISAX-audited, GDPR-aligned delivery.",
        "repl": {},
    },
    "why-achala": {
        "hero": "Enterprises choose Achala for four reasons: a business metric signed before delivery starts, a named owner on every control, proprietary platforms that arrive configured instead of blank-page, and a delivery method that documents every gate.",
        "meta": "Why enterprises choose Achala: signed baselines, named control owners, proprietary platforms and a delivery method that documents every gate.",
        "repl": {},
    },
    "contact": {
        "hero": "Tell us what you are building. A practice lead — not a call center — replies within one business day with the fastest path from proof of concept to production.",
        "meta": "Reach Achala IT Solutions: +91 7337444922, info@achalasolutions.com. Offices in Hyderabad (India), Munich (Germany) and Sofia (Bulgaria).",
        "repl": {
            "A practice lead — not a call-center — replies with the fastest path from POC to production.": "A practice lead — not a call center — replies within one business day with the fastest path from proof of concept to production.",
        },
    },
    "book-a-briefing": {
        "hero": "A 45-minute working session with a practice lead: your metric, our reference architectures, three comparable engagements and an honest feasibility read you can circulate.",
        "meta": "Book a 45-minute briefing with an Achala practice lead: your metric, our reference architectures and an honest feasibility read.",
        "repl": {
            "A working session on your use case, not a demo script.": "A working session on your use case, not a scripted demo.",
        },
    },
}

# global phrase cleanup applied to every page block body (the AI-tell vocabulary)
PHRASE_MAP = {
    "one governed spine": "one delivery standard",
    "the operating physics": "daily workflows",
    "vendor theater": "vendor noise",
    "governed stack": "platform suite",
    "decision estate": "decision systems",
    "policy envelope": "defined policy limit",
    "the retrieval layer": "retrieval",
    "evidence-or-stop contract": "evidence-gated delivery contract",
    "a staffing plan": "a staffing schedule",
    "blank page and a": "blank page and a",
    "Ambition is common in this industry; production is not.": "Most providers can promise this. Fewer can show it in production.",
    "the advisor is the builder": "the advisor is also the builder",
    "where your P&L leaks today": "where your P&L loses money today",
    "acceleration you can audit, not a claim": "acceleration your auditors can verify",
    "speed you can audit, not a claim": "speed your auditors can verify",
    "the frontline gets leverage, not another dashboard": "the frontline gets real leverage",
    "Controls that survive audit": "Audit-ready controls",
    "Capacity, cutover, ERP cores or a helpdesk that has to answer.": "Capacity, system cutover, ERP cores or a helpdesk that has to answer.",
    "An estate that will not move without breaking something.": "An estate that resists change because everything depends on it.",
    "Data nobody trusts, disputes nobody resolves.": "Data nobody trusts and disputes nobody resolves.",
    "Risk you can sense but cannot evidence to a regulator.": "Risk you can sense but cannot prove to a regulator.",
    "Decisions too slow to defend, or too opaque to audit.": "Decisions too slow to defend, or too opaque to audit.",
    "findings filed automatically, with timestamps": "findings filed automatically with timestamps",
    "so week two already reads like your business": "so week two already reflects your business",
}

# em-dash policy: in body text, " — " becomes ", " (kept in titles/breadcrumbs)
DASH_FIX_BODY = True
