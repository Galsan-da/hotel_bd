from fastapi import Query, HTTPException, APIRouter, Body
from sqlalchemy import insert, select, func
from typing import Optional

from src.schemas.hotels import HotelAdd, HotelPATCH
from src.api.dependencies import PaginationDep
from src.models.hotels import HotelsOrm
from src.database import async_session_maker, engine
from src.repositories.hotels import HotelsRepository

# Создаем экземпляр FastAPI приложения
router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("")
async def get_hotel(
        pagination: PaginationDep,
        #id: int | None = Query(default=None, description="ID города"),
        title: str | None = Query(default=None, description="Название отеля"),
        location: str | None = Query(default=None, description="Локация отеля")
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.delete("/{hotel_id}")
async def delete_hotel(
    hotel_id: int
):
    """
    Удалить отель.

    """
    async with async_session_maker() as session:
      await HotelsRepository(session).delete(id=hotel_id)
      await session.commit()
    return {'status': 'ok'}

@router.post("")
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples={
    "1": {"summary": "Сочи", "value":{
        "title": "Отел у моря",
        "location": "Сочи, ул. У Моря, 1",
    }},
    "2": {"summary": "Дубай", "value":{
        "title": "Отель Дубай",
        "location": "Дубай, пр. Шейха, 1"
    }}
})):
    """
    Создать новый отель.
    """
    async with async_session_maker() as session:
      hotel = await HotelsRepository(session).add(hotel_data)
      await session.commit()
      return {'status': 'ok', "data": hotel}

@router.put("/{hotel_id}")
async def create_update(
    hotel_id: int,
    hotel_data: HotelAdd= Body(openapi_examples={
    "1": {"summary": "Сочи", "value":{
        "title": "Отел у моря",
        "location": "Сочи, ул. У Моря, 1",
    }},
    "2": {"summary": "Дубай", "value":{
        "title": "Отель Дубай",
        "location": "Дубай, пр. Шейха, 1"
    }}
}),
):
    """
    Полное обновление отеля.

    """
    async with async_session_maker() as session:
      await HotelsRepository(session).edit(hotel_data, id=hotel_id)
      await session.commit()
      return {'status': 'ok'}

@router.patch("/{hotel_id}")
async def create_patch(
    hotel_id: int,
    hotel_data: HotelPATCH
):
    """
    Частичное обновление отеля по ID.

    """
    async with async_session_maker() as session:
      await HotelsRepository(session).edit(hotel_data, id=hotel_id, exclude_unset=True)
      await session.commit()
      return {'status': 'ok'}

    # Если отель не найден, возвращаем ошибку
    raise HTTPException(status_code=404, detail="Отель не найден")

@router.get("/{hotel_id}")
async def get_one_hotel(hotel_id: int):
   async with async_session_maker() as session:
      hotel = await HotelsRepository(session).get_one_or_none(id=hotel_id)
      return {'status': 'ok', "data": hotel}