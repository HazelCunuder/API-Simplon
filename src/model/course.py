from sqlalchemy import String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from model.database import Base
from enum import Enum

class Level(str, Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    EXPERT = "EXPERT"

class Course(Base):

    __tablename__ = "course_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    duration: Mapped[int] = mapped_column(nullable=False)
    level: Mapped[Level] = mapped_column(SQLEnum(Level, native_enum=True), nullable=False, default=Level.BEGINNER)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)