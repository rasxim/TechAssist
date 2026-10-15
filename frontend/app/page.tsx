import { CasesTodayCard } from "@/components/CasesTodayCard";
import { Header } from "@/components/Header";
import { QuickResourcesCard } from "@/components/QuickResourcesCard";
import { RecentCasesCard } from "@/components/RecentCasesCard";
import { Sidebar } from "@/components/Sidebar";
import { StartNewCaseCard } from "@/components/StartNewCaseCard";

export default function DashboardPage() {
  return (
    // Fills the screen exactly; below 640px tall the page scrolls instead of squashing.
    <div className="flex h-screen min-h-[640px] bg-bg">
      <Sidebar />

      <div className="flex min-w-0 flex-1 flex-col">
        <Header />

        <main className="flex min-h-0 flex-1 flex-col gap-5 overflow-y-auto px-6 py-5">
          <div className="grid min-h-0 flex-1 grid-cols-[3fr_2fr] grid-rows-[minmax(0,1fr)] gap-5">
            <StartNewCaseCard />
            <div className="flex min-h-0 flex-col gap-5">
              <CasesTodayCard />
              <RecentCasesCard />
            </div>
          </div>

          <QuickResourcesCard />
        </main>
      </div>
    </div>
  );
}
