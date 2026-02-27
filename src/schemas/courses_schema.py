from pydantic import BaseModel, Field

class CoursesCreateSchema(BaseModel):
    """
    Schema for creating a new course.

    Attributes:
        title (str): The course title. Must be between 0 and 255 characters.
        description (str): A description of the course.
        duration (int): Duration of the course in minutes/hours. Must be greater than 0.
        level (int): Difficulty level of the course. Accepts values 0 through 3.
        status (int): Publication status of the course. Accepts values 0 through 2.
    """
    title: str = Field(min_length=0, max_length=255)
    description: str = Field()
    duration: int = Field(gt=0, allow_inf_nan=False)
    level: int = Field(ge=0, le=3)
    status: int = Field(ge=0, le=2)


class ModifyCoursesSchema(BaseModel):
    """
    Schema for updating an existing course.

    Attributes:
        title (str): The updated course title. Must be between 0 and 255 characters.
        description (str): The updated description of the course.
        duration (int): Updated duration. Must be greater than 0.
        level (int): Updated difficulty level. Accepts values 0 through 3.
        status (int): Updated publication status. Accepts values 0 through 2.
    """
    title: str = Field(min_length=0, max_length=255)
    description: str = Field()
    duration: int = Field(gt=0, allow_inf_nan=False)
    level: int = Field(ge=0, le=3)
    status: int = Field(ge=0, le=2)


class ShowCoursesSchema(BaseModel):
    """
    Schema for displaying full course information in API responses.

    Attributes:
        title (str): The course title.
        description (str): The course description.
        duration (int): The course duration.
        level (int): The difficulty level of the course.
        status (int): The publication status of the course.
    """
    title: str
    description: str
    duration: int
    level: int
    status: int


class ShowSimpleCourseInfoSchema(BaseModel):
    """
    Schema for displaying a simplified view of course information.

    Used in endpoints that return only essential course details.

    Attributes:
        title (str): The course title.
        duration (int): The course duration.
        level (int): The difficulty level of the course.
    """
    title: str
    duration: int
    level: int

    class Config:
        from_attributes = True