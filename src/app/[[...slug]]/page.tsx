import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { ContentPage } from "@/components/site/PagePieces";
import HomeView from "@/components/site/HomeView";
import { brandData, fileForUrl, pageIndex, readPage, urlToSlugSegments, type PageData } from "@/lib/content";

export const dynamicParams = false;

export function generateStaticParams(): { slug: string[] }[] {
  return pageIndex().map((r) => ({ slug: urlToSlugSegments(r.url) }));
}

const HOME_META: Metadata = {
  title: "Achala IT Solutions | IT Services & Consulting for the Intelligence Era",
  description:
    "Achala IT Solutions engineers the intelligence layer of the enterprise — applied AI, agentic automation, data platforms, cybersecurity and emerging compute with outcome-linked engagements.",
  alternates: { canonical: "/" },
};

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug?: string[] }>;
}): Promise<Metadata> {
  const { slug = [] } = await params;
  if (slug.length === 0) return HOME_META;
  const url = "/" + slug.join("/") + "/";
  const rows = pageIndex();
  const row = rows.find((r) => r.url === url);
  if (!row) return {};
  const brand = brandData();
  const title = row.seoTitle || row.title;
  const description = row.metaDescription || brand.positioning;
  return {
    title,
    description,
    alternates: { canonical: url },
    openGraph: {
      title,
      description,
      url,
      siteName: brand.name,
      type: "website",
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
    },
  };
}

function breadcrumbJsonLd(page: PageData) {
  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: page.crumbs.map((c, i) => ({
      "@type": "ListItem",
      position: i + 1,
      name: c.name,
      ...(c.url ? { item: brandData().site + c.url } : {}),
    })),
  };
}

function pageJsonLd(page: PageData): object | null {
  const brand = brandData();
  const base = { "@context": "https://schema.org" };
  switch (page.template) {
    case "service_page":
    case "tower_hub":
      return {
        ...base,
        "@type": "Service",
        name: page.title,
        description: page.meta_description,
        provider: { "@type": "Organization", name: brand.legalName, url: brand.site },
        url: brand.site + page.url,
      };
    case "case_study":
    case "insight_article":
      return {
        ...base,
        "@type": "Article",
        headline: page.title,
        description: page.meta_description,
        author: { "@type": "Organization", name: brand.name },
        publisher: { "@type": "Organization", name: brand.legalName },
        url: brand.site + page.url,
      };
    case "newsroom_article":
      return {
        ...base,
        "@type": "NewsArticle",
        headline: page.title,
        description: page.meta_description,
        datePublished: page.published,
        author: { "@type": "Organization", name: brand.name },
        publisher: { "@type": "Organization", name: brand.legalName },
        url: brand.site + page.url,
      };
    case "leadership_profile":
      return {
        ...base,
        "@type": "ProfilePage",
        name: page.profile?.role || page.title,
        url: brand.site + page.url,
        about: { "@type": "Organization", name: brand.legalName },
      };
    default:
      return null;
  }
}

export default async function CatchAllPage({ params }: { params: Promise<{ slug?: string[] }> }) {
  const { slug = [] } = await params;
  if (slug.length === 0) return <HomeView />;
  const url = "/" + slug.join("/") + "/";
  const file = fileForUrl(url);
  const page = file ? readPage(file) : null;
  if (!page) notFound();

  const bc = breadcrumbJsonLd(page);
  const extra = pageJsonLd(page);
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(bc) }} />
      {extra && <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(extra) }} />}
      <ContentPage page={page} />
    </>
  );
}
