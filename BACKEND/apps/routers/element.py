from fastapi import APIRouter,Depends,status ,HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

# -----local imports --------------------------------
from db import database
from models import models
from schemas import schemas

router = APIRouter(
    prefix='/element',
    tags=['elements']
)

get_db=database.get_db

@router.post('/',response_model=schemas.elementbase,status_code=status.HTTP_201_CREATED)
def create(request :schemas.elementbase,db :Session = Depends(get_db)):
    new_element = models.Element(Nom = request.Nom,Prenom ="naila")

    db.add(new_element)
    db.commit()
    db.refresh(new_element)


    return new_element