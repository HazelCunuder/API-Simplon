from repositories.course_repository import CourseRepository
from fastapi import Depends
from sqlalchemy.orm import Session
from model.database import Base
from schemas.courses_schema import CoursesCreateSchema, ModifyCoursesSchema, ShowCoursesSchema, ShowSimpleCourseInfoSchema

class CourseService:
    def __init__(self, repo = CourseRepository):
        self.repo = repo

    def get_courses(self):
        return self.repo.get_all_courses()

    def get_course(self, course_id: int):
        if self.repo.get_course_by_id(course_id) is None:
            raise ValueError(f"Course with ID {course_id} does not exist.")
        return self.repo.get_course_by_id(course_id)

    def get_simple_course_info(self, course_id: int):
        if self.repo.get_course_by_id(course_id) is None:
            raise ValueError(f"Course with ID {course_id} does not exist.")
        return self.repo.get_simple_course_info(course_id)

    def create(self, course: CoursesCreateSchema):
        return self.repo.create(course)

    def update_course(self, course_id: int, course: ModifyCoursesSchema):
        if course_id <= 0:
            raise ValueError("Course ID must be a positive integer.")
        if self.repo.get_course_by_id(course_id) is None:
            raise ValueError(f"Course with ID {course_id} does not exist.")
        return self.repo.update_course(course_id, course.model_dump())

    def delete_course(self, course_id: int):
        if self.repo.get_course_by_id(course_id) is None:
            raise ValueError(f"Course with ID {course_id} does not exist.")
        return self.repo.delete_course(course_id)