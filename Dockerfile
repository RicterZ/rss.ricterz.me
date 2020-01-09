FROM ubuntu

WORKDIR /opt/crawler

RUN apt update && apt -y install python python-pip
RUN pip install web.py jinja2 requests beautifulsoup4 lxml

ADD . /opt/crawler


# RUN sed -i '319d' /usr/local/lib/python2.7/dist-packages/web/httpserver.py
ENTRYPOINT python main.py
