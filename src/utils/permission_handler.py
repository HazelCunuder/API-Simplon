from fastapi import HTTPException, status, Depends
from model.user import Role
from utils.security import get_logged_user

def role_checker(required_role: Role):
    async def check_role(user = Depends(get_logged_user)):
        if user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return user
    return check_role