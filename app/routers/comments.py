from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.dependencies import get_comment_repo
from app.repositories.comment import CommentRepository
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/", response_model=List[CommentResponse])
async def get_comments(
    repo: CommentRepository = Depends(get_comment_repo)
):
    """Получить все комментарии"""
    return await repo.get_all()


@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment(
    comment_id: int,
    repo: CommentRepository = Depends(get_comment_repo)
):
    """Получить комментарий по ID"""
    comment = await repo.get_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.post("/", response_model=CommentResponse)
async def create_comment(
    comment: CommentCreate,
    repo: CommentRepository = Depends(get_comment_repo)
):
    """Создать новый комментарий"""
    return await repo.create(comment)


@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: int,
    comment: CommentUpdate,
    repo: CommentRepository = Depends(get_comment_repo)
):
    """Обновить комментарий"""
    db_comment = await repo.get_by_id(comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return await repo.update(db_comment, comment)


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    repo: CommentRepository = Depends(get_comment_repo)
):
    """Удалить комментарий"""
    db_comment = await repo.get_by_id(comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    await repo.delete(db_comment)
    return {"message": "Comment deleted successfully"}