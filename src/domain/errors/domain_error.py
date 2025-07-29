class DomainError(Exception):
    """Base domain error"""
    pass


class UserNotFoundError(DomainError):
    """Raised when a user is not found"""
    pass


class UserAlreadyExistsError(DomainError):
    """Raised when trying to create a user that already exists"""
    pass


class InvalidUserDataError(DomainError):
    """Raised when user data is invalid"""
    pass