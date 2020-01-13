#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from bs4 import BeautifulSoup
import re
import requests


def gain_json(api_key, date):
    res = []
    print(api_key)
    if not api_key:
        api_key = 'DEMO_KEY'
    print(f'https://api.nasa.gov/planetary/apod?api_key={api_key}&date={date}')
    r = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={api_key}&date={date}').json()

    if not date:
        date = r["date"]

    date_astro = date[8:10] + '.' + date[5:7] + '.' + date[:4]
    if date_astro[0] == '0':
        date_astro = date_astro[1:]
    res.append(r)
    res.append(date)
    res.append(date_astro)
    return res


app = Flask(__name__)


@app.route('/<api_key>/<date>/picture')
def api_key_date_picture(api_key, date):
    r, date, date_astro = gain_json(api_key, date)

    resp = requests.get(f'http://www.astronet.ru/db/apod.html?d={date}')
    soup = BeautifulSoup(resp.text)

    date_position = soup.find(string=re.compile(date_astro))
    if not date_position:
        return render_template('error404.html'), 404

    main = date_position.parent.find_next().text
    url = date_position.parent.find_previous().find_previous().find_previous()
    title_rus = url.text
    url_add = str(url)
    url = url_add.split('\"')[1]
    if url[:4] != 'http':
        url = 'http://www.astronet.ru' + url
    print(url)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text)

    month = str(soup.find('a', href=f'/db/apod.html?d={date[:7]}').parent.text)

    if soup.find(string=re.compile("Пояснение:")):
        exp_rus = str(soup.find(string=re.compile("Пояснение:")).parent.parent.text)
        exp_pos = exp_rus.find("Пояснение:")
        if exp_rus.find(month, exp_pos):
            exp_rus = exp_rus[exp_pos + len("Пояснение:"):exp_rus.find(month, exp_pos) - 4]
        else:
            exp_rus = exp_rus[exp_pos + len("Пояснение:"):]
    else:
        title_rus = ''
        exp_rus = 'Русский перевод отсутствует.'

    if soup.find(string=re.compile("Перевод:")):
        translate = soup.find(string=re.compile("Перевод:")).parent.find_previous().text
    else:
        translate = ''

    if soup.find(string=re.compile("Авторы и права:")):
        copyright_rus = soup.find(string=re.compile("Авторы и права:")).parent.text
    else:
        copyright_rus = ''

    return render_template("Astronomy Picture of the Day.html", explanation=r.get("explanation"),
                           explanation_rus=exp_rus,
                           url=r.get("url"), hdurl=r.get("hdurl"), main=main, title=r.get("title"), title_rus=title_rus,
                           date=date_astro, copyright=r.get("copyright"), copyright_rus=copyright_rus,
                           translate=translate)


@app.route('/<api_key>/picture')
def api_key_picture(api_key):
    return api_key_date_picture(api_key, '')


@app.route('/picture')
def api_picture():
    return api_key_date_picture('DEMO_KEY', '')


@app.route('/<api_key>/<date>')
def api_key_date(api_key, date):
    print(api_key)
    if api_key == 'favicon.ico':
        return favicon()
    r, date, date_astro = gain_json(api_key, date)

    resp = requests.get(f'http://www.astronet.ru/db/apod.html?d={date}')
    soup = BeautifulSoup(resp.text)

    date_position = soup.find(string=re.compile(date_astro))

    if not date_position:
        return render_template('error404.html'), 404

    url = date_position.parent.find_previous().find_previous().find_previous()
    r['title'] = str(url.text).strip()
    url_add = str(url)
    url = url_add.split('\"')[1]
    if url[:4] != 'http':
        url = 'http://www.astronet.ru' + url
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text)

    month = str(soup.find('a', href=f'/db/apod.html?d={date[:7]}').parent.text)

    if soup.find(string=re.compile("Пояснение:")):
        exp_rus = str(soup.find(string=re.compile("Пояснение:")).parent.parent.text)
        exp_pos = exp_rus.find("Пояснение:")
        if exp_rus.find(month, exp_pos):
            exp_rus = exp_rus[exp_pos + len("Пояснение:"):exp_rus.find(month, exp_pos) - 4]
        else:
            exp_rus = exp_rus[exp_pos + len("Пояснение:"):]
        r['explanation'] = exp_rus.strip()

    if soup.find(string=re.compile("Авторы и права:")):
        r['copyright'] = str(soup.find(string=re.compile("Авторы и права:")).parent.text).strip()

    return r


@app.route('/<api_key>/<date>/')
def api_key_date_s(api_key, date):
    return api_key_date(api_key, date)


@app.route('/<api_key>')
def api_key_(api_key):
    return api_key_date(api_key, '')


@app.route('/<api_key>/')
def api_key_s(api_key):
    return api_key_date(api_key, '')


@app.route('/')
def api():
    return api_key_date('DEMO_KEY', '')


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
