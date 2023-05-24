from fastapi import APIRouter,Depends,status ,HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

# -----local imports --------------------------------
from db import database
from models import models
from schemas import schemas
from baseController import *

router = APIRouter(
    prefix ='/transport',
    tags=['transports']
)

get_db = database.get_db

@router.post('/',response_model=schemas.showTransport,status_code=status.HTTP_201_CREATED)
def create(request:schemas.showTransport,db:Session =Depends(get_db)):
    moyen = models.MoyenTransport(Type = request.Type)
    db.add(moyen)
    db.commit()
    db.refresh(moyen)

    return moyen

@router.delete('/{id}')
def delete_moyen(id:int, db:Session = Depends(get_db)):
    moyen = db.query(models.MoyenTransport).filter(models.MoyenTransport.id == id).delete()
    db.commit()
    if not moyen : return JSONResponse({"Result":"already deleted"})
    return JSONResponse({"result":True})

@router.get('/all',response_model = list[schemas.showTransport])
def get_all_moyens(db : Session = Depends(get_db)):
    moyens =  db.query(models.MoyenTransport).filter().all()
    return moyens

@router.get('/{id}',response_model=schemas.showTransport)
def get(id:int , db:Session = Depends(get_db)):
    moyen  =db.query(models.MoyenTransport).filter(models.MoyenTransport.id == id).first()
    return moyen