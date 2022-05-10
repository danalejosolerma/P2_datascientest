# Librairies
import uvicorn
import json
import joblib
import sklearn
import random
import helpers
import secrets
import requests
import pandas as pd
from helpers import *
from requests import *
from typing import List
from pickle import FLOAT
from typing import Optional
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sklearn.metrics import recall_score, accuracy_score
from fastapi import Depends,FastAPI, Header,HTTPException, Body,status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm,HTTPBasic, HTTPBasicCredentials,HTTPBearer



# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#   datas
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

fake_users_db = {
    "alice": {
        "username":"alice",
        "password": pwd_context.hash("wonderland"),
        "disabled": False},
    "clementine": {
        "username":"clementine",
        "password": pwd_context.hash("mandarine"),
        "disabled": False},
    "bob": {
        "username": "bob",
        "password":pwd_context.hash("builder"),
        "disabled": False},
    "admin": {
        "username ": "admin",
        "password" :pwd_context.hash("4dm1N"),
        "disabled" : False}
}


# On charge les données

API_URL = "http://127.0.0.1:8000"

SECRET_KEY = "d4ae6cad92f07dc5f251c0362fc873f2cd76560cfc4f3bba65b221142707ed1c"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#    Functions
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------


api = FastAPI(title="Détecteur de fraudes",
    description="Cette API interroge des modèles de machine learning pour déterminer si une transaction est frauduleuse ou pas.",
    version="1.0.1")


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Message de bienvenue
@api.get('/')
def get_index():
    return {'Message':'Bienvenue au détecteur de transactions frauduleuses !'}


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Gestion des exceptions

# Définition d'une nouvelle exception
class MyException(Exception):
    def __init__(self,
                 status_code: int,
                 name : str,
                 date: str,
                 message: str):
        self.status_code = status_code
        self.name = name
        self.date = date
        self.message = message


# Indiquer à FastAPI comment réagir quand l'exception est soulevée
@api.exception_handler(MyException)
def MyExceptionHandler(
    request: Request,
    exception: MyException
    ):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            'url': str(request.url),
            'name': exception.name,
            'message': exception.message,
            'date': exception.date
        }
    )
    
responses_reader = {
    200: {"description": "OK"},
    401: {"description": "Unauthorized"},
    422: {"description": "Bad parameters"},
    403: {"description": "Unknown account"}
}
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
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(signin: str = Depends(oauth2_scheme)):
    credentials_exception =  MyException(
            status_code=401,
            name='Could not validate credentials ! You are not authenticated',
            date=str(datetime.now()),
            message="Sign in'"
        )

    try:
        payload = jwt.decode(signin, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
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
    if current_user.disabled:
        raise MyException(
            status_code=401,
            name='Unauthorized',
            date=str(datetime.now()),
            message="Inactive user'"
        )
    return current_user


@api.post("/signin", response_model=Token,tags=['login'])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise MyException(
            status_code=401,
            name='Error - Invalid format for login and password',
            date=str(datetime.now()),
            message="Usernames must be in lowercase'"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer","message":f"Bienvenue {user.username} !"}

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Predictions

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class FraudMeasurementData(BaseModel):
  purchase_value : float
  purchase_time=datetime.fromtimestamp(1528794338)
  signup_time=datetime.fromtimestamp(1528794326)


class FraudTypePredictionProba(BaseModel):
  isFraud : float
  notFraud : float


class FraudTypePredictionResponse(BaseModel):
  predicted_class : int
  proba : FraudTypePredictionProba 


class FraudTypePerfResponse(BaseModel):
    recall:float
    f1_score:float

with open('/my_server/features.json', 'r') as f :
    features = json.load(f)

knn_classifier = joblib.load('/my_server/knn_classifier.joblib')
logreg_classifier = joblib.load('/my_server/logreg_classifier.joblib')


@api.get("/features",tags = ['features'])
def get_features() :
  return {
    'purchase_value' :34,
    'purchase_time': datetime.fromtimestamp(1528794326),
    'signup_time':datetime.fromtimestamp(1528794323),
  }

@api.post("/PredictionModelKnn", tags = ['prediction'], response_model=FraudTypePredictionResponse)
async def make_prediction_knn(data : FraudMeasurementData,current_user: User = Depends(get_current_active_user)) :
    try:
        data = pd.DataFrame([data.dict()])
        data['tot_time']=(data['purchase_time'] - data['signup_time']).apply(lambda t: t.total_seconds()/3600)
        data.tot_time = data.tot_time.apply(lambda x: -1/x)
        data = data[features]
        predicted_class = knn_classifier.predict(data)[0]
        predicted_proba = knn_classifier.predict_proba(data)[0].tolist()

        return {
            'predicted_class' : int(predicted_class),
            'proba' : {
                'isFraud' : predicted_proba[1],
                'notFraud' : predicted_proba[0],
            },
        }
    except IndexError:
        raise MyException(
            status_code=422,
            name='Error - Invalid(s) parameter(s)',
            date=str(datetime.now()),
            message="Check authorized values in endpoint's features. Check "
                    "available values in the database at the endpoint '/features'."
        )


@api.post("/PredictionModelLogreg", tags = ['prediction'], response_model=FraudTypePredictionResponse)
async def make_prediction_logreg(data : FraudMeasurementData,current_user: User = Depends(get_current_active_user)) :
    
    try :
        data = pd.DataFrame([data.dict()])
        data['tot_time']=(data['purchase_time'] - data['signup_time']).apply(lambda t: t.total_seconds()/3600)
        data.tot_time = data.tot_time.apply(lambda x: -1/x)
        data = data[features]
        predicted_class = logreg_classifier.predict(data)[0]
        predicted_proba = logreg_classifier.predict_proba(data)[0].tolist()
        
        return {
            'predicted_class' : int(predicted_class),
            'proba' : {
                'isFraud' : predicted_proba[1],
                'notFraud' : predicted_proba[0],
            },
        }
    
    except IndexError:
        raise MyException(
            status_code=422,
            name='Error - Invalid(s) parameter(s)',
            date=str(datetime.now()),
            message="Check authorized values in endpoint's features. Check "
                    "available values in the database at the endpoint '/features'."
        )
    
@api.post("/PerfKnn", tags = ['performances'], response_model=FraudTypePerfResponse)
async def give_performances_knn() :
    data_test = pd.read_csv('/my_server/data_test.csv')
    X_test = data_test.drop('is_fraud',axis=1)
    y_test = data_test['is_fraud']
    y_pred = knn_classifier.predict(X_test)
    score = accuracy_score(y_test,y_pred)
    rec = recall_score(y_test,y_pred)

    return {
        'recall' : rec,
        'f1_score' : score
    }


@api.post("/PerfLogReg", tags = ['performances'], response_model=FraudTypePerfResponse)
async def give_performances_logreg() :
    data_test = pd.read_csv('/my_server/data_test.csv')
    X_test = data_test.drop('is_fraud',axis=1)
    y_test = data_test['is_fraud']
    y_pred = logreg_classifier.predict(X_test)
    score = accuracy_score(y_test,y_pred)
    rec = recall_score(y_test,y_pred)

    return {
        'recall' : rec,
        'f1_score' : score
    }

