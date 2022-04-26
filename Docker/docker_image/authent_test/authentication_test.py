#!/bin/python3

import os
import requests
import time
import datetime as dt

# définition de l'adresse de l'API
api_address = 'api_sentiment'

# port de l'API
api_port = 8000

# attente du démarrage de l'API + timestamp du test
time.sleep(10)
ts = dt.datetime.now().strftime("%Y/%m/%d-%H:%M:%S")

# requêtes de test
r1 = requests.get(
    url='http://{address}:{port}/permissions'.format(address=api_address, port=api_port),
    params= {
        'username': 'alice',
        'password': 'wonderland'
    }
)

r2 = requests.get(
    url='http://{address}:{port}/permissions'.format(address=api_address, port=api_port),
    params= {
        'username': 'bob',
        'password': 'builder'
    }
)

r3 = requests.get(
    url='http://{address}:{port}/permissions'.format(address=api_address, port=api_port),
    params= {
        'username': 'clementine',
        'password': 'mandarine'
    }
)


# Format de sortie
output = "{ts} : Authentication_Test_#{num} : Status={status_code} : Test={test_status}\n"

'''

============================
    Authentication test
============================

requests done at "/permissions"

Test 1 :
| username="alice"
| password="wonderland"
| expected result = 200
| actual result = {status_code}
| ==>  {test_status}

Test 2 :
| username="bob"
| password="builder"
| expected result = 200
| actual result = {status_code}
| ==>  {test_status}

Test 3 :
| username="clementine"
| password="mandarine"
| expected result = 403
| actual result = {status_code}
| ==>  {test_status}

'''

for i, r in enumerate([r1, r2]) :
    # statut de la requête
    status_code = r.status_code

    # affichage des résultats
    if status_code == 200:
        test_status = 'SUCCESS'
    else :
        test_status = 'FAILURE'
    print(output.format(ts=ts, num=i+1, status_code=status_code, test_status=test_status))

    # impression dans un fichier
    if os.environ.get('LOG') == '1':
        with open('/home/test/api_test.log', 'a') as file :
            file.write(output.format(ts=ts, num=i+1, status_code=status_code, test_status=test_status))

for r in [r3] :
    # statut de la requête
    status_code = r.status_code

    # affichage des résultats
    if status_code == 403:
        test_status = 'SUCCESS'
    else :
        test_status = 'FAILURE'
    print(output.format(ts=ts, num=3, status_code=status_code, test_status=test_status))

    # impression dans un fichier
    if os.environ.get('LOG') == '1':
        with open('/home/test/api_test.log', 'a') as file:
            file.write(output.format(ts=ts, num=3, status_code=status_code, test_status=test_status))
