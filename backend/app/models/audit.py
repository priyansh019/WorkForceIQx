from sqlalchemy import DateTime, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, utc_now


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), index=True)
    action: Mapped[str] = mapped_column(String(120), index=True)
    resource_type: Mapped[str | None] = mapped_column(String(120), index=True)
    resource_id: Mapped[str | None] = mapped_column(String(120), index=True)
    timestamp = mapped_column(DateTime(timezone=True), default=utc_now, index=True)
    log_metadata: Mapped[dict | None] = mapped_column(JSON)

