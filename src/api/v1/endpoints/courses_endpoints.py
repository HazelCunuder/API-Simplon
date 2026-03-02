from fastapi import APIRouter, Depends
from services.courses_services import CourseService
from repositories.course_repository import CourseRepository
from schemas.courses_schema import CoursesCreateSchema, ModifyCoursesSchema, ShowCoursesSchema, ShowSimpleCourseInfoSchema
from model.database import get_db
from sqlalchemy.orm import Session
from utils.security import verify_token

router = APIRouter(prefix="/courses", tags=["courses"])


def get_course_service(db: Session = Depends(get_db)) -> CourseService:
    """
    Dependency factory for CourseService.

    Constructs a CourseService instance with an injected database session,
    wiring it to a CourseRepository for data access.

    Args:
        db (Session): The SQLAlchemy database session provided by get_db.

    Returns:
        CourseService: A fully initialized CourseService instance.
    """
    return CourseService(repo=CourseRepository(db=db))


@router.get("/", response_model=ShowCoursesSchema)
async def get_courses(service: CourseService = Depends(get_course_service)):
    """
    Retrieve all courses.

    Args:
        service (CourseService): The course service instance, injected via dependency.

    Returns:
        ShowCoursesSchema: A list of all courses serialized with full course info.
    """
    return service.get_courses()


@router.get("/{course_id}")
async def get_course(course_id: int, service: CourseService = Depends(get_course_service)):
    """
    Retrieve a single course by its ID.

    Args:
        course_id (int): The ID of the course to retrieve.
        service (CourseService): The course service instance, injected via dependency.

    Returns:
        Course: The course record matching the given ID.

    Raises:
        HTTPException: If the course is not found (propagated from the service layer).
    """
    return service.get_course(course_id)


@router.get("/{course_id}/simple-info", response_model=ShowSimpleCourseInfoSchema)
async def get_simple_course_info(course_id: int, service: CourseService = Depends(get_course_service)):
    """
    Retrieve simplified course information by course ID.

    Args:
        course_id (int): The ID of the course to retrieve.
        service (CourseService): The course service instance, injected via dependency.

    Returns:
        ShowSimpleCourseInfoSchema: A simplified view of the course containing
                                    title, duration, and level.

    Raises:
        HTTPException: If the course is not found (propagated from the service layer).
    """
    return service.get_simple_course_info(course_id)


@router.put("/update/{course_id}")
async def update_course(course_id: int, course: ModifyCoursesSchema, service: CourseService = Depends(get_course_service)):
    """
    Update an existing course by its ID.

    Requires a valid authentication token.

    Args:
        course_id (int): The ID of the course to update.
        course (ModifyCoursesSchema): The request body containing updated course data.
        service (CourseService): The course service instance, injected via dependency.

    Returns:
        Course: The updated course record.

    Raises:
        HTTPException: If the course is not found (propagated from the service layer).
    """
    _: dict = Depends(verify_token)
    return service.update_course(course_id, course)


@router.post("/create-course")
async def create_course(course: CoursesCreateSchema, _: dict = Depends(verify_token), service: CourseService = Depends(get_course_service)):
    """
    Create a new course.

    Requires a valid authentication token.

    Args:
        course (CoursesCreateSchema): The request body containing the new course data.
        service (CourseService): The course service instance, injected via dependency.

    Returns:
        Course: The newly created course record.
    """
    return service.create(course)


@router.delete("/delete/{course_id}")
async def delete_course(course_id: int, _: dict = Depends(verify_token), service: CourseService = Depends(get_course_service)):
    """
    Delete a course by its ID.

    Requires a valid authentication token.

    Args:
        course_id (int): The ID of the course to delete.
        service (CourseService): The course service instance, injected via dependency.

    Returns:
        bool: True if the course was successfully deleted.

    Raises:
        HTTPException: If the course is not found (propagated from the service layer).
    """
    return service.delete_course(course_id)

@router.patch("/delete-soft/{course_id}")
async def delete_soft_course(course_id: int, _: dict = Depends(verify_token), service: CourseService = Depends(get_course_service)):
    """
    Soft delete a course by its ID.

    Requires a valid authentication token.

    Args:
        course_id (int): The ID of the course to soft delete.
        service (CourseService): The course service instance, injected via dependency.

    Returns:
        bool: True if the course was successfully soft deleted. 
    Raises:        HTTPException: If the course is not found (propagated from the service layer).
    """
    return service.delete_soft_course(course_id)
