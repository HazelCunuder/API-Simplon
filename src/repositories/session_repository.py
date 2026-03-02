from sqlalchemy.orm import Session
from model import Session as SessionModel
from schemas.sessions_schema import SessionCreate, SessionUpdate

class SessionRepository:
    """
    Data access layer for session-related database operations.

    Attributes:
        db (Session): SQLAlchemy ORM session for database operations.
    """

    def __init__(self, db: Session):
        """
        Initializes the SessionRepository with a database session.

        Args:
            db (Session): SQLAlchemy database session instance.
        """
        self.db = db

    def get_by_id(self, session_id: int):
        """
        Retrieves a single session by its unique identifier.

        Performs a database query to find the session with the specified ID.

        Args:
            session_id (int): The unique identifier of the session to retrieve.

        Returns:
            SessionModel | None: The session object if found, None otherwise.
        """
        return self.db.query(SessionModel).filter(SessionModel.id == session_id).first()

    def create(self, session_data: SessionCreate) -> SessionModel:
        """
        Creates a new session in the database.

        Args:
            session_data (SessionCreate): Validated session creation data.

        Returns:
            SessionModel: The newly created session object with database-generated ID.
        """
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
        """
        Updates an existing session with partial or complete new data.

        Args:
            session_id (int): The unique identifier of the session to update.
            session_data (SessionUpdate): Partial session data with optional fields.

        Returns:
            SessionModel | None: The updated session object if found and updated successfully,
                None if no session with the given ID exists.
        """
        db_session = self.db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not db_session:
            return None

        for key, value in session_data.model_dump(exclude_unset=True).items():
            setattr(db_session, key, value)

        self.db.commit()
        self.db.refresh(db_session)
        return db_session

    def delete(self, session_id: int) -> bool:
        """
        Deletes a session from the database.

        Removes the session with the specified ID.

        Args:
            session_id (int): The unique identifier of the session to delete.

        Returns:
            bool: True if the deletion was successful, False if the session
                was not found or could not be deleted.
        """
        db_session = self.db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not db_session:
            return False

        self.db.delete(db_session)
        self.db.commit()
        return True
    
    def soft_delete(self, session_id: int) -> bool:
        """
        Soft deletes a session by marking its status as 'cancelled'.

        Args:
            session_id (int): The unique identifier of the session to soft delete.
        Returns:
            bool: True if the soft deletion was successful, False if the session
                  was not found or could not be updated.
        """        
        db_session = self.db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not db_session:
            return False

        db_session.is_active = False
        self.db.commit()
        self.db.refresh(db_session)
        return True