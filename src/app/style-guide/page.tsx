import type { Metadata } from "next";
import Logo from "@/components/site/Logo";

/* Hidden style-guide page (Wave 1, CHG-097): renders every token and core
   component for visual QA and developer onboarding. Not linked in navigation. */
export const metadata: Metadata = {
  title: "Achala IT Solutions — Style Guide",
  description: "Internal design-system reference. Not for publication.",
  robots: { index: false, follow: false },
};

const SWATCHES: { name: string; cls: string; hex: string }[] = [
  { name: "Brand Orange", cls: "bg-brand", hex: "#d20000" },
  { name: "Orange Hover", cls: "bg-brand-hover", hex: "#a80000" },
  { name: "Orange Deep (text-safe)", cls: "bg-brand-deep", hex: "#8f0000" },
  { name: "Orange 300 (on navy)", cls: "bg-brand-300", hex: "#ff9d96" },
  { name: "Orange Tint", cls: "bg-brand-tint", hex: "#fdecec" },
  { name: "Navy 950", cls: "bg-navy-950", hex: "#0e2230" },
  { name: "Navy 900", cls: "bg-navy-900", hex: "#16334a" },
  { name: "Navy 800", cls: "bg-navy-800", hex: "#2b5672" },
  { name: "Navy 700", cls: "bg-navy-700", hex: "#3a6983" },
  { name: "Navy 600", cls: "bg-navy-600", hex: "#477a95" },
  { name: "Navy 500", cls: "bg-navy-500", hex: "#568aa6" },
  { name: "Mist", cls: "bg-mist", hex: "#F6F7FB" },
  { name: "Line", cls: "bg-line", hex: "#E5E7F0" },
  { name: "Body text", cls: "bg-slate-body", hex: "#46425A" },
];

export default function StyleGuide() {
  return (
    <div className="container-dq py-14 space-y-14">
      <header>
        <p className="kicker-bar text-[12px] font-semibold uppercase tracking-[0.2em] text-brand-deep">
          Internal reference
        </p>
        <h1 className="text-display-2 mt-2 text-navy-800">Achala IT Solutions style guide</h1>
        <p className="measure mt-3 text-[14.5px] text-slate-body">
          Every color, type style and core component in one place. Not indexed, not linked from
          navigation. Source of truth: <code>src/app/globals.css</code> and{" "}
          <code>src/content/brand.json</code>.
        </p>
      </header>

      {/* Logo variants */}
      <section>
        <h2 className="text-display-3 text-navy-800">Logo variants (CHG-004/025)</h2>
        <div className="mt-5 grid gap-5 md:grid-cols-3">
          <div className="rounded-2xl border border-line bg-white p-6 shadow-1">
            <Logo height={34} />
            <p className="mt-4 text-[12px] text-slate-body/70">Full color — light surfaces</p>
          </div>
          <div className="relative overflow-hidden rounded-2xl grad-navy-field p-6">
            <div className="absolute inset-0 dot-grid" aria-hidden="true" />
            <Logo variant="reversed" height={34} className="relative" />
            <p className="relative mt-4 text-[12px] text-white/60">Reversed — navy surfaces</p>
          </div>
          <div className="rounded-2xl border border-line bg-mist p-6">
            <Logo variant="mono" height={34} />
            <p className="mt-4 text-[12px] text-slate-body/70">Mono navy — print / legal</p>
          </div>
        </div>
        <p className="mt-3 text-[12.5px] text-slate-body/70">
          Clearspace = the height of the orange block on all sides. Minimum width 120px. Never
          recolor, stretch, shadow or rotate the mark. The orange &ldquo;o&rdquo; dot bounces on
          hover — hover the header logo to see it.
        </p>
      </section>

      {/* Palette */}
      <section>
        <h2 className="text-display-3 text-navy-800">Palette</h2>
        <div className="mt-5 grid grid-cols-2 gap-3 sm:grid-cols-4 lg:grid-cols-7">
          {SWATCHES.map((s) => (
            <div key={s.hex}>
              <div className={`h-14 rounded-xl border border-line ${s.cls}`} />
              <p className="mt-1.5 text-[12px] font-semibold text-navy-800">{s.name}</p>
              <p className="text-[11px] text-slate-body/60">{s.hex}</p>
            </div>
          ))}
        </div>
        <p className="mt-3 text-[12.5px] text-slate-body/70">
          Orange stays the accent (~10% of any view). Cyan/teal are prohibited legacy tokens.
        </p>
      </section>

      {/* Type scale */}
      <section>
        <h2 className="text-display-3 text-navy-800">Fluid type scale (CHG-044)</h2>
        <div className="mt-5 space-y-4">
          <p className="text-display-1 text-navy-800">Display 1 — 40/72px</p>
          <p className="text-display-2 text-navy-800">Display 2 — 30/48px</p>
          <p className="text-display-3 text-navy-800">Display 3 — 22/30px</p>
          <p className="text-body-lg text-slate-body">Body large — 15/16.5px. Achala IT Solutions engineers the intelligence layer of the enterprise.</p>
          <p className="text-[14.5px] text-slate-body">Body — 14.5px/1.75 for long-form prose with a 68ch measure.</p>
        </div>
      </section>

      {/* Buttons */}
      <section>
        <h2 className="text-display-3 text-navy-800">Buttons (CHG-052/053)</h2>
        <div className="mt-5 flex flex-wrap items-center gap-3">
          <button className="btn-sheen rounded-[10px] bg-brand px-5 py-2.5 text-[13px] font-semibold text-white hover:bg-brand-hover">
            Primary — orange
          </button>
          <button className="rounded-[10px] bg-navy-800 px-5 py-2.5 text-[13px] font-semibold text-white hover:bg-navy-700">
            Dark — navy
          </button>
          <button className="rounded-[10px] border border-line bg-white px-5 py-2.5 text-[13px] font-medium text-navy-800 hover:border-brand hover:text-brand-deep">
            Ghost on light
          </button>
          <button className="rounded-[10px] border border-white/25 px-5 py-2.5 text-[13px] font-medium text-white/85 hover:border-brand-300 hover:text-brand-300 grad-navy-field">
            Ghost on dark
          </button>
        </div>
      </section>

      {/* Inputs */}
      <section>
        <h2 className="text-display-3 text-navy-800">Inputs (CHG-054/055)</h2>
        <div className="mt-5 grid max-w-xl gap-4">
          <div>
            <label className="mb-1 block text-[12px] font-semibold text-navy-800" htmlFor="sg-input">Input</label>
            <input
              id="sg-input"
              className="w-full rounded-[10px] border border-line px-3 py-2.5 text-[13.5px] text-navy-800 focus:outline-none focus:ring-2 focus:ring-brand/70 focus:border-brand"
              placeholder="Type to see the orange focus ring"
            />
          </div>
          <label className="flex items-center gap-2 text-[13px] text-slate-body">
            <input type="checkbox" className="h-4 w-4 accent-[#d20000]" defaultChecked /> Orange checked state
          </label>
        </div>
      </section>

      {/* Chips + callouts */}
      <section>
        <h2 className="text-display-3 text-navy-800">Chips &amp; callouts (CHG-057/082)</h2>
        <div className="mt-5 flex flex-wrap gap-2">
          <span className="rounded-full bg-brand px-3 py-1 text-[12px] font-semibold text-white">Solid orange</span>
          <span className="rounded-full border border-navy-800 px-3 py-1 text-[12px] font-medium text-navy-800">Outline navy</span>
          <span className="rounded-full bg-mist px-3 py-1 text-[12px] font-medium text-navy-800">Soft mist</span>
          <span className="rounded-full border border-white/20 bg-white/10 px-3 py-1 text-[12px] font-medium text-white grad-navy-field">Glass dark</span>
        </div>
        <div className="mt-5 grid gap-3 md:grid-cols-2">
          <p className="flex items-start gap-2.5 rounded-xl border border-brand/30 bg-brand-tint px-4 py-3 text-[12.5px] text-slate-body">
            <span className="mt-0.5 h-2 w-2 shrink-0 rounded-full bg-brand" /> Insight callout — orange.
          </p>
          <p className="flex items-start gap-2.5 rounded-xl border border-navy-800/30 bg-navy-800 px-4 py-3 text-[12.5px] text-white/85">
            <span className="mt-0.5 h-2 w-2 shrink-0 rounded-full bg-brand-300" /> Compliance callout — navy.
          </p>
        </div>
      </section>

      {/* Patterns */}
      <section>
        <h2 className="text-display-3 text-navy-800">Dark-band patterns (CHG-089)</h2>
        <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {[
            { cls: "dot-grid", label: "Dot grid" },
            { cls: "pattern-hatch", label: "Diagonal hatch" },
            { cls: "pattern-mesh", label: "Mesh glow" },
            { cls: "pattern-noise", label: "Noise" },
          ].map((p) => (
            <div key={p.label} className="relative flex h-24 items-end overflow-hidden rounded-2xl grad-navy-field">
              <div className={`absolute inset-0 ${p.cls}`} aria-hidden="true" />
              <p className="relative p-3 text-[12px] text-white/70">{p.label}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
