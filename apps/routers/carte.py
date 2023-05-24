from fastapi import APIRouter,Depends,status ,HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

# -----local imports --------------------------------
from db import database
from models import models
from schemas import schemas

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


    return new_element
