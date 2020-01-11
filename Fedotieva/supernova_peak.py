import requests
import json
import numpy as np
import argparse
import julian

#Function shows data sources
def print_source(source, alias, name, reference, bibcode, url):
	print('Source(s): ')
	source_s = source.split(',')
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




#Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('name', action='store', type = str, help = 'Supernova name') 
parser_args = parser.parse_args()
SN_name = parser_args.name

#Check request status
try:
	response = requests.get('https://sne.space/astrocats/astrocats/supernovae/output/json/'+SN_name+'.json')
	response.raise_for_status()
except Exception as e:
	print(e)
	raise SystemExit

data = response.json()

#Get information about maximum from output data

maxappmag = data[SN_name]['maxappmag'][0]['value']
maxappmag_source = data[SN_name]['maxappmag'][0]['source']
maxband = data[SN_name]['maxband'][0]['value']
maxdate = data[SN_name]['maxdate'][0]['value']

maxvisualappmag = data[SN_name]['maxvisualappmag'][0]['value']
maxvisualappmag_source = data[SN_name]['maxvisualappmag'][0]['source']
maxvisualband = data[SN_name]['maxvisualband'][0]['value']
maxvisualdate = data[SN_name]['maxvisualdate'][0]['value']


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
band_names = set(band)

time = np.asarray(time)
mag = np.asarray(mag)
band = np.asarray(band)
source = np.asarray(source)

bibcode = np.asarray(bibcode)
reference = np.asarray(reference)
alias = np.asarray(alias)

#Output data information

print(f'max {maxband} band value\t{maxappmag}')
print(f'max date\t{maxdate}')
print_source(maxappmag_source, alias, name, reference, bibcode, url)
print('\n')

print(f'max {maxvisualband} band value\t{maxvisualappmag}')
print(f'max date\t{maxvisualdate}')
print_source(maxvisualappmag_source, alias, name, reference, bibcode, url)
print('\n')



#Derived information
for b in band_names:
	ind = band==b
	time_ = time[ind]
	mag_ = mag[ind]
	source_ = source[ind]
	i_max = np.argmin(mag_)
	print(f'{b} band')
	print(f'MJD max\t{time_[i_max]}')
	date = julian.from_jd(time_[i_max], fmt='mjd')
	print(f'Time max\t{date}')
	print(f'{b} value max\t{mag_[i_max]}')
	print_source(source_[i_max], alias, name, reference, bibcode, url)
		
	print('\n')

 

