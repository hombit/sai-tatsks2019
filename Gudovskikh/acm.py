import numpy as np
from influxdb import InfluxDBClient
import datetime
import argparse

def createParser():
	parser = argparse.ArgumentParser(prog='acm.py')

	parser.add_argument ('-p', '--plot', action='store_const', const=True, default=False, 
		help = 'make plot')

	parser.add_argument ('-c', '--console', action='store_const', const=True, default=False, 
	 help = 'print data')


	return parser

parser = createParser()
namespace = parser.parse_args()


client = InfluxDBClient(host='eagle.sai.msu.ru', port=80)
base=client.get_list_database()
#print(base)
response = client.query('SELECT * FROM "mass.seeing" WHERE time > now() - 365d; ',database='taxandria')

print('response done')

data_list = list(response)[0]

time_array=[]

for point in data_list:
	if point['type']!='profile':
		continue

	point_time = datetime.datetime.strptime(point['time'],'%Y-%m-%dT%H:%M:%SZ')
	time_array.append(point_time)

time_array=np.array(time_array)

start_time = time_array[0]
period = time_array[-1]-time_array[0]
length_bin = datetime.timedelta(days = 30)

N = period//length_bin

time_dat=[]
sky_dat = []

for i in range(N):
	mask = (start_time+i*length_bin<time_array) & (time_array<start_time+(i+1)*length_bin)
	needed_points = time_array[mask]

	number_points=0
	for k in range(len(needed_points)-1):
		tdelt = (needed_points[k+1]-needed_points[k]).total_seconds() 
		if tdelt<300:
			number_points+=tdelt

	time_dat.append(start_time+(i+0.5)*length_bin)
	sky_dat.append(number_points/3600)

print('parsing done')

if namespace.console:
	for i in range(len(time_dat)):
		print(time_dat[i].strftime('%m.%Y'),':',int(sky_dat[i]),'h')

if namespace.plot:
	import matplotlib.pyplot as plt
	plt.figure(figsize=(13,7))
	plt.plot(time_dat,sky_dat,'o')
	plt.ylabel('hours of open dome')
	plt.xlabel('time')
	plt.title('KGO open dome')
	plt.show()
