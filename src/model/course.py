from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from model.database import Base
from enum import IntEnum

class Level(IntEnum):
    BEGINNER = 0
    INTERMEDIATE = 1
    ADVANCED = 2
    EXPERT = 3

class Status(IntEnum):
    PLANNED = 0
    ONGOING = 1
    DONE = 2

class Course(Base):

    __tablename__ = "course_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    duration: Mapped[int] = mapped_column(nullable=False)
    level: Mapped[int] = mapped_column(nullable=False, default=int(Level.BEGINNER))
    status: Mapped[int] = mapped_column(nullable=False, default=int(Status.PLANNED))