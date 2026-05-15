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
  const [mode, setMode] = useState<ThemeMode>("system");

  useEffect(() => {
    const savedMode = getInitialMode();
    const mediaQuery = window.matchMedia("(prefers-color-scheme: light)");

    applyTheme(savedMode);

    if (savedMode !== "system") {
      window.setTimeout(() => setMode(savedMode), 0);
    }

    function handleSystemThemeChange() {
      const currentMode = window.localStorage.getItem("theme-mode");

      if (!currentMode || currentMode === "system") {
        applyTheme("system");
      }
    }

    mediaQuery.addEventListener("change", handleSystemThemeChange);
    return () => mediaQuery.removeEventListener("change", handleSystemThemeChange);
  }, []);

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
