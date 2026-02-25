from fastapi import APIRouter
from api.v1.endpoints.user_endpoints import router as user_router
from api.v1.endpoints.session_endpoints import router as session_router

api_router = APIRouter()
api_router.include_router(user_router)
api_router.include_router(session_router)