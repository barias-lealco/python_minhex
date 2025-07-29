import asyncio
from typing import Any, List
from ...domain.ports.event_publisher import EventPublisher
from ...domain.events.user_created import UserCreated


class InMemoryEventPublisher(EventPublisher):
    """In-memory implementation of EventPublisher for development and testing"""
    
    def __init__(self):
        self._events: List[Any] = []
        self._lock = asyncio.Lock()
    
    async def publish(self, event: Any) -> None:
        """Publish a domain event to in-memory storage"""
        async with self._lock:
            self._events.append(event)
            print(f"📢 Event published: {type(event).__name__}")
    
    async def publish_user_created(self, event: UserCreated) -> None:
        """Publish a UserCreated event specifically"""
        await self.publish(event)
    
    async def get_events(self) -> List[Any]:
        """Get all published events (for testing)"""
        async with self._lock:
            return self._events.copy()
    
    async def clear_events(self) -> None:
        """Clear all events (for testing)"""
        async with self._lock:
            self._events.clear()