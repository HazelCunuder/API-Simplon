from fastapi import APIRouter, status, Depends

from model.user import Role
from schemas.user_schema import UserCreate, UserUpdate, UserRead
from services.user_service import UserService
from utils.permission_handler import role_checker
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

@router.patch("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
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
    __ = Depends(role_checker(Role.ADMIN)),
    service: UserService = Depends()
):
    return service.delete_user(user_id)

@router.patch("/soft-delete/{user_id}", status_code=status.HTTP_200_OK)
async def soft_delete_user(
    user_id: int,
    _: dict = Depends(verify_token),
    service: UserService = Depends()
):
    return service.soft_delete_user(user_id)
