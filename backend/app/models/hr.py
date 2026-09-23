from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class Department(Base, TimestampMixin):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text)

    employees: Mapped[list["Employee"]] = relationship(back_populates="department")
    job_roles: Mapped[list["JobRole"]] = relationship(back_populates="department")


class JobRole(Base, TimestampMixin):
    __tablename__ = "job_roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(160), index=True)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    required_skills: Mapped[str | None] = mapped_column(Text)

    department: Mapped[Department] = relationship(back_populates="job_roles")
    employees: Mapped[list["Employee"]] = relationship(back_populates="job_role")


class Employee(Base, TimestampMixin):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_code: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(120))
    last_name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(40))
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), index=True)
    job_role_id: Mapped[int] = mapped_column(ForeignKey("job_roles.id"), index=True)
    manager_id: Mapped[int | None] = mapped_column(ForeignKey("employees.id"), index=True)
    location: Mapped[str | None] = mapped_column(String(120))
    joining_date: Mapped[date] = mapped_column(Date)
    employment_status: Mapped[str] = mapped_column(String(40), index=True, default="ACTIVE")
    employment_type: Mapped[str] = mapped_column(String(40), default="FULL_TIME")

    department: Mapped[Department] = relationship(back_populates="employees")
    job_role: Mapped[JobRole] = relationship(back_populates="employees")
    manager: Mapped["Employee | None"] = relationship(remote_side=[id])
    user: Mapped["User | None"] = relationship(back_populates="employee", foreign_keys="User.employee_id")
    skills: Mapped[list["EmployeeSkill"]] = relationship(back_populates="employee")

    __table_args__ = (
        Index("ix_employees_department_status", "department_id", "employment_status"),
    )


class Skill(Base, TimestampMixin):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    category: Mapped[str] = mapped_column(String(120), index=True)
    description: Mapped[str | None] = mapped_column(Text)

    employee_skills: Mapped[list["EmployeeSkill"]] = relationship(back_populates="skill")


class EmployeeSkill(Base, TimestampMixin):
    __tablename__ = "employee_skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), index=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), index=True)
    proficiency_level: Mapped[int] = mapped_column(Integer)
    years_experience: Mapped[Decimal] = mapped_column(Numeric(4, 1), default=0)
    last_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    employee: Mapped[Employee] = relationship(back_populates="skills")
    skill: Mapped[Skill] = relationship(back_populates="employee_skills")

    __table_args__ = (
        UniqueConstraint("employee_id", "skill_id", name="uq_employee_skills_employee_skill"),
    )


class AttendanceRecord(Base, TimestampMixin):
    __tablename__ = "attendance_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), index=True)
    date: Mapped[date] = mapped_column(Date, index=True)
    status: Mapped[str] = mapped_column(String(40), index=True)
    hours_worked: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0)
    overtime_hours: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0)
    late_minutes: Mapped[int] = mapped_column(Integer, default=0)

    __table_args__ = (
        UniqueConstraint("employee_id", "date", name="uq_attendance_employee_date"),
        Index("ix_attendance_employee_date", "employee_id", "date"),
    )


class PerformanceReview(Base, TimestampMixin):
    __tablename__ = "performance_reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), index=True)
    review_period: Mapped[str] = mapped_column(String(40), index=True)
    overall_rating: Mapped[Decimal] = mapped_column(Numeric(3, 2))
    goal_completion: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    manager_summary: Mapped[str | None] = mapped_column(Text)
    strengths: Mapped[str | None] = mapped_column(Text)
    improvement_areas: Mapped[str | None] = mapped_column(Text)


class PerformanceGoal(Base, TimestampMixin):
    __tablename__ = "performance_goals"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), index=True)
    title: Mapped[str] = mapped_column(String(180))
    description: Mapped[str | None] = mapped_column(Text)
    target: Mapped[str | None] = mapped_column(Text)
    progress: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0)
    status: Mapped[str] = mapped_column(String(40), index=True, default="NOT_STARTED")
    deadline: Mapped[date | None] = mapped_column(Date)


class Feedback(Base, TimestampMixin):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), index=True)
    author: Mapped[str] = mapped_column(String(180))
    feedback_type: Mapped[str] = mapped_column(String(80), index=True)
    content: Mapped[str] = mapped_column(Text)


class EngagementSurvey(Base, TimestampMixin):
    __tablename__ = "engagement_surveys"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), index=True)
    survey_date: Mapped[date] = mapped_column(Date, index=True)
    engagement_score: Mapped[Decimal] = mapped_column(Numeric(4, 2))
    manager_score: Mapped[Decimal] = mapped_column(Numeric(4, 2))
    workload_score: Mapped[Decimal] = mapped_column(Numeric(4, 2))
    growth_score: Mapped[Decimal] = mapped_column(Numeric(4, 2))
    satisfaction_score: Mapped[Decimal] = mapped_column(Numeric(4, 2))


class TrainingCourse(Base, TimestampMixin):
    __tablename__ = "training_courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(180), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    skills: Mapped[str | None] = mapped_column(Text)
    difficulty: Mapped[str] = mapped_column(String(40), index=True)
    duration: Mapped[str | None] = mapped_column(String(80))


class EmployeeTraining(Base, TimestampMixin):
    __tablename__ = "employee_training"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("training_courses.id"), index=True)
    status: Mapped[str] = mapped_column(String(40), index=True)
    completion_percentage: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint("employee_id", "course_id", name="uq_employee_training_employee_course"),
    )


class OnboardingPlan(Base, TimestampMixin):
    __tablename__ = "onboarding_plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), index=True)
    title: Mapped[str] = mapped_column(String(180))
    status: Mapped[str] = mapped_column(String(40), index=True, default="ACTIVE")


class OnboardingTask(Base, TimestampMixin):
    __tablename__ = "onboarding_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey("onboarding_plans.id"), index=True)
    title: Mapped[str] = mapped_column(String(180))
    description: Mapped[str | None] = mapped_column(Text)
    phase: Mapped[str] = mapped_column(String(80), index=True)
    owner: Mapped[str | None] = mapped_column(String(120))
    due_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(40), index=True, default="OPEN")

