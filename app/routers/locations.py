from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.dependencies import get_location_repo
from app.repositories.location import LocationRepository
from app.schemas.location import LocationCreate, LocationUpdate, LocationResponse

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get("/", response_model=List[LocationResponse])
async def get_locations(
    repo: LocationRepository = Depends(get_location_repo)
):
    """Получить все местоположения"""
    return await repo.get_all()


@router.get("/{location_id}", response_model=LocationResponse)
async def get_location(
    location_id: int,
    repo: LocationRepository = Depends(get_location_repo)
):
    """Получить местоположение по ID"""
    location = await repo.get_by_id(location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.post("/", response_model=LocationResponse)
async def create_location(
    location: LocationCreate,
    repo: LocationRepository = Depends(get_location_repo)
):
    """Создать новое местоположение"""
    return await repo.create(location)


@router.put("/{location_id}", response_model=LocationResponse)
async def update_location(
    location_id: int,
    location: LocationUpdate,
    repo: LocationRepository = Depends(get_location_repo)
):
    """Обновить местоположение"""
    db_location = await repo.get_by_id(location_id)
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    return await repo.update(db_location, location)


@router.delete("/{location_id}")
async def delete_location(
    location_id: int,
    repo: LocationRepository = Depends(get_location_repo)
):
    """Удалить местоположение"""
    db_location = await repo.get_by_id(location_id)
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    await repo.delete(db_location)
    return {"message": "Location deleted successfully"}