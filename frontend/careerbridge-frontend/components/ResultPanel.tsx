type SavedResult = {
  id: number;
  feature_type: string;
  target_role?: string | null;
  location?: string | null;
  result_text: string;
  created_at: string;
};

type JobItem = {
  title?: string | null;
  company?: string | null;
  location?: string | null;
  salary_min?: number | null;
  salary_max?: number | null;
  description?: string | null;
  redirect_url?: string | null;
  apply_url?: string | null;
  application_url?: string | null;
  url?: string | null;
};

function parseJson(text: string) {
  try {
    return JSON.parse(text) as unknown;
  } catch {
    return null;
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function firstTextValue(value: Record<string, unknown>) {
  for (const item of Object.values(value)) {
    if (typeof item === "string") {
      return item;
    }
  }

  return "";
}

function isSavedResult(value: unknown): value is SavedResult {
  return (
    isRecord(value) &&
    typeof value.id === "number" &&
    typeof value.feature_type === "string" &&
    typeof value.result_text === "string"
  );
}

function isJobItem(value: unknown): value is JobItem {
  return (
    isRecord(value) &&
    ("title" in value ||
      "company" in value ||
      "redirect_url" in value ||
      "apply_url" in value ||
      "application_url" in value ||
      "url" in value)
  );
}

function getApplyUrl(job: JobItem) {
  return job.redirect_url || job.apply_url || job.application_url || job.url || null;
}

function JobCards({ jobs, countLabel }: { jobs: JobItem[]; countLabel: string }) {
  return (
    <div className="space-y-4">
      <p className="text-slate-300">{countLabel}</p>

      {jobs.map((job, index) => {
        const applyUrl = getApplyUrl(job);

        return (
          <article key={`${job.title}-${job.company}-${index}`} className="bg-slate-900 border border-slate-800 p-5 rounded">
            <h2 className="text-xl font-semibold">{job.title || "Untitled role"}</h2>
            <p className="text-slate-400">
              {[job.company, job.location].filter(Boolean).join(" - ")}
            </p>
            {(job.salary_min || job.salary_max) && (
              <p className="mt-2 text-slate-300">
                Salary: {[job.salary_min, job.salary_max].filter(Boolean).join(" - ")}
              </p>
            )}
            {job.description && <p className="mt-3 text-slate-200 whitespace-pre-wrap">{job.description}</p>}
            {applyUrl ? (
              <a
                href={applyUrl}
                className="mt-4 inline-flex rounded bg-blue-600 px-4 py-2 font-semibold text-white hover:bg-blue-500"
                target="_blank"
                rel="noreferrer"
              >
                Apply now
              </a>
            ) : (
              <p className="mt-4 text-sm text-slate-400">Apply link unavailable for this listing.</p>
            )}
          </article>
        );
      })}
    </div>
  );
}

export default function ResultPanel({ result }: { result: string }) {
  const parsed = parseJson(result);

  if (Array.isArray(parsed) && parsed.every(isSavedResult)) {
    return (
      <div className="space-y-4">
        {parsed.length === 0 && <p className="text-slate-300">No saved results yet.</p>}

        {parsed.map((item) => (
          <article key={item.id} className="bg-slate-900 border border-slate-800 p-5 rounded">
            <div className="flex flex-wrap gap-3 text-sm text-slate-400">
              <span>{item.feature_type.replaceAll("_", " ")}</span>
              {item.target_role && <span>{item.target_role}</span>}
              {item.location && <span>{item.location}</span>}
              <span>{new Date(item.created_at).toLocaleString()}</span>
            </div>
            <p className="mt-4 whitespace-pre-wrap text-slate-100">{item.result_text}</p>
          </article>
        ))}
      </div>
    );
  }

  if (isRecord(parsed) && Array.isArray(parsed.results) && parsed.results.every(isJobItem)) {
    return (
      <JobCards
        jobs={parsed.results}
        countLabel={`${String(parsed.count ?? parsed.results.length)} jobs found.`}
      />
    );
  }

  if (isRecord(parsed) && typeof parsed.match_result === "string") {
    const matchedJobs = Array.isArray(parsed.matched_jobs)
      ? parsed.matched_jobs.filter(isJobItem)
      : [];

    return (
      <div className="space-y-6">
        <section className="bg-slate-900 border border-slate-800 p-6 rounded">
          <h2 className="text-xl font-semibold">Match result</h2>
          <p className="mt-4 whitespace-pre-wrap text-slate-100">{parsed.match_result}</p>
        </section>

        {matchedJobs.length > 0 ? (
          <JobCards
            jobs={matchedJobs}
            countLabel={`${String(parsed.jobs_count ?? matchedJobs.length)} matched jobs found. You can apply from these listings.`}
          />
        ) : (
          <p className="text-slate-300">No matched jobs were returned for this search.</p>
        )}
      </div>
    );
  }

  if (isRecord(parsed)) {
    const text = firstTextValue(parsed);

    if (text) {
      return (
        <section className="bg-slate-900 border border-slate-800 p-6 rounded">
          <p className="whitespace-pre-wrap text-slate-100">{text}</p>
        </section>
      );
    }
  }

  return (
    <pre className="bg-black p-6 rounded whitespace-pre-wrap text-sm">
      {result}
    </pre>
  );
}
