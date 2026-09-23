export type Role = {
  id: number;
  name: string;
  description: string | null;
};

export type User = {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  role: Role;
  employee_id: number | null;
  created_at: string;
};

export type TokenResponse = {
  access_token: string;
  token_type: "bearer";
  user: User;
};

export type ApiEnvelope<T> = {
  success: boolean;
  data: T;
};

export class ApiError extends Error {
  code: string;
  status: number;

  constructor(message: string, code: string, status: number) {
    super(message);
    this.code = code;
    this.status = status;
  }
}

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init.headers ?? {}),
    },
  });
  const body = await response.json().catch(() => null);
  if (!response.ok) {
    throw new ApiError(
      body?.error?.message ?? "Request failed.",
      body?.error?.code ?? "REQUEST_FAILED",
      response.status,
    );
  }
  return body.data;
}

export function login(email: string, password: string) {
  return request<TokenResponse>("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export function register(email: string, fullName: string, password: string) {
  return request<TokenResponse>("/api/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, full_name: fullName, password }),
  });
}

export function getMe(token: string) {
  return request<User>("/api/auth/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export function getHealth() {
  return request<{ status: string; app: string }>("/api/health");
}

