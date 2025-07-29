from fastapi import APIRouter, Depends
from .handlers.user_handler import UserHandler
from ..usecases.create_user.create_user import CreateUserUseCase
from ..usecases.create_user.dtos import CreateUserRequest, CreateUserResponse
from ..infra.persistence.memory.user_repository import InMemoryUserRepository

# Create router
router = APIRouter(prefix="/api/v1", tags=["users"])

# Dependency injection functions
def get_user_repository() -> InMemoryUserRepository:
    """Get user repository instance"""
    return InMemoryUserRepository()

def get_create_user_use_case(
    user_repository: InMemoryUserRepository = Depends(get_user_repository)
) -> CreateUserUseCase:
    """Get create user use case instance"""
    return CreateUserUseCase(user_repository)

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