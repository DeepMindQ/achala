import type { NextConfig } from "next";

// Static export mode: NEXT_STATIC_EXPORT=1 next build  →  pure HTML in ./out
// (used for GitHub Pages / any static host). Dev + preview use standalone mode.
const isExport = process.env.NEXT_STATIC_EXPORT === "1";

const shared = {
  typescript: { ignoreBuildErrors: true },
  reactStrictMode: false,
} satisfies Partial<NextConfig>;

const nextConfig: NextConfig = isExport
  ? {
      ...shared,
      output: "export",
      trailingSlash: true,
      images: { unoptimized: true },
      distDir: ".next-export",
      env: { NEXT_PUBLIC_SITE_URL: process.env.NEXT_PUBLIC_SITE_URL || "https://www.achalasolutions.com" },
    }
  : {
      ...shared,
      output: "standalone",
    };

export default nextConfig;
