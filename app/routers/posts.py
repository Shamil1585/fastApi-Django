from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.dependencies import get_post_repo, get_current_user
from app.repositories.post import PostRepository
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.models.user import User

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[PostResponse])
async def get_posts(repo: PostRepository = Depends(get_post_repo)):
    """Публично: получить все посты"""
    return await repo.get_all()


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    repo: PostRepository = Depends(get_post_repo)
):
    """Публично: получить пост по ID"""
    post = await repo.get_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    repo: PostRepository = Depends(get_post_repo),
    current_user: User = Depends(get_current_user)
):
    """Только авторизованные: создать пост"""
    post_data.author_id = current_user.id
    return await repo.create(post_data)


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    repo: PostRepository = Depends(get_post_repo),
    current_user: User = Depends(get_current_user)
):
    """Только автор: обновить пост"""
    db_post = await repo.get_by_id(post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail={"message": "Только автор может редактировать"})
    return await repo.update(db_post, post_data)


@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(
    post_id: int,
    repo: PostRepository = Depends(get_post_repo),
    current_user: User = Depends(get_current_user)
):
    """Только автор: удалить пост"""
    db_post = await repo.get_by_id(post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail={"message": "Только автор может удалять"})
    await repo.delete(db_post)
    return {"message": "Post deleted", "post_id": post_id}
