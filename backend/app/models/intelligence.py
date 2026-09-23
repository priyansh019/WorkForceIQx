from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Index, JSON, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin

try:
    from pgvector.sqlalchemy import Vector
except Exception:
    Vector = None


def embedding_type():
    return Vector(1536) if Vector else JSON


class HrDocument(Base, TimestampMixin):
    __tablename__ = "hr_documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(240), index=True)
    document_type: Mapped[str] = mapped_column(String(80), index=True)
    source_filename: Mapped[str] = mapped_column(String(255))
    storage_path: Mapped[str] = mapped_column(String(500))
    uploaded_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), index=True)
    synthetic_demo_notice: Mapped[str | None] = mapped_column(Text)


class HrDocumentChunk(Base, TimestampMixin):
    __tablename__ = "hr_document_chunks"

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("hr_documents.id"), index=True)
    chunk_index: Mapped[int] = mapped_column(index=True)
    content: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float] | None] = mapped_column(embedding_type(), nullable=True)
    page_number: Mapped[int | None] = mapped_column()
    section: Mapped[str | None] = mapped_column(String(180))
    chunk_metadata: Mapped[dict | None] = mapped_column(JSON)

    __table_args__ = (
        Index("ix_hr_document_chunks_document_chunk", "document_id", "chunk_index"),
    )


class EmployeeRiskScore(Base, TimestampMixin):
    __tablename__ = "employee_risk_scores"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), index=True)
    risk_probability: Mapped[Decimal] = mapped_column(Numeric(5, 4))
    risk_band: Mapped[str] = mapped_column(String(40), index=True)
    contributing_features: Mapped[dict] = mapped_column(JSON)
    historical_context: Mapped[dict | None] = mapped_column(JSON)
    model_version: Mapped[str] = mapped_column(String(80))
    data_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class WorkforceInsight(Base, TimestampMixin):
    __tablename__ = "workforce_insights"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(220), index=True)
    summary: Mapped[str] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(40), index=True)
    department_id: Mapped[int | None] = mapped_column(ForeignKey("departments.id"), index=True)
    evidence: Mapped[list[dict]] = mapped_column(JSON)
    metrics: Mapped[dict | None] = mapped_column(JSON)
    time_period: Mapped[str | None] = mapped_column(String(120))
    recommended_action: Mapped[str | None] = mapped_column(Text)
    confidence: Mapped[Decimal] = mapped_column(Numeric(4, 3), default=0)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(40), index=True, default="NEW")


class Recommendation(Base, TimestampMixin):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(80), index=True)
    title: Mapped[str] = mapped_column(String(220))
    description: Mapped[str] = mapped_column(Text)
    evidence: Mapped[list[dict] | None] = mapped_column(JSON)
    priority: Mapped[str] = mapped_column(String(40), index=True)
    status: Mapped[str] = mapped_column(String(40), index=True, default="NEW")
    assigned_to: Mapped[int | None] = mapped_column(ForeignKey("users.id"), index=True)


class Notification(Base, TimestampMixin):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(180))
    message: Mapped[str] = mapped_column(Text)
    notification_type: Mapped[str] = mapped_column(String(80), index=True)
    resource_type: Mapped[str | None] = mapped_column(String(80))
    resource_id: Mapped[int | None] = mapped_column()
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

