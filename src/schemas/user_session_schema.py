from pydantic import BaseModel
from datetime import date
from model.user import Role


class UserDetail(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    role: Role

    class Config:
        from_attributes = True


class SessionDetail(BaseModel):
    id: int
    teacher_id: int
    course_id: int
    start_date: date
    end_date: date
    capacity: int

    class Config:
        from_attributes = True


class EnrollmentCreate(BaseModel):
    user_id: int
    session_id: int


class EnrollmentResponse(BaseModel):
    id: int
    user_id: int
    session_id: int
    enrollment_date: date

    class Config:
        from_attributes = True


class EnrollmentDetail(BaseModel):
    id: int
    enrollment_date: date
    user: UserDetail

    class Config:
        from_attributes = True


class StudentsBySessionResponse(BaseModel):
    session_id: int
    teacher_id: int
    students: list[EnrollmentDetail]

    class Config:
        from_attributes = True


class SessionsByStudentResponse(BaseModel):
    user_id: int
    sessions: list[EnrollmentDetail]

    class Config:
        from_attributes = True