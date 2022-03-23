FROM ubuntu:18.04

WORKDIR /opt/crawler

RUN apt update && apt -y install python python-pip proxychains
ADD requirements.txt /opt/crawler
RUN pip install -r requirements.txt

ADD conf/proxychains.conf /etc
ADD rsser /opt/crawler/rsser

RUN mkdir /opt/crawler/data
ENTRYPOINT python -m rsser.server
