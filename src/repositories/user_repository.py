from sqlalchemy.orm import Session
from model import User
from schemas.user_schema import UserCreate, UserUpdate
from utils.security import hash_password
from typing import List
from datetime import date

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def create(self, user_data: UserCreate) -> User:
        db_user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            password=hash_password(user_data.password.get_secret_value()),
            role=user_data.role,
            register_date=user_data.register_date,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, user_id: int, user_data: UserUpdate) -> User | None:
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return None

        for key, value in user_data.model_dump().items():
            setattr(db_user, key, value)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete(self, user_id: int) -> bool:
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return False

        self.db.delete(db_user)
        self.db.commit()
        return True
    
    def get_all_users(self) -> List[User]:
        return self.db.query(User).all()
    
    def soft_delete(self, user_id: int) -> bool:
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return False

        db_user.is_active = False
        self.db.commit()
        return True

    def update_last_login(self, user_id: int) -> User | None:
        db_user = self.db.query(User).filter(User.id == user_id).first()

        db_user.last_login_date = date.today()

        self.db.commit()
        self.db.refresh(db_user)
        return db_user
