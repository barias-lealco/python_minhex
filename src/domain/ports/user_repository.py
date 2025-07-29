from abc import ABC, abstractmethod
from typing import Optional
from ..entities.user import User


class UserRepository(ABC):
    """Abstract base class for user repository operations"""
    
    @abstractmethod
    async def save(self, user: User) -> None:
        """Save a user to the repository"""
        pass
    
    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]:
        """Find a user by ID"""
        pass
    
    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        """Find a user by email"""
        pass