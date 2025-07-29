from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
import uuid


def generate_id() -> str:
    """Generate a unique user ID"""
    return f"user_{uuid.uuid4().hex[:8]}"


class User(BaseModel):
    """User domain entity"""
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    email: str
    name: str
    created_at: datetime = Field(default_factory=datetime.now)