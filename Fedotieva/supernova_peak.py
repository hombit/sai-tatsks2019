import requests
from requests.exceptions import HTTPError
import json
import numpy as np
import argparse
import julian

#Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('name', action='store', type = str, help = 'Supernova name') 
parser_args = parser.parse_args()
SN_name = parser_args.name

#Check request status
try:
	response = requests.get('https://sne.space/astrocats/astrocats/supernovae/output/json/'+SN_name+'.json')
	response.raise_for_status()
except HTTPError:
	print('Supernova '+SN_name+' is not found')
	raise SystemExit

data = response.json()

#Get photometry and source information from json
photometry_list = data[SN_name]['photometry']
sources_list = data[SN_name]['sources']

band = []
time = []
mag = []
source = []

name = []
bibcode = []
reference = []
url = []
alias = []

#Extract needed data
for element in photometry_list:
	try:
		band.append(element['band'])
	except KeyError:
		continue
	time.append(float(element['time']))
	mag.append(float(element['magnitude']))
	source.append(element['source'])

for element in sources_list:
	try:
		name.append(element['name'])
	except KeyError:
		name.append("no name")
	try:
		bibcode.append(element['bibcode'])
	except KeyError:
		bibcode.append("no bibcode")
	try:
		reference.append(element['reference'])
	except:
		reference.append("no reference")
	try:
		url.append(element['url'])
	except KeyError:
		url.append("no url")

	alias.append(element['alias'])

#Find available bands
band_names = []

for b in band:
	if b in band_names:
		continue
	else:
		band_names.append(b)

time = np.asarray(time)
mag = np.asarray(mag)
band = np.asarray(band)
source = np.asarray(source)

bibcode = np.asarray(bibcode)
reference = np.asarray(reference)
alias = np.asarray(alias)

#Output information
for b in band_names:
	ind = band==b
	time_ = time[ind]
	mag_ = mag[ind]
	source_ = source[ind]
	i_max = np.argmin(mag_)
	print(b+' band')
	print('MJD max\t', time_[i_max])
	print('Time max\t', julian.from_jd(time_[i_max], fmt='mjd'))
	print(b+' value max\t', mag_[i_max])
	print('Source(s): ')
	source_s = source_[i_max].split(',')
	for s in source_s:
		i, = np.where(alias==s)
		i = i[0]
		source_list = []
		if name[i] != "no name":
			source_list.append(name[i])
		if reference[i] != "no reference":
			source_list.append(reference[i])
		if bibcode[i] != "no bibcode":
			source_list.append(bibcode[i])
		if url[i] != "no url":
			source_list.append(url[i])

		print(source_list)

		
	print('\n')

 

