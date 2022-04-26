#!/bin/python3

### Fichier de l'API qui permet de gérer les QCM de Datascientest
# Release 1.0.0


### Prérequis / Dépendance concernant la base de données
# La base de données est stockée dans un fichier CSV nommé 'questions.csv'
# stocké dans le même répertoire que ce fichier.
# Au moment de la rédaction de ce code, on trouve dans ce fichier les champs
# suivants :
# - `question`: l'intitulé de la question
# - `subject`: la catégorie de la question
# - `correct`: la liste des réponses correctes
# - `use`: le type de QCM pour lequel cette question est utilisée
# - `responseA`: réponse A
# - `responseB`: réponse B
# - `responseC`: réponse C
# - `responseD`: la réponse D (si elle existe)
# - `remark` : remarques
# Tous les champs sont de type string non formaté.

"""
Description de l'API : L'API permet de réaliser des opérations sur la base de données des QCM.
L'API permet de réaliser les opérations suivantes :
- Interroger un point de terminaison 'welcome'.
- Interroger un point de terminaison pour vérifier que l'API est fonctionnelle.
- Interroger un point de terminaison pour obtenir les usages et les sujets en base.
- Interroger un point de terminaison pour obtenir une série de 5, 10 ou 20 questions en fonction
  d'un usage et d'une sélection de catégories.
- Avec un accès administrateur (mdp exigé), créer une nouvelle question dans la base de données. 

Droits d'accès :
- L'accès aux opérations de consultation nécessite d'utiliser un compte de consultation.
- L'accès aux opérations d'écriture en base nécessite d'utiliser un compte d'administrateur.

Méthodes utilisées :
- GET
- PUT

Base de données :
- Stockée dans le fichier questions.csv dans le même répertoire que le fichier python.
- Base entièrement chargée en DataFrame (petite taille) et réécrite dans le fichier si ajout
  d'une question.

Variables globales :
- FILE_DB : Contient le nom du fichier de bse de données.
- API_URL : URL et port de l'API en localhost.
"""

import pandas as pd
import numpy as np
from fastapi import FastAPI, Header, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import requests
import re
import datetime


########################
### CHARGEMENT / SAUVEGARDE DE LA BASE DE DONNEES
# Stockage de la base de données : fichier questions.csv.
# Chargement de la base de données : en totalité dans un DataFrame pandas questions.
# Enregistrement de la base de données : sauvegarde du DataFrame dans le fichier après chaque ajout de question.

# Initialisation du DataFrame de la base de données
FILE_DB = 'questions.csv'

def charger_db(filename=FILE_DB) :
    """Charge la base de données depuis le fichier.
       Retourne le dataframe.
    """
    return pd.read_csv(FILE_DB)

def sauver_db(df, filename=FILE_DB) :
    """Sauve le DataFrame base de données dans le fichier.
       Réécrit entièrement le fichier (très petite bdd).
       Renvoie le code retour de la fonction d'écriture.
    """
    return df.to_csv(FILE_DB, sep=',', index=False)

questions = charger_db()


########################
### CLASSES POUR UTILISER L'API (en corps de requête)

# Classe New_question : Uploader une question dans la base de données
class New_question(BaseModel):
    """Classe pour uploader une nouvelle question dans la base de données.
    """
    question:   str
    subject :   str
    correct :   str
    use :       str
    responseA : str
    responseB : str
    responseC : str
    responseD : str
    remark :    Optional[str] = None


class Query_params(BaseModel):
    """Classe pour passer les paramètres pour obtenir un set de questions pour un usage et un ou plusieurs thème(s).
    """
    quantity : int
    use     : str
    subject : Optional[List[str]] = []


########################
### CREATION DE L'API

API_URL = 'http://127.0.0.1:8000'

# Instanciation de l'API
api = FastAPI(
    title="API de gestion des QCM",
    description="L'API permet de réaliser des opérations sur la base de données des QCM.",
    version="1.0.0",
    openapi_tags=[
       {
           'name': 'public',
           'description': 'public query functions'
       },
       {
           'name': 'admin',
           'description': 'admin functions (password required)'
       }
    ])


########################
### GESTION DES EXCEPTIONS

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


########################
### GESTION DES DROITS
# Liste des utilisateurs avec les droits de lecture
READERS_ACCOUNTS = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine"
}

# Liste des utilisateurs avec les droits d'écriture (admin)
WRITERS_ACCOUNTS = {
    "admin": "4dm1N"
}

# upload des données dans des DataFrames
readers_accounts = pd.DataFrame({'login': list(READERS_ACCOUNTS.keys()), 'password': list(READERS_ACCOUNTS.values())})
writers_accounts = pd.DataFrame({'login': list(WRITERS_ACCOUNTS.keys()), 'password': list(WRITERS_ACCOUNTS.values())})

# Fonction extract_login_pwd : Fonction d'extraction et de test de format du login et du mot de passe
def extract_login_pwd(authorization) :
    import re

    login = ''
    password = ''

    def raise_format_error(code) :

        # code is passed only for debug use (unused)
            raise MyException(
                status_code=490,
                name='Error - Invalid format for login and password',
                date=str(datetime.datetime.now()),
                message="Valid format is 'authorize: Basic username:password'"
                )

    try :
        # Test de présence du premier token
        if authorization[:6] == 'Basic ' :
            authorization = authorization[6:]
        else :
            raise_format_error(1)

        # "Ecarter" les blancs après 'Basic'
        while authorization[0]==' ' :
            authorization = authorization[1:]

        # S'il reste des blancs, erreur de format
        tokens = re.split(' ', authorization)
        if len(tokens) != 1 :
            raise_format_error(2)
            return

        # Isoler le login & le password. Si 2 caractères ':', erreur de format.
        tokens = re.split(':', authorization)
        if len(tokens) != 2 :
            raise_format_error(3)
            return

        login = tokens[0]
        password = tokens[1]

        # Si pas d'erreur de format, retourner login et password
        return login, password

    except :
        raise_format_error('Final')


# Fonction are_writing_rights_ok : Vérifier les droits d'écriture. Lève une exception si les droits sont KO.
#                                  Sinon, renvoie True.
def are_writing_rights_ok(login, password) :
    """Contrôle si le couple login, password possède les droits d'écriture.
       Si ce n'est pas le cas, une exception est levée. Sinon, la fonction retourne True.
    """

    if ((login not in writers_accounts.login.to_list())
          & (login in readers_accounts.login.to_list())) :
        raise MyException(
            status_code=492,
            name='Error - Read-only account',
            date=str(datetime.datetime.now()),
            message='This account allows to query, but not to write in the database.'
            )
    elif ((login not in writers_accounts.login.to_list())
            & (login not in readers_accounts.login.to_list())) :
        raise MyException(
            status_code=491,
            name='Error - Unknown account',
            date=str(datetime.datetime.now()),
            message="This account does not exist."
            )
    elif ((login in writers_accounts.login.to_list())
            & (writers_accounts.loc[writers_accounts[writers_accounts.login==login].index
              .to_list()[0], 'password'] != password)) :
        raise MyException(
            status_code=495,
            name='Error - Invalid password',
            date=str(datetime.datetime.now()),
            message="This password is invalid."
            )
    else :     # is_admin !
        return True


# Fonction are_querying_rights_ok : Vérifier les droits de requêter l'API. Lève une exception si les droits 
#                                   sont KO. Sinon, renvoie True.
def are_reading_rights_ok(login, password) :
    """Contrôle si le couple login, password possède les droits de requêter l'API.
       Si ce n'est pas le cas, une exception est levée. Sinon, la fonction retourne True.
    """

    # On travaille sur la base concaténée des accès read et write car un accès write
    # permet automatiquement un accès read.
    all_accounts = pd.concat([readers_accounts, writers_accounts],
                             ignore_index=True)

    if login not in all_accounts.login.to_list() :
       raise MyException(
            status_code=491,
            name='Error - Unknown account',
            date=str(datetime.datetime.now()),
            message="This account does not exist."
            )
    elif (login in all_accounts.login.to_list())  \
            & (all_accounts.loc[all_accounts[all_accounts.login==login].index
              .to_list()[0], 'password'] != password) :
        raise MyException(
            status_code=495,
            name='Error - Invalid password',
            date=str(datetime.datetime.now()),
            message="This password is invalid."
            )
    else :     # is_authorized !
        return True


########################
### GESTION DES API

# Erreurs retournées pour les endpoint en accès lecture sans paramètres
responses_reader = {
    200: {"description": "OK"},
    490: {"description": "Invalid format for login and password"},
    491: {"description": "Unknown account"},
    495: {"description": "Invalid password"}
}

# Erreurs retournées pour les endpoint en accès lecture avec paramètres
responses_reader_param = {
    200: {"description": "OK"},
    480: {"description": "Invalid parameters"},
    490: {"description": "Invalid format for login and password"},
    491: {"description": "Unknown account"},
    495: {"description": "Invalid password"}
}

# Erreurs retournées pour les endpoint en accès écriture (comprend les doits en lecture)
responses_writer = {
    200: {"description": "OK"},
    480: {"description": "Invalid parameters"},
    490: {"description": "Invalid format for login and password"},
    491: {"description": "Unknown account"},
    492: {"description": "Read-only account"},
    495: {"description": "Invalid password"}
}


# GET / Renvoie un message de bienvenue
@api.get('/', tags=['public'], name='Welcome message',
              responses=responses_reader)
def get_index(authorize=Header(None, description='Basic username:password')) :

    """Returns greetings
    """

    # Récupérer les login + password dans le header + test de format
    login, password = extract_login_pwd(authorize)

    # Si les droits sont ok, renvoyer le set de questions
    if are_reading_rights_ok(login, password) :
        return {'greetings':'Welcome on my api !'}


# GET / Vérifie que l'interface est fonctionnelle
@api.get('/working', tags=['public'],
                     name='Working status',
                     responses=responses_reader)
def get_working(authorize=Header(None, description='Basic username:password')):

    """Retourne un statut de fonctionnement (0 : ne fonctionne pas, 1 : fonctionne)
    """

    # Récupérer les login + password dans le header + test de format
    login, password = extract_login_pwd(authorize)

    # Si les droits sont ok, renvoyer le set de questions
    if are_reading_rights_ok(login, password) :
        response = requests.get(url = f"{API_URL}/working")
        # Si l'interface renvoie un status_code 490, elle fonctionne
        if response.status_code == 490 :
            working_status = 1
        else :
            working_status = 0
        return {'working status': working_status}


# GET / Obtenir la liste des valeurs en base pour le type (champs 'use') et le sujet ('subject')
@api.get('/existing_values', tags=['public'],
                             name='Get uses and subjects in the database',
                             responses=responses_reader)
def get_existing_values(authorize=
                        Header(None,
                        description='Basic username:password')
                        ) :

    """Retourne la liste des types ('use') et des thèmes ('subject') disponibles en base de données.
    """

    # Récupérer les login + password dans le header + test de format
    login, password = extract_login_pwd(authorize)

    # Si les droits sont ok, renvoyer le set de questions
    if are_reading_rights_ok(login, password) :
        return {'use' : list(questions['use'].unique()),
                'subject' : list(questions['subject'].unique())
              }


# PUT / Obtenir un set de questions
@api.put('/questions', tags=['public'],
                       name='Get a set of questions',
                       responses=responses_reader_param)
def get_questions(query_params: Query_params,
                  authorize=Header(None,
                                   description='Basic username:password'),
                  ):
    """Retourne un jeu de questions dont la taille maximale est à préciser dans la requête (5, 10 ou 20).
       Si aucun match, un dictionnaire vide est renvoyé.
       Il faut passer un login et un mot de passe en entête.
       Il faut préciser l'usage (obligatoire) et les sujets (optionnel) dans le corps de la requête.
       Si les sujets ne sont pas précisés, tous seront sélectionnés.
       Pour avoir connaissance des sujets en base, rdv sur le point de terminaison '/existing_values'.
    """

    qty = query_params.quantity
    use = query_params.use
    sub = query_params.subject

    if sub == [] :
        sub = list(questions['subject'].unique())

    # Récupérer les login + password dans le header + test de format
    login, password = extract_login_pwd(authorize)

    # Limitation à 5, 10 ou 20 questions
    if qty not in [5, 10, 20] :
        raise MyException(
            status_code=480,
            name='Error - Invalid(s) parameter(s)',
            date=str(datetime.datetime.now()),
            message="Check authorized values in endpoint's description. Check "
                    "available values in the database at the endpoint '/existing_values'."
        )

    # Si les droits sont ok, renvoyer le set de questions
    try :
        if are_reading_rights_ok(login, password) :
            selection = questions[(questions.use==use) & (questions.subject.apply(lambda x: x in sub))]
            nb = selection.shape[0]
            # Gérer les sélections trop petites ou inexistantes (ne pas déclencher d'erreur)
            if nb==0 :
                return {}
            elif nb < qty :
                qty = nb

            # Sélectionner les questions
            select = selection.sample(n=qty)
            select = select.replace(np.nan, '')
            return select.to_dict('records')

    except IndexError:
        raise MyException(
            status_code=480,
            name='Error - Invalid(s) parameter(s)',
            date=str(datetime.datetime.now()),
            message="Check authorized values in endpoint's description. Check "
                    "available values in the database at the endpoint '/existing_values'."
        )

    except ValueError:
        raise MyException(
            status_code=480,
            name='Error - Invalid(s) parameter(s)',
            date=str(datetime.datetime.now()),
            message="Check authorized values in endpoint's description. Check "
                    "available values in the database at the endpoint '/existing_values'."
        )


@api.put('/add_question', tags=['admin'],
                name='Save a new question in the database (restricted access)',
                responses=responses_writer)
def put_add_question(new_question : New_question,
                     authorize=Header(None,
                               description='Basic username:password')
                     ):

    """Ajoute une question dans la base de données.
       Condition : disposer des droits en écriture (admin).
       Les informations d'authentification sont passées dans le header.
       Les informations de la question sont passées dans le corps de la requête.
    """


    global questions      # La variable va être modifiée dans la fonction


    # Récupérer les login + password dans le header + test de format
    login, password = extract_login_pwd(authorize)

    # Contrôle des droits et ajout en base si autorisé
    if are_writing_rights_ok(login, password) :

        # Formatter la nouvelle question 'pour' append le DataFrame
        col_names = questions.columns.to_list()

        new_q = []
        for col in col_names :
            if col == 'question' :
                new_q.append(new_question.question)
            elif col == 'subject' :
                new_q.append(new_question.subject)
            elif col == 'use' :
                new_q.append(new_question.use)
            elif col == 'correct' :
                new_q.append(new_question.correct)
            elif col == 'responseA' :
                new_q.append(new_question.responseA)
            elif col == 'responseB' :
                new_q.append(new_question.responseB)
            elif col == 'responseC' :
                new_q.append(new_question.responseC)
            elif col == 'responseD' :
                new_q.append(new_question.responseD)
            elif col == 'remark' :
                if new_question.remark is None :
                    new_q.append(np.nan)
                else :
                    new_q.append(new_question.remark)
            else : pass

        new_q = pd.DataFrame(new_q, index=col_names).T

        # Append le DataFrame
        questions = pd.concat([questions, new_q], ignore_index=True)

        # Enregistrer la base de données
        print(sauver_db(questions))

        # Renvoyer l'enregistrement ajouté
        new_q = new_q.replace(np.nan, '')
        return new_q.to_dict('records')

