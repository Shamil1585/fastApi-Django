# Импорт необходимых модулей
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse

router = APIRouter(prefix="/comments", tags=["Comments"])


# GET все комментарии
@router.get("/", response_model=List[CommentResponse])
async def get_comments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Comment))
    return result.scalars().all()


# GET один комментарий по ID
@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    return comment


# POST создать комментарий
@router.post("/", response_model=CommentResponse)
async def create_comment(
    comment: CommentCreate,
    db: AsyncSession = Depends(get_db)
):
    new_comment = Comment(**comment.model_dump())
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return new_comment


# PUT обновить комментарий
@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: int,
    comment: CommentUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    db_comment = result.scalar_one_or_none()
    
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    update_data = comment.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_comment, field, value)
    
    await db.commit()
    await db.refresh(db_comment)
    return db_comment


# DELETE удалить комментарий
@router.delete("/{comment_id}")
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    await db.delete(comment)
    await db.commit()
    
    return {"message": "Comment deleted successfully"}