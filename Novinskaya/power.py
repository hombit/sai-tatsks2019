from influxdb import InfluxDBClient
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#Пороговое значение напряжения
voltage_threshold=10


client = InfluxDBClient(host='eagle.sai.msu.ru',port=80,database='collectd')

#Минимальные значения напряжения в период с 30 ноября по 30 декабря
query=client.query("select min(value) from snmp_value where \"type\"='voltage' and \"type_instance\"='input' and time >= '2020-11-30T00:00:00Z' and time<= '2020-12-30T23:59:59Z' group by time(1h)",database='collectd')

#Временные метки, формат
data=np.array(query.raw['series'][0]['values'])
dates=pd.to_datetime(data[:,0])
vals=data[:,1].astype(np.double)


with np.errstate(invalid='ignore'):
    indx_less=np.argwhere(vals<voltage_threshold)


#График зависимсоти напряжения от времени
plt.plot(dates,vals)
plt.xticks(rotation=25)
plt.grid()
plt.ylabel('Voltage')
plt.xlabel('Data')
plt.title('')
plt.tick_params(axis='x', which='both', labelsize=8, direction = 'in')
plt.tick_params(axis='y', which='both', labelsize=8, direction = 'in')
plt.title('Voltage vs data')
plt.show()


print('Number of times when voltage was less than {} = {}'.format(voltage_threshold,len(indx_less)))

client.close()
