"use client";

import { useState } from "react";
import { apiPost, endpoints } from "@/lib/api";
import Link from "next/link";
import ActionButton from "@/components/ActionButton";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [message, setMessage] = useState("");
  const [codeRequested, setCodeRequested] = useState(false);
  const [pendingAction, setPendingAction] = useState<"code" | "reset" | null>(null);

  async function requestCode() {
    setMessage("");
    setPendingAction("code");

    try {
      const data = await apiPost(endpoints.forgotPassword, { email });
      setCodeRequested(true);
      setMessage(data.message || "If the email exists, a reset code has been sent.");
    } catch (err: unknown) {
      setMessage(err instanceof Error ? err.message : "Could not request reset code.");
    } finally {
      setPendingAction(null);
    }
  }

  async function resetPassword() {
    setMessage("");
    setPendingAction("reset");

    try {
      const data = await apiPost(endpoints.resetPassword, {
        email,
        code,
        new_password: newPassword,
      });
      setMessage(data.message || "Password reset successfully.");
    } catch (err: unknown) {
      setMessage(err instanceof Error ? err.message : "Could not reset password.");
    } finally {
      setPendingAction(null);
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white px-6 py-16">
      <div className="max-w-md mx-auto bg-slate-900 p-6 rounded space-y-4">
        <h1 className="text-3xl font-bold">Reset Password</h1>

        <input
          className="w-full p-3 rounded bg-slate-800 border border-slate-700"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <ActionButton
          onClick={requestCode}
          pending={pendingAction === "code"}
          pendingLabel="Sending..."
          className="w-full bg-blue-600 py-3 rounded font-semibold"
        >
          Send Reset Code
        </ActionButton>

        {codeRequested && (
          <>
            <input
              className="w-full p-3 rounded bg-slate-800 border border-slate-700"
              placeholder="Reset code"
              value={code}
              onChange={(e) => setCode(e.target.value)}
            />

            <input
              className="w-full p-3 rounded bg-slate-800 border border-slate-700"
              placeholder="New password"
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
            />

            <ActionButton
              onClick={resetPassword}
              pending={pendingAction === "reset"}
              pendingLabel="Resetting..."
              className="w-full bg-green-600 py-3 rounded font-semibold"
            >
              Reset Password
            </ActionButton>
          </>
        )}

        {message && <p className="text-slate-300">{message}</p>}

        <Link href="/login" className="block text-blue-400">
          Back to login
        </Link>
      </div>
    </main>
  );
}
