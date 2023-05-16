from pydantic import BaseModel


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

    class Config:
        orm_mode = True
