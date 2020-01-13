from django.shortcuts import render
from io import BytesIO
import base64
import astropy
import matplotlib.pyplot as plt
import matplotlib; matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from astroplan.plots import plot_airmass
from astroplan.plots import plot_altitude
from astroplan import FixedTarget
from astroplan import Observer
from astropy.coordinates import SkyCoord
from astropy.coordinates import Angle
from astropy.time import Time
import astropy.units as u
import matplotlib.dates as mdates
from matplotlib import rc, rcParams
import matplotlib.font_manager
import numpy as np
import math
import django.utils
from django.http import HttpResponseNotFound

def index(request):
    if request.method == 'POST':
        try:
            content = {
            'Name':request.POST["Name"],
            'Times':request.POST["Times"],
            'image': "data:image/png;base64,"+ base64.b64encode(createPicture(request.POST["Name"], request.POST["Times"])).decode("UTF-8")
            }

        except astropy.coordinates.name_resolve.NameResolveError:
            return HttpResponseNotFound("NOT RESOLVED YOUR STAR")

        except ValueError:
            return HttpResponseNotFound("INVALID VALUE (PRESUMABLY FOR DATE)")

        return render(request, 'stars/index.html', content)
    return render(request, 'stars/index.html')



def createPicture(name, times):
    rcParams['font.size'] = 13
    rcParams['lines.linewidth'] = 3
    rcParams['lines.markersize'] = 0
    rcParams['grid.linestyle'] = '--'
    rcParams['axes.titlepad'] = 13
    rcParams['xtick.direction'] = 'in'
    rcParams['ytick.direction'] = 'in'
    rcParams['xtick.top'] = True
    rcParams['ytick.right'] = True
    rcParams['font.family'] = 'serif'
    rcParams['mathtext.fontset'] = 'dejavuserif'
    rc('legend', fontsize=13)
    rc('xtick.major', size=5, width=1.5)
    rc('ytick.major', size=5, width=1.5)
    rc('xtick.minor', size=3, width=1)
    rc('ytick.minor', size=3, width=1)

    star_name = name
    star_style = {'linestyle': '--', 'linewidth': 4, 'color': 'tomato'}
    star = FixedTarget.from_name(star_name)

    longitude_kgo = 42.6675*u.deg
    latitude_kgo = 43.73611*u.deg
    elevation_kgo = 2112*u.m

    kgo = Observer(longitude=longitude_kgo, latitude=latitude_kgo,
                      elevation=elevation_kgo, name="KGO", timezone="Europe/Moscow")

    observe_time = Time(times)
    visible_time = observe_time + np.linspace(-10, +10, 25)*u.hour
    stars_alts = kgo.altaz(visible_time, star).alt
    sun_alts = kgo.sun_altaz(visible_time).alt
    
    moon_coord = kgo.moon_altaz(visible_time)
    star_coord = kgo.altaz(visible_time, star)
    angle = moon_coord.separation(star_coord)
    moon_star = angle.deg


    locator = mdates.MonthLocator() 
    fmt = mdates.DateFormatter('%b')

    canvas = FigureCanvasAgg(plt.figure(1))
    plt.figure(figsize=(8,7))
    plt.subplot(211)
    plt.plot_date(visible_time.plot_date, stars_alts, linestyle = '-.', color = 'mediumslateblue', label = star_name)
    plt.plot_date(visible_time.plot_date, sun_alts, linestyle = '-.', color = 'gold', label = 'Sun')
    plt.ylim(0, np.max([stars_alts, sun_alts]) + 5)
    plt.ylabel('Altitude, degrees')
    plt.legend(shadow=True, loc="best")
    plt.gcf().autofmt_xdate() 
    plt.grid()

    plt.subplot(212)
    plt.plot_date(visible_time.plot_date, moon_star, linestyle = '-', color = 'slategrey')
    plt.ylabel('Moon-Star angle, degrees')
    plt.gcf().autofmt_xdate() 
    plt.grid()
    data = BytesIO()

    plt.savefig(data, format='png')
    return data.getvalue()

