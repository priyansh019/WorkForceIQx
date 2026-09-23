from datetime import datetime

from pydantic import BaseModel, EmailStr


class RoleRead(BaseModel):
    id: int
    name: str
    description: str | None

    model_config = {"from_attributes": True}


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool
    role: RoleRead
    employee_id: int | None
    created_at: datetime

    model_config = {"from_attributes": True}

