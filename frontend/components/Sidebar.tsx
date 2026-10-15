import { FolderOpen, House, Settings, SquareLibrary } from "lucide-react";

const navItems = [
  { icon: House, label: "Home", active: true },
  { icon: FolderOpen, label: "Cases", active: false },
  { icon: SquareLibrary, label: "Resources", active: false },
  { icon: Settings, label: "Settings", active: false },
];

export function Sidebar() {
  return (
    <aside className="flex w-[84px] shrink-0 flex-col items-center border-r border-border bg-bg-secondary py-6">
      <div className="flex h-10 w-10 items-center justify-center rounded-[10px] bg-maroon text-lg font-semibold text-white">
        T
      </div>

      <nav className="mt-8 flex flex-col gap-2">
        {navItems.map(({ icon: Icon, label, active }) => (
          <button
            key={label}
            type="button"
            title={label}
            aria-label={label}
            className={`flex h-10 w-10 items-center justify-center rounded-[10px] transition-colors duration-200 ${
              active
                ? "bg-maroon/25 text-white"
                : "text-muted hover:bg-surface-hover hover:text-secondary"
            }`}
          >
            <Icon className="h-5 w-5" strokeWidth={1.75} />
          </button>
        ))}
      </nav>

      <div className="flex-1" />

      <div className="flex h-9 w-9 items-center justify-center rounded-full bg-surface-raised text-xs font-medium text-secondary">
        AR
      </div>
    </aside>
  );
}
