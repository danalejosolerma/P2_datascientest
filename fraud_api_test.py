#!/bin/python3

####################################
#|  Test de l'API fraud : v1.0.2
####################################


import os
import requests
import time
import numpy as np
import datetime as dt
from integration import format_integration_test


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
time.sleep(10)
ts = dt.datetime.now().strftime("%Y/%m/%d-%H:%M:%S")

# Fichier jeux de test pour les tests d'intégration
knn_file = "./data_integration/output_knn.json"
logreg_file = "./data_integration/output_logreg.json"


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
                    'purchase_time': "2018-06-12T09:05:38",
                    'signup_time': "2018-06-12T09:05:26"
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
                    'purchase_time': "2018-06-12T09:05:38",
                    'signup_time': "2018-06-12T09:05:26"
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
                    'purchase_time': "2019-01-12T09:05:38",
                    'signup_time': "2019-01-12T09:05:33"
                },
                'target': np.nan
            },
            "wrong_type_test": {
                'features': {
                    'purchase_value': 'bad',
                    'purchase_time': "2018-06-12T09:05:38",
                    'signup_time': "2018-06-12T09:05:26"
                },
                'target': np.nan
            },
            "missing_value_test": {
                'features': {
                    'purchase_time': "2018-06-12T09:05:38",
                    'signup_time': "2018-06-12T09:05:26"
                },
                'target': np.nan
            }
}

test_set = format_integration_test(
                test_set=test_set,
                path_and_name_of_knn_integration_test=knn_file,
                path_and_name_of_logreg_integration_test=logreg_file,
                max_number_of_tests=10)


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
###      3.1.2 Endpoint '/signin' avec ('alice', 'wonderland')
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

r = requests.post(url='http://{address}:{port}/signin'.format(address=api_address, port=api_port), \
                       headers=headers, data=data
)
reqs["/signin (alice:wonderland)"] = r


######
###      3.1.3 Endpoint '/signin' avec ('clement', 'mandarine')
# 

headers = {
    'accept': 'application/json',
}

data = {
    'grant_type': '',
    'username': 'clement',
    'password': 'mandarine',
    'scope': '',
    'client_id': '',
    'client_secret': '',
}
r = requests.post(url='http://{address}:{port}/signin'.format(address=api_address, port=api_port), \
                       headers=headers, data=data
)
reqs["/signin (clement:mandarine)"] = r


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

r = requests.post(url='http://{address}:{port}/signin'.format(address=api_address, port=api_port), \
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
    Objective : Test that the API is online
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
    Objective : Test authentication and authorization functionalities
============================

Test AA_DOES_ALICE_CONNECTION_WORK
| endpoint = '/signin'
| username = 'alice'
| password = 'wonderland'
| expected result = 200
| actual result = {status_code}
| ==>  {test_status}

Test AA_IS_ALICE_CONNECTION_MSG_OK
| endpoint = '/signin'
| username = 'alice'
| password = 'wonderland'
| expected result = "Bienvenue alice !"
| actual result = {message}
| ==>  {test_message}

Test AA_DOES_CLEMENT_CONNECTION_FAIL
| endpoint = '/signin'
| username = 'clement'
| password = 'mandarine'
| expected result = 401
| actual result = {status_code}
| ==>  {test_status}

Test AA_IS_CLEMENT_CONNECTION_MSG_OK (not implemented)
| endpoint = '/signin'
| username = 'clement'
| password = 'mandarine'
| expected result = "Incorrect username or password"
| actual result = {message}
| ==>  {test_message}

Test AA_DOES_PERFKNN_WORK
| endpoint = '/PerfKnn'
| expected result = 200
| actual result = {status_code}
| ==>  {test_status}

Test AA_DOES_PERFLOGREG_WORK
| endpoint = '/PerfLogReg'
| expected result = 200
| actual result = {status_code}
| ==>  {test_status}

Test AA_DOES_CLEMENT_KNNPREDICTION_FAIL
| endpoint = '/PredictionModelKnn'
| expected result = 401
| actual result = {status_code}
| ==>  {test_status}

Test AA_IS_CLEMENT_KNNPREDICTION_FAIL_MSG_OK
| endpoint = '/PredictionModelKnn'
| expected result = "Not authenticated"
| actual result = {detail}
| ==>  {test_detail}

Test AA_DOES_CLEMENT_LOGREGPREDICTION_FAIL
| endpoint = '/PredictionModelLogreg'
| expected result = 401
| actual result = {status_code}
| ==>  {test_status}

Test AA_IS_CLEMENT_LOGREGPREDICTION_FAIL_MSG_OK
| endpoint = '/PredictionModelLogreg'
| expected result = "Not authenticated"
| actual result = {detail}
| ==>  {test_detail}

============================
    INT tests (Integration)
    Objective : Check that the model works as it used to be in the training program
    <Index> Identifies a test set
============================

Test INT_DOES_KNN_INTEGRATIONTEST<INDEX>_WORK
| endpoint = '/PredictionModelKnn'
| testvec = 'integration_test_{id}'
| expected result = 200
| actual result = {status_code}
| ==>  {test_status}

Test INT_IS_KNN_INTEGRATIONTEST<INDEX>_CORRECT
| endpoint = '/PredictionModelKnn'
| testvec = 'integration_test_{id}'
| expected result = test_set['integration_test_{id}']['target_KNN']
| actual result = {response_body}
| ==>  {test_response_body}

Test INT_DOES_LOGREG_INTEGRATIONTEST<INDEX>_WORK
| endpoint = '/PredictionModeLogreg'
| testvec = 'integration_test_{id}'
| expected result = 200
| actual result = {status_code}
| ==>  {test_status}

Test INT_IS_LOGREG_INTEGRATIONTEST<INDEX>_CORRECT
| endpoint = '/PredictionModelLogreg'
| testvec = 'integration_test_{id}'
| expected result = test_set['integration_test_{id}']['target_LogReg']
| actual result = {response_body}
| ==>  {test_response_body}


============================
    CT tests (Contents)
    Objective : Test that the prediction service works fine in a regular use
============================

Test CT_DOES_KNN_PREDICTRANDOM_WORK
| endpoint = '/PredictionModelKnn'
| testvec = 'random_test'
| expected result = 200
| actual result = {status_code}
| ==>  {test_status}

Test CT_IS_KNN_PREDICTRANDOM_CORRECT
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

Test CT_DOES_KNN_PREDICTWRONGTYPE_FAIL
| endpoint = '/PredictionModelKnn'
| testvec = 'wrong_type_test'
| expected result = 422
| actual result = {status_code}
| ==>  {test_status}

Test CT_IS_KNN_PREDICTWRONGTYPE_MSG_OK (not implemented)
| endpoint = '/PredictionModelKnn'
| testvec = 'wrong_type_test'
| expected result = "Bad parameters"
| actual result = {???}
| ==>  {???}

Test CT_DOES_KNN_PREDICTWITHMISSINGPARAM_FAIL
| endpoint = '/PredictionModelKnn'
| testvec = 'missing_value_test'
| expected result = 422
| actual result = {status_code}
| ==>  {test_status}

Test CT_IS_KNN_PREDICTWITHMISSINGPARAM_MSG_OK (not implemented)
| endpoint = '/PredictionModelKnn'
| testvec = 'missing_value_test'
| expected result = "Bad parameters"
| actual result = {???}
| ==>  {???}

Test CT_DOES_LOGREG_PREDICTRANDOM_WORK
| endpoint = '/PredictionModelLogreg'
| testvec = 'random_test'
| expected result = 200
| actual result = {status_code}
| ==>  {test_status}

Test CT_IS_LOGREG_PREDICTRANDOM_CORRECT
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

Test CT_DOES_LOGREG_PREDICTWRONGTYPE_FAIL
| endpoint = '/PredictionModelLogreg'
| testvec = 'wrong_type_test'
| expected result = 422
| actual result = {status_code}
| ==>  {test_status}

Test CT_IS_LOGREG_PREDICTWRONGTYPE_MSG_OK
| endpoint = '/PredictionModelLogreg'
| testvec = 'wrong_type_test'
| expected result = "Bad parameters"
| actual result = {???}
| ==>  {???}

Test CT_DOES_LOGREG_PREDICTWITHMISSINGPARAM_FAIL
| endpoint = '/PredictionModelLogreg'
| testvec = 'missing_value_test'
| expected result = 422
| actual result = {status_code}
| ==>  {test_status}

Test CT_IS_LOGREG_PREDICTWITHMISSINGPARAM_MSG_OK (not implemented)
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
    return

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
        'response':reqs["/signin (alice:wonderland)"], 
        'expected_result':200
    },
    "AA_IS_ALICE_CONNECTION_MSG_OK":{
        'test_func':test_value,
        'response':reqs["/signin (alice:wonderland)"].json()['message'],
        'expected_result':"Bienvenue alice !"
    },
    "AA_DOES_CLEMENT_CONNECTION_FAIL":{
        'test_func':test_status, 
        'response':reqs["/signin (clement:mandarine)"], 
        'expected_result':401
    },
    "AA_IS_CLEMENT_CONNECTION_MSG_OK":{
        'test_func':test_value, 
        'response':reqs["/signin (clement:mandarine)"].json()['message'], 
        'expected_result':'Incorrect username or password'
    },
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
    "AA_DOES_CLEMENT_KNNPREDICTION_FAIL":{
        'test_func':test_status,
        'response':reqs["/PredictionModelKnn - Non connecté"],
        'expected_result':401
    },
    "AA_IS_CLEMENT_KNNPREDICTION_FAIL_MSG_OK":
        {'test_func':test_value,
        'response':reqs["/PredictionModelKnn - Non connecté"].json()['detail'],
        'expected_result':"Not authenticated"
    },
    "AA_DOES_CLEMENT_LOGREGPREDICTION_FAIL":{
        'test_func':test_status,
        'response':reqs["/PredictionModelLogreg - Non connecté"],
        'expected_result':401
    },
    "AA_IS_CLEMENT_LOGREGPREDICTION_FAIL_MSG_OK":{
        'test_func':test_value,
        'response':reqs["/PredictionModelLogreg - Non connecté"].json()['detail'],
        'expected_result':"Not authenticated"
    },
    "CT_DOES_KNN_PREDICTRANDOM_WORK":{
        'test_func':test_status,
        'response':reqs['/PredictionModelKnn - Connecté - random_test'],
        'expected_result':200
    },
    "CT_IS_KNN_PREDICTRANDOM_CORRECT":{
        'test_func':test_value_consistency,
        'response':reqs['/PredictionModelKnn - Connecté - random_test'].json(),
        'expected_result':np.nan         # unused
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

# Ajout des tests d'intégration à test_code_map
integration_req_list = [value for value in reqs.keys() if 'integration' in value]

for req in integration_req_list :
    if 'Knn' in req : (algo, target_algo) = ('KNN', 'KNN') 
    if 'Logreg' in req : (algo, target_algo) = ('LOGREG', 'LogReg') 
    id = req.split("_")[-1]

    test_code_map['INT_DOES_'+algo+'_INTEGRATIONTEST'+id+'_WORK'] = dict(
                test_func=test_status,
                response=reqs[req],
                expected_result=200
    )

    test_code_map['INT_IS_'+algo+'_INTEGRATIONTEST'+id+'_CORRECT'] = dict(
                test_func=test_value,
                response=reqs[req].json(),
                expected_result=test_set["integration_test_"+id]['target_'+target_algo]
    )


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
