import uvicorn
from fastapi import FastAPI,Depends
from fastapi.responses import HTMLResponse

from fastapi import Request
from fastapi import FastAPI

from db import database
from models import models

from routers import pointInteret, theme, evenement, categorie, moyenTransport, lieu,user,authenticate

from sqlalchemy.orm import Session

from authentication.valid import get_current_user_email


app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

app.include_router(user.router)
app.include_router(authenticate.router)

app.include_router(pointInteret.router)
app.include_router(theme.router)
app.include_router(evenement.router)
app.include_router(moyenTransport.router)

app.include_router(categorie.router)
app.include_router(lieu.router)

@app.post('/protected')
def test(current_email: str = Depends(get_current_user_email)):
    return 'welcome to protected web'


if __name__ == '__main__':
    uvicorn.run(app, port=5000)