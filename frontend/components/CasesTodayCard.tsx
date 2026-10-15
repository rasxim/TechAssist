import { ProgressRing } from "./ProgressRing";

export function CasesTodayCard() {
  return (
    <section className="shrink-0 rounded-2xl border border-border bg-surface px-6 py-4">
      <h3 className="text-lg font-semibold">Cases Today</h3>

      <div className="mt-2 flex items-center justify-between">
        <div className="flex items-center gap-6">
          <p className="text-[44px] font-semibold leading-none tracking-tight">12</p>

          <div className="space-y-1.5 text-sm">
            <div className="flex items-center gap-2 text-secondary">
              <span className="h-2 w-2 rounded-full bg-success" />
              9 Solved
            </div>
            <div className="flex items-center gap-2 text-secondary">
              <span className="h-2 w-2 rounded-full bg-warning" />
              3 Escalated
            </div>
          </div>
        </div>

        <ProgressRing percent={75} label="Solved" size={84} stroke={7} />
      </div>
    </section>
  );
}
