from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.dependencies import get_post_repo
from app.repositories.post import PostRepository
from app.schemas.post import PostCreate, PostUpdate, PostResponse

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[PostResponse])
async def get_posts(
    repo: PostRepository = Depends(get_post_repo)
):
    """Получить все посты"""
    return await repo.get_all()


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    repo: PostRepository = Depends(get_post_repo)
):
    """Получить пост по ID"""
    post = await repo.get_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/", response_model=PostResponse)
async def create_post(
    post: PostCreate,
    repo: PostRepository = Depends(get_post_repo)
):
    """Создать новый пост"""
    return await repo.create(post)


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post: PostUpdate,
    repo: PostRepository = Depends(get_post_repo)
):
    """Обновить пост"""
    db_post = await repo.get_by_id(post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return await repo.update(db_post, post)


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    repo: PostRepository = Depends(get_post_repo)
):
    """Удалить пост"""
    db_post = await repo.get_by_id(post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    await repo.delete(db_post)
    return {"message": "Post deleted successfully"}