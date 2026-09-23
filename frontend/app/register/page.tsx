import { AuthForm } from "@/components/auth-form";

export default function RegisterPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-background px-4 py-10">
      <AuthForm mode="register" />
    </main>
  );
}

