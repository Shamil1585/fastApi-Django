from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.dependencies import get_user_repo
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserResponse])
async def get_users(
    repo: UserRepository = Depends(get_user_repo)
):
    """Получить всех пользователей"""
    return await repo.get_all()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    repo: UserRepository = Depends(get_user_repo)
):
    """Получить пользователя по ID"""
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    repo: UserRepository = Depends(get_user_repo)
):
    """Создать нового пользователя"""
    # Проверка уникальности email
    existing = await repo.get_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await repo.create(user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user: UserUpdate,
    repo: UserRepository = Depends(get_user_repo)
):
    """Обновить пользователя"""
    db_user = await repo.get_by_id(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return await repo.update(db_user, user)


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    repo: UserRepository = Depends(get_user_repo)
):
    """Удалить пользователя"""
    db_user = await repo.get_by_id(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    await repo.delete(db_user)
    return {"message": "User deleted successfully"}