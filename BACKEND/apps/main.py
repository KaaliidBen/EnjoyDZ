import uvicorn
from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

from db import database
from models import models

from routers import pointInteret, theme, evenement, categorie, moyenTransport, lieu, user, auth, commentaire

from sqlalchemy.orm import Session


#from authentication.valid import get_current_user_email


app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)


app.include_router(user.router)
app.include_router(auth.router)
#app.include_router(authenticate.router)

app.include_router(pointInteret.router)
app.include_router(categorie.router)
app.include_router(lieu.router)
app.include_router(theme.router)
app.include_router(moyenTransport.router)
app.include_router(commentaire.router)
app.include_router(evenement.router)

#@app.post('/protected')
#def test(current_email: str = Depends(get_current_user_email)):
 #   return 'welcome to protected web'


if __name__ == '__main__':
    uvicorn.run(app, port=5000)