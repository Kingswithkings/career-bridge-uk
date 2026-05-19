const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "https://career-bridge-uk.onrender.com";
const REQUEST_TIMEOUT_MS = 15000;
const AI_REQUEST_TIMEOUT_MS = 120000;
const AI_ENDPOINTS = new Set([
  "/api/cv/analyze",
  "/api/cv/generate",
  "/api/cv/generate-from-analysis",
  "/api/interview/prepare",
  "/api/interview/mock",
  "/api/jobs/match",
]);

type ApiErrorResponse = {
  detail?: string;
  message?: string;
};

type ApiResponse = Record<string, unknown> & {
  access_token?: string;
  email?: string;
  message?: string;
};

function parseErrorMessage(result: unknown, status: number) {
  if (typeof result === "object" && result !== null) {
    const response = result as ApiErrorResponse;
    return response.detail || response.message || JSON.stringify(result);
  }

  if (typeof result === "string" && result) {
    return result;
  }

  return `Request failed with status ${status}`;
}

export async function apiPost(path: string, data: unknown, token?: string): Promise<ApiResponse> {
  const controller = new AbortController();
  const isAiEndpoint = AI_ENDPOINTS.has(path);
  const timeoutMs = isAiEndpoint ? AI_REQUEST_TIMEOUT_MS : REQUEST_TIMEOUT_MS;
  const timeoutId = window.setTimeout(() => controller.abort(), timeoutMs);

  const res = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    signal: controller.signal,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify(data),
  })
    .catch((error: unknown) => {
      if (error instanceof DOMException && error.name === "AbortError") {
        throw new Error(
          isAiEndpoint
            ? "The AI response took too long. Please try again with a shorter CV or job description."
            : "The API took too long to respond. Please try again.",
        );
      }

      throw new Error("Could not reach the API. Check the backend URL and CORS settings.");
    })
    .finally(() => window.clearTimeout(timeoutId));

  const text = await res.text();

  let result: unknown = null;

  try {
    result = text ? JSON.parse(text) : null;
  } catch {
    result = text;
  }

  if (!res.ok) {
    throw new Error(parseErrorMessage(result, res.status));
  }

  return result as ApiResponse;
}

export async function apiUploadFile(path: string, file: File, token?: string): Promise<ApiResponse> {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    signal: controller.signal,
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: formData,
  })
    .catch((error: unknown) => {
      if (error instanceof DOMException && error.name === "AbortError") {
        throw new Error("The API took too long to read that file. Please try again.");
      }

      throw new Error("Could not reach the API. Check the backend URL and CORS settings.");
    })
    .finally(() => window.clearTimeout(timeoutId));

  const text = await res.text();

  let result: unknown = null;

  try {
    result = text ? JSON.parse(text) : null;
  } catch {
    result = text;
  }

  if (!res.ok) {
    throw new Error(parseErrorMessage(result, res.status));
  }

  return result as ApiResponse;
}

export async function apiGet(path: string, token?: string): Promise<ApiResponse> {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  const res = await fetch(`${API_BASE_URL}${path}`, {
    signal: controller.signal,
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
  })
    .catch((error: unknown) => {
      if (error instanceof DOMException && error.name === "AbortError") {
        throw new Error("The API took too long to respond. Please try again.");
      }

      throw new Error("Could not reach the API. Check the backend URL and CORS settings.");
    })
    .finally(() => window.clearTimeout(timeoutId));

  const text = await res.text();

  let result: unknown = null;

  try {
    result = text ? JSON.parse(text) : null;
  } catch {
    result = text;
  }

  if (!res.ok) {
    throw new Error(parseErrorMessage(result, res.status));
  }

  return result as ApiResponse;
}

export const endpoints = {
  register: "/api/auth/register",
  login: "/api/auth/login",
  forgotPassword: "/api/auth/forgot-password",
  resetPassword: "/api/auth/reset-password",

  analyzeCv: "/api/cv/analyze",
  uploadCv: "/api/cv/upload",
  generateCv: "/api/cv/generate",
  generateCvFromAnalysis: "/api/cv/generate-from-analysis",

  prepareInterview: "/api/interview/prepare",
  mockInterview: "/api/interview/mock",

  matchJobs: "/api/jobs/match",
  searchJobs: "/api/jobs/search",

  saveResult: "/api/results/save",
  getResults: "/api/results/",
};
