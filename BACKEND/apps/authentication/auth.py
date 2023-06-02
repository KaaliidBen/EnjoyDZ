from google.auth import crypt
from google.auth import jwt
from . import valid
import os
from fastapi import FastAPI, Depends, status, Request, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from db import database
from models import models
from schemas import schemas


get_db = database.get_db


myapp = FastAPI()


CREDENTIALS_EXCEPTION = valid.CREDENTIALS_EXCEPTION


# OAuth settings
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID') or None
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET') or None
if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise BaseException('Missing env variables')

# Set up OAuth
config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID,
               'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'prompt': "consent",
                   'scope': 'openid email profile'},
)

# Set up the middleware to read the request session
SECRET_KEY = os.environ.get('SECRET_KEY') or None
if SECRET_KEY is None:
    raise 'Missing SECRET_KEY'
myapp.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Frontend URL:
FRONTEND_URL = os.environ.get(
    'FRONTEND_URL') or 'http://127.0.0.1:5000/auth/callback'


# --------------------------------------------------------------------------------------------------------------------------------

@myapp.get('/login')
async def login(request: Request):
    redirect_uri = FRONTEND_URL  # This creates the url for our /auth endpoint
    return await oauth.google.authorize_redirect(request, redirect_uri)


@myapp.get('/callback', response_model=Schemas.showuser)
async def callback(request: Request, db: Session = Depends(get_db)):

    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1> callback function error {error.error}</h1>')
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    # new_user = db.query(models.user).filter(
    #     models.user.email == user.email).first()
    # if new_user:
    #     new_user.token = token.get('id_token')
    #     #
    #     db.commit()
    #     return new_user

    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                     detail=f'user not found')
    return token


@myapp.get('/signup')
async def login(request: Request):
    # This creates the url for our /auth endpoint
    redirect_uri = 'http://127.0.0.1:5000/auth/callback2'
    return await oauth.google.authorize_redirect(request, redirect_uri)


@myapp.get('/callback2')
async def callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1> callback2 function error {error.error}</h1>')
    user = token.get('userinfo')
    # new_user = db.query(models.user).filter(
    #     models.user.email == user.email).first()
    # if new_user:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail=f'user not found')
    # return JSONResponse({'token':  jwt.decode(token.get('access_token'), certs=public_certs)})
    return token


@myapp.get('/')
async def root():
    return HTMLResponse(
        '<body><a href="/auth/login">Log In</a> <a href="/auth/signup">singup</a></body>')
