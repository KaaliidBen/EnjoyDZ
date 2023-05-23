import uvicorn
from fastapi import FastAPI,Depends
from fastapi.responses import HTMLResponse

from fastapi import Request
from fastapi import FastAPI

from db import database
from models import models

from routers import pointInteret, horaire, theme

from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

app.include_router(pointInteret.router)
app.include_router(horaire.router)
app.include_router(theme.router)


if __name__ == '__main__':
    uvicorn.run(app, port=5001)