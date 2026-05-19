"use client";

import { useState } from "react";
import AuthGate from "@/components/AuthGate";
import { apiPost, endpoints } from "@/lib/api";

type QuestionKey =
  | "cv_analysis_helpful"
  | "interview_preparation_useful"
  | "job_matching_accurate"
  | "app_loaded_quickly"
  | "would_use_again";

const questions: { key: QuestionKey; label: string }[] = [
  { key: "cv_analysis_helpful", label: "Was the CV analysis helpful?" },
  { key: "interview_preparation_useful", label: "Was the interview preparation useful?" },
  { key: "job_matching_accurate", label: "Did job matching feel accurate?" },
  { key: "app_loaded_quickly", label: "Did the app load quickly?" },
  { key: "would_use_again", label: "Would you use this again?" },
];

export default function FeedbackPage() {
  const [rating, setRating] = useState(0);
  const [page, setPage] = useState("");
  const [message, setMessage] = useState("");
  const [answers, setAnswers] = useState<Record<QuestionKey, boolean | null>>({
    cv_analysis_helpful: null,
    interview_preparation_useful: null,
    job_matching_accurate: null,
    app_loaded_quickly: null,
    would_use_again: null,
  });
  const [status, setStatus] = useState("");
  const [submitting, setSubmitting] = useState(false);

  function getToken() {
    return localStorage.getItem("token") || "";
  }

  function setAnswer(key: QuestionKey, value: boolean) {
    setAnswers((current) => ({ ...current, [key]: value }));
  }

  async function submitFeedback(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const token = getToken();

    if (!token) {
      setStatus("Please log in before sending feedback.");
      return;
    }

    if (rating < 1 || rating > 5) {
      setStatus("Choose a rating from 1 to 5.");
      return;
    }

    setSubmitting(true);
    setStatus("Sending feedback...");

    try {
      const data = await apiPost(
        endpoints.feedback,
        {
          rating,
          page: page || null,
          message: message || null,
          ...answers,
        },
        token,
      );

      setStatus(typeof data.message === "string" ? data.message : "Feedback submitted successfully.");
      setRating(0);
      setPage("");
      setMessage("");
      setAnswers({
        cv_analysis_helpful: null,
        interview_preparation_useful: null,
        job_matching_accurate: null,
        app_loaded_quickly: null,
        would_use_again: null,
      });
    } catch (err: unknown) {
      setStatus(err instanceof Error ? err.message : "Could not submit feedback.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <AuthGate>
      <main className="min-h-screen bg-slate-950 px-6 py-12 text-white">
        <section className="mx-auto max-w-3xl space-y-8">
          <div className="space-y-3">
            <h1 className="text-4xl font-bold">Feedback</h1>
            <p className="text-lg text-slate-300">
              Tell us what worked, what felt slow, and what should improve next.
            </p>
          </div>

          <form onSubmit={submitFeedback} className="space-y-6 rounded border border-slate-800 bg-slate-900 p-6">
            <fieldset className="space-y-3">
              <legend className="font-semibold text-slate-100">Overall rating</legend>
              <div className="flex gap-2" aria-label="Rating out of 5">
                {[1, 2, 3, 4, 5].map((value) => (
                  <button
                    key={value}
                    type="button"
                    onClick={() => setRating(value)}
                    className={`h-11 w-11 rounded border text-xl ${
                      value <= rating
                        ? "border-yellow-400 bg-yellow-400 text-slate-950"
                        : "border-slate-700 bg-slate-800 text-slate-300"
                    }`}
                    aria-label={`${value} star${value === 1 ? "" : "s"}`}
                  >
                    ★
                  </button>
                ))}
              </div>
            </fieldset>

            <label className="block space-y-2">
              <span className="font-semibold text-slate-100">Page or feature</span>
              <select
                value={page}
                onChange={(event) => setPage(event.target.value)}
                className="w-full rounded border border-slate-700 bg-slate-800 p-3 text-white"
              >
                <option value="">General feedback</option>
                <option value="cv">CV Tools</option>
                <option value="jobs">Jobs</option>
                <option value="interview">Interview</option>
                <option value="uk-visas">UK Visas</option>
                <option value="results">Results</option>
                <option value="dashboard">Dashboard</option>
              </select>
            </label>

            <div className="space-y-4">
              {questions.map((question) => (
                <fieldset
                  key={question.key}
                  className="flex flex-col gap-3 border-b border-slate-800 pb-4 md:flex-row md:items-center md:justify-between"
                >
                  <legend className="text-slate-200">{question.label}</legend>
                  <div className="flex gap-2">
                    <button
                      type="button"
                      onClick={() => setAnswer(question.key, true)}
                      className={`rounded px-4 py-2 ${
                        answers[question.key] === true
                          ? "bg-blue-600 text-white"
                          : "bg-slate-800 text-slate-300"
                      }`}
                    >
                      Yes
                    </button>
                    <button
                      type="button"
                      onClick={() => setAnswer(question.key, false)}
                      className={`rounded px-4 py-2 ${
                        answers[question.key] === false
                          ? "bg-blue-600 text-white"
                          : "bg-slate-800 text-slate-300"
                      }`}
                    >
                      No
                    </button>
                  </div>
                </fieldset>
              ))}
            </div>

            <label className="block space-y-2">
              <span className="font-semibold text-slate-100">Tell us what we should improve</span>
              <textarea
                value={message}
                onChange={(event) => setMessage(event.target.value)}
                maxLength={4000}
                className="min-h-36 w-full rounded border border-slate-700 bg-slate-800 p-3 text-white"
                placeholder="Tell us what we should improve..."
              />
            </label>

            <button
              type="submit"
              disabled={submitting}
              className="rounded bg-blue-600 px-5 py-3 font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
            >
              {submitting ? "Sending..." : "Send feedback"}
            </button>

            {status && <p className="text-sm text-slate-300">{status}</p>}
          </form>
        </section>
      </main>
    </AuthGate>
  );
}
