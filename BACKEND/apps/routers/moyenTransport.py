from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

# --------------------------- local imports --------------------------------
from db import database
from models import models
from schemas import schemas

router = APIRouter(
    prefix ='/transport',
    tags=['transports']
)

get_db = database.get_db

@router.post('/add/',response_model=schemas.transport,status_code=status.HTTP_201_CREATED)
def create_moyen(request:schemas.transport,db:Session =Depends(get_db)):
    try:
        moyen = models.MoyenTransport(Type = request.Type)
        db.add(moyen)
        db.commit()
        db.refresh(moyen)

        return moyen
    except Exception as e:
        raise HTTPException(status_code = 404, detail = str(e))

@router.delete('/{id}/delete/')
def delete_moyen(id:int, db:Session = Depends(get_db)):
    try:
        moyen = db.query(models.MoyenTransport).filter(models.MoyenTransport.id == id).first()
        if not moyen:
            raise HTTPException(status_code=404, detail="Moyen not found")
        db.delete(moyen)
        db.commit()
        if not moyen : return JSONResponse({"Result":"already deleted"})
        return JSONResponse({"result":True})
    except Exception as e:
        raise HTTPException(status_code = 404, detail = str(e))

@router.get('/all/',response_model = list[schemas.transport])
def get_all_moyens(db : Session = Depends(get_db)):
    try:
        moyens =  db.query(models.MoyenTransport).filter().all()
        return moyens
    except Exception as e:
        raise HTTPException(status_code = 404, detail = str(e))

@router.get('/{id}/',response_model=schemas.transport)
def get_moyen(id:int , db:Session = Depends(get_db)):
    try:
        moyen = db.query(models.MoyenTransport).filter(models.MoyenTransport.id == id).first()
        if not moyen:
            raise HTTPException(status_code=404, detail="Moyen not found")
        return moyen
    except Exception as e:
        raise HTTPException(status_code = 404, detail = str(e))
    
@router.post('/{id}/update/', response_model = schemas.transport)
def update_moyen(id : int, request : schemas.transport, db : Session = Depends(get_db)):
    try:
        moyen_to_update = db.query(models.MoyenTransport).filter(models.MoyenTransport.id == id).first()
        if not moyen_to_update:
            raise HTTPException(status_code=404, detail="Moyen not found")
        updated_moyen = request.dict(exclude_unset=True)
        for key, value in updated_moyen.items():
            setattr(moyen_to_update, key, value)
        db.add(moyen_to_update)
        db.commit()
        db.refresh(moyen_to_update)
        return moyen_to_update
    except Exception as e:
        raise HTTPException(status_code = 404, detail = str(e))