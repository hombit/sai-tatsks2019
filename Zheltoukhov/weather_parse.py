#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import requests
import pickle
import os
from subprocess import call
from datetime import datetime, timezone
import re
from bs4 import BeautifulSoup
import socket
#cron 
#1 0,3,6,9,12,15,18,21 * * * .../weather_parse.py

def kgo_METEO():
	try:
		sock = socket.socket()
		sock.settimeout(0.5)
		sock.connect(('192.168.10.8', 16303))
		sock.send('1 get data\n'.encode('ascii'))
		data = sock.recv(1024).decode()[5:].split()
		sock.close()
		#print(data)
		kgo_vailasa={}
		for p in data:
			tmp = p.split('=')
			try:
				kgo_vailasa[tmp[0]]=float(tmp[1])
			except:
				if len(tmp)==2:
					kgo_vailasa[tmp[0]]=tmp[1]
				else:
					kgo_vailasa[tmp[0]]=None
		print(kgo_vailasa)
	except:
		print('SOCKET ERROR')
		kgo_vailasa={}
	return kgo_vailasa


def got_it(city,lat,lon):
	api_key = 'c96fa545e84b8e9f45c79b25051d2dd8'
	url='https://api.darksky.net/forecast/'+api_key+'/'+lat+','+lon

	# print( type( resp.json()))

	querystring = {"lang":"en","units":"si","exclude":"minutely,hourly,daily,alerts,flags"}
	try:
		response = requests.request("GET", url, params=querystring)
		resp_dict = response.json()['currently']
	except:
		resp_dict = {}


	now = datetime.now(timezone.utc)
	hour= int(round((now.hour+now.minute/60)/3)*3)
	now = now.replace(second = 0)
	now = now.replace(minute=0)
	now = now.replace(microsecond = 0)
	now = now.replace(hour = hour)

	ontimeDict = {'time':now,'current':resp_dict}
	if city =='KGO':
		ontimeDict['meteo']=kgo_METEO()
	print('')
	print('')
	print('')
	print('')
	print(now,city,resp_dict)

	path=os.path.dirname(os.path.abspath(__file__) )+'/'
	try:
		os.makedirs(path+city+'/windy/',exist_ok=True)

		url = 'https://www.windy.com/multimodel/'+lat+'/'+lon+'?55.752,37.639,5'
		name_of_file =path+city+'/windy/'+now.strftime('%Y_%m_%dT%H_%M_%S')+'.html'
		call('vncserver :5',shell=True)
		call('export DISPLAY=":5"',shell=True)
		call(path+'saveme '+url+' --browser "firefox" --destination '+name_of_file+' --load-wait-time 15 --save-wait-time 10',shell=True)
		#name_of_file = './windyMoscow/2019_11_16T19_33_51_windy.html'

		with open(name_of_file) as fp:
		    soup = BeautifulSoup(fp, 'html.parser')

		model_list = soup.findAll(class_='model-box')

		allmodelsdict = {}

		for i in range(4):
			model = model_list[i].get('data-model')
			print(model)

			hours = model_list[i].find(class_="td-hour height-hour d-display-table")
			Timestamps = []
			for time_h in hours:
				Timestamps.append(datetime.fromtimestamp(int(time_h.get('data-ts')[:-3]),timezone.utc) )
			#print('Timestamps',Timestamps[0])

			icons = model_list[i].find(class_="td-icon height-icon d-display-table")
			icons_list = []
			for icon in icons:
				icons_list.append((list(icon.children)[0]).get('src').split('/')[-1] )
			#print('icons_list',icons_list[0])

			temps = model_list[i].find(class_="td-temp height-temp d-display-table")
			temp_list = []
			for temp in temps:
				temp_list.append(int(temp.contents[0][:-1]) )
			#print('temp_list',temp_list[0])

			winds = model_list[i].find(class_="td-wind height-wind d-display-table")
			wind_list = []
			for wind in winds:
				wind_list.append(int(wind.contents[0]) )
			#print('wind_list',wind_list[0])

			winddirs = model_list[i].find(class_="td-windDir height-windDir d-display-table")
			winddir_list = []
			for winddir in winddirs:
				styl = (list(winddir.children)[0]).get('style')
				winddir_list.append(int(re.search(r'\d+',styl).group()) ) 
			#print('winddir_list',winddir_list[0])

			rains = model_list[i].find(class_="td-rain height-rain d-display-table")
			rain_list=[]
			for rain in rains:
				if len(rain.contents)!=0:
					if i!=0:
						rain_list.append(float(rain.contents[0]) ) 
					else:
						rain_list.append(float(rain.contents[0][:-2])*10 ) 
				else:
					rain_list.append(0. ) 
			#print('rain_list',rain_list[0])


			info =  model_list[i].find(class_="multi-model-desc")
			model_time_str = list(info.children)[-1][17:-1]


			if i==2: 
				model_time_str = list(info.children)[-1][17:-1]
				model_time = datetime.strptime(model_time_str,'%Y-%m-%d')
			else:
				model_time_str = list(info.children)[-1][17:-2]
				model_time = datetime.strptime(model_time_str,'%Y-%m-%dT%H:%M:%S')
			
			model_time = model_time.replace(tzinfo=timezone.utc)

			print(model_time)
			# print(Timestamps[0]-model_time)

			model_dict ={'model':model,'model_time':model_time, 'time':Timestamps, 'icon':icons_list, 
			'temperature':temp_list, 'wind_speed':wind_list, 'wind_dir':winddir_list, 'rain':rain_list }

			allmodelsdict[model]=model_dict
	except:
		allmodelsdict={}

	ontimeDict['forecast']=allmodelsdict


	f = open(path+city+'/'+now.strftime('%Y_%m_%dT%H_%M_%S')+'.pkl',"wb")
	pickle.dump(ontimeDict,f)
	f.close()


city='Moscow'
lat='55.7415'		
lon='37.6156'
got_it(city,lat,lon)

city='KGO'
lat='43.74611'		
lon='42.6675'
got_it(city,lat,lon)
