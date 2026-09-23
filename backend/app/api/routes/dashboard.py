from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.common import ApiResponse
from app.services.dashboard import get_dashboard_summary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=ApiResponse[dict])
def dashboard_summary(db: Session = Depends(get_db)) -> ApiResponse[dict]:
    return ApiResponse(data=get_dashboard_summary(db))

