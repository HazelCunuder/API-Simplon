from sqlalchemy.orm import Session
from model import Session as SessionModel
from schemas.sessions_schema import SessionCreate, SessionUpdate

class SessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, session_id: int):
        return self.db.query(SessionModel).filter(SessionModel.id == session_id).first()

    def create(self, session_data: SessionCreate) -> SessionModel:
        db_session = SessionModel(
            teacher_id=session_data.teacher_id,
            course_id=session_data.course_id,
            start_date=session_data.start_date,
            end_date=session_data.end_date,
            capacity=session_data.capacity,
        )
        self.db.add(db_session)
        self.db.commit()
        self.db.refresh(db_session)
        return db_session

    def update(self, session_id: int, session_data: SessionUpdate) -> SessionModel | None:
        db_session = self.db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not db_session:
            return None

        for key, value in session_data.model_dump(exclude_unset=True).items():
            setattr(db_session, key, value)

        self.db.commit()
        self.db.refresh(db_session)
        return db_session

    def delete(self, session_id: int) -> bool:
        db_session = self.db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not db_session:
            return False

        self.db.delete(db_session)
        self.db.commit()
        return True