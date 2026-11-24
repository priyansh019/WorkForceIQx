# WorkForceIQ

WorkForceIQ is an AI-powered workforce intelligence platform for HR teams. It combines employee data, HR policies, workforce analytics, machine learning, and generative AI to provide clear, evidence-backed insights.

Live demo: https://workforceiqx.vercel.app

## What It Does

- Analyzes employee and organizational data
- Finds potential workforce risks and trends
- Answers questions about HR policies
- Summarizes documents and highlights supporting evidence
- Supports recruitment, onboarding, performance, and workforce planning workflows
- Provides role-based access for administrators and HR users

## Key Features

- **AI and RAG:** Retrieves relevant company data and policy documents before generating answers.
- **HR Analytics:** Uses workforce data to identify patterns, risks, and opportunities.
- **Document Support:** Processes HR documents and makes them searchable.
- **Role-Based Access:** Controls what different users can view and manage.
- **Evidence-Aware Responses:** Links answers to retrieved information when available.
- **Secure Backend:** Keeps API keys and AI integrations on the server.

## Technology

- **Backend:** Python, FastAPI, SQLAlchemy, PostgreSQL
- **Frontend:** TypeScript, Next.js, React, Tailwind CSS
- **AI:** Embeddings and large language model integrations
- **Data and ML:** Pandas, NumPy, scikit-learn
- **Infrastructure:** Docker, Docker Compose, Redis

## Project Structure

```text
WorkForceIQx/
├── backend/       # FastAPI application, database, AI, and services
├── frontend/      # Next.js web interface
├── docker-compose.yml
└── .env.example
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm
- Docker and Docker Compose

### Run with Docker

```bash
cp .env.example .env
docker compose up --build
```

Open:

- Frontend: http://localhost:3000
- API: http://localhost:8000
- API documentation: http://localhost:8000/docs

### Run the Backend Locally

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment:

- Windows: `.venv\Scripts\activate`
- macOS/Linux: `source .venv/bin/activate`

Then install and start the backend:

```bash
pip install -r requirements.txt
python -m scripts.seed
uvicorn app.main:app --reload
```

If `DATABASE_URL` is not configured, the backend uses SQLite.

### Run the Frontend Locally

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000.

## Environment Variables

Create `.env` from `.env.example`, then update the values required by your environment.

Important variables include:

- `DATABASE_URL` — Database connection string
- `JWT_SECRET` — Secret used to sign authentication tokens
- `LLM_API_KEY` — API key for the AI provider
- `EMBEDDING_API_KEY` — API key for embedding generation
- `REDIS_URL` — Redis connection string

Keep real API keys and production secrets out of source control.

## Testing

Run backend tests:

```bash
cd backend
pytest
```

Check the frontend:

```bash
cd frontend
npm run typecheck
npm run lint
npm run build
```

## Responsible Use

WorkForceIQ processes sensitive workforce and employee information. Any deployment should include:

- Strong authentication and authorization
- Secure storage of secrets and personal data
- Appropriate access controls
- Data retention and deletion policies
- Human review of important decisions
- Compliance checks for applicable laws and regulations

AI insights should support—not replace—qualified human judgment.

## License

A license has not been specified yet.
