"use client";

import { useState } from "react";
import { apiGet, endpoints } from "@/lib/api";
import { useRouter } from "next/navigation";
import AuthGate from "@/components/AuthGate";
import ResultPanel from "@/components/ResultPanel";

export default function ResultsPage() {
  const router = useRouter();

  const [result, setResult] = useState("");

  function getToken() {
    return localStorage.getItem("token") || "";
  }

  async function getResults() {
    const token = getToken();

    if (!token) {
      setResult("Not authenticated. Please log in first.");
      router.push("/login");
      return;
    }

    try {
      const data = await apiGet(endpoints.getResults, token);
      setResult(JSON.stringify(data, null, 2));
    } catch (err: unknown) {
      setResult(err instanceof Error ? err.message : "Could not load saved results.");
    }
  }

  return (
    <AuthGate>
      <main className="min-h-screen bg-slate-950 text-white px-6 py-12">
      <div className="max-w-5xl mx-auto space-y-6">
        <h1 className="text-4xl font-bold">Saved Results</h1>

        <button onClick={getResults} className="bg-blue-600 px-5 py-3 rounded">
          Load Saved Results
        </button>

        {result && <ResultPanel result={result} />}
      </div>
      </main>
    </AuthGate>
  );
}
