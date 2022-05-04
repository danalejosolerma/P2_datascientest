FROM ubuntu:latest

ADD requirements.txt /requirements.txt

RUN apt-get update && apt-get install python3-pip -y && pip install -r requirements.txt

COPY main.py ML_models/features.json ML_models/knn_classifier.joblib ML_models/logreg_classifier.joblib ./my_server/

WORKDIR /my_server/

EXPOSE 8000

CMD uvicorn main:api --host 0.0.0.0
