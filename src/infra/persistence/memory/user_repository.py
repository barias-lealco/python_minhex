import asyncio
from typing import Optional, Dict
from ....domain.entities.user import User
from ....domain.ports.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    """In-memory implementation of UserRepository for testing and development"""
    
    _instance = None
    _lock = asyncio.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._users: Dict[str, User] = {}
            cls._instance._data_lock = asyncio.Lock()
        return cls._instance
    
    async def save(self, user: User) -> None:
        """Save a user to the in-memory store"""
        async with self._data_lock:
            self._users[user.id] = user
    
    async def find_by_id(self, user_id: str) -> Optional[User]:
        """Find a user by ID"""
        async with self._data_lock:
            return self._users.get(user_id)
    
    async def find_by_email(self, email: str) -> Optional[User]:
        """Find a user by email"""
        async with self._data_lock:
            for user in self._users.values():
                if user.email == email:
                    return user
            return None
    
    async def clear(self) -> None:
        """Clear all users (for testing purposes)"""
        async with self._data_lock:
            self._users.clear()