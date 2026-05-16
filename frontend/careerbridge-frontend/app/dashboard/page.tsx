import Link from "next/link";
import AuthGate from "@/components/AuthGate";

export default function DashboardPage() {
  return (
    <AuthGate>
      <main className="min-h-screen bg-slate-950 text-white px-6 py-12">
        <div className="max-w-6xl mx-auto space-y-8">
          <h1 className="text-4xl font-bold">Dashboard</h1>

          <div className="grid md:grid-cols-3 gap-6">
            <Link href="/cv" className="bg-slate-900 p-6 rounded-2xl">
              <h2 className="text-2xl font-semibold">CV Tools</h2>
              <p className="text-slate-400 mt-2">Analyze and improve your CV.</p>
            </Link>

            <Link href="/jobs" className="bg-slate-900 p-6 rounded-2xl">
              <h2 className="text-2xl font-semibold">Job Match</h2>
              <p className="text-slate-400 mt-2">Find and match jobs.</p>
            </Link>

            <Link href="/interview" className="bg-slate-900 p-6 rounded-2xl">
              <h2 className="text-2xl font-semibold">Interview Prep</h2>
              <p className="text-slate-400 mt-2">Prepare for interviews.</p>
            </Link>

            <Link href="/uk-visas" className="bg-slate-900 p-6 rounded-2xl">
              <h2 className="text-2xl font-semibold">UK Visas</h2>
              <p className="text-slate-400 mt-2">Compare UK work routes and official GOV.UK guidance.</p>
            </Link>

            <Link href="/sponsorship-jobs" className="bg-slate-900 p-6 rounded-2xl">
              <h2 className="text-2xl font-semibold">Sponsorship Jobs</h2>
              <p className="text-slate-400 mt-2">Plan a sponsored UK job search.</p>
            </Link>

            <Link href="/career-paths" className="bg-slate-900 p-6 rounded-2xl">
              <h2 className="text-2xl font-semibold">Career Paths</h2>
              <p className="text-slate-400 mt-2">Explore UK career routes by sector.</p>
            </Link>

            <Link href="/salary-insights" className="bg-slate-900 p-6 rounded-2xl">
              <h2 className="text-2xl font-semibold">Salary Insights</h2>
              <p className="text-slate-400 mt-2">Research pay expectations and visa salary signals.</p>
            </Link>
          </div>
        </div>
      </main>
    </AuthGate>
  );
}
