from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

# -----local imports --------------------------------
from db import database
from models import models
from schemas import schemas

router = APIRouter(
    prefix='/evenement',
    tags=['evenements']
)

get_db = database.get_db

#Get all Evenements
@router.get('/all/', response_model = list[schemas.evenement])
def get_all_evenements(db : Session = Depends(get_db)):
    try:
        evenements = db.query(models.Evenement).all()
        return evenements
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))


#Get Evenement based on id
@router.get('/{id}/', response_model = schemas.evenement)
def get_evenement(id : int, db : Session = Depends(get_db)):
    try:
        evenement = db.query(models.Evenement).filter(models.Evenement.id == id).first()
        if not evenement:
            raise HTTPException(status_code=404, detail="Event not found")
        return evenement
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

#Add an Evenement
@router.post('/add/')
def add_evenement(request : schemas.evenement, db : Session = Depends(get_db)):
    try:
        new_evenement = models.Evenement(
            Nom = request.Nom,
            Description = request.Description,
            DateDebut = request.DateDebut,
            DateFin = request.DateFin,
            point_id = request.point_id
        )
        db.add(new_evenement)
        point = db.query(models.PointInteret).filter(models.PointInteret.id == request.point_id).first()
        following_users = point.fans
        for user in following_users:
            new_notification = models.Notification(
                Content = f"New event at {point.Nom} : {request.Description}",
                Read = False
            )
            user.notifications.append(new_notification)
            db.add(user)
        db.commit()
        db.refresh(new_evenement)
        return new_evenement
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
    

#Delete an Evenement
@router.delete('/{id}/delete/')
def delete_evenement(id : int, db : Session = Depends(get_db)):
    try:
        evenement_to_delete = db.query(models.Evenement).filter(models.Evenement.id == id).first()
        if not evenement_to_delete:
            raise HTTPException(status_code=404, detail="Event not found")
        db.delete(evenement_to_delete)
        db.commit()
        return JSONResponse({
            "message" : "Evenement deleted"
        })
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
    
#Update an Evenement
@router.post("/{id}/update/", response_model = schemas.evenement)
def update_evenement(request : schemas.evenement, id : int, db : Session = Depends(get_db)):
    try:
        evenement_to_update = db.query(models.Evenement).filter(models.Evenement.id == id).first()
        if not evenement_to_update:
            raise HTTPException(status_code=404, detail="Event not found")
        updated_evenement = request.dict(exclude_unset=True)
        for key, value in updated_evenement.items():
            setattr(evenement_to_update, key, value)
        db.add(evenement_to_update)
        db.commit()
        db.refresh(evenement_to_update)
        return evenement_to_update
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))