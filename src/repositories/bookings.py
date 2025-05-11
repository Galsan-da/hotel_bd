# repositories/bookings.py
from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking

    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return [self.schema.model_validate(row) for row in result.scalars().all()]

    async def get_filtered(self, **filters):
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        return [self.schema.model_validate(row) for row in result.scalars().all()]