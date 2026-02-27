from enum import IntEnum
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column
from datetime import date
from model.database import Base

class Status(IntEnum):
    PLANNED = 0
    ONGOING = 1
    DONE = 2

class Session(Base):
    __tablename__ = 'session_table'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey('user_table.id'))
    course_id: Mapped[int] = mapped_column(ForeignKey('course_table.id'))
    start_date: Mapped[date] = mapped_column()
    end_date: Mapped[date] = mapped_column()
    capacity: Mapped[int] = mapped_column()
    status: Mapped[int] = mapped_column(nullable=False)
    
    teacher: Mapped["User"] = relationship(back_populates="sessions")
    enrollments: Mapped[List["UserSession"]] = relationship(back_populates="session")