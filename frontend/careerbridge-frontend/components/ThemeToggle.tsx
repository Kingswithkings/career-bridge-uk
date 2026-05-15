"use client";

import { useEffect, useState } from "react";

type ThemeMode = "system" | "light" | "dark";
type ResolvedTheme = "light" | "dark";

function getSystemTheme(): ResolvedTheme {
  if (typeof window === "undefined") {
    return "dark";
  }

  return window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
}

function getInitialMode(): ThemeMode {
  if (typeof window === "undefined") {
    return "system";
  }

  const savedTheme = window.localStorage.getItem("theme-mode");

  if (savedTheme === "system" || savedTheme === "light" || savedTheme === "dark") {
    return savedTheme;
  }

  return "system";
}

function resolveTheme(mode: ThemeMode): ResolvedTheme {
  return mode === "system" ? getSystemTheme() : mode;
}

function applyTheme(mode: ThemeMode) {
  document.documentElement.dataset.themeMode = mode;
  document.documentElement.dataset.theme = resolveTheme(mode);
}

export default function ThemeToggle() {
  const [mode, setMode] = useState<ThemeMode>(getInitialMode);

  useEffect(() => {
    applyTheme(mode);

    if (mode !== "system") {
      return;
    }

    const mediaQuery = window.matchMedia("(prefers-color-scheme: light)");
    const handleChange = () => applyTheme("system");

    mediaQuery.addEventListener("change", handleChange);
    return () => mediaQuery.removeEventListener("change", handleChange);
  }, [mode]);

  function selectMode(nextMode: ThemeMode) {
    setMode(nextMode);
    window.localStorage.setItem("theme-mode", nextMode);
    applyTheme(nextMode);
  }

  return (
    <div className="theme-mode-control" aria-label="Theme setting">
      {(["system", "light", "dark"] as const).map((themeMode) => (
        <button
          key={themeMode}
          type="button"
          onClick={() => selectMode(themeMode)}
          className="theme-toggle"
          aria-pressed={mode === themeMode}
        >
          {themeMode[0].toUpperCase() + themeMode.slice(1)}
        </button>
      ))}
    </div>
  );
}
