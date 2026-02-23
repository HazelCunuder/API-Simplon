from pydantic import BaseModel, ConfigDict, validate_call
from datetime import date

class User(BaseModel):
    id: int
    last_name: str 
    first_name: str
    email: str
    role: int
    register_date: date

    model_config = ConfigDict(str_max_length=10)
    
class UserCreate(BaseModel):
    last_name: str 
    first_name: str
    email: str
    role: int
    register_date: date

class UserUpdate(BaseModel):
    last_name: str | None
    first_name: str | None
    email: str | None
    role: int | None
    register_date: date | None

class UserDelete(BaseModel):
    id: int
    

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
def validate_mail(email: str) -> str:
    if "@" not in email:
        raise ValueError("Invalid email address")
    return email

@validate_call
def validate_role(role: int) -> int:
    if role not in [0, 1, 2]:
        raise ValueError("Invalid role value")
    return role

@validate_call
def validate_register_date(register_date: date) -> date:
    if register_date > date.today():
        raise ValueError("Register date cannot be in the future")
    return register_date