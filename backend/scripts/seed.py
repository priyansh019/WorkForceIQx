from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from random import Random

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.permissions import RoleName
from app.core.security import hash_password
from app.db.init_db import create_tables, ensure_roles
from app.db.session import SessionLocal
from app.models import (
    Application,
    AttendanceRecord,
    Candidate,
    CandidateSkill,
    Department,
    Employee,
    EmployeeRiskScore,
    EmployeeSkill,
    EmployeeTraining,
    EngagementSurvey,
    HrDocument,
    HrDocumentChunk,
    Job,
    JobRole,
    PerformanceReview,
    Recommendation,
    Role,
    Skill,
    TrainingCourse,
    User,
    WorkforceInsight,
)

RANDOM = Random(42)
DEMO_NOTICE = "Synthetic demonstration data."
DEMO_USERS = [
    ("admin@workforceiq.demo", "Demo Admin", "Demo@123", RoleName.ADMIN),
    ("hr.admin@workforceiq.demo", "HR Admin", "HrAdminPass123!", RoleName.HR_ADMIN),
    ("recruiter@workforceiq.demo", "Recruiter User", "RecruiterPass123!", RoleName.RECRUITER),
    ("employee@workforceiq.demo", "Employee User", "EmployeePass123!", RoleName.EMPLOYEE),
]

DEPARTMENTS = [
    "Engineering",
    "Cloud Engineering",
    "Product",
    "Sales",
    "Marketing",
    "Customer Success",
    "HR",
    "Finance",
    "Operations",
    "Data Science",
]

ROLE_TITLES = [
    "Backend Engineer",
    "Cloud Backend Engineer",
    "Frontend Engineer",
    "Platform Engineer",
    "Data Scientist",
    "ML Engineer",
    "Product Manager",
    "UX Designer",
    "Account Executive",
    "Sales Development Rep",
    "Customer Success Manager",
    "HR Business Partner",
    "Recruiter",
    "Finance Analyst",
    "Operations Manager",
    "QA Engineer",
    "Security Engineer",
    "Analytics Engineer",
    "Marketing Manager",
    "Support Specialist",
]

SKILL_NAMES = [
    "Python",
    "FastAPI",
    "PostgreSQL",
    "SQL",
    "React",
    "Next.js",
    "TypeScript",
    "Tailwind CSS",
    "AWS",
    "Kubernetes",
    "Terraform",
    "Docker",
    "CI/CD",
    "Data Modeling",
    "Machine Learning",
    "Scikit-learn",
    "Pandas",
    "Prompt Engineering",
    "Vector Search",
    "HR Analytics",
    "Recruiting",
    "Interviewing",
    "Policy Writing",
    "Employee Relations",
    "Performance Management",
    "Onboarding",
    "Salesforce",
    "Negotiation",
    "Account Planning",
    "Customer Health",
    "Product Strategy",
    "Roadmapping",
    "UX Research",
    "Figma",
    "Financial Modeling",
    "Forecasting",
    "Compliance",
    "Security Training",
    "Incident Response",
    "Data Visualization",
]

FIRST_NAMES = [
    "Aarav",
    "Isha",
    "Maya",
    "Dev",
    "Priya",
    "Neel",
    "Anika",
    "Rohan",
    "Sara",
    "Kabir",
    "Meera",
    "Vikram",
    "Nina",
    "Arjun",
    "Leah",
    "Owen",
    "Mina",
    "Sam",
    "Tara",
    "Noah",
]

LAST_NAMES = [
    "Shah",
    "Patel",
    "Iyer",
    "Rao",
    "Mehta",
    "Kapoor",
    "Menon",
    "Singh",
    "Brown",
    "Garcia",
    "Chen",
    "Wilson",
    "Thomas",
    "Nair",
    "Das",
]


def _decimal(value: float, digits: int = 2) -> Decimal:
    return Decimal(str(round(value, digits)))


def _role_for_department(index: int, department: Department) -> str:
    if department.name == "Engineering":
        return RANDOM.choice(["Backend Engineer", "Frontend Engineer", "QA Engineer", "Platform Engineer"])
    if department.name == "Cloud Engineering":
        return RANDOM.choice(["Cloud Backend Engineer", "Platform Engineer", "Security Engineer"])
    if department.name == "Data Science":
        return RANDOM.choice(["Data Scientist", "ML Engineer", "Analytics Engineer"])
    if department.name == "Sales":
        return RANDOM.choice(["Account Executive", "Sales Development Rep"])
    if department.name == "HR":
        return RANDOM.choice(["HR Business Partner", "Recruiter"])
    return ROLE_TITLES[index % len(ROLE_TITLES)]


def _month_start(day: date, months_ago: int) -> date:
    month = day.month - months_ago
    year = day.year
    while month <= 0:
        month += 12
        year -= 1
    return date(year, month, 1)


def seed_users(db: Session) -> None:
    ensure_roles(db)
    roles = {role.name: role for role in db.scalars(select(Role)).all()}
    for email, full_name, password, role_name in DEMO_USERS:
        existing = db.scalar(select(User).where(User.email == email))
        if existing is not None:
            existing.full_name = full_name
            existing.hashed_password = hash_password(password)
            existing.role = roles[role_name.value]
            continue
        db.add(
            User(
                email=email,
                full_name=full_name,
                hashed_password=hash_password(password),
                role=roles[role_name.value],
            )
        )
    db.commit()


def seed_workforce_data(db: Session) -> None:
    if db.scalar(select(Department).limit(1)) is not None:
        return

    departments = [Department(name=name, description=f"{DEMO_NOTICE} {name} department.") for name in DEPARTMENTS]
    db.add_all(departments)
    db.commit()

    department_by_name = {department.name: department for department in departments}
    job_roles = []
    for index, title in enumerate(ROLE_TITLES):
        department = departments[index % len(departments)]
        if "Cloud" in title:
            department = department_by_name["Cloud Engineering"]
        elif title in {"Backend Engineer", "Frontend Engineer", "Platform Engineer", "QA Engineer", "Security Engineer"}:
            department = department_by_name["Engineering"]
        elif title in {"Data Scientist", "ML Engineer", "Analytics Engineer"}:
            department = department_by_name["Data Science"]
        job_roles.append(
            JobRole(
                title=title,
                department_id=department.id,
                description=f"{DEMO_NOTICE} {title} role.",
                required_skills=", ".join(RANDOM.sample(SKILL_NAMES, 5)),
            )
        )
    db.add_all(job_roles)

    skills = []
    categories = ["Engineering", "Cloud", "Data", "HR", "Business"]
    for index, name in enumerate(SKILL_NAMES):
        skills.append(
            Skill(
                name=name,
                category=categories[index % len(categories)],
                description=f"{DEMO_NOTICE} {name} capability.",
            )
        )
    db.add_all(skills)
    db.commit()

    role_by_title = {role.title: role for role in job_roles}
    skill_by_name = {skill.name: skill for skill in skills}
    today = date.today()
    employees = []
    for index in range(300):
        department = departments[index % len(departments)]
        title = _role_for_department(index, department)
        if index == 41:
            department = department_by_name["Cloud Engineering"]
            title = "Cloud Backend Engineer"
        employees.append(
            Employee(
                employee_code=f"EMP-{1001 + index}",
                first_name=FIRST_NAMES[index % len(FIRST_NAMES)],
                last_name=LAST_NAMES[(index * 3) % len(LAST_NAMES)],
                email=f"employee{1001 + index}@workforceiq.demo",
                phone=f"+1-555-{1000 + index}",
                department_id=department.id,
                job_role_id=role_by_title[title].id,
                manager_id=None,
                location=RANDOM.choice(["Bengaluru", "Pune", "Austin", "London", "Remote"]),
                joining_date=today - timedelta(days=RANDOM.randint(45, 2200)),
                employment_status="ACTIVE" if index % 37 else "LEAVE",
                employment_type=RANDOM.choice(["FULL_TIME", "FULL_TIME", "FULL_TIME", "CONTRACT"]),
            )
        )
    db.add_all(employees)
    db.commit()

    employees = db.scalars(select(Employee).order_by(Employee.id)).all()
    for index, employee in enumerate(employees):
        if index > 10:
            employee.manager_id = employees[index % 10].id
    db.commit()

    employee_skills = []
    for employee in employees:
        base_skill_names = ["SQL", "Data Visualization"]
        if employee.department.name in {"Engineering", "Cloud Engineering"}:
            base_skill_names += ["Python", "FastAPI", "PostgreSQL", "Docker"]
        if employee.department.name == "Cloud Engineering":
            base_skill_names += ["AWS", "Kubernetes", "Terraform"]
        if employee.department.name == "Data Science":
            base_skill_names += ["Python", "Pandas", "Machine Learning", "Scikit-learn"]
        if employee.department.name == "HR":
            base_skill_names += ["HR Analytics", "Policy Writing", "Employee Relations", "Onboarding"]
        if employee.department.name == "Sales":
            base_skill_names += ["Salesforce", "Negotiation", "Account Planning"]
        selected = list(dict.fromkeys(base_skill_names + RANDOM.sample(SKILL_NAMES, 4)))
        for name in selected[:8]:
            proficiency = RANDOM.randint(2, 5)
            if employee.department.name == "Cloud Engineering" and name in {"Kubernetes", "Terraform", "AWS"}:
                proficiency = RANDOM.choice([1, 2, 3])
            employee_skills.append(
                EmployeeSkill(
                    employee_id=employee.id,
                    skill_id=skill_by_name[name].id,
                    proficiency_level=proficiency,
                    years_experience=_decimal(RANDOM.uniform(0.5, 8), 1),
                    last_verified_at=datetime.now(timezone.utc) - timedelta(days=RANDOM.randint(1, 180)),
                )
            )
    db.add_all(employee_skills)

    courses = [
        TrainingCourse(
            name=f"{name} Accelerator",
            description=f"{DEMO_NOTICE} Role-ready learning path for {name}.",
            skills=name,
            difficulty=RANDOM.choice(["Beginner", "Intermediate", "Advanced"]),
            duration=f"{RANDOM.randint(2, 8)} weeks",
        )
        for name in SKILL_NAMES[:30]
    ]
    db.add_all(courses)
    db.commit()

    attendance_records = []
    engagement_records = []
    performance_reviews = []
    training_records = []
    risk_scores = []
    quarter_dates = [today - timedelta(days=180), today - timedelta(days=90), today]
    review_periods = ["2026 Q1", "2026 Q2", "2026 Q3"]
    for employee in employees:
        dept_name = employee.department.name
        for day_index in range(60):
            record_date = today - timedelta(days=day_index)
            if record_date.weekday() >= 5:
                continue
            overtime_base = 1.2 if dept_name in {"Engineering", "Cloud Engineering"} else 0.4
            if dept_name == "Engineering" and day_index < 30:
                overtime_base = 2.3
            attendance_records.append(
                AttendanceRecord(
                    employee_id=employee.id,
                    date=record_date,
                    status=RANDOM.choices(["PRESENT", "REMOTE", "LEAVE", "ABSENT"], [72, 18, 7, 3])[0],
                    hours_worked=_decimal(RANDOM.uniform(6.5, 8.8), 2),
                    overtime_hours=_decimal(max(0, RANDOM.gauss(overtime_base, 0.5)), 2),
                    late_minutes=max(0, int(RANDOM.gauss(7, 9))),
                )
            )
        for q_index, survey_date in enumerate(quarter_dates):
            base = 7.7
            if dept_name == "Engineering":
                base = [7.8, 7.4, 6.8][q_index]
            elif dept_name == "Cloud Engineering":
                base = [7.5, 7.1, 6.7][q_index]
            elif dept_name == "HR":
                base = [8.0, 8.1, 8.0][q_index]
            engagement_score = max(1, min(10, RANDOM.gauss(base, 0.45)))
            engagement_records.append(
                EngagementSurvey(
                    employee_id=employee.id,
                    survey_date=survey_date,
                    engagement_score=_decimal(engagement_score),
                    manager_score=_decimal(max(1, min(10, engagement_score + RANDOM.uniform(-0.6, 0.4)))),
                    workload_score=_decimal(max(1, min(10, engagement_score - RANDOM.uniform(0.1, 1.0)))),
                    growth_score=_decimal(max(1, min(10, engagement_score + RANDOM.uniform(-0.5, 0.7)))),
                    satisfaction_score=_decimal(max(1, min(10, engagement_score + RANDOM.uniform(-0.4, 0.4)))),
                )
            )
            performance_reviews.append(
                PerformanceReview(
                    employee_id=employee.id,
                    review_period=review_periods[q_index],
                    overall_rating=_decimal(max(1, min(5, RANDOM.gauss(3.7, 0.5))), 2),
                    goal_completion=_decimal(max(35, min(100, RANDOM.gauss(78, 12))), 2),
                    manager_summary=f"{DEMO_NOTICE} Review summary for {employee.employee_code}.",
                    strengths="Execution, collaboration, and learning agility.",
                    improvement_areas="Prioritization and cross-functional visibility.",
                )
            )
        for course in RANDOM.sample(courses, 3):
            completion = RANDOM.gauss(82, 12)
            if dept_name in {"Engineering", "Cloud Engineering"}:
                completion = RANDOM.gauss(70, 16)
            training_records.append(
                EmployeeTraining(
                    employee_id=employee.id,
                    course_id=course.id,
                    status="COMPLETED" if completion >= 85 else "IN_PROGRESS",
                    completion_percentage=_decimal(max(0, min(100, completion)), 2),
                    completed_at=datetime.now(timezone.utc) if completion >= 85 else None,
                )
            )
        risk_probability = RANDOM.uniform(0.08, 0.28)
        if dept_name in {"Engineering", "Cloud Engineering"}:
            risk_probability += RANDOM.uniform(0.12, 0.32)
        if employee.id % 11 == 0:
            risk_probability += 0.18
        risk_probability = min(risk_probability, 0.91)
        risk_band = "LOW" if risk_probability < 0.33 else "MODERATE" if risk_probability < 0.62 else "ELEVATED"
        risk_scores.append(
            EmployeeRiskScore(
                employee_id=employee.id,
                risk_probability=_decimal(risk_probability, 4),
                risk_band=risk_band,
                contributing_features={
                    "engagement": "declining" if dept_name in {"Engineering", "Cloud Engineering"} else "stable",
                    "overtime": "above team baseline" if dept_name in {"Engineering", "Cloud Engineering"} else "normal",
                    "training_completion": "below target" if dept_name in {"Engineering", "Cloud Engineering"} else "healthy",
                },
                historical_context={"notice": DEMO_NOTICE, "model_input_window": "last 90 days"},
                model_version="demo-risk-v1",
                data_timestamp=datetime.now(timezone.utc),
            )
        )
    db.add_all(attendance_records)
    db.add_all(engagement_records)
    db.add_all(performance_reviews)
    db.add_all(training_records)
    db.add_all(risk_scores)

    jobs = []
    for index in range(60):
        title = "Cloud Backend Engineer" if index == 0 else ROLE_TITLES[index % len(ROLE_TITLES)]
        jobs.append(
            Job(
                title=title,
                department="Cloud Engineering" if "Cloud" in title else DEPARTMENTS[index % len(DEPARTMENTS)],
                description=f"{DEMO_NOTICE} Hiring plan for {title}.",
                required_skills=", ".join(
                    ["Python", "FastAPI", "PostgreSQL", "AWS", "Kubernetes"]
                    if "Cloud" in title
                    else RANDOM.sample(SKILL_NAMES, 5)
                ),
                preferred_skills=", ".join(RANDOM.sample(SKILL_NAMES, 3)),
                minimum_experience=_decimal(RANDOM.uniform(2, 8), 1),
                location=RANDOM.choice(["Bengaluru", "Pune", "Austin", "Remote"]),
                employment_type="FULL_TIME",
                status=RANDOM.choice(["OPEN", "OPEN", "OPEN", "PAUSED", "CLOSED"]),
            )
        )
    db.add_all(jobs)
    db.commit()

    jobs = db.scalars(select(Job).order_by(Job.id)).all()
    candidates = []
    for index in range(180):
        candidates.append(
            Candidate(
                name="Candidate Demo 01" if index == 0 else f"Candidate Demo {index + 1:02d}",
                email=f"candidate{index + 1:03d}@workforceiq.demo",
                phone=f"+1-444-{2000 + index}",
                resume_text=f"{DEMO_NOTICE} Resume with Python, SQL, collaboration, and project delivery evidence.",
                experience_years=_decimal(RANDOM.uniform(1, 12), 1),
                education=RANDOM.choice(["B.Tech Computer Science", "MBA", "M.S. Data Science", "B.Com"]),
            )
        )
    db.add_all(candidates)
    db.commit()

    candidates = db.scalars(select(Candidate).order_by(Candidate.id)).all()
    applications = []
    candidate_skills = []
    for index, candidate in enumerate(candidates):
        selected_job = jobs[index % len(jobs)]
        applications.append(
            Application(
                candidate_id=candidate.id,
                job_id=selected_job.id,
                status=RANDOM.choices(["APPLIED", "SCREENING", "INTERVIEW", "OFFER", "HIRED", "REJECTED"], [35, 25, 18, 8, 6, 8])[0],
            )
        )
        skill_names = ["Python", "SQL", "FastAPI", "PostgreSQL"] + RANDOM.sample(SKILL_NAMES, 3)
        for name in list(dict.fromkeys(skill_names))[:6]:
            candidate_skills.append(
                CandidateSkill(
                    candidate_id=candidate.id,
                    skill_id=skill_by_name[name].id,
                    proficiency=RANDOM.randint(2, 5),
                    years_experience=_decimal(RANDOM.uniform(0.5, 7), 1),
                )
            )
    db.add_all(applications)
    db.add_all(candidate_skills)

    policy_texts = {
        "Relocation Policy": "Synthetic demonstration policy - not a real company policy. Section 4.2: eligible employees may request relocation reimbursement when the relocation is business approved, manager endorsed, and receipts are submitted within 30 days.",
        "Remote Work Policy": "Synthetic demonstration policy - not a real company policy. Employees may work remotely when role requirements, data security expectations, and manager coverage plans are satisfied.",
        "Learning and Development Policy": "Synthetic demonstration policy - not a real company policy. Employees should have equitable access to role-relevant learning paths and manager-approved development goals.",
    }
    for title, content in policy_texts.items():
        document = HrDocument(
            title=title,
            document_type="POLICY",
            source_filename=f"{title.lower().replace(' ', '-')}.txt",
            storage_path=f"demo-policies/{title.lower().replace(' ', '-')}.txt",
            uploaded_by_user_id=None,
            synthetic_demo_notice=DEMO_NOTICE,
        )
        db.add(document)
        db.flush()
        db.add(
            HrDocumentChunk(
                document_id=document.id,
                chunk_index=0,
                content=content,
                embedding=[0.0] * 1536,
                page_number=1,
                section="Demo policy summary",
                chunk_metadata={"notice": DEMO_NOTICE},
            )
        )

    engineering = department_by_name["Engineering"]
    cloud = department_by_name["Cloud Engineering"]
    insights = [
        WorkforceInsight(
            title="Engineering workload and engagement indicators changed together",
            summary="Engineering shows lower engagement, higher overtime, and reduced learning completion in the latest period.",
            severity="high",
            department_id=engineering.id,
            evidence=[
                {"source": "engagement_surveys", "metric": "Engagement", "previous_value": 7.8, "current_value": 6.8, "period": "2026 Q3"},
                {"source": "attendance_records", "metric": "Overtime", "previous_value": 1.2, "current_value": 2.3, "period": "Last 30 days"},
                {"source": "employee_training", "metric": "Training completion", "previous_value": 84, "current_value": 70, "period": "Current quarter"},
            ],
            metrics={"engagement_delta": -1.0, "overtime_delta": 1.1, "training_delta": -14},
            time_period="2026 Q3",
            recommended_action="Review workload distribution and verify training access for engineering teams.",
            confidence=_decimal(0.86, 3),
            generated_at=datetime.now(timezone.utc),
        ),
        WorkforceInsight(
            title="Cloud role coverage has Kubernetes and Terraform gaps",
            summary="Cloud Engineering has strong Python and SQL coverage, but Kubernetes and Terraform proficiency remains below target for cloud backend roles.",
            severity="medium",
            department_id=cloud.id,
            evidence=[
                {"source": "employee_skills", "metric": "Kubernetes coverage", "current_value": 42, "period": "Current"},
                {"source": "employee_skills", "metric": "Terraform coverage", "current_value": 38, "period": "Current"},
                {"source": "jobs", "metric": "Cloud Backend Engineer required skills", "current_value": "AWS, Kubernetes, Terraform", "period": "Open roles"},
            ],
            metrics={"kubernetes_coverage": 42, "terraform_coverage": 38},
            time_period="Current",
            recommended_action="Offer targeted cloud infrastructure learning paths and review hiring focus.",
            confidence=_decimal(0.81, 3),
            generated_at=datetime.now(timezone.utc),
        ),
    ]
    db.add_all(insights)
    db.flush()
    db.add_all(
        [
            Recommendation(
                type="WORKLOAD_REVIEW",
                title="Review Engineering workload distribution",
                description="Several indicators suggest HR should review workload balance and capacity planning with managers.",
                evidence=insights[0].evidence,
                priority="HIGH",
                status="NEW",
            ),
            Recommendation(
                type="SKILL_GAP",
                title="Launch cloud infrastructure learning path",
                description="Kubernetes and Terraform gaps are visible for Cloud Backend Engineer coverage.",
                evidence=insights[1].evidence,
                priority="MEDIUM",
                status="NEW",
            ),
        ]
    )
    db.commit()


def main() -> None:
    create_tables()
    db = SessionLocal()
    try:
        seed_users(db)
        seed_workforce_data(db)
        print("Seeded WorkForceIQ demo users and synthetic workforce test data.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
