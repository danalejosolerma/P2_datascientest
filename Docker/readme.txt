README.TXT - Pipeline de test de l'API Analyse de sentiment
v1.0.0 (Avril 2022)
------------------------------------

1. Prérequis :
   - Docker installé sur la machine hôte.

2. Installation : 
   - Pour créer les images et lancer le pipeline de test, il faut exécuter le script setup.sh.
   - L'installation démarrera automatiquement le serveur d'API à tester ainsi que les 3 serveurs
  de test.

3. Séquencement des tests :
   - Tous les serveurs démarrent en même temps. Une temporisation dans les fichiers python 
     permet de garantir que les requêtes arrivent quand le serveur est disponible.

4. Fichiers  du livrable :
   - 3 fichiers Python + 3 fichiers Dockerfile (répertoire docker_image).
   - 1 fichier `docker-compose.yml` qui contient l'enchaînement des tests à effectuer.
   - 1 fichier `setup.sh` contenant les commandes utilisées pour construire les images 
     et lancer le docker-compose.
   - 1 fichier `log.txt` : résultat des logs pour un lancement de tests.
   - 1 fichier 'api_test.log' : echantillon des résultats de test. Ce fichier est dans le
     répertoire de lancement du pipeline et est alimenté en delta.
