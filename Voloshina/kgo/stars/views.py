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

def index(request):
    if request.method == 'POST':
        try:
            content = {
            'Name':request.POST["Name"],
            'Times':request.POST["Times"],
            'image': "data:image/png;base64,"+ base64.b64encode(createPicture(request.POST["Name"], request.POST["Times"])).decode("UTF-8")
            }
        except:
            content={
            "Error":"404 NOT FOUND YOUR STAR"
            }
        return render(request, 'stars/index.html', content)
    return render(request, 'stars/index.html')



def createPicture(name, times):
    print(type(times))
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

    kgo = Observer(longitude=37.5425*u.deg, latitude=55.701*u.deg,
                      elevation=194*u.m, name="KGO", timezone="Europe/Moscow")
                      #observe_time = Time('2000-01-13 03:00:00')

    start_time = Time('2020-01-01 '+ times)
    end_time = Time('2020-12-31 '+ times)
    delta_t = end_time - start_time
    observe_time = start_time + delta_t*np.linspace(0, 1, 366)
    moon_coord = kgo.moon_altaz(observe_time)
    star_coord = kgo.altaz(observe_time, star)
    angle = moon_coord.separation(star_coord)
    moon_star = angle.deg
    locator = mdates.MonthLocator() 
    fmt = mdates.DateFormatter('%b')

    canvas = FigureCanvasAgg(plt.figure(1))
    plt.figure(figsize=(8,7))
    plt.subplot(211)
    plot_airmass(star, kgo, observe_time, style_kwargs=star_style, altitude_yaxis=True)

    X = plt.gca().xaxis
    X.set_major_locator(locator)
    X.set_major_formatter(fmt)
    plt.gcf().autofmt_xdate() 
    plt.tight_layout()
    plt.grid()

    plt.subplot(212)
    t = Time(observe_time, format='iso', scale='utc')
    plt.plot_date(t.plot_date, moon_star, linestyle = '-', color = 'mediumseagreen', label = star_name+'\n'+times)
    plt.xlim(t.plot_date[0], t.plot_date[-1])
    plt.ylabel('Moon-Star angle, degrees')
    X = plt.gca().xaxis
    X.set_major_locator(locator)
    X.set_major_formatter(fmt)
    plt.grid()
    plt.legend(shadow=True, loc=2)
    data = BytesIO()

    plt.savefig(data, format='png')
    return data.getvalue()
