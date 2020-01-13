import requests
import sys
import csv
import os

name = sys.argv[1]

def get_lightcurve(band, name):
    
    length = len(name)
    
    url = "http://ogledb.astrouw.edu.pl/~ogle/CVS/data/{}/{}/{}{}".format(band, name[-3:], name, ".dat")

    filereq = requests.get(url)

    lightcurve = filereq.text

    dir = "data"

    filename = "{}-{}.csv".format(name, band)
    
    os.makedirs(dir, exist_ok=True)

    os.path.join(dir, filename)
    
    with open(filename, "wt") as file:

        file.write("HJD-2450000   mag  err")

        file.write("\n")

        file.write(lightcurve)

    
get_lightcurve("I", name)

get_lightcurve("V", name)