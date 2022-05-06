import os
import requests
import time
import numpy as np
import datetime as dt

import json


def format_integration_test(test_set={},
                            path_and_name_of_knn_integration_test="./data_integration/output_knn.json",
                            path_and_name_of_logreg_integration_test="./data_integration/output_logreg.json",
                            max_number_of_tests=10
    ):
    """ Picks up values for integration test from two files, format the data and add it to the provided
        test_set dictionary. If no dictionary provided, a new one is created.
    """

    remaining_tests = max_number_of_tests

    # Collecter les données des tests d'intégration
    with open(path_and_name_of_knn_integration_test) as mon_fichier:
        integration_knn = json.load(mon_fichier)

    with open(path_and_name_of_logreg_integration_test) as mon_fichier:
        integration_logreg = json.load(mon_fichier)

    # Récuper les test_ids
    integration_test_ids_knn = integration_knn['purchase_value'].keys()
    integration_test_ids_logreg = integration_knn['purchase_value'].keys()
    integration_test_ids = [value for value in integration_test_ids_knn if value in integration_test_ids_logreg]

    # Ajouter les tests d'intégration à test_set
    for id in integration_test_ids :
        features = dict(
            purchase_value = integration_knn['purchase_value'][id],
            purchase_time = integration_knn['purchase_time'][id],
            signup_time = integration_knn['signup_time'][id] 
        )
        target_KNN = dict(
            predicted_class = integration_knn['is_fraud'][id],
    #        predicted_class = integration_knn['predicted_class'][id],
    #        proba = dict(
    #            isFraud = integration_knn['is_fraud'][id],
    #            notFraud = integration_knn['notFraud'][id]
    #        )
        )
        target_LogReg = dict(
            predicted_class = integration_logreg['is_fraud'][id],
    #        predicted_class = integration_logreg['predicted_class'][id],
    #        proba = dict(
    #            isFraud = integration_logreg['is_fraud'][id],
    #            notFraud = integration_logreg['notFraud'][id]
    #        )
        )
        test_set['integration_test_'+id] = dict(
            features=features,
            target_KNN=target_KNN,
            target_LogReg=target_LogReg
        )

        # comptage des tests et exit la boucle
        remaining_tests-=1
        if not remaining_tests : break
    return test_set



""" FORMAT TEST_SET

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


"""


""" FORMAT FICHIER D'INTEGRATION
{
  "purchase_value": {
    "0": 33,
    "1": 49,
    "2": 51,
    "3": 21,
    "4": 72,
    "5": 37,
    "6": 71,
    "7": 77,
    "8": 44,
    "9": 78
  },
  "tot_time": {
    "0": -0.0008851585,
    "1": -0.0003766472,
    "2": -0.0004220359,
    "3": -0.0003545583,
    "4": -0.0004138338,
    "5": -3600,
    "6": -0.0003932242,
    "7": -0.00049721,
    "8": -0.0025107019,
    "9": -0.0012341861
  },
  "is_fraud": {
    "0": 0,
    "1": 1,
    "2": 0,
    "3": 0,
    "4": 1,
    "5": 1,
    "6": 0,
    "7": 0,
    "8": 1,
    "9": 0
  },
  "prediction.csv": {
    "0": 1,
    "1": 0,
    "2": 0,
    "3": 0,
    "4": 0,
    "5": 1,
    "6": 1,
    "7": 0,
    "8": 0,
    "9": 0
  },
  "signup_time": {
    "0": "2015-03-09 10:57:17",
    "1": "2015-05-28 12:40:49",
    "2": "2015-02-20 15:17:57",
    "3": "2015-05-22 16:11:37",
    "4": "2015-06-04 19:09:48",
    "5": "2015-01-04 19:56:46",
    "6": "2015-02-10 23:50:59",
    "7": "2015-07-27 19:57:38",
    "8": "2015-04-17 7:26:15",
    "9": "2015-04-04 11:40:23"
  },
  "purchase_time": {
    "0": "2015-04-25 12:41:45",
    "1": "2015-09-16 3:41:06",
    "2": "2015-05-30 8:45:57",
    "3": "2015-09-17 4:36:16",
    "4": "2015-09-13 11:35:32",
    "5": "2015-01-04 19:56:47",
    "6": "2015-05-27 22:55:41",
    "7": "2015-10-19 15:10:59",
    "8": "2015-05-03 21:43:57",
    "9": "2015-05-08 5:55:25"
  }
}
"""