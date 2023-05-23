from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class elementbase(BaseModel):
    #id:int
    Nom:str
    class Config(): 
        orm_mode=True
   

class carteCreate(BaseModel):
    Nom:str


class horaire(BaseModel):
    id : int
    date_debut:datetime
    date_fin:datetime

    class Config():
        orm_mode = True

class theme(BaseModel):
    Nom:str

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
