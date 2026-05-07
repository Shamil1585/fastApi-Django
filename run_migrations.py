from alembic import command
from alembic.config import Config
import os

def run_migrations():
    print("🚀 Запуск миграций Alembic...")
    
    alembic_cfg = Config("alembic.ini")
    
    # ЖЕСТКАЯ КОНФИГУРАЦИЯ ДЛЯ DOCKER
    # Мы игнорируем любые переменные окружения и задаем данные явно.
    # В docker-compose.yml сервис базы данных называется 'db'.
    DB_USER = "shamil"
    DB_PASSWORD = "Shamil1234"
    DB_HOST = "db"        # Имя сервиса в docker-compose.yml
    DB_PORT = "5432"
    DB_NAME = "blog_db"
    
    print(f"   Подключение к: {DB_HOST}:{DB_PORT}/{DB_NAME}")
    
    # Формируем строку подключения для psycopg2 (синхронный драйвер)
    sync_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # Передаем URL явно в конфиг Alembic, перезаписывая всё остальное
    alembic_cfg.set_main_option("sqlalchemy.url", sync_url)
    
    try:
        command.upgrade(alembic_cfg, "head")
        print("✅ Миграции успешно применены!")
    except Exception as e:
        print(f"❌ Ошибка при применении миграций: {e}")
        raise

if __name__ == "__main__":
    run_migrations()