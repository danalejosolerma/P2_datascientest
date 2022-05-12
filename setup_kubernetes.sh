#!/bin/bash
kubectl create -f deployment-fraud.yaml
kubectl create -f service-fraud.yaml
kubectl create -f ingress-fraud.yaml