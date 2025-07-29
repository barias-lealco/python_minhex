import pytest
import pytest_asyncio
from src.usecases.create_user.create_user import CreateUserUseCase
from src.usecases.create_user.dtos import CreateUserRequest
from src.infra.persistence.memory.user_repository import InMemoryUserRepository
from src.domain.errors.domain_error import UserAlreadyExistsError


@pytest_asyncio.fixture
async def repository():
    """Fixture to provide a clean repository for each test"""
    repo = InMemoryUserRepository()
    await repo.clear()
    return repo


@pytest.mark.asyncio
async def test_create_user_success(repository):
    """Test successful user creation"""
    # Arrange
    use_case = CreateUserUseCase(repository)
    request = CreateUserRequest(email="test@example.com", name="Test User")
    
    # Act
    response = await use_case.execute(request)
    
    # Assert
    assert response.user_id.startswith("user_")
    assert len(response.user_id) > 5


@pytest.mark.asyncio
async def test_create_user_duplicate_email(repository):
    """Test that creating a user with duplicate email raises error"""
    # Arrange
    use_case = CreateUserUseCase(repository)
    request = CreateUserRequest(email="test@example.com", name="Test User")
    
    # Act - Create first user
    await use_case.execute(request)
    
    # Act & Assert - Try to create duplicate
    with pytest.raises(UserAlreadyExistsError):
        await use_case.execute(request)


@pytest.mark.asyncio
async def test_create_user_different_emails(repository):
    """Test that users with different emails can be created"""
    # Arrange
    use_case = CreateUserUseCase(repository)
    
    # Act
    response1 = await use_case.execute(
        CreateUserRequest(email="user1@example.com", name="User 1")
    )
    response2 = await use_case.execute(
        CreateUserRequest(email="user2@example.com", name="User 2")
    )
    
    # Assert
    assert response1.user_id != response2.user_id