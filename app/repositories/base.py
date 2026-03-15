from typing import TypeVar, Generic, List, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Базовый репозиторий с общими методами для всех сущностей"""
    
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session
    
    async def get_by_id(self, id: int) -> Optional[ModelType]:
        """Получить запись по ID"""
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self) -> List[ModelType]:
        """Получить все записи"""
        result = await self.session.execute(select(self.model))
        return result.scalars().all()
    
    async def create(self, obj_create) -> ModelType:
        """Создать новую запись"""
        db_obj = self.model(**obj_create.model_dump())
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj
    
    async def update(self, db_obj: ModelType, obj_update) -> ModelType:
        """Обновить запись"""
        update_data = obj_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj
    
    async def delete(self, db_obj: ModelType) -> bool:
        """Удалить запись"""
        await self.session.delete(db_obj)
        await self.session.commit()
        return True