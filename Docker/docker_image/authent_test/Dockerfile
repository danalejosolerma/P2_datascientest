FROM ubuntu:latest
RUN apt-get update && apt-get install python3-pip -y && pip install requests
ADD authentication_test.py /my_server/authentication_test.py
WORKDIR /my_server/
CMD python3 authentication_test.py
