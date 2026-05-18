"use client";

import { useEffect, useSyncExternalStore, type ReactNode } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

const INACTIVITY_TIMEOUT_MS = 15 * 60 * 1000;
const LAST_ACTIVITY_KEY = "lastActivityAt";
const activityEvents = ["click", "keydown", "mousemove", "scroll", "touchstart"];

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
  const router = useRouter();
  const token = useSyncExternalStore(subscribeToAuthChanges, getAuthToken, () => null);

  useEffect(() => {
    if (!token) {
      return;
    }

    let timeoutId: ReturnType<typeof window.setTimeout> | null = null;

    function logout() {
      localStorage.removeItem("token");
      localStorage.removeItem("email");
      localStorage.removeItem(LAST_ACTIVITY_KEY);
      window.dispatchEvent(new Event("auth-change"));
      router.push("/login");
    }

    function getLastActivity() {
      const lastActivity = Number(localStorage.getItem(LAST_ACTIVITY_KEY));
      return Number.isFinite(lastActivity) && lastActivity > 0 ? lastActivity : Date.now();
    }

    function scheduleLogout() {
      if (timeoutId) {
        window.clearTimeout(timeoutId);
      }

      const remainingTime = INACTIVITY_TIMEOUT_MS - (Date.now() - getLastActivity());

      if (remainingTime <= 0) {
        logout();
        return;
      }

      timeoutId = window.setTimeout(scheduleLogout, remainingTime);
    }

    function recordActivity() {
      localStorage.setItem(LAST_ACTIVITY_KEY, Date.now().toString());
      scheduleLogout();
    }

    const existingLastActivity = Number(localStorage.getItem(LAST_ACTIVITY_KEY));

    if (
      Number.isFinite(existingLastActivity) &&
      existingLastActivity > 0 &&
      Date.now() - existingLastActivity >= INACTIVITY_TIMEOUT_MS
    ) {
      logout();
      return;
    }

    recordActivity();
    activityEvents.forEach((eventName) => {
      window.addEventListener(eventName, recordActivity, { passive: true });
    });

    return () => {
      if (timeoutId) {
        window.clearTimeout(timeoutId);
      }

      activityEvents.forEach((eventName) => {
        window.removeEventListener(eventName, recordActivity);
      });
    };
  }, [router, token]);

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
