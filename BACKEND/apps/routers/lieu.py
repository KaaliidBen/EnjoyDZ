from fastapi import APIRouter,Depends,status ,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from starlette.responses import JSONResponse

# -----local imports --------------------------------
from db import database
from models import models
from schemas import schemas

router = APIRouter(
    prefix='/lieu',
    tags=['lieus']
)

get_db=database.get_db

#creer, supprimer, maj, recherche(cat,theme)

#Add a Lieu
@router.post('/add/',response_model=schemas.lieu, status_code=status.HTTP_201_CREATED)
def add_lieu(request : schemas.lieu, db : Session = Depends(get_db)):
    try:
        new_lieu = models.Lieu(
            Nom = request.Nom,
            Description = request.Description,
            DateOuverture = request.DateOuverture,
            DateFermeture = request.DateFermeture
        )
        db.add(new_lieu)
        db.commit()
        db.refresh(new_lieu)
        return new_lieu
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

#Delete a Lieu
@router.delete('/{id}/delete/')
def delete_lieu(id:int, db:Session = Depends(get_db)):
    try:
        lieu_to_delete = db.query(models.Lieu).filter(models.Lieu.id == id).first()
        if not lieu_to_delete :
            raise HTTPException(status_code = 400, detail = "Lieu not found")
        db.delete(lieu_to_delete)
        db.commit()
        return JSONResponse({
            "result" : True,
            "message" : "Lieu deleted"
            })
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

#Get all Lieux
@router.get('/all/', response_model = list[schemas.lieu])
def get_all_lieux(db : Session = Depends(get_db)):
    try:
        lieux  = db.query(models.Lieu).all()
        return lieux
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

#Get a Lieu based on id
@router.get('/{id}/',response_model=schemas.lieu)
def get_lieu(id:int, db:Session = Depends(get_db)):
    try:
        lieu = db.query(models.Lieu).filter(models.Lieu.id == id).first()
        return lieu
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

#Update a Lieu
@router.post('/{id}/update/', response_model = schemas.lieu)
def update_lieu(id : int, request : schemas.lieu, db : Session = Depends(get_db)):
    try:
        lieu_to_update = db.query(models.Lieu).filter(models.Lieu.id == id).first()
        updated_lieu = request.dict(exclude_unset=True)
        for key, value in updated_lieu.items():
            setattr(lieu_to_update, key, value)
        db.add(lieu_to_update)
        db.commit()
        db.refresh(lieu_to_update)
        return lieu_to_update
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))