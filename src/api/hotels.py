from fastapi import Query, HTTPException, APIRouter, Body
from sqlalchemy import insert, select
#from sqlalchemy.orm import Session

from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.models.hotels import HotelsOrm
from src.database import async_session_maker, engine

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
        query = select(HotelsOrm)
        #if id:
            #query = query.filter_by(id=id)
        if title:
            query = query.filter(HotelsOrm.title.ilike(f"%{title}%"))
        if location:
            query = query.filter(HotelsOrm.location.ilike(f"%{location}%"))
        query = (
            query
            .filter_by(id=id, title=title)
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels

@router.delete("/{hotels_id}")
def delete_hotel(hotels_id: int):
    """
    Удалить отель по ID.

    :param hotels_id: ID отеля, который нужно удалить
    :return: Статус операции
    """
    global hotels
    hotels = [hotel for hotel in hotels if hotels_id != hotel['id']]
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

    :param title: Название города
    :param name: Название отеля
    :return: Статус операции
    """
    async with async_session_maker() as session:
      add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
      print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds":True}))
      await session.execute(add_hotel_stmt)
      await session.commit()

    return {'status': 'ok'}

@router.put("/{hotel_id}")
def create_update(
    hotel_id: int,
    hotel_data: Hotel
):
    """
    Полное обновление отеля по ID.

    :param hotel_id: ID отеля, который нужно обновить
    :param title: Новое название города (опционально)
    :param hotel_name: Новое название отеля (опционально)
    :return: Сообщение об успешном обновлении или ошибка
    """
    global hotels
    # Ищем отель по ID
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if hotel_data.title is not None:
                hotel['title'] = hotel_data.title
            if hotel_data.title is not None:
                hotel['name'] = hotel_data.title
            return {"message": "Обновление прошло успешно", "hotel": hotel}  # Возвращаем обновленный отель

    # Если отель не найден, возвращаем ошибку
    raise HTTPException(status_code=404, detail="Отель не найден")

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