FROM python:3.8-buster

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY istina.py /app/istina.py

ENTRYPOINT ["python", "/app/istina.py"]
