from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class CafeBase(BaseModel):
    name: str
    location: str
    can_take_calls: bool
    coffee_price: float
    has_sockets: bool
    has_wifi: bool
    map_url: str
    seats: int


class CafeCreate(CafeBase):
    pass

# Response Model


class Cafe(CafeBase):
    id: int
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
