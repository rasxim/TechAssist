export function Header() {
  return (
    <header className="flex h-24 shrink-0 items-center justify-between border-b border-border px-6">
      <div>
        <h1 className="text-[28px] font-semibold leading-none tracking-tight">
          Tech<span className="text-maroon-hover">Assist</span>
        </h1>
        <p className="mt-2 text-sm text-secondary">Lafayette College Tech Lounge</p>
      </div>

      <div className="flex items-center gap-5">
        <div className="text-right">
          <p className="text-sm text-primary">Good evening, Aaru</p>
          <p className="mt-0.5 text-xs text-muted">Saturday, May 24, 2025</p>
        </div>
        <div className="h-8 w-px bg-border" />
        <div className="flex items-center gap-2 text-sm text-primary">
          <span className="h-2 w-2 rounded-full bg-success" />
          Staff Online
        </div>
      </div>
    </header>
  );
}
