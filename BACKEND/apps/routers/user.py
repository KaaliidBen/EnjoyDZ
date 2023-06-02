from fastapi import APIRouter,Depends,HTTPException,status
from db import database
from models import models
from schemas import schemas
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from typing import List

router = APIRouter(
    prefix='/user',
    tags=['Users']
)
get_db=database.get_db

@router.post('/', response_model=schemas.showuser)
def create(request:schemas.createuser,db :Session = Depends( get_db)):
    new_user = models.Utilisateur(Nom=request.Nom,Email=request.Email,token = request.token)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}',response_model=schemas.showuser)
def get_user(id:int,db :Session = Depends(get_db)):
    user=db.query(models.Utilisateur).filter(models.Utilisateur.id == id).first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'user with id {id} not found')
    return user

