import os
import random
import sys

import requests
from flask import Flask, render_template

app = Flask(__name__)
months = {'1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May', '6': 'June', '7': 'July',
          '8': 'August', '9': 'September', '10': 'October', '11': 'November', '12': 'December'}


def Wiki_text(data):
    numer = data.find('-')
    year = data[:numer]
    data = data[numer+1:]
    numer = data.find('-')
    data_final = months[data[:numer]] + ' ' + data[numer+1:]
    par = {
        'action': 'parse',
        'format': 'json',
        'page': data_final,
        'section': '1',
    }
    text = requests.get('https://en.wikipedia.org/w/api.php', params=par).json()['parse']['text']['*']
    return text, year + ' ' + data_final


def NASA_photo(data):
    par = {'earth_date': data,
           'api_key': NASA_API_key}
    p = requests.get('https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos', params=par).json()['photos']
    if len(p) == 0:
        return False, data
    else:
        link = p[random.randint(0, len(p) - 1)]['img_src']
        return True, link


@app.route('/')
def title_site():
    return render_template('main_site.html')


@app.route('/<data>')
def main_site(data):
    textum, data_final = Wiki_text(data)
    flag, photo_link = NASA_photo(data)
    if flag:
        link = photo_link
        not_image = False
    else:
        link = False
        not_image = True
    return render_template('site.html', datum='Martian news for ' + data_final,
                           image=link, not_image=not_image, textx=textum)


if __name__ == '__main__':
    NASA_API_key = os.environ.get('NASA_API')
    if NASA_API_key is not None:
        app.run('0.0.0.0', 5000)
    else:
        print('Enter NASA_API')
        sys.exit(1)

