from .. import models, schemas
from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from ..database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/cafes",
    tags=["Cafes"]
)


# all_cafes = [{
#     "name": "fantasy",
#     "location": "indore",
#     "can_take_calls": True,
#     "coffee_price": 10,
#     "has_sockets": True,
#     "has_toilet": True,
#     "has_wifi": True,
#     "map_url": "indore",
#     "seats": 20,
#     "id": 1
# },
#     {
#     "name": "Tinku's",
#     "location": "indore",
#     "can_take_calls": True,
#     "coffee_price": 15,
#     "has_sockets": True,
#     "has_toilet": True,
#     "has_wifi": True,
#     "map_url": "indore",
#     "seats": 20,
#     "id": 2
# }
# ]


@router.get("/", response_model=List[schemas.Cafe])
def get_cafes(db: Session = Depends(get_db)):
    cafes = db.query(models.Cafe).all()
    return cafes


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Cafe)
def create_cafe(cafe: schemas.CafeCreate, db: Session = Depends(get_db)):
    new_cafe = models.Cafe(**cafe.dict())
    db.add(new_cafe)
    db.commit()
    db.refresh(new_cafe)
    return new_cafe


@router.get("/{id}", response_model=schemas.Cafe)
def get_cafe(id: int, response: Response, db: Session = Depends(get_db)):
    cafe = db.query(models.Cafe).filter(models.Cafe.id == id).first()
    if not cafe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cafe with the id: {id} was not found")

    return cafe


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cafe(id: int, db: Session = Depends(get_db)):
    cafe = db.query(models.Cafe).filter(models.Cafe.id == id)
    if cafe.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cafe with id: {id} was not found")

    cafe.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Cafe)
def update_cafe(id: int, cafe: schemas.CafeCreate, db: Session = Depends(get_db)):
    cafe_query = db.query(models.Cafe).filter(models.Cafe.id == id)
    cafe_to_update = cafe_query.first()

    if cafe_to_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cafe with the id: {id} not found")

    cafe_query.update(cafe.dict(), synchronize_session=False)
    db.commit()
    updated_cafe = cafe_query.first()
    return updated_cafe


@router.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    return {"status": "success"}
