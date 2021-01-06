import requests
import json
import csv
import datetime
import schedule 

# Сайт https://openweathermap.org/

latitude_kgo = "43.74611"
longitude_kgo = "42.6675"


def hourly_weather_KGO(latitude, longitude, API_key, table):
    """Take weather parameters each minute or hour"""

    param_for_url = {'lat':latitude, 'lon':longitude, 'appid':API_key, 'units':'metric'}

    json_data = requests.get('https://api.openweathermap.org/data/2.5/onecall', params=param_for_url).json()

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
        #lat = input("Write latitude of the place: ")  #uncomment if custom coordinates are needed 
        #lon = input("Write longitude of the place: ")
        lat = latitude_kgo # use KGO coordinates
        lon = longitude_kgo
        
        regime = input("Do you want to save data every minute or hour? Write minute(or min) or hour: ")

        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)

        with open('api_key.txt') as a:			
            api_key = a.read().strip()

        if regime == 'minute' or regime == 'min':
            print('Activate ', regime, 'save regime')
            i = 1
                
        elif regime == 'hour':
            print('Activate ', regime, 'save regime')
            i = 60

        else:
            raise ValueError('Command is not available, write "min" or "hour"!')

            
        schedule.every(i).minutes.do(hourly_weather_KGO, lat, lon, api_key, writer)
            
        while True:   
            schedule.run_pending()
        



   
if __name__ == "__main__":
    main()

