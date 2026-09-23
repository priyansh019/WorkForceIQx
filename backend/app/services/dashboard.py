from collections import Counter, defaultdict
from datetime import date, timedelta
from decimal import Decimal
from statistics import mean

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import (
    Application,
    AttendanceRecord,
    Candidate,
    Department,
    Employee,
    EmployeeRiskScore,
    EmployeeSkill,
    EmployeeTraining,
    EngagementSurvey,
    Job,
    PerformanceReview,
    Recommendation,
    Skill,
    WorkforceInsight,
)


def _number(value: Decimal | float | int | None, digits: int = 1) -> float:
    if value is None:
        return 0
    return round(float(value), digits)


def _period_label(day: date) -> str:
    return f"{day.year} Q{((day.month - 1) // 3) + 1}"


def _average(values: list[Decimal | float | int]) -> float:
    return _number(mean([float(value) for value in values]), 1) if values else 0


def get_dashboard_summary(db: Session) -> dict:
    employees = db.scalars(
        select(Employee).options(joinedload(Employee.department), joinedload(Employee.job_role))
    ).all()
    active_employees = [employee for employee in employees if employee.employment_status == "ACTIVE"]
    jobs = db.scalars(select(Job)).all()
    candidates = db.scalars(select(Candidate)).all()
    applications = db.scalars(select(Application)).all()
    engagement = db.scalars(select(EngagementSurvey)).all()
    attendance = db.scalars(select(AttendanceRecord)).all()
    performance = db.scalars(select(PerformanceReview)).all()
    training = db.scalars(select(EmployeeTraining)).all()
    risks = db.scalars(select(EmployeeRiskScore)).all()
    insights = db.scalars(
        select(WorkforceInsight).order_by(WorkforceInsight.generated_at.desc()).limit(6)
    ).all()
    recommendations = db.scalars(
        select(Recommendation).order_by(Recommendation.created_at.desc()).limit(6)
    ).all()
    skills = db.scalars(select(Skill)).all()
    employee_skills = db.scalars(select(EmployeeSkill).options(joinedload(EmployeeSkill.skill))).all()

    active_candidate_ids = {
        application.candidate_id
        for application in applications
        if application.status not in {"HIRED", "REJECTED"}
    }
    current_engagement = _average([survey.engagement_score for survey in engagement])
    skill_coverage = (
        round(
            100
            * len([skill for skill in employee_skills if skill.proficiency_level >= 3])
            / max(len(employee_skills), 1),
            1,
        )
        if employee_skills
        else 0
    )

    today = date.today()
    month_starts = []
    for months_ago in range(5, -1, -1):
        month = today.month - months_ago
        year = today.year
        while month <= 0:
            month += 12
            year -= 1
        month_starts.append(date(year, month, 1))

    headcount_trend = []
    for month_start in month_starts:
        next_month = date(month_start.year + (month_start.month == 12), 1 if month_start.month == 12 else month_start.month + 1, 1)
        month_end = next_month - timedelta(days=1)
        headcount_trend.append(
            {
                "period": month_start.strftime("%b"),
                "value": len([employee for employee in employees if employee.joining_date <= month_end]),
            }
        )

    engagement_by_period: dict[str, list[Decimal]] = defaultdict(list)
    for survey in engagement:
        engagement_by_period[_period_label(survey.survey_date)].append(survey.engagement_score)
    engagement_trend = [
        {"period": period, "value": _average(values)}
        for period, values in sorted(engagement_by_period.items())[-6:]
    ]

    performance_by_period: dict[str, list[Decimal]] = defaultdict(list)
    for review in performance:
        performance_by_period[review.review_period].append(review.overall_rating)
    performance_trend = [
        {"period": period, "value": _average(values)}
        for period, values in sorted(performance_by_period.items())[-6:]
    ]

    funnel_counter = Counter(application.status for application in applications)
    recruitment_funnel = [
        {"stage": stage.title(), "value": funnel_counter.get(stage, 0)}
        for stage in ["APPLIED", "SCREENING", "INTERVIEW", "OFFER", "HIRED"]
    ]

    department_metrics = []
    departments = db.scalars(select(Department)).all()
    latest_risk_by_employee = {}
    for risk in sorted(risks, key=lambda item: item.data_timestamp):
        latest_risk_by_employee[risk.employee_id] = risk

    training_by_employee: dict[int, list[Decimal]] = defaultdict(list)
    for record in training:
        training_by_employee[record.employee_id].append(record.completion_percentage)

    attendance_by_employee: dict[int, list[AttendanceRecord]] = defaultdict(list)
    for record in attendance:
        attendance_by_employee[record.employee_id].append(record)

    performance_by_employee: dict[int, list[Decimal]] = defaultdict(list)
    for review in performance:
        performance_by_employee[review.employee_id].append(review.overall_rating)

    engagement_by_employee: dict[int, list[Decimal]] = defaultdict(list)
    for survey in engagement:
        engagement_by_employee[survey.employee_id].append(survey.engagement_score)

    for department in departments:
        dept_employees = [employee for employee in employees if employee.department_id == department.id]
        dept_employee_ids = {employee.id for employee in dept_employees}
        dept_attendance = [
            record for employee_id in dept_employee_ids for record in attendance_by_employee.get(employee_id, [])
        ]
        overtime = _average([record.overtime_hours for record in dept_attendance])
        dept_engagement = _average(
            [score for employee_id in dept_employee_ids for score in engagement_by_employee.get(employee_id, [])]
        )
        dept_performance = _average(
            [score for employee_id in dept_employee_ids for score in performance_by_employee.get(employee_id, [])]
        )
        dept_training = _average(
            [
                score
                for employee_id in dept_employee_ids
                for score in training_by_employee.get(employee_id, [])
            ]
        )
        dept_elevated = len(
            [
                employee_id
                for employee_id in dept_employee_ids
                if latest_risk_by_employee.get(employee_id)
                and latest_risk_by_employee[employee_id].risk_band == "ELEVATED"
            ]
        )
        department_metrics.append(
            {
                "department": department.name,
                "headcount": len(dept_employees),
                "engagement": dept_engagement,
                "overtime": overtime,
                "performance": dept_performance,
                "trainingCompletion": dept_training,
                "elevatedRisk": dept_elevated,
            }
        )

    skill_categories = Counter(skill.category for skill in skills)
    employee_skill_categories = Counter(
        employee_skill.skill.category for employee_skill in employee_skills if employee_skill.proficiency_level >= 3
    )
    skill_coverage_chart = [
        {
            "category": category,
            "coverage": round(100 * employee_skill_categories.get(category, 0) / max(count, 1), 1),
        }
        for category, count in skill_categories.items()
    ]

    return {
        "total_employees": len(employees),
        "active_employees": len(active_employees),
        "open_positions": len([job for job in jobs if job.status == "OPEN"]),
        "active_candidates": len(active_candidate_ids) or len(candidates),
        "onboarding_completion": _average([record.completion_percentage for record in training]),
        "average_engagement": current_engagement,
        "skill_coverage": skill_coverage,
        "elevated_risk_count": len(
            [risk for risk in latest_risk_by_employee.values() if risk.risk_band == "ELEVATED"]
        ),
        "headcount_trend": headcount_trend,
        "engagement_trend": engagement_trend,
        "performance_trend": performance_trend,
        "recruitment_funnel": recruitment_funnel,
        "department_metrics": sorted(department_metrics, key=lambda item: item["headcount"], reverse=True),
        "skill_coverage_chart": sorted(skill_coverage_chart, key=lambda item: item["category"]),
        "ai_insights": [
            {
                "id": insight.id,
                "title": insight.title,
                "summary": insight.summary,
                "severity": insight.severity,
                "evidence": insight.evidence,
                "department": next(
                    (department.name for department in departments if department.id == insight.department_id),
                    "Organization",
                ),
                "recommended_action": insight.recommended_action,
                "confidence": _number(insight.confidence, 2),
            }
            for insight in insights
        ],
        "recommendations": [
            {
                "id": recommendation.id,
                "title": recommendation.title,
                "description": recommendation.description,
                "priority": recommendation.priority,
                "status": recommendation.status,
                "evidence": recommendation.evidence or [],
            }
            for recommendation in recommendations
        ],
        "demo_notice": "Synthetic demonstration data.",
    }

