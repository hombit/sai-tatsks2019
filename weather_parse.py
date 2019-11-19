#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import requests
import pickle
import os
from datetime import datetime
import socket
#cron 
#1 0,3,6,9,12,15,18,21 * * * .../weather_parse.py

#testing dark sky forecast data
#Почему darksky?
#мне удалось найти два сервиса, согласных бесплатно отдавать хоть чуть-чуть релевантное по API
#darksky и weatherbit.io Оба выдают почасовое усреднение(свое) gfs и icon (Это две основные бесплатные модели)
#weather underground закрыл api год назад. Да и ну их, с proprietary forecasting system BestForecast(tm)

city='KGO'
lat='43.74611'		
lon='42.6675'

def kgo_METEO():
	try:
		sock = socket.socket()
		sock.settimeout(0.5)
		sock.connect(('37.29.115.163', 16303))			#сокет сервер метеостанции КГО
		sock.send('1 get data\n'.encode('ascii'))
		data = sock.recv(1024).decode()[5:].split()
		sock.close()
		kgo_vailasa={}
		for p in data:
			tmp = p.split('=')
			try:
				kgo_vailasa[tmp[0]]=float(tmp[1])		
			except:
				if len(tmp)==2:						#на всякий случай, что бы одно кривое поле не обвалило все данные с метеостанции
					kgo_vailasa[tmp[0]]=tmp[1]
				else:
					kgo_vailasa[tmp[0]]=None
	except Exception as e:
		print('SOCKET ERROR')
		print(str(e))
		kgo_vailasa={}
	return kgo_vailasa

with open('key.txt') as f:					#read api key
	api_key = str(f.readline()[:-1])

url='https://api.darksky.net/forecast/'+api_key+'/'+lat+','+lon				#api ссылка

querystring = {"lang":"en","units":"si","exclude":"minutely,daily,alerts,flags"}		#выбираем только нужные прогнозы
try:
	response = requests.request("GET", url, params=querystring)
	resp_dict_current = response.json()['currently']
	resp_dict_forecast = response.json()['hourly']		
except Exception as e:
	print(str(e))
	resp_dict_current = {}
	resp_dict_forecast={}

kgo_vailasa = kgo_METEO()

now = datetime.now()
now = now.replace(second = 0)
now = now.replace(minute=0)
now = now.replace(microsecond = 0)				#округляем время

ontimeDict = {'time':now,'current':resp_dict_current, 'forecast':resp_dict_forecast, 'meteo':kgo_vailasa}		#Создаем словарь c прогнозами
print(now)
print(city,'darksky current weather',resp_dict_current)
#print(now,city,resp_dict_forecast)
print(city,'meteostation',kgo_vailasa)

path=os.path.dirname(os.path.abspath(__file__) )+'/'

with open(path+now.strftime('%Y_%m_%dT%H_%M_%S')+'.pkl',"wb") as f:			#пишем в файл для дальнейшей обработки
	pickle.dump(ontimeDict,f)


#writing test
# with open('2019_11_19T19_00_00.pkl',"rb") as f:
# 	mydict = pickle.load(f)
# print(mydict['forecast'].keys())
# print(datetime.fromtimestamp(mydict['forecast']['data'][-1]['time']) )
