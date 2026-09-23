"use client";

import { useRouter } from "next/navigation";
import { createContext, useContext, useEffect, useMemo, useState } from "react";

import type { User } from "@/lib/api";

export const DEMO_TOKEN = "workforceiq-demo-session";
export const DEMO_USER: User = {
  id: 1,
  email: "demo@workforceiq.app",
  full_name: "Alex Morgan",
  is_active: true,
  role: {
    id: 1,
    name: "HR Administrator",
    description: "Demo workspace administrator",
  },
  employee_id: null,
  created_at: "2025-01-01T00:00:00Z",
};

type AuthContextValue = {
  ready: boolean;
  token: string | null;
  user: User | null;
  setSession: (token: string, user: User) => void;
  clearSession: () => void;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [ready, setReady] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const storedToken = window.localStorage.getItem("workforceiq_token");
    const storedUser = window.localStorage.getItem("workforceiq_user");
    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
    }
    setReady(true);
  }, []);

  const value = useMemo<AuthContextValue>(
    () => ({
      ready,
      token,
      user,
      setSession(nextToken, nextUser) {
        window.localStorage.setItem("workforceiq_token", nextToken);
        window.localStorage.setItem("workforceiq_user", JSON.stringify(nextUser));
        setToken(nextToken);
        setUser(nextUser);
      },
      clearSession() {
        window.localStorage.removeItem("workforceiq_token");
        window.localStorage.removeItem("workforceiq_user");
        setToken(null);
        setUser(null);
        router.push("/login");
      },
    }),
    [ready, router, token, user],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
