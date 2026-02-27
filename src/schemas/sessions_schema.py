from pydantic import BaseModel, Field, model_validator
from datetime import date
from typing import Optional, Self

class SessionCreate(BaseModel):
    teacher_id: int
    course_id: int
    start_date: date
    end_date: date
    capacity: int = Field(gt=0)
    status: Optional[int] = Field(default=None, ge=0, le=2)

    @model_validator(mode='after')
    def check_dates(self) -> Self:
        if self.end_date <= self.start_date:
            raise ValueError('The end date must be later than the start date')
        return self

    @model_validator(mode='after')
    def set_status(self) -> Self:
        today = date.today()

        if self.status is None:
            if self.end_date < today:
                print("2 - Done")
                self.status = 2  # Done
            elif self.start_date > today:
                print("0 - Planned")
                self.status = 0  # Planned
            else:
                print("0 - Ongoing")
                self.status = 1  # Ongoing

        return self

class SessionRead(SessionCreate):
    id: int
    teacher_id: int
    course_id: int
    start_date: date
    end_date: date
    capacity: int
    status: int

class SessionUpdate(BaseModel):
    teacher_id: Optional[int] = None
    course_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    capacity: Optional[int] = Field(default=None, gt=0)
    status: int = Field(ge=0, le=2)