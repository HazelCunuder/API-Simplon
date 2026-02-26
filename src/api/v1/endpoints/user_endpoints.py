from fastapi import APIRouter, status, Depends
from schemas.user_schema import UserCreate, UserUpdate
from services.user_service import UserService
from utils.security import verify_token

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(
    user_id: int,
    _: dict = Depends(verify_token),
    service: UserService = Depends()
):
    return service.get_user(user_id)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    service: UserService = Depends()
):
    return service.create_user(user)

@router.put("/{user_id}")
async def update_user(
    user_id: int,
    user: UserUpdate,
    _: dict = Depends(verify_token),
    service: UserService = Depends()
):
    return service.update_user(user_id, user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    _: dict = Depends(verify_token),
    service: UserService = Depends()
):
    return service.delete_user(user_id)
