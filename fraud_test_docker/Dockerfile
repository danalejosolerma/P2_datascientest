FROM ubuntu:latest

RUN apt-get update && apt-get install python3-pip -y curl && pip3 install fastapi requests uvicorn

ADD content.py /my_server/fraud_api_test.py

WORKDIR /my_server/

CMD python3 fraud_api_test.py
