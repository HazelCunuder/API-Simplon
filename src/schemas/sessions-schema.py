from pydantic import BaseModel, Field, model_validator
from datetime import date
from typing import Optional, Self

class SessionCreate(BaseModel):
    teacher_id: int
    course_id: int
    start_date: date
    end_date: date
    capacity: int = Field(gt=0)

    @model_validator(mode='after')
    def check_dates(self) -> Self:
        if self.end_date <= self.start_date:
            raise ValueError('The end date must be later than the start date')
        return self


class SessionRead(SessionCreate):
    id: int
    teacher_id: int
    course_id: int
    start_date: date
    end_date: date
    capacity: int


class SessionUpdate(BaseModel):
    teacher_id: Optional[int] = None
    course_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    capacity: Optional[int] = Field(default=None, gt=0)