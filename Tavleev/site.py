from flask import Flask, render_template
import requests
import random

app = Flask(__name__)
months = {'1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May', '6': 'June', '7': 'July',
          '8': 'August', '9': 'September', '10': 'October', '11': 'November', '12': 'December'}


def Wiki_text(data):
    numer = data.find('-')
    data_final = months[data[:numer]] + ' ' + data[numer+1:]
    par = {
        'action': 'parse',
        'format': 'json',
        'page': data_final,
        'section': '1',
    }
    text = requests.get('https://en.wikipedia.org/w/api.php', params=par).json()['parse']['text']['*']
    return [text, data_final]


@app.route('/')
def hello_world():
    return render_template('main_site.html')


@app.route('/<data>')
def NASA_photo(data):
    while True:
        dat = random.randint(2012, 2019)
        par = {'earth_date': str(dat) + '-' + data,
               'api_key': NASA_API_key}
        p = requests.get('https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos', params=par).json()['photos']
        if len(p) != 0:
            break
    link = p[random.randint(0, len(p) - 1)]['img_src']
    textum = Wiki_text(data)
    return render_template('site.html', datum='Martian news for ' + textum[1], image=link, textx=textum[0])


if __name__ == '__main__':
    NASA_API_key = 'API'  # Your NASA_API_key here
    app.run('0.0.0.0', 5000)
