"use client";

import { useState } from "react";
import { apiPost, endpoints } from "@/lib/api";
import { useRouter } from "next/navigation";
import Link from "next/link";
import ActionButton from "@/components/ActionButton";

export default function RegisterPage() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [isRegistering, setIsRegistering] = useState(false);

  async function register() {
    setMessage("");
    setIsRegistering(true);

    try {
      const data = await apiPost(endpoints.register, { email, password });

      if (!data.access_token) {
        throw new Error("Registration response did not include an access token.");
      }

      localStorage.setItem("token", data.access_token);
      localStorage.setItem("email", data.email || email);
      window.dispatchEvent(new Event("auth-change"));

      router.push("/dashboard");
    } catch (err: unknown) {
      setMessage(err instanceof Error ? err.message : "Registration failed.");
    } finally {
      setIsRegistering(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white px-6 py-16">
      <div className="max-w-md mx-auto bg-slate-900 p-6 rounded-2xl space-y-4">
        <h1 className="text-3xl font-bold">Create Account</h1>

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
          onClick={register}
          pending={isRegistering}
          pendingLabel="Creating account..."
          className="w-full bg-green-600 py-3 rounded font-semibold"
        >
          Register
        </ActionButton>

        {message && <p className="text-slate-300">{message}</p>}

        <Link href="/login" className="text-blue-400">
          Already have an account? Login
        </Link>
      </div>
    </main>
  );
}
