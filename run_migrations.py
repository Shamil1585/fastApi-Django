from alembic import command
from alembic.config import Config
from app.core.config import settings

def run_migrations():
    print("🚀 Запуск миграций Alembic...")
    
    alembic_cfg = Config("alembic.ini")
    
    # ВАЖНО: Используем синхронный драйвер psycopg2 для миграций!
    # Заменяем asyncpg на psycopg2 в URL
    sync_url = settings.DATABASE_URL.replace("+asyncpg", "+psycopg2")
    
    print(f"   Подключение к: {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}")
    
    # Передаем URL явно в конфиг Alembic
    alembic_cfg.set_main_option("sqlalchemy.url", sync_url)
    
    try:
        # Запускаем миграцию до последней версии (head)
        command.upgrade(alembic_cfg, "head")
        print("✅ Миграции успешно применены!")
    except Exception as e:
        print(f"❌ Ошибка при применении миграций: {e}")
        raise

if __name__ == "__main__":
    run_migrations()
