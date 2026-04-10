from typing import List
from app.repositories.post import PostRepository
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.exceptions import NotFoundException, ValidationError


class PostUseCase:
    """Бизнес-логика для постов"""
    
    def __init__(self, post_repo: PostRepository):
        self.post_repo = post_repo
    
    async def get_all_posts(self) -> List[PostResponse]:
        """Получить все посты"""
        posts = await self.post_repo.get_all()
        return [PostResponse.model_validate(post) for post in posts]
    
    async def get_post_by_id(self, post_id: int) -> PostResponse:
        """Получить пост по ID"""
        post = await self.post_repo.get_by_id(post_id)
        
        if not post:
            raise NotFoundException(resource="Post", resource_id=post_id)
        
        return PostResponse.model_validate(post)
    
    async def create_post(self, post_data: PostCreate) -> PostResponse:  # ← : после post_data
        """Создать пост"""
        # Бизнес-валидация
        if not post_data.title.strip():
            raise ValidationError(message="Заголовок не может быть пустым", field="title")
        
        if len(post_data.text.strip()) < 10:
            raise ValidationError(message="Текст должен содержать минимум 10 символов", field="text")
        
        post = await self.post_repo.create(post_data)
        return PostResponse.model_validate(post)
    
    async def update_post(self, post_id: int, post_data: PostUpdate) -> PostResponse:  # ← : после post_data
        """Обновить пост"""
        existing = await self.post_repo.get_by_id(post_id)
        
        if not existing:
            raise NotFoundException(resource="Post", resource_id=post_id)
        
        if post_data.title is not None and not post_data.title.strip():
            raise ValidationError(message="Заголовок не может быть пустым", field="title")
        
        updated = await self.post_repo.update(existing, post_data)
        return PostResponse.model_validate(updated)
    
    async def delete_post(self, post_id: int) -> dict:
        """Удалить пост"""
        post = await self.post_repo.get_by_id(post_id)
        
        if not post:
            raise NotFoundException(resource="Post", resource_id=post_id)
        
        await self.post_repo.delete(post)
        return {"message": "Post deleted", "id": post_id}