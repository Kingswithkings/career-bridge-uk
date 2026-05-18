"use client";

import { type ChangeEvent, useState } from "react";
import { apiPost, apiUploadFile, endpoints } from "@/lib/api";
import { useRouter } from "next/navigation";
import AuthGate from "@/components/AuthGate";
import ResultPanel from "@/components/ResultPanel";
import ActionButton from "@/components/ActionButton";

const jobRoleOptions = [
  "Accountant",
  "Administrative Assistant",
  "AI Engineer",
  "Android Developer",
  "Backend Developer",
  "Business Analyst",
  "Care Assistant",
  "Civil Engineer",
  "Cloud Engineer",
  "Content Designer",
  "Customer Service Advisor",
  "Cyber Security Analyst",
  "Data Analyst",
  "Data Engineer",
  "Data Scientist",
  "Delivery Driver",
  "DevOps Engineer",
  "Digital Marketing Manager",
  "Doctor",
  "Electrician",
  "Finance Analyst",
  "Frontend Developer",
  "Full Stack Developer",
  "Graphic Designer",
  "Healthcare Assistant",
  "HR Advisor",
  "iOS Developer",
  "IT Support Analyst",
  "Java Developer",
  "Machine Learning Engineer",
  "Marketing Executive",
  "Mechanical Engineer",
  "Nurse",
  "Operations Manager",
  "Pharmacist",
  "Product Manager",
  "Project Manager",
  "Python Developer",
  "QA Engineer",
  "React Developer",
  "Recruiter",
  "Sales Executive",
  "Scrum Master",
  "Security Officer",
  "Software Engineer",
  "Teacher",
  "UX Designer",
  "Warehouse Operative",
  "Web Developer",
];

const ukJobRoleOptions = [
  "Accounts Assistant",
  "Accounts Payable Clerk",
  "Accounts Receivable Clerk",
  "Actuary",
  "Adult Social Worker",
  "Advertising Account Executive",
  "Aerospace Engineer",
  "Agricultural Engineer",
  "Architect",
  "Architectural Technologist",
  "Audit Associate",
  "Audit Manager",
  "Automotive Technician",
  "Barrister",
  "Bid Manager",
  "Biomedical Scientist",
  "Bookkeeper",
  "Branch Manager",
  "Building Surveyor",
  "Bus Driver",
  "Business Development Manager",
  "Buyer",
  "Carer",
  "Carpenter",
  "Case Worker",
  "Chef",
  "Children's Social Worker",
  "Clinical Psychologist",
  "Compliance Analyst",
  "Compliance Manager",
  "Construction Manager",
  "Copywriter",
  "Credit Controller",
  "Data Protection Officer",
  "Database Administrator",
  "Dental Nurse",
  "Dentist",
  "Design Engineer",
  "Digital Project Manager",
  "Early Years Practitioner",
  "Education Support Worker",
  "Electrical Engineer",
  "Employment Advisor",
  "Estimator",
  "Facilities Manager",
  "Financial Adviser",
  "Financial Controller",
  "Fire Safety Officer",
  "Forklift Driver",
  "Graduate Trainee",
  "Health and Safety Advisor",
  "Helpdesk Analyst",
  "Housing Officer",
  "Immigration Advisor",
  "Insurance Broker",
  "Lab Technician",
  "Learning Support Assistant",
  "Legal Assistant",
  "Legal Secretary",
  "Management Accountant",
  "Manufacturing Engineer",
  "Marketing Manager",
  "Mental Health Nurse",
  "Midwife",
  "Network Engineer",
  "Occupational Therapist",
  "Office Manager",
  "Paralegal",
  "Payroll Administrator",
  "Personal Assistant",
  "Physiotherapist",
  "Planning Officer",
  "Plumber",
  "Police Officer",
  "Procurement Manager",
  "Quantity Surveyor",
  "Radiographer",
  "Receptionist",
  "Registered Manager",
  "Retail Assistant",
  "Retail Manager",
  "Risk Analyst",
  "School Administrator",
  "Secondary School Teacher",
  "Site Manager",
  "Solicitor",
  "Support Worker",
  "Systems Analyst",
  "Teaching Assistant",
  "Technical Architect",
  "Technical Support Engineer",
  "Town Planner",
  "Train Driver",
  "Transport Planner",
  "Vehicle Technician",
  "Veterinary Nurse",
  "Welder",
];

const roleOptions = Array.from(new Set([...jobRoleOptions, ...ukJobRoleOptions])).sort(
  (roleA, roleB) => roleA.localeCompare(roleB)
);

const countryRegionCodes = [
  "AF",
  "AX",
  "AL",
  "DZ",
  "AS",
  "AD",
  "AO",
  "AI",
  "AQ",
  "AG",
  "AR",
  "AM",
  "AW",
  "AU",
  "AT",
  "AZ",
  "BS",
  "BH",
  "BD",
  "BB",
  "BY",
  "BE",
  "BZ",
  "BJ",
  "BM",
  "BT",
  "BO",
  "BQ",
  "BA",
  "BW",
  "BV",
  "BR",
  "IO",
  "BN",
  "BG",
  "BF",
  "BI",
  "CV",
  "KH",
  "CM",
  "CA",
  "KY",
  "CF",
  "TD",
  "CL",
  "CN",
  "CX",
  "CC",
  "CO",
  "KM",
  "CG",
  "CD",
  "CK",
  "CR",
  "CI",
  "HR",
  "CU",
  "CW",
  "CY",
  "CZ",
  "DK",
  "DJ",
  "DM",
  "DO",
  "EC",
  "EG",
  "SV",
  "GQ",
  "ER",
  "EE",
  "SZ",
  "ET",
  "FK",
  "FO",
  "FJ",
  "FI",
  "FR",
  "GF",
  "PF",
  "TF",
  "GA",
  "GM",
  "GE",
  "DE",
  "GH",
  "GI",
  "GR",
  "GL",
  "GD",
  "GP",
  "GU",
  "GT",
  "GG",
  "GN",
  "GW",
  "GY",
  "HT",
  "HM",
  "VA",
  "HN",
  "HK",
  "HU",
  "IS",
  "IN",
  "ID",
  "IR",
  "IQ",
  "IE",
  "IM",
  "IL",
  "IT",
  "JM",
  "JP",
  "JE",
  "JO",
  "KZ",
  "KE",
  "KI",
  "KP",
  "KR",
  "KW",
  "KG",
  "LA",
  "LV",
  "LB",
  "LS",
  "LR",
  "LY",
  "LI",
  "LT",
  "LU",
  "MO",
  "MG",
  "MW",
  "MY",
  "MV",
  "ML",
  "MT",
  "MH",
  "MQ",
  "MR",
  "MU",
  "YT",
  "MX",
  "FM",
  "MD",
  "MC",
  "MN",
  "ME",
  "MS",
  "MA",
  "MZ",
  "MM",
  "NA",
  "NR",
  "NP",
  "NL",
  "NC",
  "NZ",
  "NI",
  "NE",
  "NG",
  "NU",
  "NF",
  "MK",
  "MP",
  "NO",
  "OM",
  "PK",
  "PW",
  "PS",
  "PA",
  "PG",
  "PY",
  "PE",
  "PH",
  "PN",
  "PL",
  "PT",
  "PR",
  "QA",
  "RE",
  "RO",
  "RU",
  "RW",
  "BL",
  "SH",
  "KN",
  "LC",
  "MF",
  "PM",
  "VC",
  "WS",
  "SM",
  "ST",
  "SA",
  "SN",
  "RS",
  "SC",
  "SL",
  "SG",
  "SX",
  "SK",
  "SI",
  "SB",
  "SO",
  "ZA",
  "GS",
  "SS",
  "ES",
  "LK",
  "SD",
  "SR",
  "SJ",
  "SE",
  "CH",
  "SY",
  "TW",
  "TJ",
  "TZ",
  "TH",
  "TL",
  "TG",
  "TK",
  "TO",
  "TT",
  "TN",
  "TR",
  "TM",
  "TC",
  "TV",
  "UG",
  "UA",
  "AE",
  "GB",
  "US",
  "UM",
  "UY",
  "UZ",
  "VU",
  "VE",
  "VN",
  "VG",
  "VI",
  "WF",
  "EH",
  "YE",
  "ZM",
  "ZW",
];

const countryNames = new Intl.DisplayNames(["en"], { type: "region" });
const countryOptions = countryRegionCodes
  .map((regionCode) => countryNames.of(regionCode))
  .filter((countryName): countryName is string => Boolean(countryName))
  .sort((countryA, countryB) => countryA.localeCompare(countryB));

const cityOptionsByCountry: Record<string, string[]> = {
  Australia: ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Canberra"],
  Canada: ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", "Edmonton"],
  France: ["Paris", "Lyon", "Marseille", "Toulouse", "Nice", "Bordeaux"],
  Germany: ["Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne", "Stuttgart"],
  Ghana: ["Accra", "Kumasi", "Tamale", "Takoradi", "Cape Coast"],
  India: ["Bengaluru", "Mumbai", "Delhi", "Hyderabad", "Chennai", "Pune"],
  Ireland: ["Dublin", "Cork", "Galway", "Limerick", "Waterford"],
  Italy: ["Rome", "Milan", "Naples", "Turin", "Florence", "Bologna"],
  Netherlands: ["Amsterdam", "Rotterdam", "The Hague", "Utrecht", "Eindhoven"],
  Nigeria: ["Lagos", "Abuja", "Port Harcourt", "Ibadan", "Kano"],
  Portugal: ["Lisbon", "Porto", "Braga", "Coimbra", "Faro"],
  Singapore: ["Singapore"],
  "South Africa": ["Johannesburg", "Cape Town", "Durban", "Pretoria", "Gqeberha"],
  Spain: ["Madrid", "Barcelona", "Valencia", "Seville", "Bilbao"],
  Switzerland: ["Zurich", "Geneva", "Basel", "Bern", "Lausanne"],
  "United Arab Emirates": ["Dubai", "Abu Dhabi", "Sharjah", "Ajman"],
  "United Kingdom": [
    "Remote",
    "Hybrid",
    "London",
    "Manchester",
    "Birmingham",
    "Leeds",
    "Glasgow",
    "Edinburgh",
    "Bristol",
    "Liverpool",
    "Sheffield",
    "Cardiff",
    "Belfast",
    "Aberdeen",
    "Bath",
    "Blackpool",
    "Bolton",
    "Bournemouth",
    "Bradford",
    "Brighton",
    "Cambridge",
    "Canterbury",
    "Chelmsford",
    "Coventry",
    "Derby",
    "Dundee",
    "Exeter",
    "Hull",
    "Inverness",
    "Leicester",
    "Luton",
    "Milton Keynes",
    "Newcastle upon Tyne",
    "Norwich",
    "Nottingham",
    "Oxford",
    "Peterborough",
    "Plymouth",
    "Portsmouth",
    "Preston",
    "Reading",
    "Southampton",
    "Stoke-on-Trent",
    "Sunderland",
    "Swansea",
    "Wakefield",
    "Wolverhampton",
    "York",
  ],
  "United States": ["New York", "San Francisco", "Los Angeles", "Chicago", "Austin", "Seattle"],
};

export default function JobsPage() {
  const router = useRouter();

  const [role, setRole] = useState("");
  const [country, setCountry] = useState("");
  const [city, setCity] = useState("");
  const [cvText, setCvText] = useState("");
  const [cvFileName, setCvFileName] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState("");
  const [lastFeatureType, setLastFeatureType] = useState("");
  const [lastResultText, setLastResultText] = useState("");
  const [pendingAction, setPendingAction] = useState<"search" | "match" | "save" | null>(null);
  const cityOptions = cityOptionsByCountry[country] || [];

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

  function getLocation() {
    return [city.trim(), country.trim()].filter(Boolean).join(", ");
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
      setResult(`${file.name} uploaded. You can now match your CV to a job.`);
    } catch (err: unknown) {
      setResult(err instanceof Error ? err.message : "Could not read that CV file.");
    }
  }

  async function searchJobs() {
    const token = requireToken();

    if (!token) {
      return;
    }

    setResult("Searching jobs...");
    setPendingAction("search");

    try {
      const data = await apiPost(
        endpoints.searchJobs,
        {
          query: role,
          location: getLocation(),
        },
        token
      );

      showResult(data, "job_search");
    } catch (err: unknown) {
      setResult(err instanceof Error ? err.message : "Job search failed.");
    } finally {
      setPendingAction(null);
    }
  }

  async function matchJob() {
    const token = requireToken();

    if (!token) {
      return;
    }

    setResult("Matching candidate to job...");
    setPendingAction("match");

    try {
      const data = await apiPost(
        endpoints.matchJobs,
        {
          cv_text: cvText,
          target_role: role,
          job_description: jobDescription,
          location: getLocation(),
        },
        token
      );

      showResult(data, "job_match");
    } catch (err: unknown) {
      setResult(err instanceof Error ? err.message : "Job match failed.");
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
          feature_type: lastFeatureType || "jobs",
          target_role: role,
          location: getLocation(),
          input_text: cvText || jobDescription || role,
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
        <h1 className="text-4xl font-bold">Jobs</h1>

        <input
          className="w-full p-3 rounded bg-slate-800 border border-slate-700"
          list="job-role-options"
          placeholder="Job role e.g. Software Engineer"
          value={role}
          onChange={(e) => setRole(e.target.value)}
        />
        <datalist id="job-role-options">
          {roleOptions.map((option) => (
            <option key={option} value={option} />
          ))}
        </datalist>

        <div className="grid gap-4 md:grid-cols-2">
          <input
            className="w-full p-3 rounded bg-slate-800 border border-slate-700"
            list="job-country-options"
            placeholder="Country e.g. United Kingdom"
            value={country}
            onChange={(e) => {
              setCountry(e.target.value);
              setCity("");
            }}
          />

          <input
            className="w-full p-3 rounded bg-slate-800 border border-slate-700"
            list="job-city-options"
            placeholder="City e.g. London"
            value={city}
            onChange={(e) => setCity(e.target.value)}
          />
        </div>

        <datalist id="job-country-options">
          {countryOptions.map((option) => (
            <option key={option} value={option} />
          ))}
        </datalist>
        <datalist id="job-city-options">
          {cityOptions.map((option) => (
            <option key={option} value={option} />
          ))}
        </datalist>

        <ActionButton
          onClick={searchJobs}
          pending={pendingAction === "search"}
          pendingLabel="Searching..."
          className="bg-blue-600 px-5 py-3 rounded"
        >
          Search Jobs
        </ActionButton>

        <div className="rounded border border-slate-700 bg-slate-900 p-4">
          <label className="block text-sm font-semibold text-slate-200" htmlFor="jobs-cv-upload">
            Upload CV
          </label>
          <input
            id="jobs-cv-upload"
            type="file"
            accept=".pdf,.docx,.txt,.md,.markdown,.rtf,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,text/plain,text/markdown,text/rtf"
            onChange={uploadCv}
            className="mt-3 block w-full cursor-pointer rounded bg-slate-800 text-sm text-slate-300 file:mr-4 file:cursor-pointer file:border-0 file:bg-blue-600 file:px-4 file:py-3 file:font-semibold file:text-white"
          />
          {cvFileName && <p className="mt-2 text-sm text-slate-400">Loaded: {cvFileName}</p>}
        </div>

        <textarea
          className="w-full p-3 rounded bg-slate-800 border border-slate-700 min-h-44"
          placeholder="Paste CV text for job match..."
          value={cvText}
          onChange={(e) => setCvText(e.target.value)}
        />

        <textarea
          className="w-full p-3 rounded bg-slate-800 border border-slate-700 min-h-44"
          placeholder="Paste job description..."
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
        />

        <ActionButton
          onClick={matchJob}
          pending={pendingAction === "match"}
          pendingLabel="Matching..."
          className="bg-green-600 px-5 py-3 rounded"
        >
          Match Candidate To Job
        </ActionButton>

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
