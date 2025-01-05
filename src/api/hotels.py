from fastapi import Query, HTTPException, APIRouter, Body
from sqlalchemy import insert, select, func
from typing import Optional

from src.schemas.hotels import Hotel, HotelPATCH
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


@router.delete("/")
async def delete_hotel(
    id: Optional[int] = Query(None),
    title: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
):
    """
    Удалить отель.

    """

    filter_params = {}
    if id is not None:
        filter_params['id'] = id
    if title is not None:
        filter_params['title'] = title
    if location is not None:
        filter_params['location'] = location

    if not filter_params:
        raise HTTPException(status_code=400, detail="Необходимо указать хотя бы один параметр фильтрации.")

    async with async_session_maker() as session:
      hotel = await HotelsRepository(session).delete(**filter_params)
      await session.commit()
    return {'status': 'ok'}

@router.post("")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
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

@router.put("/")
async def create_update(
    hotel_data: Hotel= Body(openapi_examples={
    "1": {"summary": "Сочи", "value":{
        "title": "Отел у моря",
        "location": "Сочи, ул. У Моря, 1",
    }},
    "2": {"summary": "Дубай", "value":{
        "title": "Отель Дубай",
        "location": "Дубай, пр. Шейха, 1"
    }}
}),
    id: Optional[int] = Query(None),
    title: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
):
    """
    Полное обновление отеля.

    """
    filter_params = {}
    if id is not None:
        filter_params['id'] = id
    if title is not None:
        filter_params['title'] = title
    if location is not None:
        filter_params['location'] = location

    if not filter_params:
        raise HTTPException(status_code=400, detail="Необходимо указать хотя бы один параметр фильтрации.")

    async with async_session_maker() as session:
      hotel = await HotelsRepository(session).edit(hotel_data, **filter_params)
      await session.commit()
      return {'status': 'ok', 'hotel': hotel}

@router.patch("/{hotel_id}")
def create_patch(
    hotel_id: int,
    hotel_data: HotelPATCH
):
    """
    Частичное обновление отеля по ID.

    :param hotel_id: ID отеля, который нужно обновить
    :param title: Новое название города (опционально)
    :param hotel_name: Новое название отеля (опционально)
    :return: Обновленный отель или ошибка
    """
    # Проверяем, что хотя бы одно поле для обновления указано
    if hotel_data.title is None and hotel_data.title is None:
        raise HTTPException(status_code=400, detail="Необходимо предоставить данные для обновления")

    # Ищем отель по ID
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            # Обновляем только те поля, которые переданы
            if hotel_data.title is not None:
                hotel['title'] = hotel_data.title
            if hotel_data.title is not None:
                hotel['name'] = hotel_data.title
            return hotel  # Возвращаем обновленный отель

    # Если отель не найден, возвращаем ошибку
    raise HTTPException(status_code=404, detail="Отель не найден")