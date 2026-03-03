from fastapi import HTTPException, status, Depends
from model.user import Role
from utils.security import get_logged_user

def role_checker(required_role: Role):
    async def check_role(user = Depends(get_logged_user)):
        allowed_roles = [Role.STUDENT]

        match user.role:
            case Role.TEACHER:
                allowed_roles = [Role.STUDENT, Role.TEACHER]
            case Role.ADMIN:
                allowed_roles = [Role.STUDENT, Role.TEACHER, Role.ADMIN]

        if not required_role in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return user
    return check_role