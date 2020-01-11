import os
import random
import sys

import requests
from flask import Flask, render_template

app = Flask(__name__)
months = {'1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May', '6': 'June', '7': 'July',
          '8': 'August', '9': 'September', '10': 'October', '11': 'November', '12': 'December'}


def Wiki_text(date):
    numer = date.find('-')
    year = date[:numer]
    date = date[numer+1:]
    numer = date.find('-')
    date_final = months[date[:numer]] + ' ' + date[numer+1:]
    par = {
        'action': 'parse',
        'format': 'json',
        'page': date_final,
        'section': '1',
    }
    text = requests.get('https://en.wikipedia.org/w/api.php', params=par).json()['parse']['text']['*']
    return text, year + ' ' + date_final


def NASA_photo(date):
    par = {'earth_date': date,
           'api_key': NASA_API_key}
    p = requests.get('https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos', params=par).json()['photos']
    if len(p) == 0:
        return False, date
    else:
        link = p[random.randint(0, len(p) - 1)]['img_src']
        return True, link


@app.route('/')
def title_site():
    return render_template('main_site.html')


@app.route('/favicon.ico')
def favicon():
    return '1'


@app.route('/<date>')
def main_site(date):
    textum, date_final = Wiki_text(date)
    flag, photo_link = NASA_photo(date)
    if flag:
        link = photo_link
        not_image = False
    else:
        link = False
        not_image = True
    return render_template('site.html', datum='Martian news for ' + date_final,
                           image=link, not_image=not_image, textx=textum)


if __name__ == '__main__':
    NASA_API_key = os.environ.get('NASA_API')
    if NASA_API_key is not None:
        app.run('0.0.0.0', 5000)
    else:
        print('Enter NASA_API')
        sys.exit(1)

