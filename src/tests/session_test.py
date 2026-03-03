import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.database import Base, get_db
from schemas.sessions_schema import SessionCreate, SessionUpdate, SessionRead
from services.session_services import SessionService
from repositories.session_repository import SessionRepository
from api.v1.endpoints.session_endpoints import router
from fastapi import FastAPI
import os
from dotenv import load_dotenv

@pytest.fixture
def db():
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    engine = create_engine(database_url)
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    yield TestingSessionLocal()


@pytest.fixture
def app(db):
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_db] = lambda: db
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture
def session_repository(db):
    return SessionRepository(db)


@pytest.fixture
def session_service(db):
    return SessionService(db)



def get_valid_start_date():
    return date.today()


def get_valid_end_date():
    return date.today() + timedelta(days=30)


class TestSessionRepository:
    def test_create_session(self, session_repository):
        session_data = SessionCreate(
            course_id=1,
            start_date=get_valid_start_date(),
            end_date=get_valid_end_date(),
            capacity=30
        )
        session = session_repository.create(session_data)
        
        assert session.id is not None
        assert session.course_id == 1
        assert session.capacity == 30

    def test_get_by_id_existing(self, session_repository):
        session_data = SessionCreate(
            course_id=1,
            start_date=get_valid_start_date(),
            end_date=get_valid_end_date(),
            capacity=30
        )
        created_session = session_repository.create(session_data)
        retrieved = session_repository.get_by_id(created_session.id)
        
        assert retrieved is not None
        assert retrieved.id == created_session.id

    def test_get_by_id_nonexistent(self, session_repository):
        result = session_repository.get_by_id(999)
        assert result is None

    def test_update_session(self, session_repository):
        session_data = SessionCreate(
            course_id=1,
            start_date=get_valid_start_date(),
            end_date=get_valid_end_date(),
            capacity=30
        )
        created_session = session_repository.create(session_data)
        
        update_data = SessionUpdate(capacity=50)
        updated = session_repository.update(created_session.id, update_data)
        
        assert updated.capacity == 50

    def test_update_session_nonexistent(self, session_repository):
        update_data = SessionUpdate(capacity=50)
        result = session_repository.update(999, update_data)
        
        assert result is None

    def test_delete_session(self, session_repository):
        session_data = SessionCreate(
            course_id=1,
            start_date=get_valid_start_date(),
            end_date=get_valid_end_date(),
            capacity=30
        )
        created_session = session_repository.create(session_data)
        
        result = session_repository.delete(created_session.id)
        assert result is True
        
        retrieved = session_repository.get_by_id(created_session.id)
        assert retrieved is None

    def test_delete_nonexistent_session(self, session_repository):
        result = session_repository.delete(999)
        assert result is False


class TestSessionService:
    def test_get_session_valid(self, session_service, session_repository):
        session_data = SessionCreate(
            course_id=1,
            start_date=get_valid_start_date(),
            end_date=get_valid_end_date(),
            capacity=30
        )
        created = session_repository.create(session_data)
        
        result = session_service.get_session(created.id)
        assert isinstance(result, SessionRead)
        assert result.id == created.id

    def test_get_session_not_found(self, session_service):
        with pytest.raises(Exception):
            session_service.get_session(999)

    def test_create_session(self, session_service):
        session_data = SessionCreate(
            course_id=1,
            start_date=get_valid_start_date(),
            end_date=get_valid_end_date(),
            capacity=30
        )
        result = session_service.create_session(session_data)
        
        assert result.id is not None

    def test_create_duplicate_session(self, session_service):
        session_data = SessionCreate(
            course_id=1,
            start_date=get_valid_start_date(),
            end_date=get_valid_end_date(),
            capacity=30
        )
        first = session_service.create_session(session_data)
        second = session_service.create_session(session_data)
        
        assert first.id == second.id

    def test_update_session(self, session_service, session_repository):
        session_data = SessionCreate(
            course_id=1,
            start_date=get_valid_start_date(),
            end_date=get_valid_end_date(),
            capacity=30
        )
        created = session_repository.create(session_data)
        
        update_data = SessionUpdate(capacity=50)
        result = session_service.update_session(created.id, update_data)
        
        assert result.capacity == 50

    def test_update_session_not_found(self, session_service):
        update_data = SessionUpdate(capacity=50)
        with pytest.raises(Exception):
            session_service.update_session(999, update_data)

    def test_delete_session(self, session_service, session_repository):
        session_data = SessionCreate(
            course_id=1,
            start_date=get_valid_start_date(),
            end_date=get_valid_end_date(),
            capacity=30
        )
        created = session_repository.create(session_data)
        
        result = session_service.delete_session(created.id)
        assert result is True

    def test_delete_session_not_found(self, session_service):
        with pytest.raises(Exception):
            session_service.delete_session(999)


class TestSessionSchemas:
    def test_session_create_valid(self):
        data = SessionCreate(
            course_id=1,
            start_date=get_valid_start_date(),
            end_date=get_valid_end_date(),
            capacity=30
        )
        assert data.capacity == 30

    def test_session_create_invalid_capacity(self):
        with pytest.raises(Exception):
            SessionCreate(
                course_id=1,
                start_date=get_valid_start_date(),
                end_date=get_valid_end_date(),
                capacity=0
            )

    def test_session_create_invalid_dates(self):
        with pytest.raises(Exception):
            SessionCreate(
                course_id=1,
                start_date=get_valid_end_date(),
                end_date=get_valid_start_date(),
                capacity=30
            )

    def test_session_create_same_dates(self):
        with pytest.raises(Exception):
            SessionCreate(
                course_id=1,
                start_date=get_valid_start_date(),
                end_date=get_valid_start_date(),
                capacity=30
            )

    def test_session_update_partial(self):
        data = SessionUpdate(capacity=50)
        assert data.capacity == 50


class TestSessionEndpoints:
    def test_get_session_endpoint(self, client, session_repository):
        session_data = SessionCreate(
            course_id=1,
            start_date=get_valid_start_date(),
            end_date=get_valid_end_date(),
            capacity=30
        )
        created = session_repository.create(session_data)
        
        response = client.get(f"/sessions/{created.id}")
        assert response.status_code == 200

    def test_create_session_endpoint(self, client):
        payload = {
            "course_id": 1,
            "start_date": str(get_valid_start_date()),
            "end_date": str(get_valid_end_date()),
            "capacity": 30
        }
        response = client.post("/sessions/", json=payload)
        assert response.status_code == 201

    def test_update_session_endpoint(self, client, session_repository):
        session_data = SessionCreate(
            course_id=1,
            start_date=get_valid_start_date(),
            end_date=get_valid_end_date(),
            capacity=30
        )
        created = session_repository.create(session_data)
        
        payload = {"capacity": 50}
        response = client.put(f"/sessions/{created.id}", json=payload)
        assert response.status_code == 200
        assert response.json()["capacity"] == 50

    def test_get_nonexistent_endpoint(self, client):
        response = client.get("/sessions/999")
        assert response.status_code == 404

    def test_update_nonexistent_endpoint(self, client):
        response = client.put("/sessions/999", json={"capacity": 50})
        assert response.status_code == 404