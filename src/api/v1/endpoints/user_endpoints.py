from fastapi import APIRouter, status
from schemas.user_schema import UserCreate, UserUpdate

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    # TODO : call service
    return {"message": "User created", "data": user}

@router.put("/users/{user_id}")
async def update_user(user_id: int, user: UserUpdate):
    # TODO : call service
    return {"message": f"User {user_id} updated"}

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    # TODO : call service
    return None
