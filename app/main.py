from fastapi import FastAPI
from .routers import cafe
from . import models, schemas
from .database import engine, SessionLocal, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(cafe.router)