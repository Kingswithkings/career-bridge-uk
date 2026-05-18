"use client";

import { type ChangeEvent, useState } from "react";
import { apiPost, apiUploadFile, endpoints } from "@/lib/api";
import { useRouter } from "next/navigation";
import AuthGate from "@/components/AuthGate";
import ResultPanel from "@/components/ResultPanel";
import ActionButton from "@/components/ActionButton";

type InterviewMessage = {
  role: "candidate" | "interviewer";
  content: string;
};

export default function InterviewPage() {
  const router = useRouter();

  const [targetRole, setTargetRole] = useState("");
  const [cvText, setCvText] = useState("");
  const [cvFileName, setCvFileName] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState("");
  const [lastFeatureType, setLastFeatureType] = useState("");
  const [lastResultText, setLastResultText] = useState("");
  const [messages, setMessages] = useState<InterviewMessage[]>([]);
  const [candidateAnswer, setCandidateAnswer] = useState("");
  const [pendingAction, setPendingAction] = useState<"prepare" | "mock" | "save" | null>(null);

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
    const token = requireToken();
    const file = event.target.files?.[0];

    if (!token || !file) {
      return;
    }

    const isSupportedFile =
      file.type.startsWith("text/") ||
      /\.(txt|md|markdown|rtf|pdf|docx)$/i.test(file.name);

    if (!isSupportedFile) {
      setResult("Please upload a CV as PDF, DOCX, TXT, MD, Markdown, or RTF.");
      event.target.value = "";
      return;
    }

    try {
      setResult(`Reading ${file.name}...`);
      const data = await apiUploadFile(endpoints.uploadCv, file, token);

      if (typeof data.cv_text !== "string") {
        throw new Error("The upload response did not include CV text.");
      }

      setCvText(data.cv_text);
      setCvFileName(file.name);
      setResult(`${file.name} uploaded. You can now prepare for interviews.`);
    } catch (err: unknown) {
      setResult(err instanceof Error ? err.message : "Could not read that CV file.");
    }
  }

  async function prepareInterview() {
    const token = requireToken();

    if (!token) {
      return;
    }

    setResult("Preparing interview guidance...");
    setPendingAction("prepare");

    try {
      const data = await apiPost(
        endpoints.prepareInterview,
        {
          cv_text: cvText,
          job_description: jobDescription,
          target_role: targetRole,
        },
        token
      );

      showResult(data, "interview_preparation");
    } catch (err: unknown) {
      setResult(err instanceof Error ? err.message : "Interview preparation failed.");
    } finally {
      setPendingAction(null);
    }
  }

  function saveConversation(nextMessages: InterviewMessage[]) {
    const text = nextMessages
      .map((message) => `${message.role === "candidate" ? "Candidate" : "Interviewer"}: ${message.content}`)
      .join("\n\n");

    setLastResultText(text);
    setLastFeatureType("mock_interview");
  }

  async function mockInterview() {
    const token = requireToken();

    if (!token) {
      return;
    }

    const trimmedAnswer = candidateAnswer.trim();
    const outgoingMessages = trimmedAnswer
      ? [...messages, { role: "candidate" as const, content: trimmedAnswer }]
      : messages;

    setCandidateAnswer("");
    setResult("Getting interviewer response...");
    setPendingAction("mock");

    try {
      const data = await apiPost(
        endpoints.mockInterview,
        {
          cv_text: cvText,
          target_role: targetRole,
          experience_level: "Entry-level",
          messages: outgoingMessages,
        },
        token
      );

      const reply =
        typeof data === "object" &&
        data !== null &&
        "reply" in data &&
        typeof data.reply === "string"
          ? data.reply
          : JSON.stringify(data, null, 2);
      const nextMessages: InterviewMessage[] = [
        ...outgoingMessages,
        { role: "interviewer", content: reply },
      ];

      setMessages(nextMessages);
      saveConversation(nextMessages);
      setResult("");
    } catch (err: unknown) {
      setResult(err instanceof Error ? err.message : "Mock interview failed.");
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
          feature_type: lastFeatureType || "interview",
          target_role: targetRole,
          input_text: cvText || jobDescription,
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
        <h1 className="text-4xl font-bold">Interview Preparation</h1>

        <input
          className="w-full p-3 rounded bg-slate-800 border border-slate-700"
          placeholder="Target role"
          value={targetRole}
          onChange={(e) => setTargetRole(e.target.value)}
        />

        <div className="rounded border border-slate-700 bg-slate-900 p-4">
          <label className="block text-sm font-semibold text-slate-200" htmlFor="interview-cv-upload">
            Upload CV
          </label>
          <input
            id="interview-cv-upload"
            type="file"
            accept=".pdf,.docx,.txt,.md,.markdown,.rtf,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,text/plain,text/markdown,text/rtf"
            onChange={uploadCv}
            className="mt-3 block w-full cursor-pointer rounded bg-slate-800 text-sm text-slate-300 file:mr-4 file:cursor-pointer file:border-0 file:bg-blue-600 file:px-4 file:py-3 file:font-semibold file:text-white"
          />
          {cvFileName && <p className="mt-2 text-sm text-slate-400">Loaded: {cvFileName}</p>}
        </div>

        <textarea
          className="w-full p-3 rounded bg-slate-800 border border-slate-700 min-h-44"
          placeholder="Paste CV text..."
          value={cvText}
          onChange={(e) => setCvText(e.target.value)}
        />

        <textarea
          className="w-full p-3 rounded bg-slate-800 border border-slate-700 min-h-44"
          placeholder="Paste job description..."
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
        />

        <div className="flex gap-3">
          <ActionButton
            onClick={prepareInterview}
            pending={pendingAction === "prepare"}
            pendingLabel="Preparing..."
            className="bg-blue-600 px-5 py-3 rounded"
          >
            Prepare Interview
          </ActionButton>

          <ActionButton
            onClick={mockInterview}
            pending={pendingAction === "mock"}
            pendingLabel="Starting..."
            className="bg-purple-600 px-5 py-3 rounded"
          >
            Start Mock Interview
          </ActionButton>
        </div>

        {messages.length > 0 && (
          <div className="space-y-3 bg-slate-900 border border-slate-800 p-5 rounded">
            {messages.map((message, index) => (
              <div
                key={`${message.role}-${index}`}
                className={message.role === "candidate" ? "text-right" : "text-left"}
              >
                <p className="text-xs uppercase text-slate-500">
                  {message.role === "candidate" ? "You" : "Interviewer"}
                </p>
                <p className="inline-block max-w-3xl rounded bg-slate-800 px-4 py-3 text-left whitespace-pre-wrap">
                  {message.content}
                </p>
              </div>
            ))}
          </div>
        )}

        <div className="space-y-3">
          <textarea
            className="w-full p-3 rounded bg-slate-800 border border-slate-700 min-h-28"
            placeholder="Type your answer, then continue the mock interview..."
            value={candidateAnswer}
            onChange={(e) => setCandidateAnswer(e.target.value)}
          />

          <ActionButton
            onClick={mockInterview}
            pending={pendingAction === "mock"}
            pendingLabel="Sending..."
            className="bg-green-600 px-5 py-3 rounded"
          >
            Send Answer
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
