import { ArrowUpRight, BookOpen, FileSpreadsheet, LifeBuoy, MessageSquare } from "lucide-react";

const resources = [
  { icon: FileSpreadsheet, title: "Tech Lounge Cheat Sheet", description: "Procedures and lookups" },
  { icon: BookOpen, title: "Student Handbook", description: "Policies and shift guide" },
  { icon: LifeBuoy, title: "ITS Documentation", description: "help.lafayette.edu" },
  { icon: MessageSquare, title: "Tech Lounge Slack", description: "Ask for help" },
];

export function QuickResourcesCard() {
  return (
    <section className="shrink-0 rounded-2xl border border-border bg-surface px-6 py-4">
      <h3 className="text-lg font-semibold">Quick Resources</h3>

      <div className="mt-3 grid grid-cols-4 gap-3">
        {resources.map((r) => (
          <button
            key={r.title}
            className="flex items-center justify-between gap-3 rounded-xl border border-border bg-bg-secondary px-4 py-3 text-left transition-colors duration-200 hover:border-border-strong hover:bg-surface-hover"
          >
            <div className="flex min-w-0 items-center gap-3">
              <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-maroon/20 text-white/85">
                <r.icon className="h-[18px] w-[18px]" strokeWidth={1.75} />
              </div>
              <div className="min-w-0">
                <p className="truncate text-sm font-medium text-primary">{r.title}</p>
                <p className="mt-0.5 truncate text-xs text-muted">{r.description}</p>
              </div>
            </div>
            <ArrowUpRight className="h-4 w-4 shrink-0 text-muted" strokeWidth={1.75} />
          </button>
        ))}
      </div>
    </section>
  );
}
