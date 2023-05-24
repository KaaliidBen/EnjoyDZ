from fastapi import APIRouter,Depends,status ,HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from starlette.responses import JSONResponse

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

@router.post('/',response_model=schemas.showCat,status_code=status.HTTP_201_CREATED)
def create(request :schemas.showCat,db :Session = Depends(get_db)):
    
    new_categorie = models.Categorie(Nom = request.Nom)

    db.add(new_categorie)
    db.commit()
    db.refresh(new_categorie)


    return new_categorie

@router.delete('/{id}')
def delete_cat(id:int, db:Session = Depends(get_db)):
    cat = db.query(models.Categorie).filter(models.Categorie.id == id).delete()
    db.commit()
    if not cat : return JSONResponse({"Result":"already deleted"})
    return JSONResponse({"result": True})

@router.get('/all/',response_model = list[schemas.showCat])
def get_all_cat(db : Session = Depends(get_db)):
    cats = db.query(models.Categorie).filter().all()
    return cats

@router.get('/{id}',response_model=schemas.showCat)
def get(id:int, db:Session = Depends(get_db)):
    cat = db.query(models.Categorie).filter(models.Categorie.id == id).first()
    return cat
