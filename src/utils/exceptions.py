from typing import Optional

class AppError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(message)

class InvalidCredentialsError(Exception):
    code = "INVALID_CREDENTIALS"

    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "Invalid username or password."
        super().__init__(code=self.code, message=message)

class EmailIsAlreadyInUseError(Exception):
    code = "EMAIL_ALREADY_IN_USE"

    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "This email is already used."
        super().__init__(code=self.code, message=message)

class UserNotFoundError(Exception):
    code = "USER_NOT_FOUND"

    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "User not found."
        super().__init__(code=self.code, message=message)

class InvalidTokenError(Exception):
    code = "INVALID_TOKEN"

    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "The provided token is invalid."
        super().__init__(code=self.code, message=message)

class ExpiredTokenError(Exception):
    code = "EXPIRED_TOKEN"

    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "The provided token has expired."
        super().__init__(code=self.code, message=message)

class SessionAlreadyExistsError(Exception):
    code = "SESSION_ALREADY_EXISTS"

    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "This session already exists."
        super().__init__(code=self.code, message=message)

class SessionAlreadyStartedError(Exception):
    code = "SESSION_ALREADY_STARTED"

    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "The session has already been started."
        super().__init__(code=self.code, message=message)

class SessionNotFoundError(Exception):
    code = "SESSION_NOT_FOUND"

    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "Session not found."
        super().__init__(code=self.code, message=message)

class SessionAlreadyEndedError(Exception):
    code = "SESSION_ALREADY_ENDED"

    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "The session has already ended."
        super().__init__(code=self.code, message=message)

class InvalidSessionStateError(Exception):
    code = "INVALID_SESSION_STATE"

    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "The session is in an invalid state for this operation."
        super().__init__(code=self.code, message=message)

class CourseNotFoundError(Exception):
    code = "COURSE_NOT_FOUND"

    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "Course not found."
        super().__init__(code=self.code, message=message)

class CourseAlreadyExistsError(Exception):
    code = "COURSE_ALREADY_EXISTS"

    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "This course already exists."
        super().__init__(code=self.code, message=message)

class CourseEnrollmentError(Exception):
    code = "COURSE_ENROLLMENT_ERROR"

    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "An error occurred during course enrollment."
        super().__init__(code=self.code, message=message)

class UserAlreadyEnrolledError(Exception):
    code = "USER_ALREADY_ENROLLED"

    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "User is already enrolled in this course."
        super().__init__(code=self.code, message=message)

class SessionAlreadyFullError(Exception):
    code = "SESSION_ALREADY_FULL"

    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "The session is already full."
        super().__init__(code=self.code, message=message)
