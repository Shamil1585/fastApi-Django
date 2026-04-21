from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.domain.use_cases.post import PostUseCase
from app.exceptions import NotFoundException, ValidationError, DatabaseError
from app.dependencies import get_post_repo, get_current_user
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.models.user import User


def get_post_use_case(repo=Depends(get_post_repo)) -> PostUseCase:
    """Создание экземпляра PostUseCase"""
    return PostUseCase(repo)


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[PostResponse])
async def get_posts(use_case: PostUseCase = Depends(get_post_use_case)):
    """Публично: получить все посты"""
    return await use_case.get_all_posts()


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    use_case: PostUseCase = Depends(get_post_use_case)
):
    """Публично: получить пост по ID"""
    try:
        return await use_case.get_post_by_id(post_id)
    except NotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "not_found",
                "resource": e.resource,
                "resource_id": e.resource_id,
                "message": e.message
            }
        )


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user),
    use_case: PostUseCase = Depends(get_post_use_case)
):
    """Только авторизованные: создать пост"""
    try:
        return await use_case.create_post(post_data, user_id=current_user.id)
    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "validation_error",
                "field": e.field,
                "message": e.message
            }
        )
    except DatabaseError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "database_error",
                "message": e.message
            }
        )


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    current_user: User = Depends(get_current_user),
    use_case: PostUseCase = Depends(get_post_use_case)
):
    """Только автор: обновить пост"""
    try:
        return await use_case.update_post(
            post_id=post_id,
            post_data=post_data,
            user_id=current_user.id
        )
    except NotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "not_found",
                "resource": e.resource,
                "resource_id": e.resource_id
            }
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=403,
            detail={
                "error": "access_denied",
                "message": e.message,
                "user_id": e.user_id,
                "post_id": e.post_id
            }
        )


@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    use_case: PostUseCase = Depends(get_post_use_case)
):
    """Только автор: удалить пост"""
    try:
        return await use_case.delete_post(
            post_id=post_id,
            user_id=current_user.id
        )
    except NotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "not_found",
                "resource": e.resource,
                "resource_id": e.resource_id
            }
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=403,
            detail={
                "error": "access_denied",
                "message": e.message,
                "user_id": e.user_id,
                "post_id": e.post_id
            }
        )
