from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.repositories.location import LocationRepository
from app.schemas.location import LocationCreate, LocationUpdate, LocationResponse
from app.dependencies import get_location_repo, get_current_user
from app.models.user import User

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get("/", response_model=List[LocationResponse])
async def get_locations(repo: LocationRepository = Depends(get_location_repo)):
    """Получить все локации (публично)"""
    return await repo.get_all()


@router.get("/{location_id}", response_model=LocationResponse)
async def get_location(location_id: int, repo: LocationRepository = Depends(get_location_repo)):
    """Получить локацию по ID (публично)"""
    location = await repo.get_by_id(location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Локация не найдена")
    return location


@router.post("/", response_model=LocationResponse, status_code=201)
async def create_location(
    location_: LocationCreate,
    current_user: User = Depends(get_current_user),
    repo: LocationRepository = Depends(get_location_repo)
):
    """Создать локацию (только авторизованные)"""
    return await repo.create(location_)


@router.put("/{location_id}", response_model=LocationResponse)
async def update_location(
    location_id: int,
    location_: LocationUpdate,
    current_user: User = Depends(get_current_user),
    repo: LocationRepository = Depends(get_location_repo)
):
    """Обновить локацию (только авторизованные)"""
    db_location = await repo.get_by_id(location_id)
    if not db_location:
        raise HTTPException(status_code=404, detail="Локация не найдена")
    
    return await repo.update(db_location, location_)


@router.delete("/{location_id}", status_code=200)
async def delete_location(
    location_id: int,
    current_user: User = Depends(get_current_user),
    repo: LocationRepository = Depends(get_location_repo)
):
    """Удалить локацию (только авторизованные)"""
    db_location = await repo.get_by_id(location_id)
    if not db_location:
        raise HTTPException(status_code=404, detail="Локация не найдена")
    
    await repo.delete(db_location)
    return {"message": "Локация удалена", "id": location_id}
