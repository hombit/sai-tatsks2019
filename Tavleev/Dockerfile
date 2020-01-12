FROM python:3.8-buster

RUN pip install gunicorn

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8888

ENTRYPOINT ["gunicorn", "-w4", "-b0.0.0.0:8888", "martian_news:app"]
