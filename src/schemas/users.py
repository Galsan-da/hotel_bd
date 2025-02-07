from pydantic import BaseModel, ConfigDict

class UserRequestAdd(BaseModel):
    email: str
    user_name: str
    password: str

class UserAdd(BaseModel):
    email: str
    user_name: str
    hashed_password: str

class User(UserAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)

class UserWithHashedPassword(User):
    hashed_password: str