from fastapi import APIRouter, Depends, status , HTTPException, Query
from sqlalchemy.orm import Session

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
        raise HTTPException(status_code = 404, detail = str(e))


#Add an Evenement
@router.post('/add/')
def add_an_evenement(request, db : Session = Depends(get_db)):
    new_evenement = models.Evenement(
        Nom = request.Nom,
        Description = request.Description,
        Horaire_id = models.Horaire(
            date_debut = request.date_debut,
            date_fin = request.date_fin
        ).id,
        point_id = request.point_id
    )
    db.add(new_evenement)
    db.commit()
    db.refresh(new_evenement)

    return new_evenement