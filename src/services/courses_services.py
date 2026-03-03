from repositories.course_repository import CourseRepository
from schemas.courses_schema import CoursesCreateSchema, ModifyCoursesSchema, ShowCoursesSchema, ShowSimpleCourseInfoSchema

class CourseService:
    """
    Service layer for course-related business logic.

    Acts as an intermediary between the API layer and the CourseRepository,
    handling validation and delegating data access to the repository.
    """

    def __init__(self, repo = CourseRepository):
        """
        Initialize the CourseService with a repository.

        Args:
            repo: The repository class or instance used for course data access.
                  Defaults to CourseRepository.
        """
        self.repo = repo

    def get_courses(self):
        """
        Retrieve all courses.

        Returns:
            A list of all course records.
        """
        return self.repo.get_all_courses()

    def get_course(self, course_id: int):
        """
        Retrieve a single course by its ID.

        Args:
            course_id (int): The ID of the course to retrieve.

        Returns:
            The course record matching the given ID.

        Raises:
            ValueError: If no course with the given ID exists.
        """
        if self.repo.get_course_by_id(course_id) is None:
            raise ValueError(f"Course with ID {course_id} does not exist.")
        return self.repo.get_course_by_id(course_id)

    def create(self, course: CoursesCreateSchema):
        """
        Create a new course.

        Args:
            course (CoursesCreateSchema): The schema containing the data for the new course.

        Returns:
            The newly created course record.
        """
        return self.repo.create(course)

    def update_course(self, course_id: int, course: ModifyCoursesSchema):
        """
        Update an existing course by its ID.

        Args:
            course_id (int): The ID of the course to update. Must be a positive integer.
            course (ModifyCoursesSchema): The schema containing the updated course data.

        Returns:
            The updated course record.

        Raises:
            ValueError: If course_id is not a positive integer, or if no course
                        with the given ID exists.
        """
        if course_id <= 0:
            raise ValueError("Course ID must be a positive integer.")
        if self.repo.get_course_by_id(course_id) is None:
            raise ValueError(f"Course with ID {course_id} does not exist.")
        return self.repo.update_course(course_id, course.model_dump())

    def delete_course(
        self,
        course_id: int,
        soft_delete: bool,
    ):
        """
        Delete a course by its ID.

        Args:
            course_id (int): The ID of the course to delete.
            soft_delete (bool): If True, mark as inactive. If False, permanently delete.
        Returns:
            The result of the deletion operation from the repository.

        Raises:
            ValueError: If no course with the given ID exists.
        """
        if not self.repo.get_course_by_id(course_id):
            raise ValueError(f"Course with ID {course_id} does not exist.")

        if soft_delete:
            return self.repo.soft_delete(course_id)
        else:
            return self.repo.delete_course(course_id)