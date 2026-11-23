import type { MetadataRoute } from "next";
import { pageIndex } from "@/lib/content";

export const dynamic = "force-static";

const SITE = process.env.NEXT_PUBLIC_SITE_URL || "https://www.achalasolutions.com";

export default function sitemap(): MetadataRoute.Sitemap {
  const rows = pageIndex();
  const extra = [
    { url: "/patented-intelligence/", priority: 0.8 },
  ];
  return [
    ...rows.map((r) => {
      const priority =
        r.url === "/" ? 1.0 : r.template.endsWith("_hub") ? 0.8 : r.l4 ? 0.5 : 0.6;
      return {
        url: SITE + r.url,
        lastModified: new Date(),
        changeFrequency: "monthly" as const,
        priority,
      };
    }),
    ...extra.map((e) => ({
      url: SITE + e.url,
      lastModified: new Date(),
      changeFrequency: "monthly" as const,
      priority: e.priority,
    })),
  ];
}
