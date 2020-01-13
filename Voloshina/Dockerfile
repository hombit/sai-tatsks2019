FROM python:3.8-buster

RUN pip install daphne

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY ./kgo /app
WORKDIR /app

EXPOSE 8888

ENTRYPOINT ["daphne", "-b0.0.0.0", "-p8888", "kgo.asgi:application"]
