from typing import List
from sqlalchemy import String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from enum import Enum
from model.database import Base

class Role(str, Enum):
    ADMIN = "ADMIN"
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"

class User(Base):
    __tablename__ = "user_table"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[Role] = mapped_column(SQLEnum(Role, native_enum=True), nullable=False, default=Role.STUDENT)
    register_date: Mapped[date] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    last_login_date: Mapped[date] = mapped_column(nullable=True)

    enrollments: Mapped[List["UserSession"]] = relationship(back_populates="user")