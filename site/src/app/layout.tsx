import type { Metadata, Viewport } from "next";
import { Sora, Inter } from "next/font/google";
import "./globals.css";
import { Toaster } from "@/components/ui/toaster";
import SiteHeader from "@/components/site/SiteHeader";
import SiteFooter from "@/components/site/SiteFooter";
import CookieConsent from "@/components/site/CookieConsent";
import { ScrollProgress, BackToTop } from "@/components/site/Motion";
import MotionRuntime from "@/components/site/MotionRuntime";
import { brandData, navData } from "@/lib/content";
import { BP } from "@/lib/bp";

/* Self-hosted variable fonts with preload + display swap (Wave 1, CHG-099). */
const sora = Sora({
  subsets: ["latin"],
  variable: "--font-sora",
  display: "swap",
  weight: "variable",
});
const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
  weight: "variable",
});

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || "https://www.achalasolutions.com"),
  title: {
    default: "Achala IT Solutions | Enterprise AI solutions, platforms & engineering services",
    template: "%s",
  },
  description:
    "Achala IT Solutions builds AI-first platforms and engineering services that take enterprise programs from proof of concept to production. ISO/IEC 27001 certified, TISAX-audited, GDPR-aligned — with delivery teams in India, Germany and Bulgaria.",
  robots: { index: true, follow: true },
  /* Browser-fetched same-origin assets get the base path (gh-pages preview);
   * og:image stays metadataBase-resolved (production domain, crawler-side). */
  manifest: `${BP}/manifest.json`,
  icons: {
    icon: [
      { url: `${BP}/icon.svg`, type: "image/svg+xml" },
      { url: `${BP}/favicon.ico`, sizes: "48x48", type: "image/x-icon" },
    ],
    apple: [{ url: `${BP}/apple-touch-icon.png`, sizes: "180x180" }],
  },
  openGraph: {
    type: "website",
    siteName: "Achala IT Solutions",
    images: [{ url: "/og-default.png", width: 1200, height: 630, alt: "Achala IT Solutions — Transforming industries through AI acceleration." }],
  },
  twitter: {
    card: "summary_large_image",
    images: ["/og-default.png"],
  },
};

/* Mobile browser chrome carries the brand (CHG-006 / CHG-039). */
export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#2b5672" },
    { media: "(prefers-color-scheme: dark)", color: "#0e2230" },
  ],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const brand = brandData();
  const { nav, footer } = navData();
  const orgJsonLd = {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: brand.legalName,
    alternateName: brand.name,
    url: brand.site,
    logo: `${brand.site}/logo.svg`,
    slogan: brand.tagline,
    description: brand.positioning,
    email: brand.emails.general,
    // Social profiles from achalasolutions.com
    sameAs: [
      "https://www.linkedin.com/company/achala-it-solutions-pvt-ltd/",
      "https://twitter.com/AchalaIt",
      "https://www.facebook.com/Achala-it-Solutions-Pvt-Ltd-2009-100557234648701/",
      "https://www.instagram.com/achala_itsolutions/",
    ],
    address: brand.offices.map((o) => ({
      "@type": "PostalAddress",
      addressLocality: o.city,
    })),
  };
  const siteJsonLd = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: brand.name,
    url: brand.site,
    potentialAction: {
      "@type": "SearchAction",
      target: `${brand.site}/search?q={search_term_string}`,
      "query-input": "required name=search_term_string",
    },
  };
  return (
    <html lang="en" className={`${sora.variable} ${inter.variable}`}>
      <body className="min-h-screen flex flex-col bg-white antialiased">
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(orgJsonLd) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(siteJsonLd) }}
        />
        {/* Paint-time flag: all scroll choreography is scoped under .js-motion,
            so content stays fully visible when JS is unavailable. */}
        <script
          dangerouslySetInnerHTML={{
            __html: "try{document.documentElement.classList.add('js-motion')}catch(e){}",
          }}
        />
        <SiteHeader nav={nav} brand={brand} />
        <MotionRuntime />
        <ScrollProgress />
        <main id="main-content" className="flex-1">{children}</main>
        <SiteFooter brand={brand} footer={footer} />
        <BackToTop />
        <CookieConsent />
        <Toaster />
      </body>
    </html>
  );
}
