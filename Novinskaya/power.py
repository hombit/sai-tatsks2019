from influxdb import InfluxDBClient
import numpy as np
#from datetime import datetime, timedelta
#import matplotlib.pyplot as plt

from datetime import date
from dateutil.relativedelta import relativedelta
from itertools import groupby


#Пороговое значение напряжения
VOLTAGE_THRESHOLD = 10

def power_kgo():
    client = InfluxDBClient(host='eagle.sai.msu.ru',port=80,database='collectd')

    #Минимальные значения напряжения в период с 30 ноября по 30 декабря
    #begin_date = datetime(2020, 11, 30, 0, 0)
    #end_date = datetime(2020, 12, 30, 0, 0)
    
    #begin_date = datetime.now()
    #end_date = datetime.now() + timedelta(months=1)
    
    begin_date = date.today() + relativedelta(months=-1)
    end_date = date.today()
    
    #Задаем дату программно 
    begin_date_str = begin_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    query = client.query('''select min(value) from snmp_value where "type"='voltage' and "type_instance"='input' and time >= '{}' and time<= '{}' group by time(1h)'''.format(begin_date_str,end_date_str), database='collectd')
    

    #Временные метки, формат
    data = np.array(query.raw['series'][0]['values'])
    #dates = pd.to_datetime(data[:,0])
    vals = data[:,1].astype(np.double)
    #print(vals<VOLTAGE_THRESHOLD)
    



    #with np.errstate(invalid='ignore'):
    #indx_less = np.argwhere(vals<VOLTAGE_THRESHOLD)
    
    
    #l=indx_less
    #result= np.split(l, np.where(np.diff(l,axis=0)>1)[0]+1)

    #print('Number of power outages = {}'.format(len(indx_less)))
  
    
    #print('Number of power outages = {}'.format(sum(k for k,v in groupby(vals<VOLTAGE_THRESHOLD))))
    
    print('Number of power outages = {}'.format(np.sum(np.diff(np.concatenate([[0],vals<VOLTAGE_THRESHOLD,[0]]))>0)))
    
    client.close()
    
    #return

if __name__ == '__main__':
    
    power_kgo()
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   #График зависимости напряжения от времени
#plt.plot(dates,vals)
#plt.xticks(rotation=25)
#plt.grid()
#plt.ylabel('Voltage')
#plt.xlabel('Data')
#plt.title('')
#plt.tick_params(axis='x', which='both', labelsize=8, direction = 'in')
#plt.tick_params(axis='y', which='both', labelsize=8, direction = 'in')
#plt.title('Voltage vs data')
#plt.show()
