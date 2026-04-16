from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.models.user import User
from app.repositories.base import BaseRepository
from app.core.security import get_password_hash, verify_password


class UserRepository(BaseRepository[User]):
    
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)
    
    async def get_by_username(self, username: str) -> User | None:
        try:
            result = await self.session.execute(
                select(User).where(User.username == username)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError:
            return None
    
    async def get_by_email(self, email: str) -> User | None:
        try:
            result = await self.session.execute(
                select(User).where(User.email == email)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError:
            return None
    
    async def create_user(self, username: str, email: str, password: str) -> User:
        try:
            hashed_password = get_password_hash(password)
            db_user = User(
                username=username,
                email=email,
                hashed_password=hashed_password
            )
            self.session.add(db_user)
            await self.session.commit()
            await self.session.refresh(db_user)
            return db_user
        except IntegrityError:
            await self.session.rollback()
            raise
        except SQLAlchemyError:
            await self.session.rollback()
            raise
    
    async def authenticate(self, username: str, password: str) -> User | None:
        """Аутентификация: проверка логина и пароля"""
        user = await self.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None
        return user