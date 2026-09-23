from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import audit_protected_read, get_current_user
from app.db.session import get_db
from app.models import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.common import ApiResponse
from app.schemas.user import UserRead
from app.services.auth import authenticate_user, register_user

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=ApiResponse[TokenResponse], status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> ApiResponse[TokenResponse]:
    return ApiResponse(data=register_user(db, payload))


@router.post("/login", response_model=ApiResponse[TokenResponse])
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> ApiResponse[TokenResponse]:
    return ApiResponse(data=authenticate_user(db, payload))


@router.get("/me", response_model=ApiResponse[UserRead])
def me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[UserRead]:
    audit_protected_read(
        db=db,
        user=current_user,
        resource_type="user",
        resource_id=str(current_user.id),
        action="current_user_viewed",
    )
    return ApiResponse(data=current_user)

