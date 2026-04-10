# Должен экспортировать все классы:
from app.exceptions.base import (
    AppException,
    NotFoundException,
    ValidationError,
    DatabaseError,
    ConflictError,
    ForbiddenError,
)

__all__ = [
    "AppException",
    "NotFoundException",
    "ValidationError",
    "DatabaseError",
    "ConflictError",
    "ForbiddenError",
]