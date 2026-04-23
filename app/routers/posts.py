from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.repositories.post import PostRepository
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.dependencies import get_post_repo, get_current_user
from app.models.user import User

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[PostResponse])
async def get_posts(repo: PostRepository = Depends(get_post_repo)):
    """Получить все посты (публично)"""
    return await repo.get_all()


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, repo: PostRepository = Depends(get_post_repo)):
    """Получить пост по ID (публично)"""
    post = await repo.get_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    return post


@router.post("/", response_model=PostResponse, status_code=201)
async def create_post(
    post_: PostCreate,
    current_user: User = Depends(get_current_user),
    repo: PostRepository = Depends(get_post_repo)
):
    """Создать пост (только авторизованные)"""
    # Ставим author_id из токена
    post_.author_id = current_user.id
    return await repo.create(post_)


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_: PostUpdate,
    current_user: User = Depends(get_current_user),
    repo: PostRepository = Depends(get_post_repo)
):
    """Обновить пост (только автор)"""
    db_post = await repo.get_by_id(post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    
    # Проверка: только автор может редактировать
    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Только автор может редактировать")
    
    return await repo.update(db_post, post_)


@router.delete("/{post_id}", status_code=200)
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    repo: PostRepository = Depends(get_post_repo)
):
    """Удалить пост (только автор)"""
    db_post = await repo.get_by_id(post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    
    # Проверка: только автор может удалить
    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Только автор может удалить")
    
    await repo.delete(db_post)
    return {"message": "Пост удалён", "id": post_id}
