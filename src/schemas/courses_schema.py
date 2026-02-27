from pydantic import BaseModel, Field

class CoursesCreateSchema(BaseModel):
    title : str = Field(min_length=0, max_length=255)
    description : str = Field()
    duration : int = Field(gt = 0, allow_inf_nan=False)
    level : int = Field(ge=0, le= 3)

class ModifyCoursesSchema(BaseModel):
    title : str = Field(min_length=0, max_length=255)
    description : str = Field()
    duration : int = Field(gt = 0, allow_inf_nan=False)
    level : int = Field(ge=0, le= 3)

class ShowCoursesSchema(BaseModel):
    title : str
    description : str
    duration : int
    level : int
    status : int

class ShowSimpleCourseInfoSchema(BaseModel):
    title: str
    duration: int
    level: int

    class Config:
        from_attributes = True

