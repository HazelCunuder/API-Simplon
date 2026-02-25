from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from configs.database import (
    get_db_connection,
)

from model.course import Course
from schemas.courses_schema import CoursesCreateSchema, ModifyCoursesSchema, ShowCoursesSchema, ShowSimpleCourseInfoSchema

class CourseRepository:
    def __init__(self, db: Session = Depends(get_db_connection)):
        self.db = db

    def get_all_courses(self) -> List[Course]:
        return self.db.query(Course).all()

    def get_course_by_id(self, course_id: int) -> Optional[Course]:
        return self.db.query(Course).filter(Course.id == course_id).first()
    
    def get_simple_course_info(self, course_id: int) -> Optional[Course]:
        return self.db.query(Course).filter(Course.id == course_id).first()

    def create(self, course_data: CoursesCreateSchema) -> Course:
        new_course = Course(**course_data.model_dump())
        self.db.add(new_course)
        self.db.commit()
        self.db.refresh(new_course)
        return new_course

    def update_course(self, course_id: int, course_data: ModifyCoursesSchema) -> Optional[Course]:
        course = self.get_course_by_id(course_id)
        if not course:
            return None
        data = course_data if isinstance(course_data) else course_data.model_dump()
        for key, value in data.items():
            setattr(course, key, value)
        self.db.commit()
        self.db.refresh(course)
        return course

    def delete_course(self, course_id: int) -> bool:
        course = self.get_course_by_id(course_id)
        if not course:
            return False
        self.db.delete(course)
        self.db.commit()
        return True