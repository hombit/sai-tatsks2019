import requests
import json
import csv
import datetime
import schedule 

import pandas as pd

# Сайт https://openweathermap.org/

with open('api_key.txt') as a:		# read api key		
    api_key = a.readline()[:-1]


lat = input("Write latitude of the place: ")   #43.74611 KGO latitude
lon = input("Write longitude of the place: ")  #42.6675  KGO longitude

param_for_url = {'lat':lat,'lon':lon,'appid':api_key,'units':'metric'} 

url_adress = requests.get('https://api.openweathermap.org/data/2.5/onecall', params=param_for_url)

regime = input("Do you want to save data every minute or hour?")

fieldnames = ['current_time','temperature','temperature_feel','pressure','humidity','clouds','wind_speed','wind_degree','visibility']
    

def hourly_weather_KGO(url, lattitude, longitude, API_key, table):
    """Take weather parameters each minute or hour"""
    json_data = requests.get(url).json()
        
    table.writerow([datetime.datetime.now(), json_data['current']['temp'], json_data['current']['feels_like'], json_data['current']['pressure'], json_data['current']['humidity'], json_data['current']['clouds'],json_data['current']['wind_speed'],json_data['current']['wind_deg'], json_data['current']['visibility']])
        
    print('Data saved', datetime.datetime.now()) #отображаем время в которое произошла запись данных
    return



if regime == 'minute' or regime == 'min':

    print('Activate ', regime, 'save regime')

    def main():
        
        with open('hourly_weather_KGO.csv', 'w', encoding='utf8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            
            schedule.every(1).minutes.do(hourly_weather_KGO, url_adress.url, lat, lon, api_key, writer)

            while True:   
                schedule.run_pending()
    
        return
    
       
    if __name__ == "__main__":
        main()
        
if regime == 'hour':

    print('Activate ', regime, 'save regime')

    def main():
         
        with open('hourly_weather_KGO.csv', 'w', encoding='utf8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)

            
            schedule.every(1).hour.do(hourly_weather_KGO, url_adress.url, lat, lon, api_key, writer)
            while True:   
                schedule.run_pending()
    
        return
    
    
    if __name__ == "__main__":
        main()  
        
else:
    print('Sorry, command not available')




