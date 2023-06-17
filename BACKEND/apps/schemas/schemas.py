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

class transport(BaseModel):
    id : Optional[int]
    Type : str
    
    class Config():
        orm_mode=True

class point(BaseModel):
    id : Optional[int]
    Nom : str
    Description : str
    Wilaya : str
    Region : str
    TempsOuverture : str
    TempsFermeture : str
    Latitude : float
    Longitude : float
    themes : Optional[theme]
    categories : Optional[categorie]
    moyenTransport : Optional[list[transport]]

    class Config(): 
        orm_mode=True 

class evenement(BaseModel):
    id : Optional[int]
    Nom : str
    Description : str
    DateDebut : datetime
    DateFin : datetime
    evPoint : point

    class Config():
        orm_mode = True


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
    #token : str
    Email : str
    #token : str
    Password : str
    class Config():
        orm_mode=True

class addAdmin(BaseModel):
    Nom : str
    Email : str
    Password : str
    class Config():
        orm_mode = True

class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None

#class Token(BaseModel):
#    id_token : str

class Token(BaseModel):
    user_id : int
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


class notification(BaseModel):
    id : Optional[int]
    Content : str
    Read : bool
    user_id : int
    class Config():
        orm_mode=True