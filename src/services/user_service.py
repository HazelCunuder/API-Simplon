from model import User
from repositories.user_repository import UserRepository
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from model.database import get_db
from schemas.user_schema import UserCreate, UserUpdate, UserRead
from datetime import date, timedelta

class UserService:
    def __init__(self, db: Session = Depends(get_db)):
        self.repo = UserRepository(db)

    def get_user(self, user_id: int):
        user = self.repo.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return UserRead.model_validate(user)

    def create_user(self, user_data: UserCreate):
        existing_user = self.repo.db.query(User).filter(
            User.email == user_data.email
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        return self.repo.create(user_data)

    def update_user(self, user_id: int, user_data: UserUpdate):
        return self.repo.update(user_id, user_data)

    def delete_user(self, user_id: int):
        return self.repo.delete(user_id)
    
    
    def delete_inactive_user_data(self):
        users = self.repo.get_all_users()
        current_date = date.today()

        for user in users:
            if user.last_login_date is None:
                continue
            if user.last_login_date + timedelta(days=1095) < current_date:
                self.repo.delete(user.id)

    def soft_delete_user(self, user_id: int):
        return self.repo.soft_delete(user_id)
