const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "https://career-bridge-uk.onrender.com";

export async function apiPost(path: string, data: unknown, token?: string) {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify(data),
  }).catch(() => {
    throw new Error("Could not reach the API. Check the backend URL and CORS settings.");
  });

  const text = await res.text();

  let result: any = null;

  try {
    result = text ? JSON.parse(text) : null;
  } catch {
    result = text;
  }

  if (!res.ok) {
    throw new Error(
      result?.detail ||
        result?.message ||
        JSON.stringify(result) ||
        `Request failed with status ${res.status}`
    );
  }

  return result;
}

export async function apiGet(path: string, token?: string) {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
  }).catch(() => {
    throw new Error("Could not reach the API. Check the backend URL and CORS settings.");
  });

  const text = await res.text();

  let result: any = null;

  try {
    result = text ? JSON.parse(text) : null;
  } catch {
    result = text;
  }

  if (!res.ok) {
    throw new Error(
      result?.detail ||
        result?.message ||
        JSON.stringify(result) ||
        `Request failed with status ${res.status}`
    );
  }

  return result;
}

export const endpoints = {
  register: "/api/auth/register",
  login: "/api/auth/login",
  forgotPassword: "/api/auth/forgot-password",
  resetPassword: "/api/auth/reset-password",

  analyzeCv: "/api/cv/analyze",
  generateCv: "/api/cv/generate",
  generateCvFromAnalysis: "/api/cv/generate-from-analysis",

  prepareInterview: "/api/interview/prepare",
  mockInterview: "/api/interview/mock",

  matchJobs: "/api/jobs/match",
  searchJobs: "/api/jobs/search",

  saveResult: "/api/results/save",
  getResults: "/api/results/",
};