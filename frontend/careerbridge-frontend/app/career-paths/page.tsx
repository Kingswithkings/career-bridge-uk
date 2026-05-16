import AuthGate from "@/components/AuthGate";

const paths = [
  {
    title: "Technology",
    roles: ["Software Engineer", "Cloud Engineer", "Cybersecurity Analyst", "Data Analyst", "AI Engineer"],
    focus: "Build projects, certifications and role-specific CV evidence.",
  },
  {
    title: "Healthcare and Social Care",
    roles: ["Nurse", "Doctor", "Care Worker", "Healthcare Assistant", "Clinical Support Worker"],
    focus: "Check registration, sponsorship eligibility and care-sector requirements.",
  },
  {
    title: "Business and Operations",
    roles: ["Business Analyst", "Project Manager", "Operations Coordinator", "Finance Analyst"],
    focus: "Show measurable business impact, stakeholder work and process improvement.",
  },
  {
    title: "Engineering and Built Environment",
    roles: ["Civil Engineer", "Mechanical Engineer", "Electrical Engineer", "Quantity Surveyor"],
    focus: "Match technical skills, project experience and professional standards.",
  },
];

export default function CareerPathsPage() {
  return (
    <AuthGate>
      <main className="min-h-screen bg-slate-950 text-white px-6 py-12">
        <div className="max-w-6xl mx-auto space-y-8">
          <section className="space-y-4">
            <p className="text-blue-400 font-semibold">UK Opportunity Platform</p>
            <h1 className="text-4xl font-bold">UK Career Paths</h1>
            <p className="text-slate-300 max-w-3xl">
              Explore practical career routes for the UK market, including common
              role progressions and what to highlight in applications.
            </p>
          </section>

          <section className="grid lg:grid-cols-2 gap-5">
            {paths.map((path) => (
              <article key={path.title} className="bg-slate-900 border border-slate-800 rounded p-6 space-y-4">
                <div>
                  <h2 className="text-2xl font-bold">{path.title}</h2>
                  <p className="text-slate-400 mt-2">{path.focus}</p>
                </div>
                <div className="flex flex-wrap gap-2">
                  {path.roles.map((role) => (
                    <span key={role} className="bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm">
                      {role}
                    </span>
                  ))}
                </div>
              </article>
            ))}
          </section>
        </div>
      </main>
    </AuthGate>
  );
}
