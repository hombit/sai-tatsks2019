import requests
import sys
import csv
import os

name = sys.argv[1]

def get_lightcurve(band, name):
    
    length = len(name)
    
    dirfile = "http://ogledb.astrouw.edu.pl/~ogle/CVS/data/{}/{}/".format(band, name[length - 2] + name[length-1])

    fullpath = dirfile + name + ".dat"

    filereq = requests.get(fullpath)

    lightcurve = filereq.text

    dir = "data"
    
    os.makedirs(dir, exist_ok=True)
    
    filename = "{}-{}.csv".format(name, band)

    with open(dir.filename, "wt") as file:

        file.write("HJD-2450000   mag  err")

        file.write("\n")

        file.write(lightcurve)

    
get_lightcurve("I", name)

get_lightcurve("V", name)