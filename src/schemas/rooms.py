from pydantic import BaseModel, Field, ConfigDict

class RoomAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int = Field(gt=0)
    quantity: int = Field(ge=0)

class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int = Field(gt=0)
    quantity: int = Field(ge=0)

class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

class RoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = Field(None, gt=0)
    quantity: int | None = Field(None, ge=0)


class RoomPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = Field(None, gt=0)
    quantity: int | None = Field(None, ge=0)
