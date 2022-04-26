# Librairies
import uvicorn
import json
import random
import helpers
import secrets
import requests
import datetime
import pandas as pd
from helpers import *
from requests import *
from typing import List
from pickle import FLOAT
from fastapi import FastAPI
from fastapi import Header
from fastapi import Depends
from typing import Optional
from pydantic import BaseModel
from jose import JWTError, jwt
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.responses import JSONResponse
from fastapi import Body,status
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#   datas
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
  "alice": {
    "username":"alice",
    "password": pwd_context.hash("wonderland"),
    "disabled": False},

  "bob": {
    "username": "bob",
    "password":pwd_context.hash("builder"),
    "disabled": False},

  "clementine" : {
    "username ": "clementine",
    "password" :pwd_context.hash("mandarine"),
    "disabled" : False},

   "admin": {
    "username ": "admin",
    "password" :pwd_context.hash("4dm1N"),
    "disabled" : False}
}


# On charge les données

API_URL = "http://127.0.0.1:8000"

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#    Functions
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------


api = FastAPI(title="Détecteur fr fraudes",
    description="Cette API interroge des modèles de machine learning pour déterminer si une transaction est frauduleuse ou pas.",
    version="1.0.1")


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Message de bienvenue
@api.get('/')
def get_index():
    return {'Bienvenue au détecteur de transactions frauduleuses !'}



# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Authentification du client

class Token(BaseModel):
    access_token: str
    token_type: str
    message: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    disabled: Optional[bool] = None


class User_me(BaseModel):
    username: str
    password: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    password: str


def verify_password(plain_password, password):
    return pwd_context.verify(plain_password, password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    print('ici')
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    print('test_current')
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        print(username)
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    print('ici 1')
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@api.post("/token", response_model=Token,tags=['login'])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer","message":f"Bienvenue {user.username} !"}


@api.get("/users/me/", response_model=User_me,tags=['infos'])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    user = {'username':current_user.username,
	    'password':'*******************',
	    'disabled':current_user.disabled}
    return user



@api.get("/users/me/ressources/",tags=['infos'])
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"ressources": "Nature de votre transaction : ...", "owner": current_user.username}]


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Predictions

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class FraudMeasurementData(BaseModel):
  var1 : float
  var2: float


class FraudTypePredictionProba(BaseModel):
  isFraud : float
  notFraud : float


class FraudTypePredictionResponse(BaseModel):
  predicted_class : int
  proba : FraudTypePredictionProba 


class FraudTypePerfResponse(BaseModel):
    recall:float
    accuracy:float


@api.post("/PredictionModelKnn", tags = ['prediction'], response_model=FraudTypePredictionResponse)
async def make_prediction_knn(data : FraudMeasurementData) :

  return {
      'predicted_class' : 1,
      'proba' : {
          'isFraud' : 0.4,
          'notFraud' : 0.6,
      },
  }


@api.post("/PredictionModelLogreg", tags = ['prediction'], response_model=FraudTypePredictionResponse)
async def make_prediction_logreg(data : FraudMeasurementData) :

  return {
      'predicted_class' : 1,
      'proba' : {
          'isFraud' : 0.4,
          'notFraud' :0.6,
      },
  }



@api.post("/PerfKnn", tags = ['performances'], response_model=FraudTypePerfResponse)
async def give_performances_knn() :

  return {
      'recall' : 0.7,
      'accuracy' : 0.7
  }


@api.post("/PerfLogReg", tags = ['performances'], response_model=FraudTypePerfResponse)
async def give_performances_logreg() :

  return {
      'recall' : 0.7,
      'accuracy' : 0.7
  }

