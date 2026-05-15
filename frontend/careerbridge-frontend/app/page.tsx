import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 text-white px-6 py-20">
      <div className="max-w-5xl mx-auto text-center space-y-6">
        <h1 className="text-5xl font-bold">CareerBridge UK</h1>

        <p className="text-slate-300 text-lg">
          AI-powered career mentor for CV analysis, job matching, interview preparation,
          and UK job applications.
        </p>

        <div className="flex justify-center gap-4">
          <Link
            href="/register"
            className="bg-blue-600 px-6 py-3 rounded-xl font-semibold"
          >
            Get Started
          </Link>

          <Link
            href="/login"
            className="bg-slate-800 px-6 py-3 rounded-xl font-semibold"
          >
            Login
          </Link>
        </div>
      </div>
    </main>
  );
}