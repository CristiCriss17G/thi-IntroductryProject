# to get RUN-output: export DOCKER_BUILDKIT=0 in shell before docker compose build
FROM python:3.7.17-slim

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
     apt-get -y install gcc mono-mcs && \
     apt-get -y install g++ && \
     rm -rf /var/lib/apt/lists/*
#WORKDIR /app
#COPY . .

RUN python3.7 -m pip install --upgrade pip
RUN pip install -U pip setuptools wheel
RUN pip install flask
RUN pip install gunicorn
RUN pip install chatterbot==1.0.8
RUN pip install --use-pep517 spacy==2.1.8
RUN python -m spacy download en
