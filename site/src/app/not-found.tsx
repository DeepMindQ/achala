import Link from "next/link";
import { ArrowRight, Search } from "lucide-react";
import Logo from "@/components/site/Logo";

/* Branded animated 404 (Wave 1 CHG-030 + Wave 2 CHG-162 + BG-020):
   brand line, search box, top-8 destination links, closing CTA — no dead ends. */
export default function NotFound() {
  const top8 = [
    { label: "Services — eight expertise domains", url: "/services/" },
    { label: "Industries — twelve sectors", url: "/industries/" },
    { label: "Platforms in production", url: "/platforms/" },
    { label: "Case studies & evidence", url: "/case-studies/" },
    { label: "Patented intelligence", url: "/patented-intelligence/" },
    { label: "Insights library", url: "/insights/" },
    { label: "About Achala IT Solutions", url: "/about-us/" },
    { label: "Contact & briefings", url: "/contact/" },
  ];
  return (
    <section className="relative overflow-hidden grad-navy-field text-white">
      <div className="bg-field-drift absolute inset-0 dot-grid" aria-hidden="true" />
      <div className="absolute inset-0 grad-orange-glow" aria-hidden="true" />
      <div className="relative container-dq py-16 text-center sm:py-20">
        <Logo variant="reversed" height={30} className="mx-auto" />
        <p className="animate-float mt-8 font-display text-[72px] font-bold leading-none text-brand sm:text-[88px]">404</p>
        <h1 className="mt-4 text-display-3 text-white">This page drifted outside the grid.</h1>
        <p className="mx-auto mt-3 max-w-lg text-[14px] text-white/65">
          The URL may have moved in our relaunch. Search the site or start with the most
          visited destinations below — everything is four clicks from home.
        </p>

        {/* search box (static export: routes to the pagefind-powered search page) */}
        <form action="/search/" method="get" className="mx-auto mt-8 flex max-w-md items-center gap-2 rounded-xl border border-white/20 bg-white/[0.06] px-4 py-2.5 backdrop-blur">
          <Search className="h-4 w-4 shrink-0 text-brand-300" aria-hidden="true" />
          <input
            type="search"
            name="q"
            placeholder="Search services, industries, insights…"
            aria-label="Search the site"
            className="min-w-0 flex-1 bg-transparent text-[13.5px] text-white placeholder:text-white/40 focus:outline-none"
          />
          <button
            type="submit"
            className="shrink-0 rounded-lg bg-brand px-3.5 py-1.5 text-[12px] font-semibold text-white transition hover:bg-brand-hover"
          >
            Search
          </button>
        </form>

        {/* top-8 destinations */}
        <div className="mx-auto mt-8 grid max-w-3xl gap-2.5 text-left sm:grid-cols-2">
          {top8.map((l) => (
            <Link
              key={l.url}
              href={l.url}
              className="group flex items-center justify-between gap-3 rounded-xl border border-white/15 bg-white/[0.04] px-4 py-3 text-[13px] font-medium text-white/85 transition hover:border-brand-300/60 hover:bg-white/[0.08] hover:text-white"
            >
              {l.label}
              <ArrowRight className="h-3.5 w-3.5 shrink-0 text-brand-300 transition group-hover:translate-x-0.5" aria-hidden="true" />
            </Link>
          ))}
        </div>

        {/* closing CTA */}
        <div className="mt-10">
          <Link
            href="/book-a-briefing/"
            className="btn-sheen inline-flex items-center gap-2 rounded-[10px] bg-brand px-6 py-3 text-[14px] font-semibold text-white transition hover:bg-brand-hover"
          >
            Book an executive briefing <ArrowRight className="h-4 w-4" aria-hidden="true" />
          </Link>
          <p className="mt-3 text-[11.5px] text-white/45">
            45 minutes with a practice lead — your metric, our pattern library, three reference engagements.
          </p>
        </div>
      </div>
    </section>
  );
}
