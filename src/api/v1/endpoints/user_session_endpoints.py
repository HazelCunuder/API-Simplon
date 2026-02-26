from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from schemas.user_session_schema import EnrollmentCreate, EnrollmentResponse
from model.database import get_db
from services.user_session_services import UserSessionService


router = APIRouter(prefix="/enrollments", tags=["enrollments"])

@router.post("/", response_model=EnrollmentResponse, status_code=201)
def enroll_student(payload: EnrollmentCreate, db: DBSession = Depends(get_db)):
    try:
        return UserSessionService(db).enroll_student(payload.user_id, payload.session_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}/{session_id}", status_code=204)
def unenroll_student(user_id: int, session_id: int, db: DBSession = Depends(get_db)):
    try:
        UserSessionService(db).unenroll_student(user_id, session_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}/{session_id}", response_model=EnrollmentResponse)
def get_enrollment(user_id: int, session_id: int, db: DBSession = Depends(get_db)):
    try:
        return UserSessionService(db).get_enrollment(user_id, session_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/student/{user_id}", response_model=list[EnrollmentResponse])
def get_sessions_by_student(user_id: int, db: DBSession = Depends(get_db)):
    try:
        return UserSessionService(db).get_sessions_by_student(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/session/{session_id}", response_model=list[EnrollmentResponse])
def get_students_by_session(session_id: int, db: DBSession = Depends(get_db)):
    try:
        return UserSessionService(db).get_students_by_session(session_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))