# Импорт необходимых модулей
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse

# Создание роутера с префиксом и тегом для документации
router = APIRouter(prefix="/categories", tags=["Categories"])


# GET запрос - получить все категории
@router.get("/", response_model=List[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category))
    return result.scalars().all()


# GET запрос - получить одну категорию по ID
@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return category


# POST запрос - создать новую категорию
@router.post("/", response_model=CategoryResponse)
async def create_category(
    category: CategoryCreate,
    db: AsyncSession = Depends(get_db)
):
    new_category = Category(**category.model_dump())
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category


# PUT запрос - обновить категорию
@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Category).where(Category.id == category_id))
    db_category = result.scalar_one_or_none()
    
    if not db_category:
        raise