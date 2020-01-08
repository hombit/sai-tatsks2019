FROM python:3.8-buster

RUN apt-get update\
    && apt-get install -y libproj-dev proj-data proj-bin libgeos-dev

RUN mkdir /app
WORKDIR /app

EXPOSE 8888

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

CMD ["python", "skyStar.py"]
