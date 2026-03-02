from repositories.session_repository import SessionRepository
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from model.database import get_db
from schemas.sessions_schema import SessionCreate, SessionUpdate, SessionRead
from model import Session as SessionModel

class SessionService:
    """
    Service layer for session-related business logic.

    Acts as an intermediary between the API layer and the SessionRepository,
    handling validation and delegating data access to the repository.
    """
    def __init__(self, db: Session = Depends(get_db)):
        """
        Initializes the SessionService with a database session.

        Args:
            db (Session): SQLAlchemy database session provided by FastAPI dependency injection.
        """
        self.repo = SessionRepository(db)

    def get_session(self, session_id: int):
        """
        Retrieves a single session by its ID.

        Queries the database for a session with the given ID and converts
        it to a SessionRead schema for API response.

        Args:
            session_id (int): The unique identifier of the session to retrieve.

        Returns:
            SessionRead: The validated session data.

        Raises:
            HTTPException: With status code 404 if the session is not found.
        """
        session = self.repo.get_by_id(session_id)

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )

        return SessionRead.model_validate(session)

    def create_session(self, session_data: SessionCreate):
        """
        Creates a new session in the database.

        Checks if a session with the same teacher, course, and date range
        already exists. If not, creates and persists the new session with
        the status automatically initialized based on the session dates.

        The status is calculated as follows:
            - 0 (Planned): If start_date is in the future
            - 1 (Ongoing): If the session has started but not ended
            - 2 (Done): If end_date is in the past

        Args:
            session_data (SessionCreate): Validated session creation data including
                teacher_id, course_id, start_date, end_date, capacity, and optional status.

        Returns:
            SessionModel: The created session object with database-generated ID.
        """
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
        """
        Updates an existing session with partial or complete new data.

        Retrieves the session by ID and updates only the fields provided in
        the update payload (exclude_unset=True). If date fields are updated,
        the status may be automatically recalculated based on the new dates.

        Args:
            session_id (int): The unique identifier of the session to update.
            session_data (SessionUpdate): Partial session data with optional fields.
                    Only non-None fields will be updated.

        Returns:
            SessionModel: The updated session object.

        Raises:
            HTTPException: With status code 404 if the session is not found.
        """
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
        """
        Deletes a session from the database.

        Removes the session with the given ID.

        Args:
            session_id (int): The unique identifier of the session to delete.

        Returns:
            bool: True if the deletion was successful.

        Raises:
            HTTPException: With status code 404 if the session is not found.
        """
        db_session = self.repo.db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not db_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )

        self.repo.db.delete(db_session)
        self.repo.db.commit()
        return True
    
    def soft_delete_session(self, session_id: int):
        """
        Soft deletes a session by marking its is_active field as False.

        Args:
            session_id (int): The unique identifier of the session to soft delete.
        Returns:
            bool: True if the soft deletion was successful.
        Raises:
            HTTPException: With status code 404 if the session is not found.
        """        
        db_session = self.repo.db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not db_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )

        db_session.is_active = False
        self.repo.db.commit()
        self.repo.db.refresh(db_session)
        return True