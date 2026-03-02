import pytest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import HTTPException
from model.user import User, Role
from model.database import Base
from schemas.user_schema import UserCreate, UserUpdate, UserRead
from services.user_service import UserService
from repositories.user_repository import UserRepository
from utils.security import hash_password
import os
from dotenv import load_dotenv
from datetime import date

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

class TestUserModel:
    def test_user_creation(self):
        user = User(
            id=1,
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="hashed_password",
            role=Role.STUDENT,
            register_date=date.today()
        )
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john@example.com"
        assert user.role == Role.STUDENT

    def test_user_role_enum(self):
        assert Role.ADMIN == 0
        assert Role.TEACHER == 1
        assert Role.STUDENT == 2


class TestUserRepository:
    def test_get_by_id_found(self, db: Session):
        user = User(
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com",
            password=hash_password("password123"),
            role=Role.TEACHER,
            register_date=date.today()
        )
        db.add(user)
        db.commit()
        
        repo = UserRepository(db)
        found_user = repo.get_by_id(user.id)
        assert found_user is not None
        assert found_user.email == "jane@example.com"

    def test_get_by_id_not_found(self, db: Session):
        repo = UserRepository(db)
        found_user = repo.get_by_id(9999)
        assert found_user is None

    def test_create_user(self, db: Session):
        user_data = UserCreate(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            password="securepass123",
            role=Role.ADMIN,
            register_date=date.today()
        )
        repo = UserRepository(db)
        created_user = repo.create(user_data)
        assert created_user.id is not None
        assert created_user.email == "admin@example.com"

    def test_update_user(self, db: Session):
        user = User(
            first_name="Old",
            last_name="Name",
            email="old@example.com",
            password=hash_password("password"),
            role=Role.STUDENT,
            register_date=date.today()
        )
        db.add(user)
        db.commit()
        
        update_data = UserUpdate(
            first_name="New",
            last_name="Name",
            email="new@example.com",
            password="newpass",
            role=Role.TEACHER,
            register_date=date.today()
        )
        repo = UserRepository(db)
        updated_user = repo.update(user.id, update_data)
        assert updated_user.first_name == "New"

    def test_delete_user(self, db: Session):
        user = User(
            first_name="Delete",
            last_name="Me",
            email="delete@example.com",
            password=hash_password("password"),
            role=Role.STUDENT,
            register_date=date.today()
        )
        db.add(user)
        db.commit()
        
        repo = UserRepository(db)
        result = repo.delete(user.id)
        assert result is True
        assert repo.get_by_id(user.id) is None


class TestUserService:
    def test_get_user_success(self, db: Session):
        user = User(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password=hash_password("password"),
            role=Role.STUDENT,
            register_date=date.today()
        )
        db.add(user)
        db.commit()
        
        service = UserService(db)
        result = service.get_user(user.id)
        assert isinstance(result, UserRead)
        assert result.email == "test@example.com"

    def test_get_user_not_found(self, db: Session):
        service = UserService(db)
        with pytest.raises(HTTPException) as exc_info:
            service.get_user(9999)
        assert exc_info.value.status_code == 404

    def test_create_user_success(self, db: Session):
        user_data = UserCreate(
            first_name="New",
            last_name="User",
            email="newuser@example.com",
            password="password123",
            role=Role.STUDENT,
            register_date=date.today()
        )
        service = UserService(db)
        result = service.create_user(user_data)
        assert result.email == "newuser@example.com"

    def test_create_user_duplicate_email(self, db: Session):
        existing_user = User(
            first_name="Existing",
            last_name="User",
            email="existing@example.com",
            password=hash_password("password"),
            role=Role.STUDENT,
            register_date=date.today()
        )
        db.add(existing_user)
        db.commit()
        
        user_data = UserCreate(
            first_name="New",
            last_name="User",
            email="existing@example.com",
            password="password123",
            role=Role.STUDENT,
            register_date=date.today()
        )
        service = UserService(db)
        with pytest.raises(HTTPException) as exc_info:
            service.create_user(user_data)
        assert exc_info.value.status_code == 409

    def test_update_user(self, db: Session):
        user = User(
            first_name="Original",
            last_name="User",
            email="original@example.com",
            password=hash_password("password"),
            role=Role.STUDENT,
            register_date=date.today()
        )
        db.add(user)
        db.commit()
        
        update_data = UserUpdate(
            first_name="Updated",
            last_name="User",
            email="updated@example.com",
            password="newpass",
            role=Role.TEACHER,
            register_date=date.today()
        )
        service = UserService(db)
        result = service.update_user(user.id, update_data)
        assert result.first_name == "Updated"

    def test_delete_user(self, db: Session):
        user = User(
            first_name="Delete",
            last_name="User",
            email="delete@example.com",
            password=hash_password("password"),
            role=Role.STUDENT,
            register_date=date.today()
        )
        db.add(user)
        db.commit()
        
        service = UserService(db)
        result = service.delete_user(user.id)
        assert result is True

    def test_delete_inactive_users(self, db:Session):
        user = User(
            first_name="Delete",
            last_name="User",
            email="delete@example.com",
            password=hash_password("password"),
            role=Role.STUDENT,
            register_date= date(2020,10,24),
            last_login_date= date(2022, 1, 30)
        )
        db.add(user)
        db.commit()

        service = UserService(db)
        result = service.delete_inactive_user_data()
        assert result is True