from pydantic import BaseModel, ConfigDict
from datetime import datetime
from ..entities.user import User


class UserCreated(BaseModel):
    """Domain event for when a user is created"""
    model_config = ConfigDict(from_attributes=True)
    
    user_id: str
    email: str
    name: str
    created_at: datetime

    @classmethod
    def from_user(cls, user: User) -> "UserCreated":
        """Create UserCreated event from User entity"""
        return cls(
            user_id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at
        )