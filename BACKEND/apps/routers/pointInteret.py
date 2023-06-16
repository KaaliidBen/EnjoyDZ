from fastapi import APIRouter, Depends, status, HTTPException
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

#Get an Interest Point based on id
@router.get('/{id}/',response_model=schemas.point)
def get_point(id : int, db : Session = Depends(get_db)):
    try:
        point = db.query(models.PointInteret).filter(models.PointInteret.id == id).first()
        return point
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))


#Adds an Interest Point
@router.post('/add/', status_code=status.HTTP_201_CREATED)
def create_new_point(request : schemas.point,
           themeid : int,
           categorieid : int,
           db : Session = Depends(get_db),
           lieuid : Optional[int] = 0
           ) :
    try:
        new_point = models.PointInteret(
            Nom = request.Nom, 
            Description = request.Description,
            Wilaya = request.Wilaya,
            Lieu_id = lieuid,
            Theme_id = themeid,
            Categorie_id = categorieid
            )

        db.add(new_point)
        db.commit()
        db.refresh(new_point)

        return new_point
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))


#Returns all Interest Points
@router.get('/all', response_model = list[schemas.point])
def get_all_points(db : Session = Depends(get_db)):
    try:
        points = db.query(models.PointInteret).filter().all()
        return points
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

#Deletes an Interest Point
@router.delete('/{id}/delete/')
def delete_point(id:int, db:Session = Depends(get_db)):
    try:
        point = db.query(models.PointInteret).filter(models.PointInteret.id == id).delete()
        db.commit()
        if not point : return JSONResponse({"Result":"already deleted"})

        return JSONResponse({"result": True})
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))


#Returns Interest Points filtered by category or theme or both
@router.get('/filtered',response_model=List[schemas.point])
def getPointsFiltered(cat : int=0, theme : int=0, db : Session = Depends(get_db)):
    try:
        if cat == 0:
            Points=db.query(models.PointInteret).filter( models.PointInteret.Theme_id == theme).all()
        elif theme == 0:
            Points=db.query(models.PointInteret).filter( models.PointInteret.Categorie_id == cat ).all()
        else:
            Points=db.query(models.PointInteret).filter( models.PointInteret.Categorie_id == cat ,
                                                        models.PointInteret.Theme_id == theme).all()

        return Points
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
    

#Returns all Interest Points containing a search term in their description
@router.get('/bySearch',response_model = List[schemas.point])
def getPointsBySearch(search: str = '',db :Session = Depends(get_db)):
    try:
        Points = db.query(models.PointInteret).filter(or_(models.PointInteret.Description.contains(search),
                                                          models.PointInteret.Nom.contains(search),
                                                          models.PointInteret.Wilaya.contains(search))).all()
        return Points
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))


#Update an Interest Point
@router.post('/{id}/update/', response_model = schemas.point)
def update_point(id : int, request : schemas.point, db : Session = Depends(get_db)):
    try:
        point_to_update = db.query(models.PointInteret).filter(models.PointInteret.id == id).first()
        updated_point = request.dict(exclude_unset=True)
        for key, value in updated_point.items():
            setattr(point_to_update, key, value)
        db.add(point_to_update)
        db.commit()
        db.refresh(point_to_update)
        return point_to_update
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))