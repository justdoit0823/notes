
FROM python:3.6

LABEL maintainer="justdoit920823@gmail.com"

RUN mkdir /app
VOLUME /app

RUN pip install numpy==1.14.0

RUN cd /tmp && git clone https://github.com/thunlp/OpenNE.git && \
    cd /tmp/OpenNE && pip install -r requirements.txt && \
    cd src && python setup.py install && \
    cd /app && rm -rf /tmp/OpenNE

WORKDIR /app

ENTRYPOINT ["python"]
