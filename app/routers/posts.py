# Импорт необходимых модулей
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate, PostResponse

router = APIRouter(prefix="/posts", tags=["Posts"])


# GET все посты
@router.get("/", response_model=List[PostResponse])
async def get_posts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post))
    return result.scalars().all()


# GET один пост по ID
@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return post


# POST создать пост
@router.post("/", response_model=PostResponse)
async def create_post(
    post: PostCreate,
    db: AsyncSession = Depends(get_db)
):
    new_post = Post(**post.model_dump())
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post


# PUT обновить пост
@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post: PostUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Post).where(Post.id == post_id))
    db_post = result.scalar_one_or_none()
    
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    update_data = post.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_post, field, value)
    
    await db.commit()
    await db.refresh(db_post)
    return db_post


# DELETE удалить пост
@router.delete("/{post_id}")
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    await db.delete(post)
    await db.commit()
    
    return {"message": "Post deleted successfully"}