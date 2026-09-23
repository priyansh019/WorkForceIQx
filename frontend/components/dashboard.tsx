"use client";

import {
  ArrowUpRight,
  BriefcaseBusiness,
  CheckCircle2,
  ChevronRight,
  CircleAlert,
  Sparkles,
  TrendingUp,
  Users,
} from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { Area, AreaChart, Bar, BarChart, CartesianGrid, Cell, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { Card } from "@/components/ui/card";
import { useAuth } from "@/lib/auth";
import { getHealth } from "@/lib/api";

export function Dashboard() {
  const { user } = useAuth();
  const healthQuery = useQuery({ queryKey: ["health"], queryFn: getHealth });
  const currentUser = user;
  const headcount = [
    { month: "Apr", employees: 238 },
    { month: "May", employees: 247 },
    { month: "Jun", employees: 251 },
    { month: "Jul", employees: 264 },
    { month: "Aug", employees: 276 },
    { month: "Sep", employees: 284 },
  ];
  const departments = [
    { name: "Engineering", value: 34, color: "#0e7490" },
    { name: "Sales", value: 22, color: "#8b5cf6" },
    { name: "Product", value: 17, color: "#f59e0b" },
    { name: "Operations", value: 15, color: "#10b981" },
    { name: "Other", value: 12, color: "#cbd5e1" },
  ];
  const activity = [
    ["09:42", "Priya Shah", "completed onboarding", "bg-emerald-100 text-emerald-700"],
    ["09:18", "Marcus Lee", "was flagged for flight risk", "bg-rose-100 text-rose-700"],
    ["08:56", "Talent team", "opened 3 new applications", "bg-violet-100 text-violet-700"],
  ];

  return (
    <div className="mx-auto max-w-[1500px] space-y-6">
      <div className="relative overflow-hidden rounded-2xl bg-slate-950 px-6 py-7 text-white shadow-xl shadow-slate-200 lg:px-8">
        <div className="absolute -right-10 -top-24 h-72 w-72 rounded-full bg-cyan-500/20 blur-3xl" />
        <div className="absolute bottom-[-100px] right-1/3 h-52 w-52 rounded-full bg-violet-500/20 blur-3xl" />
        <div className="relative flex flex-col justify-between gap-6 md:flex-row md:items-end">
          <div>
            <div className="mb-3 flex items-center gap-2 text-sm font-medium text-cyan-300">
              <Sparkles className="h-4 w-4" /> Workforce intelligence briefing
            </div>
            <h1 className="text-3xl font-semibold tracking-tight lg:text-4xl">
              Good morning, {currentUser?.full_name?.split(" ")[0] ?? "there"}.
            </h1>
            <p className="mt-2 max-w-xl text-sm leading-6 text-slate-300">
              Your workforce is growing steadily. Here&apos;s the pulse of your organization for
              Tuesday, September 23, 2026.
            </p>
          </div>
          <div className="rounded-xl border border-white/10 bg-white/10 px-4 py-3 text-sm backdrop-blur">
            <div className="text-slate-300">Workspace status</div>
            <div className="mt-1 flex items-center gap-2 font-semibold">
              <span className="h-2 w-2 rounded-full bg-emerald-400" /> All systems operational
            </div>
          </div>
        </div>
      </div>

      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {[
          { label: "Total employees", value: "284", trend: "+8.4%", Icon: Users, color: "text-cyan-700 bg-cyan-50" },
          { label: "Engagement score", value: "84.6", trend: "+3.2%", Icon: TrendingUp, color: "text-violet-700 bg-violet-50" },
          { label: "Open positions", value: "18", trend: "6 urgent", Icon: BriefcaseBusiness, color: "text-amber-700 bg-amber-50" },
          { label: "At-risk employees", value: "12", trend: "−4 this month", Icon: CircleAlert, color: "text-rose-700 bg-rose-50" },
        ].map(({ label, value, trend, Icon, color }) => (
          <Card key={label} className="p-5 transition hover:-translate-y-0.5 hover:shadow-lg">
            <div className="flex items-start justify-between">
              <div className={`flex h-10 w-10 items-center justify-center rounded-xl ${color}`}>
                <Icon className="h-5 w-5" />
              </div>
              <span className="rounded-full bg-emerald-50 px-2 py-1 text-xs font-semibold text-emerald-700">
                {trend}
              </span>
            </div>
            <div className="mt-5 text-2xl font-semibold tracking-tight">{value}</div>
            <div className="mt-1 text-sm text-muted-foreground">{label}</div>
          </Card>
        ))}
      </section>

      <section className="grid gap-4 xl:grid-cols-[1.45fr_0.8fr]">
        <Card className="min-h-[350px]">
          <div className="flex items-start justify-between">
            <div>
              <h2 className="text-lg font-semibold">Headcount growth</h2>
              <p className="mt-1 text-sm text-muted-foreground">Active employees · last 6 months</p>
            </div>
            <button className="flex items-center gap-1 text-sm font-semibold text-primary">View report <ArrowUpRight className="h-4 w-4" /></button>
          </div>
          <div className="mt-6 h-56">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={headcount}>
                <defs><linearGradient id="headcountFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#0891b2" stopOpacity={0.25} /><stop offset="100%" stopColor="#0891b2" stopOpacity={0} /></linearGradient></defs>
                <CartesianGrid vertical={false} stroke="#e2e8f0" />
                <XAxis dataKey="month" axisLine={false} tickLine={false} tick={{ fill: "#64748b", fontSize: 12 }} />
                <YAxis axisLine={false} tickLine={false} tick={{ fill: "#64748b", fontSize: 12 }} domain={[220, 300]} />
                <Tooltip />
                <Area type="monotone" dataKey="employees" stroke="#0891b2" strokeWidth={3} fill="url(#headcountFill)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Card>
        <Card>
          <div>
            <h2 className="text-lg font-semibold">Workforce mix</h2>
            <p className="mt-1 text-sm text-muted-foreground">By department</p>
          </div>
          <div className="relative mx-auto mt-2 h-44 w-44">
            <ResponsiveContainer width="100%" height="100%"><PieChart><Pie data={departments} dataKey="value" innerRadius={55} outerRadius={78} paddingAngle={3}>{departments.map((item) => <Cell key={item.name} fill={item.color} />)}</Pie></PieChart></ResponsiveContainer>
            <div className="absolute inset-0 flex flex-col items-center justify-center"><strong className="text-2xl">284</strong><span className="text-xs text-muted-foreground">people</span></div>
          </div>
          <div className="mt-2 grid grid-cols-2 gap-3 text-xs">{departments.map((item) => <div key={item.name} className="flex items-center gap-2"><span className="h-2 w-2 rounded-full" style={{ backgroundColor: item.color }} />{item.name}<span className="ml-auto font-semibold">{item.value}%</span></div>)}</div>
        </Card>
      </section>

      <section className="grid gap-4 xl:grid-cols-[1fr_1fr]">
        <Card>
          <div className="flex items-center justify-between"><div><h2 className="text-lg font-semibold">Hiring pipeline</h2><p className="mt-1 text-sm text-muted-foreground">Candidate movement this month</p></div><ChevronRight className="h-5 w-5 text-muted-foreground" /></div>
          <div className="mt-6 h-48"><ResponsiveContainer width="100%" height="100%"><BarChart data={[{ stage: "Applied", count: 126 }, { stage: "Screening", count: 64 }, { stage: "Interview", count: 28 }, { stage: "Offer", count: 9 }]}><CartesianGrid vertical={false} stroke="#e2e8f0" /><XAxis dataKey="stage" axisLine={false} tickLine={false} tick={{ fill: "#64748b", fontSize: 11 }} /><YAxis axisLine={false} tickLine={false} tick={{ fill: "#64748b", fontSize: 11 }} /><Tooltip cursor={{ fill: "#f8fafc" }} /><Bar dataKey="count" fill="#8b5cf6" radius={[5, 5, 0, 0]} /></BarChart></ResponsiveContainer></div>
        </Card>
        <Card>
          <div className="flex items-center justify-between"><div><h2 className="text-lg font-semibold">Recent activity</h2><p className="mt-1 text-sm text-muted-foreground">Live updates from your workspace</p></div><button className="text-sm font-semibold text-primary">See all</button></div>
          <div className="mt-5 space-y-4">{activity.map(([time, name, action, badge]) => <div key={time} className="flex items-center gap-3"><div className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-xs font-bold ${badge}`}>{name.split(" ").map((part) => part[0]).join("")}</div><div className="min-w-0 flex-1 text-sm"><span className="font-semibold">{name}</span> <span className="text-muted-foreground">{action}</span></div><span className="text-xs text-muted-foreground">{time}</span></div>)}</div>
          <div className="mt-5 flex items-center gap-2 rounded-lg bg-emerald-50 px-3 py-2 text-xs text-emerald-800"><CheckCircle2 className="h-4 w-4" /> Data refreshed just now {healthQuery.isError ? "(demo mode)" : ""}</div>
        </Card>
      </section>
    </div>
  );
}
