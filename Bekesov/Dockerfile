FROM python:3.8-buster

COPY . /app/
WORKDIR /app
RUN python setup.py install

WORKDIR /
VOLUME /data

ENTRYPOINT ["OGLI.py"]
