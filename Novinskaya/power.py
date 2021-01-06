from influxdb import InfluxDBClient
import numpy as np
from datetime import date
from dateutil.relativedelta import relativedelta
from itertools import groupby


#Пороговое значение напряжения
VOLTAGE_THRESHOLD = 10

def power_kgo():
    client = InfluxDBClient(host='eagle.sai.msu.ru',port=80,database='collectd')
    
    begin_date = date.today() + relativedelta(months=-1)
    end_date = date.today()
    
    #Задаем дату программно 
    begin_date_str = begin_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    query = client.query('''select min(value) from snmp_value where "type"='voltage' and "type_instance"='input' and time >= '{}' and time<= '{}' group by time(1h)'''.format(begin_date_str,end_date_str), database='collectd')
    

    #Временные метки, формат
    data = np.array(query.raw['series'][0]['values'])
    vals = data[:,1].astype(np.double)
    
    
    print('Number of power outages = {}'.format(np.sum(np.diff(np.concatenate([[0],vals<VOLTAGE_THRESHOLD,[0]]))>0)))
    
    client.close()
    
    

if __name__ == '__main__':
    
    power_kgo()
   
  
