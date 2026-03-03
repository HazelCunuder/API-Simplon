from pydantic import BaseModel
from datetime import date
from model.user import Role

class UserDetail(BaseModel):
    id: int
    first_name: str
    last_name: str
    role: Role

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
