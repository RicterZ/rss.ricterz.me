FROM ubuntu:22.04

WORKDIR /opt/crawler

COPY sources.list /etc/apt
RUN apt update && apt -y install python3 python3-pip proxychains
ENV all_proxy=http://192.168.13.1:7890
ADD requirements.txt /opt/crawler
RUN pip3 install -r requirements.txt

ADD conf/proxychains.conf /etc
ADD rsser /opt/crawler/rsser

RUN mkdir /opt/crawler/data
ENTRYPOINT python3 -m rsser.server
