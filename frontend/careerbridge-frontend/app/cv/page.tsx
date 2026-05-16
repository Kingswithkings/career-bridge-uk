"use client";

import { useState } from "react";
import { apiPost, endpoints } from "@/lib/api";
import { useRouter } from "next/navigation";
import AuthGate from "@/components/AuthGate";
import ResultPanel from "@/components/ResultPanel";

export default function CvPage() {
  const router = useRouter();

  const [cvText, setCvText] = useState("");
  const [targetRole, setTargetRole] = useState("");
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

  async function analyzeCv() {
    const token = requireToken();

    if (!token) {
      return;
    }

    try {
      const data = await apiPost(
        endpoints.analyzeCv,
        {
          cv_text: cvText,
          target_role: targetRole,
        },
        token
      );

      showResult(data, "cv_analysis");
    } catch (err: unknown) {
      setResult(err instanceof Error ? err.message : "CV analysis failed.");
    }
  }

  async function generateCv() {
    const token = requireToken();

    if (!token) {
      return;
    }

    try {
      const data = await apiPost(
        endpoints.generateCv,
        {
          cv_text: cvText,
          target_role: targetRole,
        },
        token
      );

      showResult(data, "cv_generation");
    } catch (err: unknown) {
      setResult(err instanceof Error ? err.message : "CV generation failed.");
    }
  }

  async function generateCvFromAnalysis() {
    const token = requireToken();

    if (!token) {
      return;
    }

    if (!lastResultText) {
      setResult("Analyze your CV first, then generate from analysis.");
      return;
    }

    try {
      const data = await apiPost(
        endpoints.generateCvFromAnalysis,
        {
          cv_text: cvText,
          cv_analysis: lastResultText,
          target_role: targetRole,
        },
        token
      );

      showResult(data, "cv_from_analysis");
    } catch (err: unknown) {
      setResult(err instanceof Error ? err.message : "CV generation from analysis failed.");
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
          feature_type: lastFeatureType || "cv",
          target_role: targetRole,
          input_text: cvText,
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
        <h1 className="text-4xl font-bold">CV Tools</h1>

        <input
          className="w-full p-3 rounded bg-slate-800 border border-slate-700"
          placeholder="Target role e.g. AI Engineer"
          value={targetRole}
          onChange={(e) => setTargetRole(e.target.value)}
        />

        <textarea
          className="w-full p-3 rounded bg-slate-800 border border-slate-700 min-h-72"
          placeholder="Paste your CV text here..."
          value={cvText}
          onChange={(e) => setCvText(e.target.value)}
        />

        <div className="flex gap-3">
          <button onClick={analyzeCv} className="bg-blue-600 px-5 py-3 rounded">
            Analyze CV
          </button>

          <button onClick={generateCv} className="bg-purple-600 px-5 py-3 rounded">
            Generate Improved CV
          </button>

          <button onClick={generateCvFromAnalysis} className="bg-green-600 px-5 py-3 rounded">
            Generate From Analysis
          </button>
        </div>

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
