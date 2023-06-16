from fastapi import APIRouter, Depends, status , HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from starlette.responses import JSONResponse

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

#Get all Themes
@router.get('/all/', response_model = list[schemas.theme])
def get_all_themes(db : Session = Depends(get_db)):
    try:
        themes = db.query(models.Theme).all()

        return themes
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


#Get Theme according to id
@router.get('/{id}/', response_model = schemas.theme)
def get_theme(id : int, db : Session = Depends(get_db)):
    try:
        theme = db.query(models.Theme).filter(models.Theme.id == id).first()
        return theme
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

#Add a Theme
@router.post('/add/', response_model = schemas.theme, status_code=status.HTTP_201_CREATED)
def add_theme(request :schemas.theme, db :Session = Depends(get_db)):
    try:
        new_theme = models.Theme(Nom = request.Nom)
        db.add(new_theme)
        db.commit()
        db.refresh(new_theme)

        return new_theme
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

#Update a Theme
@router.post('/{id}/update/', response_model = schemas.theme)
def modify_theme(id : int, request : schemas.theme, db : Session = Depends(get_db)):
    try:
        theme_to_update = db.query(models.Theme).filter(models.Theme.id == id).first()
        updated_theme = request.dict(exclude_unset=True)
        for key, value in updated_theme.items():
            setattr(theme_to_update, key, value)
        db.add(theme_to_update)
        db.commit()

        return theme_to_update
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

#Delete a Theme
@router.delete('/{id}/delete/')
def delete_theme(id : int, db : Session = Depends(get_db)):
    try:
        theme_to_delete = db.query(models.Theme).filter(models.Theme.id == id).first()
        db.delete(theme_to_delete)
        db.commit()
        return JSONResponse({
            "result" : True,
            "message" : "Theme deleted"
            })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))