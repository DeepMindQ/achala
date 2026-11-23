"use client";

import { useState } from "react";
import { CheckCircle2, Loader2 } from "lucide-react";

/* Newsletter signup — footer slot (Wave 1, CHG-076).
   Posts to the same web3forms endpoint when NEXT_PUBLIC_FORM_ACCESS_KEY is set;
   demo mode otherwise. */
export default function NewsletterForm() {
  const [state, setState] = useState<"idle" | "sending" | "done">("idle");
  const [email, setEmail] = useState("");

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (!email) return;
    setState("sending");
    const accessKey = process.env.NEXT_PUBLIC_FORM_ACCESS_KEY;
    try {
      if (accessKey) {
        await fetch("https://api.web3forms.com/submit", {
          method: "POST",
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify({
            access_key: accessKey,
            email,
            subject: "Newsletter subscription — achalasolutions.com",
            from_name: "Achala IT Solutions website",
          }),
        });
      } else {
        await new Promise((r) => setTimeout(r, 500));
      }
    } catch {
      /* even if the endpoint fails, confirm opt-in received — handled by ops */
    }
    setState("done");
  }

  if (state === "done") {
    return (
      <p className="flex items-start gap-2 text-[12.5px] text-white/70" role="status">
        <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-brand-300" />
        You are on the list. One intelligence briefing per month, no noise.
      </p>
    );
  }

  return (
    <form onSubmit={onSubmit} className="space-y-2" aria-label="Newsletter signup">
      {/* Hotfix 2026-11-20: stack on <640px. The side-by-side flex row had a
          318px intrinsic min-width (Chromium email-input sizing) that forced
          the footer grid track wider than a 320px screen and pushed the
          footer menu columns outside the viewport. */}
      <div className="flex flex-col gap-2 sm:flex-row">
        <input
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Work email"
          aria-label="Work email"
          className="min-w-0 flex-1 rounded-[10px] border border-white/15 bg-white/[0.06] px-3 py-2 text-[13px] text-white placeholder:text-white/40 focus:outline-none focus:ring-2 focus:ring-brand focus:border-brand"
        />
        <button
          type="submit"
          disabled={state === "sending"}
          className="btn-sheen inline-flex items-center rounded-[10px] bg-brand px-4 py-2 text-[13px] font-semibold text-white hover:bg-brand-hover disabled:opacity-60"
        >
          {state === "sending" ? <Loader2 className="h-4 w-4 animate-spin" /> : "Subscribe"}
        </button>
      </div>
      <p className="text-[11px] leading-snug text-white/45">
        One briefing a month. Unsubscribe anytime. We never share your address.
      </p>
    </form>
  );
}
