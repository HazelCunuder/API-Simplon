from fastapi import APIRouter, status
from schemas.sessions_schema import SessionCreate

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("/sessions", status_code=status.HTTP_201_CREATED)
async def create_session(session: SessionCreate):
    # TODO : call service
    return {"message": "Session created", "data": session}

@router.put("/sessions/{session_id}")
async def update_session(session_id: int, session: SessionCreate):
    # TODO : call service
    return {"message": f"Session {session_id} updated"}

@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(session_id: int):
    # TODO : call service
    return None