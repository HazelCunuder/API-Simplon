from sqlalchemy.orm import Session as DBSession
from model.user_session import UserSession
from model.user import User, Role
from model.session import Session
from repositories.user_session_repo import UserSessionRepository
from repositories.user_repository import UserRepository
from repositories.session_repository import SessionRepository

class UserSessionService:
    def __init__(self, db: DBSession):
        self.user_session_repo = UserSessionRepository(db)
        self.user_repo = UserRepository(db)
        self.session_repo = SessionRepository(db)

    def enroll_student(self, user_id: int, session_id: int) -> UserSession:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        if user.role != Role.STUDENT:
            raise ValueError(f"User {user_id} is not a student")

        session = self.session_repo.get_by_id(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        enrollments = self.user_session_repo.get_students_by_session(session_id)
        if len(enrollments) >= session.capacity:
            raise ValueError(f"Session {session_id} is full")

        from datetime import date
        if session.start_date <= date.today():
            raise ValueError(f"Session {session_id} has already started")

        return self.user_session_repo.enroll(user_id, session_id)

    def unenroll_student(self, user_id: int, session_id: int) -> None:
        enrollment = self.user_session_repo.get_by_user_and_session(user_id, session_id)
        if not enrollment:
            raise ValueError(f"User {user_id} is not enrolled in session {session_id}")

        from datetime import date
        session = self.session_repo.get_by_id(session_id)
        if session.start_date <= date.today():
            raise ValueError(f"Cannot unenroll from a session that has already started")

        self.user_session_repo.unenroll(user_id, session_id)

    def get_sessions_by_student(self, user_id: int) -> list[UserSession]:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        return self.user_session_repo.get_sessions_by_student(user_id)

    def get_students_by_session(self, session_id: int) -> list[UserSession]:
        session = self.session_repo.get_by_id(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        return self.user_session_repo.get_students_by_session(session_id)

    def get_enrollment(self, user_id: int, session_id: int) -> UserSession:
        enrollment = self.user_session_repo.get_by_user_and_session(user_id, session_id)
        if not enrollment:
            raise ValueError(f"Enrollment not found")
        return enrollment