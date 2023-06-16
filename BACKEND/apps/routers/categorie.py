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

#Add a Categorie
@router.post('/add/', response_model = schemas.categorie)
def add_categorie(request : schemas.categorie, db :Session = Depends(get_db)):
    try:
        new_categorie = models.Categorie(Nom = request.Nom)
        db.add(new_categorie)
        db.commit()
        db.refresh(new_categorie)
        return new_categorie
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))


#Delete a Categorie
@router.delete('/{id}/delete/')
def delete_categorie(id:int, db:Session = Depends(get_db)):
    try:
        categorie_to_delete = db.query(models.Categorie).filter(models.Categorie.id == id).first()
        if not categorie_to_delete : 
            raise HTTPException(status_code = 400, detail = 'Categorie not found')
        db.delete(categorie_to_delete)
        db.commit()
        return JSONResponse({
            "result": True,
            "message" : "Categorie deleted"}
        )
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))


#Get all Categories
@router.get('/all/', response_model = list[ schemas.categorie])
def get_all_cat(db : Session = Depends(get_db)):
    try:
        categories = db.query(models.Categorie).all()
        return categories
    except Exception as e:
        raise HTTPException(status_code=400, detail = str(e))

#Get Categorie based on id
@router.get('/{id}/', response_model = schemas.categorie)
def get_categorie(id : int, db:Session = Depends(get_db)):
    try:
        categorie = db.query(models.Categorie).filter(models.Categorie.id == id).first()
        if not categorie:
            raise HTTPException(status_code=400, detail='Categorie not found')
        return categorie
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


#Update a Categorie
@router.post('/{id}/update/', response_model = schemas.categorie)
def update_categorie(id : int, request : schemas.categorie, db : Session = Depends(get_db)):
    try:
        categorie_to_update = db.query(models.Categorie).filter(models.Categorie.id == id).first()
        updated_categorie = request.dict(exclude_unset=True)
        for key, value in updated_categorie.items():
            setattr(categorie_to_update, key, value)
        db.add(categorie_to_update)
        db.commit()
        db.refresh(categorie_to_update)
        return categorie_to_update
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))