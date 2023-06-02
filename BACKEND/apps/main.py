import uvicorn
from fastapi import FastAPI

from fastapi import Request
from fastapi import FastAPI

from db import database
from models import models

<<<<<<< HEAD
from routers import pointInteret, theme, evenement, categorie, moyenTransport, lieu,user,authenticate
=======
from routers import pointInteret, theme, evenement, categorie, moyenTransport, lieu, commentaire
>>>>>>> b3413d25f7293a2a6b375d667c503c39494cba2a

from sqlalchemy.orm import Session

from authentication.valid import get_current_user_email


app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

app.include_router(user.router)
app.include_router(authenticate.router)

app.include_router(pointInteret.router)
app.include_router(evenement.router)

app.include_router(categorie.router)
app.include_router(lieu.router)
app.include_router(theme.router)
app.include_router(moyenTransport.router)
app.include_router(commentaire.router)

@app.post('/protected')
def test(current_email: str = Depends(get_current_user_email)):
    return 'welcome to protected web'


if __name__ == '__main__':
    uvicorn.run(app, port=5000)