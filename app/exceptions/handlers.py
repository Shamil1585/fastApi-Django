from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.base import AppException, NotFoundException, ValidationError, DatabaseError, ConflictError


async def app_exception_handler(request: Request, exc: AppException):
    """Обработчик всех исключений приложения"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.to_dict()}
    )


async def not_found_handler(request: Request, exc: NotFoundException):
    """Обработчик 404 ошибок"""
    return JSONResponse(
        status_code=404,
        content={"error": {"message": str(exc)}}
    )


async def validation_error_handler(request: Request, exc: ValidationError):
    """Обработчик 400 ошибок"""
    return JSONResponse(
        status_code=400,
        content={"error": {"message": str(exc)}}
    )


async def database_error_handler(request: Request, exc: DatabaseError):
    """Обработчик 500 ошибок"""
    return JSONResponse(
        status_code=500,
        content={"error": {"message": str(exc)}}
    )


async def conflict_error_handler(request: Request, exc: ConflictError):
    """Обработчик 409 ошибок"""
    return JSONResponse(
        status_code=409,
        content={"error": {"message": str(exc)}}
    )


def register_exception_handlers(app):
    """Регистрация всех обработчиков в FastAPI"""
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(NotFoundException, not_found_handler)
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(DatabaseError, database_error_handler)
    app.add_exception_handler(ConflictError, conflict_error_handler)
