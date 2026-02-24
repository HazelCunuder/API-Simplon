from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from enum import IntEnum
from model.database import Base

class Role(IntEnum):
    ADMIN = 0
    TEACHER = 1
    STUDENT = 2

class User(Base):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    role: Mapped[Role] = mapped_column(nullable=False, default=Role.STUDENT)
    register_date: Mapped[date] = mapped_column(nullable=False)
    sessions: Mapped[List["Session"]] = relationship(back_populates="teacher")