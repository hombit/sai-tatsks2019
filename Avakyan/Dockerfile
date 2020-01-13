FROM python:3.8-buster

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

VOLUME /app/data

ENTRYPOINT ["python", "GarryPovar.py"]
