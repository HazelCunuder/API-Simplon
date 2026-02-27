from repositories.session_repository import SessionRepository
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from model.database import get_db
from schemas.sessions_schema import SessionCreate, SessionUpdate, SessionRead
from model import Session as SessionModel

class SessionService:
    def __init__(self, db: Session = Depends(get_db)):
        self.repo = SessionRepository(db)

    def get_session(self, session_id: int):
        session = self.repo.get_by_id(session_id)

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )

        return SessionRead.model_validate(session)

    def create_session(self, session_data: SessionCreate):
        db_session = self.repo.db.query(SessionModel).filter(
            SessionModel.teacher_id == session_data.teacher_id,
            SessionModel.course_id == session_data.course_id,
            SessionModel.start_date == session_data.start_date,
            SessionModel.end_date == session_data.end_date
        ).first()
        
        if not db_session:
            db_session = SessionModel(
                teacher_id=session_data.teacher_id,
                course_id=session_data.course_id,
                start_date=session_data.start_date,
                end_date=session_data.end_date,
                capacity=session_data.capacity,
                status=session_data.status
            )
            self.repo.db.add(db_session)
            self.repo.db.commit()
            self.repo.db.refresh(db_session)
        
        return db_session

    def update_session(self, session_id: int, session_data: SessionUpdate):
        db_session = self.repo.db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not db_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )

        for key, value in session_data.model_dump(exclude_unset=True).items():
            setattr(db_session, key, value)

        self.repo.db.commit()
        self.repo.db.refresh(db_session)
        return db_session

    def delete_session(self, session_id: int):
        db_session = self.repo.db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not db_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )

        self.repo.db.delete(db_session)
        self.repo.db.commit()
        return True