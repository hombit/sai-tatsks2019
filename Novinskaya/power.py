from influxdb import InfluxDBClient
import pandas as pd
import numpy as np
from datetime import datetime


#Пороговое значение напряжения
voltage_threshold = 10

def power_kgo():
    client = InfluxDBClient(host='eagle.sai.msu.ru',port=80,database='collectd')

    #Задаем дату программно
    begin_date = datetime(2020, 11, 30, 0, 0)
    end_date = datetime(2020, 12, 30, 0, 0)
    #end_date = datetime.now()
     
    begin_date_str = begin_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    #Минимальные значения напряжения в определенный период
    query = client.query('''select min(value) from snmp_value where "type"='voltage' and "type_instance"='input' and time >= '{}' and time<= '{}' group by time(1h)'''.format(begin_date_str,end_date_str), database='collectd')
    

    #Временные метки, формат
    data = np.array(query.raw['series'][0]['values'])
    dates = pd.to_datetime(data[:,0])
    vals = data[:,1].astype(np.double)

    indx_less = np.argwhere(vals<voltage_threshold)

    print('Number of power outages = {}'.format(len(indx_less)))

    client.close()
    
    return

if __name__ == '__main__':
    
    power_kgo()
   
