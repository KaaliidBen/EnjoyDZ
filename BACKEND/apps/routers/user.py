from fastapi import APIRouter,Depends,HTTPException,status
from db import database
from models import models
from schemas import schemas
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from typing import List

router = APIRouter(
    prefix='/user',
    tags=['Users']
)
get_db=database.get_db

#creer, supprimer, maj, recherche(cat,theme)

#Returns all Users
@router.get('/all/', response_model = list[schemas.showuser])
def get_all_users(db : Session = Depends(get_db)):
    try:
        users = db.query(models.Utilisateur).filter().all()
        return users
    except Exception as e:
        return HTTPException(404, detail=str(e))


#Returns specific User according to id
@router.get('/{id}/',response_model = schemas.showuser)
def get_user(id:int,db :Session = Depends(get_db)):
    try:
        user = db.query(models.Utilisateur).filter(models.Utilisateur.id == id).first()
        if not user:
            raise HTTPException(404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(404, detail=str(e))


#Add a new User
@router.post('/add/', response_model = schemas.showuser)
def add_user(request:schemas.createuser ,db :Session = Depends(get_db)):
    try:
        hashed_password = request.Password + 'hash'
        new_user = models.Utilisateur(Nom=request.Nom, 
                                      Email=request.Email,
                                      HashedPassword = hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        return HTTPException(404, detail = str(e))

#Modify a User
@router.post('/{id}/modify/', response_model = schemas.showuser)
def modify_user(request : schemas.showuser, id : int, db : Session = Depends(get_db)):
    try:
        user_to_update = db.query(models.Utilisateur).filter(models.Utilisateur.id == id).first()
        updated_user = request.dict(exclude_unset=True)
        for key, value in updated_user.items():
            setattr(user_to_update, key, value)
        db.add(user_to_update)
        db.commit()
        db.refresh(user_to_update)

        return user_to_update
    except Exception as e:
        return HTTPException(404, detail=str(e))


#Delete a User
@router.delete('/{id}/delete/')
def delete_user(id : int, db : Session = Depends(get_db)):
    user_to_delete = db.query(models.Utilisateur).filter(models.Utilisateur.id == id).first()
    db.delete(user_to_delete)
    db.commit()

    return {"message" : "User deleted"}

