from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from db import database
from schemas import schemas
from sqlalchemy.orm import Session
from models.models import Utilisateur
from deps import get_current_user
from utils import get_hashed_password, verify_password, create_access_token, create_refresh_token

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

get_db = database.get_db

@router.post('/signup', response_model=schemas.showuser)
async def signup(request: schemas.createuser, db : Session = Depends(get_db)):
    try:
        user = db.query(Utilisateur).filter(Utilisateur.Email == request.Email).first()
        if user is not None:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exist"
            )
        hashed_password = get_hashed_password(request.Password)
        new_user = Utilisateur(Nom=request.Nom, 
                            Email=request.Email,
                            HashedPassword = hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
         raise HTTPException(status_code = 400, detail = str(e))
    


@router.post('/login', response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), 
                db : Session = Depends(get_db)):
    email = form_data.username
    user = db.query(Utilisateur).filter(Utilisateur.Email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found for given email"
        )

    hashed_pass = user.HashedPassword
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    
    return {
        "user_id" : user.id,
        "access_token": create_access_token(user.Email),
        "refresh_token": create_refresh_token(user.Email),
    }

@router.get('/me', response_model=schemas.showuser)
async def get_me(user : schemas.showuser = Depends(get_current_user)):
    return user