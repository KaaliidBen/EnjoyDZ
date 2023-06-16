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

class point(BaseModel):
    id : Optional[int]
    Nom : str
    Description : str
    Wilaya : str

    class Config(): 
        orm_mode=True 

class evenement(BaseModel):
    id : Optional[int]
    Nom : str
    Description : str
    DateDebut : datetime
    DateFin : datetime
    point_id : int

    class Config():
        orm_mode = True


class transport(BaseModel):
    id : Optional[int]
    Type : str
    
    class Config():
        orm_mode=True

class showuser(BaseModel):
    id : Optional[int]
    Nom : str
    Email : str
    UserType : Optional[bool]
    #token : Optional[str] 
    HashedPassword : str
    class Config():
        orm_mode=True

class createuser(BaseModel):
    Nom : str
    Email : str 
    #token : str 
    Password : str
    class Config():
        orm_mode=True

class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None

#class Token(BaseModel):
#    id_token : str

class Token(BaseModel):
    access_token : str
    refresh_token : str
    
class Access_token(BaseModel):
    token : str

class Login(BaseModel):
    username:str
    password:str

class TokenData(BaseModel):
    email: Optional[str] = None


class commentaire(BaseModel):
    id : Optional[int]
    user_id : Optional[int]
    point_id : Optional[int]
    Content : str

    class Config():
        orm_mode = True
