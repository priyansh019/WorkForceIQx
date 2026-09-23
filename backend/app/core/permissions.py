from enum import StrEnum


class RoleName(StrEnum):
    ADMIN = "ADMIN"
    HR_ADMIN = "HR_ADMIN"
    HR_MANAGER = "HR_MANAGER"
    RECRUITER = "RECRUITER"
    MANAGER = "MANAGER"
    EMPLOYEE = "EMPLOYEE"


ROLE_PERMISSIONS: dict[RoleName, set[str]] = {
    RoleName.ADMIN: {"*"},
    RoleName.HR_ADMIN: {
        "employee:read",
        "employee:write",
        "recruitment:read",
        "recruitment:write",
        "policy:read",
        "policy:write",
        "analytics:read",
        "onboarding:write",
    },
    RoleName.HR_MANAGER: {
        "employee:read",
        "performance:read",
        "analytics:read",
        "onboarding:write",
    },
    RoleName.RECRUITER: {
        "recruitment:read",
        "recruitment:write",
        "interview:write",
    },
    RoleName.MANAGER: {
        "team:read",
        "performance:read",
        "onboarding:write",
        "analytics:read",
    },
    RoleName.EMPLOYEE: {"self:read", "self:update"},
}


def role_has_permission(role_name: str, permission: str) -> bool:
    role = RoleName(role_name)
    permissions = ROLE_PERMISSIONS[role]
    return "*" in permissions or permission in permissions

