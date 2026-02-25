from fastapi import APIRouter
from schemas.courses_schema import CoursesCreateSchema, ModifyCoursesSchema, ShowCoursesSchema, ShowSimpleCourseInfoSchema

router = APIRouter(prefix="/courses", tags=["courses"])

# GET

@router.get("/")
async def get_courses(course: ShowCoursesSchema):
    return {"message": "Get all courses"}

@router.get("/{course_id}")
async def get_course(course_id: int, course: ShowCoursesSchema):
    return {"message": f"Get course with id {course_id}"}

@router.get("/simple/{course_id}")
async def get_simple_course_info(course_id: int, course: ShowSimpleCourseInfoSchema):
    return {"message": f"Get simple info for course with id {course_id}"}

# POST

@router.post("/create-course")
async def create_course(course: CoursesCreateSchema):
    return {"message": "Create a new course", "course": course}

# PUT

@router.put("/update/{course_id}")
async def update_course(course_id: int, course: ModifyCoursesSchema):
    return {"message": f"Update course with id {course_id}", "course": course}

# DELETE

@router.delete("/delete/{course_id}")
async def delete_course(course_id: int):
    return {"message": f"Delete course with id {course_id}"}
