from fastapi import APIRouter, status
from schemas.sessions_schema import SessionCreate, SessionRead, SessionUpdate

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("/sessions", status_code=status.HTTP_201_CREATED)
async def create_session(session: SessionCreate):
    # TODO : call service
    return {"message": "Session created", "data": session}

@router.put("/sessions/{session_id}")
async def update_session(session_id: int, session: SessionUpdate):
    # TODO : call service
    return {"message": f"Session {session_id} updated"}

@router.get("/sessions/{session_id}", response_model=SessionRead)
async def get_session(session_id: int):
    # TODO : call service 
    return None