from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.core.security import create_access_token, create_refresh_token, verify_token
from app.core.config import settings
from app.dependencies import get_user_repo, get_current_user
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserResponse, Token
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    repo: UserRepository = Depends(get_user_repo)
):
    """Регистрация нового пользователя"""
    if await repo.get_by_username(user_data.username):
        raise HTTPException(status_code=400, detail={"message": "Username занят"})
    
    if await repo.get_by_email(user_data.email):
        raise HTTPException(status_code=400, detail={"message": "Email занят"})
    
    try:
        user = await repo.create_user(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password
        )
        return UserResponse.model_validate(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail={"message": "Ошибка регистрации", "error": str(e)})


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    repo: UserRepository = Depends(get_user_repo)
):
    """Вход: получение токенов"""
    user = await repo.authenticate(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Неверный логин или пароль"},
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access = create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh = create_refresh_token(
        data={"sub": user.username, "user_id": user.id}
    )
    
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}


@router.post("/refresh", response_model=Token)
async def refresh_token_endpoint(
    refresh_token_data: dict,
    repo: UserRepository = Depends(get_user_repo)
):
    """Обновление access токена"""
    token = refresh_token_data.get("refresh_token")
    if not token:
        raise HTTPException(status_code=400, detail={"message": "Нет refresh токена"})
    
    payload = verify_token(token, token_type="refresh")
    if not payload:
        raise HTTPException(status_code=401, detail={"message": "Неверный refresh токен"})
    
    user = await repo.get_by_username(payload.get("sub"))
    if not user:
        raise HTTPException(status_code=404, detail={"message": "Пользователь не найден"})
    
    new_access = create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    new_refresh = create_refresh_token(
        data={"sub": user.username, "user_id": user.id}
    )
    
    return {"access_token": new_access, "refresh_token": new_refresh, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user)
):
    """Получить информацию о текущем пользователе"""
    return current_user
