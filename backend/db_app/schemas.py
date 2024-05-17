from pydantic import BaseModel
import datetime

class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class ConnectionBase(BaseModel):
    sender_id: int
    receiver_id: int

class ConnectionCreate(ConnectionBase):
    pass

class Connection(ConnectionBase):
    id: int
    answered: bool | None

    class Config:
        orm_mode = True