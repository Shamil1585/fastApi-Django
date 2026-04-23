from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.repositories.category import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.dependencies import get_category_repo, get_current_user
from app.models.user import User

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[CategoryResponse])
async def get_categories(repo: CategoryRepository = Depends(get_category_repo)):
    """Получить все категории (публично)"""
    return await repo.get_all()


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, repo: CategoryRepository = Depends(get_category_repo)):
    """Получить категорию по ID (публично)"""
    category = await repo.get_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category


@router.post("/", response_model=CategoryResponse, status_code=201)
async def create_category(
    category_: CategoryCreate,
    current_user: User = Depends(get_current_user),
    repo: CategoryRepository = Depends(get_category_repo)
):
    """Создать категорию (только авторизованные)"""
    return await repo.create(category_)


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category_: CategoryUpdate,
    current_user: User = Depends(get_current_user),
    repo: CategoryRepository = Depends(get_category_repo)
):
    """Обновить категорию (только авторизованные)"""
    db_category = await repo.get_by_id(category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    return await repo.update(db_category, category_)


@router.delete("/{category_id}", status_code=200)
async def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    repo: CategoryRepository = Depends(get_category_repo)
):
    """Удалить категорию (только авторизованные)"""
    db_category = await repo.get_by_id(category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    await repo.delete(db_category)
    return {"message": "Категория удалена", "id": category_id}
