import type { NextConfig } from "next";

// Static export mode: NEXT_STATIC_EXPORT=1 next build  →  pure HTML in ./out
// (used for GitHub Pages / any static host). Dev + preview use standalone mode.
const isExport = process.env.NEXT_STATIC_EXPORT === "1";

const shared = {
  typescript: { ignoreBuildErrors: true },
  reactStrictMode: false,
  // Pin Turbopack's workspace root to site/ — without this, the stray bun.lock
  // in the parent repo makes Turbopack trace the whole parent tree (uploads,
  // second node_modules) and OOM the sandbox during the production build.
  turbopack: { root: __dirname, memoryLimit: 1536 },
} satisfies Partial<NextConfig>;

const nextConfig: NextConfig = isExport
  ? {
      ...shared,
      output: "export",
      trailingSlash: true,
      images: { unoptimized: true },
      distDir: ".next-export",
      // GitHub Pages project-site preview: GHPAGES=1 builds with /achala base path.
      // NEXT_PUBLIC_BASE_PATH lets server components prefix raw <img src> paths,
      // because next/image does NOT prefix under unoptimized+basePath.
      ...(process.env.GHPAGES === "1" ? { basePath: "/achala" } : {}),
      env: {
        NEXT_PUBLIC_SITE_URL: process.env.NEXT_PUBLIC_SITE_URL || "https://www.achalasolutions.com",
        NEXT_PUBLIC_BASE_PATH: process.env.GHPAGES === "1" ? "/achala" : "",
      },
    }
  : {
      ...shared,
      output: "standalone",
    };

export default nextConfig;
