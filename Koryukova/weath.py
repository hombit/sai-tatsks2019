import requests
import json
import csv
import datetime
import schedule 

# Сайт https://openweathermap.org/


def hourly_weather_KGO(url, lattitude, longitude, API_key, table):
    """Take weather parameters each minute or hour"""
    json_data = requests.get(url).json()

    row = []
    param_names = ['temp','feels_like','pressure','humidity','clouds','wind_speed','wind_deg']

    row.append(datetime.datetime.now()) 
 
    for i in param_names:

        row.append(json_data['current'][i]) 
  
    table.writerow(row)
        
    print('Data saved', datetime.datetime.now()) #отображаем время в которое произошла запись данных



def main():
    
    fieldnames = ['current_time','temperature','temperature_feel','pressure','humidity','clouds','wind_speed','wind_degree'] #имена колонок
    
    name_of_saved_file = input('Write the name of the file to be saved: ')    

    with open(name_of_saved_file + '.csv', 'w', encoding='utf8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)

        with open('api_key.txt') as a:			
            api_key = a.readline()[:-1]

        lat = input("Write latitude of the place: ")   
        lon = input("Write longitude of the place: ")  

        param_for_url = {'lat':lat,'lon':lon,'appid':api_key,'units':'metric'} 

        url_adress = requests.get('https://api.openweathermap.org/data/2.5/onecall', params=param_for_url)
        
        regime = input("Do you want to save data every minute or hour? Write minute(or min) or hour: ")
        
        if regime == 'minute' or regime == 'min':

            print('Activate ', regime, 'save regime')

            schedule.every(1).minutes.do(hourly_weather_KGO, url_adress.url, lat, lon, api_key, writer)

            while True:   
                schedule.run_pending()
                
        if regime == 'hour':

            print('Activate ', regime, 'save regime')
            
            schedule.every(1).hour.do(hourly_weather_KGO, url_adress.url, lat, lon, api_key, writer)
            
            while True:   
                schedule.run_pending()
        
        else:
            print('Sorry, command not available')
   
if __name__ == "__main__":
    main()

