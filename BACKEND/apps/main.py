import uvicorn
from fastapi import FastAPI

from fastapi import Request
from fastapi import FastAPI

from db import database
from models import models

from routers import pointInteret, theme, evenement, categorie, moyenTransport, lieu, commentaire

from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

app.include_router(pointInteret.router)
app.include_router(evenement.router)

app.include_router(categorie.router)
app.include_router(lieu.router)
app.include_router(theme.router)
app.include_router(moyenTransport.router)
app.include_router(commentaire.router)


if __name__ == '__main__':
    uvicorn.run(app, port=5001)