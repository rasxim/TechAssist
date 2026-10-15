import { ArrowRight, Mic } from "lucide-react";

export function StartNewCaseCard() {
  return (
    <section className="flex min-h-0 flex-col rounded-2xl border border-border bg-surface p-7">
      <h2 className="text-xl font-semibold">Start a New Case</h2>
      <p className="mt-1.5 text-sm text-secondary">
        Describe the student&apos;s issue using your voice or type it below.
      </p>

      <div className="flex min-h-0 flex-1 flex-col items-center justify-center gap-4 py-6">
        {/* Matte, static button per DESIGN.md: 144px, subtle border, no glow or aura. */}
        <button
          type="button"
          aria-label="Tap to record"
          className="flex h-36 w-36 shrink-0 items-center justify-center rounded-full border border-white/10 bg-maroon shadow-sm transition-colors duration-200 hover:bg-maroon-hover"
        >
          <Mic className="h-11 w-11 text-white" strokeWidth={1.75} />
        </button>

        <div className="text-center">
          <p className="text-[15px] font-medium text-primary">Tap to record</p>
          <p className="mt-0.5 text-xs text-muted">or press space</p>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <input
          type="text"
          placeholder="Describe the issue..."
          className="h-11 flex-1 rounded-[10px] border border-border bg-bg-secondary px-4 text-sm text-primary placeholder:text-muted focus:border-maroon focus:outline-none focus:ring-1 focus:ring-maroon"
        />
        <button
          type="button"
          aria-label="Submit"
          className="flex h-11 w-11 shrink-0 items-center justify-center rounded-[10px] bg-maroon text-white transition-colors duration-200 hover:bg-maroon-hover"
        >
          <ArrowRight className="h-[18px] w-[18px]" strokeWidth={2} />
        </button>
      </div>
    </section>
  );
}
