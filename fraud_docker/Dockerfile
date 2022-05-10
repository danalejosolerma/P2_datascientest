FROM ubuntu:20.04

ADD requirements.txt /requirements.txt

RUN apt update && apt install -y apt-transport-https && apt install python3-pip -y && pip install -r requirements.txt

COPY main.py data_test.csv features.json knn_classifier.joblib logreg_classifier.joblib ./my_server/

WORKDIR /my_server/

CMD uvicorn main:api --host 0.0.0.0 --port 8000
