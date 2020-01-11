from flask import Flask, render_template
from bs4 import BeautifulSoup
import re
import requests

app = Flask(__name__)


@app.route('/')
def homepage():
    try:
        key_file = open('key.txt')
    except IOError:
        api_key = 'DEMO_KEY'
        date = ''
    else:
        with key_file:
            api_key = str(key_file.readline())
            date = str(key_file.readline())
    api_key = api_key.rstrip()
    date = date.rstrip()
    print('https://api.nasa.gov/planetary/apod?api_key=' + api_key + '&date=' + date)
    r = requests.get('https://api.nasa.gov/planetary/apod?api_key=' + api_key + '&date=' + date).json()

    if not date:
        date = r["date"]

    date_astro = date[8:10] + '.' + date[5:7] + '.' + date[:4]
    if date_astro[0] == '0':
        date_astro = date_astro[1:]

    resp = requests.get("http://www.astronet.ru/db/apod.html?d=" + date)
    soup = BeautifulSoup(resp.text)

    date_position = soup.find(string=re.compile(date_astro))
    if not date_position:
        print('На дату: ' + date_astro + ' астрономической картинки дня нет.')
        return render_template("Astronomy Picture of the Day.html", main='На дату: ' + date_astro + ' астрономической '
                                                                                                    'картинки дня '
                                                                                                    'нет')
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

    month = str(soup.find('a', href='/db/apod.html?d=' + date[:7]).parent.text)

    if soup.find(string=re.compile("Пояснение:")):
        exp_rus = str(soup.find(string=re.compile("Пояснение:")).parent.parent.text)
        exp_pos = exp_rus.find("Пояснение:")
        if exp_rus.find(month, exp_pos):
            exp_rus = exp_rus[exp_pos + 10:exp_rus.find(month, exp_pos) - 4]
        else:
            exp_rus = exp_rus[exp_pos + 10:]
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


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
