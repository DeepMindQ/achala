import Link from "next/link";
import { Mail, MapPin, ShieldCheck, Linkedin, Twitter, Facebook, Instagram, Rss } from "lucide-react";
import Logo from "./Logo";
import { BP } from "@/lib/bp";
import Reveal from "./Reveal";
import ContactForm from "./ContactForm";
import NewsletterForm from "./NewsletterForm";
import type { Brand, FooterCol } from "@/lib/content";

export default function SiteFooter({ brand, footer }: { brand: Brand; footer: FooterCol[] }) {
  return (
    <footer className="mt-auto grad-navy-field text-white">
      {/* contact band */}
      <div className="border-b border-white/10 dot-grid">
        <div className="container-dq grid gap-10 py-14 lg:grid-cols-2">
          <div>
            <p className="kicker-bar-dark text-[12px] font-semibold uppercase tracking-[0.18em] text-brand-300">
              Contact Achala IT Solutions
            </p>
            <h2 className="mt-2 font-display text-2xl font-semibold leading-snug text-white sm:text-3xl">
              Tell us the outcome you need to move.
            </h2>
            <p className="mt-3 max-w-md text-[14px] leading-relaxed text-white/65">
              A practice lead — not a call center — responds within one business day with the
              relevant domain pod and three reference engagements. {brand.promise}
            </p>
            <div className="mt-6 space-y-2.5 text-[13px] text-white/75">
              <p className="flex flex-wrap items-center gap-x-2 gap-y-1">
                <Mail className="h-4 w-4 shrink-0 text-brand-300" />
                <a href={`mailto:${brand.emails.general}`} className="hover:text-brand-300">
                  {brand.emails.general}
                </a>
                <span className="text-white/30">·</span>
                <a href={`mailto:${brand.emails.press}`} className="hover:text-brand-300">
                  {brand.emails.press}
                </a>
                <span className="text-white/30">·</span>
                <a href={`mailto:${brand.emails.careers}`} className="hover:text-brand-300">
                  {brand.emails.careers}
                </a>
              </p>
              <p className="flex items-start gap-2">
                <MapPin className="mt-0.5 h-4 w-4 shrink-0 text-brand-300" />
                <span>
                  {brand.offices.map((o) => o.city.split(",")[0]).join(" · ")} — global delivery from India, Germany and Bulgaria
                </span>
              </p>
            </div>
            <div className="mt-6 flex flex-wrap gap-2">
              {brand.credentials.map((c) => (
                <span
                  key={c}
                  className="inline-flex max-w-full items-center gap-1.5 rounded-full border border-white/15 bg-white/5 px-3 py-1 text-[11px] text-white/70"
                >
                  <ShieldCheck className="h-3 w-3 text-brand-300" />
                  {c}
                </span>
              ))}
            </div>
          </div>
          <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-6 backdrop-blur">
            <ContactForm />
          </div>
        </div>
      </div>

      {/* link columns + newsletter — staggered reveal (CHG-143) */}
      <div className="container-dq py-12">
        <Reveal className="footer-stagger">
          <div className="grid gap-8 md:grid-cols-3 lg:grid-cols-5">
          {footer.map((col) => (
            <div key={col.title}>
              <p className="text-[12px] font-semibold uppercase tracking-[0.16em] text-white/50">
                {col.title}
              </p>
              <ul className="mt-3 space-y-2">
                {col.links.map((l) => (
                  <li key={l.label + l.url}>
                    <Link href={l.url} className="text-[13px] text-white/70 hover:text-brand-300">
                      {l.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
          <div>
            <p className="text-[12px] font-semibold uppercase tracking-[0.16em] text-white/50">
              The Delivery Floor — monthly
            </p>
            <p className="mt-1 text-[11.5px] leading-snug text-white/45">
              One email a month. The delivery-floor thesis and the vendor questions.
            </p>
            <div className="mt-3">
              <NewsletterForm />
            </div>
          </div>
          </div>
        </Reveal>
      </div>

      {/* legal bar — reversed lockup on navy (CHG-003/025) */}
      <div className="border-t border-white/10">
        <div className="container-dq flex flex-col gap-4 py-6 md:flex-row md:items-center md:justify-between">
          <div className="flex flex-col gap-3 md:flex-row md:items-center md:gap-6">
            <Logo variant="reversed" height={34} />
            <nav aria-label="Legal" className="flex flex-wrap gap-x-4 gap-y-1 text-[12px] text-white/55">
              <Link href="/privacy-policy/" className="hover:text-brand-300">
                Privacy Policy
              </Link>
              <Link href="/terms-of-use/" className="hover:text-brand-300">
                Terms of Use
              </Link>
              <Link href="/cookie-policy/" className="hover:text-brand-300">
                Cookie Policy
              </Link>
              <Link href="/accessibility/" className="hover:text-brand-300">
                Accessibility
              </Link>
              <Link href="/html-sitemap/" className="hover:text-brand-300">
                Sitemap
              </Link>
</nav>
          </div>
          <div className="flex flex-col gap-3 md:items-end">
            {/* Social row (CHG-077): wire hrefs to the real profiles when public */}
            <div className="flex items-center gap-2" aria-label="Social profiles">
              {[
                { icon: Linkedin, label: "LinkedIn", href: "https://www.linkedin.com/company/achala-it-solutions-pvt-ltd/" },
                { icon: Twitter, label: "X (Twitter)", href: "https://twitter.com/AchalaIt" },
                { icon: Facebook, label: "Facebook", href: "https://www.facebook.com/Achala-it-Solutions-Pvt-Ltd-2009-100557234648701/" },
                { icon: Instagram, label: "Instagram", href: "https://www.instagram.com/achala_itsolutions/" },
                { icon: Rss, label: "RSS", href: `${BP}/insights/` },
              ].map(({ icon: Icon, label, href }) => (
                <a
                  key={label}
                  href={href}
                  aria-label={label}
                  title={label}
                  className="inline-flex h-8 w-8 items-center justify-center rounded-full border border-white/15 text-white/60 transition hover:border-brand hover:text-brand-300"
                >
                  <Icon className="h-3.5 w-3.5" />
                </a>
              ))}
            </div>
            <p className="text-[12px] text-white/45">
              © {new Date().getFullYear()} {brand.legalName}. ISO/IEC 27001 · TISAX · GDPR-aligned delivery.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}
