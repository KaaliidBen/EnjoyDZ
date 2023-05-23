from fastapi import APIRouter,Depends,status ,HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List

# -----local imports --------------------------------
from db import database
from models import models
from schemas import schemas
from baseController import *

router = APIRouter(
    prefix='/horaire',
    tags=['horaires']
)

get_db=database.get_db

#creer, supprimer, maj, recherche(cat,theme)

#Returns all Horaires
@router.get('/all/', response_model = list[schemas.horaire])
def get_all_horaires(db : Session = Depends(get_db)):
    horaires = db.query(models.Horaire).filter().all()

    return horaires


#Returns specific Horaire according to id
@router.get('/{id}/', response_model = schemas.horaire)
def get_horaire(id : int, db : Session = Depends(get_db)):
    horaire = db.query(models.Horaire).filter(models.Horaire.id == id).first()

    return horaire


#Add a new Horaire
@router.post('/add/', response_model = schemas.horaire, status_code = status.HTTP_201_CREATED)
def add_horaire(request : schemas.horaire, db : Session = Depends(get_db)):
    new_horaire = models.Horaire(date_debut = request.date_debut, 
                             date_fin = request.date_fin)
    db.add(new_horaire)
    db.commit()
    db.refresh(new_horaire)

    return new_horaire


#Modify an Horaire
@router.post('/{id}/modify/', response_model = schemas.horaire)
def modify_horaire(request : schemas.horaire, id : int, db : Session = Depends(get_db)):
    horaire_to_update = db.query(models.Horaire).filter(models.Horaire.id == id).first()
    updated_horaire = request.dict(exclude_unset=True)
    for key, value in updated_horaire.items():
        setattr(horaire_to_update, key, value)
    db.add(horaire_to_update)
    db.commit()
    db.refresh(horaire_to_update)

    return horaire_to_update


#Delete an Horaire
@router.delete('/{id}/delete/')
def delete_horaire(id : int, db : Session = Depends(get_db)):
    horaire_to_delete = db.query(models.Horaire).filter(models.Horaire.id == id).first()
    db.delete(horaire_to_delete)
    db.commit()

    return {"message" : "Horaire deleted"}