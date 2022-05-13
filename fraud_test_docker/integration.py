import os
import requests
import time
import numpy as np
import datetime as dt

import json


def format_integration_test(test_set={},
                            path_and_name_of_knn_integration_test="./output_knn.json",
                            path_and_name_of_logreg_integration_test="./output_logreg.json",
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
            predicted_class = integration_knn['predicted_class'][id],
            proba = dict(
                isFraud = integration_knn['is_fraud'][id],
                notFraud = integration_knn['not_fraud'][id]
            )
        )
        target_LogReg = dict(
            predicted_class = integration_logreg['predicted_class'][id],
            proba = dict(
                isFraud = integration_logreg['is_fraud'][id],
                notFraud = integration_logreg['not_fraud'][id]
            )
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
