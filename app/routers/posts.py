from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from app.dependencies import get_post_repo
from app.repositories.post import PostRepository
from app.domain.use_cases.post import PostUseCase
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.exceptions import AppException, NotFoundException, ValidationError, DatabaseError, ConflictError

router = APIRouter(prefix="/posts", tags=["Posts"])


# === Dependency для создания Use Case ===
def get_post_use_case(repo: PostRepository = Depends(get_post_repo)) -> PostUseCase:
    """Создаёт PostUseCase с внедрённым репозиторием"""
    return PostUseCase(post_repo=repo)


# === Helper для конвертации исключений в HTTPException ===
def handle_app_exception(exc: AppException) -> HTTPException:
    """Конвертирует кастомное исключение в HTTPException с правильным статусом"""
    return HTTPException(
        status_code=exc.status_code,
        detail=exc.to_dict()
    )


@router.get("/", response_model=List[PostResponse])
async def get_posts(
    use_case: PostUseCase = Depends(get_post_use_case)
):
    """Получить все посты"""
    try:
        return await use_case.get_all_posts()
    except DatabaseError as e:
        raise handle_app_exception(e)
    except AppException as e:
        raise handle_app_exception(e)


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    use_case: PostUseCase = Depends(get_post_use_case)
):
    """Получить пост по ID"""
    try:
        return await use_case.get_post_by_id(post_id)
    except NotFoundException as e:
        raise handle_app_exception(e)
    except DatabaseError as e:
        raise handle_app_exception(e)
    except AppException as e:
        raise handle_app_exception(e)


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    use_case: PostUseCase = Depends(get_post_use_case)
):
    """Создать новый пост"""
    try:
        return await use_case.create_post(post)
    except ValidationError as e:
        raise handle_app_exception(e)
    except ConflictError as e:
        raise handle_app_exception(e)
    except DatabaseError as e:
        raise handle_app_exception(e)
    except AppException as e:
        raise handle_app_exception(e)


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post: PostUpdate,
    use_case: PostUseCase = Depends(get_post_use_case)
):
    """Обновить пост"""
    try:
        return await use_case.update_post(post_id, post)
    except NotFoundException as e:
        raise handle_app_exception(e)
    except ValidationError as e:
        raise handle_app_exception(e)
    except DatabaseError as e:
        raise handle_app_exception(e)
    except AppException as e:
        raise handle_app_exception(e)


@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(
    post_id: int,
    use_case: PostUseCase = Depends(get_post_use_case)
):
    """Удалить пост"""
    try:
        return await use_case.delete_post(post_id)
    except NotFoundException as e:
        raise handle_app_exception(e)
    except DatabaseError as e:
        raise handle_app_exception(e)
    except AppException as e:
        raise handle_app_exception(e)


@router.get("/author/{author_id}", response_model=List[PostResponse])
async def get_posts_by_author(
    author_id: int,
    use_case: PostUseCase = Depends(get_post_use_case)
):
    """Получить посты автора"""
    try:
        return await use_case.get_posts_by_author(author_id)
    except ValidationError as e:
        raise handle_app_exception(e)
    except DatabaseError as e:
        raise handle_app_exception(e)
    except AppException as e:
        raise handle_app_exception(e)