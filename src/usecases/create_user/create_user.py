from typing import Optional
from ...domain.entities.user import User, generate_id
from ...domain.ports.user_repository import UserRepository
from ...domain.ports.event_publisher import EventPublisher
from ...domain.events.user_created import UserCreated
from ...domain.errors.domain_error import UserAlreadyExistsError
from .dtos import CreateUserRequest, CreateUserResponse


class CreateUserUseCase:
    """Use case for creating a new user"""
    
    def __init__(self, user_repository: UserRepository, event_publisher: EventPublisher):
        self.user_repository = user_repository
        self.event_publisher = event_publisher
    
    async def execute(self, request: CreateUserRequest) -> CreateUserResponse:
        """Execute the create user use case"""
        # Check if user already exists
        existing_user = await self.user_repository.find_by_email(request.email)
        if existing_user:
            raise UserAlreadyExistsError(f"User with email {request.email} already exists")
        
        # Create new user with generated ID
        user = User(
            id=generate_id(),
            email=request.email, 
            name=request.name
        )
        
        # Save user
        await self.user_repository.save(user)
        
        # Publish domain event
        user_created_event = UserCreated.from_user(user)
        await self.event_publisher.publish_user_created(user_created_event)
        
        return CreateUserResponse(user_id=user.id)