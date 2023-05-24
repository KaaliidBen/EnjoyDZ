from fastapi import APIRouter,Depends,status ,HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

# -----local imports --------------------------------
from db import database
from models import models
from schemas import schemas

router = APIRouter(
    prefix='/theme',
    tags=['themes']
)

get_db=database.get_db

#creer, supprimer, maj, recherche(cat,theme)

@router.post('/',response_model=schemas.theme,status_code=status.HTTP_201_CREATED)
def create(request :schemas.theme,db :Session = Depends(get_db)):
    
    new_theme = models.Theme(Nom = request.Nom)

    db.add(new_theme)
    db.commit()
    db.refresh(new_theme)


    return new_theme
