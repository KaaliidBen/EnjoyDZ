from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class carteCreate(BaseModel):
    Nom:str


class horaire(BaseModel):
    id : Optional[int]
    date_debut:datetime
    date_fin:datetime

    class Config():
        orm_mode = True

class theme(BaseModel):
    id : Optional[int]
    Nom : str

    class Config():
        orm_mode = True

class categorie(BaseModel):
    Nom:str

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
    date_debut : datetime
    date_fin : datetime
    point_id : int

    class Config():
        orm_mode = True