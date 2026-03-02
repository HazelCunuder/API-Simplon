from sqlalchemy.orm import Session as DBSession
from sqlalchemy import select
from datetime import date
from model.user_session import UserSession
from model.user import User, Role

class UserSessionRepository:
    def __init__(self, db: DBSession):
        self.db = db

    def enroll(self, user_id: int, session_id: int) -> UserSession:
        user = self.db.get(User, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        if user.role != Role.STUDENT:
            raise ValueError(f"User {user_id} is not a student")

        existing = self.get_by_user_and_session(user_id, session_id)
        if existing:
            raise ValueError(f"User {user_id} is already enrolled in session {session_id}")

        enrollment = UserSession(
            user_id=user_id,
            session_id=session_id,
            enrollment_date=date.today()
        )
        self.db.add(enrollment)
        self.db.commit()
        self.db.refresh(enrollment)
        return enrollment

    def unenroll(self, user_id: int, session_id: int) -> None:
        enrollment = self.get_by_user_and_session(user_id, session_id)
        if not enrollment:
            raise ValueError(f"Enrollment not found")
        self.db.delete(enrollment)
        self.db.commit()

    def get_by_id(self, enrollment_id: int) -> UserSession | None:
        return self.db.get(UserSession, enrollment_id)

    def get_by_user_and_session(self, user_id: int, session_id: int) -> UserSession | None:
        return self.db.scalar(
            select(UserSession).where(
                UserSession.user_id == user_id,
                UserSession.session_id == session_id
            )
        )

    def get_students_by_session(self, session_id: int) -> list[UserSession]:
        return list(self.db.scalars(
            select(UserSession).where(UserSession.session_id == session_id)
        ))

    def get_sessions_by_student(self, user_id: int) -> list[UserSession]:
        return list(self.db.scalars(
            select(UserSession).where(UserSession.user_id == user_id)
        ))

    def get_all(self) -> list[UserSession]:
        return list(self.db.scalars(select(UserSession)))
    
    def soft_delete(self, enrollment_id: int) -> None:
        enrollment = self.get_by_id(enrollment_id)
        if not enrollment:
            raise ValueError(f"Enrollment {enrollment_id} not found")
        enrollment.is_active = False
        self.db.commit()