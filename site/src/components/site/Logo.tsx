import type { CSSProperties } from "react";

/*
 * Achala IT Solutions lockup — the approved artwork from www.achalasolutions.com
 * (red mark #d20000 + gray wordmark #898989 on transparent).
 * Variants: full (light surfaces) · reversed (white wordmark, dark surfaces) ·
 * mono (single steel blue, print/legal). Clearspace rule: keep free space equal
 * to the lockup height on all sides; never recolor, stretch, shadow or rotate.
 */
const LOGOS: Record<"full" | "reversed" | "mono", string> = {
  full: "/achala-logo.png",
  reversed: "/achala-logo-white.png",
  mono: "/achala-logo-mono.png",
};

type LogoProps = {
  variant?: "full" | "reversed" | "mono";
  height?: number;
  className?: string;
  style?: CSSProperties;
};

export default function Logo({ variant = "full", height = 38, className = "", style }: LogoProps) {
  const width = Math.round(height * (440 / 171));
  return (
    <img
      src={LOGOS[variant]}
      alt="Achala IT Solutions"
      width={width}
      height={height}
      className={`logo-lockup shrink-0 ${className}`}
      style={{ width: `${width}px`, height: `${height}px`, objectFit: "contain", ...style }}
    />
  );
}
