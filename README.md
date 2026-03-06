# Описание
API для блога, мигрированное с Django на FastAPI.

## Технологии
- FastAPI
- SQLAlchemy (Async)
- Pydantic
- SQLite

## Установка

```bash
# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Запуск сервера
uvicorn main:app --reload