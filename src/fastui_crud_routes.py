from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session as DBSession
from model.database import get_db
from services.user_service import UserService
from services.courses_services import CourseService
from services.session_services import SessionService
from repositories.course_repository import CourseRepository
from utils.security import verify_token

router = APIRouter(prefix="/admin", include_in_schema=False)


# ============= USERS CRUD =============

@router.get("/users/{user_id}/delete")
async def delete_user(
    user_id: int,
    _: dict = Depends(verify_token),
    db: DBSession = Depends(get_db)
):
    """Supprimer un utilisateur"""
    service = UserService(db=db)
    try:
        service.delete_user(user_id, soft_delete=False)
        return RedirectResponse(url="/admin/users", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============= COURSES CRUD =============

@router.get("/courses/{course_id}/delete")
async def delete_course(
    course_id: int,
    token: dict = Depends(verify_token),
    db: DBSession = Depends(get_db)
):
    """Supprimer un cours"""
    service = CourseService(repo=CourseRepository(db=db))
    try:
        service.delete_course(course_id, soft_delete=False)
        return RedirectResponse(url="/admin/courses", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============= SESSIONS CRUD =============

@router.get("/sessions/{session_id}/delete")
async def delete_session(
    session_id: int,
    token: dict = Depends(verify_token),
    db: DBSession = Depends(get_db)
):
    """Supprimer une session"""
    service = SessionService(db=db)
    try:
        service.soft_delete_session(session_id)
        return RedirectResponse(url="/admin/sessions", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
