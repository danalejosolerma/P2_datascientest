FROM ubuntu:20.04

RUN apt-get update && apt-get install python3-pip -y curl && pip3 install fastapi requests uvicorn numpy

ADD fraud_api_test.py integration.py output_knn.json output_logreg.json ./my_server/

WORKDIR /my_server/

CMD python3 fraud_api_test.py
