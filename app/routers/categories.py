from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.dependencies import get_category_repo
from app.repositories.category import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[CategoryResponse])
async def get_categories(
    repo: CategoryRepository = Depends(get_category_repo)
):
    """Получить все категории"""
    return await repo.get_all()


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int,
    repo: CategoryRepository = Depends(get_category_repo)
):
    """Получить категорию по ID"""
    category = await repo.get_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/", response_model=CategoryResponse)
async def create_category(
    category: CategoryCreate,
    repo: CategoryRepository = Depends(get_category_repo)
):
    """Создать новую категорию"""
    # Проверка уникальности slug
    existing = await repo.get_by_slug(category.slug)
    if existing:
        raise HTTPException(status_code=400, detail="Slug already exists")
    return await repo.create(category)


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category: CategoryUpdate,
    repo: CategoryRepository = Depends(get_category_repo)
):
    """Обновить категорию"""
    db_category = await repo.get_by_id(category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return await repo.update(db_category, category)


@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    repo: CategoryRepository = Depends(get_category_repo)
):
    """Удалить категорию"""
    db_category = await repo.get_by_id(category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    await repo.delete(db_category)
    return {"message": "Category deleted successfully"}