import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from model.course import Course, Level, Status
from model.database import Base
from repositories.course_repository import CourseRepository
from schemas.courses_schema import CoursesCreateSchema, ModifyCoursesSchema
from services.courses_services import CourseService
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
def repository(db_session):
    """Create a CourseRepository instance."""
    return CourseRepository(db=db_session)


@pytest.fixture
def service(repository):
    """Create a CourseService instance."""
    service = CourseService()
    service.repo = repository
    return service


class TestCourseModel:
    def test_course_creation(self, db_session):
        course = Course(title="Python Basics", description="Learn Python", duration=10, level=0, status=0)
        db_session.add(course)
        db_session.commit()
        assert course.id is not None
        assert course.title == "Python Basics"

    def test_course_defaults(self, db_session):
        course = Course(title="Advanced Python", duration=20)
        db_session.add(course)
        db_session.commit()
        assert course.level == int(Level.BEGINNER)
        assert course.status == int(Status.PLANNED)


class TestCourseRepository:
    def test_get_all_courses(self, repository, db_session):
        db_session.add(Course(title="Course 1", duration=10))
        db_session.add(Course(title="Course 2", duration=20))
        db_session.commit()
        courses = repository.get_all_courses()
        assert len(courses) == 2

    def test_get_course_by_id(self, repository, db_session):
        course = Course(title="Test Course", duration=15)
        db_session.add(course)
        db_session.commit()
        found = repository.get_course_by_id(course.id)
        assert found.title == "Test Course"

    def test_get_course_by_id_not_found(self, repository):
        found = repository.get_course_by_id(999)
        assert found is None

    def test_create_course(self, repository):
        schema = CoursesCreateSchema(title="New Course", description="Desc", duration=10, level=1, status=0)
        course = repository.create(schema)
        assert course.id is not None
        assert course.title == "New Course"

    def test_update_course(self, repository, db_session):
        course = Course(title="Old Title", duration=10)
        db_session.add(course)
        db_session.commit()
        update_data = {"title": "New Title", "description": "New Desc", "duration": 20, "level": 2, "status": 1}
        updated = repository.update_course(course.id, update_data)
        assert updated.title == "New Title"
        assert updated.duration == 20

    def test_update_nonexistent_course(self, repository):
        update_data = {"title": "New", "description": "", "duration": 10, "level": 0, "status": 0}
        result = repository.update_course(999, update_data)
        assert result is None

    def test_delete_course(self, repository, db_session):
        course = Course(title="Delete Me", duration=10)
        db_session.add(course)
        db_session.commit()
        result = repository.delete_course(course.id)
        assert result is True
        assert repository.get_course_by_id(course.id) is None

    def test_delete_nonexistent_course(self, repository):
        result = repository.delete_course(999)
        assert result is False

    def test_get_simple_course_info(self, repository, db_session):
        course = Course(title="Simple Course", duration=15, level=2)
        db_session.add(course)
        db_session.commit()
        info = repository.get_simple_course_info(course.id)
        assert info.title == "Simple Course"
        assert info.duration == 15


class TestCourseService:
    def test_get_courses(self, service, db_session):
        db_session.add(Course(title="C1", duration=10))
        db_session.add(Course(title="C2", duration=20))
        db_session.commit()
        courses = service.get_courses()
        assert len(courses) == 2

    def test_get_course(self, service, db_session):
        course = Course(title="Get This", duration=10)
        db_session.add(course)
        db_session.commit()
        found = service.get_course(course.id)
        assert found.title == "Get This"

    def test_get_course_not_found(self, service):
        with pytest.raises(ValueError, match="does not exist"):
            service.get_course(999)

    def test_get_simple_course_info(self, service, db_session):
        course = Course(title="Simple", duration=10, level=1)
        db_session.add(course)
        db_session.commit()
        info = service.get_simple_course_info(course.id)
        assert info.title == "Simple"

    def test_get_simple_course_info_not_found(self, service):
        with pytest.raises(ValueError, match="does not exist"):
            service.get_simple_course_info(999)

    def test_create_course_service(self, service):
        schema = CoursesCreateSchema(title="Service Course", description="Desc", duration=25, level=2, status=1)
        course = service.create(schema)
        assert course.title == "Service Course"

    def test_update_course_valid(self, service, db_session):
        course = Course(title="Old", duration=10)
        db_session.add(course)
        db_session.commit()
        schema = ModifyCoursesSchema(title="New", description="New", duration=20, level=1, status=1)
        updated = service.update_course(course.id, schema)
        assert updated.title == "New"

    def test_update_course_invalid_id(self, service):
        schema = ModifyCoursesSchema(title="New", description="", duration=10, level=0, status=0)
        with pytest.raises(ValueError, match="positive integer"):
            service.update_course(-1, schema)

    def test_update_course_not_found(self, service):
        schema = ModifyCoursesSchema(title="New", description="", duration=10, level=0, status=0)
        with pytest.raises(ValueError, match="does not exist"):
            service.update_course(999, schema)

    def test_delete_course(self, service, db_session):
        course = Course(title="Delete", duration=10)
        db_session.add(course)
        db_session.commit()
        result = service.delete_course(course.id)
        assert result is True

    def test_delete_course_not_found(self, service):
        with pytest.raises(ValueError, match="does not exist"):
            service.delete_course(999)