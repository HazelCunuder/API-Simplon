from enum import Enum
from typing import List
from sqlalchemy import ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column
from datetime import date
from model.database import Base

class Status(Enum):
    PLANNED = "PLANNED"
    ONGOING = "ONGOING"
    DONE = "DONE"

class Session(Base):
    __tablename__ = 'session_table'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey('course_table.id'))
    start_date: Mapped[date] = mapped_column()
    end_date: Mapped[date] = mapped_column()
    capacity: Mapped[int] = mapped_column()
    status: Mapped[Status] = mapped_column(SQLEnum(Status, native_enum=True), nullable=False, default=Status.PLANNED)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

    enrollments: Mapped[List["UserSession"]] = relationship(back_populates="session")