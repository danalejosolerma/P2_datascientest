FROM ubuntu:latest
RUN apt-get update && apt-get install python3-pip -y && pip install requests
ADD authorization_test.py /my_server/authorization_test.py
WORKDIR /my_server/
CMD python3 authorization_test.py
