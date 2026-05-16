"use client";

import { useState } from "react";
import { apiPost, endpoints } from "@/lib/api";
import { useRouter } from "next/navigation";
import AuthGate from "@/components/AuthGate";
import ResultPanel from "@/components/ResultPanel";

type InterviewMessage = {
  role: "candidate" | "interviewer";
  content: string;
};

export default function InterviewPage() {
  const router = useRouter();

  const [targetRole, setTargetRole] = useState("");
  const [cvText, setCvText] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState("");
  const [lastFeatureType, setLastFeatureType] = useState("");
  const [lastResultText, setLastResultText] = useState("");
  const [messages, setMessages] = useState<InterviewMessage[]>([]);
  const [candidateAnswer, setCandidateAnswer] = useState("");

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

  async function prepareInterview() {
    const token = requireToken();

    if (!token) {
      return;
    }

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
    } catch (err: unknown) {
      setResult(err instanceof Error ? err.message : "Mock interview failed.");
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
          <button onClick={prepareInterview} className="bg-blue-600 px-5 py-3 rounded">
            Prepare Interview
          </button>

          <button onClick={mockInterview} className="bg-purple-600 px-5 py-3 rounded">
            Start Mock Interview
          </button>
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

          <button onClick={mockInterview} className="bg-green-600 px-5 py-3 rounded">
            Send Answer
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
