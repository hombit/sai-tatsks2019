import requests
import sys
import csv

name = sys.argv[2]

length = len(name)

band = sys.argv[1]

dirfile = "http://ogledb.astrouw.edu.pl/~ogle/CVS/data/{}/{}/".format(band, name[length - 2] + name[length-1])

fullpath = dirfile + name + ".dat"

filereq = requests.get(fullpath)

lightcurve = filereq.text

with open(name + ".csv", "wt") as file:

       file.write("HJD-2450000   mag  err")

       file.write("\n")

       file.write(lightcurve)
