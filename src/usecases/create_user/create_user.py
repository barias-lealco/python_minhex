from typing import Optional
from ...domain.entities.user import User, generate_id
from ...domain.ports.user_repository import UserRepository
from ...domain.errors.domain_error import UserAlreadyExistsError
from .dtos import CreateUserRequest, CreateUserResponse


class CreateUserUseCase:
    """Use case for creating a new user"""
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
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
        
        return CreateUserResponse(user_id=user.id)