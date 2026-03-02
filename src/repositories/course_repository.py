from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from model.database import get_db

from model.course import Course
from schemas.courses_schema import CoursesCreateSchema, ModifyCoursesSchema, ShowCoursesSchema, ShowSimpleCourseInfoSchema

class CourseRepository:
    """
    Repository layer for course data access.

    Handles all direct interactions with the database for Course entities,
    providing CRUD operations via SQLAlchemy.
    """

    def __init__(self, db: Session = Depends(get_db)):
        """
        Initialize the CourseRepository with a database session.

        Args:
            db (Session): The SQLAlchemy database session. Injected via FastAPI's
                          dependency system using get_db.
        """
        self.db = db

    def get_all_courses(self) -> List[Course]:
        """
        Retrieve all courses from the database.

        Returns:
            List[Course]: A list of all Course records in the database.
        """
        return self.db.query(Course).all()

    def get_course_by_id(self, course_id: int) -> Optional[Course]:
        """
        Retrieve a single course by its ID.

        Args:
            course_id (int): The ID of the course to look up.

        Returns:
            Optional[Course]: The matching Course record, or None if not found.
        """
        return self.db.query(Course).filter(Course.id == course_id).first()

    def get_simple_course_info(self, course_id: int) -> Optional[Course]:
        """
        Retrieve a course by its ID for simplified info display.

        Args:
            course_id (int): The ID of the course to look up.

        Returns:
            Optional[Course]: The matching Course record, or None if not found.
        """
        return self.db.query(Course).filter(Course.id == course_id).first()

    def create(self, course_data: CoursesCreateSchema) -> Course:
        """
        Create and persist a new course in the database.

        Args:
            course_data (CoursesCreateSchema): The validated schema containing
                                               the data for the new course.

        Returns:
            Course: The newly created and refreshed Course record.
        """
        new_course = Course(**course_data.model_dump())
        self.db.add(new_course)
        self.db.commit()
        self.db.refresh(new_course)
        return new_course

    def update_course(self, course_id: int, course_data: ModifyCoursesSchema) -> Optional[Course]:
        """
        Update an existing course's fields by its ID.

        Args:
            course_id (int): The ID of the course to update.
            course_data (ModifyCoursesSchema): A schema or dict containing the
                                               updated field values.

        Returns:
            Optional[Course]: The updated and refreshed Course record, or None
                              if no course with the given ID was found.
        """
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
        """
        Delete a course from the database by its ID.

        Args:
            course_id (int): The ID of the course to delete.

        Returns:
            bool: True if the course was found and deleted, False otherwise.
        """
        course = self.get_course_by_id(course_id)
        if not course:
            return False
        self.db.delete(course)
        self.db.commit()
        return True
    
    def soft_delete(self, course_id: int) -> bool:
        """
        Soft delete a course by setting its 'is_active' flag to True.

        Args:
            course_id (int): The ID of the course to soft delete.

        Returns:
            bool: True if the course was found and soft deleted, False otherwise.
        """
        course = self.get_course_by_id(course_id)
        if not course:
            return False
        course.is_active = False
        self.db.commit()
        self.db.refresh(course)
        return True