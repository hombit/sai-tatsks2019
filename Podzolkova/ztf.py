from __future__ import unicode_literals
import requests
import numpy as np
from io import BytesIO
from astropy.io.votable import parse_single_table
from astropy.table import Table
import sys

def create_table(bandname, coord):
    response = requests.get('https://irsa.ipac.caltech.edu/cgi-bin/ZTF/nph_light_curves?POS=CIRCLE {0[0]} {0[1]} 0.0014&BANDNAME={1[0]}'.format(coord, bandname))
    if response.status_code == 200:
        print('OK')
        res = response.content
        obj = BytesIO(res)
        table = parse_single_table(obj)
        data = Table(table.array) #Полученная кривая блеска
        return(data)
    else:
        print('err: ' + str(response.status_code))
            
def calc_mean(data):    
    if (len(data) != 0): #Может не быть объекта по заданным координатам
        objects = np.unique(np.array(data['oid'])) #Cписок ID всех объектов
        mag = np.array(data['mag']) #Нужные столбцы
        magerr = np.array(data['magerr'])
        for k in objects: #Отсеиваем объекты со слишком малым числом точек по ID
            ind_start = np.where(np.array(data['oid']) == k)[0][0] #Начало и конец соответствующих одному объекту измерений
            ind_fin = np.where(np.array(data['oid']) == k)[0][-1]
            d_array = np.where(data['oid'] == k)[0] #Список индексов
            if ind_fin - ind_start < 25: #Удаляем
                mag = np.delete(mag, d_array)
                magerr = np.delete(magerr, d_array)   
        b_mag = np.sum(mag/((magerr)**2))/np.sum(1/((magerr)**2)) #Считаем среднее
        err = np.sqrt(1/(np.sum(1/((magerr)**2))))
        return(b_mag, err)
    else:
        print('Нет объекта с такими координатами!')
        
def calc(bandname, coord):
    table = create_table(bandname, coord)
    b_mag, err = calc_mean(table)
    return(b_mag, err)

def main():   
    if len(sys.argv) == 1:
        RA = 298.0025
        DEC = 29.87147
    elif len(sys.argv) == 2: 
        RA, DEC = sys.argv[1], sys.argv[2]
    coord = (RA, DEC)
    r_mag, rerr = calc('r', coord)
    g_mag, gerr = calc('g', coord)
    gr = g_mag - r_mag
    grerr = np.sqrt(gerr**2 + rerr**2)
    print('g - r: ' + str(gr) + ' +- ' + str(grerr))    
    
if __name__ == '__main__':
    main()
    



