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