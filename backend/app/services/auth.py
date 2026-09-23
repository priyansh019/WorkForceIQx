from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.core.permissions import RoleName
from app.core.security import create_access_token, hash_password, verify_password
from app.models import Role, User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.services.audit import log_action


def _get_role(db: Session, role_name: RoleName) -> Role:
    role = db.scalar(select(Role).where(Role.name == role_name.value))
    if role is None:
        raise AppError("ROLE_NOT_FOUND", f"Role {role_name.value} is not configured.", 500)
    return role


def register_user(db: Session, payload: RegisterRequest) -> TokenResponse:
    existing = db.scalar(select(User).where(func.lower(User.email) == payload.email.lower()))
    if existing is not None:
        raise AppError("EMAIL_ALREADY_REGISTERED", "A user with this email already exists.", 409)

    user_count = db.scalar(select(func.count(User.id))) or 0
    role_name = RoleName.ADMIN if user_count == 0 else RoleName.EMPLOYEE
    role = _get_role(db, role_name)

    user = User(
        email=payload.email.lower(),
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    log_action(db, user_id=user.id, action="user_registered", resource_type="user", resource_id=str(user.id))

    token = create_access_token(str(user.id), {"role": user.role.name})
    return TokenResponse(access_token=token, user=user)


def authenticate_user(db: Session, payload: LoginRequest) -> TokenResponse:
    user = db.scalar(select(User).where(func.lower(User.email) == payload.email.lower()))
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise AppError("INVALID_CREDENTIALS", "Email or password is incorrect.", 401)
    if not user.is_active:
        raise AppError("USER_INACTIVE", "This account is inactive.", 403)

    log_action(db, user_id=user.id, action="login", resource_type="user", resource_id=str(user.id))
    token = create_access_token(str(user.id), {"role": user.role.name})
    return TokenResponse(access_token=token, user=user)

