from fastapi import APIRouter, Depends
from .handlers.user_handler import UserHandler
from ..usecases.create_user.create_user import CreateUserUseCase
from ..usecases.create_user.dtos import CreateUserRequest, CreateUserResponse
from ..infra.persistence.memory.user_repository import InMemoryUserRepository
from ..infra.messaging.in_memory_event_publisher import InMemoryEventPublisher

# Create router
router = APIRouter(prefix="/api/v1", tags=["users"])

# Dependency injection functions
def get_user_repository() -> InMemoryUserRepository:
    """Get user repository instance"""
    return InMemoryUserRepository()

def get_event_publisher() -> InMemoryEventPublisher:
    """Get event publisher instance"""
    return InMemoryEventPublisher()

def get_create_user_use_case(
    user_repository: InMemoryUserRepository = Depends(get_user_repository),
    event_publisher: InMemoryEventPublisher = Depends(get_event_publisher)
) -> CreateUserUseCase:
    """Get create user use case instance"""
    return CreateUserUseCase(user_repository, event_publisher)

def get_user_handler(
    create_user_use_case: CreateUserUseCase = Depends(get_create_user_use_case)
) -> UserHandler:
    """Get user handler instance"""
    return UserHandler(create_user_use_case)

# Routes
@router.post("/users", response_model=CreateUserResponse, status_code=201)
async def create_user(
    request: CreateUserRequest,
    handler: UserHandler = Depends(get_user_handler)
) -> CreateUserResponse:
    """Create a new user"""
    return await handler.create_user(request)