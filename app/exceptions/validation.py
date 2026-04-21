from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


ERROR_TRANSLATIONS = {
    "string_too_short": lambda ctx: f"должно содержать не менее {ctx.get('min_length')} символов",
    "string_too_long": lambda ctx: f"должно содержать не более {ctx.get('max_length')} символов",
    "greater_than": lambda ctx: f"должно быть больше {ctx.get('gt')}",
    "greater_than_equal": lambda ctx: f"должно быть не меньше {ctx.get('ge')}",
    "less_than": lambda ctx: f"должно быть меньше {ctx.get('lt')}",
    "less_than_equal": lambda ctx: f"должно быть не больше {ctx.get('le')}",
    "multiple_of": lambda ctx: f"должно быть кратно {ctx.get('multiple_of')}",
    "value_error.email": lambda ctx: "должно быть валидным email-адресом",
    "value_error.url": lambda ctx: "должно быть валидным URL (начинаться с http:// или https://)",
    "value_error.uuid": lambda ctx: "должно быть валидным UUID",
    "value_error.date": lambda ctx: "должно быть валидной датой (формат: ГГГГ-ММ-ДД)",
    "value_error.datetime": lambda ctx: "должно быть валидной датой и временем",
    "missing": lambda ctx: "это поле обязательно для заполнения",
    "int_parsing": lambda ctx: "должно быть целым числом",
    "float_parsing": lambda ctx: "должно быть числом",
    "bool_parsing": lambda ctx: "должно быть true или false",
    "too_short": lambda ctx: f"должно содержать не менее {ctx.get('min_length')} элементов",
    "too_long": lambda ctx: f"должно содержать не более {ctx.get('max_length')} элементов",
    "literal_error": lambda ctx: "должно быть одним из допустимых значений",
    "enum": lambda ctx: "должно быть одним из допустимых значений",
    "url_parsing": lambda ctx: "неверный формат URL",
    "url_scheme": lambda ctx: "URL должен начинаться с http:// или https://",
    "decimal_parsing": lambda ctx: "должно быть десятичным числом",
}

FIELD_NAMES = {
    "title": "заголовок поста", "text": "текст поста", "pub_date": "дата публикации",
    "is_published": "статус публикации", "image": "ссылка на изображение", "rating": "рейтинг",
    "username": "имя пользователя", "email": "адрес электронной почты", "password": "пароль",
    "is_active": "статус аккаунта", "author_id": "ID автора", "location_id": "ID местоположения",
    "category_id": "ID категории", "post_id": "ID поста", "user_id": "ID пользователя",
    "id": "идентификатор", "created_at": "дата создания", "updated_at": "дата обновления",
}

CUSTOM_ERROR_PREFIX = "Value error,"


def _get_field_name(loc: list) -> str:
    field_key = loc[-1] if len(loc) > 1 else (loc[0] if loc else "поле")
    return FIELD_NAMES.get(field_key, field_key)


def _format_error_message(error: dict) -> str:
    error_type = error.get("type", "unknown")
    ctx = error.get("ctx", {}) or {}
    loc = error.get("loc", [])
    msg = error.get("msg", "Неизвестная ошибка")
    field_name = _get_field_name(loc)
    
    if error_type in ERROR_TRANSLATIONS:
        description = ERROR_TRANSLATIONS[error_type](ctx)
        return f"Ошибка: {field_name} {description}"
    
    if CUSTOM_ERROR_PREFIX in msg:
        custom_msg = msg.split(CUSTOM_ERROR_PREFIX, 1)[1].strip()
        return f"Ошибка: {custom_msg}"
    
    clean_msg = msg.split(":")[-1].strip() if ":" in msg else msg
    return f"Ошибка: {field_name} — {clean_msg}"


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = exc.errors()
    if not errors:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": "Ошибка: неверные данные в запросе"}
        )
    first_error = errors[0]
    message = _format_error_message(first_error)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": message}
    )


def register_validation_handler(app):
    app.add_exception_handler(RequestValidationError, validation_error_handler)
