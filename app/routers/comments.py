from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.repositories.comment import CommentRepository
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from app.dependencies import get_comment_repo, get_current_user
from app.models.user import User

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/", response_model=List[CommentResponse])
async def get_comments(repo: CommentRepository = Depends(get_comment_repo)):
    """Получить все комментарии (публично)"""
    return await repo.get_all()


@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment(comment_id: int, repo: CommentRepository = Depends(get_comment_repo)):
    """Получить комментарий по ID (публично)"""
    comment = await repo.get_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    return comment


@router.post("/", response_model=CommentResponse, status_code=201)
async def create_comment(
    comment_: CommentCreate,
    current_user: User = Depends(get_current_user),
    repo: CommentRepository = Depends(get_comment_repo)
):
    """Создать комментарий (только авторизованные)"""
    comment_.author_id = current_user.id
    return await repo.create(comment_)


@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: int,
    comment_: CommentUpdate,
    current_user: User = Depends(get_current_user),
    repo: CommentRepository = Depends(get_comment_repo)
):
    """Обновить комментарий (только автор)"""
    db_comment = await repo.get_by_id(comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    
    if db_comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Только автор может редактировать")
    
    return await repo.update(db_comment, comment_)


@router.delete("/{comment_id}", status_code=200)
async def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    repo: CommentRepository = Depends(get_comment_repo)
):
    """Удалить комментарий (только автор)"""
    db_comment = await repo.get_by_id(comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    
    if db_comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Только автор может удалить")
    
    await repo.delete(db_comment)
    return {"message": "Комментарий удалён", "id": comment_id}
