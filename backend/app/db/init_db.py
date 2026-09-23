from sqlalchemy.orm import Session

from app.core.permissions import RoleName
from app.db.base import Base
from app.db.session import engine
from app.models import Role


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def ensure_roles(db: Session) -> None:
    existing = {role.name for role in db.query(Role).all()}
    for role_name in RoleName:
        if role_name.value not in existing:
            db.add(Role(name=role_name.value, description=f"{role_name.value} access role"))
    db.commit()

