from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest, Booking

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

@router.post("")
async def add_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest,
):
    # получение цену номера
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room.price
    # создание схемы данных BookingAdd
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump()
    )
    # добавим бронирование конкретному пользователю
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"statuc": "OK", "data": booking}

@router.get("", response_model=list[Booking])
async def get_all_bookings(db: DBDep):
    """Получение всех бронирований"""
    return await db.bookings.get_all()

@router.get("/me", response_model=list[Booking])
async def get_my_bookings(
    db: DBDep,
    user_id: UserIdDep
):
    """Получение бронирований текущего пользователя"""

    return await db.bookings.get_filtered(user_id=user_id)