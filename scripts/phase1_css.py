#!/usr/bin/env python3
"""Phase 1: globals.css motion retune + editorial article system.
Each replacement asserts exactly one occurrence before applying."""
import re, sys

P = "/home/z/my-project/site/src/app/globals.css"
s = open(P, encoding="utf-8").read()
applied = []

def rep(old, new, label):
    global s
    n = s.count(old)
    if n == 0:
        if new and new in s:
            applied.append(f"{label} (already)")
            return
        print(f"FAIL [{label}]: not found"); sys.exit(1)
    if n != 1:
        print(f"FAIL [{label}]: {n} occurrences"); sys.exit(1)
    s = s.replace(old, new)
    applied.append(label)

# 1. reveal base — faster + smaller distance
rep(""".reveal {
  opacity: 0;
  transform: translateY(14px);""",
""".reveal {
  opacity: 0;
  transform: translateY(12px);""", "reveal-base")

# 2. mega preview animation (after the 100dvh mega-panel block)
old_mega = """@supports (height: 100dvh) {
  .mega-panel {
    max-height: calc(100dvh - 6rem);
  }
}"""
new_mega = old_mega + """

/* preview pane: fades up when the rail switches group (remount-keyed) */
@keyframes mega-preview-in {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: none; }
}
.mega-preview-in {
  animation: mega-preview-in 0.22s var(--ease-out-expo) both;
}
@media (prefers-reduced-motion: reduce) {
  .mega-preview-in { animation: none; }
}"""
rep(old_mega, new_mega, "mega-preview")

# 3. section cascade retune
rep(""".js-motion main section > * {
  opacity: 0;
  transform: translateY(26px);
  transition:
    opacity 0.8s var(--dq-ease),
    transform 0.8s var(--dq-ease);
  will-change: opacity, transform;
}""",
""".js-motion main section > * {
  opacity: 0;
  transform: translateY(14px);
  transition:
    opacity 0.5s var(--dq-ease),
    transform 0.5s var(--dq-ease);
  will-change: opacity, transform;
}""", "section-cascade")

rep(""".js-motion main section.is-inview > *:nth-child(2) { transition-delay: 70ms; }
.js-motion main section.is-inview > *:nth-child(3) { transition-delay: 140ms; }
.js-motion main section.is-inview > *:nth-child(4) { transition-delay: 210ms; }
.js-motion main section.is-inview > *:nth-child(5) { transition-delay: 280ms; }
.js-motion main section.is-inview > *:nth-child(n + 6) { transition-delay: 340ms; }""",
""".js-motion main section.is-inview > *:nth-child(2) { transition-delay: 45ms; }
.js-motion main section.is-inview > *:nth-child(3) { transition-delay: 90ms; }
.js-motion main section.is-inview > *:nth-child(4) { transition-delay: 135ms; }
.js-motion main section.is-inview > *:nth-child(5) { transition-delay: 180ms; }
.js-motion main section.is-inview > *:nth-child(n + 6) { transition-delay: 220ms; }""", "cascade-delays")

# 4. data-reveal retune
rep(""".js-motion main [data-reveal] {
  opacity: 0;
  transform: translateY(24px);
  transition:
    opacity 0.7s var(--dq-ease),
    transform 0.7s var(--dq-ease);
}
.js-motion main [data-reveal="left"] { transform: translateX(-30px); }
.js-motion main [data-reveal="right"] { transform: translateX(30px); }
.js-motion main [data-reveal="zoom"] { transform: scale(0.94); }""",
""".js-motion main [data-reveal] {
  opacity: 0;
  transform: translateY(14px);
  transition:
    opacity 0.5s var(--dq-ease),
    transform 0.5s var(--dq-ease);
}
.js-motion main [data-reveal="left"] { transform: translateX(-18px); }
.js-motion main [data-reveal="right"] { transform: translateX(18px); }
.js-motion main [data-reveal="zoom"] { transform: scale(0.975); }""", "data-reveal")

# 5. dv-card retune
rep(""".js-motion main .dv-card {
  opacity: 0;
  transform: translateY(30px) scale(0.985);
  transition:
    opacity 0.75s var(--dq-ease),
    transform 0.75s var(--dq-ease);
  transition-delay: 120ms;
}""",
""".js-motion main .dv-card {
  opacity: 0;
  transform: translateY(16px);
  transition:
    opacity 0.55s var(--dq-ease),
    transform 0.55s var(--dq-ease);
  transition-delay: 60ms;
}""", "dv-card")

# 6. wave-4 motion tokens
rep("""  --dur-1: 0.28s;
  --dur-2: 0.55s;
  --dur-3: 0.8s;
  --stagger-step: 70ms;
}""",
"""  --dur-1: 0.18s;
  --dur-2: 0.3s;
  --dur-3: 0.5s;
  --stagger-step: 40ms;
}""", "motion-tokens")

# 7. hero cascade
rep("""@keyframes dq-hero-item {
  from { opacity: 0; transform: translateY(22px); }
  to { opacity: 1; transform: none; }
}
.dq-hero > * {
  animation: dq-hero-item 0.9s var(--ease-out-expo) both;
  animation-delay: calc(var(--i, 0) * 90ms + 80ms);
}""",
"""@keyframes dq-hero-item {
  from { opacity: 0; transform: translateY(14px); }
  to { opacity: 1; transform: none; }
}
.dq-hero > * {
  animation: dq-hero-item 0.65s var(--ease-out-expo) both;
  animation-delay: calc(var(--i, 0) * 55ms + 60ms);
}""", "hero-cascade")

# 8. split-word retune
rep(""".js-motion-v3 main [data-split] .split-word-inner {
  display: inline-block;
  transform: translateY(110%) rotate(4deg);
  opacity: 0;
  transition:
    transform 0.85s var(--ease-out-expo),
    opacity 0.6s ease-out;
  transition-delay: calc(var(--i, 0) * 55ms + 120ms);
  will-change: transform, opacity;
}""",
""".js-motion-v3 main [data-split] .split-word-inner {
  display: inline-block;
  transform: translateY(110%) rotate(2deg);
  opacity: 0;
  transition:
    transform 0.6s var(--ease-out-expo),
    opacity 0.45s ease-out;
  transition-delay: calc(var(--i, 0) * 36ms + 90ms);
  will-change: transform, opacity;
}""", "split-word")

# 9. stagger engine retune
rep(""".js-motion-v3 main [data-stagger] > * {
  opacity: 0;
  transform: translateY(24px);
  transition:
    opacity 0.7s var(--ease-out-expo),
    transform 0.7s var(--ease-spring);
  transition-delay: calc(var(--i, 0) * var(--stagger-step));
}""",
""".js-motion-v3 main [data-stagger] > * {
  opacity: 0;
  transform: translateY(14px);
  transition:
    opacity 0.45s var(--ease-out-expo),
    transform 0.45s var(--ease-out-expo);
  transition-delay: calc(var(--i, 0) * var(--stagger-step));
}""", "stagger-engine")

# 10. tilt-card removal (keep class as neutral hook)
m = re.search(r"/\* ── card lift \+ tilt \+ glare[^\n]*\*/\n\.tilt-card \{.*?\n\}\n\.tilt-card:hover \{[^}]*\}\n", s, re.S)
if not m:
    print("FAIL: tilt block regex"); sys.exit(1)
s = s[:m.start()] + """/* ── cards: calm lift only (Phase 1 removed 3D tilt + pointer glare) ─── */
.tilt-card {
  position: relative;
}
""" + s[m.end():]
applied.append("tilt-removed")

# 11. pi-figure retime
rep("""  transform: scale(0.985);
  transition:
    opacity 0.9s var(--ease-out-expo),
    clip-path 1.1s var(--ease-swift),
    transform 0.9s var(--ease-out-expo);
}""",
"""  transform: scale(0.99);
  transition:
    opacity 0.6s var(--ease-out-expo),
    clip-path 0.8s var(--ease-swift),
    transform 0.6s var(--ease-out-expo);
}""", "pi-figure")

# 12. magnetic transition removal
rep(""".btn-sheen, a.btn-sheen {
  transition:
    transform 0.35s var(--dq-ease),
    box-shadow 0.35s var(--dq-ease),
    background-color 0.3s ease;
}""",
""".btn-sheen, a.btn-sheen {
  transition:
    box-shadow 0.3s var(--dq-ease),
    background-color 0.3s ease;
}""", "magnetic-removed")

# 13. cursor glow removal
m = re.search(r"/\* cursor spotlight \(pointer-only, set by MotionRuntime\) \*/\n#dq-cursor-glow \{.*?\n\}\n@media \(hover: none\) \{\n  #dq-cursor-glow \{ display: none; \}\n\}\n", s, re.S)
if not m:
    print("FAIL: cursor glow regex"); sys.exit(1)
s = s[:m.start()] + """/* (cursor spotlight removed in Phase 1 — decorative glow competed with
   content and cost a rAF loop on every pointer move) */
""" + s[m.end():]
applied.append("glow-removed")

# 14. glow-hot removal
rep("""/* ── spotlight v2: expands over interactive elements ───────────────────── */
#dq-cursor-glow.glow-hot {
  background: radial-gradient(circle, rgba(210, 0, 0, 0.16), rgba(210, 0, 0, 0.06) 45%, transparent 70%);
}""",
"""/* (spotlight hot state removed in Phase 1) */""", "glow-hot")

# 15. quote fade retune
rep("""  opacity: 0;
  transform: translateY(14px);
  transition: opacity 0.8s var(--ease-out-expo), transform 0.8s var(--ease-out-expo);
}""",
"""  opacity: 0;
  transform: translateY(12px);
  transition: opacity 0.55s var(--ease-out-expo), transform 0.55s var(--ease-out-expo);
}""", "quote-fade")

# 16. kill-switch cleanup + editorial article system appended
rep("""  .tilt-card,
  .tilt-card::before {
    transform: none !important;
    opacity: 0 !important;
  }""",
"""  .tilt-card,
  .tilt-card::before {
    transform: none !important;
  }""", "killswitch-tilt")

rep("""  .count-live { transform: none; }
  [data-parallax] { transform: none !important; }
  #dq-cursor-glow { display: none !important; }
  .js-motion-v3 .marquee:not(.mq-live) .marquee-inner {
    animation-play-state: running;
  }
}""",
"""  .count-live { transform: none; }
  .js-motion-v3 .marquee:not(.mq-live) .marquee-inner {
    animation-play-state: running;
  }
}

/* ═══════════ Phase 1 editorial article system ═══════════════════════════
   One centered article column replaces the old prose + TOC-rail split.
   Sections carry a leading orange index (01, 02, …) for orientation —
   the wayfinding job the removed "On this page" rail used to do.         */
.dq-article {
  counter-reset: dq-h2;
}
.dq-article .dq-h2 {
  counter-increment: dq-h2;
}
.dq-article .dq-h2::before {
  content: counter(dq-h2, decimal-leading-zero);
  flex: none;
  font-family: var(--font-display);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--color-brand);
  transform: translateY(-0.18em);
}
.dq-article .dq-h2::after {
  content: "";
  flex: 1 1 auto;
  height: 1px;
  align-self: center;
  margin-left: 4px;
  background: linear-gradient(90deg, var(--color-line), transparent);
  opacity: 0.9;
}
@media (max-width: 640px) {
  .dq-article .dq-h2::after { display: none; }
}""", "article-system")

# 17. remove dead [data-parallax] base rule
rep("""/* ── parallax layers (transform set by runtime; base state safe) ───────── */
[data-parallax] {
  will-change: transform;
}

""",
"", "parallax-base")

open(P, "w", encoding="utf-8").write(s)
print("APPLIED:", len(applied))
for a in applied: print("  +", a)
