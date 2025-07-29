from abc import ABC, abstractmethod
from typing import Any
from ..events.user_created import UserCreated


class EventPublisher(ABC):
    """Abstract base class for publishing domain events"""
    
    @abstractmethod
    async def publish(self, event: Any) -> None:
        """Publish a domain event"""
        pass
    
    @abstractmethod
    async def publish_user_created(self, event: UserCreated) -> None:
        """Publish a UserCreated event specifically"""
        pass