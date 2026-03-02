from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from model.user import Role
from repositories.session_repository import SessionRepository
from schemas.user_session_schema import EnrollmentCreate, EnrollmentResponse, SessionsByStudentResponse, StudentsBySessionResponse, EnrollmentDetail
from model.database import get_db
from services.user_session_services import UserSessionService
from utils.permission_handler import role_checker
from utils.security import verify_token

router = APIRouter(prefix="/enrollments", tags=["enrollments"])

@router.post("/", response_model=EnrollmentResponse, status_code=201)
def enroll_student(payload: EnrollmentCreate,_: dict = Depends(verify_token), _ = Depends(role_checker(Role.ADMIN)), db: DBSession = Depends(get_db)):
    try:
        return UserSessionService(db).enroll_student(payload.user_id, payload.session_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/student/{user_id}", response_model=SessionsByStudentResponse)
def get_sessions_by_student(user_id: int, _: dict = Depends(verify_token), db: DBSession = Depends(get_db)):
    try:
        enrollments = UserSessionService(db).get_sessions_by_student(user_id)
        return SessionsByStudentResponse(user_id=user_id, sessions=enrollments)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/session/{session_id}", response_model=StudentsBySessionResponse)
def get_students_by_session(session_id: int, _: dict = Depends(verify_token), db: DBSession = Depends(get_db)):
    try:
        enrollments = UserSessionService(db).get_students_by_session(session_id)
        session = enrollments[0].session if enrollments else SessionRepository(db).get_by_id(session_id)
        return StudentsBySessionResponse(
            session_id=session_id,
            teacher_id=session.teacher_id,
            students=enrollments
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{user_id}/{session_id}", response_model=EnrollmentDetail)
def get_enrollment(user_id: int, session_id: int, _: dict = Depends(verify_token), db: DBSession = Depends(get_db)):
    try:
        return UserSessionService(db).get_enrollment(user_id, session_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.patch("/{user_id}/{session_id}", response_model=EnrollmentResponse)
def update_enrollment(user_id: int, session_id: int, payload: EnrollmentCreate, db: DBSession = Depends(get_db), _: dict = Depends(verify_token)):
    try:        
        return UserSessionService(db).update_enrollment(user_id, session_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}/{session_id}", status_code=204)
def unenroll_student(user_id: int, session_id: int,_: dict = Depends(verify_token), _ = Depends(role_checker(Role.ADMIN)), db: DBSession = Depends(get_db)):
    try:
        UserSessionService(db).unenroll_student(user_id, session_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.patch("/delete-soft/{enrollment_id}", status_code=204)
def soft_delete_enrollment(enrollment_id: int, _: dict = Depends(verify_token), db: DBSession = Depends(get_db)):
    try:
        UserSessionService(db).soft_delete_enrollment(enrollment_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))