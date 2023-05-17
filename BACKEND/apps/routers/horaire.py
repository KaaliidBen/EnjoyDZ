from fastapi import APIRouter,Depends,status ,HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

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

@router.post('/',response_model=schemas.horaire,status_code=status.HTTP_201_CREATED)
def create(request :schemas.horaire,db :Session = Depends(get_db)):
    
    new_horaire = models.Horaire(date_debut = request.date_debut,date_fin = request.date_fin)

    db.add(new_horaire)
    db.commit()
    db.refresh(new_horaire)


    return new_element
