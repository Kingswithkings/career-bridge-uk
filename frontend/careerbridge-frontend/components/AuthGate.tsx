"use client";

import { useSyncExternalStore, type ReactNode } from "react";
import Link from "next/link";

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

export default function AuthGate({ children }: { children: ReactNode }) {
  const token = useSyncExternalStore(subscribeToAuthChanges, getAuthToken, () => null);

  if (token) {
    return children;
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white px-6 py-20">
      <section className="max-w-xl mx-auto space-y-6">
        <div className="space-y-3">
          <p className="text-sm font-semibold uppercase tracking-wide text-blue-300">
            Account required
          </p>
          <h1 className="text-4xl font-bold">Log in to use CareerBridge UK</h1>
          <p className="text-slate-300 text-lg">
            Create an account or log in before using CV tools, job matching,
            interview preparation, dashboard, and saved results.
          </p>
        </div>

        <div className="flex flex-wrap gap-3">
          <Link href="/login" className="bg-blue-600 px-5 py-3 rounded font-semibold">
            Login
          </Link>
          <Link href="/register" className="bg-slate-800 px-5 py-3 rounded font-semibold">
            Register
          </Link>
        </div>
      </section>
    </main>
  );
}
