from fastapi import APIRouter,Depends,status ,HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

# -----local imports --------------------------------
from db import database
from models import models
from schemas import schemas
from baseController import *

router = APIRouter(
    prefix='/carte',
    tags=['cartes']
)

get_db=database.get_db

#creer, supprimer, maj, recherche(cat,theme)

@router.post('/',response_model=schemas.carteCreate,status_code=status.HTTP_201_CREATED)
def create(request :schemas.carteCreate,db :Session = Depends(get_db)):
    new_carte = models.Carte(Nom = request.Nom)

    db.add(new_carte)
    db.commit()
    db.refresh(new_carte)

    return new_carte

@router.delete('/{id}')
def delete_point(id:int, db:Session = Depends(get_db)):

    carte = db.query(models.Carte).filter(models.Carte == id).delete()
    db.commit()
    if not carte : return JSONResponse({"Result":"already deleted"})

    return JSONResponse({"result":True})

@router.get('/all', response_model = list[schemas.showCarte])
def get_all_cartes(db : Session = Depends(get_db)):
    cartes  = db.query(models.Carte).filter().all()
    return cartes

@router.get('/{id}',response_model=schemas.showCarte)
def get(id:int, db:Session = Depends(get_db)):
    carte = db.query(models.Carte).filter(models.Carte.id == id).first()
    return carte


