"use client";

import { useEffect, useRef } from "react";
import { usePathname } from "next/navigation";

/* ── MotionRuntime v5 — route-aware scroll choreography ────────────────────
   ONE client component, mounted once in the root layout. Everything is
   decorative, pointer/reduced-motion aware, and CSS-driven.

   v5 fix (auto-load bug): the old runtime scanned the DOM exactly once per
   full page load. Inside the App Router the layout never remounts, so after
   a client-side <Link> navigation the NEW page's sections, chart cards and
   figures were never observed — they stayed at opacity:0 until the visitor
   manually refreshed. v5 keeps one long-lived IntersectionObserver and
   re-scans on: (1) every route change, (2) any DOM mutation anywhere (lazy
   charts, deferred client components), and (3) bfcache restores.

   What it does:
   1.  Scroll choreography — sections, [data-reveal], cards, figures get
       .is-inview once; stagger children get capped --i variables (max 8).
   2.  Word-split headline masks — [data-split] headlines animate per word.
   3.  Header state — .is-scrolled after 24px (CSS drives shrink/blur).
   4.  Marquee auto-pause — marquees stop when off-screen (perf).
   5.  CTA click ripple — small, purposeful press feedback.                */

export default function MotionRuntime() {
  const pathname = usePathname();
  const scanRef = useRef<() => void>(() => {});

  useEffect(() => {
    try {
      const reduced =
        window.matchMedia?.("(prefers-reduced-motion: reduce)").matches ?? false;
      const root = document.documentElement;
      root.classList.add("js-motion-v3");
      if (reduced) root.classList.add("js-motion-off");

      const FORCE_VISIBLE =
        "main section, main [data-reveal], main .dv-card, main figure.pi-figure, [data-stagger], .wipe-section, .vignette-section, .quote-fade, .stat-flip";

      /* ── one long-lived IO, shared across every scan/route change ───── */
      let io: IntersectionObserver | null = null;
      if (!reduced && "IntersectionObserver" in window) {
        io = new IntersectionObserver(
          (entries) => {
            for (const e of entries) {
              if (!e.isIntersecting) continue;
              (e.target as HTMLElement).classList.add("is-inview");
              io?.unobserve(e.target);
            }
          },
          // fire early: 0.04 threshold + small bottom margin, so content is
          // already readable when it enters the viewport (no mid-fade scans)
          { threshold: 0.04, rootMargin: "0px 0px -4% 0px" },
        );
      }

      const staggers = new WeakSet<HTMLElement>();
      const indexChildren = (el: HTMLElement) => {
        if (staggers.has(el)) return;
        staggers.add(el);
        const kids = el.children;
        for (let i = 0; i < kids.length; i++) {
          (kids[i] as HTMLElement).style.setProperty("--i", String(Math.min(i, 8)));
        }
      };

      const splitHeadline = (el: HTMLElement) => {
        if (reduced) {
          el.setAttribute("data-split-done", "1");
          return;
        }
        el.setAttribute("data-split-done", "1");
        const text = el.textContent || "";
        const words = text.split(/\s+/).filter(Boolean);
        if (words.length === 0 || words.length > 14) return;
        el.setAttribute("aria-label", text);
        el.textContent = "";
        words.forEach((w, i) => {
          const outer = document.createElement("span");
          outer.className = "split-word";
          outer.style.setProperty("--i", String(i));
          outer.setAttribute("aria-hidden", "true");
          const inner = document.createElement("span");
          inner.className = "split-word-inner";
          inner.textContent = w;
          outer.appendChild(inner);
          el.appendChild(outer);
          if (i < words.length - 1) el.appendChild(document.createTextNode(" "));
        });
        io?.observe(el);
      };

      /* ── the scan — idempotent, safe to run on every route change ────── */
      const scan = () => {
        document
          .querySelectorAll<HTMLElement>(
            [
              "main section:not(.reveal):not([data-motion-done])",
              "main [data-reveal]:not([data-motion-done])",
              "main .dv-card:not([data-motion-done])",
              "main figure.pi-figure:not([data-motion-done])",
              "main [data-stagger]:not([data-motion-done])",
              "main .mq-stagger:not([data-motion-done])",
              "main .wipe-section:not([data-motion-done])",
              "main .vignette-section:not([data-motion-done])",
              "main .quote-fade:not([data-motion-done])",
              "main .stat-flip:not([data-motion-done])",
            ].join(", "),
          )
          .forEach((el) => {
            el.setAttribute("data-motion-done", "1");
            if (el.hasAttribute("data-stagger") || el.classList.contains("mq-stagger")) {
              indexChildren(el);
            }
            if (io) io.observe(el);
            else el.classList.add("is-inview");
          });
        document
          .querySelectorAll<HTMLElement>("main [data-split]:not([data-split-done])")
          .forEach(splitHeadline);
        document
          .querySelectorAll<HTMLElement>(".marquee:not([data-mq-done])")
          .forEach((m) => {
            m.setAttribute("data-mq-done", "1");
            mqIo.observe(m);
          });
      };
      scanRef.current = scan;

      /* ── 4. marquee auto-pause (own IO, also route-aware) ────────────── */
      const mqIo = new IntersectionObserver(
        (entries) => {
          for (const e of entries) {
            (e.target as HTMLElement).classList.toggle("mq-live", e.isIntersecting);
          }
        },
        { threshold: 0 },
      );

      /* ── MutationObserver: catch ANY new content — route changes, lazy
         charts hydrating late, deferred client components — debounced to
         one scan per animation frame.                                  */
      let raf = 0;
      const mo = new MutationObserver(() => {
        if (raf) return;
        raf = requestAnimationFrame(() => {
          raf = 0;
          scan();
        });
      });
      mo.observe(document.body, { childList: true, subtree: true });

      /* first scan + a couple of late passes for pre-hydration content */
      scan();
      const t1 = window.setTimeout(scan, 400);
      const t2 = window.setTimeout(scan, 1200);

      /* ── 3. header state + scroll progress var ─────────────────────── */
      let scrollRaf = 0;
      const header = document.querySelector("header");
      const onScroll = () => {
        if (scrollRaf) return;
        scrollRaf = requestAnimationFrame(() => {
          scrollRaf = 0;
          const y = window.scrollY;
          if (header) header.classList.toggle("is-scrolled", y > 24);
          const max = document.documentElement.scrollHeight - window.innerHeight;
          const p = max > 0 ? Math.min(1, y / max) : 0;
          root.style.setProperty("--scroll-p", p.toFixed(4));
        });
      };
      window.addEventListener("scroll", onScroll, { passive: true });
      onScroll();

      /* bfcache restore (back/forward): observers died with the page —
         re-scan everything so nothing stays hidden */
      const onPageShow = (ev: PageTransitionEvent) => {
        if (ev.persisted) scan();
      };
      window.addEventListener("pageshow", onPageShow);

      /* ── 5. ripple on CTA click (press feedback only, no pull) ─────── */
      const onClick = (ev: MouseEvent) => {
        const el = (ev.target as Element | null)?.closest?.("a.btn-sheen, button.btn-sheen") as HTMLElement | null;
        if (!el) return;
        const r = el.getBoundingClientRect();
        const rip = document.createElement("span");
        rip.className = "dq-ripple";
        rip.style.left = `${ev.clientX - r.left}px`;
        rip.style.top = `${ev.clientY - r.top}px`;
        el.appendChild(rip);
        window.setTimeout(() => rip.remove(), 650);
      };
      window.addEventListener("click", onClick, { passive: true });

      return () => {
        window.clearTimeout(t1);
        window.clearTimeout(t2);
        if (raf) cancelAnimationFrame(raf);
        mo.disconnect();
        io?.disconnect();
        mqIo.disconnect();
        window.removeEventListener("scroll", onScroll);
        window.removeEventListener("pageshow", onPageShow);
        window.removeEventListener("click", onClick);
        if (scrollRaf) cancelAnimationFrame(scrollRaf);
      };
    } catch {
      /* motion is decorative — never block the page: force everything visible */
      try {
        document
          .querySelectorAll<HTMLElement>(
            "main section, main [data-reveal], main .dv-card, main figure.pi-figure, [data-stagger], .wipe-section, .vignette-section, .quote-fade, .stat-flip, .dq-hero > *",
          )
          .forEach((el) => {
            el.classList.add("is-inview");
            el.style.opacity = "1";
            el.style.transform = "none";
            el.style.clipPath = "none";
          });
      } catch {
        /* give up silently */
      }
    }
  }, []);

  /* route change: new page content must be observed the moment it mounts.
     The MutationObserver usually catches it; this is the belt-and-braces
     pass that also re-runs after the page settles.                      */
  useEffect(() => {
    const a = requestAnimationFrame(() => scanRef.current());
    const b = window.setTimeout(() => scanRef.current(), 260);
    return () => {
      cancelAnimationFrame(a);
      window.clearTimeout(b);
    };
  }, [pathname]);

  return null;
}
