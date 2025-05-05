# repositories/bookings.py
from sqlalchemy import select, text
from datetime import date

from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm

class BookingsRepository(BaseRepository):
    model = BookingsOrm

    async def check_room_availability(
        self, room_id: str, date_from: date, date_to: date
    ) -> bool:
        query = text("""
            SELECT COUNT(*) FROM bookings
            WHERE room_id = :room_id
            AND NOT (date_to <= :date_from OR date_from >= :date_to)
        """)
        result = await self.session.execute(
            query, {"room_id": room_id, "date_from": date_from, "date_to": date_to}
        )
        return result.scalar() == 0

    async def get_room_price(self, room_id: str) -> int:
        room = await self.session.get(RoomsOrm, room_id)
        if not room:
            raise ValueError("Номер с указанным ID не существует")
        return room.price