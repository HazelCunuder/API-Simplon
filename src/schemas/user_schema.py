from pydantic import BaseModel,validate_call, Field, EmailStr, SecretStr
from datetime import date

    
class UserCreate(BaseModel):
    last_name: str = Field(description="The user's last name", strict=True)
    first_name: str = Field(description="The user's first name", strict=True)
    password: SecretStr = Field(description="The user's password", strict=True)
    email: EmailStr = Field(description="The user's email address", strict=True)
    role: int = Field(description="The user's role (0=Admin, 1=Manager, 2=Employee)", ge=0, le=2)
    register_date: date = Field(description="The date the user registered")

class UserUpdate(BaseModel):
    last_name: str = Field(description="The user's last name", strict=True)
    first_name: str = Field(description="The user's first name", strict=True)
    password: SecretStr = Field(description="The user's password", strict=True)
    email: EmailStr = Field(description="The user's email address", strict=True)
    role: int = Field(description="The user's role (0=Admin, 1=Manager, 2=Employee)", ge=0, le=2)
    register_date: date = Field(description="The date the user registered")

class UserDelete(BaseModel):
    id: int = Field(description="The user's ID", ge=0)

@validate_call
def validate_name(name: str) -> str:
    if not name.isalpha():
        raise ValueError("Name must contain only letters")
    return name

@validate_call
def validate_last_name(last_name: str) -> str:
    if not last_name.isalpha():
        raise ValueError("Last name must contain only letters")
    return last_name


@validate_call
def validate_register_date(register_date: date) -> date:
    if register_date > date.today():
        raise ValueError("Register date cannot be in the future")
    return register_date