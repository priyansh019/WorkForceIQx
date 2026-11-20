# WorkForceIQ

**AI-powered workforce intelligence for smarter, evidence-backed HR decisions.**

WorkForceIQ combines workforce analytics, machine learning, retrieval-augmented generation (RAG), and generative AI to help HR teams understand employee data, reason over HR policies, identify workforce risks, and generate actionable insights across multiple HR data sources.

## Why WorkForceIQ

HR teams often need to interpret information spread across employee records, policy documents, performance data, recruitment activity, and organizational reports. WorkForceIQ provides a unified foundation for turning that information into clear, governed, and decision-ready insights.

The platform is being built around a responsible AI approach: approved data is retrieved before AI processing, API credentials remain server-side, and role-based access controls protect sensitive workforce information.

## Key Features

### Workforce Intelligence

- Analyze workforce data and organizational patterns
- Identify potential workforce risk indicators
- Generate summaries and evidence-backed insights
- Support recruitment, onboarding, performance, and policy workflows
- Bring analytics and AI assistance into a single HR platform

### AI and RAG

- Dedicated backend prompt structure for workforce use cases
- Retrieval-ready architecture using pgvector
- Server-side LLM and embedding API integration
- Context-specific prompts for recruitment, policy, onboarding, performance, interviewing, and workforce analysis
- Designed to retrieve approved enterprise data before generating responses

### Enterprise Application Foundation

- FastAPI REST API
- JWT-based authentication
- Role-based access control
- SQLAlchemy 2 database models
- PostgreSQL and pgvector support
- Redis-backed infrastructure
- Centralized exception and API error handling
- Audit logging for authentication and protected user access
- Docker Compose deployment for the full application stack

### Frontend Experience

- Next.js 15 application with React 19
- Login and registration flows
- Enterprise dashboard shell
- Sidebar and top navigation
- Dashboard cards and notifications
- TanStack Query API integration
- Recharts-based visualization support
- Responsive Tailwind CSS interface

## User Roles

WorkForceIQ includes foundations for the following roles:

- `ADMIN`
- `HR_ADMIN`
- `HR_MANAGER`
- `RECRUITER`
- `MANAGER`
- `EMPLOYEE`

Role definitions support future, fine-grained authorization across workforce, recruitment, policy, and analytics features.

## Demo Credentials

After running the seed script:

| Role | Email | Password |
| --- | --- | --- |
| Admin | `admin@workforceiq.demo` | `AdminPass123!` |
| HR Admin | `hr.admin@workforceiq.demo` | `HrAdminPass123!` |
| Recruiter | `recruiter@workforceiq.demo` | `RecruiterPass123!` |
| Employee | `employee@workforceiq.demo` | `EmployeePass123!` |

## Technology Stack

### Backend

- Python
- FastAPI
- SQLAlchemy 2
- Alembic
- Pydantic
- JWT authentication
- PostgreSQL
- pgvector
- Redis
- Pandas and NumPy
- Scikit-learn
- Pytest
- PDF and DOCX processing

### Frontend

- TypeScript
- Next.js 15
- React 19
- TanStack Query
- React Hook Form
- Zod
- Tailwind CSS
- Recharts

### Infrastructure

- Docker
- Docker Compose
- PostgreSQL 16 with pgvector
- Redis 7

## Architecture

```text
Browser
  │
  ▼
Next.js Frontend
  │  REST API
  ▼
FastAPI Backend
  ├── Authentication and RBAC
  ├── Workforce domain services
  ├── API validation and error handling
  └── AI and RAG services
       │
       ├── Retrieval: PostgreSQL + pgvector
       ├── Analytics: Pandas, NumPy, Scikit-learn
       └── Generative AI: server-side LLM providers

Redis provides supporting infrastructure for caching, jobs, and asynchronous workflows.
```

API keys and provider configuration are kept on the backend. They are not exposed through the Next.js application.

## Project Structure

```text
WorkForceIQx/
├── backend/
│   ├── app/
│   │   ├── ai/              # Prompts and AI integration foundations
│   │   ├── api/             # Routes and API router
│   │   ├── core/            # Configuration, security, and errors
│   │   ├── db/              # Database initialization and sessions
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic request and response schemas
│   │   └── services/        # Business and application services
│   ├── migrations/          # Alembic migrations
│   ├── scripts/             # Database seed and maintenance scripts
│   └── tests/               # Backend test suite
├── frontend/
│   ├── app/                 # Next.js routes and layouts
│   ├── components/          # Shared and application components
│   └── lib/                 # API clients and frontend utilities
├── docker-compose.yml
└── .env.example
```

## Getting Started

### Prerequisites

- Python 3.10 or newer
- Node.js 18 or newer
- npm
- Docker and Docker Compose for the containerized setup

### Option 1: Docker Compose

From the repository root:

```bash
cp .env.example .env
docker compose up --build
```

The application services will be available at:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`

Stop the stack with:

```bash
docker compose down
```

To remove the PostgreSQL volume as well:

```bash
docker compose down -v
```

### Option 2: Local Backend

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment:

- Windows: `.venv\Scripts\activate`
- macOS/Linux: `source .venv/bin/activate`

Install dependencies and seed the database:

```bash
pip install -r requirements.txt
python -m scripts.seed
uvicorn app.main:app --reload
```

Without `DATABASE_URL`, the backend uses SQLite at `sqlite:///./workforceiq.db`. Docker uses PostgreSQL.

### Option 3: Local Frontend

In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000.

## Environment Variables

Copy `.env.example` to `.env` and update values for your environment.

| Variable | Purpose |
| --- | --- |
| `DATABASE_URL` | SQLAlchemy database connection URL |
| `JWT_SECRET` | Secret used to sign access tokens |
| `JWT_ALGORITHM` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime |
| `BACKEND_CORS_ORIGINS` | Comma-separated frontend origins allowed by CORS |
| `LLM_API_KEY` | API credential for the configured LLM provider |
| `EMBEDDING_API_KEY` | API credential for embedding generation |
| `REDIS_URL` | Redis connection URL |
| `NEXT_PUBLIC_API_URL` | Base URL used by the frontend to call the backend |

> Use a strong, unique `JWT_SECRET` outside local development. Do not commit real API keys or production credentials.

## API Overview

FastAPI exposes interactive API documentation through:

- Swagger UI: `/docs`
- ReDoc: `/redoc`

### Implemented endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/health` | API health status |
| `POST` | `/api/auth/register` | Register a user |
| `POST` | `/api/auth/login` | Authenticate and receive an access token |
| `GET` | `/api/auth/me` | Retrieve the authenticated user |
| `GET` | `/api/users` | List users with role authorization |

## AI Architecture

The backend AI package is organized around dedicated workforce domains:

- Recruitment
- HR policy
- Onboarding
- Performance
- Workforce analytics
- Interview support
- Shared system instructions

The intended production flow is:

1. Authenticate and authorize the request.
2. Validate and filter the user's access scope.
3. Retrieve relevant approved documents or workforce records.
4. Build a domain-specific prompt with retrieved evidence.
5. Generate a response through a server-side AI provider.
6. Return the answer with an audit trail and source context where applicable.

This design helps prevent credentials and sensitive retrieved context from being exposed to the frontend.

## Testing

Run the backend test suite from the repository root:

```bash
cd backend
pytest
```

Current tests cover:

- User registration
- Login
- Current-user retrieval
- Role-restricted user listing

For frontend validation:

```bash
cd frontend
npm run typecheck
npm run lint
npm run build
```

## Development Status

WorkForceIQ is currently established around a production-oriented application foundation and Phase 1 features. Authentication, RBAC, domain models, seed data, the frontend shell, Docker infrastructure, and AI package scaffolding are present.

Planned evolution includes:

- Document ingestion and policy indexing
- Vector search and retrieval pipelines
- ML-powered workforce risk modeling
- Recruitment and candidate intelligence workflows
- Policy question answering with source citations
- Performance and employee analytics
- Background document and embedding jobs
- Fine-grained data governance and audit trails
- Production observability and model safeguards

## Security and Responsible Use

Workforce data can contain sensitive personal information. Any deployment of WorkForceIQ should include:

- Strong production secrets
- HTTPS and secure network boundaries
- Least-privilege role policies
- Tenant and data-access isolation where required
- Prompt injection and data exfiltration protections
- Review and approval workflows for AI-generated decisions
- Human oversight for employment, promotion, discipline, and compensation decisions
- Retention, deletion, and audit policies
- Compliance review for applicable labor and privacy regulations

AI insights should support—not replace—qualified human judgment.

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make your changes with relevant tests.
4. Run backend and frontend validation.
5. Open a pull request with a clear summary and testing evidence.

## License

No license is currently specified for this repository. A license should be added before reuse or distribution outside the project team.
