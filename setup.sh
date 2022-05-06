#!/bin/bash/
# Removing older images
docker container stop api_fraud tests_api
docker container rm api_fraud tests_api
docker image rm image_fraud image_tests

# copying The models into fraud_docker
cd ML_models/
cp features.json knn_classifier.joblib logreg_classifier.joblib ../fraud_docker/
cd ..
# Building new images and copying the data_test.json file
docker image build fraud_docker/. -t image_fraud:latest
docker image build fraud_test_docker/. -t image_tests:latest

# Composing file
docker-compose up

# Creating the containers inside kubernetes
kubectl apply -f deployment-fraud.yaml
kubectl apply -f service-fraud.yaml
