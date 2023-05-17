from fastapi import FastAPI
from .routers import cafe, auth, user
from . import models, schemas
from .database import engine, SessionLocal, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(cafe.router)
app.include_router(auth.router)
app.include_router(user.router)