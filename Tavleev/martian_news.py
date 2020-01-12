import os
import random
import sys
import datetime

import requests
from flask import Flask, render_template, abort, Response

app = Flask(__name__)
months = {'1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May', '6': 'June', '7': 'July',
          '8': 'August', '9': 'September', '10': 'October', '11': 'November', '12': 'December'}

NASA_API_key = os.environ.get('NASA_API')
if NASA_API_key is None:
    print('NASA_API is required for correct work of server. Enter NASA_API')
    sys.exit(1)


def Wiki_text(year, month, day):
    date = months[month] + ' ' + day

    par = {
        'action': 'parse',
        'format': 'json',
        'page': date,
        'section': '1',
    }
    text = requests.get('https://en.wikipedia.org/w/api.php', params=par).json()['parse']['text']['*']
    return text, year + ' ' + date


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


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route('/<date>')
def main_site(date):
    numer = date.find('-')
    if numer == -1:
        abort(404)
    year = date[:numer]
    date1 = date[numer + 1:]
    numer = date1.find('-')
    if numer == -1:
        abort(404)
    month = date1[:numer]
    day = date1[numer + 1:]
    try:
        datetime.date(int(year), int(month), int(day))
    except ValueError:
        abort(404)

    textum, date_final = Wiki_text(year, month, day)
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
    app.run('0.0.0.0', 5000)
