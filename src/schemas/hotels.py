from pydantic import BaseModel, Field

class Hotel(BaseModel):
    title: str
    hotel_name: str

class HotelPATCH(BaseModel):
    title: str| None = Field(None)
    hotel_name: str| None = Field(None)