from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from model.database import Base

class Course(Base):

    __tablename__ = "course_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    duration: Mapped[int] = mapped_column(nullable=False)
    level: Mapped[str] = mapped_column()