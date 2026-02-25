from fastapi import APIRouter, Depends
from services.courses_services import CourseService
from repositories.course_repository import CourseRepository
from schemas.courses_schema import CoursesCreateSchema, ModifyCoursesSchema, ShowCoursesSchema, ShowSimpleCourseInfoSchema
from configs.database import get_db_connection
from sqlalchemy.orm import Session

router = APIRouter(prefix="/courses", tags=["courses"])

def get_course_service(db: Session = Depends(get_db_connection)) -> CourseService:
    return CourseService(repo=CourseRepository(db=db))

@router.get("/", response_model=ShowCoursesSchema)
async def get_courses(service: CourseService = Depends(get_course_service)):
    return service.get_courses()

@router.get("/{course_id}")
async def get_course(course_id: int, service: CourseService = Depends(get_course_service)):
    return service.get_course(course_id)

@router.get("/{course_id}/simple-info", response_model=ShowSimpleCourseInfoSchema)
async def get_simple_course_info(course_id: int, service: CourseService = Depends(get_course_service)):
    return service.get_simple_course_info(course_id)

@router.post("/update/{course_id}")
async def update_course(course_id: int, course: ModifyCoursesSchema, service: CourseService = Depends(get_course_service)):
    return service.update_course(course_id, course)

@router.post("/create-course")
async def create_course(course: CoursesCreateSchema, service: CourseService = Depends(get_course_service)):
    return service.create(course)

@router.delete("/delete/{course_id}")
async def delete_course(course_id: int, service: CourseService = Depends(get_course_service)):
    return service.delete_course(course_id)
