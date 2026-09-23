from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Index, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Job(Base, TimestampMixin):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(180), index=True)
    department: Mapped[str] = mapped_column(String(120), index=True)
    description: Mapped[str] = mapped_column(Text)
    required_skills: Mapped[str | None] = mapped_column(Text)
    preferred_skills: Mapped[str | None] = mapped_column(Text)
    minimum_experience: Mapped[Decimal] = mapped_column(Numeric(4, 1), default=0)
    location: Mapped[str | None] = mapped_column(String(120))
    employment_type: Mapped[str] = mapped_column(String(40), default="FULL_TIME")
    status: Mapped[str] = mapped_column(String(40), index=True, default="OPEN")


class Candidate(Base, TimestampMixin):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(180), index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(40))
    resume_text: Mapped[str | None] = mapped_column(Text)
    experience_years: Mapped[Decimal] = mapped_column(Numeric(4, 1), default=0)
    education: Mapped[str | None] = mapped_column(Text)


class CandidateSkill(Base, TimestampMixin):
    __tablename__ = "candidate_skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), index=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), index=True)
    proficiency: Mapped[int] = mapped_column()
    years_experience: Mapped[Decimal] = mapped_column(Numeric(4, 1), default=0)

    __table_args__ = (
        UniqueConstraint("candidate_id", "skill_id", name="uq_candidate_skills_candidate_skill"),
    )


class Application(Base, TimestampMixin):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), index=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), index=True)
    status: Mapped[str] = mapped_column(String(40), index=True, default="APPLIED")

    __table_args__ = (
        UniqueConstraint("candidate_id", "job_id", name="uq_applications_candidate_job"),
        Index("ix_applications_job_status", "job_id", "status"),
    )


class Resume(Base, TimestampMixin):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), index=True)
    original_filename: Mapped[str] = mapped_column(String(255))
    storage_path: Mapped[str] = mapped_column(String(500))
    content_type: Mapped[str] = mapped_column(String(120))
    extracted_text: Mapped[str | None] = mapped_column(Text)
    parsed_profile: Mapped[str | None] = mapped_column(Text)


class InterviewSession(Base, TimestampMixin):
    __tablename__ = "interview_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), index=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), index=True)
    interviewer_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), index=True)
    status: Mapped[str] = mapped_column(String(40), index=True, default="OPEN")
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class InterviewQuestion(Base, TimestampMixin):
    __tablename__ = "interview_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("interview_sessions.id"), index=True)
    question_type: Mapped[str] = mapped_column(String(80), index=True)
    skill: Mapped[str | None] = mapped_column(String(120))
    question: Mapped[str] = mapped_column(Text)
    expected_signals: Mapped[str | None] = mapped_column(Text)


class InterviewResponse(Base, TimestampMixin):
    __tablename__ = "interview_responses"

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("interview_questions.id"), index=True)
    response_text: Mapped[str] = mapped_column(Text)
    analysis: Mapped[str | None] = mapped_column(Text)

