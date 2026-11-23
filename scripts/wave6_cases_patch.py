#!/usr/bin/env python3
"""Wave 6: CaseStudies.tsx — drop manual-style UI, human consulting voice."""
P = "/home/z/my-project/site/src/components/site/CaseStudies.tsx"
s = open(P).read()

# 1. remove NDAA chip constant
old = 'const NDAA_CHIP = "Identity withheld · Baseline audited · Method under NDA";\n\n'
assert s.count(old) == 1
s = s.replace(old, "")

# 2. drop readingH2/readingP/noteX vars (section will be removed)
old = """  const readingH2 = page.blocks.find((b) => b.t === "h2")?.x;
  const readingP = page.blocks.find((b) => b.t === "p")?.x;
  const noteX = page.blocks.find((b) => b.t === "note")?.x;
  const ctaX = page.blocks.find((b) => b.t === "cta")?.x;"""
new = """  const ctaX = page.blocks.find((b) => b.t === "cta")?.x;"""
assert s.count(old) == 1
s = s.replace(old, new)

# 3. hub hero kicker + chips rewrite
old = """            <p className="kicker-bar-dark text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-300">
              Evidence library
            </p>
            <h1 className="text-display-2 mt-2 text-white">Case studies</h1>"""
new = """            <p className="kicker-bar-dark text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-300">
              Client results
            </p>
            <h1 className="text-display-2 mt-2 text-white">Case studies</h1>"""
assert s.count(old) == 1
s = s.replace(old, new)

# 4. chips row: drop NDA chip, reframe counts
old = """          <div className="mt-6 flex flex-wrap items-center gap-2.5">
            <span className="rounded-full border border-brand/40 bg-brand/15 px-3.5 py-1.5 text-[12px] font-semibold text-brand-300">
              {cards.length} case studies
            </span>
            <span className="rounded-full border border-white/15 bg-white/[0.06] px-3.5 py-1.5 text-[12px] text-white/70">
              {industries.length} industries
            </span>
            <span className="rounded-full border border-white/15 bg-white/[0.06] px-3.5 py-1.5 text-[12px] text-white/70">
              {services.length} service areas
            </span>
            <span className="inline-flex items-center gap-1.5 rounded-full border border-white/15 bg-white/[0.06] px-3.5 py-1.5 text-[12px] text-white/70">
              <ShieldCheck className="h-3.5 w-3.5 text-brand-300" aria-hidden="true" /> {NDAA_CHIP}
            </span>
          </div>"""
new = """          <div className="mt-6 flex flex-wrap items-center gap-2.5">
            <span className="rounded-full border border-brand/40 bg-brand/15 px-3.5 py-1.5 text-[12px] font-semibold text-brand-300">
              {cards.length} engagements published
            </span>
            <span className="rounded-full border border-white/15 bg-white/[0.06] px-3.5 py-1.5 text-[12px] text-white/70">
              {industries.length} industries
            </span>
            <span className="rounded-full border border-white/15 bg-white/[0.06] px-3.5 py-1.5 text-[12px] text-white/70">
              {services.length} service areas
            </span>
            <span className="inline-flex items-center gap-1.5 rounded-full border border-white/15 bg-white/[0.06] px-3.5 py-1.5 text-[12px] text-white/70">
              <ShieldCheck className="h-3.5 w-3.5 text-brand-300" aria-hidden="true" /> Measured against signed baselines
            </span>
          </div>"""
assert s.count(old) == 1
s = s.replace(old, new)

# 5. buttons
s = s.replace("Browse the full index <ArrowDownIcon />", "Explore the results <ArrowDownIcon />")
s = s.replace(""">
              Book an Executive Briefing
            </Link>""", """>
              Book a 45-minute briefing
            </Link>""")

# 6. remove the whole "reading a case" section
start = s.index("      {/* reading a case */}")
end = s.index("      {/* ── browse by industry ──")
s = s[:start] + s[end:]

# 7. browse-by-industry heading
old = """                <p className="kicker-bar text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">
                  Index one — by industry
                </p>
                <h2 className="text-display-3 mt-1 text-navy-800 sm:text-[26px]">
                  Find the cases that operate under your rules
                </h2>
              </div>
              <p className="max-w-md text-[13px] text-slate-body/70">
                Twelve industry groups — {industries.map((i) => `${i.name} (${i.count})`).slice(0, 4).join(", ")} and
                more — each case written for the sector&rsquo;s regulatory and operational reality.
              </p>"""
new = """                <p className="kicker-bar text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">
                  By industry
                </p>
                <h2 className="text-display-3 mt-1 text-navy-800 sm:text-[26px]">
                  Start with the sector you run
                </h2>
              </div>
              <p className="max-w-md text-[13px] text-slate-body/70">
                Engagement notes from every sector we serve — each written for the rules, pressures and systems of
                record of that industry.
              </p>"""
assert s.count(old) == 1
s = s.replace(old, new)

# 8. browse-by-service heading
old = """            <p className="kicker-bar text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">
              Index two — by service area
            </p>
            <h2 className="text-display-3 mt-1 text-navy-800 sm:text-[26px]">
              Or start from the capability that did the work
            </h2>"""
new = """            <p className="kicker-bar text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">
              By service area
            </p>
            <h2 className="text-display-3 mt-1 text-navy-800 sm:text-[26px]">
              Or start with the capability
            </h2>"""
assert s.count(old) == 1
s = s.replace(old, new)

# 9. full index heading
old = """            <p className="kicker-bar text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">
              Full index
            </p>
            <h2 className="text-display-3 mt-1 text-navy-800 sm:text-[26px]">
              Every engagement, filterable both ways
            </h2>"""
new = """            <p className="kicker-bar text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">
              The library
            </p>
            <h2 className="text-display-3 mt-1 text-navy-800 sm:text-[26px]">
              Every engagement, one filter away
            </h2>"""
assert s.count(old) == 1
s = s.replace(old, new)

# 10. default CTA band copy
old = '<CtaBand message={ctaX ?? "Book an executive briefing — bring the metric, leave with the method."} />'
new = '<CtaBand message={ctaX ?? "Book a briefing — bring the metric you need to move, and we will walk the closest engagement end to end."} />'
assert s.count(old) == 1
s = s.replace(old, new)

# 11. study page kicker
s = s.replace("""              Case study — anonymized
            </p>""", """              Case study
            </p>""")

# 12. study hero: remove NDAA chip
old = """            <span className="inline-flex items-center gap-1.5 rounded-full border border-brand/40 bg-brand/15 px-3.5 py-1.5 text-[12px] font-semibold text-brand-300">
              <ShieldCheck className="h-3.5 w-3.5" aria-hidden="true" /> {NDAA_CHIP}
            </span>
          </div>"""
new = """          </div>"""
assert s.count(old) == 1
s = s.replace(old, new)

# 13. study rail: rename evidence-library card
old = """                  <span className="block text-[12px] font-semibold text-brand-deep">Evidence library</span>
                  <span className="mt-0.5 block text-[13px] font-medium text-navy-800 group-hover:text-brand-deep">
                    All case studies, indexed by industry &amp; service area
                  </span>"""
new = """                  <span className="block text-[12px] font-semibold text-brand-deep">All case studies</span>
                  <span className="mt-0.5 block text-[13px] font-medium text-navy-800 group-hover:text-brand-deep">
                    The full results library, filterable by industry and capability
                  </span>"""
assert s.count(old) == 1
s = s.replace(old, new)

# 14. "Browse the full index" button in study rail
s = s.replace("""                Browse the full index <ArrowRight className="h-3.5 w-3.5" aria-hidden="true" />""",
              """                All {cards.length + 1} engagements <ArrowRight className="h-3.5 w-3.5" aria-hidden="true" />""")

open(P, "w").write(s)
print("CaseStudies.tsx rewritten OK")
