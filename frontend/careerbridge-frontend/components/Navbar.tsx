"use client";

import { useSyncExternalStore } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import ThemeToggle from "@/components/ThemeToggle";

function subscribeToAuthChanges(callback: () => void) {
  window.addEventListener("storage", callback);
  window.addEventListener("auth-change", callback);

  return () => {
    window.removeEventListener("storage", callback);
    window.removeEventListener("auth-change", callback);
  };
}

function getAuthToken() {
  return localStorage.getItem("token");
}

export default function Navbar() {
  const router = useRouter();
  const token = useSyncExternalStore(subscribeToAuthChanges, getAuthToken, () => null);
  const isLoggedIn = Boolean(token);

  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("email");
    window.dispatchEvent(new Event("auth-change"));
    router.push("/login");
  }

  return (
    <nav className="bg-slate-950 border-b border-slate-800 px-6 py-4">
      <div className="max-w-6xl mx-auto flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <Link href="/" className="text-xl font-bold text-white shrink-0">
          CareerBridge UK
        </Link>

        <div className="flex flex-col gap-3 md:flex-row md:items-center lg:justify-end">
          <div className="flex flex-wrap gap-x-5 gap-y-2 text-sm text-slate-300">
            {isLoggedIn ? (
              <>
                <Link href="/dashboard">Dashboard</Link>
                <Link href="/cv">CV Tools</Link>
                <Link href="/jobs">Jobs</Link>
                <Link href="/uk-visas">UK Visas</Link>
                <Link href="/sponsorship-jobs">Sponsorship Jobs</Link>
                <Link href="/career-paths">Career Paths</Link>
                <Link href="/salary-insights">Salary Insights</Link>
                <Link href="/interview">Interview</Link>
                <Link href="/results">Results</Link>
                <Link href="/feedback">Feedback</Link>
                <button
                  type="button"
                  onClick={logout}
                  className="text-left text-slate-300 hover:text-white"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link href="/register">Register</Link>
                <Link href="/login">Login</Link>
              </>
            )}
          </div>

          <ThemeToggle />
        </div>
      </div>
    </nav>
  );
}
