from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, field_validator

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserPayload(BaseModel):
    username: str
    password: str

    @field_validator("username")
    def validate_username(cls, v):
        if not v:
            raise ValueError("Username cannot be empty")
        if len(v) < 4:
            raise ValueError("Username must be at least 4 characters")
        return v

    @field_validator("password")
    def validate_password(cls, v):
        if not v:
            raise ValueError("Password cannot be empty")
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        return v


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True
