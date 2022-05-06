FROM ubuntu:latest

ADD requirements.txt /requirements.txt

RUN apt-get update && apt-get install python3-pip -y && pip install -r requirements.txt

COPY main.py features.json knn_classifier.joblib logreg_classifier.joblib ./my_server/

WORKDIR /my_server/

CMD uvicorn main:api --host 0.0.0.0
