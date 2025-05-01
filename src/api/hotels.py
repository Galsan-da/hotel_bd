from fastapi import Query, HTTPException, APIRouter, Body
from sqlalchemy.exc import IntegrityError

from src.schemas.hotels import HotelAdd, HotelPATCH
from src.api.dependencies import PaginationDep, DBDep


# Создаем экземпляр FastAPI приложения
router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("")
async def get_hotel(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(default=None, description="Название отеля"),
        location: str | None = Query(default=None, description="Локация отеля")
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router.delete("/{hotel_id}")
async def delete_hotel(
    hotel_id: int,
    db: DBDep
):
    """
    Удалить отель.

    """
    deleted = await db.hotels.delete(id=hotel_id)
    if not deleted:
      raise HTTPException(status_code=404, detail="Отель не найден")
    await db.commit()
    return {'status': 'ok'}

@router.post("")
async def create_hotel(
   db: DBDep,
   hotel_data: HotelAdd = Body(openapi_examples={
    "1": {"summary": "Сочи", "value":{
        "title": "Отел у моря",
        "location": "Сочи, ул. У Моря, 1",
    }},
    "2": {"summary": "Дубай", "value":{
        "title": "Отель Дубай",
        "location": "Дубай, пр. Шейха, 1"
    }}})
):
    """
    Создать новый отель.
    """
    try:
        hotel = await db.hotels.add(hotel_data)
        await db.commit()
        return {'status': 'ok', "data": hotel}
    except IntegrityError:
        await db.session.rollback()
        raise HTTPException(status_code=400, detail="Отель с такими данными уже существует")

@router.put("/{hotel_id}")
async def create_update(
    hotel_id: int,
    db: DBDep,
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
    try:
        hotel = await db.hotels.edit(hotel_data, id=hotel_id)
        if not hotel:
            raise HTTPException(status_code=404, detail="Отель не найден")
        await db.commit()
        return {'status': 'ok', "data": hotel}
    except IntegrityError:
        await db.session.rollback()
        raise HTTPException(status_code=400, detail="Ошибка целостности данных")

@router.patch("/{hotel_id}")
async def create_patch(
    hotel_id: int,
    db: DBDep,
    hotel_data: HotelPATCH
):
    """
    Частичное обновление отеля по ID.

    """
    hotel = await db.hotels.edit(hotel_data, id=hotel_id, exclude_unset=True)
    if not hotel:
        raise HTTPException(status_code=404, detail="Отель не найден")
    await db.commit()
    return {'status': 'ok', "data": hotel}

@router.get("/{hotel_id}")
async def get_one_hotel(
    hotel_id: int,
    db: DBDep
):
   hotel = await db.hotels.get_one_or_none(id=hotel_id)
   if not hotel:
        raise HTTPException(status_code=404, detail="Отель не найден")
   return {'status': 'ok', "data": hotel}