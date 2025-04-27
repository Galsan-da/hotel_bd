from pydantic import BaseModel, Field, ConfigDict

class RoomAdd(BaseModel):
    title: str
    location: str

class Room(BaseModel):
    id: int
    #model_config = ConfigDict(from_attributes=True)

class RoomPATCH(BaseModel):
    title: str| None = Field(None)
    location: str| None = Field(None)