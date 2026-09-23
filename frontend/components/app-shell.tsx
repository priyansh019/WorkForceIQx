"use client";

import {
  BarChart3,
  Bell,
  Bot,
  BriefcaseBusiness,
  Building2,
  FileText,
  GraduationCap,
  LayoutDashboard,
  LogOut,
  Network,
  Search,
  Settings,
  ShieldCheck,
  Sparkles,
  Users,
} from "lucide-react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect } from "react";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { getMe } from "@/lib/api";
import { DEMO_TOKEN, useAuth } from "@/lib/auth";
import { useQuery } from "@tanstack/react-query";

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/employees", label: "Employees", icon: Users },
  { href: "/recruitment", label: "Recruitment", icon: BriefcaseBusiness },
  { href: "/onboarding", label: "Onboarding", icon: GraduationCap },
  { href: "/policies", label: "Policies", icon: ShieldCheck },
  { href: "/performance", label: "Performance", icon: BarChart3 },
  { href: "/skills", label: "Skills", icon: Network },
  { href: "/insights", label: "Workforce Insights", icon: Sparkles },
  { href: "/recommendations", label: "Recommendations", icon: Bell },
  { href: "/documents", label: "Documents", icon: FileText },
  { href: "/settings", label: "Settings", icon: Settings },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const { ready, token, user, setSession, clearSession } = useAuth();

  const meQuery = useQuery({
    queryKey: ["me", token],
    queryFn: () => getMe(token as string),
    enabled: Boolean(token) && token !== DEMO_TOKEN,
    retry: false,
  });

  useEffect(() => {
    if (ready && token === null) {
      router.push("/login");
    }
  }, [ready, router, token]);

  useEffect(() => {
    if (meQuery.data && token) {
      setSession(token, meQuery.data);
    }
  }, [meQuery.data, setSession, token]);

  useEffect(() => {
    if (meQuery.isError && token !== DEMO_TOKEN) {
      clearSession();
    }
  }, [clearSession, meQuery.isError]);

  if (!ready || !token) {
    return <div className="min-h-screen bg-background" />;
  }

  const displayUser = meQuery.data ?? user;

  return (
    <div className="min-h-screen bg-background text-foreground">
      <aside className="fixed inset-y-0 left-0 hidden w-72 border-r border-border bg-white lg:block">
        <div className="flex h-16 items-center gap-3 border-b border-border px-5">
          <div className="flex h-9 w-9 items-center justify-center rounded-md bg-primary text-primary-foreground">
            <Building2 className="h-5 w-5" />
          </div>
          <div>
            <div className="text-sm font-bold">WorkForceIQ</div>
            <div className="text-xs text-muted-foreground">Workforce intelligence</div>
          </div>
        </div>
        <nav className="space-y-1 p-3">
          {navItems.map((item) => {
            const active = pathname === item.href || pathname.startsWith(`${item.href}/`);
            const Icon = item.icon;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex h-10 items-center gap-3 rounded-md px-3 text-sm font-medium text-muted-foreground transition hover:bg-muted hover:text-foreground",
                  active && "bg-accent text-accent-foreground",
                )}
              >
                <Icon className="h-4 w-4" />
                {item.label}
              </Link>
            );
          })}
        </nav>
      </aside>
      <div className="lg:pl-72">
        <header className="sticky top-0 z-20 flex h-16 items-center justify-between border-b border-border bg-white/95 px-4 backdrop-blur lg:px-6">
          <div className="flex min-w-0 items-center gap-3">
            <div className="hidden h-10 w-80 items-center gap-2 rounded-md border border-border bg-background px-3 text-sm text-muted-foreground md:flex">
              <Search className="h-4 w-4" />
              Search people, policies, jobs, and skills
            </div>
            <div className="flex h-10 items-center gap-2 rounded-md border border-border bg-background px-3 text-sm text-muted-foreground md:hidden">
              <Search className="h-4 w-4" />
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button
              className="flex h-10 w-10 items-center justify-center rounded-md border border-border bg-white text-muted-foreground hover:text-foreground"
              aria-label="Notifications"
            >
              <Bell className="h-4 w-4" />
            </button>
            <div className="hidden text-right sm:block">
              <div className="text-sm font-semibold">{displayUser?.full_name ?? "Signed in"}</div>
              <div className="text-xs text-muted-foreground">{displayUser?.role.name ?? "..."}</div>
            </div>
            <button
              className="flex h-10 w-10 items-center justify-center rounded-md border border-border bg-white text-muted-foreground hover:text-foreground"
              aria-label="Sign out"
              onClick={clearSession}
            >
              <LogOut className="h-4 w-4" />
            </button>
          </div>
        </header>
        <main className="px-4 py-6 lg:px-6">{children}</main>
      </div>
      <div className="fixed bottom-5 right-5">
        <Button className="h-12 rounded-full px-5 shadow-lg" type="button">
          <Bot className="h-5 w-5" />
          AI Assistant
        </Button>
      </div>
    </div>
  );
}
