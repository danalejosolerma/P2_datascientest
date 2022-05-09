#!/bin/python3

####################################
#|  Test de l'API fraud : v1.0.0
####################################


import os
import requests
import time
import numpy as np
import datetime as dt


""" Teste les fonctions d'authentification et d'autorisation de l'API Fraud.
"""


####################################
#######
####     1. DEFINITION DES VARIABLES
##          Connexion du programme à son environnement.
#

# définition de l'adresse de l'API
api_address = 'localhost'

# port de l'API
api_port = 8000

# Nom du fichier de log
log_file = '/home/ubuntu/api_test.log'

# attente du démarrage de l'API + timestamp du test
time.sleep(1)
ts = dt.datetime.now().strftime("%Y/%m/%d-%H:%M:%S")


####################################
#######
####     2. JEUX DE TEST
##          Valeurs utilisées pour les tests.
#

"""
| Le jeu de test contient des séries de N valeurs pour tester l'interface. 
| Quand elle est précisée, la valeur de 'target' correspond au résultat trouvé précédemment dans le fichier de dev
| de l'algorithme. Vérifier que la valeur est identique permet de tester la bonne intégration de l'algorithme
| et de l'API.
|
| Les autres valeurs correspondent aux features nécessaires pour calculer la prédiction.
|
| Détail du jeu de test :
|   - predict_O_in_test_set et predict_1_in_test_set : 2 jeux de valeur qui doivent aboutir à une prévision 'target'.
|                                                      Permet de vérifier la bonne intégration de l'algorithme.
|   - random_test : Test avec un jeu de valeur 'aléatoire' et cohérent.
|   - wrong_type_test : test avec un jeu de valeur qui contient de mauvais types.
|   - missing_value_test : Test avec une feature manquante.
| 
"""

# Définition du test set
test_set = {
            "predict_O_in_test_set": {
                'features': {
                    'purchase_value': 0,
                    'device_id': 'a',
                    'ip_address': 'b',
                    'purchase_time': 'c',
                    'signup_time': 'd'
                },
                'target_KNN': {
                          "predicted_class": 0,
                          "proba": {
                          "isFraud": 0.3,
                          "notFraud": 0.7
                           }
                },
                'target_LogReg': {
                          "predicted_class": 0,
                          "proba": {
                          "isFraud": 0.3,
                          "notFraud": 0.7
                           }
                }
            },
            "predict_1_in_test_set": {
                'features': {
                    'purchase_value': 0,
                    'device_id': 'a',
                    'ip_address': 'b',
                    'purchase_time': 'c',
                    'signup_time': 'd'
                },
                'target_KNN': {
                          "predicted_class": 0,
                          "proba": {
                          "isFraud": 0.7,
                          "notFraud": 0.3
                           }
                },
                'target_LogReg': {
                          "predicted_class": 0,
                          "proba": {
                          "isFraud": 0.7,
                          "notFraud": 0.3
                           }
                }
            },
            "random_test": {
                'features': {
                    'purchase_value': 0,
                    'device_id': 'a',
                    'ip_address': 'b',
                    'purchase_time': 'c',
                    'signup_time': 'd',
                    'target':np.nan
                },
                'target': np.nan
            },
            "wrong_type_test": {
                'features': {
                    'purchase_value': 0,
                    'device_id': 'a',
                    'ip_address': 'b',
                    'purchase_time': 'c',
                    'signup_time': 'd',
                    'target':np.nan
                },
                'target': np.nan
            },
            "missing_value_test": {
                'features': {
                    'purchase_value': 0,
                    'device_id': 'a',
                    'ip_address': 'b',
                    'purchase_time': 'c',
                    'signup_time': 'd',
                    'target':np.nan
                },
                'target': np.nan
            }
}


####################################
#######
####     3. REQUETES DE L'API POUR LES TESTS
##          Requêtes sur l'API avec les valeurs des jeux de test.
#

# Dictionnaire des requêtes de test.
reqs={}


##############
#####
##       3.1 Requetes non connectées
#


######
###      3.1.1 Endpoint '/'   
# 

r = requests.get(
    url='http://{address}:{port}/'.format(address=api_address, port=api_port),
)
reqs['/'] = r


######
###      3.1.2 Endpoint '/token' avec ('alice', 'wonderland')
# 

headers = {
    'accept': 'application/json',
}

data = {
    'grant_type': '',
    'username': 'alice',
    'password': 'wonderland',
    'scope': '',
    'client_id': '',
    'client_secret': '',
}

r = requests.post(url='http://{address}:{port}/token'.format(address=api_address, port=api_port), \
                       headers=headers, data=data
)
reqs["/token (alice:wonderland)"] = r


######
###      3.1.3 Endpoint '/token' avec ('clementine', 'mandarine')
# 

headers = {
    'accept': 'application/json',
}

data = {
    'grant_type': '',
    'username': 'clementine',
    'password': 'mandarine',
    'scope': '',
    'client_id': '',
    'client_secret': '',
}
r = requests.post(url='http://{address}:{port}/token'.format(address=api_address, port=api_port), \
                       headers=headers, data=data
)
reqs["/token (clementine:mandarine)"] = r


######
###      3.1.4 Endpoint '/PerfKnn'
# 

headers = {
    'accept': 'application/json',
    'content-type': 'application/x-www-form-urlencoded',
}
r = requests.post(url='http://{address}:{port}/PerfKnn'.format(address=api_address, port=api_port), \
                       headers=headers
)
reqs["/PerfKnn"] = r


######
###      3.1.5 Endpoint '/PerfLogReg'
# 

headers = {
    'accept': 'application/json',
    'content-type': 'application/x-www-form-urlencoded',
}
r = requests.post(url='http://{address}:{port}/PerfLogReg'.format(address=api_address, port=api_port), \
                       headers=headers
)
reqs["/PerfModelKnn"] = r


######
###      3.1.6 Endpoint '/PredictionModelKnn' - Non connecté
# 

headers = {
    'accept': 'application/json',
}

json_data = test_set["predict_O_in_test_set"]['features']

r = requests.post(url='http://{address}:{port}/PredictionModelKnn'.format(address=api_address, port=api_port), \
                       headers=headers, json=json_data)
reqs["/PredictionModelKnn - Non connecté"] = r


######
###      3.1.7 Endpoint '/PredictionModelLogreg' - Non connecté
# 

headers = {
    'accept': 'application/json',
}

json_data = test_set["predict_O_in_test_set"]['features']

r = requests.post(url='http://{address}:{port}/PredictionModelLogreg'.format(address=api_address, port=api_port), \
                       headers=headers, json=json_data)
reqs["/PredictionModelLogreg - Non connecté"] = r


##############
#####
##       3.2 Requetes connectées
#


######
###      3.2.1 Récupération du bearer de alice:wonderland
# 

# Authentification avec le compte alice:wonderland et récupération du token
headers = {
    'accept': 'application/json',
}

data = {
    'grant_type': '',
    'username': 'alice',
    'password': 'wonderland',
    'scope': '',
    'client_id': '',
    'client_secret': '',
}

r = requests.post(url='http://{address}:{port}/token'.format(address=api_address, port=api_port), \
                       headers=headers, data=data
)


######
###      3.2.2 Construction du bearer pour les requêtes de prédiction
#

# Construction du bearer
token = r.json()['access_token']
bearer = 'Bearer '+token


######
###      3.2.3 Construction des requêtes de prédiction
#

# Construction des requêtes de prédiction
headers = {
    'accept': 'application/json',
    'Authorization': bearer,
    # Already added when you pass json= but not when you pass data=
}

# Construction d'une requête web pour un endpoint et un jeu de test
def connected_test_request(endpoint, test_vec) :
    """ Cette fonction produit une requête web pour un endpoint et un jeu de test
    """
    json_data = test_set[test_vec]['features']
    r = requests.post(url='http://{address}:{port}/{endpoint}' \
                           .format(address=api_address, port=api_port, endpoint=endpoint), \
                           headers=headers, \
                           json=json_data)
    return r

# Liste des jeux de test et des endpoints
test_vec_list = [i for i in test_set.keys()]
endpoint_list = ['PredictionModelKnn' ,'PredictionModelLogreg']

# Archivage des requêtes pour l'ensemble des combinaisons
for endpoint in endpoint_list :
    for test_vec in test_vec_list :
        reqs["/{endpoint} - Connecté - {test_vec}".format(endpoint=endpoint, test_vec=test_vec)] \
             = connected_test_request(endpoint, test_vec)


####################################
#######
####     4. FORMAT DE SORTIE DES LOGS
##          Format du message exporté dans le fichier de test
#

output = "{ts} : TestCode={test_code} : Response={response} : Test={test_status}\n"


####################################
#######
####     5. DESCRIPTION ET NOMENCLATURE DES TESTS
##          Description des tests et attribution d'un code de test.
#

'''
============================
    OP tests (Operations tests)
============================

requests done at "/"

Test OP_1 : OP_IS_SERVICE_UP
| endpoint = '/'
| expected result = 200
| actual result = {status_code}
| ==>  {test_status}

Test OP_2 : OP_IS_SERVICE_UP_MSG_OK
| endpoint = '/'
| expected result = 'Bienvenue au détecteur de transactions frauduleuses !'
| actual result = {message}
| ==>  {test_message}

============================
    AA tests (Authentication & Authorization tests)
============================

Test AA_1 : AA_DOES_ALICE_CONNECTION_WORK
| endpoint = '/token'
| username = 'alice'
| password = 'wonderland'
| expected result = 200
| actual result = {status_code}
| ==>  {test_status}

Test AA_2 : AA_IS_ALICE_CONNECTION_MSG_OK
| endpoint = '/token'
| username = 'alice'
| password = 'wonderland'
| expected result = "Bienvenue alice !"
| actual result = {message}
| ==>  {test_message}

Test AA_3 : AA_DOES_CLEMENTINE_CONNECTION_FAIL
| endpoint = '/token'
| username = 'clementine'
| password = 'mandarine'
| expected result = 403 (ou 401 ?)
| actual result = {status_code}
| ==>  {test_status}

Test AA_4 : AA_IS_CLEMENTINE_CONNECTION_MSG_OK
| endpoint = '/token'
| username = 'alice'
| password = 'wonderland'
| expected result = "XXXXXXX"
| actual result = {message}
| ==>  {test_message}

Test AA_5 : AA_DOES_PERFKNN_WORK
| endpoint = '/PerfKnn'
| 0 =< expected result =< 1
| actual result = {recall} & actual result = {accuracy}
| ==>  {test_recall} & {test_accuracy}

Test AA_6 : AA_DOES_PERFLOGREG_WORK
| endpoint = '/PerfLogReg'
| 0 =< expected result =< 1
| actual result = {recall} & actual result = {accuracy}
| ==>  {test_recall} & {test_accuracy}

Test AA_7 : AA_DOES_CLEMENTINE_KNNPREDICTION_FAIL
| endpoint = '/PredictionModelKnn'
| expected result = 401
| actual result = {status_code}
| ==>  {test_status}

Test AA_8 : AA_IS_CLEMENTINE_KNNPREDICTION_FAIL_MSG_OK
| endpoint = '/PredictionModelKnn'
| expected result = "Not authenticated"
| actual result = {detail}
| ==>  {test_detail}

Test AA_9 : AA_DOES_CLEMENTINE_LOGREGPREDICTION_FAIL
| endpoint = '/PredictionModelLogreg'
| expected result = 401
| actual result = {status_code}
| ==>  {test_status}

Test AA_10 : AA_IS_CLEMENTINE_LOGREGPREDICTION_FAIL_MSG_OK
| endpoint = '/PredictionModelLogreg'
| expected result = "Not authenticated"
| actual result = {detail}
| ==>  {test_detail}

============================
    CT tests (Contents)
============================

Test CT_1 : CT_DOES_KNN_PREDICT0_WORK
| endpoint = '/PredictionModelKnn'
| testvec = 'predict_O_in_test_set'
| expected result = 200
| actual result = {status_code}
| ==>  {test_status}

Test CT_2 : CT_IS_KNN_PREDICT0_CORRECT
| endpoint = '/PredictionModelKnn'
| testvec = 'predict_O_in_test_set'
| expected result = 0
| actual result = {response_body}
| ==>  {test_response_body}

Test CT_3 : CT_DOES_KNN_PREDICT1_WORK
| endpoint = '/PredictionModelKnn'
| testvec = 'predict_O_in_test_set'
| expected result = 200
| actual result = {status_code}
| ==>  {test_status}

Test CT_4 : CT_IS_KNN_PREDICT1_CORRECT
| endpoint = '/PredictionModelKnn'
| testvec = 'predict_1_in_test_set'
| expected result = predict_1_in_test_set
| actual result = {response_body}
| ==>  {test_response_body}

Test CT_5 : CT_DOES_KNN_PREDICTRANDOM_WORK
| endpoint = '/PredictionModelKnn'
| testvec = 'random_test'
| expected result = 200
| actual result = {status_code}
| ==>  {test_status}

Test CT_6 : CT_IS_KNN_PREDICTRANDOM_CORRECT
| endpoint = '/PredictionModelKnn'
| testvec = 'random_test'
| expected result = ((predicted_class==0 | predicted_class==1) 
|                    & (0 =< isFraud =< 1)
|                    & (0 =< notFraud =< 1)
|                    & (isFraud+notFraud==1)
|                    & (predicted_class==0 & notFraud >= 0.5)
|                    & (predicted_class==1 | isFraud >= 0.5)
|                   )
| actual result = {response_body}
| ==>  {test_response_body}

Test CT_7 : CT_DOES_KNN_PREDICTWRONGTYPE_FAIL
| endpoint = '/PredictionModelKnn'
| testvec = 'wrong_type_test'
| expected result = 422
| actual result = {status_code}
| ==>  {test_status}

Test CT_8 : CT_IS_KNN_PREDICTWRONGTYPE_MSG_OK
| endpoint = '/PredictionModelKnn'
| testvec = 'wrong_type_test'
| expected result = "Bad parameters"
| actual result = {???}
| ==>  {???}

Test CT_9 : CT_DOES_KNN_PREDICTWITHMISSINGPARAM_FAIL
| endpoint = '/PredictionModelKnn'
| testvec = 'missing_value_test'
| expected result = 422
| actual result = {status_code}
| ==>  {test_status}

Test CT_10 : CT_IS_KNN_PREDICTWITHMISSINGPARAM_MSG_OK
| endpoint = '/PredictionModelKnn'
| testvec = 'missing_value_test'
| expected result = "Bad parameters"
| actual result = {???}
| ==>  {???}

Test CT_11 : CT_DOES_LOGREG_PREDICT0_WORK
| endpoint = '/PredictionModelLogreg'
| testvec = 'predict_O_in_test_set'
| expected result = 200
| actual result = {status_code}
| ==>  {test_status}

Test CT_12 : CT_IS_LOGREG_PREDICT0_CORRECT
| endpoint = '/PredictionModelLogreg'
| testvec = 'predict_O_in_test_set'
| expected result = 0
| actual result = {response_body}
| ==>  {test_response_body}

Test CT_13 : CT_DOES_LOGREG_PREDICT1_WORK
| endpoint = '/PredictionModelLogreg'
| testvec = 'predict_O_in_test_set'
| expected result = 200
| actual result = {status_code}
| ==>  {test_status}

Test CT_14 : CT_IS_LOGREG_PREDICT1_CORRECT
| endpoint = '/PredictionModelLogreg'
| testvec = 'predict_1_in_test_set'
| expected result = predict_1_in_test_set
| actual result = {response_body}
| ==>  {test_response_body}

Test CT_15 : CT_DOES_LOGREG_PREDICTRANDOM_WORK
| endpoint = '/PredictionModelLogreg'
| testvec = 'random_test'
| expected result = 200
| actual result = {status_code}
| ==>  {test_status}

Test CT_16 : CT_IS_LOGREG_PREDICTRANDOM_CORRECT
| endpoint = '/PredictionModelLogreg'
| testvec = 'random_test'
| expected result = ((predicted_class==0 | predicted_class==1) 
|                    & (0 =< isFraud =< 1)
|                    & (0 =< notFraud =< 1)
|                    & (isFraud+notFraud==1)
|                    & (predicted_class==0 & notFraud >= 0.5)
|                    & (predicted_class==1 | isFraud >= 0.5)
|                   )
| actual result = {response_body}
| ==>  {test_response_body}

Test CT_17 : CT_DOES_LOGREG_PREDICTWRONGTYPE_FAIL
| endpoint = '/PredictionModelLogreg'
| testvec = 'wrong_type_test'
| expected result = 422
| actual result = {status_code}
| ==>  {test_status}

Test CT_18 : CT_IS_LOGREG_PREDICTWRONGTYPE_MSG_OK
| endpoint = '/PredictionModelLogreg'
| testvec = 'wrong_type_test'
| expected result = "Bad parameters"
| actual result = {???}
| ==>  {???}

Test CT_19 : CT_DOES_LOGREG_PREDICTWITHMISSINGPARAM_FAIL
| endpoint = '/PredictionModelLogreg'
| testvec = 'missing_value_test'
| expected result = 422
| actual result = {status_code}
| ==>  {test_status}

Test CT_20 : CT_IS_LOGREG_PREDICTWITHMISSINGPARAM_MSG_OK
| endpoint = '/PredictionModelLogreg'
| testvec = 'missing_value_test'
| expected result = "Bad parameters"
| actual result = {???}
| ==>  {???}
'''


####################################
#######
####     6. REALISATION DES TESTS
##          A partir des requêtes passées précédemment.
#


##############
#####
##       6.1 Traitement des tests
#

# Afficher un log à l'écran et l'enregistrer dans le fichier de log
def echo_log(log_line) :
    """ Affichage de la log à l'écran et dans le fichier de log
    """
    # Affichage à la log à l'écran
    print(log_line)

    # Ajout de la log dans le fichier de log
    if os.environ.get('LOG') == '1':
        with open(log_file, 'a') as file :
            file.write(log_line)

# Traitement des tests de status
def test_status(test_code, response, expected_value) :
    """ Traitement des tests de status
    """
    # Statut de la requête
    status_code = response.status_code
    test = (status_code==expected_value)

    # Calcul du test
    test_status = 'SUCCESS' if test else 'FAILURE'


    return output.format(test_code=test_code, \
                         response=status_code, \
                         test_status=test_status, \
                         ts=ts)

# Traitement des tests de contenus
def test_value(test_code, response, expected_value) :
    """ Test de valeur dans le Response body
    """
    test_status = 'SUCCESS' if (response==expected_value) else 'FAILURE'
    return output.format(test_code=test_code, \
                         response=response, \
                         test_status=test_status, \
                         ts=ts)

# Traitement des tests de cohérence
def test_value_consistency(test_code, response, expected_value) :
    """ Test de la cohérence des valeurs des valeurs de sortie (cohérence != exactitude)
    """
    # Extraction des valeurs
    predicted_class = response['predicted_class']
    proba_isFraud = response['proba']['isFraud']
    proba_notFraud = response['proba']['notFraud']

    # Calcul du test
    test = ((predicted_class==0)|(predicted_class==1))
    test = test & ((proba_isFraud>=0)&(proba_isFraud<=1))
    test = test & ((proba_notFraud>=0)&(proba_notFraud<=1))
    test_status = 'SUCCESS' if test else 'FAILURE'

    return output.format(test_code=test_code, \
                         response=response, \
                         test_status=test_status, \
                         ts=ts)    

# Affichage pour les tests non développés
def TBD(test_code, response, expected_value) :
    return output.format(test_code=test_code, \
                         response='XXX', \
                         test_status='TBD', \
                         ts=ts)


##############
#####
##       6.2 Paramétrage des tests
#

test_code_map = {
    "OP_IS_SERVICE_UP":{
        'test_func':test_status,
        'response':reqs['/'],
        'expected_result':200
    },
    "OP_IS_SERVICE_UP_MSG_OK":{
        'test_func':test_value, 
        'response':reqs['/'].json()['Message'],
        'expected_result':"Bienvenue au détecteur de transactions frauduleuses !"
    },
    "AA_DOES_ALICE_CONNECTION_WORK":{
        'test_func':test_status, 
        'response':reqs["/token (alice:wonderland)"], 
        'expected_result':200
    },
    "AA_IS_ALICE_CONNECTION_MSG_OK":{
        'test_func':test_value,
        'response':reqs["/token (alice:wonderland)"].json()['message'],
        'expected_result':"Bienvenue alice !"
    },
    "AA_DOES_CLEMENTINE_CONNECTION_FAIL":{
        'test_func':test_status, 
        'response':reqs["/token (clementine:mandarine)"], 
        'expected_result':401
    },
#    "AA_IS_CLEMENTINE_CONNECTION_MSG_OK":{
#        'test_func':test_value, 
#        'response':reqs["/token (clementine:mandarine)"].json()['detail'], 
#        'expected_result':'Incorrect username or password'
#    },
    "AA_DOES_PERFKNN_WORK":{
        'test_func':test_status,
        'response':reqs["/PerfKnn"],
        'expected_result':200
    },
    "AA_DOES_PERFLOGREG_WORK":{
        'test_func':test_status,
        'response':reqs["/PerfModelKnn"],
        'expected_result':200
    },
    "AA_DOES_CLEMENTINE_KNNPREDICTION_FAIL":{
        'test_func':test_status,
        'response':reqs["/PredictionModelKnn - Non connecté"],
        'expected_result':401
    },
    "AA_IS_CLEMENTINE_KNNPREDICTION_FAIL_MSG_OK":
        {'test_func':test_value,
        'response':reqs["/PredictionModelKnn - Non connecté"].json()['detail'],
        'expected_result':"Not authenticated"
    },
    "AA_DOES_CLEMENTINE_LOGREGPREDICTION_FAIL":{
        'test_func':test_status,
        'response':reqs["/PredictionModelLogreg - Non connecté"],
        'expected_result':401
    },
    "AA_IS_CLEMENTINE_LOGREGPREDICTION_FAIL_MSG_OK":{
        'test_func':test_value,
        'response':reqs["/PredictionModelLogreg - Non connecté"].json()['detail'],
        'expected_result':"Not authenticated"
    },
    "CT_DOES_KNN_PREDICT0_WORK":{
        'test_func':test_status,
        'response':reqs['/PredictionModelKnn - Connecté - predict_O_in_test_set'],
        'expected_result':200
    },
    "CT_IS_KNN_PREDICT0_CORRECT":{
        'test_func':test_value,
        'response':reqs['/PredictionModelKnn - Connecté - predict_O_in_test_set'].json(),
        'expected_result':test_set["predict_O_in_test_set"]['target_KNN']
    },
    "CT_DOES_KNN_PREDICT1_WORK":{
        'test_func':test_status,
        'response':reqs['/PredictionModelKnn - Connecté - predict_1_in_test_set'],
        'expected_result':200
    },
    "CT_IS_KNN_PREDICT1_CORRECT":{
        'test_func':test_value,
        'response':reqs['/PredictionModelKnn - Connecté - predict_1_in_test_set'].json(),
        'expected_result':test_set["predict_1_in_test_set"]['target_KNN']
    },
    "CT_DOES_KNN_PREDICTRANDOM_WORK":{
        'test_func':test_status,
        'response':reqs['/PredictionModelKnn - Connecté - random_test'],
        'expected_result':200
    },
    "CT_IS_KNN_PREDICTRANDOM_CORRECT":{
        'test_func':test_value_consistency,
        'response':reqs['/PredictionModelKnn - Connecté - random_test'].json(),
        'expected_result':np.nan
    },
    "CT_DOES_KNN_PREDICTWRONGTYPE_FAIL":{
        'test_func':test_status,
        'response':reqs['/PredictionModelKnn - Connecté - wrong_type_test'],
        'expected_result':422
    },
    "CT_IS_KNN_PREDICTWRONGTYPE_MSG_OK":{
        'test_func':TBD,
        'response':reqs['/PredictionModelKnn - Connecté - wrong_type_test'].json(),
        'expected_result':np.nan
    },
    "CT_DOES_KNN_PREDICTWITHMISSINGPARAM_FAIL":{
        'test_func':test_status,
        'response':reqs['/PredictionModelKnn - Connecté - missing_value_test'],
        'expected_result':422
    },
    "CT_IS_KNN_PREDICTWITHMISSINGPARAM_MSG_OK":{
        'test_func':TBD,
        'response':reqs['/PredictionModelKnn - Connecté - missing_value_test'].json(),
        'expected_result':np.nan
    },
    "CT_DOES_LOGREG_PREDICT0_WORK":{
        'test_func':test_status,
        'response':reqs['/PredictionModelLogreg - Connecté - predict_O_in_test_set'],
        'expected_result':200
    },
    "CT_IS_LOGREG_PREDICT0_CORRECT":{
        'test_func':test_value,
        'response':reqs['/PredictionModelLogreg - Connecté - predict_O_in_test_set'].json(),
        'expected_result':test_set["predict_O_in_test_set"]['target_LogReg']
    },
    "CT_DOES_LOGREG_PREDICT1_WORK":{
        'test_func':test_status,
        'response':reqs['/PredictionModelLogreg - Connecté - predict_1_in_test_set'],
        'expected_result':200
    },
    "CT_IS_LOGREG_PREDICT1_CORRECT":{
        'test_func':test_value,
        'response':reqs['/PredictionModelLogreg - Connecté - predict_1_in_test_set'].json(),
        'expected_result':test_set["predict_1_in_test_set"]['target_LogReg']
    },
    "CT_DOES_LOGREG_PREDICTRANDOM_WORK":{
        'test_func':test_status,
        'response':reqs['/PredictionModelLogreg - Connecté - random_test'],
        'expected_result':200
    },
    "CT_IS_LOGREG_PREDICTRANDOM_CORRECT":{
        'test_func':test_value_consistency,
        'response':reqs['/PredictionModelLogreg - Connecté - random_test'].json(),
        'expected_result':np.nan
    },
    "CT_DOES_LOGREG_PREDICTWRONGTYPE_FAIL":{
        'test_func':test_status,
        'response':reqs['/PredictionModelLogreg - Connecté - wrong_type_test'],
        'expected_result':422
    },
    "CT_IS_LOGREG_PREDICTWRONGTYPE_MSG_OK":{
        'test_func':TBD,
        'response':reqs['/PredictionModelLogreg - Connecté - wrong_type_test'].json(),
        'expected_result':np.nan
    },
    "CT_DOES_LOGREG_PREDICTWITHMISSINGPARAM_FAIL":{
        'test_func':test_status,
        'response':reqs['/PredictionModelLogreg - Connecté - missing_value_test'],
        'expected_result':422
    },
    "CT_IS_LOGREG_PREDICTWITHMISSINGPARAM_MSG_OK":{
        'test_func':TBD,
        'response':reqs['/PredictionModelLogreg - Connecté - missing_value_test'].json(),
        'expected_result':np.nan
    }
}


##############
#####
##       6.3 Exécution des tests
#

for key, value in test_code_map.items() :
    test_code = key
    test_func = value['test_func']
    response = value['response']
    expected_result = value['expected_result']

    echo_log(test_func(test_code, response, expected_result))


#  https://docs.python-requests.org/en/latest/user/quickstart/#more-complicated-post-requests