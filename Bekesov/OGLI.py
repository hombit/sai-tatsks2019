import requests

file = input("Enter the catalog name of the star") + ".dat"

length = len(file)

band = input("Enter the band of observations")

dirfile = "http://ogledb.astrouw.edu.pl/~ogle/CVS/data/" + band + "/" + file[length-6] + file[length-5] + "/"

fullpath = dirfile + file

filereq = requests.get(fullpath)

lightcurve = filereq.text

newfile = open(file, "wt")

newfile.write(lightcurve)