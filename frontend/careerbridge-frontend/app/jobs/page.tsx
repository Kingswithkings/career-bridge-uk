"use client";

import { useState } from "react";
import { apiPost, endpoints } from "@/lib/api";
import { useRouter } from "next/navigation";
import AuthGate from "@/components/AuthGate";
import ResultPanel from "@/components/ResultPanel";

export default function JobsPage() {
  const router = useRouter();

  const [role, setRole] = useState("");
  const [location, setLocation] = useState("United Kingdom");
  const [cvText, setCvText] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState("");
  const [lastFeatureType, setLastFeatureType] = useState("");
  const [lastResultText, setLastResultText] = useState("");

  function getToken() {
    return localStorage.getItem("token") || "";
  }

  function requireToken() {
    const token = getToken();

    if (!token) {
      setResult("Not authenticated. Please log in first.");
      router.push("/login");
      return null;
    }

    return token;
  }

  function showResult(data: unknown, featureType: string) {
    const text = JSON.stringify(data, null, 2);
    setResult(text);
    setLastResultText(text);
    setLastFeatureType(featureType);
  }

  async function searchJobs() {
    const token = requireToken();

    if (!token) {
      return;
    }

    try {
      const data = await apiPost(
        endpoints.searchJobs,
        {
          query: role,
          location,
        },
        token
      );

      showResult(data, "job_search");
    } catch (err: unknown) {
      setResult(err instanceof Error ? err.message : "Job search failed.");
    }
  }

  async function matchJob() {
    const token = requireToken();

    if (!token) {
      return;
    }

    try {
      const data = await apiPost(
        endpoints.matchJobs,
        {
          cv_text: cvText,
          target_role: role,
          job_description: jobDescription,
          location,
        },
        token
      );

      showResult(data, "job_match");
    } catch (err: unknown) {
      setResult(err instanceof Error ? err.message : "Job match failed.");
    }
  }

  async function saveResult() {
    const token = requireToken();

    if (!token || !lastResultText) {
      return;
    }

    try {
      const data = await apiPost(
        endpoints.saveResult,
        {
          feature_type: lastFeatureType || "jobs",
          target_role: role,
          location,
          input_text: cvText || jobDescription || role,
          result_text: lastResultText,
        },
        token
      );

      setResult(JSON.stringify(data, null, 2));
    } catch (err: unknown) {
      setResult(err instanceof Error ? err.message : "Could not save result.");
    }
  }

  return (
    <AuthGate>
      <main className="min-h-screen bg-slate-950 text-white px-6 py-12">
      <div className="max-w-5xl mx-auto space-y-6">
        <h1 className="text-4xl font-bold">Jobs</h1>

        <input
          className="w-full p-3 rounded bg-slate-800 border border-slate-700"
          placeholder="Role e.g. AI Engineer"
          value={role}
          onChange={(e) => setRole(e.target.value)}
        />

        <input
          className="w-full p-3 rounded bg-slate-800 border border-slate-700"
          placeholder="Location"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />

        <button onClick={searchJobs} className="bg-blue-600 px-5 py-3 rounded">
          Search Jobs
        </button>

        <textarea
          className="w-full p-3 rounded bg-slate-800 border border-slate-700 min-h-44"
          placeholder="Paste CV text for job match..."
          value={cvText}
          onChange={(e) => setCvText(e.target.value)}
        />

        <textarea
          className="w-full p-3 rounded bg-slate-800 border border-slate-700 min-h-44"
          placeholder="Paste job description..."
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
        />

        <button onClick={matchJob} className="bg-green-600 px-5 py-3 rounded">
          Match Candidate To Job
        </button>

        {lastResultText && (
          <button onClick={saveResult} className="bg-slate-700 px-5 py-3 rounded">
            Save Result
          </button>
        )}

        {result && <ResultPanel result={result} />}
      </div>
      </main>
    </AuthGate>
  );
}
