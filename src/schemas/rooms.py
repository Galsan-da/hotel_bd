from pydantic import BaseModel, Field, ConfigDict

class RoomBase(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int = Field(gt=0)
    quantity: int = Field(ge=0)

class RoomAdd(RoomBase):
    pass

class RoomUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = Field(None, gt=0)
    quantity: int | None = Field(None, ge=0)

class RoomResponse(RoomBase):
    id: int

    class Config:
        from_attributes = True