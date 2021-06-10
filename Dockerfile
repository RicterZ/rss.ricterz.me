FROM ubuntu:18.04

WORKDIR /opt/crawler

RUN apt update && apt -y install python python-pip proxychains && \
    pip install web.py jinja2 requests beautifulsoup4 lxml

ADD conf/proxychains.conf /etc
ADD rsser /opt/crawler/

ENTRYPOINT proxychains python main.py
