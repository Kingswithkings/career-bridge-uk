import AuthGate from "@/components/AuthGate";

const visaGroups = [
  {
    title: "Popular Sponsored Work Visas",
    description: "Best for applicants who already have a UK job offer from an approved sponsor.",
    visas: [
      {
        name: "Skilled Worker visa",
        workType: "Eligible skilled jobs with an approved UK sponsor",
        needsJobOffer: "Yes",
        bestFor: "Tech, business, engineering, education, finance, healthcare and other eligible roles",
        link: "https://www.gov.uk/skilled-worker-visa",
      },
      {
        name: "Health and Care Worker visa",
        workType: "Eligible NHS, healthcare, adult social care and medical roles",
        needsJobOffer: "Yes",
        bestFor: "Nurses, doctors, eligible health professionals and eligible adult social care roles",
        link: "https://www.gov.uk/health-care-worker-visa",
      },
      {
        name: "Scale-up Worker visa",
        workType: "Eligible roles with fast-growing UK businesses",
        needsJobOffer: "Yes",
        bestFor: "Workers joining eligible scale-up companies",
        link: "https://www.gov.uk/scale-up-worker-visa",
      },
    ],
  },
  {
    title: "Routes That Usually Do Not Need a Job Offer",
    description: "Useful for graduates, talented professionals, eligible young people and eligible nationals.",
    visas: [
      {
        name: "Graduate visa",
        workType: "Most types of work after completing an eligible UK course",
        needsJobOffer: "No",
        bestFor: "International students who completed an eligible UK degree or course",
        link: "https://www.gov.uk/graduate-visa",
      },
      {
        name: "Global Talent visa",
        workType: "Work in academia, research, arts, culture or digital technology",
        needsJobOffer: "No",
        bestFor: "Leaders or potential leaders in digital technology, research, science, arts or culture",
        link: "https://www.gov.uk/global-talent",
      },
      {
        name: "High Potential Individual visa",
        workType: "Work in the UK after graduating from an eligible top global university",
        needsJobOffer: "No",
        bestFor: "Graduates from eligible overseas universities",
        link: "https://www.gov.uk/high-potential-individual-visa",
      },
      {
        name: "Youth Mobility Scheme visa",
        workType: "Temporary work and living in the UK",
        needsJobOffer: "No",
        bestFor: "Eligible young people from participating countries and territories",
        link: "https://www.gov.uk/youth-mobility",
      },
      {
        name: "UK Ancestry visa",
        workType: "Work in the UK if you have eligible UK ancestry",
        needsJobOffer: "No",
        bestFor: "Eligible Commonwealth citizens and others with a UK-born grandparent",
        link: "https://www.gov.uk/ancestry-visa",
      },
    ],
  },
  {
    title: "Business, Founder and Global Business Mobility Routes",
    description: "For people building businesses or moving through international business routes.",
    visas: [
      {
        name: "Innovator Founder visa",
        workType: "Set up and run an innovative business in the UK",
        needsJobOffer: "No",
        bestFor: "Founders with endorsed innovative business ideas",
        link: "https://www.gov.uk/innovator-founder-visa",
      },
      {
        name: "UK Expansion Worker visa",
        workType: "Set up a UK branch of an overseas business",
        needsJobOffer: "Yes / overseas employer route",
        bestFor: "Senior managers or specialist employees expanding an overseas company into the UK",
        link: "https://www.gov.uk/uk-expansion-worker-visa",
      },
      {
        name: "Senior or Specialist Worker visa",
        workType: "Temporary UK assignment for an overseas employer",
        needsJobOffer: "Yes",
        bestFor: "Senior or specialist staff transferring within an international business",
        link: "https://www.gov.uk/senior-specialist-worker-visa",
      },
      {
        name: "Graduate Trainee visa",
        workType: "UK placement as part of a graduate training programme",
        needsJobOffer: "Yes",
        bestFor: "Graduate trainees moving through an overseas employer's UK branch",
        link: "https://www.gov.uk/graduate-trainee-visa",
      },
      {
        name: "Service Supplier visa",
        workType: "Provide services to a UK business under an eligible trade agreement",
        needsJobOffer: "Yes",
        bestFor: "Contractual service suppliers and independent professionals",
        link: "https://www.gov.uk/service-supplier-visa",
      },
      {
        name: "Secondment Worker visa",
        workType: "Temporary UK secondment under a high-value contract or investment",
        needsJobOffer: "Yes",
        bestFor: "Overseas workers seconded to a UK organisation",
        link: "https://www.gov.uk/secondment-worker-visa",
      },
    ],
  },
  {
    title: "Temporary Worker Visas",
    description: "For short-term work, cultural work, charity work, religious work and seasonal jobs.",
    visas: [
      {
        name: "Creative Worker visa",
        workType: "Creative industries, entertainment, performance and production work",
        needsJobOffer: "Yes",
        bestFor: "Artists, musicians, performers and creative professionals",
        link: "https://www.gov.uk/creative-worker-visa",
      },
      {
        name: "Charity Worker visa",
        workType: "Unpaid voluntary charity work",
        needsJobOffer: "Yes",
        bestFor: "Applicants doing eligible charity work",
        link: "https://www.gov.uk/charity-worker-visa",
      },
      {
        name: "Seasonal Worker visa",
        workType: "Seasonal agricultural or poultry work",
        needsJobOffer: "Yes",
        bestFor: "Temporary seasonal workers",
        link: "https://www.gov.uk/seasonal-worker-visa",
      },
      {
        name: "Religious Worker visa",
        workType: "Religious work, preaching or pastoral support",
        needsJobOffer: "Yes",
        bestFor: "Religious workers and faith-based roles",
        link: "https://www.gov.uk/religious-worker-visa",
      },
      {
        name: "Government Authorised Exchange visa",
        workType: "Training, research, fellowship or work experience schemes",
        needsJobOffer: "Yes",
        bestFor: "Applicants on approved exchange or training schemes",
        link: "https://www.gov.uk/government-authorised-exchange",
      },
      {
        name: "International Agreement visa",
        workType: "Work covered by international law or treaty agreements",
        needsJobOffer: "Yes",
        bestFor: "Diplomatic, contractual service or international agreement workers",
        link: "https://www.gov.uk/international-agreement-worker-visa",
      },
    ],
  },
  {
    title: "Specialist Work Routes",
    description: "For sports, religion and specialist international work categories.",
    visas: [
      {
        name: "International Sportsperson visa",
        workType: "Elite sportsperson or qualified sports coach work",
        needsJobOffer: "Yes",
        bestFor: "Professional athletes and sports coaches",
        link: "https://www.gov.uk/sportsperson-visa",
      },
      {
        name: "Minister of Religion visa",
        workType: "Faith leadership and religious ministerial work",
        needsJobOffer: "Yes",
        bestFor: "Ministers, missionaries and religious leaders",
        link: "https://www.gov.uk/minister-of-religion-visa",
      },
      {
        name: "Overseas Domestic Worker visa",
        workType: "Domestic work in a private household",
        needsJobOffer: "Yes",
        bestFor: "Domestic workers accompanying an employer to the UK",
        link: "https://www.gov.uk/overseas-domestic-worker-visa",
      },
    ],
  },
];

const jobExamples = [
  "AI Engineer",
  "Software Engineer",
  "Data Analyst",
  "Cybersecurity Analyst",
  "Cloud Engineer",
  "Business Analyst",
  "Project Manager",
  "Nurse",
  "Doctor",
  "Healthcare Assistant",
  "Care Worker",
  "Teacher",
  "Engineer",
  "Finance and Operations roles",
];

export default function UKVisasPage() {
  return (
    <AuthGate>
      <main className="min-h-screen bg-slate-950 text-white px-6 py-12">
        <div className="max-w-6xl mx-auto space-y-10">
          <section className="space-y-4">
            <p className="text-blue-400 font-semibold">CareerBridge UK</p>
            <h1 className="text-4xl font-bold">UK Visa and Work Route Guide</h1>
            <p className="text-slate-300 max-w-3xl">
              Explore common UK work visa routes, the type of work they support,
              whether a job offer is normally needed, and which route may fit your
              career situation.
            </p>
            <div className="bg-yellow-500/10 border border-yellow-500/30 text-yellow-100 rounded p-5">
              <strong>Important:</strong> This page is for general guidance only.
              It is not legal or immigration advice. Always verify details on GOV.UK
              or speak to a qualified immigration adviser before applying.
            </div>
          </section>

          <section className="grid md:grid-cols-3 gap-5">
            <div className="bg-slate-900 border border-slate-800 rounded p-5">
              <h2 className="text-xl font-semibold">Sponsored Jobs</h2>
              <p className="text-slate-400 mt-2">
                Best for applicants with UK employers who can sponsor visas.
              </p>
            </div>
            <div className="bg-slate-900 border border-slate-800 rounded p-5">
              <h2 className="text-xl font-semibold">No Job Offer Routes</h2>
              <p className="text-slate-400 mt-2">
                Useful for graduates, Global Talent applicants and eligible young people.
              </p>
            </div>
            <div className="bg-slate-900 border border-slate-800 rounded p-5">
              <h2 className="text-xl font-semibold">Founder Routes</h2>
              <p className="text-slate-400 mt-2">
                For entrepreneurs building or expanding innovative businesses in the UK.
              </p>
            </div>
          </section>

          {visaGroups.map((group) => (
            <section key={group.title} className="space-y-5">
              <div>
                <h2 className="text-2xl font-bold">{group.title}</h2>
                <p className="text-slate-400 mt-1">{group.description}</p>
              </div>

              <div className="grid lg:grid-cols-2 gap-5">
                {group.visas.map((visa) => (
                  <div
                    key={visa.name}
                    className="bg-slate-900 border border-slate-800 rounded p-6 space-y-4"
                  >
                    <div>
                      <h3 className="text-xl font-semibold">{visa.name}</h3>
                      <p className="text-slate-400 mt-2">{visa.bestFor}</p>
                    </div>

                    <div className="space-y-2 text-sm">
                      <p>
                        <span className="text-slate-500">Type of work: </span>
                        {visa.workType}
                      </p>
                      <p>
                        <span className="text-slate-500">Job offer needed: </span>
                        {visa.needsJobOffer}
                      </p>
                    </div>

                    <a
                      href={visa.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-block bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded font-semibold"
                    >
                      View GOV.UK Guide
                    </a>
                  </div>
                ))}
              </div>
            </section>
          ))}

          <section className="bg-slate-900 border border-slate-800 rounded p-6 space-y-4">
            <h2 className="text-2xl font-bold">What jobs can users apply for?</h2>
            <div className="grid md:grid-cols-2 gap-4 text-slate-300">
              <ul className="space-y-2 list-disc list-inside">
                {jobExamples.slice(0, 7).map((job) => (
                  <li key={job}>{job}</li>
                ))}
              </ul>
              <ul className="space-y-2 list-disc list-inside">
                {jobExamples.slice(7).map((job) => (
                  <li key={job}>{job}</li>
                ))}
              </ul>
            </div>
            <p className="text-slate-400">
              For sponsored roles, users should check whether the employer is a licensed
              sponsor and whether the job is eligible under the relevant visa route.
            </p>
          </section>
        </div>
      </main>
    </AuthGate>
  );
}
