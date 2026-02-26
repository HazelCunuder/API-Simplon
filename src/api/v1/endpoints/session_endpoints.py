from fastapi import APIRouter, status, Depends
from schemas.sessions_schema import SessionCreate, SessionRead, SessionUpdate
from services.session_services import SessionService
from utils.security import verify_token

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.get("/{session_id}", response_model=SessionRead)
async def get_session(session_id: int, service: SessionService = Depends()):
    _: dict = Depends(verify_token)
    return service.get_session(session_id)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_session(session: SessionCreate, service: SessionService = Depends()):
    _: dict = Depends(verify_token)
    return service.create_session(session)

@router.put("/{session_id}")
async def update_session(session_id: int, session: SessionUpdate, service: SessionService = Depends()):
    _: dict = Depends(verify_token)
    return service.update_session(session_id, session)  

@router.get("/{session_id}", response_model=SessionRead)
async def get_session(session_id: int, service: SessionService = Depends()):
    _: dict = Depends(verify_token)
    return service.get_session(session_id)