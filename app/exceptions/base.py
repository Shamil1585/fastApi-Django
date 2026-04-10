from typing import Optional, Dict, Any


class AppException(Exception):
    """Базовый класс для всех исключений приложения"""
    
    def __init__(
        self,
        message: str = "Произошла ошибка",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Конвертирует исключение в словарь для JSON-ответа"""
        return {
            "error": {
                "type": self.__class__.__name__,
                "message": self.message,
                "details": self.details
            }
        }


class NotFoundException(AppException):
    """Ресурс не найден (404)"""
    
    def __init__(self, resource: str, resource_id: int, extra: Optional[Dict] = None):
        details = {"resource": resource, "resource_id": resource_id}
        if extra:
            details.update(extra)
        super().__init__(
            message=f"{resource} с ID {resource_id} не найден",
            status_code=404,
            details=details
        )


class ValidationError(AppException):
    """Ошибка валидации данных (400)"""
    
    def __init__(self, message: str, field: Optional[str] = None, value: Any = None):
        details = {"field": field}
        if value is not None:
            details["value"] = value
        super().__init__(
            message=message,
            status_code=400,
            details=details
        )


class DatabaseError(AppException):
    """Ошибка базы данных (500)"""
    
    def __init__(self, message: str, original_error: Optional[str] = None):
        details = {}
        if original_error:
            details["original_error"] = original_error
        super().__init__(
            message=message,
            status_code=500,
            details=details
        )


class ConflictError(AppException):
    """Конфликт ресурсов — например, уникальный slug (409)"""
    
    def __init__(self, resource: str, field: str, value: str):
        super().__init__(
            message=f"{resource} с {field}='{value}' уже существует",
            status_code=409,
            details={"resource": resource, "field": field, "value": value}
        )


class ForbiddenError(AppException):
    """Доступ запрещён (403)"""
    
    def __init__(self, message: str = "Доступ запрещён"):
        super().__init__(
            message=message,
            status_code=403
        )