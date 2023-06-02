from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models
from app.config import settings


SQLALCHEMY_DATABASE_URL = "sqlite:///./cafe_test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base.metadata.create_all(bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user2(client):
    user_data = {"email": "hello@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user(client):
    user_data = {"email": "hello123@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_cafes(test_user, test_user2, session):
    cafes_data = [{
        "name": "fantasy",
        "location": "indore",
        "can_take_calls": True,
        "coffee_price": 10,
        "has_sockets": True,
        "has_wifi": True,
        "map_url": "indore",
        "seats": 20,
        "owner_id": test_user["id"]
    },
        {
        "name": "Tinku's",
        "location": "indore",
        "can_take_calls": True,
        "coffee_price": 15,
        "has_sockets": True,
        "has_wifi": True,
        "map_url": "indore",
        "seats": 20,
        "owner_id": test_user["id"]
    },
    {
        "name": "Chai Sutta Bar",
        "location": "indore",
        "can_take_calls": True,
        "coffee_price": 25,
        "has_sockets": True,
        "has_wifi": True,
        "map_url": "indore",
        "seats": 30,
        "owner_id": test_user2["id"]
    }
    ]

    def create_cafe_model(cafe):
        return models.Cafe(**cafe)
    
    cafe_map = map(create_cafe_model, cafes_data)
    cafes = list(cafe_map)


    session.add_all(cafes)
    session.commit()

    all_cafes = session.query(models.Cafe).all()
    return all_cafes