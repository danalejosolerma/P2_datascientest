#!/bin/bash

# Timestamp dans log.txt
echo -n ">>> setup.sh - "
date

# Construire les images pour le pipeline test
echo "1... CONSTRUCTION DES IMAGES DOCKER ..."
cd ~/Docker/exam_docker/docker_image/authent_test
docker image build . -t python_authent_test:latest

cd ~/Docker/exam_docker/docker_image/author_test
docker image build . -t python_author_test:latest

cd ~/Docker/exam_docker/docker_image/content_test
docker image build . -t python_content_test:latest

# Lancer un test
cd ~/Docker/exam_docker
echo "2... LANCEMENT DES CONTENEURS DE TEST ..."
docker-compose up >> log.txt

# Arrêter le pipeline
#echo "3... ARRET DES CONTENEURS DE TEST ..."
#docker-compose down >> log.txt
