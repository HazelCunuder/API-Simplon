from fastapi import APIRouter
from api.v1.endpoints.user_endpoints import router as user_router
from api.v1.endpoints.courses_endpoints import router as courses_router

api_router = APIRouter()
api_router.include_router(user_router)
api_router.include_router(courses_router)