# Импорт необходимых модулей
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models.location import Location
from app.schemas.location import LocationCreate, LocationUpdate, LocationResponse

# Создание роутера с префиксом и тегом для документации
router = APIRouter(prefix="/locations", tags=["Locations"])


# GET запрос - получить все местоположения
@router.get("/", response_model=List[LocationResponse])
async def get_locations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Location))
    return result.scalars().all()


# GET запрос - получить одно местоположение по ID
@router.get("/{location_id}", response_model=LocationResponse)
async def get_location(location_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Location).where(Location.id == location_id))
    location = result.scalar_one_or_none()
    
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    return location


# POST запрос - создать новое местоположение
@router.post("/", response_model=LocationResponse)
async def create_location(
    location: LocationCreate,
    db: AsyncSession = Depends(get_db)
):
    new_location = Location(**location.model_dump())
    db.add(new_location)
    await db.commit()
    await db.refresh(new_location)
    return new_location


# PUT запрос - обновить местоположение
@router.put("/{location_id}", response_model=LocationResponse)
async def update_location(
    location_id: int,
    location: LocationUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Location).where(Location.id == location_id))
    db_location = result.scalar_one_or_none()
    
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    update_data = location.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_location, field, value)
    
    await db.commit()
    await db.refresh(db_location)
    return db_location


# DELETE запрос - удалить местоположение
@router.delete("/{location_id}")
async def delete_location(location_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Location).where(Location.id == location_id))
    location = result.scalar_one_or_none()
    
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    await db.delete(location)
    await db.commit()
    
    return {"message": "Location deleted successfully"}