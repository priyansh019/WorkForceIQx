# WorkForceIQ

AI-powered workforce intelligence for smarter HR decisions.

WorkForceIQ is a full-stack HR intelligence platform. Phase 1 establishes the production architecture, authentication, RBAC foundations, database models, seed data, frontend shell, and Docker setup. Later phases can build on the same backend services, schemas, AI prompt structure, and UI navigation without replacing the foundation.

## Features In Phase 1

- FastAPI backend with JWT authentication
- SQLAlchemy 2 models for the full workforce domain
- Role-based authorization foundations for ADMIN, HR_ADMIN, HR_MANAGER, RECRUITER, MANAGER, and EMPLOYEE
- Password hashing with Passlib
- Centralized error handling and consistent API error responses
- Audit logging for registration, login, and protected user access
- Deterministic seed script for roles and demo users
- Next.js 15 frontend with login/register/dashboard flows
- TanStack Query API integration
- Enterprise SaaS layout with sidebar, topbar, dashboard cards, notifications, and global assistant entry point
- Docker Compose for frontend, backend, PostgreSQL/pgvector, and Redis
- Pytest coverage for auth and RBAC basics

## Demo Credentials

After seeding:

- Admin: `admin@workforceiq.demo` / `AdminPass123!`
- HR Admin: `hr.admin@workforceiq.demo` / `HrAdminPass123!`
- Recruiter: `recruiter@workforceiq.demo` / `RecruiterPass123!`
- Employee: `employee@workforceiq.demo` / `EmployeePass123!`

## Architecture

```text
Browser
  -> Next.js frontend
  -> FastAPI REST API
  -> SQLAlchemy
  -> PostgreSQL + pgvector in Docker
  -> AI services, RAG, ML analytics, and job processing modules
```

## Local Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m scripts.seed
uvicorn app.main:app --reload
```

The backend defaults to `sqlite:///./workforceiq.db` when `DATABASE_URL` is not provided. Docker uses PostgreSQL.

## Local Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

## Docker

```bash
docker compose up --build
```

Services:

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Environment Variables

Copy `.env.example` to `.env` and adjust values for local or deployed environments.

Important variables:

- `DATABASE_URL`
- `JWT_SECRET`
- `JWT_ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `BACKEND_CORS_ORIGINS`
- `LLM_API_KEY`
- `EMBEDDING_API_KEY`
- `REDIS_URL`
- `NEXT_PUBLIC_API_URL`

## Folder Structure

```text
backend/
  app/
    ai/prompts/
    api/routes/
    core/
    db/
    models/
    schemas/
    services/
  migrations/
  scripts/
  tests/
frontend/
  app/
  components/
  lib/
```

## API Documentation

FastAPI exposes:

- `/docs`
- `/redoc`

Implemented Phase 1 endpoints:

- `GET /api/health`
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `GET /api/users`

## AI And ML Architecture

Phase 1 includes the package and prompt structure for the AI engine:

- `backend/app/ai/prompts/system.py`
- `backend/app/ai/prompts/recruitment.py`
- `backend/app/ai/prompts/policy.py`
- `backend/app/ai/prompts/onboarding.py`
- `backend/app/ai/prompts/performance.py`
- `backend/app/ai/prompts/workforce.py`
- `backend/app/ai/prompts/interview.py`

The AI contract is intentionally server-side only. API keys are never exposed to the frontend. Future phases should route all LLM calls through backend services that retrieve approved data before reasoning.

## Testing

```bash
cd backend
pytest
```

Current tests cover registration, login, `/me`, and role-restricted user listing.

