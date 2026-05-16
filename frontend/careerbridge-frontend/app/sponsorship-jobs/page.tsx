import AuthGate from "@/components/AuthGate";

const sponsorshipSteps = [
  "Check whether the employer appears on the official register of licensed sponsors.",
  "Confirm the role is eligible for the visa route you want to use.",
  "Compare salary, skill level and occupation requirements before applying.",
  "Tailor your CV to the sponsored role and the employer's sector.",
  "Ask the employer about Certificate of Sponsorship timing if you reach interview stage.",
];

const targetSectors = [
  "Software engineering and cloud",
  "Data, AI and cybersecurity",
  "Healthcare and social care",
  "Engineering and construction",
  "Education and teaching",
  "Finance, operations and business analysis",
];

export default function SponsorshipJobsPage() {
  return (
    <AuthGate>
      <main className="min-h-screen bg-slate-950 text-white px-6 py-12">
        <div className="max-w-6xl mx-auto space-y-8">
          <section className="space-y-4">
            <p className="text-blue-400 font-semibold">UK Opportunity Platform</p>
            <h1 className="text-4xl font-bold">Sponsorship Jobs</h1>
            <p className="text-slate-300 max-w-3xl">
              Use this page to plan a sponsored UK job search. Focus on licensed
              sponsors, eligible roles, salary requirements and applications that
              clearly match the employer&apos;s needs.
            </p>
            <a
              href="https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded font-semibold"
            >
              Check Licensed Sponsors
            </a>
          </section>

          <section className="grid md:grid-cols-2 gap-5">
            <div className="bg-slate-900 border border-slate-800 rounded p-6 space-y-4">
              <h2 className="text-2xl font-bold">Search checklist</h2>
              <ul className="space-y-3 text-slate-300 list-disc list-inside">
                {sponsorshipSteps.map((step) => (
                  <li key={step}>{step}</li>
                ))}
              </ul>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded p-6 space-y-4">
              <h2 className="text-2xl font-bold">High-opportunity sectors</h2>
              <div className="grid sm:grid-cols-2 gap-3">
                {targetSectors.map((sector) => (
                  <div key={sector} className="bg-slate-800 border border-slate-700 rounded p-3">
                    {sector}
                  </div>
                ))}
              </div>
            </div>
          </section>
        </div>
      </main>
    </AuthGate>
  );
}
