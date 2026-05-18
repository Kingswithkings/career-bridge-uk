"use client";

import { type ChangeEvent, useState } from "react";
import { apiPost, endpoints } from "@/lib/api";
import { useRouter } from "next/navigation";
import AuthGate from "@/components/AuthGate";
import ResultPanel from "@/components/ResultPanel";
import ActionButton from "@/components/ActionButton";

export default function CvPage() {
  const router = useRouter();

  const [cvText, setCvText] = useState("");
  const [cvFileName, setCvFileName] = useState("");
  const [targetRole, setTargetRole] = useState("");
  const [result, setResult] = useState("");
  const [lastFeatureType, setLastFeatureType] = useState("");
  const [lastResultText, setLastResultText] = useState("");
  const [pendingAction, setPendingAction] = useState<
    "analyze" | "generate" | "generateFromAnalysis" | "save" | null
  >(null);

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

  async function uploadCv(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    const isTextFile =
      file.type.startsWith("text/") ||
      /\.(txt|md|markdown|rtf)$/i.test(file.name);

    if (!isTextFile) {
      setResult("Please upload a text CV file for now, or paste your CV text below.");
      event.target.value = "";
      return;
    }

    try {
      const text = await file.text();
      setCvText(text);
      setCvFileName(file.name);
      setResult(`${file.name} uploaded. You can now analyze or generate your CV.`);
    } catch {
      setResult("Could not read that CV file. Please paste your CV text below.");
    }
  }

  async function analyzeCv() {
    const token = requireToken();

    if (!token) {
      return;
    }

    setResult("Analyzing your CV...");
    setPendingAction("analyze");

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
    } finally {
      setPendingAction(null);
    }
  }

  async function generateCv() {
    const token = requireToken();

    if (!token) {
      return;
    }

    setResult("Generating your improved CV...");
    setPendingAction("generate");

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
    } finally {
      setPendingAction(null);
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

    setResult("Generating from your CV analysis...");
    setPendingAction("generateFromAnalysis");

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
    } finally {
      setPendingAction(null);
    }
  }

  async function saveResult() {
    const token = requireToken();

    if (!token || !lastResultText) {
      return;
    }

    setResult("Saving result...");
    setPendingAction("save");

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
    } finally {
      setPendingAction(null);
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

        <div className="rounded border border-slate-700 bg-slate-900 p-4">
          <label className="block text-sm font-semibold text-slate-200" htmlFor="cv-upload">
            Upload CV
          </label>
          <input
            id="cv-upload"
            type="file"
            accept=".txt,.md,.markdown,.rtf,text/plain,text/markdown,text/rtf"
            onChange={uploadCv}
            className="mt-3 block w-full cursor-pointer rounded bg-slate-800 text-sm text-slate-300 file:mr-4 file:cursor-pointer file:border-0 file:bg-blue-600 file:px-4 file:py-3 file:font-semibold file:text-white"
          />
          {cvFileName && <p className="mt-2 text-sm text-slate-400">Loaded: {cvFileName}</p>}
        </div>

        <textarea
          className="w-full p-3 rounded bg-slate-800 border border-slate-700 min-h-72"
          placeholder="Paste your CV text here..."
          value={cvText}
          onChange={(e) => setCvText(e.target.value)}
        />

        <div className="flex gap-3">
          <ActionButton
            onClick={analyzeCv}
            pending={pendingAction === "analyze"}
            pendingLabel="Analyzing..."
            className="bg-blue-600 px-5 py-3 rounded"
          >
            Analyze CV
          </ActionButton>

          <ActionButton
            onClick={generateCv}
            pending={pendingAction === "generate"}
            pendingLabel="Generating..."
            className="bg-purple-600 px-5 py-3 rounded"
          >
            Generate Improved CV
          </ActionButton>

          <ActionButton
            onClick={generateCvFromAnalysis}
            pending={pendingAction === "generateFromAnalysis"}
            pendingLabel="Generating..."
            className="bg-green-600 px-5 py-3 rounded"
          >
            Generate From Analysis
          </ActionButton>
        </div>

        {lastResultText && (
          <ActionButton
            onClick={saveResult}
            pending={pendingAction === "save"}
            pendingLabel="Saving..."
            className="bg-slate-700 px-5 py-3 rounded"
          >
            Save Result
          </ActionButton>
        )}

        {result && <ResultPanel result={result} />}
      </div>
      </main>
    </AuthGate>
  );
}
