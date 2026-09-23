from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health_check() -> dict:
    return {"success": True, "data": {"status": "ok", "app": settings.app_name}}

