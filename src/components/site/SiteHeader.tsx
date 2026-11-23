"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { ChevronDown, Menu, X, ArrowRight, Search } from "lucide-react";
import Logo from "./Logo";
import { SearchOverlay, SkipLink, AnnouncementBar, StickyMobileCTA } from "./Wave3";
import type { Brand, Nav } from "@/lib/content";

function MegaPanel({
  item,
  open,
  onCancelClose,
  onScheduleClose,
}: {
  item: Nav["primary"][number];
  open: boolean;
  onCancelClose: () => void;
  onScheduleClose: () => void;
}) {
  if (!item.mega) return null;
  const cols = item.mega.length;
  const gridCls =
    cols >= 12
      ? "grid-cols-6"
      : cols >= 8
        ? "grid-cols-4"
        : cols >= 4
          ? "grid-cols-4"
          : "grid-cols-3";
  return (
    /* Anchored to the full-width header bar (inset-x-0), NOT the nav item.
       A 100vw panel centered on a left-side trigger overflowed the viewport
       on both edges — the panel now spans exactly the viewport width and
       its content stays inside container-dq. */
    <div
      className={`absolute inset-x-0 top-full hidden xl:block ${open ? "" : "pointer-events-none"}`}
      style={{ visibility: open ? "visible" : "hidden" }}
      onMouseEnter={onCancelClose}
      onMouseLeave={onScheduleClose}
    >
      <div
        className={`mega-panel border-t border-line bg-white shadow-3 ${open ? "" : "mega-hidden"}`}
        role="region"
        aria-label={`${item.label} menu`}
      >
        <div className="container-dq py-8">
          <div className={`grid gap-x-8 gap-y-7 ${gridCls}`}>
            {item.mega.map((col) => (
              <div key={col.label + col.url}>
                <Link
                  href={col.url}
                  className="group flex items-center justify-between text-[13.5px] font-semibold text-navy-800 hover:text-brand-deep"
                  tabIndex={open ? 0 : -1}
                >
                  <span>{col.label}</span>
                  <ArrowRight className="h-3.5 w-3.5 text-brand transition group-hover:translate-x-0.5" />
                </Link>
                {col.children.length > 0 && (
                  <ul className="mt-2.5 space-y-1.5">
                    {col.children.slice(0, 8).map((ch) => (
                      <li key={ch.label + ch.url}>
                        <Link
                          href={ch.url}
                          className="block text-[12.5px] leading-snug text-slate-body/80 hover:text-navy-800"
                          tabIndex={open ? 0 : -1}
                        >
                          {ch.label}
                        </Link>
                      </li>
                    ))}
                    {col.children.length > 8 && (
                      <li className="text-[11.5px] font-medium text-brand-deep">
                        +{col.children.length - 8} more
                      </li>
                    )}
                  </ul>
                )}
              </div>
            ))}
            {/* featured context card (CHG-352): where to start, on every wide panel */}
            <div className="rounded-xl border border-brand/25 bg-brand-tint p-4">
              <p className="text-[10.5px] font-bold uppercase tracking-[0.14em] text-brand-deep">Not sure where to start?</p>
              <p className="mt-1.5 text-[12px] leading-relaxed text-slate-body/80">
                A 45-minute briefing maps your metric to the right entry point — no deck, no pitch.
              </p>
              <div className="mt-3 flex flex-wrap gap-2">
                <Link
                  href="/book-a-briefing/"
                  className="inline-flex items-center gap-1 rounded-lg bg-brand px-3 py-1.5 text-[11.5px] font-semibold text-white hover:bg-brand-hover"
                >
                  Book a briefing <ArrowRight className="h-3 w-3" aria-hidden="true" />
                </Link>
                <Link
                  href="/value-assessment/"
                  className="inline-flex items-center rounded-lg border border-line bg-white px-3 py-1.5 text-[11.5px] font-semibold text-navy-800 hover:border-brand"
                >
                  Value assessment
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function SiteHeader({ nav, brand }: { nav: Nav; brand: Brand }) {
  const [openItem, setOpenItem] = useState<string | null>(null);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [mobileSection, setMobileSection] = useState<string | null>(null);
  const [scrolled, setScrolled] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const closeTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const pathname = usePathname();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    // close menus after navigation (deferred to avoid cascading render)
    const t = setTimeout(() => {
      setOpenItem(null);
      setMobileOpen(false);
      setMobileSection(null);
    }, 0);
    return () => clearTimeout(t);
  }, [pathname]);

  const scheduleClose = useCallback(() => {
    closeTimer.current = setTimeout(() => setOpenItem(null), 140);
  }, []);
  const cancelClose = useCallback(() => {
    if (closeTimer.current) clearTimeout(closeTimer.current);
  }, []);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setOpenItem(null);
        setMobileOpen(false);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  return (
    <header className="sticky top-0 z-50">
      <SkipLink />
      {/* announcement bar (CHG-381) */}
      <AnnouncementBar message="The patented-intelligence library is now live — see the eight method families behind every delivery" href="/patented-intelligence/" />
      {/* utility bar — brand navy (CHG-010) */}
      <div className="bg-navy-900 text-white/70 text-[11.5px]">
        <div className="container-dq flex h-8 items-center justify-between">
          <p className="tracking-wide truncate">
            SOC 2 Type II · ISO 27001 · ISO 9001 · GDPR &amp; CCPA aligned · Zero-exposure delivery
          </p>
          <a href={`mailto:${brand.emails.general}`} className="hidden md:block hover:text-brand-300">
            {brand.emails.general}
          </a>
        </div>
      </div>

      {/* main bar — `relative` anchors the full-width megamenu below */}
      {/* main bar — `relative` anchors the full-width megamenu below */}
      <div
        className={`relative border-b border-line bg-white/95 backdrop-blur transition-shadow ${scrolled ? "shadow-2" : ""}`}
      >
        {/* scroll condense (CHG-357): main bar tightens after scroll */}
        <div
          className={`container-dq flex items-center justify-between gap-4 transition-[height] duration-300 ${scrolled ? "h-[52px]" : "h-16"}`}
        >
          <Link href="/" aria-label="Achala IT Solutions home" className="shrink-0">
            <Logo height={38} />
          </Link>

          {/* desktop nav — orange active marker + sliding underline (CHG-013/087).
              Desktop nav shows at ≥1280px (xl) only: below that the row cannot fit
              logo + 7 items + CTA without wrapping, so the drawer takes over. */}
          <nav aria-label="Primary" className="hidden xl:flex items-center gap-1">
            {nav.primary.map((item) => (
              <div
                key={item.label}
                className="relative"
                onMouseEnter={() => {
                  cancelClose();
                  setOpenItem(item.mega ? item.label : null);
                }}
                onMouseLeave={item.mega ? scheduleClose : undefined}
              >
                <div className="relative">
                  <Link
                    href={item.url}
                    data-active={pathname.startsWith(item.url)}
                    aria-current={pathname === item.url ? "page" : undefined}
                    onClick={(e) => {
                      // first tap/click opens the panel; second click navigates.
                      // Guarantees menu usability on touch devices and whenever
                      // hover fails (high-DPI Windows, Edge profiles, etc.).
                      if (item.mega && openItem !== item.label) {
                        e.preventDefault();
                        setOpenItem(item.label);
                      }
                    }}
                    className={`nav-link flex items-center gap-1 px-3 py-2 text-[13.5px] font-medium whitespace-nowrap rounded-md transition-colors ${
                      pathname.startsWith(item.url)
                        ? "text-brand-deep"
                        : "text-navy-800 hover:text-brand-deep"
                    }`}
                    aria-expanded={item.mega ? openItem === item.label : undefined}
                    onFocus={() => setOpenItem(item.mega ? item.label : null)}
                  >
                    {item.label}
                    {item.mega && <ChevronDown className="h-3.5 w-3.5 opacity-60" />}
                  </Link>
                </div>
                {item.mega && null /* panels render anchored to the header bar, below */}
              </div>
            ))}
          </nav>

          <div className="flex items-center gap-2.5">
            {/* header search entry (CHG-358) */}
            <button
              type="button"
              onClick={() => setSearchOpen(true)}
              aria-label="Search the site"
              className="inline-flex h-9 w-9 items-center justify-center rounded-[10px] border border-line text-navy-800 transition hover:border-brand hover:text-brand-deep"
            >
              <Search className="h-4 w-4" aria-hidden="true" />
            </button>
            {/* primary action: solid orange (CHG-012) with sheen (CHG-053) */}
            <Link
              href={nav.cta.url}
              className="btn-sheen hidden sm:inline-flex items-center rounded-[10px] bg-brand px-4 py-2 text-[13px] font-semibold text-white transition-colors hover:bg-brand-hover"
            >
              {nav.cta.label}
            </Link>
            <button
              className="xl:hidden inline-flex h-10 w-10 items-center justify-center rounded-[10px] border border-line"
              aria-label="Open menu"
              aria-expanded={mobileOpen}
              onClick={() => setMobileOpen((v) => !v)}
            >
              {mobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </button>
          </div>
        </div>

        {/* megamenu — one full-width panel per mega item, exactly viewport-wide */}
        {nav.primary
          .filter((item) => item.mega)
          .map((item) => (
            <MegaPanel
              key={item.label}
              item={item}
              open={openItem === item.label}
              onCancelClose={cancelClose}
              onScheduleClose={scheduleClose}
            />
          ))}
      </div>

      {/* mobile drawer — drawer-scroll caps height at the dynamic viewport
          (see .drawer-scroll in globals.css) so the CTA never slides under
          mobile browser toolbars */}
      {mobileOpen && (
        <div className="drawer-scroll xl:hidden border-b border-line bg-white shadow-3 overflow-y-auto">
          <div className="container-dq space-y-1 pt-4 pb-[calc(1rem+env(safe-area-inset-bottom))]">
            {nav.primary.map((item) => (
              <div key={item.label} className="border-b border-line/70 last:border-0">
                <div className="flex items-center justify-between">
                  <Link href={item.url} className="py-3 text-[15px] font-semibold text-navy-800">
                    {item.label}
                  </Link>
                  {item.mega && (
                    <button
                      aria-label={`Expand ${item.label}`}
                      aria-expanded={mobileSection === item.label}
                      className="h-9 w-9 inline-flex items-center justify-center rounded-[10px] hover:bg-mist"
                      onClick={() => setMobileSection(mobileSection === item.label ? null : item.label)}
                    >
                      <ChevronDown
                        className={`h-4 w-4 transition-transform ${mobileSection === item.label ? "rotate-180" : ""}`}
                      />
                    </button>
                  )}
                </div>
                {item.mega && mobileSection === item.label && (
                  <div className="pb-4 space-y-3">
                    {item.mega.map((col) => (
                      <div key={col.label + col.url}>
                        <Link href={col.url} className="text-[13px] font-semibold text-brand-deep">
                          {col.label}
                        </Link>
                        {col.children.length > 0 && (
                          <ul className="mt-1 space-y-1 pl-3">
                            {col.children.map((ch) => (
                              <li key={ch.label + ch.url}>
                                <Link href={ch.url} className="text-[12.5px] text-slate-body/80">
                                  {ch.label}
                                </Link>
                              </li>
                            ))}
                          </ul>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
            <Link
              href={nav.cta.url}
              className="mt-3 flex items-center justify-center rounded-[10px] bg-brand px-4 py-3 text-[14px] font-semibold text-white hover:bg-brand-hover"
            >
              {nav.cta.label}
            </Link>
          </div>
        </div>
      )}
      {/* sticky mobile CTA bar (CHG-362) */}
      <StickyMobileCTA cta={nav.cta} />

      {/* instant search overlay (CHG-359) */}
      {searchOpen && <SearchOverlay close={() => setSearchOpen(false)} />}
    </header>
  );
}
