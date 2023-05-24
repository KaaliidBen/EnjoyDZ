from fastapi import APIRouter,Depends,status ,HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

# -----local imports --------------------------------
from db import database
from models import models
from schemas import schemas

router = APIRouter(
    prefix='/categorie',
    tags=['categories']
)

get_db=database.get_db

#creer, supprimer, maj, recherche(cat,theme)

@router.post('/',response_model=schemas.categorie,status_code=status.HTTP_201_CREATED)
def create(request :schemas.categorie,db :Session = Depends(get_db)):
    
    new_categorie = models.Theme(Nom = request.Nom)

    db.add(new_categorie)
    db.commit()
    db.refresh(new_categorie)


    return new_categorie
