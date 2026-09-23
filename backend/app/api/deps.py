from collections.abc import Callable

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.errors import AppError
from app.core.permissions import RoleName, role_has_permission
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models import User
from app.services.audit import log_action

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise AppError("NOT_AUTHENTICATED", "Authentication is required.", 401)

    payload = decode_access_token(credentials.credentials)
    subject = payload.get("sub")
    if subject is None:
        raise AppError("INVALID_TOKEN", "Authentication token is missing a subject.", 401)

    user = db.scalar(
        select(User).options(joinedload(User.role)).where(User.id == int(subject))
    )
    if user is None:
        raise AppError("USER_NOT_FOUND", "Authenticated user no longer exists.", 401)
    if not user.is_active:
        raise AppError("USER_INACTIVE", "This account is inactive.", 403)
    return user


def require_roles(*roles: RoleName) -> Callable[[User], User]:
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        allowed = {role.value for role in roles}
        if current_user.role.name not in allowed:
            raise AppError("FORBIDDEN", "You do not have access to this resource.", 403)
        return current_user

    return dependency


def require_permission(permission: str) -> Callable[[User], User]:
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if not role_has_permission(current_user.role.name, permission):
            raise AppError("FORBIDDEN", "You do not have access to this resource.", 403)
        return current_user

    return dependency


def audit_protected_read(
    *,
    db: Session,
    user: User,
    resource_type: str,
    resource_id: str,
    action: str,
) -> None:
    log_action(
        db,
        user_id=user.id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
    )

