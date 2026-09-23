from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.api.deps import require_roles
from app.core.permissions import RoleName
from app.db.session import get_db
from app.models import User
from app.schemas.common import ApiResponse
from app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=ApiResponse[list[UserRead]])
def list_users(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    _: User = Depends(require_roles(RoleName.ADMIN, RoleName.HR_ADMIN)),
    db: Session = Depends(get_db),
) -> ApiResponse[list[UserRead]]:
    users = db.scalars(
        select(User)
        .options(joinedload(User.role))
        .order_by(User.created_at.desc())
        .offset(offset)
        .limit(limit)
    ).all()
    return ApiResponse(data=list(users))

