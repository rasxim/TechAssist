import { ChevronRight, KeyRound, Printer, ShieldCheck, Wifi } from "lucide-react";

const cases = [
  { icon: Wifi, title: "Wi-Fi connection issue", device: "MacBook", status: "Solved", time: "2m ago" },
  { icon: ShieldCheck, title: "Duo authentication", device: "iPhone", status: "Escalated", time: "18m ago" },
  { icon: Printer, title: "Printer not working", device: "Windows", status: "Solved", time: "24m ago" },
  { icon: KeyRound, title: "Password reset", device: "Chromebook", status: "Solved", time: "41m ago" },
];

export function RecentCasesCard() {
  return (
    <section className="flex min-h-0 flex-1 flex-col rounded-2xl border border-border bg-surface px-6 py-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">Recent Cases</h3>
        <button className="flex items-center gap-0.5 text-[13px] text-secondary transition-colors duration-200 hover:text-primary">
          View all
          <ChevronRight className="h-3.5 w-3.5" />
        </button>
      </div>

      {/* No scrollbar: rows that don't fully fit wrap into a hidden second column,
          so only whole rows show. "View all" opens the full history. */}
      <div className="mt-2 flex min-h-0 flex-1 flex-col flex-wrap divide-y divide-border overflow-hidden">
        {cases.map((c) => (
          <div key={c.title} className="flex w-full items-center justify-between py-1.5">
            <div className="flex items-center gap-3">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-surface-raised text-secondary">
                <c.icon className="h-4 w-4" strokeWidth={1.75} />
              </div>
              <div>
                <p className="text-sm font-medium text-primary">{c.title}</p>
                <p className="mt-0.5 text-xs text-muted">
                  {c.device} ·{" "}
                  <span className={c.status === "Solved" ? "text-success" : "text-warning"}>
                    {c.status}
                  </span>
                </p>
              </div>
            </div>
            <span className="text-xs text-muted">{c.time}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
