#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import numpy as np
from influxdb import InfluxDBClient
import datetime
from astropy.coordinates import get_sun, EarthLocation, AltAz
import astropy.units as u
from astropy.time import Time
from astropy.utils import iers
iers.conf.auto_download = False

KGO_scope = EarthLocation(lat=43.73616497258118*u.deg, lon=42.66745996540703*u.deg, height=2112.*u.m)


client = InfluxDBClient(host='eagle.sai.msu.ru', port=80)

response = client.query('''SELECT * FROM "prephot.extinction" WHERE time > now() - 365d AND type = 'flux' ; ''',database='taxandria')

print('response done')

data_list = list(response)[0]

#print(data_list)

time_array=[]
data_arr = []
for point in data_list:
	point_time = datetime.datetime.strptime(point['time'],'%Y-%m-%dT%H:%M:%SZ')
	time_array.append(point_time)
	data_arr.append(point['value'])

time_array = np.array(time_array)
data_arr = np.array(data_arr)

AStime = Time(time_array, scale='utc' ) 
nowFrame = AltAz(obstime=time_array,location=KGO_scope)	
sun_alt =np.array(get_sun(AStime).transform_to(nowFrame).alt.deg)

mask = (data_arr <1) & (sun_alt<-12)
time_array=time_array[mask]
sun_alt=sun_alt[mask]

def calculate_time(time_array):
	time_points=0
	for k in range(len(time_array)-1):
		tdelt = (time_array[k+1]-time_array[k]).total_seconds() 
		if tdelt<300:
			time_points+=tdelt
	return round(time_points/3600)

htime12 = calculate_time(time_array)
print(htime12, 'hours of clear sky with sun altitude less then -12')

time_array=time_array[sun_alt>-18]

print(htime12 - calculate_time(time_array), 'hours of clear sky with sun altitude less then -18')

