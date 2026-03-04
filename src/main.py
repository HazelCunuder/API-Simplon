from fastapi import FastAPI, Request
from api.v1.routers.api import api_router
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastui_routes import router as admin_router
from fastui_crud_routes import router as crud_router
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from utils.exceptions import (
    AppError,
    CourseAlreadyExistsError,
    CourseEnrollmentError, 
    CourseNotFoundError, 
    ExpiredTokenError, 
    InvalidCredentialsError, 
    InvalidSessionStateError, 
    InvalidTokenError, 
    SessionAlreadyEndedError, 
    SessionAlreadyExistsError, 
    SessionAlreadyStartedError, 
    SessionNotFoundError, 
    UserAlreadyEnrolledError, 
    UserNotFoundError,
    EmailIsAlreadyInUseError,
    SessionAlreadyFullError 
)

app = FastAPI(
    version="1.0.0"
)

origins = [
    "http://localhost",
    "http://localhost:8080"
    # Insert origin for frontend here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"]
    )

Path("static").mkdir(exist_ok=True)

try:
    app.mount("/admin/static", StaticFiles(directory="static"), name="static")
except Exception as e:
    print(f"Unable to mount static files: {e}")

app.include_router(api_router)
app.include_router(admin_router)
app.include_router(crud_router)

@app.get("/", response_class=RedirectResponse)
async def root():
    return RedirectResponse(url="/admin/")

@app.exception_handler(AppError)
async def app_exception_handler(request: Request, exc: AppError) -> JSONResponse:
    status_code = 500

    if isinstance(
        exc,
        (
            UserNotFoundError,
            InvalidCredentialsError,
            InvalidTokenError,
            ExpiredTokenError,
            SessionNotFoundError,
            InvalidSessionStateError,
            CourseNotFoundError,
            CourseEnrollmentError,
            UserAlreadyEnrolledError,
        ),
    ):
        status_code = 400
    elif isinstance(exc, (EmailIsAlreadyInUseError, CourseAlreadyExistsError, SessionAlreadyExistsError)):
        status_code = 409
    elif isinstance(exc, 
                    (
                        SessionAlreadyStartedError, 
                        SessionAlreadyEndedError,
                        SessionAlreadyFullError
                    )
                ):
        status_code = 400
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": exc.code, "message": exc.message}},
    )