from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

# -----local imports --------------------------------
from db import database
from models import models
from schemas import schemas

router = APIRouter(
    prefix ='/commentaire',
    tags=['commentaires']
)

get_db = database.get_db

@router.post('/add/', response_model=schemas.commentaire, status_code=status.HTTP_201_CREATED)
def add_commentaire(request:schemas.commentaire, db:Session =Depends(get_db)):
    try:
        commentaire = models.Commentaire(
            user_id = request.user_id,
            point_id = request.point_id,
            Content = request.Content
            )
        db.add(commentaire)
        db.commit()
        db.refresh(commentaire)

        return commentaire
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

@router.delete('/{id}/delete/')
def delete_commentaire(id:int, db:Session = Depends(get_db)):
    try:
        commentaire_to_delete = db.query(models.Commentaire).filter(models.Commentaire.id == id).first()
        if not commentaire_to_delete:
            raise HTTPException(status_code=404, detail="Comment not found")
        db.delete(commentaire_to_delete)
        db.commit()
        return JSONResponse({"result":True})
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

@router.get('/all/',response_model = list[schemas.commentaire])
def get_all_commentaires(db : Session = Depends(get_db)):
    try:
        commentaires =  db.query(models.Commentaire).all()
        return commentaires
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

@router.get('/{id}/',response_model=schemas.commentaire)
def get_commentaire(id:int , db:Session = Depends(get_db)):
    try:
        commentaire = db.query(models.Commentaire).filter(models.Commentaire.id == id).first()
        if not commentaire:
            raise HTTPException(status_code=404, detail="Comment not found")
        return commentaire
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
    
@router.post('/{id}/update/', response_model = schemas.commentaire)
def update_commentaire(id : int, request : schemas.commentaire, db : Session = Depends(get_db)):
    try:
        commentaire_to_update = db.query(models.Commentaire).filter(models.Commentaire.id == id).first()
        if not commentaire_to_update:
            raise HTTPException(status_code=404, detail="Comment not found")
        updated_commentaire = request.dict(exclude_unset=True)
        for key, value in updated_commentaire.items():
            setattr(commentaire_to_update, key, value)
        db.add(commentaire_to_update)
        db.commit()
        db.refresh(commentaire_to_update)
        return commentaire_to_update
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))