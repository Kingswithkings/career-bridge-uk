"use client";

import { useEffect, useState, type FormEvent } from "react";
import Link from "next/link";
import AuthGate from "@/components/AuthGate";
import { apiGet, apiPost } from "@/lib/api";

type EvidenceReference = {
  source_url?: string;
  job_title?: string;
  job_id?: string;
  source_type?: string;
  source_excerpt?: string | null;
};

type SkillGap = {
  skill: string;
  jobs_mentioning_gap: number;
  live_listings_mentioning_gap?: number;
  synthetic_examples_mentioning_gap?: number;
  why_it_matters?: string;
  alternative_explanation?: string;
  verification_action?: string;
  hypothesis_investigation?: {
    next_evidence_check?: string;
  };
  evidence_references?: EvidenceReference[];
};

type SourceCritique = {
  providers?: string[];
  sample_count?: number;
  non_sample_count?: number;
  sufficient_for_cross_source_inference?: boolean;
  limitations?: string[];
};

type Investigation = {
  conclusion?: string;
  priority_skill_gaps?: SkillGap[];
  source_critique?: SourceCritique;
  next_actions?: string[];
};

type AgentStep = {
  step: string;
  status: string;
  records?: number;
  records_added?: number;
  reason?: string;
};

type XAIResponse = {
  run_id?: string;
  candidate_goal?: string;
  jobs_evaluated?: number;
  evidence_graph?: {
    relationship_count?: number;
  };
  investigation?: Investigation;
  agent_trace?: AgentStep[];
  nightshift?: {
    status?: string;
    used?: boolean;
  };
  nvidia?: {
    status?: string;
    used?: boolean;
    model_reported?: string;
    advisory_narrative?: string;
    independently_verified?: boolean;
  };
};

const XAI_DEMO_MODE =
  process.env.NEXT_PUBLIC_XAI_DEMO_MODE === "true";

const inputClass =
  "w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-white outline-none focus:border-blue-400";

function splitItems(value: string): string[] {
  return value.split(",").map((item) => item.trim()).filter(Boolean);
}

function isSafeUrl(value: string): boolean {
  try {
    const url = new URL(value);
    return url.protocol === "https:" || url.protocol === "http:";
  } catch {
    return false;
  }
}

function InvestigationPageContent() {
  const [careerGoal, setCareerGoal] = useState("Machine Learning Engineer");
  const [skills, setSkills] = useState("Python, FastAPI, LLMs, RAG");
  const [education, setEducation] = useState("MSc Applied AI");
  const [experience, setExperience] = useState("3");
  const [location, setLocation] = useState("");
  const [question, setQuestion] = useState(
    "Which evidenced skills should I investigate to improve my career prospects?"
  );
  const [includeNvidia, setIncludeNvidia] = useState(false);
  const [nvidiaAvailable, setNvidiaAvailable] = useState(false);
  useEffect(() => {
    let active = true;
    apiGet("/api/xai/capabilities")
      .then((capabilities) => {
        if (active) setNvidiaAvailable(capabilities.nvidia_available === true);
      })
      .catch(() => { /* Keep optional inference disabled if availability is unknown. */ });
    return () => { active = false; };
  }, []);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [report, setReport] = useState<XAIResponse | null>(null);

  async function runInvestigation(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setReport(null);

    try {
      const token = localStorage.getItem("token");

      if (includeNvidia && nvidiaAvailable && !token) {
        throw new Error(
          "Log in with a valid CareerBridge account to use NVIDIA inference."
        );
      }

      if (!token && !XAI_DEMO_MODE) {
        throw new Error("Your session has expired. Please log in again.");
      }

      const response = await apiPost(
        "/api/xai/run",
        {
          candidate: {
            career_goal: careerGoal.trim(),
            skills: splitItems(skills),
            education: splitItems(education),
            experience_years: Number(experience),
          },
          limit: 10,
          include_live_jobs: true,
          include_nvidia_insight: includeNvidia && nvidiaAvailable,
          location: location.trim() || null,
          question: question.trim() || null,
        },
        token ?? undefined
      );

      setReport(response as XAIResponse);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Investigation failed."
      );
    } finally {
      setLoading(false);
    }
  }

  const investigation = report?.investigation;
  const critique = investigation?.source_critique;

  return (
    <main className="min-h-screen bg-slate-950 px-6 py-10 text-white">
      <div className="mx-auto max-w-6xl space-y-8">
        <header className="space-y-3">
          <Link href="/dashboard" className="text-sm text-blue-300 hover:underline">
            ← Back to Dashboard
          </Link>

          <p className="text-sm font-semibold uppercase tracking-widest text-blue-300">
            CareerBridge XAI
          </p>

          <h1 className="text-3xl font-bold md:text-4xl">
            AI Career Investigation
          </h1>

          <p className="max-w-3xl text-slate-300">
            Investigate career opportunities using job evidence, transparent
            reasoning, source limitations, and actionable recommendations.
          </p>
        </header>

        <form
          onSubmit={runInvestigation}
          className="space-y-6 rounded-2xl border border-slate-800 bg-slate-900/50 p-6"
        >
          <h2 className="text-xl font-semibold">Candidate profile</h2>

          <div className="grid gap-5 md:grid-cols-2">
            <label className="space-y-2">
              <span className="text-sm text-slate-300">Career goal</span>
              <input
                required
                value={careerGoal}
                onChange={(event) => setCareerGoal(event.target.value)}
                className={inputClass}
              />
            </label>

            <label className="space-y-2">
              <span className="text-sm text-slate-300">Experience (years)</span>
              <input
                required
                type="number"
                min="0"
                step="0.5"
                value={experience}
                onChange={(event) => setExperience(event.target.value)}
                className={inputClass}
              />
            </label>

            <label className="space-y-2">
              <span className="text-sm text-slate-300">
                Skills (comma-separated)
              </span>
              <input
                value={skills}
                onChange={(event) => setSkills(event.target.value)}
                className={inputClass}
              />
            </label>

            <label className="space-y-2">
              <span className="text-sm text-slate-300">
                Education (comma-separated)
              </span>
              <input
                value={education}
                onChange={(event) => setEducation(event.target.value)}
                className={inputClass}
              />
            </label>

            <label className="space-y-2 md:col-span-2">
              <span className="text-sm text-slate-300">
                Job search location (optional)
              </span>
              <input
                value={location}
                onChange={(event) => setLocation(event.target.value)}
                placeholder="Leave blank for a UK-wide search"
                className={inputClass}
              />
            </label>

            <label className="space-y-2 md:col-span-2">
              <span className="text-sm text-slate-300">
                What would you like to investigate?
              </span>
              <textarea
                rows={3}
                maxLength={500}
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                className={inputClass}
              />
            </label>
          </div>

          <p className="text-sm text-slate-300">
            Investigations use live Adzuna job listings only. No sample jobs are
            used. Listing details and skill mentions are not independently verified.
          </p>

          <label className="flex items-start gap-3 text-sm text-slate-300">
            <input
              type="checkbox"
              checked={includeNvidia && nvidiaAvailable}
              disabled={!nvidiaAvailable || loading}
              onChange={(event) => setIncludeNvidia(event.target.checked)}
              className="mt-1 h-4 w-4"
            />
            {nvidiaAvailable
              ? "Include an NVIDIA Nemotron AI explanation. Requires login and may consume API credits."
              : "NVIDIA explanations are unavailable. You can still investigate live job evidence."}
          </label>

          <button
            type="submit"
            disabled={loading}
            className="rounded-xl bg-blue-600 px-6 py-3 font-semibold text-white hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? "Investigating..." : "Run Career Investigation"}
          </button>

          {error && (
            <p role="alert" className="rounded-xl border border-red-800 bg-red-950/40 p-4 text-red-200">
              {error}
            </p>
          )}
        </form>

        {report && (
          <div className="space-y-6" aria-live="polite">
            <div className="grid gap-4 sm:grid-cols-3">
              <Metric
                label="Jobs evaluated"
                value={report.jobs_evaluated ?? 0}
              />
              <Metric
                label="Evidence relationships"
                value={report.evidence_graph?.relationship_count ?? 0}
              />
              <Metric
                label="Non-sample records"
                value={critique?.non_sample_count ?? 0}
              />
            </div>

            <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6 space-y-4">
              <h2 className="text-xl font-semibold">Investigation conclusion</h2>
              <p className="leading-7 text-slate-300">
                {investigation?.conclusion || "No conclusion was returned."}
              </p>
            </section>

            <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6 space-y-5">
              <h2 className="text-xl font-semibold">
                Preliminary skill-gap hypotheses
              </h2>

              {(investigation?.priority_skill_gaps || []).length === 0 && (
                <p className="text-slate-400">No skill gaps were identified.</p>
              )}

              {(investigation?.priority_skill_gaps || []).map((gap, index) => (
                <article
                  key={`${gap.skill}-${index}`}
                  className="space-y-3 rounded-xl border border-slate-700 p-4"
                >
                  <div className="flex flex-wrap justify-between gap-2">
                    <h3 className="font-semibold">{gap.skill}</h3>
                    <span className="text-sm text-blue-300">
                      {gap.jobs_mentioning_gap} record(s) mentioning this skill
                    </span>
                  </div>

                  <p className="text-sm text-slate-400">
                    A keyword absent from the submitted profile does not prove
                    that the candidate lacks the skill.
                  </p>

                  {gap.why_it_matters && (
                    <p className="text-sm text-slate-200">
                      <strong>Why this matters:</strong> {gap.why_it_matters}
                    </p>
                  )}

                  <p className="text-sm text-slate-400">
                    Non-sample references: {gap.live_listings_mentioning_gap ?? 0}
                    {" | "}
                    Synthetic references: {gap.synthetic_examples_mentioning_gap ?? 0}
                  </p>

                  {gap.alternative_explanation && (
                    <p className="text-sm text-slate-300">
                      <strong>Alternative explanation:</strong>{" "}
                      {gap.alternative_explanation}
                    </p>
                  )}

                  {gap.hypothesis_investigation?.next_evidence_check && (
                    <p className="text-sm text-blue-200">
                      <strong>Next evidence check:</strong>{" "}
                      {gap.hypothesis_investigation.next_evidence_check}
                    </p>
                  )}

                  {(gap.evidence_references || []).length > 0 && (
                    <div className="space-y-2">
                      <h4 className="text-sm font-medium text-slate-300">
                        Supporting references
                      </h4>

                      {(gap.evidence_references || []).map((ref, refIndex) => (
                        <div key={refIndex} className="text-sm">
                          {ref.source_url && isSafeUrl(ref.source_url) ? (
                            <a
                              href={ref.source_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="break-words text-blue-300 hover:underline"
                            >
                              {ref.job_title || ref.job_id || "View job source"} ↗
                            </a>
                          ) : (
                            <span className="text-slate-400">
                              {ref.job_title || ref.job_id || "Source link unavailable"}
                            </span>
                          )}
                          {ref.source_excerpt && (
                            <blockquote className="mt-2 border-l-2 border-blue-500 pl-3 text-slate-300">
                              {ref.source_excerpt}
                            </blockquote>
                          )}
                          <p className="mt-1 text-xs text-slate-500">
                            {ref.source_type === "sample"
                              ? "Synthetic demonstration evidence"
                              : "Unverified listing evidence"}
                          </p>
                        </div>
                      ))}
                    </div>
                  )}
                </article>
              ))}
            </section>

            <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6 space-y-4">
              <h2 className="text-xl font-semibold">Evidence integrity</h2>

              <div className="grid gap-3 text-sm sm:grid-cols-2">
                <p>
                  <span className="text-slate-400">Providers: </span>
                  {(critique?.providers || []).join(", ") || "Not reported"}
                </p>
                <p>
                  <span className="text-slate-400">Sample records: </span>
                  {critique?.sample_count ?? "Unknown"}
                </p>
                <p>
                  <span className="text-slate-400">Independent corroboration: </span>
                  {critique?.sufficient_for_cross_source_inference
                    ? "Supported by source critique"
                    : "Not established"}
                </p>
              </div>

              {(critique?.limitations || []).map((item, index) => (
                <p
                  key={index}
                  className="rounded-lg border border-amber-900/60 bg-amber-950/30 p-3 text-sm text-amber-100"
                >
                  {item}
                </p>
              ))}

              <p className="text-sm text-slate-400">
                {critique?.sample_count === 0
                  ? "No synthetic demonstration records were used. "
                  : (critique?.sample_count ?? 0) > 0
                    ? "Some records are synthetic demonstrations. "
                    : "The sample record count was not reported. "}
                Live Adzuna listings
                are not independently verified, and extracted keywords are
                not confirmed employer requirements.
              </p>
            </section>

            <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6 space-y-4">
              <h2 className="text-xl font-semibold">Recommended next actions</h2>

              {(investigation?.next_actions || []).map((action, index) => (
                <p key={index} className="text-slate-300">
                  {index + 1}. {action}
                </p>
              ))}
            </section>

            {report.nvidia && report.nvidia.status !== "not_requested" && (
              <section className="space-y-4 rounded-2xl border border-blue-800 bg-slate-900 p-6">
                <h2 className="text-xl font-semibold">
                  NVIDIA Nemotron AI Explanation
                </h2>

                <p className="text-sm text-slate-400">
                  Status: {report.nvidia.status}
                </p>

                {report.nvidia.model_reported && (
                  <p className="text-sm text-blue-300">
                    Model: {report.nvidia.model_reported}
                  </p>
                )}

                {report.nvidia.used && report.nvidia.advisory_narrative && (
                  <p className="whitespace-pre-wrap leading-7 text-slate-200">
                    {report.nvidia.advisory_narrative}
                  </p>
                )}

                <p className="text-xs text-amber-200">
                  AI-generated advisory interpretation. Independently
                  verified evidence is not established by this narrative.
                  Refer to the cited investigation findings above.
                </p>
              </section>
            )}

            <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6 space-y-4">
              <h2 className="text-xl font-semibold">Agent execution trace</h2>

              {(report.agent_trace || []).map((step, index) => (
                <div
                  key={index}
                  className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 py-3 last:border-b-0"
                >
                  <div>
                    <p className="font-medium">
                      {step.step.replaceAll("_", " ")}
                    </p>
                    {step.reason && (
                      <p className="text-xs text-slate-400">{step.reason}</p>
                    )}
                  </div>

                  <span className="rounded-full bg-slate-800 px-3 py-1 text-sm text-slate-200">
                    {step.status}
                  </span>
                </div>
              ))}

              <p className="text-xs text-slate-400">
                Nightshift inference: {report.nightshift?.status || "Not reported"}
              </p>
            </section>

            {report.run_id && (
              <p className="break-all text-xs text-slate-500">
                Investigation ID: {report.run_id}
              </p>
            )}
          </div>
        )}
      </div>
    </main>
  );
}

function Metric({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
      <p className="text-sm text-slate-400">{label}</p>
      <p className="mt-2 text-3xl font-bold">{value}</p>
    </div>
  );
}

export default function XAIPage() {
  if (XAI_DEMO_MODE) {
    return <InvestigationPageContent />;
  }

  return (
    <AuthGate>
      <InvestigationPageContent />
    </AuthGate>
  );
}
