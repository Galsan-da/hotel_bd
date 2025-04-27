# Файл: routers/rooms.py
from fastapi import APIRouter, HTTPException, Body, Query, status
from sqlalchemy.exc import IntegrityError
from typing import Optional

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomResponse, RoomUpdate
from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/rooms", tags=["Номера"])


@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(room_id: int):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Номер не найден")
        return room

@router.get("", response_model=list[RoomResponse])
async def get_rooms(
    pagination: PaginationDep,
    hotel_id: Optional[int] = Query(None),
    price_min: Optional[int] = Query(None),
    price_max: Optional[int] = Query(None)
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            hotel_id=hotel_id,
            price_min=price_min,
            price_max=price_max,
            limit=pagination.per_page,
            offset=pagination.per_page * (pagination.page - 1)
        )

@router.put("/{room_id}", response_model=RoomResponse)
async def update_room(room_id: int, room_data: RoomAdd):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).edit(room_data, id=room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Номер не найден")
        await session.commit()
        return room

@router.patch("/{room_id}", response_model=RoomResponse)
async def partial_update_room(room_id: int, room_data: RoomUpdate):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).edit(room_data, id=room_id, exclude_unset=True)
        if not room:
            raise HTTPException(status_code=404, detail="Номер не найден")
        await session.commit()
        return room

@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(room_id: int):
    async with async_session_maker() as session:
        deleted = await RoomsRepository(session).delete(id=room_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Номер не найден")
        await session.commit()