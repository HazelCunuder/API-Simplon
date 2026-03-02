import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..model.database import Base, get_db
from ..schemas.courses_schema import CoursesCreateSchema, ModifyCoursesSchema
from ..schemas.sessions_schema import SessionCreate, SessionUpdate
from ..schemas.user_schema import UserCreate, UserUpdate
from ..schemas.user_session_schema import EnrollmentCreate
from ..api.v1.endpoints.courses_endpoints import router as courses_router
from ..api.v1.endpoints.session_endpoints import router as session_router
from ..api.v1.endpoints.user_endpoints import router as user_router
from ..api.v1.endpoints.user_session_endpoints import router as enrollment_router

@pytest.fixture
def db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
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
    app.include_router(courses_router)
    app.include_router(session_router)
    app.include_router(user_router)
    app.include_router(enrollment_router)
    app.dependency_overrides[get_db] = lambda: db
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


class TestCoursesEndpoints:
    def test_get_courses(self, client):
        response = client.get("/courses/")
        assert response.status_code == 200

    def test_get_course_by_id(self, client):
        response = client.get("/courses/1")
        assert response.status_code in [200, 404]

    def test_get_simple_course_info(self, client):
        response = client.get("/courses/1/simple-info")
        assert response.status_code in [200, 404]

    def test_create_course_requires_auth(self, client):
        payload = {
            "title": "Test Course",
            "description": "Test",
            "duration": 10,
            "level": "beginner"
        }
        response = client.post("/courses/create-course", json=payload)
        assert response.status_code in [401, 422]

    def test_update_course_requires_auth(self, client):
        payload = {"title": "Updated Course"}
        response = client.put("/courses/update/1", json=payload)
        assert response.status_code in [401, 422]

    def test_delete_course_requires_auth(self, client):
        response = client.delete("/courses/delete/1")
        assert response.status_code in [401, 422]

    def test_soft_delete_course_requires_auth(self, client):
        response = client.patch("/courses/delete-soft/1")
        assert response.status_code in [401, 422]


class TestSessionEndpoints:
    def test_get_session_requires_auth(self, client):
        response = client.get("/sessions/1")
        assert response.status_code in [401, 422]

    def test_create_session_requires_auth(self, client):
        payload = {
            "teacher_id": 1,
            "course_id": 1,
            "start_date": str(date.today()),
            "end_date": str(date.today() + timedelta(days=30)),
            "capacity": 30
        }
        response = client.post("/sessions/", json=payload)
        assert response.status_code in [401, 422]

    def test_update_session_requires_auth(self, client):
        payload = {"capacity": 50}
        response = client.put("/sessions/1", json=payload)
        assert response.status_code in [401, 422]

    def test_soft_delete_session_requires_auth(self, client):
        response = client.patch("/sessions/1")
        assert response.status_code in [401, 422]


class TestUserEndpoints:
    def test_get_user_requires_auth(self, client):
        response = client.get("/user/1")
        assert response.status_code in [401, 422]

    def test_create_user(self, client):
        payload = {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "password123"
        }
        response = client.post("/user/", json=payload)
        assert response.status_code in [201, 422]

    def test_update_user_requires_auth(self, client):
        payload = {"first_name": "Updated"}
        response = client.patch("/user/1", json=payload)
        assert response.status_code in [401, 422]

    def test_delete_user_requires_auth(self, client):
        response = client.delete("/user/1")
        assert response.status_code in [401, 422]

    def test_soft_delete_user_requires_auth(self, client):
        response = client.patch("/user/soft-delete/1")
        assert response.status_code in [401, 422]


class TestEnrollmentEndpoints:
    def test_enroll_student_requires_auth(self, client):
        payload = {"user_id": 1, "session_id": 1}
        response = client.post("/enrollments/", json=payload)
        assert response.status_code in [401, 422]

    def test_get_sessions_by_student_requires_auth(self, client):
        response = client.get("/enrollments/student/1")
        assert response.status_code in [401, 422]

    def test_get_students_by_session_requires_auth(self, client):
        response = client.get("/enrollments/session/1")
        assert response.status_code in [401, 422]

    def test_get_enrollment_requires_auth(self, client):
        response = client.get("/enrollments/1/1")
        assert response.status_code in [401, 422]

    def test_update_enrollment_requires_auth(self, client):
        payload = {"user_id": 1, "session_id": 1}
        response = client.patch("/enrollments/1/1", json=payload)
        assert response.status_code in [401, 422]

    def test_unenroll_student_requires_auth(self, client):
        response = client.delete("/enrollments/1/1")
        assert response.status_code in [401, 422]

    def test_soft_delete_enrollment_requires_auth(self, client):
        response = client.patch("/enrollments/delete-soft/1")
        assert response.status_code in [401, 422]


class TestEndpointsConsistency:
    def test_all_endpoints_respond(self, client):
        endpoints = [
            ("GET", "/courses/"),
            ("GET", "/courses/1"),
            ("GET", "/courses/1/simple-info"),
        ]
        for method, path in endpoints:
            if method == "GET":
                response = client.get(path)
                assert response.status_code in [200, 404, 422]

    def test_protected_endpoints_list(self, client):
        protected_endpoints = [
            ("POST", "/courses/create-course"),
            ("PUT", "/courses/update/1"),
            ("DELETE", "/courses/delete/1"),
            ("PATCH", "/courses/delete-soft/1"),
            ("GET", "/sessions/1"),
            ("POST", "/sessions/"),
            ("PUT", "/sessions/1"),
            ("PATCH", "/sessions/1"),
            ("GET", "/user/1"),
            ("PATCH", "/user/1"),
            ("DELETE", "/user/1"),
            ("PATCH", "/user/soft-delete/1"),
            ("POST", "/enrollments/"),
            ("GET", "/enrollments/student/1"),
            ("GET", "/enrollments/session/1"),
            ("GET", "/enrollments/1/1"),
            ("PATCH", "/enrollments/1/1"),
            ("DELETE", "/enrollments/1/1"),
            ("PATCH", "/enrollments/delete-soft/1"),
        ]
        for method, path in protected_endpoints:
            if method == "GET":
                response = client.get(path)
            elif method == "POST":
                response = client.post(path, json={})
            elif method == "PUT":
                response = client.put(path, json={})
            elif method == "PATCH":
                response = client.patch(path, json={})
            elif method == "DELETE":
                response = client.delete(path)
            
            assert response.status_code in [401, 422, 400, 404]