"use client";

import { useState } from "react";
import { CheckCircle2, Loader2, AlertCircle } from "lucide-react";

const INTERESTS = [
  "Applied AI & Generative AI",
  "Agentic AI & Hyperautomation",
  "Data, Analytics & Lakehouse",
  "Cybersecurity & Zero-Trust",
  "Cloud, Edge & Platform Engineering",
  "Quantum & Advanced Compute",
  "Blockchain & Digital Trust",
  "IoT, Digital Twin & Robotics",
  "Partnerships / Alliances",
  "Careers",
  "Other",
];

/* Input system per Wave 1 CHG-054/055/056: labels, focus ring orange,
   custom select arrow, orange checked states, error/success states. */
export default function ContactForm({ compact = false }: { compact?: boolean }) {
  const [state, setState] = useState<"idle" | "sending" | "success" | "error">("idle");
  const [errorMsg, setErrorMsg] = useState("");

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    const data = new FormData(form);
    // honeypot: bots fill it, humans do not see it
    if ((data.get("company_website") as string)?.length) {
      setState("success");
      return;
    }
    setState("sending");
    const accessKey = process.env.NEXT_PUBLIC_FORM_ACCESS_KEY;
    const payload: Record<string, string> = {
      name: (data.get("name") as string) || "",
      email: (data.get("email") as string) || "",
      interest: (data.get("interest") as string) || "",
      message: (data.get("message") as string) || "",
      consent: (data.get("consent") as string) || "",
      subject: "Website contact — " + ((data.get("interest") as string) || "general"),
      from_name: "Achala IT Solutions website",
    };
    try {
      if (accessKey) {
        payload.access_key = accessKey;
        const res = await fetch("https://api.web3forms.com/submit", {
          method: "POST",
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify(payload),
        });
        const json = await res.json();
        if (!json.success) throw new Error(json.message || "Submission failed");
      } else {
        // demo mode: no endpoint configured yet — simulate a short delay
        await new Promise((r) => setTimeout(r, 600));
      }
      setState("success");
      form.reset();
    } catch (err) {
      setErrorMsg(err instanceof Error ? err.message : "Submission failed");
      setState("error");
    }
  }

  if (state === "success") {
    return (
      <div className="rounded-xl border border-brand/40 bg-brand-tint p-6" role="status">
        <div className="flex items-start gap-3">
          <CheckCircle2 className="mt-0.5 h-5 w-5 text-brand-deep" />
          <div>
            <p className="font-semibold text-navy-800">Thank you — your message is with us.</p>
            <p className="mt-1 text-sm text-slate-body/80">
              A practice lead (not a call center) responds within one business day.
            </p>
          </div>
        </div>
      </div>
    );
  }

  const fieldCls =
    "w-full rounded-[10px] border border-line bg-white px-3 py-2.5 text-[13.5px] text-navy-800 placeholder:text-slate-body/40 focus:outline-none focus:ring-2 focus:ring-brand/70 focus:border-brand transition";
  const labelCls = "mb-1 block text-[12px] font-semibold text-navy-800";

  return (
    <form onSubmit={onSubmit} className="space-y-3" aria-label="Contact form">
      {/* honeypot */}
      <input type="text" name="company_website" tabIndex={-1} autoComplete="off" className="hidden" aria-hidden="true" />
      <div className={compact ? "grid gap-3 sm:grid-cols-2" : "grid gap-3 sm:grid-cols-2"}>
        <div>
          <label htmlFor="cf-name" className={labelCls}>
            Full name
          </label>
          <input id="cf-name" name="name" required minLength={2} className={fieldCls} placeholder="Your name" />
        </div>
        <div>
          <label htmlFor="cf-email" className={labelCls}>
            Work email
          </label>
          <input id="cf-email" name="email" type="email" required className={fieldCls} placeholder="you@company.com" />
        </div>
      </div>
      <div>
        <label htmlFor="cf-interest" className={labelCls}>
          Area of interest
        </label>
        <div className="relative">
          <select id="cf-interest" name="interest" className={`${fieldCls} appearance-none pr-9`} defaultValue={INTERESTS[0]}>
            {INTERESTS.map((i) => (
              <option key={i} value={i}>
                {i}
              </option>
            ))}
          </select>
          {/* custom arrow (CHG-056) */}
          <svg
            aria-hidden="true"
            className="pointer-events-none absolute right-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-slate-body/60"
            viewBox="0 0 12 12"
            fill="none"
          >
            <path d="M2.5 4.5 L6 8 L9.5 4.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </div>
      </div>
      {!compact && (
        <div>
          <label htmlFor="cf-message" className={labelCls}>
            The metric you need to move
          </label>
          <textarea
            id="cf-message"
            name="message"
            rows={4}
            className={fieldCls}
            placeholder="Tell us the outcome you are targeting and the constraint you operate under — regulatory, security, capital."
          />
        </div>
      )}
      <div className="flex items-start gap-2">
        {/* orange checked state (CHG-055) */}
        <input
          id="cf-consent"
          name="consent"
          type="checkbox"
          required
          className="mt-1 h-4 w-4 rounded border-line accent-[#d20000]"
        />
        <label htmlFor="cf-consent" className="text-[11.5px] leading-snug text-slate-body/70">
          I consent to Achala IT Solutions storing this message to respond to my inquiry, in line with the{" "}
          <a href="/privacy-policy/" className="underline hover:text-navy-800">
            Privacy Policy
          </a>
          . Client data is never used for model training.
        </label>
      </div>
      {state === "error" && (
        <p className="flex items-center gap-2 text-[12.5px] text-red-600" role="alert">
          <AlertCircle className="h-4 w-4" /> {errorMsg || "Something went wrong — please email info@achalasolutions.com."}
        </p>
      )}
      <button
        type="submit"
        disabled={state === "sending"}
        className="btn-sheen inline-flex w-full items-center justify-center gap-2 rounded-[10px] bg-brand px-5 py-3 text-[13.5px] font-semibold text-white transition-colors hover:bg-brand-hover disabled:opacity-60 sm:w-auto"
      >
        {state === "sending" ? (
          <>
            <Loader2 className="h-4 w-4 animate-spin" /> Sending…
          </>
        ) : (
          "Send message"
        )}
      </button>
    </form>
  );
}
