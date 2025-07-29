from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    """Request DTO for creating a user"""
    email: EmailStr
    name: str


class CreateUserResponse(BaseModel):
    """Response DTO for creating a user"""
    user_id: str