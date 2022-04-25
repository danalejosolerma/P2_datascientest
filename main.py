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

responses = ['question','responseA', 'responseB', 'responseC', 'responseD']


nb_questions = [5, 10, 20]


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

db_questions = pd.read_csv('questions.csv')

API_URL = "http://127.0.0.1:8000"

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#    Functions
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------


api = FastAPI(title="Generateur de questionnaires",
    description="Cette API interroge une base de données pour retourner une serie de questions.",
    version="1.0.1")


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Message de bienvenue
@api.get('/')
def get_index():
    return {'Bienvenue à votre test. Nous vous souhaitons bonne chance !'}



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


@api.get("/users/me/", response_model=User,tags=['infos'])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    print(current_user)
    return current_user



@api.get("/users/me/ressources/",tags=['infos'])
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"ressources": "test reussi", "owner": current_user.username}]


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class response_mondel_demande(BaseModel):
    question: str
    responseA: str
    responseB: str
    responseC: Optional[str]
    responseD: Optional[str]



# Génération de questionnaires 
class Demande(BaseModel):
    use: Optional[str] = db_questions.use[random.choice(range(10))]
    subject: Optional[str] = db_questions.subject[random.choice(range(10))]
    number: Optional[int]=random.choice([5,10,20])

@api.post('/test',tags=['demandes'])
async def passer_test(test:Demande):
    """
    Cette fonction permet de générer un questionnaire en fonction des arguments fournis !
    """

    # l'utilisateur doit pouvoir choisir un type de test et une ou plusieurs catégories
    uniques_subjects = db_questions.subject.unique()
    if test.subject in uniques_subjects:
        choix_categories = test.subject
    else : choix_categories=None
    

    if ((choix_categories == None) or (test.use not in db_questions.use.tolist())):
        raise HTTPException(status_code = 404, detail = 'La combinaison catégorie - type de test est incorrecte.')

    elif test.number not in nb_questions:
        raise HTTPException(status_code=404, detail="Choisir un nombre parmi 5, 10 et 20")

    else:
       
        db = db_questions.loc[db_questions.subject == test.subject]

        db = db.loc[db.use == test.use]
        
        # Ici on a des Nan : on les remplace par 'Je ne sais pas' 
        db = db.fillna('Je ne sais pas')

        if len(db):
            if test.number > len(db):
                questions = db[responses].to_dict(orient = 'records')
                
            else:
                questions = db.sample(n = test.number)[responses].to_dict(orient = 'records') # Nature aléatoire
        else:
            questions = {
                'message' : "Nous ne pouvons pas satisfaire votre demande. Veuillez réessayer ulterieurement!."
            }
    return questions


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Ajout d'une nouvelle question par l'administrateur
class Question(BaseModel):
    question: str
    subject: str
    use: str
    correct: str
    responseA: str
    responseB: str
    responseC: Optional[str]
    responseD: Optional[str]
    remark:Optional[str]

@api.post('/add_questions',tags=['add'])
def add_question(question:Question, username:str, password:str):

    """ Un administrateur peut ajouter une question grâce à son identifiant et son mot de passe.
    """
    if (username =='admin') and (password == '4dm1N'):

        global db_questions
        new_question={}


        new_question['question']= question.question,
        new_question['subject']= question.subject,
        new_question['use']= question.use,
        new_question['correct']= question.correct,
        new_question['responseA']= question.responseA,
        new_question['responseB']= question.responseB,
        new_question['responseC']= question.responseC,
        new_question['responseD']= question.responseD,
        new_question['remark']=question.remark


        new_question = pd.DataFrame(new_question)


        db_questions = pd.concat([new_question,db_questions]).reset_index(drop = True)

        return {
        'message' : "Votre question a bien été ajoutée.",
        'question ajoutée' : db_questions.head(1)
        }
    else:
        return {
        'message' : "Echec d'identification ! Vous ne pouvez pas effectuer cette opération."
        }

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------





   