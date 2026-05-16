import AuthGate from "@/components/AuthGate";

const salarySignals = [
  {
    title: "Compare role titles",
    detail: "UK salaries can vary widely between junior, mid-level, senior, lead and manager titles.",
  },
  {
    title: "Check region",
    detail: "London and South East roles often pay differently from other UK regions.",
  },
  {
    title: "Read visa salary rules",
    detail: "Sponsored roles may need to meet specific salary and occupation thresholds.",
  },
  {
    title: "Use multiple sources",
    detail: "Compare job adverts, recruiter salary guides, ONS data and GOV.UK visa guidance.",
  },
];

const sourceLinks = [
  {
    label: "Skilled Worker salary guidance",
    href: "https://www.gov.uk/skilled-worker-visa/your-job",
  },
  {
    label: "ONS earnings and working hours",
    href: "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours",
  },
];

export default function SalaryInsightsPage() {
  return (
    <AuthGate>
      <main className="min-h-screen bg-slate-950 text-white px-6 py-12">
        <div className="max-w-6xl mx-auto space-y-8">
          <section className="space-y-4">
            <p className="text-blue-400 font-semibold">UK Opportunity Platform</p>
            <h1 className="text-4xl font-bold">Salary Insights</h1>
            <p className="text-slate-300 max-w-3xl">
              Use salary research to target realistic roles, prepare negotiation
              ranges and check whether sponsored opportunities may meet visa rules.
            </p>
          </section>

          <section className="grid md:grid-cols-2 gap-5">
            {salarySignals.map((signal) => (
              <article key={signal.title} className="bg-slate-900 border border-slate-800 rounded p-6">
                <h2 className="text-xl font-semibold">{signal.title}</h2>
                <p className="text-slate-400 mt-2">{signal.detail}</p>
              </article>
            ))}
          </section>

          <section className="bg-slate-900 border border-slate-800 rounded p-6 space-y-4">
            <h2 className="text-2xl font-bold">Useful salary sources</h2>
            <div className="flex flex-wrap gap-3">
              {sourceLinks.map((source) => (
                <a
                  key={source.href}
                  href={source.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded font-semibold"
                >
                  {source.label}
                </a>
              ))}
            </div>
          </section>
        </div>
      </main>
    </AuthGate>
  );
}
