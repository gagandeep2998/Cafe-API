from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class Cafe(Base):
    __tablename__ = "cafes"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    can_take_calls = Column(Boolean, nullable=False)
    coffee_price = Column(Float, nullable=False)
    has_sockets = Column(Boolean, nullable=False)
    has_wifi = Column(Boolean, nullable=False)
    map_url = Column(String, nullable=False)
    seats = Column(Integer, nullable=False)
