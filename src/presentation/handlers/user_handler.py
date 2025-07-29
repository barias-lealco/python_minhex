from fastapi import HTTPException, status
from ...usecases.create_user.create_user import CreateUserUseCase
from ...usecases.create_user.dtos import CreateUserRequest, CreateUserResponse
from ...domain.errors.domain_error import UserAlreadyExistsError


class UserHandler:
    """HTTP handler for user operations"""
    
    def __init__(self, create_user_use_case: CreateUserUseCase):
        self.create_user_use_case = create_user_use_case
    
    async def create_user(self, request: CreateUserRequest) -> CreateUserResponse:
        """Create a new user"""
        try:
            return await self.create_user_use_case.execute(request)
        except UserAlreadyExistsError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )