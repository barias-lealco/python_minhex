import pytest
import pytest_asyncio
from src.usecases.create_user.create_user import CreateUserUseCase
from src.usecases.create_user.dtos import CreateUserRequest
from src.infra.persistence.memory.user_repository import InMemoryUserRepository
from src.infra.messaging.in_memory_event_publisher import InMemoryEventPublisher
from src.domain.errors.domain_error import UserAlreadyExistsError
from src.domain.events.user_created import UserCreated


@pytest_asyncio.fixture
async def repository():
    """Fixture to provide a clean repository for each test"""
    repo = InMemoryUserRepository()
    await repo.clear()
    return repo


@pytest_asyncio.fixture
async def event_publisher():
    """Fixture to provide a clean event publisher for each test"""
    publisher = InMemoryEventPublisher()
    await publisher.clear_events()
    return publisher


@pytest.mark.asyncio
async def test_create_user_success(repository, event_publisher):
    """Test successful user creation"""
    # Arrange
    use_case = CreateUserUseCase(repository, event_publisher)
    request = CreateUserRequest(email="test@example.com", name="Test User")
    
    # Act
    response = await use_case.execute(request)
    
    # Assert
    assert response.user_id.startswith("user_")
    assert len(response.user_id) > 5
    
    # Check that event was published
    events = await event_publisher.get_events()
    assert len(events) == 1
    assert isinstance(events[0], UserCreated)
    assert events[0].user_id == response.user_id
    assert events[0].email == request.email
    assert events[0].name == request.name


@pytest.mark.asyncio
async def test_create_user_duplicate_email(repository, event_publisher):
    """Test that creating a user with duplicate email raises error"""
    # Arrange
    use_case = CreateUserUseCase(repository, event_publisher)
    request = CreateUserRequest(email="test@example.com", name="Test User")
    
    # Act - Create first user
    await use_case.execute(request)
    
    # Clear events from first creation
    await event_publisher.clear_events()
    
    # Act & Assert - Try to create duplicate
    with pytest.raises(UserAlreadyExistsError):
        await use_case.execute(request)
    
    # Check that no event was published for duplicate
    events = await event_publisher.get_events()
    assert len(events) == 0


@pytest.mark.asyncio
async def test_create_user_different_emails(repository, event_publisher):
    """Test that users with different emails can be created"""
    # Arrange
    use_case = CreateUserUseCase(repository, event_publisher)
    
    # Act
    response1 = await use_case.execute(
        CreateUserRequest(email="user1@example.com", name="User 1")
    )
    response2 = await use_case.execute(
        CreateUserRequest(email="user2@example.com", name="User 2")
    )
    
    # Assert
    assert response1.user_id != response2.user_id
    
    # Check that both events were published
    events = await event_publisher.get_events()
    assert len(events) == 2
    assert all(isinstance(event, UserCreated) for event in events)
    assert events[0].user_id == response1.user_id
    assert events[1].user_id == response2.user_id