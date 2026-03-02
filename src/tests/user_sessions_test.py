import pytest
from unittest.mock import MagicMock, patch
from datetime import date, timedelta
from model.user import User, Role
from model.session import Session
from model.user_session import UserSession
from services.user_session_services import UserSessionService

# --- Fixtures ---

@pytest.fixture
def mock_user_repo():
    return MagicMock()

@pytest.fixture
def mock_session_repo():
    return MagicMock()

@pytest.fixture
def mock_user_session_repo():
    return MagicMock()

@pytest.fixture
def service(mock_user_repo, mock_session_repo, mock_user_session_repo):
    with patch('services.user_session_services.UserRepository', return_value=mock_user_repo), \
         patch('services.user_session_services.SessionRepository', return_value=mock_session_repo), \
         patch('services.user_session_services.UserSessionRepository', return_value=mock_user_session_repo):
        svc = UserSessionService(MagicMock())
        svc.user_repo = mock_user_repo
        svc.session_repo = mock_session_repo
        svc.user_session_repo = mock_user_session_repo
        return svc


# --- Helpers ---

def make_user(id=1, role=Role.STUDENT):
    user = MagicMock(spec=User)
    user.id = id
    user.role = role
    user.first_name = "John"
    user.last_name = "Doe"
    user.email = f"user{id}@test.com"
    return user

def make_session(id=1, capacity=10, start_date=None, end_date=None):
    session = MagicMock(spec=Session)
    session.id = id
    session.capacity = capacity
    session.start_date = start_date or date.today() + timedelta(days=7)
    session.end_date = end_date or date.today() + timedelta(days=30)
    return session

def make_enrollment(user_id=1, session_id=1):
    enrollment = MagicMock(spec=UserSession)
    enrollment.id = 1
    enrollment.user_id = user_id
    enrollment.session_id = session_id
    enrollment.enrollment_date = date.today()
    return enrollment


# --- Enroll Student ---

class TestEnrollStudent:

    def test_enroll_success(self, service, mock_user_repo, mock_session_repo, mock_user_session_repo):
        mock_user_repo.get_by_id.return_value = make_user()
        mock_session_repo.get_by_id.return_value = make_session()
        mock_user_session_repo.get_students_by_session.return_value = []
        mock_user_session_repo.enroll.return_value = make_enrollment()

        result = service.enroll_student(1, 1)
        assert result.user_id == 1
        assert result.session_id == 1

    def test_enroll_user_not_found(self, service, mock_user_repo):
        mock_user_repo.get_by_id.return_value = None

        with pytest.raises(ValueError, match="not found"):
            service.enroll_student(999, 1)

    def test_enroll_session_not_found(self, service, mock_user_repo, mock_session_repo):
        mock_user_repo.get_by_id.return_value = make_user()
        mock_session_repo.get_by_id.return_value = None

        with pytest.raises(ValueError, match="not found"):
            service.enroll_student(1, 999)

    def test_enroll_user_is_teacher(self, service, mock_user_repo):
        mock_user_repo.get_by_id.return_value = make_user(role=Role.TEACHER)

        with pytest.raises(ValueError, match="not a student"):
            service.enroll_student(1, 1)

    def test_enroll_user_is_admin(self, service, mock_user_repo):
        mock_user_repo.get_by_id.return_value = make_user(role=Role.ADMIN)

        with pytest.raises(ValueError, match="not a student"):
            service.enroll_student(1, 1)

    def test_enroll_session_full(self, service, mock_user_repo, mock_session_repo, mock_user_session_repo):
        mock_user_repo.get_by_id.return_value = make_user()
        mock_session_repo.get_by_id.return_value = make_session(capacity=2)
        mock_user_session_repo.get_students_by_session.return_value = [
            make_enrollment(user_id=2),
            make_enrollment(user_id=3),
        ]

        with pytest.raises(ValueError, match="full"):
            service.enroll_student(1, 1)

    def test_enroll_session_at_exactly_capacity(self, service, mock_user_repo, mock_session_repo, mock_user_session_repo):
        mock_user_repo.get_by_id.return_value = make_user()
        mock_session_repo.get_by_id.return_value = make_session(capacity=1)
        mock_user_session_repo.get_students_by_session.return_value = [
            make_enrollment(user_id=2)
        ]

        with pytest.raises(ValueError, match="full"):
            service.enroll_student(1, 1)

    def test_enroll_session_already_started(self, service, mock_user_repo, mock_session_repo, mock_user_session_repo):
        mock_user_repo.get_by_id.return_value = make_user()
        mock_session_repo.get_by_id.return_value = make_session(
            start_date=date.today() - timedelta(days=1)
        )
        mock_user_session_repo.get_students_by_session.return_value = []

        with pytest.raises(ValueError, match="already started"):
            service.enroll_student(1, 1)

    def test_enroll_session_starts_today(self, service, mock_user_repo, mock_session_repo, mock_user_session_repo):
        mock_user_repo.get_by_id.return_value = make_user()
        mock_session_repo.get_by_id.return_value = make_session(
            start_date=date.today()
        )
        mock_user_session_repo.get_students_by_session.return_value = []

        with pytest.raises(ValueError, match="already started"):
            service.enroll_student(1, 1)

    def test_enroll_duplicate(self, service, mock_user_repo, mock_session_repo, mock_user_session_repo):
        mock_user_repo.get_by_id.return_value = make_user()
        mock_session_repo.get_by_id.return_value = make_session()
        mock_user_session_repo.get_students_by_session.return_value = []
        mock_user_session_repo.enroll.side_effect = ValueError("already enrolled")

        with pytest.raises(ValueError, match="already enrolled"):
            service.enroll_student(1, 1)

    def test_enroll_teacher_in_their_own_session(self, service, mock_user_repo):
        mock_user_repo.get_by_id.return_value = make_user(id=99, role=Role.TEACHER)

        with pytest.raises(ValueError, match="not a student"):
            service.enroll_student(99, 1)


# --- Unenroll Student ---

class TestUnenrollStudent:

    def test_unenroll_success(self, service, mock_user_session_repo, mock_session_repo):
        mock_user_session_repo.get_by_user_and_session.return_value = make_enrollment()
        mock_session_repo.get_by_id.return_value = make_session()

        service.unenroll_student(1, 1)
        mock_user_session_repo.unenroll.assert_called_once_with(1, 1)

    def test_unenroll_not_enrolled(self, service, mock_user_session_repo):
        mock_user_session_repo.get_by_user_and_session.return_value = None

        with pytest.raises(ValueError, match="not enrolled"):
            service.unenroll_student(1, 1)

    def test_unenroll_session_already_started(self, service, mock_user_session_repo, mock_session_repo):
        mock_user_session_repo.get_by_user_and_session.return_value = make_enrollment()
        mock_session_repo.get_by_id.return_value = make_session(
            start_date=date.today() - timedelta(days=1)
        )

        with pytest.raises(ValueError, match="already started"):
            service.unenroll_student(1, 1)

    def test_unenroll_session_starts_today(self, service, mock_user_session_repo, mock_session_repo):
        mock_user_session_repo.get_by_user_and_session.return_value = make_enrollment()
        mock_session_repo.get_by_id.return_value = make_session(
            start_date=date.today()
        )

        with pytest.raises(ValueError, match="already started"):
            service.unenroll_student(1, 1)


# --- Get Sessions By Student ---

class TestGetSessionsByStudent:

    def test_get_sessions_success(self, service, mock_user_repo, mock_user_session_repo):
        mock_user_repo.get_by_id.return_value = make_user()
        mock_user_session_repo.get_sessions_by_student.return_value = [
            make_enrollment(session_id=1),
            make_enrollment(session_id=2),
        ]

        result = service.get_sessions_by_student(1)
        assert len(result) == 2

    def test_get_sessions_user_not_found(self, service, mock_user_repo):
        mock_user_repo.get_by_id.return_value = None

        with pytest.raises(ValueError, match="not found"):
            service.get_sessions_by_student(999)

    def test_get_sessions_empty(self, service, mock_user_repo, mock_user_session_repo):
        mock_user_repo.get_by_id.return_value = make_user()
        mock_user_session_repo.get_sessions_by_student.return_value = []

        result = service.get_sessions_by_student(1)
        assert result == []

    def test_get_sessions_student_enrolled_in_many(self, service, mock_user_repo, mock_user_session_repo):
        mock_user_repo.get_by_id.return_value = make_user()
        mock_user_session_repo.get_sessions_by_student.return_value = [
            make_enrollment(session_id=i) for i in range(20)
        ]

        result = service.get_sessions_by_student(1)
        assert len(result) == 20


# --- Get Students By Session ---

class TestGetStudentsBySession:

    def test_get_students_success(self, service, mock_session_repo, mock_user_session_repo):
        mock_session_repo.get_by_id.return_value = make_session()
        mock_user_session_repo.get_students_by_session.return_value = [
            make_enrollment(user_id=1),
            make_enrollment(user_id=2),
        ]

        result = service.get_students_by_session(1)
        assert len(result) == 2

    def test_get_students_session_not_found(self, service, mock_session_repo):
        mock_session_repo.get_by_id.return_value = None

        with pytest.raises(ValueError, match="not found"):
            service.get_students_by_session(999)

    def test_get_students_empty_session(self, service, mock_session_repo, mock_user_session_repo):
        mock_session_repo.get_by_id.return_value = make_session()
        mock_user_session_repo.get_students_by_session.return_value = []

        result = service.get_students_by_session(1)
        assert result == []

    def test_get_students_full_session(self, service, mock_session_repo, mock_user_session_repo):
        mock_session_repo.get_by_id.return_value = make_session(capacity=5)
        mock_user_session_repo.get_students_by_session.return_value = [
            make_enrollment(user_id=i) for i in range(5)
        ]

        result = service.get_students_by_session(1)
        assert len(result) == 5


# --- Get Enrollment ---

class TestGetEnrollment:

    def test_get_enrollment_success(self, service, mock_user_session_repo):
        mock_user_session_repo.get_by_user_and_session.return_value = make_enrollment()

        result = service.get_enrollment(1, 1)
        assert result.user_id == 1
        assert result.session_id == 1

    def test_get_enrollment_not_found(self, service, mock_user_session_repo):
        mock_user_session_repo.get_by_user_and_session.return_value = None

        with pytest.raises(ValueError, match="not found"):
            service.get_enrollment(1, 1)

    def test_get_enrollment_wrong_user(self, service, mock_user_session_repo):
        mock_user_session_repo.get_by_user_and_session.return_value = None

        with pytest.raises(ValueError, match="not found"):
            service.get_enrollment(999, 1)

    def test_get_enrollment_wrong_session(self, service, mock_user_session_repo):
        mock_user_session_repo.get_by_user_and_session.return_value = None

        with pytest.raises(ValueError, match="not found"):
            service.get_enrollment(1, 999)

    def test_get_enrollment_both_wrong(self, service, mock_user_session_repo):
        mock_user_session_repo.get_by_user_and_session.return_value = None

        with pytest.raises(ValueError, match="not found"):
            service.get_enrollment(999, 999)