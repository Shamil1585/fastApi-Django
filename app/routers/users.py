from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.dependencies import get_user_repo, get_current_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserResponse])
async def get_users(repo: UserRepository = Depends(get_user_repo)):
    """Получить всех пользователей (публично)"""
    return await repo.get_all()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, repo: UserRepository = Depends(get_user_repo)):
    """Получить пользователя по ID (публично)"""
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_: UserUpdate,
    current_user: User = Depends(get_current_user),
    repo: UserRepository = Depends(get_user_repo)
):
    """Обновить пользователя (только авторизованные)"""
    db_user = await repo.get_by_id(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    return await repo.update(db_user, user_)


@router.delete("/{user_id}", status_code=200)
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    repo: UserRepository = Depends(get_user_repo)
):
    """Удалить пользователя (только авторизованные)"""
    db_user = await repo.get_by_id(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    await repo.delete(db_user)
    return {"message": "Пользователь удалён", "id": user_id}
