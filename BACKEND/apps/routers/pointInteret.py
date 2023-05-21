from fastapi import APIRouter,Depends,status ,HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
from starlette.responses import JSONResponse
# -----local imports --------------------------------
from db import database
from models import models
from schemas import schemas

router = APIRouter(
    prefix='/point',
    tags=['points']
)

get_db=database.get_db

#creer, supprimer, maj, recherche(cat,theme)
#response_model=schemas.pointCreate

#Adds an Interest Point
@router.post('/addPoint/', status_code=status.HTTP_201_CREATED)
def create_new_point(request : schemas.pointCreate, 
           horaireid : int,
           themeid : int,
           categorieid : int,
           db : Session = Depends(get_db),
           carteid : Optional[int]=0
           ) :

    new_point = models.PointInteret(
        Nom = request.Nom, 
        Description = request.Description,
        Carte_id = carteid,
        Horaire_id = horaireid,
        Theme_id = themeid,
        Categorie_id = categorieid
        )

    db.add(new_point)
    db.commit()
    db.refresh(new_point)

    return new_point


#Deletes an Interest Point
@router.delete('/{id}')
def delete_point(id:int, db:Session = Depends(get_db)):
    point = db.query(models.PointInteret).filter(models.PointInteret.id == id).delete()
    db.commit()
    if not point : return JSONResponse({"Result":"already deleted"})

    return JSONResponse({"result": True})


#Returns Interest Points filtered by category or theme or both
@router.get('/filtered/',response_model=List[schemas.showPoint])
def getPointsFiltered(cat:int=0, theme:int=0, db :Session = Depends(get_db)):
    Point = None
    if cat == 0:
        Points=db.query(models.PointInteret).filter( models.PointInteret.Theme_id == theme).all()
    elif theme == 0:
        Points=db.query(models.PointInteret).filter( models.PointInteret.Categorie_id == cat ).all()
    else:
        Points=db.query(models.PointInteret).filter( models.PointInteret.Categorie_id == cat ,
                                                    models.PointInteret.Theme_id == theme).all()

    return Points
    

#Returns all Interest Points containing a search term in their description
@router.get('/bySearch/',response_model = List[schemas.showPoint])
def getPointsBySearch(search: str = '',db :Session = Depends(get_db)):

    Points=db.query(models.PointInteret).filter(models.PointInteret.Description.contains(search)).all()
    return Points


#Returns all Interest Points
@router.get('/all/', response_model = List[schemas.showPoint])
def get_all_points(db : Session = Depends(get_db)):
    Points = db.query(models.PointInteret).filter().all()
    return Points