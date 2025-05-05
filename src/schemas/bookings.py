# schemas/bookings.py
from pydantic import BaseModel, Field, field_validator
from datetime import date

class BookingCreate(BaseModel):
    room_id: str = Field(..., min_length=1, description="Идентификатор номера")
    date_from: date
    date_to: date

    @field_validator("date_to")
    @classmethod
    def validate_dates(cls, date_to: date, values):
        if "date_from" in values.data and date_to <= values.data["date_from"]:
            raise ValueError("Дата выезда должна быть после даты заезда")
        return date_to

class BookingResponse(BookingCreate):
    id: int
    user_id: int
    price: int
    total_cost: int  # Автоматически рассчитывается в модели

    class Config:
        from_attributes = True