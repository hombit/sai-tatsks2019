#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import requests
import os
from datetime import datetime
import socket
from urllib.parse import urljoin
import json

KGO_ADDR = ('37.29.115.163',16303)
MAGIC_COMMAND = '1 get data\n'

def Kgo_Meteo_Get_Data(only_one_flag = True):
	try:
		sock = socket.socket()
		sock.settimeout(0.5)
		sock.connect(KGO_ADDR)			#сокет сервер метеостанции КГО
		sock.send(MAGIC_COMMAND.encode('ascii'))
		data = sock.recv(1024).decode()[5:].split()
		sock.close()
		return data
	except socket.timeout:
		if only_one_flag: 
			print('timeout error Meteo')
			return Kgo_Meteo_Get_Data(False)
	except socket.error as e:
		print('SOCKET ERROR')
		print(str(e))


def Meteo_Parse_data(data):
	if data is None:
		return {}

	kgo_vailasa={}
	for p in data:
		tmp = p.split('=')
		try:
			kgo_vailasa[tmp[0]]=float(tmp[1])		
		except ValueError:
			kgo_vailasa[tmp[0]]=None
	return kgo_vailasa

def Darksky_Data(city,lat,lon,only_one_flag = True):
	with open('key.txt') as f:					#read api key
		api_key = str(f.readline()[:-1])

	url=urljoin(urljoin('https://api.darksky.net/forecast/',api_key+'/'),lat+','+lon)			#api ссылка

	querystring = {"lang":"en","units":"si","exclude":"minutely,daily,alerts,flags"}		#выбираем только нужные прогнозы
	response = requests.request("GET", url, params=querystring,timeout=(3,3))
	
	try:
		if response.status_code == 200:
			resp_dict_current = response.json()['currently']
			resp_dict_forecast = response.json()['hourly']	
		else:	
			resp_dict_current = {}
			resp_dict_forecast= {}

	except requests.exceptions.ConnectTimeout :
		if only_one_flag:
			print('timeout error Darksky')
			return Darksky_Data(city,lat,lon,False)

	except requests.exceptions.ConnectionError:
		resp_dict_current = {}
		resp_dict_forecast= {}

	return resp_dict_current, resp_dict_forecast 

def main():
	city='KGO'
	lat='43.74611'		
	lon='42.6675'
	kgo_vailasa = Meteo_Parse_data(Kgo_Meteo_Get_Data())
	resp_dict_current, resp_dict_forecast = Darksky_Data(city,lat,lon)

	now = datetime.now()
	now = now.replace(second = 0)
	now = now.replace(minute=0)
	now = now.replace(microsecond = 0)				#округляем время

	ontimeDict = {'time':now.isoformat(),'current':resp_dict_current, 'forecast':resp_dict_forecast, 'meteo':kgo_vailasa}		#Создаем словарь c прогнозами
	print(now)
	print(city,'darksky current weather',resp_dict_current)
	#print(now,city,resp_dict_forecast)
	print(city,'meteostation',kgo_vailasa)

	path=os.path.dirname(os.path.abspath(__file__) )

	filename = os.path.join(path,'weather.dat')
	if os.path.exists(filename):
		with open(filename,"r") as file:			#читаем из файла то что там было
			Wdat = json.load(file)
	else:
		Wdat={}

	Wdat[now.isoformat()]=ontimeDict
	with open(filename,"w") as file:			#пишем в файл для дальнейшей обработки
		json.dump(Wdat,file)	





if __name__ == "__main__":
	main()

