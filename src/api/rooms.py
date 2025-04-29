# Файл: routers/rooms.py
from fastapi import APIRouter, HTTPException, Body


from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest
from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)

@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
    hotel_id: int,
    room_id: int
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(
            id=room_id,
            hotel_id=hotel_id
        )

@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()
    return {"status": "OK", "data": room}

@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(hotel_id: int, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}

@router.patch("/{hotel_id}/rooms/{room_id}")
async def partial_update_room(hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        room = await RoomsRepository(session).edit(_room_data, id=room_id, hotel_id=hotel_id, exclude_unset=True)
        if not room:
            raise HTTPException(status_code=404, detail="Номер не найден")
        await session.commit()
        return room

@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        deleted = await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Номер не найден")
        await session.commit()