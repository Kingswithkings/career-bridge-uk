"use client";

import { type ChangeEvent, useState } from "react";
import { apiPost, endpoints } from "@/lib/api";
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

const fallbackCountryOptions = [
  "Australia",
  "Canada",
  "Denmark",
  "Finland",
  "France",
  "Germany",
  "Ghana",
  "India",
  "Ireland",
  "Italy",
  "Netherlands",
  "Nigeria",
  "Norway",
  "Poland",
  "Portugal",
  "Singapore",
  "South Africa",
  "Spain",
  "Sweden",
  "Switzerland",
  "United Arab Emirates",
  "United Kingdom",
  "United States",
];

const majorCityOptions = [
  "London, United Kingdom",
  "Manchester, United Kingdom",
  "Birmingham, United Kingdom",
  "Leeds, United Kingdom",
  "Glasgow, United Kingdom",
  "Edinburgh, United Kingdom",
  "Bristol, United Kingdom",
  "Liverpool, United Kingdom",
  "Sheffield, United Kingdom",
  "Cardiff, United Kingdom",
  "Belfast, United Kingdom",
  "New York, United States",
  "San Francisco, United States",
  "Los Angeles, United States",
  "Chicago, United States",
  "Austin, United States",
  "Seattle, United States",
  "Boston, United States",
  "Toronto, Canada",
  "Vancouver, Canada",
  "Montreal, Canada",
  "Calgary, Canada",
  "Sydney, Australia",
  "Melbourne, Australia",
  "Brisbane, Australia",
  "Perth, Australia",
  "Dublin, Ireland",
  "Cork, Ireland",
  "Berlin, Germany",
  "Munich, Germany",
  "Hamburg, Germany",
  "Paris, France",
  "Lyon, France",
  "Amsterdam, Netherlands",
  "Rotterdam, Netherlands",
  "Madrid, Spain",
  "Barcelona, Spain",
  "Rome, Italy",
  "Milan, Italy",
  "Lisbon, Portugal",
  "Zurich, Switzerland",
  "Geneva, Switzerland",
  "Stockholm, Sweden",
  "Oslo, Norway",
  "Copenhagen, Denmark",
  "Helsinki, Finland",
  "Warsaw, Poland",
  "Bengaluru, India",
  "Mumbai, India",
  "Delhi, India",
  "Hyderabad, India",
  "Singapore, Singapore",
  "Dubai, United Arab Emirates",
  "Abu Dhabi, United Arab Emirates",
  "Johannesburg, South Africa",
  "Cape Town, South Africa",
  "Lagos, Nigeria",
  "Abuja, Nigeria",
  "Accra, Ghana",
];

function getCountryOptions() {
  if (typeof Intl.supportedValuesOf !== "function") {
    return fallbackCountryOptions;
  }

  const displayNames = new Intl.DisplayNames(["en"], { type: "region" });

  return Intl.supportedValuesOf("region")
    .map((regionCode) => displayNames.of(regionCode))
    .filter((countryName): countryName is string => Boolean(countryName))
    .sort((countryA, countryB) => countryA.localeCompare(countryB));
}

const locationOptions = Array.from(new Set([...getCountryOptions(), ...majorCityOptions]));

export default function JobsPage() {
  const router = useRouter();

  const [role, setRole] = useState("");
  const [location, setLocation] = useState("United Kingdom");
  const [cvText, setCvText] = useState("");
  const [cvFileName, setCvFileName] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState("");
  const [lastFeatureType, setLastFeatureType] = useState("");
  const [lastResultText, setLastResultText] = useState("");
  const [pendingAction, setPendingAction] = useState<"search" | "match" | "save" | null>(null);

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
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    const isTextFile =
      file.type.startsWith("text/") ||
      /\.(txt|md|markdown|rtf)$/i.test(file.name);

    if (!isTextFile) {
      setResult("Please upload a text CV file for now, or paste your CV text below.");
      event.target.value = "";
      return;
    }

    try {
      const text = await file.text();
      setCvText(text);
      setCvFileName(file.name);
      setResult(`${file.name} uploaded. You can now match your CV to a job.`);
    } catch {
      setResult("Could not read that CV file. Please paste your CV text below.");
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
          location,
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
          location,
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
          location,
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
          placeholder="Role e.g. AI Engineer"
          value={role}
          onChange={(e) => setRole(e.target.value)}
        />
        <datalist id="job-role-options">
          {jobRoleOptions.map((option) => (
            <option key={option} value={option} />
          ))}
        </datalist>

        <input
          className="w-full p-3 rounded bg-slate-800 border border-slate-700"
          list="job-location-options"
          placeholder="Location"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />
        <datalist id="job-location-options">
          {locationOptions.map((option) => (
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
            accept=".txt,.md,.markdown,.rtf,text/plain,text/markdown,text/rtf"
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
