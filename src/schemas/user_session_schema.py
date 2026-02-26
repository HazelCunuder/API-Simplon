from pydantic import BaseModel
from datetime import date

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