from fastapi import APIRouter,Depends,status ,HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List

# -----local imports --------------------------------
from db import database
from models import models
from schemas import schemas

router = APIRouter(
    prefix='/horaire',
    tags=['horaires']
)

get_db=database.get_db

#creer, supprimer, maj, recherche(cat,theme)

#Add a new Horaire
@router.post('/addHoraire',response_model=schemas.horaire,status_code=status.HTTP_201_CREATED)
def add_horaire(request : schemas.horaire, db : Session = Depends(get_db)):
    
    new_horaire = models.Horaire(date_debut = request.date_debut, 
                                 date_fin = request.date_fin)
    db.add(new_horaire)
    db.commit()
    db.refresh(new_horaire)

    return new_horaire

#Returns all Horaires
@router.get('/all', response_model = List[schemas.horaire])
def get_all_horaires(db : Session = Depends(get_db)):
    horaires = db.query(models.Horaire).all()

    return horaires