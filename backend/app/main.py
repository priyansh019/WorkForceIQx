from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.errors import register_exception_handlers
from app.db.init_db import create_tables, ensure_roles
from app.db.session import SessionLocal


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_tables()
    db = SessionLocal()
    try:
        ensure_roles(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="WorkForceIQ API",
    description="AI-powered workforce intelligence backend for smarter HR decisions.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
app.include_router(api_router)

