from fastapi import APIRouter,Depends,HTTPException
from db import database
from models import models
from schemas import schemas
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from utils import get_hashed_password
from deps import get_current_user

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
        raise HTTPException(400, detail=str(e))


#Returns specific User according to id
@router.get('/{id}/',response_model = schemas.showuser)
def get_user(id:int,db :Session = Depends(get_db)):
    try:
        user = db.query(models.Utilisateur).filter(models.Utilisateur.id == id).first()
        if not user:
            raise HTTPException(400, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(400, detail=str(e))


#Add an Admin -> User with userType set to True
@router.post('/add/', response_model = schemas.showuser)
def add_admin(request : schemas.addAdmin, db :Session = Depends(get_db)):
    try:
        hashed_password = get_hashed_password(request.Password)
        new_admin = models.Utilisateur(Nom=request.Nom, 
                                      Email=request.Email,
                                      UserType = True,
                                      HashedPassword = hashed_password)
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return new_admin
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

#Modify a User
@router.post('/{id}/modify/', response_model = schemas.showuser)
def modify_user(request : schemas.showuser, id : int, db : Session = Depends(get_db)):
    try:
        user_to_update = db.query(models.Utilisateur).filter(models.Utilisateur.id == id).first()
        if not user_to_update:
            raise HTTPException(400, detail="User not found")
        updated_user = request.dict(exclude_unset=True)
        for key, value in updated_user.items() :
            setattr(user_to_update, key, value)
        db.add(user_to_update)
        db.commit()
        db.refresh(user_to_update)

        return user_to_update
    except Exception as e:
        raise HTTPException(400, detail=str(e))


#Delete a User
@router.delete('/{id}/delete/')
def delete_user(id : int, db : Session = Depends(get_db)):
    try:
        user_to_delete = db.query(models.Utilisateur).filter(models.Utilisateur.id == id).first()
        if not user_to_delete:
            raise HTTPException(400, detail="User not found")
        db.delete(user_to_delete)
        db.commit()

        return JSONResponse({
            "message" : "User deleted"
        })
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))


#Get User's favorite Points
@router.get('/{id}/favorites', response_model = list[schemas.point])
def get_favorites(id : int, db : Session = Depends(get_db)):
    try:
        user = db.query(models.Utilisateur).filter(models.Utilisateur.id == id).first()
        if not user:
            raise HTTPException(status_code = 404, detail = "User not found")
        user_favorite_points = user.favoris
        return user_favorite_points
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

#Get User's notifications
@router.get("/{id}/notifications", response_model=list[schemas.notification])
def get_notifications(id : int, db : Session = Depends(get_db)):
    try:
        user = db.query(models.Utilisateur).filter(models.Utilisateur.id == id).first()
        if not user:
            raise HTTPException(status_code = 404, detail = "User not found")
        notifications = user.notifications
        return notifications
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))