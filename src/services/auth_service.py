from datetime import timedelta
from fastapi import Depends
from model import Session
from model.database import get_db
from repositories.user_repository import UserRepository
from schemas.auth_schema import TokenResponse
from utils.exceptions import InvalidCredentialsError
from utils.security import verify_password, create_access_token

ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthService:
    def __init__(self, db: Session = Depends(get_db)):
        self.repo = UserRepository(db)

    def login(self, email: str, password: str):
        user = self.repo.get_user_by_email(email)

        if not user or not verify_password(user.password, password):
            raise InvalidCredentialsError("Invalid credentials")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer"
        )