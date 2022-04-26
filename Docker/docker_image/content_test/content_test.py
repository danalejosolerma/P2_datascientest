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
time.sleep(14)
ts = dt.datetime.now().strftime("%Y/%m/%d-%H:%M:%S")

# requêtes de test
sentence_list = ['life is beautiful', 'that sucks']

reqs=[]

for sent in sentence_list :
    r = requests.get(
        url='http://{address}:{port}/v1/sentiment'.format(address=api_address, port=api_port),
        params= {
            'username': 'alice',
            'password': 'wonderland',
            'sentence': sent
        }
    )
    reqs.append(r)

for sent in sentence_list :
    r = requests.get(
        url='http://{address}:{port}/v2/sentiment'.format(address=api_address, port=api_port),
        params= {
            'username': 'alice',
            'password': 'wonderland',
            'sentence': sent
        }
    )
    reqs.append(r)


# Format de sortie
output = "{ts} : Content_Test_#{num} : Status={status_code} : Score={score} : Test={test_status}\n"

'''

============================
    Authorization test
============================

requests done at "/v1/sentiment" and "/v2/sentiment"

Test 1 :
| version = "v1"
| username="alice"
| password="wonderland"
| sentence = "life is beautiful"
| expected score > 0
| actual result = {score}
| ==>  {test_status}

Test 2 :
| version = "v1"
| username="alice"
| password="wonderland"
| sentence = "that sucks"
| expected score < 0
| actual result = {score}
| ==>  {test_status}

Test 3 :
| version = "v2"
| username="alice"
| password="wonderland"
| sentence = "life is beautiful"
| expected score > 0
| actual result = {score}
| ==>  {test_status}

Test 4 :
| version = "v2"
| username="alice"
| password="wonderland"
| sentence = "that sucks"
| expected score < 0
| actual result = {score}
| ==>  {test_status}
'''

greater_than_zero  = [True, False, True, False]

for i, (r, test) in enumerate(zip(reqs, greater_than_zero)) :
    # statut et score de la requête
    status_code = r.status_code
    score = r.json()["score"]

    # affichage des résultats
    if score==0 :
        test_status = 'FAILURE'
    elif (score>0)==test :
        test_status = 'SUCCESS'
    else :
        test_status = 'FAILURE'
    print(output.format(ts=ts, num=i+1, status_code=status_code, score=score, test_status=test_status))

    # impression dans un fichier
    if os.environ.get('LOG') == '1':
        with open('/home/test/api_test.log', 'a') as file :
            file.write(output.format(ts=ts, num=i+1, status_code=status_code, score=score, test_status=test_status))
