"use client";

import { useState } from "react";
import { apiPost, endpoints } from "@/lib/api";
import { useRouter } from "next/navigation";
import Link from "next/link";
import ActionButton from "@/components/ActionButton";

export default function LoginPage() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [isLoggingIn, setIsLoggingIn] = useState(false);

  async function login() {
    setMessage("");
    setIsLoggingIn(true);

    try {
      const data = await apiPost(endpoints.login, { email, password });

      if (!data.access_token) {
        throw new Error("Login response did not include an access token.");
      }

      localStorage.setItem("token", data.access_token);
      localStorage.setItem("email", email);
      window.dispatchEvent(new Event("auth-change"));

      router.push("/dashboard");
    } catch (err: unknown) {
      setMessage(err instanceof Error ? err.message : "Invalid email or password.");
    } finally {
      setIsLoggingIn(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white px-6 py-16">
      <div className="max-w-md mx-auto bg-slate-900 p-6 rounded-2xl space-y-4">
        <h1 className="text-3xl font-bold">Login</h1>

        <input
          className="w-full p-3 rounded bg-slate-800 border border-slate-700"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          className="w-full p-3 rounded bg-slate-800 border border-slate-700"
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <ActionButton
          onClick={login}
          pending={isLoggingIn}
          pendingLabel="Logging in..."
          className="w-full bg-blue-600 py-3 rounded font-semibold"
        >
          Login
        </ActionButton>

        {message && <p className="text-red-400">{message}</p>}

        <Link href="/forgot-password" className="block text-blue-400">
          Forgot password?
        </Link>

        <Link href="/register" className="block text-blue-400">
          Need an account? Register
        </Link>
      </div>
    </main>
  );
}
