const API_BASE_URL = "";

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

  const result = await res.json().catch(() => null);

  if (!res.ok) {
    throw new Error(result?.detail || "Request failed");
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

  const result = await res.json().catch(() => null);

  if (!res.ok) {
    throw new Error(result?.detail || "Request failed");
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
  getResults: "/api/results",
};
