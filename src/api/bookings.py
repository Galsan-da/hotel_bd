from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingCreate, BookingResponse

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: BookingCreate,
    db: DBDep,
    user_id: UserIdDep
):
    try:
        # Проверка доступности номера
        if not await db.bookings.check_room_availability(
            booking_data.room_id, booking_data.date_from, booking_data.date_to
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Номер занят на указанные даты"
            )

        # Получение цены номера
        price = await db.bookings.get_room_price(booking_data.room_id)

        # Создание бронирования с сохранением цены
        booking = await db.bookings.add({
            "user_id": user_id,
            "room_id": booking_data.room_id,
            "date_from": booking_data.date_from,
            "date_to": booking_data.date_to,
            "price": price  # Сохраняем цену, total_cost расчитается автоматически
        })
        await db.commit()
        return booking

    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка целостности данных: " + str(e.orig)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )