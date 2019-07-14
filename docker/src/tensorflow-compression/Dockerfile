FROM python:3.4

LABEL maintainer="justdoit920823@gmail.com"

RUN pip install tensorflow==1.13.1

RUN pip install tensorflow-compression==1.2b1

RUN mkdir /app

VOLUME /app

COPY tfci.py /app/

WORKDIR /app
