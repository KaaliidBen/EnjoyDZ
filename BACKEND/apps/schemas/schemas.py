from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class lieu(BaseModel):
    id : Optional[int]
    Nom : str
    Description : str
    DateOuverture : datetime
    DateFermeture : datetime
    
    class Config():
        orm_mode = True


class theme(BaseModel):
    id : Optional[int]
    Nom : str

    class Config():
        orm_mode = True


class categorie(BaseModel):
    id : Optional[int]
    Nom : str

    class Config():
        orm_mode = True


class pointCreate(BaseModel):
    Nom:str
    Description:str
    class Config(): 
        orm_mode=True

class showPoint(BaseModel):
    Nom:str
    Description :str

    class Config(): 
        orm_mode=True 

class evenement(BaseModel):
    Nom : str
    Description : str
    Horaire_id : Optional[int]
    point_id : int

    class Config():
        orm_mode = True


class showTransport(BaseModel):
    id : int
    Type : str
    
    class Config():
        orm_mode=True

class showuser(BaseModel):
    id:int
    Nom:str
    Email:str
    UserType:bool
    token:str 
    class Config():
        orm_mode=True

class createuser(BaseModel):
    Nom:str
    Email:str 
    token:str 
    class Config():
        orm_mode=True

class Token(BaseModel):
    id_token:str

class Access_token(BaseModel):
    token:str

class Login(BaseModel):
    username:str
    password:str

class TokenData(BaseModel):
    email: Optional[str] = None
