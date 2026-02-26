from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from services.auth_service import AuthService
from utils.exceptions import InvalidCredentialsError

router = APIRouter(prefix="/login", tags=["login"])

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends()
):
    try:
        return service.login(form_data.username, form_data.password)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )