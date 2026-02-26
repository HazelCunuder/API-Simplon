from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship, mapped_column
from datetime import date
from model.database import Base

class UserSession(Base):
    __tablename__ = 'user_session_table'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_table.id'))
    session_id: Mapped[int] = mapped_column(ForeignKey('session_table.id'))
    enrollment_date: Mapped[date] = mapped_column()
    
    user: Mapped["User"] = relationship(back_populates="enrollments")
    session: Mapped["Session"] = relationship(back_populates="enrollments")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'session_id', name='uq_user_session'),
    )