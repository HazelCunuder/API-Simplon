from typing import List
from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column
from datetime import date
from model.course import Course
from model.user import User
from model.database import Base

session_courses = Table(
    "sessions_courses",
    Base.metadata,
    Column("session_id", Integer, ForeignKey('session_table.id')),
    Column("course_id", Integer, ForeignKey('course_table.id')),
)

class Session(Base):
    __tablename__ = 'session_table'

    id: Mapped[int] = mapped_column(primary_key=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey('user_table.id'))
    courses: Mapped[List["Course"]] = relationship(secondary=session_courses),
    teacher: Mapped["User"] = relationship(back_populates="sessions")
    start_date: Mapped[date] = mapped_column()
    end_date: Mapped[date] = mapped_column()
    capacity: Mapped[int] = mapped_column()