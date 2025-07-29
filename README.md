# Python MinHex - Minimal Hexagonal Architecture

A Python implementation of minimal hexagonal architecture using FastAPI, Pydantic, and uvicorn. This project demonstrates clean architecture principles adapted to Python conventions.

## 🏗️ Architecture Overview

This project follows hexagonal architecture (also known as ports and adapters) with the following layers:

```
src/
├── domain/                    # Business core (no external dependencies)
│   ├── entities/              # Business entities (User)
│   ├── events/                # Domain events (UserCreated)
│   ├── ports/                 # Interfaces/contracts (UserRepository)
│   └── errors/                # Domain-specific errors
├── usecases/                  # Application logic (one use case = one folder)
│   └── create_user/           # create_user.py, dtos.py
├── infra/                     # External implementations
│   └── persistence/           # Repository implementations
│       └── memory/            # In-memory for development/testing
└── presentation/              # Delivery layer
    ├── handlers/              # HTTP handlers
    ├── routes.py              # FastAPI router configuration
    └── app.py                 # FastAPI application setup
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- uv (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd python_minhex
```

2. Install dependencies:
```bash
uv sync
```

3. Run the application:
```bash
uv run python main.py
```

Or using uvicorn directly:
```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### API Documentation

Once the application is running, you can access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📝 API Endpoints

### Create User
```http
POST /api/v1/users
Content-Type: application/json

{
  "email": "user@example.com",
  "name": "John Doe"
}
```

Response:
```json
{
  "user_id": "user_a1b2c3d4"
}
```

## 🎯 Key Features

- **Hexagonal Architecture**: Clean separation of concerns with domain-driven design
- **FastAPI**: Modern, fast web framework with automatic API documentation
- **Pydantic**: Data validation and serialization
- **Async/Await**: Full async support throughout the application
- **Dependency Injection**: FastAPI's built-in DI system for clean architecture
- **Type Safety**: Full type hints and validation

## 🔧 Development

### Project Structure
- **Domain Layer**: Contains business logic, entities, and interfaces
- **Use Cases**: Application-specific business rules
- **Infrastructure**: External implementations (databases, APIs, etc.)
- **Presentation**: HTTP layer with FastAPI

### Adding New Features

1. **Domain Entity**: Add to `src/domain/entities/`
2. **Repository Interface**: Add to `src/domain/ports/`
3. **Use Case**: Create new folder in `src/usecases/`
4. **Infrastructure**: Implement repository in `src/infra/persistence/`
5. **Presentation**: Add handler and routes

### Testing
```bash
# Run tests (when implemented)
uv run pytest

# Run with coverage
uv run pytest --cov=src
```

## 🏛️ Architecture Principles

- **Dependency Inversion**: Domain never imports from other layers
- **Single Responsibility**: Each class has one reason to change
- **Open/Closed**: Open for extension, closed for modification
- **YAGNI**: You Aren't Gonna Need It - don't over-engineer
- **KISS**: Keep It Simple, Stupid

## 📦 Dependencies

- **FastAPI**: Web framework
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server
- **email-validator**: Email validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
