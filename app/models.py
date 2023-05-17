from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


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

    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"
    ), nullable=False)
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)