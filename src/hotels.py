from pydantic import BaseModel, Field

class Hotel(BaseModel):
    title: str
    hotel_name: str

class HotelPATCH(BaseModel):
    title: str | None = Field(default=None, description="Название города")
    hotel_name: str | None = Field(default=None, description="Название отеля")