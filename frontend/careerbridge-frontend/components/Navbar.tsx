import Link from "next/link";
import ThemeToggle from "@/components/ThemeToggle";

export default function Navbar() {
  return (
    <nav className="bg-slate-950 border-b border-slate-800 px-6 py-4">
      <div className="max-w-6xl mx-auto flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <Link href="/" className="text-xl font-bold text-white shrink-0">
          CareerBridge UK
        </Link>

        <div className="flex flex-col gap-3 md:flex-row md:items-center lg:justify-end">
          <div className="flex flex-wrap gap-x-5 gap-y-2 text-sm text-slate-300">
            <Link href="/dashboard">Dashboard</Link>
            <Link href="/cv">CV Tools</Link>
            <Link href="/jobs">Jobs</Link>
            <Link href="/interview">Interview</Link>
            <Link href="/results">Results</Link>
            <Link href="/register">Register</Link>
            <Link href="/login">Login</Link>
          </div>

          <ThemeToggle />
        </div>
      </div>
    </nav>
  );
}
