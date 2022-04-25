
import requests




API_URL = "http://127.0.0.1:8000"


def test_get_index():
    response = requests.get(
        url=f"{API_URL}/"
    )

    assert response.status_code == 200, response.content
    


def test_generation_donnees():
    """
    Validation de la génération de test lorsque les paramètres existent
    """

    r_valide = requests.post( url=f"{API_URL}/test", json = {'use': 'Test de positionnement', 'subject': "BDD", 'number': 5 } )


    # statut de la requête
    status_code_valide = r_valide.status_code
  
    # affichage des résultats

    assert status_code_valide  == 200, r_valide.content





def test_generation_donnees_non_valides():
    """
    Validation de la génération de test lorsque les paramètres n''existent pas
    """

    r_non_valide = requests.post( url=f"{API_URL}/test", json = {'use': 'Test de validation', 'subject': "BDD", 'number': 5 }    )


    # statut de la requête
    status_code_non_valide = r_non_valide.status_code
  
    # affichage des résultats
    assert status_code_non_valide  == 200, r_non_valide.content





