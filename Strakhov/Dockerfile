FROM python:3.8-buster

RUN apt-get update\
    && apt-get install -y libproj-dev proj-data proj-bin libgeos-dev

RUN pip install gunicorn

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8888

ENTRYPOINT ["gunicorn", "-w4", "-b0.0.0.0:8888", "skyStar:app"]
