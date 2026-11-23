/* Base-path helper for raw (non-next/image, non-next/link) asset references.
 * "" under custom-domain serving; "/achala" on the GitHub Pages preview build
 * (GHPAGES=1 → NEXT_PUBLIC_BASE_PATH is inlined by next.config.ts env).
 * Browser-fetched same-origin assets (logo, favicon, manifest link, icons)
 * must be prefixed; crawler-resolved absolute URLs (og:image via metadataBase)
 * must NOT be prefixed — they point at the production domain. */
export const BP = process.env.NEXT_PUBLIC_BASE_PATH || "";
