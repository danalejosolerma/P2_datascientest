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
time.sleep(12)
ts = dt.datetime.now().strftime("%Y/%m/%d-%H:%M:%S")

# requêtes de test
username_list = ['alice', 'bob', 'clementine']
password_list = ['wonderland', 'builder', 'mandarine']

reqs=[]

for usr, pwd in zip(username_list, password_list) :
    r = requests.get(
        url='http://{address}:{port}/v1/sentiment'.format(address=api_address, port=api_port),
        params= {
            'username': usr,
            'password': pwd,
            'sentence': 'test'
        }
    )
    reqs.append(r)

for usr, pwd in zip(username_list, password_list) :
    r = requests.get(
        url='http://{address}:{port}/v2/sentiment'.format(address=api_address, port=api_port),
        params= {
            'username': usr,
            'password': pwd,
            'sentence': 'test'
        }
    )
    reqs.append(r)


# Format de sortie
output = "{ts} : Authorization_Test_#{num} : Status={status_code} : Test={test_status}\n"

'''

============================
    Authorization test
============================

requests done at "/v1/sentiment" and "/v2/sentiment"

Test 1 :
| version = "v1"
| username="alice"
| password="wonderland"
| expected result = 200
| actual result = {status_code}
| ==>  {test_status}

Test 2 :
| version = "v1"
| username="bob"
| password="builder"
| expected result = 200
| actual result = {status_code}
| ==>  {test_status}

Test 3 :
| version = "v1"
| username="clementine"
| password="mandarine"
| expected result = 403
| actual result = {status_code}
| ==>  {test_status}

Test 4 :
| version = "v2"
| username="alice"
| password="wonderland"
| expected result = 200
| actual result = {status_code}
| ==>  {test_status}

Test 5 :
| version = "v2"
| username="bob"
| password="builder"
| expected result = 403
| actual result = {status_code}
| ==>  {test_status}

Test 6 :
| version = "v2"
| username="clementine"
| password="mandarine"
| expected result = 403
| actual result = {status_code}
| ==>  {test_status}

'''
exp_results = [200, 200, 403, 200, 403, 403]

for i, (r, res) in enumerate(zip(reqs, exp_results)) :
    # statut de la requête
    status_code = r.status_code

    # affichage des résultats
    if status_code == res:
        test_status = 'SUCCESS'
    else :
        test_status = 'FAILURE'
    print(output.format(ts=ts, num=i+1, status_code=status_code, test_status=test_status))

    # impression dans un fichier
    if os.environ.get('LOG') == '1':
        with open('/home/test/api_test.log', 'a') as file :
            file.write(output.format(ts=ts, num=i+1, status_code=status_code, test_status=test_status))

