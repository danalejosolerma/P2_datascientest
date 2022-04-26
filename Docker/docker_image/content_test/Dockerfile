FROM ubuntu:latest
RUN apt-get update && apt-get install python3-pip -y && pip install requests
ADD content_test.py /my_server/content_test.py
WORKDIR /my_server/
CMD python3 content_test.py
