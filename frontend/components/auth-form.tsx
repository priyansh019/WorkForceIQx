"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { AlertCircle, ArrowRight, LogIn, UserPlus } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { ApiError, register } from "@/lib/api";
import { DEMO_TOKEN, DEMO_USER, useAuth } from "@/lib/auth";

const loginSchema = z.object({});

const registerSchema = loginSchema.extend({
  fullName: z.string().min(2),
  password: z.string().min(10),
});

type AuthFormValues = {
  email: string;
  password: string;
  fullName?: string;
};

export function AuthForm({ mode }: { mode: "login" | "register" }) {
  const router = useRouter();
  const { setSession } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const isRegister = mode === "register";
  const schema = isRegister ? registerSchema : loginSchema;
  const form = useForm<AuthFormValues>({
    resolver: zodResolver(schema),
    defaultValues: isRegister
      ? { email: "", fullName: "", password: "" }
      : { email: "", password: "" },
  });

  async function onSubmit(values: AuthFormValues) {
    setError(null);
    try {
      if (!isRegister) {
        setSession(DEMO_TOKEN, DEMO_USER);
        router.push("/dashboard");
        return;
      }
      const response = await register(values.email, values.fullName ?? "", values.password);
      setSession(response.access_token, response.user);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Unable to authenticate.");
    }
  }

  return (
    <Card className="w-full max-w-md">
      <div className="mb-6">
        <div className="text-xs font-semibold uppercase tracking-[0.12em] text-primary">
          WorkForceIQ
        </div>
        <h1 className="mt-2 text-2xl font-semibold">
          {isRegister ? "Create your workspace account" : "Explore your workforce"}
        </h1>
        <p className="mt-2 text-sm text-muted-foreground">
          {isRegister
            ? "AI-powered workforce intelligence for smarter HR decisions."
            : "A ready-to-use demo workspace with realistic workforce data and insights."}
        </p>
      </div>
      {!isRegister ? (
        <div className="rounded-xl border border-cyan-100 bg-cyan-50/70 p-4">
          <div className="flex items-start gap-3">
            <div className="mt-0.5 flex h-8 w-8 items-center justify-center rounded-lg bg-cyan-600 text-white">
              <SparklesIcon />
            </div>
            <div>
              <div className="font-semibold text-slate-900">Demo access enabled</div>
              <p className="mt-1 text-sm leading-5 text-slate-600">
                No password or account is required. Jump straight into the sample HR workspace.
              </p>
            </div>
          </div>
        </div>
      ) : null}
      <form className="space-y-4" onSubmit={form.handleSubmit(onSubmit)}>
        {isRegister ? (
          <label className="block text-sm font-medium">
            Full name
            <Input className="mt-2" {...form.register("fullName")} autoComplete="name" />
          </label>
        ) : null}
        {isRegister ? (
          <>
            <label className="block text-sm font-medium">
              Email
              <Input className="mt-2" {...form.register("email")} autoComplete="email" />
            </label>
            <label className="block text-sm font-medium">
              Password
              <Input className="mt-2" type="password" {...form.register("password")} autoComplete="new-password" />
            </label>
          </>
        ) : null}
        {error ? (
          <div className="flex items-start gap-2 rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-700">
            <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
            <span>{error}</span>
          </div>
        ) : null}
        <Button className="w-full" disabled={form.formState.isSubmitting}>
          {isRegister ? <UserPlus className="h-4 w-4" /> : <ArrowRight className="h-4 w-4" />}
          {isRegister ? "Create account" : "Enter demo workspace"}
        </Button>
      </form>
      <div className="mt-5 text-sm text-muted-foreground">
        {isRegister ? "Already have an account?" : "Need an account?"}{" "}
        <Link className="font-semibold text-primary" href={isRegister ? "/login" : "/register"}>
          {isRegister ? "Sign in" : "Register"}
        </Link>
      </div>
    </Card>
  );
}

function SparklesIcon() {
  return <span className="text-sm font-bold">✦</span>;
}
