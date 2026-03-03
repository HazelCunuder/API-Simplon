from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from model.user import Role
from schemas.user_session_schema import EnrollmentCreate, EnrollmentResponse, EnrollmentDetail
from model.database import get_db
from services.user_session_services import UserSessionService
from utils.permission_handler import role_checker
from utils.security import verify_token

router = APIRouter(prefix="/enrollments", tags=["enrollments"])

@router.post("/", response_model=EnrollmentResponse, status_code=201)
def enroll_student(payload: EnrollmentCreate,_: dict = Depends(verify_token), __ = Depends(role_checker(Role.ADMIN)), db: DBSession = Depends(get_db)):
    try:
        return UserSessionService(db).enroll_student(payload.user_id, payload.session_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=EnrollmentDetail)
def get_enrollments( _: dict = Depends(verify_token), db: DBSession = Depends(get_db)):
    try:
        return UserSessionService(db).get_enrollments()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.delete("/", status_code=204)
def unenroll_student(user_id: int, session_id: int,_: dict = Depends(verify_token), __ = Depends(role_checker(Role.ADMIN)), db: DBSession = Depends(get_db)):
    try:
        UserSessionService(db).unenroll_student(user_id, session_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
