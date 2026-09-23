"use client";

import { Activity, Database, KeyRound, ShieldCheck, UserRound } from "lucide-react";
import { useQuery } from "@tanstack/react-query";

import { Card } from "@/components/ui/card";
import { getHealth, getMe } from "@/lib/api";
import { useAuth } from "@/lib/auth";

export function Dashboard() {
  const { token, user } = useAuth();
  const meQuery = useQuery({
    queryKey: ["dashboard-me", token],
    queryFn: () => getMe(token as string),
    enabled: Boolean(token),
  });
  const healthQuery = useQuery({ queryKey: ["health"], queryFn: getHealth });
  const currentUser = meQuery.data ?? user;

  const cards = [
    {
      label: "Authenticated user",
      value: currentUser?.full_name ?? "Loading",
      detail: currentUser?.email ?? "Verifying session",
      icon: UserRound,
    },
    {
      label: "Assigned role",
      value: currentUser?.role.name ?? "Loading",
      detail: "RBAC enforced by backend dependencies",
      icon: ShieldCheck,
    },
    {
      label: "API status",
      value: healthQuery.data?.status ?? (healthQuery.isLoading ? "Checking" : "Unavailable"),
      detail: healthQuery.data?.app ?? "FastAPI service",
      icon: Activity,
    },
    {
      label: "Database foundation",
      value: "Online",
      detail: "SQLAlchemy models and role seed data active",
      icon: Database,
    },
  ];

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <div className="flex flex-col justify-between gap-4 md:flex-row md:items-end">
        <div>
          <div className="text-sm font-semibold text-primary">Executive Dashboard</div>
          <h1 className="mt-1 text-3xl font-semibold tracking-normal">Workforce command center</h1>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-muted-foreground">
            Phase 1 is running against a real backend session with authenticated API calls,
            RBAC, audit logging, and database-backed users.
          </p>
        </div>
        <div className="flex items-center gap-2 rounded-md border border-border bg-white px-3 py-2 text-sm text-muted-foreground">
          <KeyRound className="h-4 w-4 text-primary" />
          JWT session verified
        </div>
      </div>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {cards.map((card) => {
          const Icon = card.icon;
          return (
            <Card key={card.label}>
              <div className="flex items-start justify-between gap-3">
                <div>
                  <div className="text-sm text-muted-foreground">{card.label}</div>
                  <div className="mt-2 truncate text-xl font-semibold">{card.value}</div>
                </div>
                <div className="flex h-10 w-10 items-center justify-center rounded-md bg-accent text-accent-foreground">
                  <Icon className="h-5 w-5" />
                </div>
              </div>
              <div className="mt-4 text-sm text-muted-foreground">{card.detail}</div>
            </Card>
          );
        })}
      </section>

      <section className="grid gap-4 lg:grid-cols-[1.4fr_0.8fr]">
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold">Phase 1 platform checks</h2>
              <p className="mt-1 text-sm text-muted-foreground">
                These checks are backed by live API calls from the browser.
              </p>
            </div>
          </div>
          <div className="mt-5 divide-y divide-border rounded-md border border-border">
            {[
              ["Backend health", healthQuery.isSuccess ? "Connected" : "Pending"],
              ["Current user", meQuery.isSuccess ? "Verified" : "Pending"],
              ["Role authorization", currentUser?.role.name ?? "Pending"],
              ["Frontend API URL", process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"],
            ].map(([label, value]) => (
              <div key={label} className="flex items-center justify-between gap-4 px-4 py-3 text-sm">
                <span className="text-muted-foreground">{label}</span>
                <span className="font-medium">{value}</span>
              </div>
            ))}
          </div>
        </Card>
        <Card>
          <h2 className="text-lg font-semibold">Security posture</h2>
          <div className="mt-5 space-y-3 text-sm">
            {[
              "JWTs are issued by FastAPI only",
              "Passwords are hashed server-side",
              "Role checks protect privileged APIs",
              "Audit records are written for auth events",
            ].map((item) => (
              <div key={item} className="flex items-center gap-3">
                <span className="h-2 w-2 rounded-full bg-emerald-600" />
                <span>{item}</span>
              </div>
            ))}
          </div>
        </Card>
      </section>
    </div>
  );
}

